#!/usr/bin/env python3
"""Run fair-baseline and K2 ablation arms against an existing benchmark payload."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from collections.abc import Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from k2_java_rd_demo.codex_comparison import (  # noqa: E402
    CodexCliConfig,
    evidence_rows_from_answer_citations,
    grep_baseline_prompt,
    k2_mcp_prompt,
    k2_mcp_uncoached_prompt,
    run_codex_answer,
)
from k2_java_rd_demo.eval_cases import evaluation_cases  # noqa: E402
from k2_java_rd_demo.evaluation import EvalCase, EvalRun, compare_runs  # noqa: E402
from k2_java_rd_demo.k2_mcp_server import CORPUS_IDS, HYBRID_PROFILES, PROJECT_ID  # noqa: E402


MCP_SERVER = ROOT / "scripts" / "k2_java_rd_mcp_server.py"
DEFAULT_SOURCE_BASE = Path("/tmp/k2-java-rd-demo-sources")
NO_TOOL_FEATURES = (
    "features.shell_tool=false",
    "features.browser_use=false",
    "features.web_search_request=false",
)
LOCAL_RETRIEVAL_FEATURES = (
    "features.browser_use=false",
    "features.web_search_request=false",
)
ARM_NAMES = (
    "codex_grep_filesystem",
    "codex_with_k2_mcp_tuned",
    "codex_with_k2_mcp_no_skill",
    "codex_with_k2_mcp_filters_off",
)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.parallel < 1:
        raise SystemExit("--parallel must be at least 1")
    payload = json.loads(args.scorecard_json.read_text(encoding="utf-8"))
    cases = _selected_cases(payload, suite=args.suite, max_cases=args.max_cases, case_ids=args.case_id)
    if not cases:
        raise SystemExit("no cases selected")

    arms = tuple(dict.fromkeys(args.arm or ARM_NAMES))
    if not args.execute:
        print(
            json.dumps(
                {
                    "mode": "dry-run",
                    "case_count": len(cases),
                    "cases": [case.case_id for case in cases],
                    "arms": arms,
                    "model": args.model,
                    "source_base": str(args.source_base),
                    "flink_root": str(_flink_root(args)),
                    "kafka_root": str(_kafka_root(args)),
                    "note": "pass --execute to run extension arms",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    _validate_sources(args, arms)
    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ-extension-arms")
    out_dir = (args.out_dir or args.scorecard_json.parent / "extension-runs") / run_id
    prompts_dir = out_dir / "prompts"
    answers_dir = out_dir / "answers"
    events_dir = out_dir / "events"
    mcp_logs_dir = out_dir / "mcp"
    out_dir.mkdir(parents=True, exist_ok=True)

    results_by_case: dict[str, dict[str, Any]] = {}
    if args.parallel == 1:
        for index, case in enumerate(cases, start=1):
            results_by_case[case.case_id] = _run_case(
                case,
                args=args,
                arms=arms,
                prompts_dir=prompts_dir,
                answers_dir=answers_dir,
                events_dir=events_dir,
                mcp_logs_dir=mcp_logs_dir,
            )
            print(f"[{index}/{len(cases)}] completed {case.case_id}", file=sys.stderr, flush=True)
    else:
        with ThreadPoolExecutor(max_workers=args.parallel) as executor:
            futures = {
                executor.submit(
                    _run_case,
                    case,
                    args=args,
                    arms=arms,
                    prompts_dir=prompts_dir,
                    answers_dir=answers_dir,
                    events_dir=events_dir,
                    mcp_logs_dir=mcp_logs_dir,
                ): case
                for case in cases
            }
            completed = 0
            for future in as_completed(futures):
                case = futures[future]
                results_by_case[case.case_id] = future.result()
                completed += 1
                print(f"[{completed}/{len(cases)}] completed {case.case_id}", file=sys.stderr, flush=True)

    extension_payload = _build_payload(
        base_payload=payload,
        cases=cases,
        results_by_case=results_by_case,
        arms=arms,
        args=args,
        run_id=run_id,
    )
    result_path = out_dir / "extension-scorecard.json"
    report_path = out_dir / "extension-report.md"
    _write_text(result_path, json.dumps(extension_payload, indent=2, sort_keys=True))
    _write_text(report_path, _render_report(extension_payload))
    print(
        json.dumps(
            {
                "result_path": str(result_path),
                "report_path": str(report_path),
                "scorecard": extension_payload["scorecard"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _run_case(
    case: EvalCase,
    *,
    args: argparse.Namespace,
    arms: Sequence[str],
    prompts_dir: Path,
    answers_dir: Path,
    events_dir: Path,
    mcp_logs_dir: Path,
) -> dict[str, Any]:
    result: dict[str, Any] = {"answers": {}, "rows": {}, "tool_counts": {}}
    if "codex_grep_filesystem" in arms:
        prompt = grep_baseline_prompt(
            case,
            flink_root=str(_flink_root(args)),
            kafka_root=str(_kafka_root(args)),
        )
        config = CodexCliConfig(
            model=args.model,
            timeout_s=args.codex_timeout_s,
            cwd=str(args.source_base),
            config_overrides=LOCAL_RETRIEVAL_FEATURES,
            json_events_path=events_dir / f"{case.case_id}.codex-grep.jsonl",
        )
        answer = run_codex_answer(
            prompt,
            answers_dir / f"{case.case_id}.codex-grep.md",
            config,
        )
        _write_text(prompts_dir / f"{case.case_id}.codex-grep.txt", prompt)
        result["answers"]["codex_grep_filesystem"] = answer
        result["rows"]["codex_grep_filesystem"] = evidence_rows_from_answer_citations(case, answer)
        result["tool_counts"]["codex_grep_filesystem"] = {"shell_or_file_access": 1}

    if "codex_with_k2_mcp_no_skill" in arms:
        answer, rows, tool_counts, prompt = _run_k2_arm(
            case,
            args=args,
            prompt_text=k2_mcp_uncoached_prompt(case),
            arm_name="codex_with_k2_mcp_no_skill",
            mcp_logs_dir=mcp_logs_dir,
            answers_dir=answers_dir,
            events_dir=events_dir,
            disable_metadata_filters=False,
        )
        _write_text(prompts_dir / f"{case.case_id}.k2-no-skill.txt", prompt)
        result["answers"]["codex_with_k2_mcp_no_skill"] = answer
        result["rows"]["codex_with_k2_mcp_no_skill"] = rows
        result["tool_counts"]["codex_with_k2_mcp_no_skill"] = tool_counts

    if "codex_with_k2_mcp_tuned" in arms:
        answer, rows, tool_counts, prompt = _run_k2_arm(
            case,
            args=args,
            prompt_text=k2_mcp_prompt(case),
            arm_name="codex_with_k2_mcp_tuned",
            mcp_logs_dir=mcp_logs_dir,
            answers_dir=answers_dir,
            events_dir=events_dir,
            disable_metadata_filters=False,
        )
        _write_text(prompts_dir / f"{case.case_id}.k2-tuned.txt", prompt)
        result["answers"]["codex_with_k2_mcp_tuned"] = answer
        result["rows"]["codex_with_k2_mcp_tuned"] = rows
        result["tool_counts"]["codex_with_k2_mcp_tuned"] = tool_counts

    if "codex_with_k2_mcp_filters_off" in arms:
        answer, rows, tool_counts, prompt = _run_k2_arm(
            case,
            args=args,
            prompt_text=k2_mcp_prompt(case),
            arm_name="codex_with_k2_mcp_filters_off",
            mcp_logs_dir=mcp_logs_dir,
            answers_dir=answers_dir,
            events_dir=events_dir,
            disable_metadata_filters=True,
        )
        _write_text(prompts_dir / f"{case.case_id}.k2-filters-off.txt", prompt)
        result["answers"]["codex_with_k2_mcp_filters_off"] = answer
        result["rows"]["codex_with_k2_mcp_filters_off"] = rows
        result["tool_counts"]["codex_with_k2_mcp_filters_off"] = tool_counts
    return result


def _run_k2_arm(
    case: EvalCase,
    *,
    args: argparse.Namespace,
    prompt_text: str,
    arm_name: str,
    mcp_logs_dir: Path,
    answers_dir: Path,
    events_dir: Path,
    disable_metadata_filters: bool,
) -> tuple[str, list[dict[str, Any]], dict[str, int], str]:
    mcp_log_path = mcp_logs_dir / f"{case.case_id}.{arm_name}.jsonl"
    event_path = events_dir / f"{case.case_id}.{arm_name}.jsonl"
    mcp_config = CodexCliConfig(
        model=args.model,
        timeout_s=args.codex_timeout_s,
        config_overrides=(
            *NO_TOOL_FEATURES,
            f'mcp_servers.k2-java-rd.command="{MCP_SERVER}"',
            f'mcp_servers.k2-java-rd.env.K2_MCP_BACKEND="{args.mcp_backend}"',
            f'mcp_servers.k2-java-rd.env.K2_MCP_NAMESPACE="{args.namespace}"',
            f'mcp_servers.k2-java-rd.env.K2_MCP_DEPLOYMENT="{args.deployment}"',
            f'mcp_servers.k2-java-rd.env.K2_MCP_LOG_PATH="{mcp_log_path}"',
            f'mcp_servers.k2-java-rd.env.K2_MCP_CASE_ID="{case.case_id}"',
            f'mcp_servers.k2-java-rd.env.K2_MCP_RETRIEVAL_PROFILE="{args.retrieval_profile}"',
            f'mcp_servers.k2-java-rd.env.K2_MCP_SOURCE_BASE="{args.source_base}"',
            (
                "mcp_servers.k2-java-rd.env.K2_MCP_DISABLE_METADATA_FILTERS="
                f'"{str(disable_metadata_filters).lower()}"'
            ),
            'mcp_servers.k2-java-rd.env_vars=["K2_API_KEY"]',
            *_api_host_override(args.api_host),
            "mcp_servers.k2-java-rd.startup_timeout_sec=60",
            "mcp_servers.k2-java-rd.tool_timeout_sec=240",
        ),
        dangerously_bypass_approvals_and_sandbox=True,
        json_events_path=event_path,
    )
    answer = run_codex_answer(
        prompt_text,
        answers_dir / f"{case.case_id}.{arm_name}.md",
        mcp_config,
        env_allow={"K2_API_KEY"},
    )
    log_entries = _read_mcp_log(mcp_log_path)
    if not log_entries:
        log_entries = _read_mcp_entries_from_codex_events(event_path)
    return answer, _rows_from_log_entries(log_entries), dict(Counter(_tool_names(log_entries))), prompt_text


def _build_payload(
    *,
    base_payload: Mapping[str, Any],
    cases: Sequence[EvalCase],
    results_by_case: Mapping[str, Mapping[str, Any]],
    arms: Sequence[str],
    args: argparse.Namespace,
    run_id: str,
) -> dict[str, Any]:
    base_answers = base_payload.get("answers", {})
    base_rows = base_payload.get("rows_by_case", {})
    no_tool_answers = _answers_for_run(base_answers, "codex_without_k2")
    k2_answers = _answers_for_run(base_answers, "codex_with_k2_real_mcp")
    answers_by_run: dict[str, dict[str, str]] = {
        "codex_without_k2": {
            case.case_id: str(no_tool_answers.get(case.case_id, "")) for case in cases
        },
        "codex_with_k2_real_mcp": {
            case.case_id: str(k2_answers.get(case.case_id, "")) for case in cases
        },
    }
    rows_by_run: dict[str, dict[str, list[dict[str, Any]]]] = {
        "codex_without_k2": {case.case_id: [] for case in cases},
        "codex_with_k2_real_mcp": {
            case.case_id: list(_sequence_for_case(base_rows, case.case_id)) for case in cases
        },
    }
    tool_counts_by_run: dict[str, dict[str, dict[str, int]]] = {}
    for arm in arms:
        answers_by_run[arm] = {}
        rows_by_run[arm] = {}
        tool_counts_by_run[arm] = {}
        for case in cases:
            case_result = results_by_case.get(case.case_id, {})
            answers_by_run[arm][case.case_id] = str(
                case_result.get("answers", {}).get(arm, "")
            )
            rows_by_run[arm][case.case_id] = list(case_result.get("rows", {}).get(arm, []))
            tool_counts_by_run[arm][case.case_id] = dict(
                case_result.get("tool_counts", {}).get(arm, {})
            )

    run_order = [
        "codex_without_k2",
        *(arm for arm in arms if arm in answers_by_run),
        "codex_with_k2_real_mcp",
    ]
    scorecard = compare_runs(
        cases,
        [
            EvalRun(
                name=run_name,
                results_by_case=rows_by_run[run_name],
                answers_by_case=answers_by_run[run_name],
            )
            for run_name in run_order
        ],
    )
    return {
        "run_id": run_id,
        "generated_at": datetime.now(UTC).isoformat(),
        "method": "codex_extension_arms_for_fair_baseline_and_k2_ablations",
        "base_scorecard_path": str(args.scorecard_json),
        "project_id": args.project_id,
        "corpus_ids": CORPUS_IDS,
        "retrieval_profile": args.retrieval_profile,
        "retrieval_profiles": HYBRID_PROFILES,
        "source_roots": {
            "flink": str(_flink_root(args)),
            "kafka": str(_kafka_root(args)),
        },
        "cases": [case.to_dict() for case in cases],
        "answers": answers_by_run,
        "rows_by_run": rows_by_run,
        "tool_counts_by_run": tool_counts_by_run,
        "scorecard": scorecard,
    }


def _render_report(payload: Mapping[str, Any]) -> str:
    scorecard = payload["scorecard"]
    lines = [
        "# Extended Benchmark Arms",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        "## Summary",
        "",
        f"- Cases: `{scorecard['case_count']}`",
        f"- Source roots: `{json.dumps(payload['source_roots'], sort_keys=True)}`",
        "",
        "| Run | Combined | Retrieval | Answer | Safety | Passes |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for run in scorecard["runs"]:
        components = run.get("score_components", {})
        lines.append(
            "| {name} | `{combined}` | `{retrieval}` | `{answer}` | `{safety}` | `{passes}/{cases}` |".format(
                name=run["run_name"],
                combined=_format_score(components.get("combined_score")),
                retrieval=_format_score(components.get("retrieval_score")),
                answer=_format_score(components.get("answer_score")),
                safety=_format_score(components.get("safety_score")),
                passes=run.get("passed_cases"),
                cases=run.get("case_count"),
            )
        )
    lines.extend(
        [
            "",
            "## Pairwise Deltas vs No-Tool Baseline",
            "",
            "| Run | Combined Delta | Retrieval Delta | Answer Delta |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for comparison in scorecard.get("comparisons", []):
        deltas = comparison.get("score_component_deltas_vs_baseline", {})
        lines.append(
            "| {name} | `{combined}` | `{retrieval}` | `{answer}` |".format(
                name=comparison["run_name"],
                combined=_format_score(deltas.get("combined_score")),
                retrieval=_format_score(deltas.get("retrieval_score")),
                answer=_format_score(deltas.get("answer_score")),
            )
        )
    lines.extend(["", "## Per-Case Results", ""])
    by_run = {
        run["run_name"]: {case["case_id"]: case for case in run.get("cases", [])}
        for run in scorecard["runs"]
    }
    for case in payload["cases"]:
        case_id = case["case_id"]
        lines.extend([f"### {case['title']} (`{case_id}`)", ""])
        for run_name, cases_by_id in by_run.items():
            case_score = cases_by_id.get(case_id, {})
            breakdown = case_score.get("score_breakdown", {})
            lines.append(
                "- `{run}`: combined `{combined}`, retrieval `{retrieval}`, answer `{answer}`, passed `{passed}`, results `{results}`".format(
                    run=run_name,
                    combined=_format_score(case_score.get("score")),
                    retrieval=_format_score(breakdown.get("retrieval_score")),
                    answer=_format_score(breakdown.get("answer_score")),
                    passed=str(case_score.get("passed")).lower(),
                    results=case_score.get("result_count"),
                )
            )
        lines.append("")
    return "\n".join(lines)


def _selected_cases(
    payload: Mapping[str, Any],
    *,
    suite: str,
    max_cases: int | None,
    case_ids: Sequence[str],
) -> tuple[EvalCase, ...]:
    available = {case.case_id: case for case in evaluation_cases(suite=suite, include_kafka=True)}
    if case_ids:
        ordered_ids = list(case_ids)
    else:
        ordered_ids = [
            str(case["case_id"])
            for case in payload.get("cases", [])
            if isinstance(case, Mapping) and case.get("case_id")
        ]
    selected = [available[case_id] for case_id in ordered_ids if case_id in available]
    if max_cases:
        selected = selected[:max_cases]
    return tuple(selected)


def _validate_sources(args: argparse.Namespace, arms: Sequence[str]) -> None:
    if "codex_grep_filesystem" not in arms:
        return
    missing = [path for path in (_flink_root(args), _kafka_root(args)) if not path.exists()]
    if missing:
        formatted = ", ".join(str(path) for path in missing)
        raise SystemExit(f"missing source checkout(s): {formatted}")


def _flink_root(args: argparse.Namespace) -> Path:
    return args.flink_root or args.source_base / "apache-flink-release-2.2.0"


def _kafka_root(args: argparse.Namespace) -> Path:
    return args.kafka_root or args.source_base / "apache-kafka-4.2"


def _answers_for_run(source: Any, run_name: str) -> Mapping[str, Any]:
    if not isinstance(source, Mapping):
        return {}
    answers = source.get(run_name)
    return answers if isinstance(answers, Mapping) else {}


def _sequence_for_case(source: Any, case_id: str) -> Sequence[Any]:
    if not isinstance(source, Mapping):
        return ()
    rows = source.get(case_id)
    if isinstance(rows, Sequence) and not isinstance(rows, (str, bytes)):
        return rows
    return ()


def _read_mcp_log(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    entries = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                entries.append(json.loads(line))
    return entries


def _read_mcp_entries_from_codex_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    entries: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            event = json.loads(line)
            item = event.get("item")
            if not isinstance(item, Mapping) or item.get("type") != "mcp_tool_call":
                continue
            result = item.get("result")
            if not isinstance(result, Mapping):
                continue
            payload = _mcp_payload_from_result(result)
            if not payload:
                continue
            entries.append(
                {
                    "tool_name": item.get("tool"),
                    "arguments": item.get("arguments") if isinstance(item.get("arguments"), Mapping) else {},
                    "payload": payload,
                }
            )
    return entries


def _mcp_payload_from_result(result: Mapping[str, Any]) -> dict[str, Any] | None:
    content = result.get("content")
    if not isinstance(content, Sequence) or isinstance(content, (str, bytes)):
        return None
    for part in content:
        if not isinstance(part, Mapping):
            continue
        text = part.get("text")
        if not isinstance(text, str) or not text.strip():
            continue
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, Mapping):
            return dict(parsed)
    return None


def _rows_from_log_entries(entries: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for entry in entries:
        payload = entry.get("payload")
        if not isinstance(payload, Mapping):
            continue
        for row in _payload_rows(payload):
            metadata = dict(row.get("metadata") or {})
            normalized = dict(row)
            normalized["raw_text"] = row.get("raw_text") or row.get("text") or ""
            normalized["metadata"] = metadata
            key = (
                str(normalized.get("source_uri") or ""),
                str(metadata.get("source_kind") or normalized.get("source_kind") or ""),
                str(metadata.get("path") or normalized.get("path") or ""),
            )
            if key in seen:
                continue
            seen.add(key)
            rows.append(normalized)
    return rows


def _payload_rows(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    direct_rows = payload.get("results")
    if isinstance(direct_rows, list) and direct_rows:
        return [dict(row) for row in direct_rows if isinstance(row, Mapping)]
    rows: list[dict[str, Any]] = []
    searches = payload.get("searches")
    if isinstance(searches, list):
        for search in searches:
            if not isinstance(search, Mapping):
                continue
            search_rows = search.get("results")
            if isinstance(search_rows, list):
                rows.extend(dict(row) for row in search_rows if isinstance(row, Mapping))
    return rows


def _tool_names(entries: Sequence[Mapping[str, Any]]) -> list[str]:
    return [str(entry["tool_name"]) for entry in entries if isinstance(entry.get("tool_name"), str)]


def _api_host_override(api_host: str | None) -> tuple[str, ...]:
    return (f'mcp_servers.k2-java-rd.env.K2_API_HOST="{api_host}"',) if api_host else ()


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _format_score(value: Any) -> str:
    if isinstance(value, (int, float)):
        return f"{float(value):.6f}".rstrip("0").rstrip(".")
    return ""


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scorecard_json", type=Path)
    parser.add_argument("--arm", action="append", choices=ARM_NAMES)
    parser.add_argument("--source-base", type=Path, default=DEFAULT_SOURCE_BASE)
    parser.add_argument("--flink-root", type=Path)
    parser.add_argument("--kafka-root", type=Path)
    parser.add_argument("--namespace", default="k2-mvp")
    parser.add_argument("--deployment", default="deploy/k2-mvp-api-internal")
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--mcp-backend", choices=["sdk", "kubectl", "auto"], default="sdk")
    parser.add_argument("--api-host")
    parser.add_argument("--retrieval-profile", default="java_exact", choices=sorted(HYBRID_PROFILES))
    parser.add_argument("--model", default="gpt-5.4-mini")
    parser.add_argument("--codex-timeout-s", type=int, default=900)
    parser.add_argument("--max-cases", type=int)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--parallel", type=int, default=1)
    parser.add_argument("--suite", choices=["demo", "benchmark"], default="benchmark")
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--execute", action="store_true")
    return parser


if __name__ == "__main__":
    raise SystemExit(main())
