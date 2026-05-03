#!/usr/bin/env python3
"""Run Codex without K2 vs Codex with the real K2 stdio MCP server."""

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
    baseline_prompt,
    build_answer_scorecard,
    k2_mcp_prompt,
    run_codex_answer,
)
from k2_java_rd_demo.eval_cases import evaluation_cases  # noqa: E402
from k2_java_rd_demo.evaluation import EvalCase  # noqa: E402
from k2_java_rd_demo.k2_mcp_server import CORPUS_IDS, HYBRID_PROFILES, PROJECT_ID  # noqa: E402
from k2_java_rd_demo.question_stats import write_question_stats  # noqa: E402


MCP_SERVER = ROOT / "scripts" / "k2_java_rd_mcp_server.py"
DEFAULT_SOURCE_BASE = Path("/tmp/k2-java-rd-demo-sources")
NO_TOOL_FEATURES = (
    "features.shell_tool=false",
    "features.browser_use=false",
    "features.web_search_request=false",
)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.parallel < 1:
        raise SystemExit("--parallel must be at least 1")
    selected_cases = evaluation_cases(suite=args.suite, include_kafka=True)
    if args.case_id:
        wanted = set(args.case_id)
        selected_cases = tuple(case for case in selected_cases if case.case_id in wanted)
    if args.max_cases:
        selected_cases = selected_cases[: args.max_cases]
    if not selected_cases:
        raise SystemExit("no eval cases selected")

    if not args.execute:
        print(
            json.dumps(
                {
                    "mode": "dry-run",
                    "case_count": len(selected_cases),
                    "cases": [case.case_id for case in selected_cases],
                    "model": args.model,
                    "mcp_backend": args.mcp_backend,
                    "retrieval_profile": args.retrieval_profile,
                    "source_base": str(args.source_base),
                    "project_id": args.project_id,
                    "parallel": args.parallel,
                    "note": "pass --execute to run live Codex/MCP comparison",
                },
                indent=2,
            )
        )
        return 0

    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ-real-mcp")
    out_dir = args.out_dir / run_id
    prompts_dir = out_dir / "prompts"
    answers_dir = out_dir / "answers"
    events_dir = out_dir / "events"
    mcp_logs_dir = out_dir / "mcp"
    out_dir.mkdir(parents=True, exist_ok=True)

    baseline_config = CodexCliConfig(
        model=args.model,
        timeout_s=args.codex_timeout_s,
        config_overrides=NO_TOOL_FEATURES,
    )
    baseline_answers: dict[str, str] = {}
    k2_answers: dict[str, str] = {}
    k2_rows_by_case: dict[str, list[dict[str, Any]]] = {}
    tool_counts_by_case: dict[str, dict[str, int]] = {}

    if args.parallel == 1:
        for index, case in enumerate(selected_cases, start=1):
            result = _run_case(
                case,
                args=args,
                baseline_config=baseline_config,
                prompts_dir=prompts_dir,
                answers_dir=answers_dir,
                events_dir=events_dir,
                mcp_logs_dir=mcp_logs_dir,
            )
            _store_case_result(
                result,
                baseline_answers=baseline_answers,
                k2_answers=k2_answers,
                k2_rows_by_case=k2_rows_by_case,
                tool_counts_by_case=tool_counts_by_case,
            )
            print(
                f"[{index}/{len(selected_cases)}] completed {case.case_id}",
                file=sys.stderr,
                flush=True,
            )
    else:
        with ThreadPoolExecutor(max_workers=args.parallel) as executor:
            futures = {
                executor.submit(
                    _run_case,
                    case,
                    args=args,
                    baseline_config=baseline_config,
                    prompts_dir=prompts_dir,
                    answers_dir=answers_dir,
                    events_dir=events_dir,
                    mcp_logs_dir=mcp_logs_dir,
                ): case
                for case in selected_cases
            }
            completed = 0
            for future in as_completed(futures):
                case = futures[future]
                result = future.result()
                _store_case_result(
                    result,
                    baseline_answers=baseline_answers,
                    k2_answers=k2_answers,
                    k2_rows_by_case=k2_rows_by_case,
                    tool_counts_by_case=tool_counts_by_case,
                )
                completed += 1
                print(
                    f"[{completed}/{len(selected_cases)}] completed {case.case_id}",
                    file=sys.stderr,
                    flush=True,
                )

    scorecard = build_answer_scorecard(
        selected_cases,
        baseline_answers=baseline_answers,
        k2_rows_by_case=k2_rows_by_case,
        k2_answers=k2_answers,
        k2_run_name="codex_with_k2_real_mcp",
    )
    payload = {
        "run_id": run_id,
        "generated_at": datetime.now(UTC).isoformat(),
        "method": "codex_exec_without_k2_vs_codex_exec_with_real_k2_stdio_mcp",
        "project_id": args.project_id,
        "corpus_ids": CORPUS_IDS,
        "retrieval_profile": args.retrieval_profile,
        "retrieval_profiles": HYBRID_PROFILES,
        "mcp_server": str(MCP_SERVER),
        "mcp_backend": args.mcp_backend,
        "cases": [case.to_dict() for case in selected_cases],
        "tool_counts_by_case": tool_counts_by_case,
        "rows_by_case": k2_rows_by_case,
        "answers": {
            "codex_without_k2": baseline_answers,
            "codex_with_k2_real_mcp": k2_answers,
        },
        "scorecard": scorecard,
    }
    result_path = out_dir / "scorecard.json"
    report_path = out_dir / "report.md"
    _write_text(result_path, json.dumps(payload, indent=2, sort_keys=True))
    _write_text(report_path, _render_report(payload))
    stats_paths = write_question_stats(payload, out_dir=out_dir)

    print(
        json.dumps(
            {
                "result_path": str(result_path),
                "report_path": str(report_path),
                "stats_paths": {name: str(path) for name, path in stats_paths.items()},
                "scorecard": scorecard,
            },
            indent=2,
        )
    )
    return 0


def _run_case(
    case: EvalCase,
    *,
    args: argparse.Namespace,
    baseline_config: CodexCliConfig,
    prompts_dir: Path,
    answers_dir: Path,
    events_dir: Path,
    mcp_logs_dir: Path,
) -> dict[str, Any]:
    baseline_prompt_text = baseline_prompt(case)
    baseline_answer = run_codex_answer(
        baseline_prompt_text,
        answers_dir / f"{case.case_id}.without-k2.md",
        baseline_config,
    )
    _write_text(prompts_dir / f"{case.case_id}.without-k2.txt", baseline_prompt_text)

    mcp_log_path = mcp_logs_dir / f"{case.case_id}.jsonl"
    real_mcp_prompt = k2_mcp_prompt(case)
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
            'mcp_servers.k2-java-rd.env_vars=["K2_API_KEY"]',
            *_api_host_override(args.api_host),
            "mcp_servers.k2-java-rd.startup_timeout_sec=60",
            "mcp_servers.k2-java-rd.tool_timeout_sec=240",
        ),
        dangerously_bypass_approvals_and_sandbox=True,
        json_events_path=events_dir / f"{case.case_id}.with-k2-real-mcp.jsonl",
    )
    k2_answer = run_codex_answer(
        real_mcp_prompt,
        answers_dir / f"{case.case_id}.with-k2-real-mcp.md",
        mcp_config,
        env_allow={"K2_API_KEY"},
    )
    _write_text(prompts_dir / f"{case.case_id}.with-k2-real-mcp.txt", real_mcp_prompt)
    log_entries = _read_mcp_log(mcp_log_path)
    return {
        "case_id": case.case_id,
        "baseline_answer": baseline_answer,
        "k2_answer": k2_answer,
        "k2_rows": _rows_from_log_entries(log_entries),
        "tool_counts": dict(Counter(_tool_names(log_entries))),
    }


def _store_case_result(
    result: Mapping[str, Any],
    *,
    baseline_answers: dict[str, str],
    k2_answers: dict[str, str],
    k2_rows_by_case: dict[str, list[dict[str, Any]]],
    tool_counts_by_case: dict[str, dict[str, int]],
) -> None:
    case_id = str(result["case_id"])
    baseline_answers[case_id] = str(result["baseline_answer"])
    k2_answers[case_id] = str(result["k2_answer"])
    k2_rows_by_case[case_id] = list(result["k2_rows"])
    tool_counts_by_case[case_id] = dict(result["tool_counts"])


def _read_mcp_log(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    entries = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                entries.append(json.loads(line))
    return entries


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
    names = []
    for entry in entries:
        name = entry.get("tool_name")
        if isinstance(name, str) and name:
            names.append(name)
    return names


def _render_report(payload: Mapping[str, Any]) -> str:
    scorecard = payload["scorecard"]
    runs = {run["run_name"]: run for run in scorecard["runs"]}
    baseline = runs["codex_without_k2"]
    k2 = runs["codex_with_k2_real_mcp"]
    comparison = scorecard["comparisons"][0]
    answer_counts = _answer_counts(payload)
    lines = [
        "# Codex With Real K2 MCP vs Without K2 E2E Comparison",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        "## Summary",
        "",
        f"- Cases: `{scorecard['case_count']}`",
        f"- Codex without K2 answers generated: `{answer_counts.get('codex_without_k2', 0)}`",
        f"- Codex without K2: {_score_component_summary(baseline)}; passed cases: `{baseline['passed_cases']}`",
        f"- Codex with real K2 MCP answers generated: `{answer_counts.get('codex_with_k2_real_mcp', 0)}`",
        f"- Codex with real K2 MCP: {_score_component_summary(k2)}; passed cases: `{k2['passed_cases']}`",
        f"- Score delta: `{comparison['score_delta_vs_baseline']}`",
        f"- Retrieval score delta: `{_component_delta(comparison, 'retrieval_score')}`",
        f"- Answer score delta: `{_component_delta(comparison, 'answer_score')}`",
        "",
        "`passed_cases` is an evidence-grounding threshold, not an answer-count metric. "
        "A run can generate an answer and still fail when it does not retrieve or cite the "
        "required version-pinned docs, source files, and tests.",
        "",
        "## Method",
        "",
        "- Baseline used `codex exec` with no K2 MCP server, no shell tool, no browser tool, and no web-search feature.",
        "- Assisted run used `codex exec` with a real local stdio MCP server named `k2-java-rd`.",
        f"- The K2 MCP server used the `{payload['mcp_backend']}` backend against the demo corpora and logged every tool payload used for scoring.",
        "- Non-interactive Codex requires `--dangerously-bypass-approvals-and-sandbox` for external MCP tool calls; shell, browser, and web-search features were disabled in the same run.",
        "",
        "## Retrieval Profiles",
        "",
        "```json",
        json.dumps(payload["retrieval_profiles"], indent=2, sort_keys=True),
        "```",
        "",
        "## Per-Case Results",
        "",
    ]
    by_case = {
        run["run_name"]: {case["case_id"]: case for case in run["cases"]}
        for run in scorecard["runs"]
    }
    tool_counts = payload["tool_counts_by_case"]
    for case in payload["cases"]:
        case_id = case["case_id"]
        b = by_case["codex_without_k2"][case_id]
        k = by_case["codex_with_k2_real_mcp"][case_id]
        lines.extend(
            [
                f"### {case['title']}",
                "",
                f"- Case ID: `{case_id}`",
                f"- Without K2: {_case_component_summary(b)}, passed `{b['passed']}`, results `{b['result_count']}`",
                f"- With real K2 MCP: {_case_component_summary(k)}, passed `{k['passed']}`, results `{k['result_count']}`",
                f"- MCP tool calls: `{json.dumps(tool_counts.get(case_id, {}), sort_keys=True)}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Demo Interpretation",
            "",
            "The real-MCP path demonstrates the customer-facing integration boundary: Codex calls a stdio MCP tool, the tool retrieves version-pinned evidence from K2, and the final answer cites exact docs, source classes, and neighboring tests. The baseline can give generic advice, but it cannot reliably name the same internal artifacts without the K2-backed tool call.",
            "",
        ]
    )
    return "\n".join(lines)


def _score_component_summary(run: Mapping[str, Any]) -> str:
    components = _run_score_components(run)
    return (
        f"combined `{_format_score(components.get('combined_score'))}`, "
        f"retrieval `{_format_score(components.get('retrieval_score'))}`, "
        f"answer `{_format_score(components.get('answer_score'))}`, "
        f"safety `{_format_score(components.get('safety_score'))}`"
    )


def _case_component_summary(case: Mapping[str, Any]) -> str:
    breakdown = case.get("score_breakdown")
    if not isinstance(breakdown, Mapping):
        breakdown = {}
    return (
        f"combined `{_format_score(case.get('score'))}`, "
        f"retrieval `{_format_score(breakdown.get('retrieval_score'))}`, "
        f"answer `{_format_score(breakdown.get('answer_score'))}`, "
        f"safety `{_format_score(breakdown.get('safety_score'))}`"
    )


def _run_score_components(run: Mapping[str, Any]) -> Mapping[str, Any]:
    components = run.get("score_components")
    if isinstance(components, Mapping):
        return components
    metric_averages = run.get("metric_averages")
    if not isinstance(metric_averages, Mapping):
        metric_averages = {}
    return {
        "combined_score": run.get("score"),
        "retrieval_score": metric_averages.get("retrieval_score_avg"),
        "answer_score": metric_averages.get("answer_score_avg"),
        "safety_score": metric_averages.get("hallucination_markers"),
    }


def _component_delta(comparison: Mapping[str, Any], component_name: str) -> str:
    deltas = comparison.get("score_component_deltas_vs_baseline")
    if isinstance(deltas, Mapping):
        return _format_score(deltas.get(component_name))
    metric_deltas = comparison.get("metric_deltas_vs_baseline")
    if isinstance(metric_deltas, Mapping):
        fallback_name = {
            "retrieval_score": "retrieval_score_avg",
            "answer_score": "answer_score_avg",
            "safety_score": "hallucination_markers",
        }.get(component_name, component_name)
        return _format_score(metric_deltas.get(fallback_name))
    return ""


def _format_score(value: Any) -> str:
    if isinstance(value, (int, float)):
        return f"{float(value):.6f}".rstrip("0").rstrip(".")
    return ""


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _answer_counts(payload: Mapping[str, Any]) -> dict[str, int]:
    answers = payload.get("answers")
    if not isinstance(answers, Mapping):
        return {}
    counts = {}
    for name, by_case in answers.items():
        if isinstance(by_case, Mapping):
            counts[str(name)] = sum(1 for answer in by_case.values() if str(answer).strip())
    return counts


def _api_host_override(api_host: str | None) -> tuple[str, ...]:
    return (f'mcp_servers.k2-java-rd.env.K2_API_HOST="{api_host}"',) if api_host else ()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--namespace", default="k2-mvp")
    parser.add_argument("--deployment", default="deploy/k2-mvp-api-internal")
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--source-base", type=Path, default=DEFAULT_SOURCE_BASE)
    parser.add_argument("--mcp-backend", choices=["sdk", "kubectl", "auto"], default="sdk")
    parser.add_argument("--api-host")
    parser.add_argument("--retrieval-profile", default="java_exact", choices=sorted(HYBRID_PROFILES))
    parser.add_argument("--model", default="gpt-5.4-mini")
    parser.add_argument("--codex-timeout-s", type=int, default=900)
    parser.add_argument("--max-cases", type=int)
    parser.add_argument("--case-id", action="append")
    parser.add_argument("--parallel", type=int, default=1)
    parser.add_argument("--suite", choices=["demo", "benchmark"], default="demo")
    parser.add_argument("--out-dir", type=Path, default=ROOT / ".eval-runs")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Required to run live Codex/MCP comparison. Without this flag the script prints "
        "the planned configuration and exits.",
    )
    return parser


if __name__ == "__main__":
    raise SystemExit(main())
