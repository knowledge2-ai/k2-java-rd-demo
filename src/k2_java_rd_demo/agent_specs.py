"""Dry-run K2 Agent and Knowledge Feed specifications for the demo."""

from __future__ import annotations

from typing import Any


def default_corpus_placeholders() -> dict[str, str]:
    return {
        "flink_docs": "<flink-docs-2.2-corpus-id>",
        "flink_code": "<flink-code-2.2-corpus-id>",
        "java_rd_guides": "<java-rd-guides-corpus-id>",
        "kafka_docs": "<kafka-docs-4.2-corpus-id>",
        "kafka_code": "<kafka-code-4.2-corpus-id>",
    }


def build_agent_specs(
    *,
    project_id: str = "<java-rd-demo-project-id>",
    corpus_ids: dict[str, str] | None = None,
) -> dict[str, Any]:
    corpora = {**default_corpus_placeholders(), **(corpus_ids or {})}

    agents: dict[str, dict[str, Any]] = {
        "flink_docs_agent": {
            "name": "Flink Docs Agent",
            "project_id": project_id,
            "corpus_id": corpora["flink_docs"],
            "description": "Release-specific Apache Flink documentation and how-to guidance.",
            "task_type": "answer",
            "instructions": (
                "Answer using Flink 2.2 documentation only. Prefer version-specific "
                "guidance and return source URLs for every major claim."
            ),
        },
        "flink_code_agent": {
            "name": "Flink Code Agent",
            "project_id": project_id,
            "corpus_id": corpora["flink_code"],
            "description": "Apache Flink source, tests, build files, and implementation patterns.",
            "task_type": "answer",
            "instructions": (
                "Find implementation patterns in code. Separate production code from tests. "
                "Return file paths, class names, and neighboring tests."
            ),
        },
        "java_rd_guides_agent": {
            "name": "Java R&D Guides Agent",
            "project_id": project_id,
            "corpus_id": corpora["java_rd_guides"],
            "description": "Confluence-like engineering guides generated from docs and code.",
            "task_type": "answer",
            "instructions": (
                "Use guide pages to explain conventions before recommending source changes."
            ),
        },
        "java_architect_agent": {
            "name": "Java R&D Architect Agent",
            "project_id": project_id,
            "corpus_id": corpora["java_rd_guides"],
            "description": "Routes between docs, guides, source, and tests to create coding plans.",
            "task_type": "answer",
            "instructions": (
                "For coding tasks, consult guides first, docs second, source third, and tests "
                "fourth. Produce a cited implementation plan."
            ),
            "source_agent_keys": [
                {"agent_key": "flink_docs_agent", "mode": "retrieve"},
                {"agent_key": "flink_code_agent", "mode": "retrieve"},
                {"agent_key": "java_rd_guides_agent", "mode": "retrieve"},
            ],
        },
    }

    feeds = {
        "flink_rest_guides_feed": {
            "project_id": project_id,
            "name": "Flink REST Guide Feed",
            "source_agent_key": "java_architect_agent",
            "persistent": True,
            "target_corpus": {"existing": corpora["java_rd_guides"]},
            "reactive": False,
            "execution_mode": "retrieve",
            "purpose": (
                "Materialize recurring cross-corpus findings into durable guide documents, "
                "for example REST handler implementation checklists."
            ),
        }
    }

    return {"project_id": project_id, "corpora": corpora, "agents": agents, "feeds": feeds}
