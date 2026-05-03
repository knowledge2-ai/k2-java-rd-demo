"""Per-question statistics for Codex/K2 benchmark scorecards."""

from __future__ import annotations

import argparse
import csv
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

METRIC_NAMES = (
    "artifact_matches",
    "source_kind_coverage",
    "module_hits",
    "api_surface_hits",
    "must_mention_coverage",
    "source_uri_coverage",
    "citation_coverage",
    "hallucination_markers",
)


def load_scorecard_payload(path: Path) -> dict[str, Any]:
    """Load a benchmark scorecard payload from disk."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def build_question_stats(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Build one deterministic statistics row per benchmark question."""

    scorecard = _scorecard(payload)
    runs = {str(run["run_name"]): run for run in scorecard.get("runs", [])}
    if not runs:
        raise ValueError("scorecard does not contain any runs")

    baseline_name = str(scorecard.get("baseline_run") or next(iter(runs)))
    k2_name = _comparison_run_name(scorecard, runs, baseline_name)
    baseline_run = runs[baseline_name]
    k2_run = runs[k2_name]
    baseline_cases = _cases_by_id(baseline_run)
    k2_cases = _cases_by_id(k2_run)
    catalog = _catalog_by_case_id(payload, scorecard)
    tool_counts_by_case = payload.get("tool_counts_by_case", {})
    rows_by_case = payload.get("rows_by_case", {})
    answers_by_run = payload.get("answers", {})

    stats = []
    for index, case_id in enumerate(_ordered_case_ids(catalog, baseline_cases, k2_cases), start=1):
        baseline_case = baseline_cases.get(case_id, {})
        k2_case = k2_cases.get(case_id, {})
        catalog_case = catalog.get(case_id, {})
        metric_scores = {
            metric_name: _metric_comparison(baseline_case, k2_case, metric_name)
            for metric_name in METRIC_NAMES
        }
        tool_counts = _mapping_for_case(tool_counts_by_case, case_id)
        k2_rows = _sequence_for_case(rows_by_case, case_id)
        baseline_score = _float_or_none(baseline_case.get("score"))
        k2_score = _float_or_none(k2_case.get("score"))
        baseline_components = _case_score_components(baseline_case)
        k2_components = _case_score_components(k2_case)
        baseline_answered = _has_answer(answers_by_run, baseline_name, case_id)
        k2_answered = _has_answer(answers_by_run, k2_name, case_id)
        stats.append(
            {
                "index": index,
                "case_id": case_id,
                "title": _first_string(
                    k2_case.get("title"),
                    baseline_case.get("title"),
                    catalog_case.get("title"),
                ),
                "question": _first_string(
                    k2_case.get("query"),
                    baseline_case.get("query"),
                    catalog_case.get("query"),
                ),
                "baseline_run": baseline_name,
                "k2_run": k2_name,
                "baseline_score": baseline_score,
                "k2_score": k2_score,
                "score_delta": _delta(k2_score, baseline_score),
                "baseline_score_components": baseline_components,
                "k2_score_components": k2_components,
                "score_component_deltas": _component_deltas(k2_components, baseline_components),
                "baseline_answered": baseline_answered,
                "k2_answered": k2_answered,
                "baseline_passed": bool(baseline_case.get("passed")),
                "k2_passed": bool(k2_case.get("passed")),
                "baseline_result_count": int(baseline_case.get("result_count") or 0),
                "k2_result_count": int(k2_case.get("result_count") or 0),
                "mcp_result_count": len(k2_rows),
                "mcp_tool_call_count": sum(
                    value for value in tool_counts.values() if isinstance(value, int)
                ),
                "mcp_tool_counts": dict(sorted(tool_counts.items())),
                "metric_scores": metric_scores,
                "baseline_missing": _missing_summary(baseline_case),
                "k2_missing": _missing_summary(k2_case),
            }
        )
    return stats


def write_question_stats(
    payload: Mapping[str, Any],
    *,
    out_dir: Path,
    csv_name: str = "per-question-stats.csv",
    md_name: str = "per-question-stats.md",
    json_name: str = "per-question-stats.json",
) -> dict[str, Path]:
    """Write per-question statistics as CSV, Markdown, and JSON."""

    out_dir.mkdir(parents=True, exist_ok=True)
    stats = build_question_stats(payload)
    paths = {
        "csv": out_dir / csv_name,
        "md": out_dir / md_name,
        "json": out_dir / json_name,
    }
    _write_csv(paths["csv"], stats)
    paths["md"].write_text(render_question_stats_markdown(payload, stats), encoding="utf-8")
    paths["json"].write_text(json.dumps(stats, indent=2, sort_keys=True), encoding="utf-8")
    return paths


def render_question_stats_markdown(
    payload: Mapping[str, Any],
    stats: Sequence[Mapping[str, Any]],
) -> str:
    """Render reviewer-friendly per-question benchmark statistics."""

    scorecard = _scorecard(payload)
    runs = {str(run["run_name"]): run for run in scorecard.get("runs", [])}
    baseline_name = str(scorecard.get("baseline_run") or next(iter(runs)))
    k2_name = _comparison_run_name(scorecard, runs, baseline_name)
    baseline = runs[baseline_name]
    k2 = runs[k2_name]
    improved = sum(1 for row in stats if _is_positive(row.get("score_delta")))
    regressed = sum(1 for row in stats if _is_negative(row.get("score_delta")))
    unchanged = len(stats) - improved - regressed
    baseline_answered = sum(1 for row in stats if row.get("baseline_answered"))
    k2_answered = sum(1 for row in stats if row.get("k2_answered"))

    lines = [
        "# Per-Question Benchmark Statistics",
        "",
        "## Aggregate Summary",
        "",
        f"- Cases: `{len(stats)}`",
        (
            f"- Baseline `{baseline_name}`: {_run_component_summary(baseline)}, "
            f"answered `{baseline_answered}/{len(stats)}`, "
            f"passed `{baseline.get('passed_cases')}/{baseline.get('case_count')}`"
        ),
        (
            f"- K2-assisted `{k2_name}`: {_run_component_summary(k2)}, "
            f"answered `{k2_answered}/{len(stats)}`, "
            f"passed `{k2.get('passed_cases')}/{k2.get('case_count')}`"
        ),
        "- `passed` means the answer cleared the deterministic evidence-grounding threshold; it is not an answer-count metric.",
        f"- Per-question score movement: improved `{improved}`, unchanged `{unchanged}`, regressed `{regressed}`",
        "",
        "## Summary Table",
        "",
        (
            "| # | Case ID | Question | Baseline C/R/A | K2 C/R/A | Delta C/R/A | Baseline pass | "
            "K2 pass | MCP calls | K2 evidence gaps |"
        ),
        "|---:|---|---|---:|---:|---:|---|---|---:|---|",
    ]
    for row in stats:
        lines.append(
            "| {index} | `{case_id}` | {question} | `{baseline_components}` | `{k2_components}` | "
            "`{component_deltas}` | `{baseline_passed}` | `{k2_passed}` | "
            "`{mcp_tool_call_count}` | {gaps} |".format(
                index=row["index"],
                case_id=_escape_table(str(row["case_id"])),
                question=_escape_table(_truncate(str(row["question"]), 150)),
                baseline_components=_compact_component_triplet(
                    row.get("baseline_score_components")
                ),
                k2_components=_compact_component_triplet(row.get("k2_score_components")),
                component_deltas=_compact_component_triplet(row.get("score_component_deltas")),
                baseline_passed=str(row.get("baseline_passed")).lower(),
                k2_passed=str(row.get("k2_passed")).lower(),
                mcp_tool_call_count=row.get("mcp_tool_call_count"),
                gaps=_escape_table(_gap_summary(row.get("k2_missing"))),
            )
        )

    lines.extend(["", "## Per-Question Details", ""])
    for row in stats:
        lines.extend(
            [
                f"### {row['index']}. {row['title']} (`{row['case_id']}`)",
                "",
                f"Question: {row['question']}",
                "",
                (
                    f"- Score components: baseline "
                    f"`{_component_summary(row.get('baseline_score_components'))}`, "
                    f"K2 `{_component_summary(row.get('k2_score_components'))}`, "
                    f"delta `{_component_summary(row.get('score_component_deltas'))}`"
                ),
                (
                    f"- Answer generated: baseline `{str(row.get('baseline_answered')).lower()}`, "
                    f"K2 `{str(row.get('k2_answered')).lower()}`"
                ),
                (
                    f"- Pass: baseline `{str(row.get('baseline_passed')).lower()}`, "
                    f"K2 `{str(row.get('k2_passed')).lower()}`"
                ),
                f"- MCP calls: `{json.dumps(row.get('mcp_tool_counts', {}), sort_keys=True)}`",
                f"- K2 metric scores: `{_metric_score_summary(row.get('metric_scores'), 'k2')}`",
                f"- Baseline metric scores: `{_metric_score_summary(row.get('metric_scores'), 'baseline')}`",
                f"- K2 evidence gaps: {_gap_summary(row.get('k2_missing'))}",
                f"- Baseline evidence gaps: {_gap_summary(row.get('baseline_missing'))}",
                "",
            ]
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    payload_path = args.scorecard_json.resolve()
    payload = load_scorecard_payload(payload_path)
    out_dir = args.out_dir.resolve() if args.out_dir else payload_path.parent
    paths = write_question_stats(payload, out_dir=out_dir)
    print(json.dumps({name: str(path) for name, path in paths.items()}, indent=2, sort_keys=True))
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scorecard_json", type=Path, help="Path to scorecard.json")
    parser.add_argument("--out-dir", type=Path, help="Directory for generated stats files")
    return parser


def _scorecard(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    nested = payload.get("scorecard")
    if isinstance(nested, Mapping):
        return nested
    return payload


def _comparison_run_name(
    scorecard: Mapping[str, Any],
    runs: Mapping[str, Mapping[str, Any]],
    baseline_name: str,
) -> str:
    comparisons = scorecard.get("comparisons")
    if isinstance(comparisons, Sequence) and not isinstance(comparisons, (str, bytes)):
        for comparison in comparisons:
            if isinstance(comparison, Mapping):
                run_name = comparison.get("run_name")
                if isinstance(run_name, str) and run_name in runs:
                    return run_name
    best_run = scorecard.get("best_run")
    if isinstance(best_run, str) and best_run in runs and best_run != baseline_name:
        return best_run
    for run_name in runs:
        if run_name != baseline_name:
            return run_name
    return baseline_name


def _catalog_by_case_id(
    payload: Mapping[str, Any],
    scorecard: Mapping[str, Any],
) -> dict[str, Mapping[str, Any]]:
    cases = payload.get("cases")
    if not isinstance(cases, Sequence) or isinstance(cases, (str, bytes)):
        cases = []
        for run in scorecard.get("runs", []):
            if isinstance(run, Mapping):
                cases.extend(run.get("cases", []))
    catalog = {}
    for case in cases:
        if isinstance(case, Mapping) and isinstance(case.get("case_id"), str):
            catalog[case["case_id"]] = case
    return catalog


def _cases_by_id(run: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    cases = run.get("cases")
    if not isinstance(cases, Sequence) or isinstance(cases, (str, bytes)):
        return {}
    return {
        case["case_id"]: case
        for case in cases
        if isinstance(case, Mapping) and isinstance(case.get("case_id"), str)
    }


def _ordered_case_ids(
    catalog: Mapping[str, Any],
    baseline_cases: Mapping[str, Any],
    k2_cases: Mapping[str, Any],
) -> list[str]:
    ordered = []
    for source in (catalog, k2_cases, baseline_cases):
        for case_id in source:
            if case_id not in ordered:
                ordered.append(case_id)
    return ordered


def _metric_comparison(
    baseline_case: Mapping[str, Any],
    k2_case: Mapping[str, Any],
    metric_name: str,
) -> dict[str, float | None]:
    baseline_score = _metric_score(baseline_case, metric_name)
    k2_score = _metric_score(k2_case, metric_name)
    return {
        "baseline": baseline_score,
        "k2": k2_score,
        "delta": _delta(k2_score, baseline_score),
    }


def _metric_score(case: Mapping[str, Any], metric_name: str) -> float | None:
    metrics = case.get("metrics")
    if not isinstance(metrics, Mapping):
        return None
    metric = metrics.get(metric_name)
    if not isinstance(metric, Mapping):
        return None
    return _float_or_none(metric.get("score"))


def _case_score_components(case: Mapping[str, Any]) -> dict[str, float | None]:
    breakdown = case.get("score_breakdown")
    return {
        "combined_score": _float_or_none(case.get("score")),
        "retrieval_score": _breakdown_score(breakdown, "retrieval_score"),
        "answer_score": _breakdown_score(breakdown, "answer_score"),
        "safety_score": _breakdown_score(breakdown, "safety_score"),
    }


def _breakdown_score(source: Any, component_name: str) -> float | None:
    if isinstance(source, Mapping):
        return _float_or_none(source.get(component_name))
    return None


def _component_deltas(
    left: Mapping[str, float | None],
    right: Mapping[str, float | None],
) -> dict[str, float | None]:
    return {name: _delta(left.get(name), right.get(name)) for name in left}


def _missing_summary(case: Mapping[str, Any]) -> dict[str, list[str]]:
    metrics = case.get("metrics")
    if not isinstance(metrics, Mapping):
        return {}
    return {
        "artifacts": _string_list(_metric_value(metrics, "artifact_matches", "missing")),
        "source_kinds": _string_list(_metric_value(metrics, "source_kind_coverage", "missing")),
        "modules": _string_list(_metric_value(metrics, "module_hits", "missing")),
        "api_surfaces": _string_list(_metric_value(metrics, "api_surface_hits", "missing")),
        "must_mentions": _string_list(_metric_value(metrics, "must_mention_coverage", "missing")),
        "source_uris": _string_list(_metric_value(metrics, "source_uri_coverage", "missing")),
        "citations": _string_list(_metric_value(metrics, "citation_coverage", "missing")),
        "hallucination_markers": _string_list(
            _metric_value(metrics, "hallucination_markers", "present")
        ),
    }


def _metric_value(metrics: Mapping[str, Any], metric_name: str, key: str) -> Any:
    metric = metrics.get(metric_name)
    if isinstance(metric, Mapping):
        return metric.get(key)
    return None


def _write_csv(path: Path, stats: Sequence[Mapping[str, Any]]) -> None:
    fields = [
        "index",
        "case_id",
        "title",
        "question",
        "baseline_run",
        "k2_run",
        "baseline_score",
        "baseline_retrieval_score",
        "baseline_answer_score",
        "baseline_safety_score",
        "k2_score",
        "k2_retrieval_score",
        "k2_answer_score",
        "k2_safety_score",
        "score_delta",
        "retrieval_score_delta",
        "answer_score_delta",
        "safety_score_delta",
        "baseline_answered",
        "k2_answered",
        "baseline_passed",
        "k2_passed",
        "baseline_result_count",
        "k2_result_count",
        "mcp_result_count",
        "mcp_tool_call_count",
        "mcp_tool_counts",
    ]
    for metric_name in METRIC_NAMES:
        fields.extend(
            [
                f"baseline_{metric_name}",
                f"k2_{metric_name}",
                f"delta_{metric_name}",
            ]
        )
    fields.extend(
        [
            "baseline_missing_artifacts",
            "k2_missing_artifacts",
            "baseline_missing_source_kinds",
            "k2_missing_source_kinds",
            "baseline_missing_modules",
            "k2_missing_modules",
            "baseline_missing_api_surfaces",
            "k2_missing_api_surfaces",
            "baseline_missing_must_mentions",
            "k2_missing_must_mentions",
            "baseline_missing_source_uris",
            "k2_missing_source_uris",
            "baseline_missing_citations",
            "k2_missing_citations",
            "baseline_hallucination_markers",
            "k2_hallucination_markers",
        ]
    )
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in stats:
            writer.writerow(_csv_row(row))


def _csv_row(row: Mapping[str, Any]) -> dict[str, Any]:
    csv_row = {
        "index": row.get("index"),
        "case_id": row.get("case_id"),
        "title": row.get("title"),
        "question": row.get("question"),
        "baseline_run": row.get("baseline_run"),
        "k2_run": row.get("k2_run"),
        "baseline_score": _format_score(row.get("baseline_score")),
        "k2_score": _format_score(row.get("k2_score")),
        "score_delta": _format_score(row.get("score_delta")),
        "baseline_answered": row.get("baseline_answered"),
        "k2_answered": row.get("k2_answered"),
        "baseline_passed": row.get("baseline_passed"),
        "k2_passed": row.get("k2_passed"),
        "baseline_result_count": row.get("baseline_result_count"),
        "k2_result_count": row.get("k2_result_count"),
        "mcp_result_count": row.get("mcp_result_count"),
        "mcp_tool_call_count": row.get("mcp_tool_call_count"),
        "mcp_tool_counts": json.dumps(row.get("mcp_tool_counts", {}), sort_keys=True),
    }
    baseline_components = row.get("baseline_score_components", {})
    k2_components = row.get("k2_score_components", {})
    component_deltas = row.get("score_component_deltas", {})
    if isinstance(baseline_components, Mapping):
        csv_row["baseline_retrieval_score"] = _format_score(
            baseline_components.get("retrieval_score")
        )
        csv_row["baseline_answer_score"] = _format_score(baseline_components.get("answer_score"))
        csv_row["baseline_safety_score"] = _format_score(baseline_components.get("safety_score"))
    if isinstance(k2_components, Mapping):
        csv_row["k2_retrieval_score"] = _format_score(k2_components.get("retrieval_score"))
        csv_row["k2_answer_score"] = _format_score(k2_components.get("answer_score"))
        csv_row["k2_safety_score"] = _format_score(k2_components.get("safety_score"))
    if isinstance(component_deltas, Mapping):
        csv_row["retrieval_score_delta"] = _format_score(
            component_deltas.get("retrieval_score")
        )
        csv_row["answer_score_delta"] = _format_score(component_deltas.get("answer_score"))
        csv_row["safety_score_delta"] = _format_score(component_deltas.get("safety_score"))

    metric_scores = row.get("metric_scores", {})
    for metric_name in METRIC_NAMES:
        metric = metric_scores.get(metric_name, {}) if isinstance(metric_scores, Mapping) else {}
        csv_row[f"baseline_{metric_name}"] = _format_score(metric.get("baseline"))
        csv_row[f"k2_{metric_name}"] = _format_score(metric.get("k2"))
        csv_row[f"delta_{metric_name}"] = _format_score(metric.get("delta"))

    baseline_missing = row.get("baseline_missing", {})
    k2_missing = row.get("k2_missing", {})
    for key, csv_key in (
        ("artifacts", "missing_artifacts"),
        ("source_kinds", "missing_source_kinds"),
        ("modules", "missing_modules"),
        ("api_surfaces", "missing_api_surfaces"),
        ("must_mentions", "missing_must_mentions"),
        ("source_uris", "missing_source_uris"),
        ("citations", "missing_citations"),
        ("hallucination_markers", "hallucination_markers"),
    ):
        csv_row[f"baseline_{csv_key}"] = _join_list(_missing_values(baseline_missing, key))
        csv_row[f"k2_{csv_key}"] = _join_list(_missing_values(k2_missing, key))
    return csv_row


def _mapping_for_case(source: Any, case_id: str) -> dict[str, int]:
    if not isinstance(source, Mapping):
        return {}
    value = source.get(case_id)
    if not isinstance(value, Mapping):
        return {}
    return {str(key): int(count) for key, count in value.items() if isinstance(count, int)}


def _sequence_for_case(source: Any, case_id: str) -> Sequence[Any]:
    if not isinstance(source, Mapping):
        return ()
    value = source.get(case_id)
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return value
    return ()


def _has_answer(source: Any, run_name: str, case_id: str) -> bool:
    if not isinstance(source, Mapping):
        return False
    by_case = source.get(run_name)
    if not isinstance(by_case, Mapping):
        return False
    return bool(str(by_case.get(case_id) or "").strip())


def _first_string(*values: Any) -> str:
    for value in values:
        if isinstance(value, str) and value:
            return value
    return ""


def _float_or_none(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return round(float(value), 6)
    return None


def _delta(left: float | None, right: float | None) -> float | None:
    if left is None or right is None:
        return None
    return round(left - right, 6)


def _string_list(value: Any) -> list[str]:
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [str(item) for item in value]
    return []


def _missing_values(source: Any, key: str) -> list[str]:
    if isinstance(source, Mapping):
        return _string_list(source.get(key))
    return []


def _join_list(values: Sequence[str]) -> str:
    return "; ".join(values)


def _format_score(value: Any) -> str:
    if isinstance(value, (int, float)):
        return f"{float(value):.6f}".rstrip("0").rstrip(".")
    return ""


def _gap_summary(missing: Any) -> str:
    if not isinstance(missing, Mapping):
        return "none"
    parts = []
    labels = (
        ("artifacts", "artifacts"),
        ("source_kinds", "source kinds"),
        ("modules", "modules"),
        ("api_surfaces", "API surfaces"),
        ("must_mentions", "must-mentions"),
        ("source_uris", "source URIs"),
        ("citations", "citations"),
        ("hallucination_markers", "hallucinations"),
    )
    for key, label in labels:
        values = _missing_values(missing, key)
        if values:
            parts.append(f"{label}: {len(values)}")
    return "; ".join(parts) if parts else "none"


def _metric_score_summary(metric_scores: Any, run_key: str) -> str:
    if not isinstance(metric_scores, Mapping):
        return ""
    parts = []
    for metric_name in METRIC_NAMES:
        metric = metric_scores.get(metric_name)
        if isinstance(metric, Mapping):
            score = _format_score(metric.get(run_key))
            if score:
                parts.append(f"{metric_name}={score}")
    return ", ".join(parts)


def _run_component_summary(run: Mapping[str, Any]) -> str:
    return _component_summary(_run_score_components(run))


def _run_score_components(run: Mapping[str, Any]) -> dict[str, Any]:
    components = run.get("score_components")
    if isinstance(components, Mapping):
        return dict(components)
    metric_averages = run.get("metric_averages")
    if not isinstance(metric_averages, Mapping):
        metric_averages = {}
    return {
        "combined_score": run.get("score"),
        "retrieval_score": metric_averages.get("retrieval_score_avg"),
        "answer_score": metric_averages.get("answer_score_avg"),
        "safety_score": metric_averages.get("hallucination_markers"),
    }


def _component_summary(components: Any) -> str:
    if not isinstance(components, Mapping):
        return ""
    return (
        f"combined={_format_score(components.get('combined_score'))}, "
        f"retrieval={_format_score(components.get('retrieval_score'))}, "
        f"answer={_format_score(components.get('answer_score'))}, "
        f"safety={_format_score(components.get('safety_score'))}"
    )


def _compact_component_triplet(components: Any) -> str:
    if not isinstance(components, Mapping):
        return ""
    return "/".join(
        [
            _format_score(components.get("combined_score")),
            _format_score(components.get("retrieval_score")),
            _format_score(components.get("answer_score")),
        ]
    )


def _truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 3].rstrip() + "..."


def _escape_table(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def _is_positive(value: Any) -> bool:
    return isinstance(value, (int, float)) and value > 0


def _is_negative(value: Any) -> bool:
    return isinstance(value, (int, float)) and value < 0
