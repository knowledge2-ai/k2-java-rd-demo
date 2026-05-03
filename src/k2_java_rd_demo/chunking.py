"""Chunking profiles for K2 Java R&D demo ingestion."""

from __future__ import annotations

from typing import Any

DOCS_CHUNKING: dict[str, Any] = {
    "strategy": "fixed",
    "chunk_size": 220,
    "overlap": 40,
    "dedup_mode": "minhash",
}

DOCS_CHUNKING_FALLBACK: dict[str, Any] = {
    "strategy": "unstructured",
    "chunking_strategy": "by_title",
    "chunk_size": 1200,
    "overlap": 120,
    "combine_text_under_n_chars": 500,
    "multipage_sections": True,
    "dedup_mode": "minhash",
}

GUIDE_CHUNKING: dict[str, Any] = {
    "strategy": "semantic",
    "chunk_size": 900,
    "overlap": 90,
    "dedup_mode": "minhash",
}

CODE_CHUNKING: dict[str, Any] = {
    "strategy": "fixed",
    "chunk_size": 1200,
    "overlap": 200,
    "dedup_mode": "off",
}

TEST_CHUNKING: dict[str, Any] = {
    "strategy": "fixed",
    "chunk_size": 1400,
    "overlap": 220,
    "dedup_mode": "off",
}

CONFIG_CHUNKING: dict[str, Any] = {
    "strategy": "fixed",
    "chunk_size": 140,
    "overlap": 20,
    "dedup_mode": "off",
}


def chunking_for_source_kind(source_kind: str) -> dict[str, Any]:
    if source_kind in {"docs"}:
        return dict(DOCS_CHUNKING)
    if source_kind == "guide":
        return dict(GUIDE_CHUNKING)
    if source_kind == "test":
        return dict(TEST_CHUNKING)
    if source_kind in {"build", "config"}:
        return dict(CONFIG_CHUNKING)
    return dict(CODE_CHUNKING)


def chunking_catalog() -> dict[str, dict[str, Any]]:
    return {
        "docs": DOCS_CHUNKING,
        "docs_fallback": DOCS_CHUNKING_FALLBACK,
        "guide": GUIDE_CHUNKING,
        "code": CODE_CHUNKING,
        "test": TEST_CHUNKING,
        "config": CONFIG_CHUNKING,
    }
