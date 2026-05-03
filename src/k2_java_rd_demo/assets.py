"""Offline asset builders for K2-ready demo documents."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Any

from .metadata import build_code_metadata, build_guide_metadata, infer_source_kind, validate_metadata

DEFAULT_SUFFIXES = {
    ".java",
    ".scala",
    ".kt",
    ".md",
    ".xml",
    ".properties",
    ".yaml",
    ".yml",
    ".gradle",
}

EXCLUDED_DIR_NAMES = {
    ".git",
    ".idea",
    ".gradle",
    "target",
    "build",
    "dist",
    "out",
    "node_modules",
    "__pycache__",
    "generated",
}


@dataclass(frozen=True)
class DemoDocument:
    source_uri: str
    raw_text: str
    metadata: dict[str, Any]

    def to_k2_item(self) -> dict[str, Any]:
        validate_metadata(self.metadata)
        return {
            "source_uri": self.source_uri,
            "raw_text": self.raw_text,
            "metadata": self.metadata,
        }


def should_exclude(path: Path) -> bool:
    return any(part in EXCLUDED_DIR_NAMES for part in path.parts)


def iter_source_files(
    repo_root: str | Path,
    *,
    suffixes: set[str] | None = None,
    max_files: int | None = None,
) -> Iterator[Path]:
    root = Path(repo_root)
    selected_suffixes = suffixes or DEFAULT_SUFFIXES
    count = 0
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if should_exclude(rel):
            continue
        if path.suffix.lower() not in selected_suffixes and path.name not in {"pom.xml"}:
            continue
        yield path
        count += 1
        if max_files is not None and count >= max_files:
            return


def source_uri_for(repo: str, repo_ref: str, rel_path: str) -> str:
    return f"repo://{repo}@{repo_ref}/{rel_path}"


def build_raw_text_header(metadata: dict[str, Any]) -> str:
    lines = [
        f"Repository: {metadata.get('repo')}",
        f"Ref: {metadata.get('repo_ref')}",
        f"Path: {metadata.get('path')}",
        f"Module: {metadata.get('module')}",
        f"Framework: {metadata.get('framework')} {metadata.get('framework_version')}",
        f"Source kind: {metadata.get('source_kind')}",
        f"API surface: {metadata.get('api_surface')}",
    ]
    if metadata.get("java_package"):
        lines.append(f"Package: {metadata['java_package']}")
    if metadata.get("class_name"):
        lines.append(f"Class: {metadata['class_name']}")
    if metadata.get("extends"):
        lines.append(f"Extends: {metadata['extends']}")
    if metadata.get("implements"):
        lines.append(f"Implements: {', '.join(metadata['implements'])}")
    return "\n".join(lines) + "\n\n"


def build_documents_from_repo(
    repo_root: str | Path,
    *,
    framework: str,
    framework_version: str,
    repo: str,
    repo_ref: str,
    max_files: int | None = None,
) -> list[DemoDocument]:
    root = Path(repo_root)
    documents: list[DemoDocument] = []
    for file_path in iter_source_files(root, max_files=max_files):
        rel_path = file_path.relative_to(root).as_posix()
        text = file_path.read_text(encoding="utf-8", errors="replace")
        metadata = build_code_metadata(
            path=rel_path,
            text=text,
            framework=framework,
            framework_version=framework_version,
            repo=repo,
            repo_ref=repo_ref,
        )
        raw_text = build_raw_text_header(metadata) + text
        documents.append(
            DemoDocument(
                source_uri=source_uri_for(repo, repo_ref, rel_path),
                raw_text=raw_text,
                metadata=metadata,
            )
        )
    return documents


def generate_seed_guides(framework: str, framework_version: str) -> list[DemoDocument]:
    guides = [
        {
            "path": f"guides/{framework}/rest-handler-checklist.md",
            "title": "REST Handler Implementation Checklist",
            "guide_type": "how_to",
            "api_surface": "rest",
            "topic": "rest-api",
            "body": (
                "# REST Handler Implementation Checklist\n\n"
                "Use this guide before adding a controller-like endpoint.\n\n"
                "1. Start with the public API or REST documentation for the target version.\n"
                "2. Find an existing handler in the same module and API surface.\n"
                "3. Identify request parameters, response body classes, route registration, "
                "and handler tests.\n"
                "4. Search tests before editing production code.\n"
                "5. Cite the docs, source class, and neighboring test in the implementation plan.\n"
            ),
        },
        {
            "path": f"guides/{framework}/test-patterns.md",
            "title": "Test Pattern Selection",
            "guide_type": "test_checklist",
            "api_surface": "testing",
            "topic": "testing",
            "body": (
                "# Test Pattern Selection\n\n"
                "When adding Java functionality, retrieve tests with the same module and API "
                "surface. Prefer tests that exercise route registration, serialization, "
                "validation, and failure handling. Do not copy test-only helpers into "
                "production code without checking stability metadata.\n"
            ),
        },
    ]
    guides.extend(_customer_guardrail_guides(framework))

    documents: list[DemoDocument] = []
    for guide in guides:
        metadata = build_guide_metadata(
            framework=framework,
            framework_version=framework_version,
            path=guide["path"],
            guide_type=guide["guide_type"],
            api_surface=guide["api_surface"],
            topic=guide["topic"],
            title=guide["title"],
        )
        documents.append(
            DemoDocument(
                source_uri=f"generated://{guide['path']}",
                raw_text=guide["body"],
                metadata=metadata,
            )
        )
    return documents


def _customer_guardrail_guides(framework: str) -> list[dict[str, str]]:
    if framework == "flink":
        return [
            {
                "path": "guides/flink/confluence-rest-handler-guardrails.md",
                "title": "CF-FLINK-REST-001 REST Handler Guardrails",
                "guide_type": "guardrail",
                "api_surface": "rest",
                "topic": "rest-api",
                "body": (
                    "# CF-FLINK-REST-001 REST Handler Guardrails\n\n"
                    "This Confluence-style guide is the customer analogue for adding "
                    "controller-like Java endpoints.\n\n"
                    "Required guardrails:\n"
                    "- Do not add Spring MVC, servlet, or JAX-RS controllers.\n"
                    "- Implement Flink REST endpoints through `MessageHeaders`, "
                    "`AbstractRestHandler`, request/response message classes, and "
                    "`WebMonitorEndpoint` registration.\n"
                    "- Preserve existing JSON field naming and compatibility.\n"
                    "- Add or update handler and serialization tests before proposing the "
                    "change for review.\n"
                    "- The implementation plan must cite this guide, the target handler "
                    "source, and a neighboring test.\n"
                ),
            },
            {
                "path": "guides/flink/confluence-checkpoint-upgrade-guardrails.md",
                "title": "CF-FLINK-CKPT-004 Checkpointing Upgrade Guardrails",
                "guide_type": "guardrail",
                "api_surface": "checkpointing",
                "topic": "checkpointing",
                "body": (
                    "# CF-FLINK-CKPT-004 Checkpointing Upgrade Guardrails\n\n"
                    "Required guardrails:\n"
                    "- Do not resurrect deprecated `FsStateBackend` or "
                    "`MemoryStateBackend` patterns in new code.\n"
                    "- Use current checkpointing and savepoint configuration APIs for "
                    "Flink 2.2.\n"
                    "- Cite the version-pinned checkpointing docs, the production class, "
                    "and focused checkpointing tests.\n"
                    "- Call out migration risk explicitly when changing checkpointing "
                    "state or retention behavior.\n"
                ),
            },
        ]
    if framework == "kafka":
        return [
            {
                "path": "guides/kafka/confluence-connect-rest-entity-guardrails.md",
                "title": "CF-KAFKA-CONNECT-007 REST Entity Compatibility Guardrails",
                "guide_type": "guardrail",
                "api_surface": "connect",
                "topic": "connect",
                "body": (
                    "# CF-KAFKA-CONNECT-007 REST Entity Compatibility Guardrails\n\n"
                    "Required guardrails:\n"
                    "- Keep Kafka Connect REST entity changes backwards-compatible.\n"
                    "- Optional JSON fields must remain nullable or omitted when absent.\n"
                    "- Follow existing Jackson annotation and entity-test patterns.\n"
                    "- Do not introduce Spring Validator, Bean Validation, or "
                    "`javax.validation` into Connect REST entities.\n"
                    "- Cite this guide, the target REST entity, and the neighboring JSON "
                    "serialization/deserialization test.\n"
                ),
            },
        ]
    return []


def write_jsonl(documents: Iterable[DemoDocument], out_path: str | Path) -> int:
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for document in documents:
            handle.write(json.dumps(document.to_k2_item(), sort_keys=True) + "\n")
            count += 1
    return count


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            item = json.loads(stripped)
            if not isinstance(item, dict):
                raise ValueError(f"line {line_number}: item is not an object")
            metadata = item.get("metadata")
            if not isinstance(metadata, dict):
                raise ValueError(f"line {line_number}: missing metadata object")
            validate_metadata(metadata)
            if not item.get("source_uri") or not item.get("raw_text"):
                raise ValueError(f"line {line_number}: missing source_uri or raw_text")
            items.append(item)
    return items


def summarize_jsonl(path: str | Path) -> dict[str, Any]:
    items = read_jsonl(path)
    by_source_kind: dict[str, int] = {}
    by_api_surface: dict[str, int] = {}
    for item in items:
        metadata = item["metadata"]
        source_kind = str(metadata.get("source_kind"))
        api_surface = str(metadata.get("api_surface"))
        by_source_kind[source_kind] = by_source_kind.get(source_kind, 0) + 1
        by_api_surface[api_surface] = by_api_surface.get(api_surface, 0) + 1
    return {
        "documents": len(items),
        "source_kind": dict(sorted(by_source_kind.items())),
        "api_surface": dict(sorted(by_api_surface.items())),
    }


def split_by_source_kind(documents: Iterable[DemoDocument]) -> dict[str, list[DemoDocument]]:
    grouped: dict[str, list[DemoDocument]] = {}
    for document in documents:
        source_kind = document.metadata.get("source_kind") or infer_source_kind(
            document.metadata.get("path", "")
        )
        grouped.setdefault(str(source_kind), []).append(document)
    return grouped
