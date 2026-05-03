"""Offline-testable live K2 eval runner for the Java R&D demo."""

from __future__ import annotations

import inspect
import json
from collections.abc import Iterable, Mapping, Sequence
from copy import deepcopy
from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any

from .eval_cases import demo_eval_cases
from .evaluation import EvalCase, EvalRun, compare_runs, normalize_result_row
from .filters import (
    DEMO_HYBRID,
    DEMO_RETURN,
    eq,
    flink_checkpoint_docs_or_guides_filter,
    flink_docs_filter,
    flink_rest_code_filter,
    flink_rest_tests_filter,
    in_,
    kafka_connect_filter,
    structured_filter,
)
from .metadata import DEMO_DATASET_ID


class LiveEvalError(Exception):
    """Base error for live eval runner failures."""


class LiveEvalConfigError(LiveEvalError, ValueError):
    """Raised when live eval configuration is incomplete or unsafe."""


class LiveEvalClientError(LiveEvalError, RuntimeError):
    """Raised when the supplied K2-like client cannot run searches."""


def _default_hybrid() -> dict[str, Any]:
    return dict(DEMO_HYBRID)


def _default_return_config() -> dict[str, Any]:
    return dict(DEMO_RETURN)


@dataclass(frozen=True)
class LiveEvalConfig:
    """Configuration for one guarded live K2 eval run."""

    project_id: str
    corpus_ids: Mapping[str, str]
    include_kafka: bool = False
    top_k: int = 12
    execute: bool = False
    run_name: str = "k2"
    baseline_name: str = "baseline"
    include_guides: bool = True
    hybrid: Mapping[str, Any] = field(default_factory=_default_hybrid)
    return_config: Mapping[str, Any] = field(default_factory=_default_return_config)

    def __post_init__(self) -> None:
        _require_non_empty(self.project_id, "project_id")
        if self.top_k < 1:
            raise LiveEvalConfigError("top_k must be at least 1")
        if not _clean_optional(self.run_name):
            raise LiveEvalConfigError("run_name is required")
        if not _clean_optional(self.baseline_name):
            raise LiveEvalConfigError("baseline_name is required")

        normalized = _normalized_corpus_ids(self.corpus_ids)
        required_roles = {"docs", "code"}
        if self.include_guides:
            required_roles.add("guides")
        frameworks = ["flink", "kafka"] if self.include_kafka else ["flink"]
        missing = sorted(
            role
            for framework in frameworks
            for role in required_roles
            if not _has_corpus_id(normalized, role, framework)
        )
        if missing:
            raise LiveEvalConfigError(
                f"missing corpus id(s) for role(s): {', '.join(_dedupe(missing))}"
            )
        object.__setattr__(self, "corpus_ids", normalized)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LiveEvalSearchRequest:
    """One routed K2 search generated from an eval case."""

    case_id: str
    role: str
    source_kind: str
    corpus_id: str
    query: str
    filters: Mapping[str, Any]
    top_k: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def select_eval_cases(
    cases: Iterable[EvalCase] | None = None,
    *,
    include_kafka: bool = False,
) -> tuple[EvalCase, ...]:
    """Return caller-provided cases or the demo catalog selected by config."""

    if cases is not None:
        return tuple(cases)
    return tuple(demo_eval_cases(include_kafka=include_kafka))


def build_live_eval_search_requests(
    config: LiveEvalConfig,
    cases: Iterable[EvalCase] | None = None,
) -> tuple[LiveEvalSearchRequest, ...]:
    """Build routed corpus searches without touching the network."""

    selected_cases = select_eval_cases(cases, include_kafka=config.include_kafka)
    requests: list[LiveEvalSearchRequest] = []
    for case in selected_cases:
        framework = _case_framework(case)
        for source_kind in _source_kinds_for_case(case, include_guides=config.include_guides):
            role = _role_for_source_kind(source_kind)
            for corpus_id in _lookup_corpus_ids(config.corpus_ids, role, framework):
                requests.append(
                    LiveEvalSearchRequest(
                        case_id=case.case_id,
                        role=role,
                        source_kind=source_kind,
                        corpus_id=corpus_id,
                        query=case.query,
                        filters=build_case_search_filter(case, source_kind),
                        top_k=config.top_k,
                    )
                )
    return tuple(requests)


def build_case_search_filter(case: EvalCase, source_kind: str) -> dict[str, Any]:
    """Build a metadata filter for one case/source-kind search."""

    normalized_source_kind = _require_non_empty(source_kind, "source_kind")
    recipe = _filter_recipe_for_case(case, normalized_source_kind)
    fallback = _case_metadata_filter(case, normalized_source_kind)
    return _merge_filters(recipe, fallback)


def collect_k2_eval_run(
    client: Any,
    config: LiveEvalConfig,
    cases: Iterable[EvalCase] | None = None,
) -> EvalRun:
    """Execute live K2 searches and return an ``EvalRun`` for scoring."""

    _assert_execute(config)
    selected_cases = select_eval_cases(cases, include_kafka=config.include_kafka)
    requests = build_live_eval_search_requests(config, selected_cases)
    rows_by_case: dict[str, list[dict[str, Any]]] = {
        case.case_id: [] for case in selected_cases
    }
    seen_by_case: dict[str, set[tuple[str, str, str]]] = {
        case.case_id: set() for case in selected_cases
    }

    for request in requests:
        response = _call_search(client, request, config)
        raw_rows = _response_rows(response)
        normalized_rows = normalize_live_eval_rows(
            raw_rows,
            inferred_metadata={
                "corpus_role": request.role,
                "source_kind": request.source_kind,
            },
        )
        _merge_case_rows(
            rows_by_case[request.case_id],
            seen_by_case[request.case_id],
            normalized_rows,
        )

    return EvalRun(name=config.run_name, results_by_case=rows_by_case)


def run_live_eval(
    client: Any,
    config: LiveEvalConfig,
    cases: Iterable[EvalCase] | None = None,
    *,
    baseline: EvalRun | Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Run live K2 retrieval evals and return ``compare_runs`` output."""

    selected_cases = select_eval_cases(cases, include_kafka=config.include_kafka)
    baseline_run = coerce_baseline_run(baseline, name=config.baseline_name)
    k2_run = collect_k2_eval_run(client, config, selected_cases)
    return compare_runs(selected_cases, [baseline_run, k2_run])


def coerce_baseline_run(
    baseline: EvalRun | Mapping[str, Any] | None,
    *,
    name: str = "baseline",
) -> EvalRun:
    """Accept an ``EvalRun``, a case-row mapping, or ``None`` as baseline."""

    if baseline is None:
        return EvalRun(name=name, results_by_case={})
    if isinstance(baseline, EvalRun):
        return baseline
    if not isinstance(baseline, Mapping):
        raise LiveEvalConfigError("baseline must be an EvalRun, mapping, or None")

    if "results_by_case" in baseline:
        raw_name = baseline.get("name") or baseline.get("run_name") or name
        results_by_case = baseline.get("results_by_case")
        answers_by_case = baseline.get("answers_by_case", {})
        if not isinstance(results_by_case, Mapping):
            raise LiveEvalConfigError("baseline results_by_case must be a mapping")
        if not isinstance(answers_by_case, Mapping):
            raise LiveEvalConfigError("baseline answers_by_case must be a mapping")
        return EvalRun(
            name=str(raw_name),
            results_by_case=_normalize_results_mapping(results_by_case),
            answers_by_case={str(key): str(value) for key, value in answers_by_case.items()},
        )

    return EvalRun(name=name, results_by_case=_normalize_results_mapping(baseline))


def normalize_live_eval_rows(
    rows: Iterable[Any],
    *,
    inferred_metadata: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Normalize K2-like rows into the row shape consumed by ``evaluation``."""

    normalized: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        mapping = _row_mapping(row)
        result = normalize_result_row(mapping, index=index)
        metadata = dict(result.metadata)
        for key, value in dict(inferred_metadata or {}).items():
            if value is not None and not metadata.get(key):
                metadata[key] = value

        item: dict[str, Any] = {
            "source_uri": result.source_uri,
            "raw_text": result.text,
            "metadata": metadata,
        }
        if result.score is not None:
            item["score"] = result.score
        normalized.append(item)
    return normalized


def _assert_execute(config: LiveEvalConfig) -> None:
    if not config.execute:
        raise LiveEvalConfigError("live eval searches require execute=True")


def _call_search(client: Any, request: LiveEvalSearchRequest, config: LiveEvalConfig) -> Any:
    methods = _search_methods(client)
    if not methods:
        raise LiveEvalClientError(
            "client must provide search() or a namespace search method such as corpora.search()"
        )

    common_kwargs = {
        "top_k": request.top_k,
        "filters": deepcopy(dict(request.filters)),
        "hybrid": deepcopy(dict(config.hybrid)),
        "return_config": deepcopy(dict(config.return_config)),
    }
    project_kwargs = {"project_id": config.project_id}
    candidates = [
        ((request.corpus_id, request.query), common_kwargs),
        ((), {"corpus_id": request.corpus_id, "query": request.query, **common_kwargs}),
        ((), {"corpus": request.corpus_id, "query": request.query, **common_kwargs}),
        ((), {"corpus_ids": [request.corpus_id], "query": request.query, **common_kwargs}),
        ((request.corpus_id, request.query), {**common_kwargs, **project_kwargs}),
        (
            (),
            {
                "project_id": config.project_id,
                "corpus_id": request.corpus_id,
                "query": request.query,
                **common_kwargs,
            },
        ),
    ]

    errors: list[str] = []
    for method_name, method in methods:
        for args, kwargs in candidates:
            if not _signature_accepts(method, args, kwargs):
                continue
            try:
                return method(*args, **kwargs)
            except TypeError as exc:
                errors.append(f"{method_name}: {exc}")

    details = "; ".join(errors) if errors else "no compatible search signature"
    raise LiveEvalClientError(f"unable to call client search method: {details}")


def _search_methods(client: Any) -> list[tuple[str, Any]]:
    methods: list[tuple[str, Any]] = []
    direct = getattr(client, "search", None)
    if callable(direct):
        methods.append(("search", direct))
    for namespace_name in ("corpora", "corpus", "documents", "retrieval"):
        namespace = getattr(client, namespace_name, None)
        method = getattr(namespace, "search", None)
        if callable(method):
            methods.append((f"{namespace_name}.search", method))
    return methods


def _signature_accepts(method: Any, args: tuple[Any, ...], kwargs: Mapping[str, Any]) -> bool:
    try:
        signature = inspect.signature(method)
    except (TypeError, ValueError):
        return True
    try:
        signature.bind(*args, **dict(kwargs))
    except TypeError:
        return False
    return True


def _response_rows(response: Any) -> list[Mapping[str, Any]]:
    if isinstance(response, Mapping):
        for key in ("results", "chunks", "documents", "items", "data"):
            value = response.get(key)
            if _is_row_sequence(value):
                return [_row_mapping(item) for item in value]
        nested = response.get("response")
        if nested is not response:
            nested_rows = _response_rows(nested)
            if nested_rows:
                return nested_rows
        if any(key in response for key in ("source_uri", "metadata", "document", "chunk")):
            return [dict(response)]
        return []

    if _is_row_sequence(response):
        return [_row_mapping(item) for item in response]

    for attr_name in ("results", "chunks", "documents", "items", "data"):
        value = getattr(response, attr_name, None)
        if _is_row_sequence(value):
            return [_row_mapping(item) for item in value]
    return []


def _row_mapping(row: Any) -> Mapping[str, Any]:
    if isinstance(row, Mapping):
        return dict(row)
    if is_dataclass(row) and not isinstance(row, type):
        return asdict(row)
    to_dict = getattr(row, "to_dict", None)
    if callable(to_dict):
        value = to_dict()
        if isinstance(value, Mapping):
            return dict(value)
    if hasattr(row, "__dict__"):
        return {
            str(key): value
            for key, value in vars(row).items()
            if not str(key).startswith("_")
        }
    return {"text": str(row)}


def _merge_case_rows(
    merged: list[dict[str, Any]],
    seen: set[tuple[str, str, str]],
    rows: Iterable[dict[str, Any]],
) -> None:
    for row in rows:
        result = normalize_result_row(row, index=len(merged))
        key = (
            _norm(result.source_uri),
            _norm(result.metadata.get("path")),
            _norm(result.text),
        )
        if key in seen:
            continue
        seen.add(key)
        merged.append(row)


def _source_kinds_for_case(case: EvalCase, *, include_guides: bool) -> tuple[str, ...]:
    kinds: list[str] = []
    for source_kind in case.expected_source_kinds:
        _append_unique(kinds, source_kind)
    for artifact in case.expected_artifacts:
        if artifact.source_kind:
            _append_unique(kinds, artifact.source_kind)
    if include_guides:
        _append_unique(kinds, "guide")
    return tuple(kinds)


def _role_for_source_kind(source_kind: str) -> str:
    if source_kind == "docs":
        return "docs"
    if source_kind == "guide":
        return "guides"
    return "code"


def _filter_recipe_for_case(case: EvalCase, source_kind: str) -> dict[str, Any] | None:
    framework = _case_framework(case)
    api_surfaces = set(case.required_api_surfaces)
    if framework == "kafka":
        return kafka_connect_filter()
    if framework != "flink":
        return None

    if source_kind == "docs":
        if "checkpointing" in api_surfaces:
            return flink_checkpoint_docs_or_guides_filter()
        return flink_docs_filter()
    if source_kind == "guide" and "checkpointing" in api_surfaces:
        return flink_checkpoint_docs_or_guides_filter()
    if source_kind == "code" and "rest" in api_surfaces:
        return flink_rest_code_filter()
    if source_kind == "test" and "rest" in api_surfaces:
        return flink_rest_tests_filter()
    if source_kind in {"code", "test"} and "checkpointing" in api_surfaces:
        return structured_filter(
            [
                eq("framework", "flink"),
                eq("framework_version", "2.2.0"),
                eq("source_kind", source_kind),
                eq("module", "flink-runtime"),
                in_("api_surface", ["checkpointing", "rest"]),
            ]
        )
    return None


def _case_metadata_filter(case: EvalCase, source_kind: str) -> dict[str, Any]:
    filters: list[dict[str, Any]] = [
        eq("demo_dataset_id", DEMO_DATASET_ID),
        eq("source_kind", source_kind),
    ]
    framework = _case_framework(case)
    if framework:
        filters.append(eq("framework", framework))
    version = _case_framework_version(case, framework)
    if version:
        filters.append(eq("framework_version", version))

    modules = _metadata_values_for_source_kind(case, source_kind, "module")
    if source_kind == "guide":
        modules = ["guides"]
    elif source_kind == "docs" and not modules:
        modules = ["docs"]
    filters.extend(_value_filter("module", modules))

    api_surfaces = _metadata_values_for_source_kind(case, source_kind, "api_surface")
    if not api_surfaces:
        api_surfaces = list(case.required_api_surfaces)
    filters.extend(_value_filter("api_surface", api_surfaces))

    return structured_filter(filters)


def _metadata_values_for_source_kind(
    case: EvalCase,
    source_kind: str,
    field_name: str,
) -> list[str]:
    values: list[str] = []
    for artifact in case.expected_artifacts:
        if artifact.source_kind != source_kind:
            continue
        value = getattr(artifact, field_name, None)
        if value:
            _append_unique(values, str(value))
    return values


def _case_framework(case: EvalCase) -> str | None:
    haystack = " ".join(
        [
            case.case_id,
            case.title,
            case.query,
            *[
                artifact.source_uri or ""
                for artifact in case.expected_artifacts
            ],
            *case.required_api_surfaces,
        ]
    ).casefold()
    if "kafka" in haystack or "connect" in case.required_api_surfaces:
        return "kafka"
    if "flink" in haystack:
        return "flink"
    return None


def _case_framework_version(case: EvalCase, framework: str | None) -> str | None:
    values: list[str] = []
    for artifact in case.expected_artifacts:
        value = artifact.metadata_equals.get("framework_version")
        if value:
            _append_unique(values, str(value))
    if len(values) == 1:
        return values[0]
    if framework == "flink":
        return "2.2.0"
    if framework == "kafka":
        return "4.2.0"
    return None


def _value_filter(key: str, values: Sequence[str]) -> list[dict[str, Any]]:
    unique = [value for value in _dedupe(values) if value]
    if not unique:
        return []
    if len(unique) == 1:
        return [eq(key, unique[0])]
    return [in_(key, unique)]


def _merge_filters(*filters: Mapping[str, Any] | None) -> dict[str, Any]:
    merged: list[dict[str, Any]] = []
    seen: set[str] = set()
    for filter_object in filters:
        for item in _filter_items(filter_object):
            key = json.dumps(item, sort_keys=True, default=str)
            if key in seen:
                continue
            seen.add(key)
            merged.append(item)
    return structured_filter(merged)


def _filter_items(filter_object: Mapping[str, Any] | None) -> list[dict[str, Any]]:
    if not filter_object:
        return []
    condition = filter_object.get("condition")
    items = filter_object.get("filters")
    if condition == "and" and _is_row_sequence(items):
        return [dict(item) for item in items if isinstance(item, Mapping)]
    return [dict(filter_object)]


def _normalize_results_mapping(value: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    normalized: dict[str, list[dict[str, Any]]] = {}
    for case_id, rows in value.items():
        if isinstance(rows, Mapping):
            row_values: Iterable[Any] = (rows,)
        elif _is_row_sequence(rows):
            row_values = rows
        else:
            raise LiveEvalConfigError(f"baseline rows for {case_id!r} must be a sequence")
        normalized[str(case_id)] = normalize_live_eval_rows(row_values)
    return normalized


def _normalized_corpus_ids(corpus_ids: Mapping[str, str]) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for raw_role, raw_corpus_id in corpus_ids.items():
        role = _normalize_role(str(raw_role))
        corpus_id = _require_non_empty(str(raw_corpus_id), f"corpus id for {raw_role!r}")
        normalized[role] = corpus_id
    return normalized


def _normalize_role(role: str) -> str:
    lowered = role.strip().lower()
    aliases = {
        "java_rd_guides": "guides",
        "guide": "guides",
    }
    return aliases.get(lowered, lowered)


def _has_corpus_id(corpus_ids: Mapping[str, str], role: str, framework: str | None) -> bool:
    try:
        _lookup_corpus_id(corpus_ids, role, framework)
    except LiveEvalConfigError:
        return False
    return True


def _lookup_corpus_id(
    corpus_ids: Mapping[str, str],
    role: str,
    framework: str | None = None,
) -> str:
    return _lookup_corpus_ids(corpus_ids, role, framework)[0]


def _lookup_corpus_ids(
    corpus_ids: Mapping[str, str],
    role: str,
    framework: str | None = None,
) -> tuple[str, ...]:
    candidate_keys: list[str] = []
    if framework and role in {"docs", "code"}:
        candidate_keys.append(f"{framework}_{role}")
        candidate_keys.extend(
            key
            for key in sorted(corpus_ids)
            if key.startswith(f"{framework}_{role}_")
        )
    candidate_keys.append(role)
    candidate_keys.extend(
        key
        for key in sorted(corpus_ids)
        if key.startswith(f"{role}_")
    )

    selected: list[str] = []
    for key in candidate_keys:
        corpus_id = _clean_optional(corpus_ids.get(key))
        if corpus_id:
            _append_unique(selected, corpus_id)
    if not selected:
        joined = ", ".join(candidate_keys)
        raise LiveEvalConfigError(f"missing corpus id for role {role!r}; tried {joined}")
    return tuple(selected)


def _require_non_empty(value: str | None, label: str) -> str:
    cleaned = _clean_optional(value)
    if not cleaned:
        raise LiveEvalConfigError(f"{label} is required")
    return cleaned


def _clean_optional(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _append_unique(values: list[str], value: Any) -> None:
    cleaned = str(value).strip()
    if cleaned and cleaned not in values:
        values.append(cleaned)


def _dedupe(values: Iterable[Any]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = _norm(value)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(str(value))
    return result


def _is_row_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _norm(value: Any) -> str:
    return str(value or "").casefold()


__all__ = [
    "LiveEvalClientError",
    "LiveEvalConfig",
    "LiveEvalConfigError",
    "LiveEvalError",
    "LiveEvalSearchRequest",
    "build_case_search_filter",
    "build_live_eval_search_requests",
    "coerce_baseline_run",
    "collect_k2_eval_run",
    "normalize_live_eval_rows",
    "run_live_eval",
    "select_eval_cases",
]
