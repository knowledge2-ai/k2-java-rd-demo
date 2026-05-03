"""Deterministic OSS source catalog for the Java R&D demo."""

from __future__ import annotations

import json
from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Iterable, Mapping

from .metadata import DEMO_DATASET_ID

FLINK_DOCS_ENTRYPOINT = "https://nightlies.apache.org/flink/flink-docs-release-2.2/"
KAFKA_DOCS_ENTRYPOINT = "https://kafka.apache.org/42/"
KAFKA_CONNECT_GUIDE = "https://kafka.apache.org/42/kafka-connect/connector-development-guide/"

FRAMEWORK_ORDER = ("flink", "kafka")


class CliSerializable:
    """Mixin for stable CLI-friendly dictionary and JSON output."""

    def to_dict(self) -> dict[str, Any]:
        return _jsonable(self)

    def to_json(self, *, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)


@dataclass(frozen=True, kw_only=True)
class DocsSourceManifest(CliSerializable):
    framework: str
    version: str
    repo: str
    repo_ref: str
    corpus_name: str
    corpus_role: str = "docs"
    source_kind: str = "docs"
    doc_type: str = "release_docs"
    seed_urls: tuple[str, ...] = ()
    clone_urls: tuple[str, ...] = ()
    include_paths: tuple[str, ...] = ()
    exclude_paths: tuple[str, ...] = ()
    description: str = ""

    def __post_init__(self) -> None:
        _validate_common_source(self)
        if not self.seed_urls:
            raise ValueError("docs source manifests require at least one seed URL")


@dataclass(frozen=True, kw_only=True)
class CodeSourceManifest(CliSerializable):
    framework: str
    version: str
    repo: str
    repo_ref: str
    corpus_name: str
    corpus_role: str = "code"
    source_kind: str = "code"
    source_kinds: tuple[str, ...] = ("code", "test", "build", "config")
    seed_urls: tuple[str, ...] = ()
    clone_urls: tuple[str, ...] = ()
    include_paths: tuple[str, ...] = ()
    exclude_paths: tuple[str, ...] = ()
    description: str = ""

    def __post_init__(self) -> None:
        _validate_common_source(self)
        object.__setattr__(self, "source_kinds", _string_tuple(self.source_kinds))
        if not self.clone_urls:
            raise ValueError("code source manifests require at least one clone URL")


SourceManifest = DocsSourceManifest | CodeSourceManifest


@dataclass(frozen=True, kw_only=True)
class IngestionManifest(CliSerializable):
    dataset_id: str
    project_name: str
    frameworks: tuple[str, ...]
    include_kafka: bool
    docs_sources: tuple[DocsSourceManifest, ...]
    code_sources: tuple[CodeSourceManifest, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "frameworks", _string_tuple(self.frameworks))
        object.__setattr__(self, "docs_sources", tuple(self.docs_sources))
        object.__setattr__(self, "code_sources", tuple(self.code_sources))
        if not self.frameworks:
            raise ValueError("ingestion manifest requires at least one framework")

    @property
    def sources(self) -> tuple[SourceManifest, ...]:
        return (*self.docs_sources, *self.code_sources)


def _validate_common_source(source: SourceManifest) -> None:
    for name in ("framework", "version", "repo", "repo_ref", "corpus_name"):
        value = getattr(source, name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{name} is required")

    for name in ("seed_urls", "clone_urls", "include_paths", "exclude_paths"):
        object.__setattr__(source, name, _string_tuple(getattr(source, name)))


def _string_tuple(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(str(value).strip() for value in values if str(value).strip())


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {
            field.name: _jsonable(getattr(value, field.name))
            for field in fields(value)
        }
    if isinstance(value, tuple | list):
        return [_jsonable(item) for item in value]
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    return value


FLINK_DOCS_SOURCE = DocsSourceManifest(
    framework="flink",
    version="2.2.0",
    repo="apache/flink",
    repo_ref="release-2.2.0",
    corpus_name="flink-docs-2.2",
    seed_urls=(FLINK_DOCS_ENTRYPOINT,),
    clone_urls=("https://github.com/apache/flink.git",),
    include_paths=(
        "flink-docs-release-2.2/",
        "docs/dev/datastream/",
        "docs/dev/table/",
        "docs/ops/rest_api/",
        "docs/connectors/",
        "docs/deployment/",
        "docs/flinkDev/",
    ),
    exclude_paths=(
        "flink-docs-master/",
        "flink-docs-release-1.",
        "flink-docs-release-2.0/",
        "flink-docs-release-2.1/",
    ),
    description="Apache Flink 2.2 release documentation and selected Javadocs.",
)

FLINK_CODE_SOURCE = CodeSourceManifest(
    framework="flink",
    version="2.2.0",
    repo="apache/flink",
    repo_ref="release-2.2.0",
    corpus_name="flink-code-2.2",
    clone_urls=("https://github.com/apache/flink.git",),
    include_paths=(
        "flink-runtime/src/main/java/",
        "flink-runtime/src/test/java/",
        "flink-core/src/main/java/",
        "flink-core/src/test/java/",
        "flink-connectors/",
        "flink-libraries/",
        "flink-table/",
        "flink-docs/",
        "pom.xml",
    ),
    exclude_paths=(
        ".git/",
        ".github/",
        ".gradle/",
        "build/",
        "target/",
        "dist/",
        "out/",
        "node_modules/",
        "generated/",
    ),
    description="Apache Flink source, tests, build files, and implementation patterns.",
)

KAFKA_DOCS_SOURCE = DocsSourceManifest(
    framework="kafka",
    version="4.2.0",
    repo="apache/kafka-site",
    repo_ref="4.2",
    corpus_name="kafka-docs-4.2",
    seed_urls=(KAFKA_DOCS_ENTRYPOINT, KAFKA_CONNECT_GUIDE),
    clone_urls=("https://github.com/apache/kafka-site.git",),
    include_paths=(
        "42/",
        "42/kafka-connect/",
        "42/kafka-connect/connector-development-guide/",
        "42/streams/",
        "42/generated/",
        "42/documentation/",
    ),
    exclude_paths=(
        "40/",
        "41/",
        "trunk/",
        "latest/",
    ),
    description="Apache Kafka 4.2 documentation, including Kafka Connect development.",
)

KAFKA_CODE_SOURCE = CodeSourceManifest(
    framework="kafka",
    version="4.2.0",
    repo="apache/kafka",
    repo_ref="4.2",
    corpus_name="kafka-code-4.2",
    clone_urls=("https://github.com/apache/kafka.git",),
    include_paths=(
        "clients/src/main/java/",
        "connect/api/src/main/java/",
        "connect/runtime/src/main/java/",
        "connect/runtime/src/test/java/",
        "connect/transforms/src/main/java/",
        "streams/src/main/java/",
        "streams/src/test/java/",
        "core/src/main/scala/",
        "server/src/main/java/",
        "build.gradle",
    ),
    exclude_paths=(
        ".git/",
        ".github/",
        ".gradle/",
        "build/",
        "gradle/",
        "generated/",
        "out/",
        "node_modules/",
    ),
    description="Apache Kafka source, tests, examples, and Connect/Streams patterns.",
)

_DOCS_BY_FRAMEWORK: Mapping[str, DocsSourceManifest] = {
    "flink": FLINK_DOCS_SOURCE,
    "kafka": KAFKA_DOCS_SOURCE,
}

_CODE_BY_FRAMEWORK: Mapping[str, CodeSourceManifest] = {
    "flink": FLINK_CODE_SOURCE,
    "kafka": KAFKA_CODE_SOURCE,
}


def docs_source_manifests(
    selected_frameworks: Iterable[str] | str | None = None,
    *,
    include_kafka: bool = False,
) -> tuple[DocsSourceManifest, ...]:
    frameworks = normalize_frameworks(selected_frameworks, include_kafka=include_kafka)
    return tuple(_DOCS_BY_FRAMEWORK[framework] for framework in frameworks)


def code_source_manifests(
    selected_frameworks: Iterable[str] | str | None = None,
    *,
    include_kafka: bool = False,
) -> tuple[CodeSourceManifest, ...]:
    frameworks = normalize_frameworks(selected_frameworks, include_kafka=include_kafka)
    return tuple(_CODE_BY_FRAMEWORK[framework] for framework in frameworks)


def build_ingestion_manifest(
    selected_frameworks: Iterable[str] | str | None = None,
    *,
    include_kafka: bool = False,
    project_name: str = "java-rd-demo",
) -> IngestionManifest:
    """Build the deterministic source manifest for Flink only or Flink plus Kafka."""

    frameworks = normalize_frameworks(selected_frameworks, include_kafka=include_kafka)
    return IngestionManifest(
        dataset_id=DEMO_DATASET_ID,
        project_name=project_name,
        frameworks=frameworks,
        include_kafka="kafka" in frameworks,
        docs_sources=docs_source_manifests(frameworks),
        code_sources=code_source_manifests(frameworks),
    )


def normalize_frameworks(
    selected_frameworks: Iterable[str] | str | None = None,
    *,
    include_kafka: bool = False,
) -> tuple[str, ...]:
    requested = set(_iter_framework_names(selected_frameworks))
    if not requested:
        requested.add("flink")
    if include_kafka or "kafka" in requested:
        requested.update({"flink", "kafka"})

    unknown = requested.difference(FRAMEWORK_ORDER)
    if unknown:
        raise ValueError(f"unsupported source catalog framework(s): {sorted(unknown)}")

    return tuple(framework for framework in FRAMEWORK_ORDER if framework in requested)


def manifest_to_json(manifest: IngestionManifest, *, indent: int | None = 2) -> str:
    return manifest.to_json(indent=indent)


def _iter_framework_names(selected_frameworks: Iterable[str] | str | None) -> tuple[str, ...]:
    if selected_frameworks is None:
        return ()

    raw_values: Iterable[str]
    if isinstance(selected_frameworks, str):
        raw_values = (selected_frameworks,)
    else:
        raw_values = selected_frameworks

    names: list[str] = []
    for raw_value in raw_values:
        for part in str(raw_value).split(","):
            name = part.strip().lower()
            if name and name not in names:
                names.append(name)
    return tuple(names)


__all__ = [
    "CodeSourceManifest",
    "DocsSourceManifest",
    "FLINK_CODE_SOURCE",
    "FLINK_DOCS_ENTRYPOINT",
    "FLINK_DOCS_SOURCE",
    "FRAMEWORK_ORDER",
    "IngestionManifest",
    "KAFKA_CODE_SOURCE",
    "KAFKA_CONNECT_GUIDE",
    "KAFKA_DOCS_ENTRYPOINT",
    "KAFKA_DOCS_SOURCE",
    "SourceManifest",
    "build_ingestion_manifest",
    "code_source_manifests",
    "docs_source_manifests",
    "manifest_to_json",
    "normalize_frameworks",
]
