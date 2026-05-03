#!/usr/bin/env python3
"""Delete and reload the live K2 Java R&D demo corpora.

The reload keeps source files/pages as K2 documents and configures chunking at
the corpus level. Docs/guides use character-oriented K2 chunking so dense
indexes can build safely. Code uses the faster fixed/token K2 path and queues
sparse + metadata indexes; dense code indexing still needs the platform-side
embedder-limit fix.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator

PROJECT_NAME = "java-rd-demo-full"
TARGET_NAMES = {
    "flink-docs-2.2-full",
    "kafka-docs-4.2-full",
    "flink-code-2.2-full",
    "flink-code-2.2-full-part2",
    "flink-code-2.2-full-part3",
    "kafka-code-4.2-full",
    "java-rd-guides-full",
    "docs-direct-compare-20260426",
    "docs-tavily-compare-20260426",
}

DOCS_CHUNKING = {
    "strategy": "fixed",
    "chunk_size": 180,
    "overlap": 30,
    "dedup_mode": "minhash",
}

CODE_CHUNKING = {
    "strategy": "fixed",
    "chunk_size": 180,
    "overlap": 30,
    "dedup_mode": "off",
}

GUIDES_CHUNKING = {
    "strategy": "unstructured",
    "chunking_strategy": "basic",
    "chunk_size": 1800,
    "overlap": 120,
    "dedup_mode": "minhash",
}


@dataclass(frozen=True)
class CorpusPlan:
    role: str
    name: str
    description: str
    paths: tuple[Path, ...]
    chunking: dict[str, Any]
    max_documents: int | None = None
    max_document_chars: int | None = None


def build_plans(asset_dir: Path) -> tuple[CorpusPlan, ...]:
    return (
        CorpusPlan(
            role="flink_docs",
            name="flink-docs-2.2-full",
            description="Apache Flink 2.2 documentation and selected Javadocs.",
            paths=(asset_dir / "flink-docs.jsonl",),
            chunking=DOCS_CHUNKING,
            max_document_chars=1500,
        ),
        CorpusPlan(
            role="kafka_docs",
            name="kafka-docs-4.2-full",
            description="Apache Kafka 4.2 documentation.",
            paths=(asset_dir / "kafka-docs-only.jsonl",),
            chunking=DOCS_CHUNKING,
            max_document_chars=1500,
        ),
        CorpusPlan(
            role="flink_code",
            name="flink-code-2.2-full",
            description="Apache Flink source, tests, build files, and implementation patterns.",
            paths=(asset_dir / "flink-code.jsonl",),
            chunking=CODE_CHUNKING,
            max_documents=5000,
        ),
        CorpusPlan(
            role="kafka_code",
            name="kafka-code-4.2-full",
            description="Apache Kafka source, tests, examples, and Connect/Streams patterns.",
            paths=(asset_dir / "kafka-code.jsonl",),
            chunking=CODE_CHUNKING,
        ),
        CorpusPlan(
            role="guides",
            name="java-rd-guides-full",
            description="Generated Java R&D engineering guides.",
            paths=(asset_dir / "flink-guides.jsonl", asset_dir / "kafka-guides.jsonl"),
            chunking=GUIDES_CHUNKING,
        ),
    )


def iter_jsonl(paths: Iterable[Path]) -> Iterator[dict[str, Any]]:
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                item = json.loads(stripped)
                if not isinstance(item, dict):
                    raise ValueError(f"{path}:{line_number}: expected JSON object")
                yield item


def count_jsonl(paths: Iterable[Path]) -> int:
    return sum(1 for _ in iter_jsonl(paths))


def count_plan_documents(plan: CorpusPlan) -> int:
    return sum(1 for _ in iter_plan_documents(plan))


def iter_plan_documents(plan: CorpusPlan) -> Iterator[dict[str, Any]]:
    for item in iter_jsonl(plan.paths):
        if plan.max_document_chars:
            yield from split_document_by_chars(item, max_chars=plan.max_document_chars)
        else:
            yield item


def split_document_by_chars(document: dict[str, Any], *, max_chars: int) -> Iterator[dict[str, Any]]:
    text = str(document.get("raw_text") or "")
    if len(text) <= max_chars:
        yield document
        return

    parts = split_text(text, max_chars=max_chars)
    part_count = len(parts)
    source_uri = str(document.get("source_uri") or "document")
    for index, part in enumerate(parts, start=1):
        item = dict(document)
        metadata = dict(item.get("metadata") or {})
        metadata["part_index"] = index
        metadata["part_count"] = part_count
        item["metadata"] = metadata
        item["source_uri"] = f"{source_uri}#part-{index:04d}"
        item["raw_text"] = part
        yield item


def split_text(text: str, *, max_chars: int) -> list[str]:
    parts: list[str] = []
    remaining = text
    while len(remaining) > max_chars:
        boundary = remaining.rfind("\n\n", 0, max_chars)
        if boundary < max_chars // 2:
            boundary = remaining.rfind("\n", 0, max_chars)
        if boundary < max_chars // 2:
            boundary = remaining.rfind(" ", 0, max_chars)
        if boundary < max_chars // 2:
            boundary = max_chars
        part = remaining[:boundary].strip()
        if part:
            parts.append(part)
        remaining = remaining[boundary:].strip()
    if remaining:
        parts.append(remaining)
    return parts


def chunked(items: Iterable[dict[str, Any]], size: int) -> Iterator[list[dict[str, Any]]]:
    batch: list[dict[str, Any]] = []
    for item in items:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


def split_plan(plan: CorpusPlan) -> list[tuple[str, list[dict[str, Any]]]]:
    docs = list(iter_plan_documents(plan))
    if not plan.max_documents or len(docs) <= plan.max_documents:
        return [(plan.name, docs)]

    parts: list[tuple[str, list[dict[str, Any]]]] = []
    for index, start in enumerate(range(0, len(docs), plan.max_documents), start=1):
        suffix = "" if index == 1 else f"-part{index}"
        parts.append((f"{plan.name}{suffix}", docs[start : start + plan.max_documents]))
    return parts


def find_project_id(client: Any, project_name: str) -> str:
    for project in client.iter_projects(limit=100):
        if project.get("name") == project_name:
            return str(project["id"])
    created = client.create_project(project_name)
    return str(created["id"])


def list_target_corpora(client: Any, *, project_id: str | None) -> list[dict[str, Any]]:
    corpora = []
    for corpus in client.iter_corpora(limit=100):
        if corpus.get("name") not in TARGET_NAMES:
            continue
        if project_id and corpus.get("project_id") not in {project_id, None}:
            # Also keep the historical empty Default duplicate in target names
            # visible to the delete step by not filtering Default here.
            if corpus.get("project_name") != "Default":
                continue
        corpora.append(corpus)
    return corpora


def delete_targets(client: Any, corpora: Iterable[dict[str, Any]], *, execute: bool) -> list[dict[str, Any]]:
    deleted = []
    for corpus in corpora:
        row = {
            "id": corpus.get("id"),
            "name": corpus.get("name"),
            "project_name": corpus.get("project_name"),
            "document_count": corpus.get("document_count"),
        }
        if execute:
            response = client.delete_corpus(str(corpus["id"]), confirm=True, force=True)
            row["deleted"] = True
            row["delete_response"] = response
        else:
            row["deleted"] = False
        deleted.append(row)
        print(json.dumps({"delete": row}, default=str), flush=True)
    return deleted


def create_and_upload(
    client: Any,
    *,
    project_id: str,
    plan: CorpusPlan,
    batch_size: int,
    execute: bool,
) -> list[dict[str, Any]]:
    summaries = []
    for corpus_name, docs in split_plan(plan):
        summary: dict[str, Any] = {
            "role": plan.role,
            "name": corpus_name,
            "documents": len(docs),
            "chunking": plan.chunking,
        }
        if not execute:
            summaries.append(summary)
            print(json.dumps({"upload_plan": summary}, default=str), flush=True)
            continue

        corpus = client.create_corpus(project_id, corpus_name, description=plan.description)
        corpus_id = str(corpus["id"])
        client.update_corpus(corpus_id, chunking_config=plan.chunking)
        summary["corpus_id"] = corpus_id
        print(json.dumps({"created": summary}, default=str), flush=True)

        uploaded = 0
        for batch_number, batch in enumerate(chunked(docs, batch_size), start=1):
            response = client.upload_documents_batch(
                corpus_id,
                batch,
                auto_index=False,
                wait=True,
                poll_s=5,
                timeout_s=None,
            )
            uploaded += len(batch)
            print(
                json.dumps(
                    {
                        "uploaded_batch": {
                            "corpus_id": corpus_id,
                            "name": corpus_name,
                            "batch_number": batch_number,
                            "batch_documents": len(batch),
                            "uploaded_documents": uploaded,
                            "total_documents": len(docs),
                            "response": response,
                        }
                    },
                    default=str,
                ),
                flush=True,
            )

        summary["uploaded_documents"] = uploaded
        summaries.append(summary)
    return summaries


def build_indexes(client: Any, corpora: Iterable[dict[str, Any]], *, execute: bool) -> list[dict[str, Any]]:
    jobs = []
    for corpus in corpora:
        corpus_id = corpus.get("corpus_id")
        if not corpus_id:
            continue
        role = str(corpus.get("role") or "")
        dense = role not in {"flink_code", "kafka_code"}
        row = {
            "corpus_id": corpus_id,
            "name": corpus["name"],
            "role": role,
            "dense": dense,
            "sparse": True,
            "sparse_metadata": True,
        }
        if execute:
            response = client.build_indexes(
                corpus_id,
                dense=dense,
                sparse=True,
                sparse_metadata=True,
                mode="full",
                wait=False,
            )
            row["response"] = response
        jobs.append(row)
        print(json.dumps({"index_job": row}, default=str), flush=True)
    return jobs


def check_assets(plans: Iterable[CorpusPlan]) -> list[dict[str, Any]]:
    rows = []
    for plan in plans:
        for path in plan.paths:
            if not path.exists():
                raise FileNotFoundError(path)
        rows.append(
            {
                "role": plan.role,
                "name": plan.name,
                "paths": [str(path) for path in plan.paths],
                "source_documents": count_jsonl(plan.paths),
                "upload_documents": count_plan_documents(plan),
                "chunking": plan.chunking,
                "max_document_chars": plan.max_document_chars,
            }
        )
    return rows


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--asset-dir", type=Path, default=Path("/private/tmp/k2-java-rd-demo-full"))
    parser.add_argument("--project-id")
    parser.add_argument("--project-name", default=PROJECT_NAME)
    parser.add_argument("--batch-size", type=int, default=1000)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--delete-existing", action="store_true")
    parser.add_argument("--build-indexes", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.batch_size < 1:
        raise ValueError("--batch-size must be positive")

    if not args.execute:
        print(json.dumps({
            "mode": "dry-run",
            "asset_dir": str(args.asset_dir),
            "project_name": args.project_name,
            "batch_size": args.batch_size,
            "note": "pass --execute to reload live demo",
        }))
        return 0

    # --- everything below requires --execute ---
    from sdk import Knowledge2  # lazy import

    if not os.environ.get("K2_API_KEY"):
        raise RuntimeError("K2_API_KEY is required")
    if not args.delete_existing:
        raise RuntimeError("--delete-existing is required with --execute for this reload")

    plans = build_plans(args.asset_dir)
    print(json.dumps({"asset_plan": check_assets(plans)}, default=str), flush=True)

    client = Knowledge2(api_key=os.environ["K2_API_KEY"])
    project_id = args.project_id or find_project_id(client, args.project_name)
    print(json.dumps({"project_id": project_id, "project_name": args.project_name}), flush=True)

    targets = list_target_corpora(client, project_id=project_id)
    print(
        json.dumps(
            {
                "delete_targets": [
                    {
                        "id": corpus.get("id"),
                        "name": corpus.get("name"),
                        "project_name": corpus.get("project_name"),
                        "document_count": corpus.get("document_count"),
                    }
                    for corpus in targets
                ]
            },
            default=str,
        ),
        flush=True,
    )
    if args.delete_existing:
        delete_targets(client, targets, execute=args.execute)

    uploaded: list[dict[str, Any]] = []
    for plan in plans:
        uploaded.extend(
            create_and_upload(
                client,
                project_id=project_id,
                plan=plan,
                batch_size=args.batch_size,
                execute=args.execute,
            )
        )

    jobs = build_indexes(client, uploaded, execute=args.execute and args.build_indexes)
    print(json.dumps({"uploaded": uploaded, "index_jobs": jobs}, default=str), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
