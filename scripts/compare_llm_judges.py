#!/usr/bin/env python3
"""Compare two blinded LLM-judge result files."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    left = json.loads(args.left.read_text(encoding="utf-8"))
    right = json.loads(args.right.read_text(encoding="utf-8"))
    scorecard = json.loads(args.scorecard.read_text(encoding="utf-8")) if args.scorecard else {}
    report = build_report(left, right, scorecard=scorecard)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report, encoding="utf-8")
    else:
        print(report)
    return 0


def build_report(
    left: Mapping[str, Any],
    right: Mapping[str, Any],
    *,
    scorecard: Mapping[str, Any] | None = None,
) -> str:
    left_name = _judge_name(left, default="judge_a")
    right_name = _judge_name(right, default="judge_b")
    left_by_case = _results_by_case(left)
    right_by_case = _results_by_case(right)
    shared_case_ids = sorted(set(left_by_case) & set(right_by_case))
    labels = sorted(
        {
            str(result.get("winner_run") or "tie")
            for case_id in shared_case_ids
            for result in (left_by_case[case_id], right_by_case[case_id])
        }
    )
    pairs = [
        (
            str(left_by_case[case_id].get("winner_run") or "tie"),
            str(right_by_case[case_id].get("winner_run") or "tie"),
        )
        for case_id in shared_case_ids
    ]
    agreement = _agreement(pairs)
    kappa = _cohens_kappa(pairs, labels=labels)
    left_counts = Counter(left_label for left_label, _ in pairs)
    right_counts = Counter(right_label for _, right_label in pairs)
    compared_runs = _compared_run_names(left, right)
    deterministic = _deterministic_case_scores(scorecard or {}, compared_runs)

    lines = [
        "# LLM Judge Family Comparison",
        "",
        f"Generated: `{datetime.now(UTC).isoformat()}`",
        "",
        "## Summary",
        "",
        f"- Shared cases: `{len(shared_case_ids)}`",
        f"- Left judge: `{left_name}`",
        f"- Right judge: `{right_name}`",
        f"- Simple agreement: `{agreement:.3f}`",
        f"- Cohen's kappa: `{kappa:.3f}`",
        "",
        "| Winner | Left count | Right count |",
        "| --- | ---: | ---: |",
    ]
    for label in labels:
        lines.append(f"| `{label}` | `{left_counts[label]}` | `{right_counts[label]}` |")

    disagreements = [
        case_id
        for case_id in shared_case_ids
        if left_by_case[case_id].get("winner_run") != right_by_case[case_id].get("winner_run")
    ]
    lines.extend(
        [
            "",
            "## Disagreements",
            "",
            f"- Disagreement count: `{len(disagreements)}`",
            "",
            "| Case | Left winner | Right winner | "
            f"Deterministic `{compared_runs[0]}` | Deterministic `{compared_runs[1]}` |",
            "| --- | --- | --- | ---: | ---: |",
        ]
    )
    for case_id in disagreements:
        scores = deterministic.get(case_id, {})
        lines.append(
            "| `{case}` | `{left}` | `{right}` | `{base}` | `{k2}` |".format(
                case=case_id,
                left=left_by_case[case_id].get("winner_run") or "tie",
                right=right_by_case[case_id].get("winner_run") or "tie",
                base=scores.get(compared_runs[0], ""),
                k2=scores.get(compared_runs[1], ""),
            )
        )
    lines.extend(
        [
            "",
            "Agreement is computed after each judge's randomized A/B labels are mapped back to "
            "run names. The judges still see answer fingerprints such as citations and file "
            "paths, so this is a second-family robustness check rather than full human-blind "
            "validation.",
        ]
    )
    return "\n".join(lines)


def _results_by_case(payload: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {
        str(result["case_id"]): result
        for result in payload.get("results", [])
        if isinstance(result, Mapping) and result.get("case_id")
    }


def _judge_name(payload: Mapping[str, Any], *, default: str) -> str:
    provider = payload.get("provider") or default
    model = payload.get("model")
    return f"{provider}:{model}" if model else str(provider)


def _compared_run_names(
    left: Mapping[str, Any],
    right: Mapping[str, Any],
) -> tuple[str, str]:
    for payload in (left, right):
        compared = payload.get("compared_runs")
        if isinstance(compared, Sequence) and not isinstance(compared, (str, bytes)):
            names = [str(name) for name in compared if name is not None]
            if len(names) >= 2:
                return (names[0], names[1])
    for payload in (left, right):
        for result in payload.get("results", []):
            if not isinstance(result, Mapping):
                continue
            scores = result.get("scores_by_run")
            if isinstance(scores, Mapping):
                names = sorted(str(name) for name in scores)
                if len(names) >= 2:
                    return (names[0], names[1])
    return ("run_a", "run_b")


def _agreement(pairs: Sequence[tuple[str, str]]) -> float:
    if not pairs:
        return 0.0
    return sum(left == right for left, right in pairs) / len(pairs)


def _cohens_kappa(pairs: Sequence[tuple[str, str]], *, labels: Sequence[str]) -> float:
    if not pairs:
        return 0.0
    observed = _agreement(pairs)
    left_counts = Counter(left for left, _ in pairs)
    right_counts = Counter(right for _, right in pairs)
    total = len(pairs)
    expected = sum(
        (left_counts[label] / total) * (right_counts[label] / total)
        for label in labels
    )
    if expected >= 1.0:
        return 1.0 if observed >= 1.0 else 0.0
    return (observed - expected) / (1 - expected)


def _deterministic_case_scores(
    scorecard_payload: Mapping[str, Any],
    run_names: Sequence[str],
) -> dict[str, dict[str, Any]]:
    scorecard = scorecard_payload.get("scorecard", scorecard_payload)
    if not isinstance(scorecard, Mapping):
        return {}
    runs = {
        run.get("run_name"): {
            case["case_id"]: case.get("score")
            for case in run.get("cases", [])
            if isinstance(case, Mapping) and case.get("case_id")
        }
        for run in scorecard.get("runs", [])
        if isinstance(run, Mapping)
    }
    selected = {run_name: runs.get(run_name, {}) for run_name in run_names}
    case_ids = set()
    for cases in selected.values():
        case_ids.update(cases)
    return {
        case_id: {
            run_name: selected.get(run_name, {}).get(case_id, "")
            for run_name in run_names
        }
        for case_id in case_ids
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--scorecard", type=Path)
    parser.add_argument("--out", type=Path)
    return parser


if __name__ == "__main__":
    raise SystemExit(main())
