"""K2 search and metadata filter recipes for the Java R&D demo."""

from __future__ import annotations

from typing import Any

DEMO_HYBRID: dict[str, Any] = {
    "enabled": True,
    "fusion_mode": "rrf",
    "rrf_k": 60,
    "dense_weight": 0.60,
    "sparse_weight": 0.30,
    "metadata_sparse_weight": 0.10,
    "metadata_sparse_enabled": True,
}

DEMO_RETURN: dict[str, Any] = {
    "include_text": True,
    "include_scores": True,
    "include_provenance": True,
}


def structured_filter(filters: list[dict[str, Any]], *, condition: str = "and") -> dict[str, Any]:
    if condition not in {"and", "or"}:
        raise ValueError("condition must be 'and' or 'or'")
    return {"condition": condition, "filters": filters}


def eq(key: str, value: Any) -> dict[str, Any]:
    return {"key": key, "op": "==", "value": value}


def ne(key: str, value: Any) -> dict[str, Any]:
    return {"key": key, "op": "!=", "value": value}


def in_(key: str, values: list[Any]) -> dict[str, Any]:
    return {"key": key, "op": "in", "value": values}


def text_match(key: str, value: str) -> dict[str, Any]:
    return {"key": key, "op": "text_match", "value": value}


def flink_docs_filter(version: str = "2.2.0") -> dict[str, Any]:
    return structured_filter(
        [
            eq("demo_dataset_id", "java-rd-oss-2026-04"),
            eq("framework", "flink"),
            eq("framework_version", version),
            eq("source_kind", "docs"),
        ]
    )


def flink_rest_code_filter(version: str = "2.2.0") -> dict[str, Any]:
    return structured_filter(
        [
            eq("framework", "flink"),
            eq("framework_version", version),
            eq("source_kind", "code"),
            eq("module", "flink-runtime"),
            eq("api_surface", "rest"),
            ne("stability", "test_only"),
        ]
    )


def flink_rest_tests_filter(version: str = "2.2.0") -> dict[str, Any]:
    return structured_filter(
        [
            eq("framework", "flink"),
            eq("framework_version", version),
            eq("source_kind", "test"),
            eq("module", "flink-runtime"),
            eq("api_surface", "rest"),
        ]
    )


def flink_checkpoint_docs_or_guides_filter(version: str = "2.2.0") -> dict[str, Any]:
    return structured_filter(
        [
            eq("framework", "flink"),
            eq("framework_version", version),
            in_("source_kind", ["docs", "guide"]),
            in_("api_surface", ["checkpointing", "rest"]),
        ]
    )


def kafka_connect_filter(version: str = "4.2.0") -> dict[str, Any]:
    return structured_filter(
        [
            eq("framework", "kafka"),
            eq("framework_version", version),
            in_("api_surface", ["connect", "rest"]),
            in_("source_kind", ["docs", "code", "test"]),
        ]
    )


def class_lookup_filter(framework: str, class_fragment: str) -> dict[str, Any]:
    return structured_filter(
        [
            eq("framework", framework),
            eq("language", "java"),
            text_match("class_name", class_fragment),
        ]
    )


def demo_filter_catalog() -> dict[str, dict[str, Any]]:
    return {
        "flink_docs_22": flink_docs_filter(),
        "flink_rest_code": flink_rest_code_filter(),
        "flink_rest_tests": flink_rest_tests_filter(),
        "flink_checkpoint_docs_or_guides": flink_checkpoint_docs_or_guides_filter(),
        "kafka_connect": kafka_connect_filter(),
        "flink_class_lookup_rest_handler": class_lookup_filter("flink", "RestHandler"),
    }
