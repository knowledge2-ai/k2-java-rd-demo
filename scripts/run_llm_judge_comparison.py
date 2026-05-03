#!/usr/bin/env python3
"""Run a blinded LLM-as-judge comparison over an existing scorecard."""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from k2_java_rd_demo.llm_judge import (  # noqa: E402
    ClaudeCliJudgeClient,
    CodexCliJudgeClient,
    HeuristicJudgeClient,
    OpenAIResponsesJudgeClient,
    build_judge_cases,
    build_judge_prompt,
    judge_case,
    render_judge_report,
    summarize_judge_results,
)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.parallel < 1:
        raise SystemExit("--parallel must be at least 1")
    if args.provider != "heuristic" and not args.execute:
        raise SystemExit("non-heuristic providers require --execute")

    scorecard_path = args.scorecard_json
    payload = json.loads(scorecard_path.read_text(encoding="utf-8"))
    cases = build_judge_cases(
        payload,
        seed=args.seed,
        baseline_run=args.baseline_run,
        candidate_run=args.candidate_run,
        include_evidence=args.include_evidence,
    )
    if args.case_id:
        wanted = set(args.case_id)
        cases = [case for case in cases if case.case_id in wanted]
    if args.max_cases:
        cases = cases[: args.max_cases]
    if not cases:
        raise SystemExit("no judge cases selected")

    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ-llm-judge")
    out_dir = (args.out_dir or scorecard_path.parent / "llm-judge-runs") / run_id
    prompts_dir = out_dir / "prompts"
    raw_dir = out_dir / "raw" if args.write_raw else None
    out_dir.mkdir(parents=True, exist_ok=True)

    client = _client(args)
    if args.write_prompts:
        for case in cases:
            _write_text(prompts_dir / f"{case.case_id}.txt", build_judge_prompt(case))

    results: list[dict[str, Any]] = []
    if args.parallel == 1:
        for index, case in enumerate(cases, start=1):
            result = _run_case(case, client=client, raw_dir=raw_dir)
            results.append(result)
            print(f"[{index}/{len(cases)}] judged {case.case_id}", file=sys.stderr, flush=True)
    else:
        with ThreadPoolExecutor(max_workers=args.parallel) as executor:
            futures = {
                executor.submit(_run_case, case, client=client, raw_dir=raw_dir): case
                for case in cases
            }
            completed = 0
            for future in as_completed(futures):
                case = futures[future]
                results.append(future.result())
                completed += 1
                print(f"[{completed}/{len(cases)}] judged {case.case_id}", file=sys.stderr, flush=True)

    results.sort(key=lambda result: [case.case_id for case in cases].index(result["case_id"]))
    judge_payload = {
        "run_id": run_id,
        "generated_at": datetime.now(UTC).isoformat(),
        "provider": args.provider,
        "model": args.model,
        "scorecard_path": str(scorecard_path),
        "seed": args.seed,
        "compared_runs": sorted(cases[0].label_to_run.values()),
        "method": "blinded_pairwise_llm_judge_secondary_metric",
        "answer_sanitization": "explicit_system_identity_terms_normalized",
        "evidence_mode": "retrieval_snippets_included" if args.include_evidence else "answer_only",
        "summary": summarize_judge_results(results),
        "results": results,
    }
    result_path = out_dir / "judge-results.json"
    report_path = out_dir / "judge-report.md"
    _write_text(result_path, json.dumps(judge_payload, indent=2, sort_keys=True))
    _write_text(report_path, render_judge_report(payload, judge_payload))
    print(
        json.dumps(
            {
                "result_path": str(result_path),
                "report_path": str(report_path),
                "summary": judge_payload["summary"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _run_case(case: Any, *, client: Any, raw_dir: Path | None) -> dict[str, Any]:
    raw_output_path = raw_dir / f"{case.case_id}.json" if raw_dir else None
    return judge_case(case, client, raw_output_path=raw_output_path)


def _client(args: argparse.Namespace) -> Any:
    if args.provider == "heuristic":
        return HeuristicJudgeClient()
    if args.provider == "codex-cli":
        return CodexCliJudgeClient(
            codex_bin=args.codex_bin,
            model=args.model,
            timeout_s=args.timeout_s,
        )
    if args.provider == "claude-cli":
        return ClaudeCliJudgeClient(
            claude_bin=args.claude_bin,
            model=args.model,
            timeout_s=args.timeout_s,
        )
    if args.provider == "openai":
        return OpenAIResponsesJudgeClient(
            model=args.model,
            timeout_s=args.timeout_s,
        )
    raise SystemExit(f"unsupported provider: {args.provider}")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scorecard_json", type=Path)
    parser.add_argument(
        "--provider",
        choices=("heuristic", "codex-cli", "claude-cli", "openai"),
        default="heuristic",
        help="Judge provider. heuristic is deterministic and offline; others require --execute.",
    )
    parser.add_argument("--model", default="gpt-5.4-mini")
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--claude-bin", default="claude")
    parser.add_argument("--timeout-s", type=int, default=600)
    parser.add_argument("--seed", default="k2-llm-judge-v1")
    parser.add_argument("--baseline-run")
    parser.add_argument("--candidate-run")
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--max-cases", type=int)
    parser.add_argument("--parallel", type=int, default=1)
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--write-prompts", action="store_true")
    parser.add_argument("--write-raw", action="store_true")
    parser.add_argument("--include-evidence", action="store_true")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Required for paid/live judge providers.",
    )
    return parser


if __name__ == "__main__":
    raise SystemExit(main())
