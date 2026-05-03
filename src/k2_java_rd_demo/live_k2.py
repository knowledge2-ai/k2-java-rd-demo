"""Offline-testable live K2 orchestration for the Java R&D demo.

The helpers in this module intentionally use duck-typed client methods instead
of importing the Knowledge2 SDK. Unit tests can use fake clients, while the CLI
or a later integration layer can pass a real SDK client.
"""

from __future__ import annotations

import os
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .assets import read_jsonl
from .chunking import chunking_for_source_kind
from .filters import DEMO_HYBRID, DEMO_RETURN, flink_checkpoint_docs_or_guides_filter
from .filters import flink_rest_code_filter
from .metadata import validate_metadata


class LiveK2Error(Exception):
    """Base error for live K2 orchestration failures."""


class LiveK2ConfigError(LiveK2Error, ValueError):
    """Raised when required live K2 configuration is missing or invalid."""


class LiveK2ClientError(LiveK2Error, RuntimeError):
    """Raised when a duck-typed K2 client does not meet the expected contract."""


@dataclass(frozen=True)
class CorpusDefinition:
    role: str
    name: str
    description: str
    chunking_source_kind: str
    env_vars: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.role.strip():
            raise LiveK2ConfigError("corpus role is required")
        if not self.name.strip():
            raise LiveK2ConfigError(f"corpus name for role {self.role!r} is required")
        if not self.chunking_source_kind.strip():
            raise LiveK2ConfigError(
                f"chunking source kind for role {self.role!r} is required"
            )


DEFAULT_CORPUS_DEFINITIONS: dict[str, CorpusDefinition] = {
    "docs": CorpusDefinition(
        role="docs",
        name="flink-docs-2.2",
        description="Apache Flink 2.2 documentation and selected Javadocs.",
        chunking_source_kind="docs",
        env_vars=("K2_DOCS_CORPUS_ID", "K2_FLINK_DOCS_CORPUS_ID"),
    ),
    "code": CorpusDefinition(
        role="code",
        name="flink-code-2.2",
        description="Apache Flink source, tests, build files, and implementation patterns.",
        chunking_source_kind="code",
        env_vars=("K2_CODE_CORPUS_ID", "K2_FLINK_CODE_CORPUS_ID"),
    ),
    "guides": CorpusDefinition(
        role="guides",
        name="java-rd-guides",
        description="Generated Java R&D engineering guides.",
        chunking_source_kind="guide",
        env_vars=("K2_GUIDES_CORPUS_ID", "K2_JAVA_RD_GUIDES_CORPUS_ID"),
    ),
}


def _default_corpus_definitions() -> dict[str, CorpusDefinition]:
    return dict(DEFAULT_CORPUS_DEFINITIONS)


@dataclass(frozen=True)
class LiveK2Config:
    project_name: str = "java-rd-demo"
    project_id: str | None = None
    corpus_ids: Mapping[str, str] = field(default_factory=dict)
    corpus_definitions: Mapping[str, CorpusDefinition] = field(
        default_factory=_default_corpus_definitions
    )
    org_id: str | None = None
    org_name: str | None = None
    api_host: str | None = None

    @classmethod
    def from_env(
        cls,
        environ: Mapping[str, str] | None = None,
        *,
        require_api_key: bool = True,
    ) -> "LiveK2Config":
        """Build non-secret live config from environment variables.

        The API key is validated but never stored on the returned dataclass, so
        serializing orchestration results cannot leak credentials.
        """

        env = os.environ if environ is None else environ
        if require_api_key and not _clean_optional(env.get("K2_API_KEY")):
            raise LiveK2ConfigError("missing required environment variable: K2_API_KEY")

        definitions = _default_corpus_definitions()
        corpus_ids: dict[str, str] = {}
        for role, definition in definitions.items():
            for env_var in definition.env_vars:
                value = _clean_optional(env.get(env_var))
                if value:
                    corpus_ids[role] = value
                    break

        return cls(
            project_name=_clean_optional(env.get("K2_PROJECT_NAME")) or "java-rd-demo",
            project_id=_clean_optional(env.get("K2_PROJECT_ID")),
            corpus_ids=corpus_ids,
            corpus_definitions=definitions,
            org_id=_clean_optional(env.get("K2_ORG_ID")),
            org_name=_clean_optional(env.get("K2_ORG_NAME")),
            api_host=_clean_optional(env.get("K2_API_HOST"))
            or _clean_optional(env.get("K2_BASE_URL")),
        )


@dataclass(frozen=True)
class ProjectSetupResult:
    project_id: str
    project_name: str
    created: bool
    response: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CorpusSetupResult:
    role: str
    corpus_id: str
    name: str
    created: bool
    response: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LiveK2SetupResult:
    project: ProjectSetupResult
    corpora: Mapping[str, CorpusSetupResult]

    @property
    def project_id(self) -> str:
        return self.project.project_id

    @property
    def corpus_ids(self) -> dict[str, str]:
        return {role: result.corpus_id for role, result in self.corpora.items()}

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class UploadResult:
    role: str
    corpus_id: str
    document_count: int
    chunking: dict[str, Any]
    response: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SyncResult:
    role: str
    corpus_id: str
    wait: bool
    response: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReadinessProbe:
    name: str
    role: str
    query: str
    filters: Mapping[str, Any]
    min_results: int = 1
    top_k: int = 12

    def __post_init__(self) -> None:
        _require_non_empty(self.name, "probe name")
        _require_non_empty(self.role, f"corpus role for probe {self.name!r}")
        _require_non_empty(self.query, f"query for probe {self.name!r}")
        if self.min_results < 1:
            raise LiveK2ConfigError(f"probe {self.name!r} min_results must be at least 1")
        if self.top_k < 1:
            raise LiveK2ConfigError(f"probe {self.name!r} top_k must be at least 1")


@dataclass(frozen=True)
class ReadinessProbeResult:
    name: str
    role: str
    corpus_id: str
    query: str
    min_results: int
    result_count: int
    passed: bool
    error: str | None = None
    response: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LiveK2RunResult:
    setup: LiveK2SetupResult
    uploads: Mapping[str, UploadResult] = field(default_factory=dict)
    syncs: Mapping[str, SyncResult] = field(default_factory=dict)
    probes: tuple[ReadinessProbeResult, ...] = ()

    @property
    def project_id(self) -> str:
        return self.setup.project_id

    @property
    def corpus_ids(self) -> dict[str, str]:
        return self.setup.corpus_ids

    @property
    def ready(self) -> bool:
        return bool(self.probes) and all(probe.passed for probe in self.probes)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def default_readiness_probes() -> tuple[ReadinessProbe, ...]:
    return (
        ReadinessProbe(
            name="flink_checkpoint_docs_or_guides",
            role="docs",
            query="how do I add a REST API endpoint for checkpoint information",
            filters=flink_checkpoint_docs_or_guides_filter(),
            min_results=3,
            top_k=12,
        ),
        ReadinessProbe(
            name="flink_rest_code",
            role="code",
            query="REST handler implementation pattern for job checkpoint endpoint",
            filters=flink_rest_code_filter(),
            min_results=5,
            top_k=12,
        ),
    )


def ensure_project(
    client: Any,
    config: LiveK2Config | None = None,
    *,
    create_missing: bool = False,
) -> ProjectSetupResult:
    selected = config or LiveK2Config()
    project_id = _clean_optional(selected.project_id)
    project_name = _require_non_empty(selected.project_name, "project name")

    if project_id:
        return ProjectSetupResult(project_id=project_id, project_name=project_name, created=False)
    if not create_missing:
        raise LiveK2ConfigError("K2_PROJECT_ID is required when create_missing=False")

    create_project = _require_method(client, "create_project")
    kwargs: dict[str, str] = {}
    if selected.org_id:
        kwargs["org_id"] = selected.org_id
    if selected.org_name:
        kwargs["org_name"] = selected.org_name
    response = create_project(project_name, **kwargs)
    return ProjectSetupResult(
        project_id=_extract_id(response, "project"),
        project_name=project_name,
        created=True,
        response=_response_mapping(response),
    )


def ensure_corpora(
    client: Any,
    project_id: str,
    config: LiveK2Config | None = None,
    *,
    roles: Iterable[str] | None = None,
    create_missing: bool = False,
) -> dict[str, CorpusSetupResult]:
    selected = config or LiveK2Config()
    normalized_project_id = _require_non_empty(project_id, "project id")
    existing_ids = _normalized_id_mapping(selected.corpus_ids, "corpus_ids")
    definitions = dict(selected.corpus_definitions)
    selected_roles = _ordered_roles(roles or definitions.keys())
    results: dict[str, CorpusSetupResult] = {}

    for role in selected_roles:
        _require_non_empty(role, "corpus role")
        definition = definitions.get(role)
        existing_id = existing_ids.get(role)
        if existing_id:
            results[role] = CorpusSetupResult(
                role=role,
                corpus_id=existing_id,
                name=definition.name if definition else role,
                created=False,
            )
            continue
        if not create_missing:
            raise LiveK2ConfigError(
                f"corpus id for role {role!r} is required when create_missing=False"
            )
        if definition is None:
            raise LiveK2ConfigError(f"missing corpus definition for role {role!r}")

        create_corpus = _require_method(client, "create_corpus")
        response = create_corpus(
            normalized_project_id,
            definition.name,
            description=definition.description,
        )
        results[role] = CorpusSetupResult(
            role=role,
            corpus_id=_extract_id(response, "corpus"),
            name=definition.name,
            created=True,
            response=_response_mapping(response),
        )

    return results


def ensure_live_project_and_corpora(
    client: Any,
    config: LiveK2Config | None = None,
    *,
    roles: Iterable[str] | None = None,
    create_missing: bool = False,
) -> LiveK2SetupResult:
    selected = config or LiveK2Config()
    project = ensure_project(client, selected, create_missing=create_missing)
    corpora = ensure_corpora(
        client,
        project.project_id,
        selected,
        roles=roles,
        create_missing=create_missing,
    )
    return LiveK2SetupResult(project=project, corpora=corpora)


def load_jsonl_documents_by_role(
    jsonl_paths: Iterable[str | Path],
) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for jsonl_path in jsonl_paths:
        for item in read_jsonl(jsonl_path):
            role = _document_role(item)
            grouped.setdefault(role, []).append(item)
    return grouped


def upload_documents_by_role(
    client: Any,
    documents_by_role: Mapping[str, Iterable[Mapping[str, Any]]],
    corpus_ids: Mapping[str, str],
    *,
    corpus_definitions: Mapping[str, CorpusDefinition] | None = None,
    chunking_by_role: Mapping[str, Mapping[str, Any]] | None = None,
    auto_index: bool = False,
    poll_s: int = 5,
    timeout_s: float | None = None,
    idempotency_prefix: str | None = None,
) -> dict[str, UploadResult]:
    upload = _resolve_batch_upload_method(client)
    definitions = dict(corpus_definitions or DEFAULT_CORPUS_DEFINITIONS)
    normalized_corpus_ids = _normalized_id_mapping(corpus_ids, "corpus_ids")
    results: dict[str, UploadResult] = {}

    for role, documents in documents_by_role.items():
        normalized_role = _require_non_empty(role, "corpus role")
        docs = [_validated_document_dict(document) for document in documents]
        if not docs:
            continue
        corpus_id = _lookup_corpus_id(normalized_corpus_ids, normalized_role)
        chunking = _chunking_for_role(normalized_role, definitions, chunking_by_role)
        kwargs: dict[str, Any] = {
            "auto_index": auto_index,
            "chunking": chunking,
            "poll_s": poll_s,
        }
        if timeout_s is not None:
            kwargs["timeout_s"] = timeout_s
        idempotency_key = _idempotency_key(idempotency_prefix, normalized_role, "upload")
        if idempotency_key:
            kwargs["idempotency_key"] = idempotency_key

        response = upload(corpus_id, docs, **kwargs)
        results[normalized_role] = UploadResult(
            role=normalized_role,
            corpus_id=corpus_id,
            document_count=len(docs),
            chunking=chunking,
            response=_response_mapping(response),
        )

    return results


def _resolve_batch_upload_method(client: Any) -> Any:
    upload_and_wait = getattr(client, "upload_documents_batch_and_wait", None)
    if callable(upload_and_wait):
        return upload_and_wait

    upload_batch = getattr(client, "upload_documents_batch", None)
    if not callable(upload_batch):
        raise LiveK2ClientError(
            "client missing required method 'upload_documents_batch_and_wait' "
            "or 'upload_documents_batch'"
        )

    def upload_with_wait(corpus_id: str, docs: list[dict[str, Any]], **kwargs: Any) -> Any:
        return upload_batch(corpus_id, docs, wait=True, **kwargs)

    return upload_with_wait


def sync_corpus_indexes(
    client: Any,
    corpus_ids: Mapping[str, str],
    *,
    roles: Iterable[str] | None = None,
    wait: bool = True,
    poll_s: int = 5,
    idempotency_prefix: str | None = None,
) -> dict[str, SyncResult]:
    sync_indexes = _require_method(client, "sync_indexes")
    normalized_corpus_ids = _normalized_id_mapping(corpus_ids, "corpus_ids")
    selected_roles = _ordered_roles(roles or normalized_corpus_ids.keys())
    results: dict[str, SyncResult] = {}

    for role in selected_roles:
        corpus_id = _lookup_corpus_id(normalized_corpus_ids, role)
        kwargs: dict[str, Any] = {"wait": wait, "poll_s": poll_s}
        idempotency_key = _idempotency_key(idempotency_prefix, role, "sync")
        if idempotency_key:
            kwargs["idempotency_key"] = idempotency_key
        response = sync_indexes(corpus_id, **kwargs)
        results[role] = SyncResult(
            role=role,
            corpus_id=corpus_id,
            wait=wait,
            response=_response_mapping(response),
        )

    return results


def run_readiness_probes(
    client: Any,
    corpus_ids: Mapping[str, str],
    probes: Iterable[ReadinessProbe] | None = None,
    *,
    hybrid: Mapping[str, Any] | None = None,
    return_config: Mapping[str, Any] | None = None,
    raise_on_error: bool = False,
) -> tuple[ReadinessProbeResult, ...]:
    search = _require_method(client, "search")
    normalized_corpus_ids = _normalized_id_mapping(corpus_ids, "corpus_ids")
    selected_hybrid = dict(hybrid or DEMO_HYBRID)
    selected_return = dict(return_config or DEMO_RETURN)
    results: list[ReadinessProbeResult] = []

    for probe in tuple(probes or default_readiness_probes()):
        corpus_id = _lookup_corpus_id(normalized_corpus_ids, probe.role)
        try:
            response = search(
                corpus_id,
                probe.query,
                top_k=probe.top_k,
                filters=dict(probe.filters),
                hybrid=selected_hybrid,
                return_config=selected_return,
            )
            result_count = _search_result_count(response)
            results.append(
                ReadinessProbeResult(
                    name=probe.name,
                    role=probe.role,
                    corpus_id=corpus_id,
                    query=probe.query,
                    min_results=probe.min_results,
                    result_count=result_count,
                    passed=result_count >= probe.min_results,
                    response=_response_mapping(response),
                )
            )
        except Exception as exc:
            message = _safe_error_message(exc)
            if raise_on_error:
                raise LiveK2ClientError(
                    f"readiness probe {probe.name!r} failed: {message}"
                ) from exc
            results.append(
                ReadinessProbeResult(
                    name=probe.name,
                    role=probe.role,
                    corpus_id=corpus_id,
                    query=probe.query,
                    min_results=probe.min_results,
                    result_count=0,
                    passed=False,
                    error=message,
                )
            )

    return tuple(results)


def orchestrate_live_k2(
    client: Any,
    *,
    jsonl_paths: Iterable[str | Path] = (),
    config: LiveK2Config | None = None,
    probes: Iterable[ReadinessProbe] | None = None,
    roles: Iterable[str] | None = None,
    create_missing: bool = False,
    run_sync: bool = True,
    run_probes: bool = True,
    auto_index: bool = False,
    idempotency_prefix: str | None = None,
) -> LiveK2RunResult:
    selected = config or LiveK2Config()
    documents_by_role = load_jsonl_documents_by_role(jsonl_paths)
    selected_probes = tuple(probes or default_readiness_probes()) if run_probes else ()
    setup_roles = _ordered_roles(
        list(roles or [])
        + list(documents_by_role.keys())
        + [probe.role for probe in selected_probes]
    )
    if not setup_roles:
        setup_roles = _ordered_roles(selected.corpus_definitions.keys())

    setup = ensure_live_project_and_corpora(
        client,
        selected,
        roles=setup_roles,
        create_missing=create_missing,
    )
    corpus_ids = setup.corpus_ids
    uploads = upload_documents_by_role(
        client,
        documents_by_role,
        corpus_ids,
        corpus_definitions=selected.corpus_definitions,
        auto_index=auto_index,
        idempotency_prefix=idempotency_prefix,
    )
    syncs = (
        sync_corpus_indexes(
            client,
            corpus_ids,
            roles=setup_roles,
            idempotency_prefix=idempotency_prefix,
        )
        if run_sync
        else {}
    )
    probe_results = (
        run_readiness_probes(client, corpus_ids, selected_probes) if run_probes else ()
    )

    return LiveK2RunResult(
        setup=setup,
        uploads=uploads,
        syncs=syncs,
        probes=probe_results,
    )


def _clean_optional(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _require_non_empty(value: str | None, label: str) -> str:
    stripped = _clean_optional(value)
    if stripped is None:
        raise LiveK2ConfigError(f"{label} is required")
    return stripped


def _require_method(client: Any, method_name: str) -> Any:
    method = getattr(client, method_name, None)
    if not callable(method):
        raise LiveK2ClientError(f"client missing required method {method_name!r}")
    return method


def _extract_id(response: Any, label: str) -> str:
    if isinstance(response, Mapping):
        candidates = ("id", f"{label}_id")
        for key in candidates:
            value = _clean_optional(str(response[key])) if key in response else None
            if value:
                return value
    value = getattr(response, "id", None)
    if value is not None:
        cleaned = _clean_optional(str(value))
        if cleaned:
            return cleaned
    raise LiveK2ClientError(f"{label} response did not include an id")


def _response_mapping(response: Any) -> dict[str, Any] | None:
    if isinstance(response, Mapping):
        return dict(response)
    return None


def _normalized_id_mapping(value: Mapping[str, str], label: str) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for role, item_id in value.items():
        normalized_role = _require_non_empty(str(role), f"{label} role")
        normalized_id = _require_non_empty(str(item_id), f"{label}[{normalized_role!r}]")
        normalized[normalized_role] = normalized_id
    return normalized


def _ordered_roles(roles: Iterable[str]) -> list[str]:
    ordered: list[str] = []
    for role in roles:
        normalized = _require_non_empty(str(role), "corpus role")
        if normalized not in ordered:
            ordered.append(normalized)
    return ordered


def _lookup_corpus_id(corpus_ids: Mapping[str, str], role: str) -> str:
    normalized_role = _require_non_empty(role, "corpus role")
    corpus_id = _clean_optional(corpus_ids.get(normalized_role))
    if not corpus_id:
        raise LiveK2ConfigError(f"missing corpus id for role {normalized_role!r}")
    return corpus_id


def _document_role(document: Mapping[str, Any]) -> str:
    metadata = document.get("metadata")
    if not isinstance(metadata, Mapping):
        raise LiveK2ConfigError("document metadata must be an object")
    role = metadata.get("corpus_role")
    if not isinstance(role, str):
        raise LiveK2ConfigError("document metadata missing corpus_role")
    return _require_non_empty(role, "document metadata corpus_role")


def _validated_document_dict(document: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(document, Mapping):
        raise LiveK2ConfigError("document must be an object")
    metadata = document.get("metadata")
    if not isinstance(metadata, dict):
        raise LiveK2ConfigError("document metadata must be a dict")
    validate_metadata(metadata)
    if not _clean_optional(str(document.get("source_uri", ""))):
        raise LiveK2ConfigError("document source_uri is required")
    if not _clean_optional(str(document.get("raw_text", ""))):
        raise LiveK2ConfigError("document raw_text is required")
    return dict(document)


def _chunking_for_role(
    role: str,
    definitions: Mapping[str, CorpusDefinition],
    chunking_by_role: Mapping[str, Mapping[str, Any]] | None,
) -> dict[str, Any]:
    if chunking_by_role and role in chunking_by_role:
        return dict(chunking_by_role[role])
    definition = definitions.get(role)
    source_kind = definition.chunking_source_kind if definition else role
    return chunking_for_source_kind(source_kind)


def _idempotency_key(prefix: str | None, role: str, operation: str) -> str | None:
    cleaned_prefix = _clean_optional(prefix)
    if not cleaned_prefix:
        return None
    safe_role = re.sub(r"[^A-Za-z0-9_.-]+", "-", role)
    return f"{cleaned_prefix}-{safe_role}-{operation}"


def _search_result_count(response: Any) -> int:
    if isinstance(response, Mapping):
        for key in ("results", "chunks", "documents"):
            value = response.get(key)
            if _is_sequence(value):
                return len(value)
        for key in ("count", "total", "total_results"):
            value = response.get(key)
            if isinstance(value, int):
                return value
        return 0
    if _is_sequence(response):
        return len(response)
    return 0


def _is_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _safe_error_message(exc: Exception) -> str:
    message = str(exc)
    patterns = (
        r"(?i)(api[_-]?key\s*[=:]\s*)\S+",
        r"(?i)(authorization\s*[=:]\s*)\S+",
        r"(?i)(bearer\s+)\S+",
        r"(?i)(token\s*[=:]\s*)\S+",
        r"(?i)(secret\s*[=:]\s*)\S+",
        r"(?i)(password\s*[=:]\s*)\S+",
    )
    for pattern in patterns:
        message = re.sub(pattern, r"\1<redacted>", message)
    if not message:
        return type(exc).__name__
    return f"{type(exc).__name__}: {message}"
