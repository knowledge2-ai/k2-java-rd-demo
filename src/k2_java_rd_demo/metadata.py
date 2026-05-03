"""Metadata contract and source-code enrichment for the Java R&D demo."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

DEMO_DATASET_ID = "java-rd-oss-2026-04"

METADATA_MAX_KEYS = 50
METADATA_MAX_TOTAL_BYTES = 10 * 1024
METADATA_MAX_VALUE_BYTES = 1024

RESERVED_CUSTOM_KEYS = {
    "document_id",
    "source_uri",
    "provenance",
    "chunk_index",
    "page_start",
    "page_end",
}

REQUIRED_METADATA_KEYS = {
    "demo_dataset_id",
    "corpus_role",
    "framework",
    "framework_version",
    "source_kind",
    "artifact_type",
    "language",
    "license",
    "repo",
    "repo_ref",
    "path",
    "module",
    "api_surface",
    "topic",
    "audience",
    "stability",
    "tags",
}

BUILD_FILE_NAMES = {
    "pom.xml",
    "build.gradle",
    "settings.gradle",
    "gradle.properties",
    "maven-wrapper.properties",
}

CONFIG_SUFFIXES = {
    ".properties",
    ".yaml",
    ".yml",
    ".conf",
    ".ini",
}

LANGUAGE_BY_SUFFIX = {
    ".java": "java",
    ".scala": "scala",
    ".kt": "kotlin",
    ".md": "markdown",
    ".html": "html",
    ".htm": "html",
    ".xml": "xml",
    ".properties": "properties",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".gradle": "gradle",
}


class MetadataValidationError(ValueError):
    """Raised when a document's custom metadata is not K2-demo compatible."""


def posix_path(path: str | Path) -> str:
    return Path(path).as_posix()


def infer_language(path: str | Path) -> str:
    p = Path(path)
    return LANGUAGE_BY_SUFFIX.get(p.suffix.lower(), "text")


def infer_source_kind(path: str | Path) -> str:
    p = posix_path(path).lower()
    name = Path(path).name.lower()

    if "/src/test/" in p or name.endswith("test.java") or name.endswith("tests.java"):
        return "test"
    if name in BUILD_FILE_NAMES or name.endswith(".gradle"):
        return "build"
    if Path(path).suffix.lower() in CONFIG_SUFFIXES:
        return "config"
    if Path(path).suffix.lower() in {".md", ".html", ".htm"}:
        return "docs"
    return "code"


def infer_artifact_type(path: str | Path, source_kind: str) -> str:
    if source_kind == "test":
        p = posix_path(path).lower()
        if "itcase" in p or "integration" in p:
            return "integration_test"
        return "unit_test"
    if source_kind == "build":
        return "build_config"
    if source_kind == "config":
        return "runtime_config"
    if source_kind == "docs":
        return "reference"
    return "source"


def infer_module(path: str | Path) -> str:
    parts = Path(path).parts
    if not parts:
        return "root"
    first = parts[0]
    if first in {"src", "docs", "documentation"}:
        return first
    return first or "root"


def infer_api_surface(path: str | Path, text: str = "") -> str:
    path_haystack = posix_path(path).lower()
    for surface, tokens in [
        ("connect", ("connect", "connector", "configdef")),
        ("checkpointing", ("checkpoint", "savepoint")),
    ]:
        if any(token in path_haystack for token in tokens):
            return surface

    haystack = f"{path_haystack} {text[:2000].lower()}"
    checks = [
        ("connect", ("connect", "connector", "configdef")),
        ("rest", ("rest", "handler", "endpoint")),
        ("checkpointing", ("checkpoint", "savepoint")),
        ("datastream", ("datastream", "streamoperator")),
        ("table-sql", ("table api", "sql", "planner")),
        ("streams", ("streams", "kstream", "processor")),
        ("configuration", ("config", "configuration")),
        ("state", ("state", "statebackend")),
        ("metrics", ("metric", "reporter")),
    ]
    for surface, tokens in checks:
        if any(token in haystack for token in tokens):
            return surface
    return "general"


def infer_topic(api_surface: str, source_kind: str) -> str:
    if source_kind == "test":
        return f"{api_surface}-testing"
    return api_surface


def infer_audience(source_kind: str, api_surface: str) -> str:
    if source_kind in {"code", "test", "build", "config"}:
        return "framework_contributor"
    if api_surface == "connect":
        return "connector_author"
    if api_surface in {"configuration", "metrics"}:
        return "platform_operator"
    return "application_developer"


def infer_stability(source_kind: str, path: str | Path) -> str:
    if source_kind == "test":
        return "test_only"
    p = posix_path(path).lower()
    if "/internal/" in p or ".internal." in p:
        return "internal"
    if "experimental" in p:
        return "experimental"
    return "internal" if source_kind == "code" else "public_api"


PACKAGE_RE = re.compile(r"^\s*package\s+([\w.]+)\s*;", re.MULTILINE)
TYPE_RE = re.compile(
    r"\b(?:(?:public|protected|private|abstract|final|static)\s+)*"
    r"(class|interface|enum|record)\s+([A-Za-z_]\w*)"
    r"(?:\s+extends\s+([A-Za-z_][\w.<>]*))?"
    r"(?:\s+implements\s+([A-Za-z_][\w.<>,\s]*))?",
    re.MULTILINE,
)
METHOD_RE = re.compile(
    r"\b(?:public|protected|private)\s+"
    r"(?:static\s+)?(?:final\s+)?[\w.<>\[\], ?]+\s+([A-Za-z_]\w*)\s*\(",
    re.MULTILINE,
)

SYMBOL_LIST_MAX_ITEMS = 20
SYMBOL_LIST_MAX_JSON_BYTES = 900
SYMBOL_NAME_MAX_CHARS = 96


def extract_java_symbols(text: str) -> dict[str, Any]:
    package_match = PACKAGE_RE.search(text)
    type_match = TYPE_RE.search(text)
    methods = []
    for match in METHOD_RE.finditer(text):
        name = match.group(1)
        if name not in {"if", "for", "while", "switch", "catch"} and name not in methods:
            methods.append(name)
        if len(methods) >= 20:
            break

    implements: list[str] = []
    if type_match and type_match.group(4):
        implements = [item.strip() for item in type_match.group(4).split(",") if item.strip()]
        implements = compact_metadata_list(implements, max_items=10)

    return {
        "java_package": package_match.group(1) if package_match else None,
        "symbol_kind": type_match.group(1) if type_match else None,
        "class_name": type_match.group(2) if type_match else None,
        "extends": type_match.group(3) if type_match and type_match.group(3) else None,
        "implements": implements,
        "symbols": compact_metadata_list(methods, max_items=SYMBOL_LIST_MAX_ITEMS),
    }


def compact_metadata_list(
    values: list[str],
    *,
    max_items: int,
    max_json_bytes: int = SYMBOL_LIST_MAX_JSON_BYTES,
) -> list[str]:
    compacted: list[str] = []
    for value in values:
        normalized = value.strip()
        if not normalized:
            continue
        if len(normalized) > SYMBOL_NAME_MAX_CHARS:
            normalized = normalized[:SYMBOL_NAME_MAX_CHARS]
        if normalized in compacted:
            continue
        candidate = [*compacted, normalized]
        if len(candidate) > max_items:
            break
        if len(json.dumps(candidate, sort_keys=True).encode("utf-8")) > max_json_bytes:
            break
        compacted.append(normalized)
    return compacted


def compact_tags(*values: str | None) -> list[str]:
    tags: list[str] = []
    for value in values:
        if not value:
            continue
        for raw in re.split(r"[^A-Za-z0-9_.-]+", value):
            tag = raw.strip().lower()
            if tag and tag not in tags:
                tags.append(tag)
    return tags[:20]


def build_code_metadata(
    *,
    path: str | Path,
    text: str,
    framework: str,
    framework_version: str,
    repo: str,
    repo_ref: str,
) -> dict[str, Any]:
    normalized_path = posix_path(path)
    source_kind = infer_source_kind(normalized_path)
    language = infer_language(normalized_path)
    module = infer_module(normalized_path)
    api_surface = infer_api_surface(normalized_path, text)
    topic = infer_topic(api_surface, source_kind)
    symbols = extract_java_symbols(text) if language == "java" else {}

    metadata: dict[str, Any] = {
        "demo_dataset_id": DEMO_DATASET_ID,
        "corpus_role": "code",
        "framework": framework,
        "framework_version": framework_version,
        "source_kind": source_kind,
        "artifact_type": infer_artifact_type(normalized_path, source_kind),
        "language": language,
        "license": "apache-2.0",
        "repo": repo,
        "repo_ref": repo_ref,
        "path": normalized_path,
        "module": module,
        "api_surface": api_surface,
        "topic": topic,
        "audience": infer_audience(source_kind, api_surface),
        "stability": infer_stability(source_kind, normalized_path),
        "tags": compact_tags(framework, module, api_surface, topic, source_kind),
    }

    for key, value in symbols.items():
        if value:
            metadata[key] = value
    if source_kind == "test":
        metadata["is_test"] = True
        if metadata.get("class_name"):
            metadata["test_target"] = str(metadata["class_name"]).removesuffix("Test")
    else:
        metadata["is_test"] = False

    validate_metadata(metadata)
    return metadata


def build_guide_metadata(
    *,
    framework: str,
    framework_version: str,
    path: str,
    guide_type: str,
    api_surface: str,
    topic: str,
    title: str,
) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "demo_dataset_id": DEMO_DATASET_ID,
        "corpus_role": "guides",
        "framework": framework,
        "framework_version": framework_version,
        "source_kind": "guide",
        "artifact_type": "how_to" if guide_type == "how_to" else guide_type,
        "language": "markdown",
        "license": "apache-2.0",
        "repo": "generated",
        "repo_ref": "demo-generated",
        "path": path,
        "module": "guides",
        "api_surface": api_surface,
        "topic": topic,
        "audience": "framework_contributor",
        "stability": "public_api",
        "tags": compact_tags(framework, api_surface, topic, guide_type, title),
        "guide_type": guide_type,
        "doc_section": "Engineering Guides",
        "nav_path": f"Engineering Guides > {title}",
        "heading_path": title,
    }
    validate_metadata(metadata)
    return metadata


def validate_metadata(metadata: dict[str, Any], *, require_demo_keys: bool = True) -> None:
    if not isinstance(metadata, dict):
        raise MetadataValidationError("metadata must be a dict")
    if len(metadata) > METADATA_MAX_KEYS:
        raise MetadataValidationError(f"metadata has more than {METADATA_MAX_KEYS} keys")
    reserved = RESERVED_CUSTOM_KEYS.intersection(metadata)
    if reserved:
        raise MetadataValidationError(f"metadata contains reserved K2 keys: {sorted(reserved)}")
    if require_demo_keys:
        missing = REQUIRED_METADATA_KEYS.difference(metadata)
        if missing:
            raise MetadataValidationError(f"metadata missing required keys: {sorted(missing)}")

    try:
        encoded = json.dumps(metadata, sort_keys=True, separators=(",", ":")).encode("utf-8")
    except TypeError as exc:
        raise MetadataValidationError(f"metadata is not JSON serializable: {exc}") from exc
    if len(encoded) > METADATA_MAX_TOTAL_BYTES:
        raise MetadataValidationError("metadata exceeds 10 KB")

    for key, value in metadata.items():
        if not isinstance(key, str) or not key:
            raise MetadataValidationError("metadata keys must be non-empty strings")
        value_bytes = json.dumps(value, sort_keys=True).encode("utf-8")
        if len(value_bytes) > METADATA_MAX_VALUE_BYTES:
            raise MetadataValidationError(f"metadata value for {key!r} exceeds 1 KB")
