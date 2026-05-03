"""Offline retrieval evaluation scorecards for the Java R&D demo."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from ._manifest import build_reproducibility_manifest
from .source_links import repo_relative_path, repo_web_url

TEXT_KEYS = ("text", "raw_text", "content", "chunk_text", "body", "snippet")
SOURCE_URI_KEYS = ("source_uri", "sourceUri", "uri", "url")
NESTED_ROW_KEYS = ("document", "item", "chunk", "payload", "result")


@dataclass(frozen=True)
class ExpectedArtifact:
    """Expected source artifact described by metadata, URI, and/or text predicates."""

    key: str
    source_uri: str | None = None
    source_kind: str | None = None
    module: str | None = None
    api_surface: str | None = None
    path_contains: str | None = None
    class_name: str | None = None
    text_contains: Sequence[str] = field(default_factory=tuple)
    metadata_equals: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "text_contains", _string_tuple(self.text_contains))
        object.__setattr__(self, "metadata_equals", dict(self.metadata_equals))

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "source_uri": self.source_uri,
            "source_kind": self.source_kind,
            "module": self.module,
            "api_surface": self.api_surface,
            "path_contains": self.path_contains,
            "class_name": self.class_name,
            "text_contains": list(self.text_contains),
            "metadata_equals": dict(self.metadata_equals),
        }


@dataclass(frozen=True)
class EvalCase:
    """A single offline scorecard case for a retrieval or answer run."""

    case_id: str
    query: str
    title: str = ""
    expected_artifacts: Sequence[ExpectedArtifact] = field(default_factory=tuple)
    expected_source_kinds: Sequence[str] = field(default_factory=tuple)
    required_modules: Sequence[str] = field(default_factory=tuple)
    required_api_surfaces: Sequence[str] = field(default_factory=tuple)
    must_mentions: Sequence[str] = field(default_factory=tuple)
    required_source_uris: Sequence[str] = field(default_factory=tuple)
    hallucination_markers: Sequence[str] = field(default_factory=tuple)
    pass_threshold: float = 0.8

    def __post_init__(self) -> None:
        object.__setattr__(self, "expected_artifacts", tuple(self.expected_artifacts))
        object.__setattr__(self, "expected_source_kinds", _string_tuple(self.expected_source_kinds))
        object.__setattr__(self, "required_modules", _string_tuple(self.required_modules))
        object.__setattr__(self, "required_api_surfaces", _string_tuple(self.required_api_surfaces))
        object.__setattr__(self, "must_mentions", _string_tuple(self.must_mentions))
        object.__setattr__(self, "required_source_uris", _string_tuple(self.required_source_uris))
        object.__setattr__(self, "hallucination_markers", _string_tuple(self.hallucination_markers))
        if not 0 <= self.pass_threshold <= 1:
            raise ValueError("pass_threshold must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "title": self.title,
            "query": self.query,
            "expected_artifacts": [artifact.to_dict() for artifact in self.expected_artifacts],
            "expected_source_kinds": list(self.expected_source_kinds),
            "required_modules": list(self.required_modules),
            "required_api_surfaces": list(self.required_api_surfaces),
            "must_mentions": list(self.must_mentions),
            "required_source_uris": list(self.required_source_uris),
            "hallucination_markers": list(self.hallucination_markers),
            "pass_threshold": self.pass_threshold,
        }


@dataclass(frozen=True)
class EvalRun:
    """Results for one system under evaluation, such as baseline or K2."""

    name: str
    results_by_case: Mapping[str, Sequence[Mapping[str, Any]]]
    answers_by_case: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "answers_by_case", dict(self.answers_by_case))


@dataclass(frozen=True)
class RetrievedResult:
    index: int
    source_uri: str
    text: str
    metadata: dict[str, Any]
    score: float | None = None

    def compact_summary(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "source_uri": self.source_uri,
            "path": self.metadata.get("path"),
            "source_kind": self.metadata.get("source_kind"),
            "module": self.metadata.get("module"),
            "api_surface": self.metadata.get("api_surface"),
            "class_name": self.metadata.get("class_name"),
            "score": self.score,
        }


def normalize_result_row(row: Mapping[str, Any], *, index: int = 0) -> RetrievedResult:
    """Normalize a K2-like result row into fields used by offline metrics."""

    parts = _row_parts(row)
    metadata: dict[str, Any] = {}
    for part in reversed(parts):
        for metadata_key in ("metadata", "custom_metadata"):
            part_metadata = part.get(metadata_key)
            if isinstance(part_metadata, Mapping):
                metadata.update(dict(part_metadata))

    source_uri = ""
    for part in parts:
        source_uri = _first_string(part, SOURCE_URI_KEYS)
        if source_uri:
            break
    if not source_uri:
        source_uri = _first_string(metadata, SOURCE_URI_KEYS)
    if not source_uri:
        source_uri = _source_uri_from_system_metadata(parts)

    texts = []
    for part in parts:
        text = _first_string(part, TEXT_KEYS)
        if text and text not in texts:
            texts.append(text)

    score = _coerce_score(row.get("score"))
    if score is None:
        score = _coerce_score(row.get("rerank_score"))

    return RetrievedResult(
        index=index,
        source_uri=source_uri,
        text="\n".join(texts),
        metadata=metadata,
        score=score,
    )


RETRIEVAL_METRICS = frozenset({
    "artifact_matches",
    "source_kind_coverage",
    "module_hits",
    "api_surface_hits",
    "source_uri_coverage",
})

ANSWER_METRICS = frozenset({
    "must_mention_coverage",
    "citation_coverage",
})


def score_case(
    case: EvalCase,
    result_rows: Sequence[Mapping[str, Any]],
    *,
    answer_text: str = "",
) -> dict[str, Any]:
    """Score one eval case against retrieved rows and optional generated answer text."""

    results = [normalize_result_row(row, index=index) for index, row in enumerate(result_rows)]
    citation_candidates = _required_source_uris(case)

    metrics = {
        "artifact_matches": _artifact_match_metric(case.expected_artifacts, results),
        "source_kind_coverage": _metadata_coverage_metric(
            case.expected_source_kinds, results, "source_kind"
        ),
        "module_hits": _metadata_coverage_metric(case.required_modules, results, "module"),
        "api_surface_hits": _metadata_coverage_metric(
            case.required_api_surfaces, results, "api_surface"
        ),
        "must_mention_coverage": _phrase_coverage_metric(
            case.must_mentions,
            answer_text,
            scope="answer",
        ) if answer_text else {
            "applicable": False,
            "score": 0.0,
            "scope": "answer",
            "required": list(_dedupe(case.must_mentions)),
            "matched": [],
            "missing": list(_dedupe(case.must_mentions)),
        },
        "source_uri_coverage": _source_uri_coverage_metric(citation_candidates, results),
        "citation_coverage": _citation_coverage_metric(citation_candidates, answer_text),
        "hallucination_markers": _hallucination_metric(case.hallucination_markers, answer_text),
    }

    retrieval_scores = [
        metrics[name]["score"]
        for name in RETRIEVAL_METRICS
        if metrics[name]["applicable"]
    ]
    answer_scores = [
        metrics[name]["score"]
        for name in ANSWER_METRICS
        if metrics[name]["applicable"]
    ]
    retrieval_score = _average(retrieval_scores) if retrieval_scores else None
    answer_score = _average(answer_scores) if answer_scores else None
    safety_score = metrics["hallucination_markers"]["score"]

    applicable_subscores = [
        s for s in (retrieval_score, answer_score) if s is not None
    ]
    # Retrieval and answer quality contribute equally to base_score.
    # This means individual retrieval metrics (5) have less per-metric
    # weight than individual answer metrics (2). This is intentional:
    # we care about retrieval and answer quality as categories, not
    # about equal weight per metric.
    base_score = _average(applicable_subscores) if applicable_subscores else 1.0
    score = base_score * safety_score

    return {
        "case_id": case.case_id,
        "title": case.title,
        "query": case.query,
        "score": round(score, 6),
        "base_score": round(base_score, 6),
        "score_breakdown": {
            "retrieval_score": round(retrieval_score, 6) if retrieval_score is not None else None,
            "answer_score": round(answer_score, 6) if answer_score is not None else None,
            "safety_score": round(safety_score, 6),
        },
        "passed": score >= case.pass_threshold,
        "pass_threshold": case.pass_threshold,
        "result_count": len(results),
        "metrics": metrics,
    }


def score_run(cases: Sequence[EvalCase], run: EvalRun) -> dict[str, Any]:
    """Score all cases for one named run."""

    case_summaries = []
    for case in cases:
        rows = run.results_by_case.get(case.case_id, ())
        answer_text = run.answers_by_case.get(case.case_id, "")
        case_summaries.append(score_case(case, rows, answer_text=answer_text))

    score = _average(summary["score"] for summary in case_summaries)
    score_components = _score_component_averages(case_summaries, combined_score=score)
    return {
        "run_name": run.name,
        "score": round(score, 6),
        "score_components": score_components,
        "case_count": len(case_summaries),
        "passed_cases": sum(1 for summary in case_summaries if summary["passed"]),
        "metric_averages": _metric_averages(case_summaries),
        "cases": case_summaries,
    }


def compare_runs(cases: Sequence[EvalCase], runs: Sequence[EvalRun]) -> dict[str, Any]:
    """Build a JSON-serializable baseline-vs-K2 scorecard summary."""

    run_summaries = [score_run(cases, run) for run in runs]
    if not run_summaries:
        return {
            "case_count": len(cases),
            "baseline_run": None,
            "best_run": None,
            "runs": [],
            "comparisons": [],
        }

    baseline = run_summaries[0]
    best = max(run_summaries, key=lambda summary: summary["score"])
    comparisons = []
    for summary in run_summaries[1:]:
        comparisons.append(
            {
                "run_name": summary["run_name"],
                "score_delta_vs_baseline": round(summary["score"] - baseline["score"], 6),
                "score_component_deltas_vs_baseline": _score_component_deltas(
                    baseline.get("score_components", {}),
                    summary.get("score_components", {}),
                ),
                "metric_deltas_vs_baseline": _metric_deltas(
                    baseline["metric_averages"], summary["metric_averages"]
                ),
            }
        )

    return {
        "case_count": len(cases),
        "baseline_run": baseline["run_name"],
        "best_run": best["run_name"],
        "runs": run_summaries,
        "comparisons": comparisons,
        "manifest": build_reproducibility_manifest(),
    }


def _artifact_match_metric(
    expected_artifacts: Sequence[ExpectedArtifact], results: Sequence[RetrievedResult]
) -> dict[str, Any]:
    items = []
    for artifact in expected_artifacts:
        matches = [
            result.compact_summary()
            for result in results
            if _artifact_matches(artifact, result)
        ]
        items.append(
            {
                "artifact": artifact.key,
                "matched": bool(matches),
                "matched_rows": matches,
                "expected": artifact.to_dict(),
            }
        )

    matched_count = sum(1 for item in items if item["matched"])
    return {
        "applicable": bool(expected_artifacts),
        "score": _coverage_score(matched_count, len(expected_artifacts)),
        "matched": [item["artifact"] for item in items if item["matched"]],
        "missing": [item["artifact"] for item in items if not item["matched"]],
        "items": items,
    }


def _artifact_matches(artifact: ExpectedArtifact, result: RetrievedResult) -> bool:
    metadata = result.metadata
    checks = [
        artifact.source_uri,
        artifact.source_kind,
        artifact.module,
        artifact.api_surface,
        artifact.path_contains,
        artifact.class_name,
        *artifact.text_contains,
        *[str(value) for value in artifact.metadata_equals.values()],
    ]
    if not any(checks):
        return False

    if artifact.source_uri and _norm(result.source_uri) != _norm(artifact.source_uri):
        return False
    if artifact.source_kind and _norm(metadata.get("source_kind")) != _norm(artifact.source_kind):
        return False
    if artifact.module and _norm(metadata.get("module")) != _norm(artifact.module):
        return False
    if artifact.api_surface and _norm(metadata.get("api_surface")) != _norm(artifact.api_surface):
        return False
    if artifact.class_name and _norm(metadata.get("class_name")) != _norm(artifact.class_name):
        return False
    if artifact.path_contains:
        path_haystack = f"{metadata.get('path', '')} {result.source_uri}"
        if not _contains(path_haystack, artifact.path_contains):
            return False
    for key, expected in artifact.metadata_equals.items():
        if _norm(metadata.get(key)) != _norm(expected):
            return False

    text_haystack = f"{result.text}\n{_metadata_text(metadata)}"
    return all(_contains(text_haystack, phrase) for phrase in artifact.text_contains)


def _metadata_coverage_metric(
    required_values: Sequence[str], results: Sequence[RetrievedResult], key: str
) -> dict[str, Any]:
    required = _dedupe(required_values)
    observed = _dedupe(
        str(result.metadata.get(key)) for result in results if result.metadata.get(key)
    )
    observed_norm = {_norm(value) for value in observed}
    matched = [value for value in required if _norm(value) in observed_norm]
    missing = [value for value in required if _norm(value) not in observed_norm]
    return {
        "applicable": bool(required),
        "score": _coverage_score(len(matched), len(required)),
        "required": required,
        "observed": observed,
        "matched": matched,
        "missing": missing,
    }


def _phrase_coverage_metric(
    required_phrases: Sequence[str], haystack: str, *, scope: str
) -> dict[str, Any]:
    required = _dedupe(required_phrases)
    matched = [phrase for phrase in required if _contains(haystack, phrase)]
    missing = [phrase for phrase in required if phrase not in matched]
    return {
        "applicable": bool(required),
        "score": _coverage_score(len(matched), len(required)),
        "scope": scope,
        "required": required,
        "matched": matched,
        "missing": missing,
    }


def _source_uri_coverage_metric(
    required_uris: Sequence[str], results: Sequence[RetrievedResult]
) -> dict[str, Any]:
    required = _dedupe(required_uris)
    observed = _dedupe(result.source_uri for result in results if result.source_uri)
    observed_norm = {_norm(uri) for uri in observed}
    matched = [uri for uri in required if _norm(uri) in observed_norm]
    missing = [uri for uri in required if _norm(uri) not in observed_norm]
    return {
        "applicable": bool(required),
        "score": _coverage_score(len(matched), len(required)),
        "required": required,
        "observed": observed,
        "matched": matched,
        "missing": missing,
    }


def _citation_coverage_metric(required_uris: Sequence[str], answer_text: str) -> dict[str, Any]:
    required = _dedupe(required_uris)
    matched = [uri for uri in required if answer_text and _answer_cites_required_uri(answer_text, uri)]
    missing = [uri for uri in required if uri not in matched]
    return {
        "applicable": bool(required and answer_text),
        "score": _coverage_score(len(matched), len(required)) if answer_text else 1.0,
        "required": required,
        "matched": matched,
        "missing": missing if answer_text else [],
    }


def _answer_cites_required_uri(answer_text: str, source_uri: str) -> bool:
    if _contains(answer_text, source_uri):
        return True
    web_url = repo_web_url(source_uri)
    if web_url and _contains(answer_text, web_url):
        return True
    path = repo_relative_path(source_uri)
    return bool(path and _contains(answer_text, path))


def _hallucination_metric(markers: Sequence[str], answer_text: str) -> dict[str, Any]:
    required = _dedupe(markers)
    present = [marker for marker in required if answer_text and _contains(answer_text, marker)]
    return {
        "applicable": bool(required and answer_text),
        "score": 0.0 if present else 1.0,
        "markers": required,
        "present": present,
    }


def _metric_averages(case_summaries: Sequence[Mapping[str, Any]]) -> dict[str, float]:
    metric_names = sorted(
        {
            metric_name
            for summary in case_summaries
            for metric_name in summary.get("metrics", {})
            if metric_name != "hallucination_markers"
        }
    )
    averages: dict[str, float] = {}
    for metric_name in metric_names:
        scores = [
            summary["metrics"][metric_name]["score"]
            for summary in case_summaries
            if summary["metrics"][metric_name]["applicable"]
        ]
        if scores:
            averages[metric_name] = round(_average(scores), 6)
    hallucination_scores = [
        summary["metrics"]["hallucination_markers"]["score"]
        for summary in case_summaries
        if summary["metrics"]["hallucination_markers"]["applicable"]
    ]
    if hallucination_scores:
        averages["hallucination_markers"] = round(_average(hallucination_scores), 6)

    retrieval_scores = [
        summary["score_breakdown"]["retrieval_score"]
        for summary in case_summaries
        if summary.get("score_breakdown", {}).get("retrieval_score") is not None
    ]
    answer_scores = [
        summary["score_breakdown"]["answer_score"]
        for summary in case_summaries
        if summary.get("score_breakdown", {}).get("answer_score") is not None
    ]
    if retrieval_scores:
        averages["retrieval_score_avg"] = round(_average(retrieval_scores), 6)
    if answer_scores:
        averages["answer_score_avg"] = round(_average(answer_scores), 6)

    return averages


def _score_component_averages(
    case_summaries: Sequence[Mapping[str, Any]], *, combined_score: float
) -> dict[str, float | None]:
    return {
        "combined_score": round(combined_score, 6),
        "retrieval_score": _breakdown_average(case_summaries, "retrieval_score"),
        "answer_score": _breakdown_average(case_summaries, "answer_score"),
        "safety_score": _breakdown_average(case_summaries, "safety_score"),
    }


def _breakdown_average(
    case_summaries: Sequence[Mapping[str, Any]], component_name: str
) -> float | None:
    values = [
        float(summary["score_breakdown"][component_name])
        for summary in case_summaries
        if summary.get("score_breakdown", {}).get(component_name) is not None
    ]
    return round(_average(values), 6) if values else None


def _score_component_deltas(
    baseline_components: Mapping[str, Any],
    current_components: Mapping[str, Any],
) -> dict[str, float | None]:
    names = sorted(set(baseline_components) | set(current_components))
    deltas: dict[str, float | None] = {}
    for name in names:
        baseline_value = baseline_components.get(name)
        current_value = current_components.get(name)
        if isinstance(baseline_value, (int, float)) and isinstance(current_value, (int, float)):
            deltas[name] = round(float(current_value) - float(baseline_value), 6)
        else:
            deltas[name] = None
    return deltas


def _metric_deltas(
    baseline_metrics: Mapping[str, float], current_metrics: Mapping[str, float]
) -> dict[str, float]:
    names = sorted(set(baseline_metrics) | set(current_metrics))
    return {
        name: round(current_metrics.get(name, 0.0) - baseline_metrics.get(name, 0.0), 6)
        for name in names
    }


def _required_source_uris(case: EvalCase) -> tuple[str, ...]:
    artifact_uris = [
        artifact.source_uri for artifact in case.expected_artifacts if artifact.source_uri
    ]
    return tuple(_dedupe([*case.required_source_uris, *artifact_uris]))


def _metadata_text(metadata: Mapping[str, Any]) -> str:
    values: list[str] = []
    for value in metadata.values():
        if isinstance(value, Mapping):
            values.append(_metadata_text(value))
        elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
            values.extend(str(item) for item in value)
        elif value is not None:
            values.append(str(value))
    return "\n".join(values)


def _row_parts(row: Mapping[str, Any]) -> tuple[Mapping[str, Any], ...]:
    parts: list[Mapping[str, Any]] = [row]
    for key in NESTED_ROW_KEYS:
        value = row.get(key)
        if isinstance(value, Mapping):
            parts.append(value)
            break
    return tuple(parts)


def _source_uri_from_system_metadata(parts: Sequence[Mapping[str, Any]]) -> str:
    for part in parts:
        system_metadata = part.get("system_metadata")
        if not isinstance(system_metadata, Mapping):
            continue
        source_uri = _first_string(system_metadata, SOURCE_URI_KEYS)
        if source_uri:
            return source_uri
        provenance = system_metadata.get("provenance")
        if isinstance(provenance, Mapping):
            source_uri = _first_string(provenance, SOURCE_URI_KEYS)
            if source_uri:
                return source_uri
    return ""


def _first_string(mapping: Mapping[str, Any], keys: Sequence[str]) -> str:
    for key in keys:
        value = mapping.get(key)
        if isinstance(value, str):
            return value
    return ""


def _coerce_score(value: Any) -> float | None:
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _string_tuple(values: Sequence[str]) -> tuple[str, ...]:
    if isinstance(values, str):
        return (values,)
    return tuple(str(value) for value in values if value is not None)


def _dedupe(values: Iterable[Any]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value is None:
            continue
        normalized = _norm(value)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(str(value))
    return result


def _coverage_score(matched_count: int, required_count: int) -> float:
    if required_count == 0:
        return 1.0
    return round(matched_count / required_count, 6)


def _average(values: Iterable[float]) -> float:
    items = list(values)
    return sum(items) / len(items) if items else 0.0


def _contains(haystack: str, needle: str) -> bool:
    return _norm(needle) in _norm(haystack)


def _norm(value: Any) -> str:
    return str(value or "").casefold()


__all__ = [
    "ANSWER_METRICS",
    "EvalCase",
    "EvalRun",
    "ExpectedArtifact",
    "RETRIEVAL_METRICS",
    "RetrievedResult",
    "compare_runs",
    "normalize_result_row",
    "score_case",
    "score_run",
]
