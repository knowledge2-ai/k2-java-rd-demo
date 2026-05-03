from __future__ import annotations

import json
import unittest
from typing import Any

from tests import _paths  # noqa: F401

from k2_java_rd_demo.eval_cases import demo_eval_cases
from k2_java_rd_demo.evaluation import EvalCase, EvalRun
from k2_java_rd_demo.live_eval import (
    LiveEvalConfig,
    LiveEvalConfigError,
    build_live_eval_search_requests,
    run_live_eval,
    select_eval_cases,
)


class FakeSearchClient:
    def __init__(self, rows_by_kind: dict[str, list[dict[str, Any]]] | None = None) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []
        self.rows_by_kind = rows_by_kind or {}

    def search(self, corpus_id: str, query: str, **kwargs: Any) -> dict[str, Any]:
        self.calls.append((corpus_id, query, kwargs))
        source_kind = _filter_value(kwargs["filters"], "source_kind")
        return {"results": self.rows_by_kind.get(source_kind, [])}


class NamespaceSearch:
    def __init__(self, rows_by_kind: dict[str, list[dict[str, Any]]]) -> None:
        self.calls: list[dict[str, Any]] = []
        self.rows_by_kind = rows_by_kind

    def search(self, **payload: Any) -> dict[str, Any]:
        self.calls.append(payload)
        source_kind = _filter_value(payload["filters"], "source_kind")
        return {"results": self.rows_by_kind.get(source_kind, [])}


class NamespaceSearchClient:
    def __init__(self, rows_by_kind: dict[str, list[dict[str, Any]]]) -> None:
        self.corpora = NamespaceSearch(rows_by_kind)


class ExplodingClient:
    def __init__(self) -> None:
        self.calls = 0

    def search(self, *_args: Any, **_kwargs: Any) -> dict[str, Any]:
        self.calls += 1
        raise AssertionError("search should not be called")


class LiveEvalTests(unittest.TestCase):
    def test_build_requests_is_offline_and_requires_execute_for_live_calls(self) -> None:
        client = ExplodingClient()
        config = _config(execute=False)

        requests = build_live_eval_search_requests(config, demo_eval_cases()[:1])

        self.assertEqual(client.calls, 0)
        self.assertEqual(
            [(request.role, request.source_kind, request.corpus_id) for request in requests],
            [
                ("docs", "docs", "docs-1"),
                ("code", "code", "code-1"),
                ("code", "test", "code-1"),
                ("guides", "guide", "guides-1"),
            ],
        )
        with self.assertRaisesRegex(LiveEvalConfigError, "execute=True"):
            run_live_eval(client, config, demo_eval_cases()[:1])
        self.assertEqual(client.calls, 0)

    def test_run_live_eval_routes_docs_code_tests_and_returns_compare_output(self) -> None:
        case = demo_eval_cases()[0]
        rows_by_kind = _rows_by_kind(case)
        client = FakeSearchClient(rows_by_kind)
        baseline = EvalRun(
            name="baseline",
            results_by_case={case.case_id: rows_by_kind["docs"]},
        )

        scorecard = run_live_eval(
            client,
            _config(execute=True, top_k=3),
            [case],
            baseline=baseline,
        )

        routed = [
            (corpus_id, _filter_value(kwargs["filters"], "source_kind"), kwargs["top_k"])
            for corpus_id, _query, kwargs in client.calls
        ]
        self.assertEqual(
            routed,
            [
                ("docs-1", "docs", 3),
                ("code-1", "code", 3),
                ("code-1", "test", 3),
                ("guides-1", "guide", 3),
            ],
        )
        self.assertEqual(scorecard["baseline_run"], "baseline")
        self.assertEqual(scorecard["best_run"], "k2")
        self.assertEqual(scorecard["case_count"], 1)
        self.assertGreater(scorecard["comparisons"][0]["score_delta_vs_baseline"], 0)
        self.assertTrue(scorecard["runs"][1]["cases"][0]["passed"])
        json.dumps(scorecard)

    def test_include_kafka_selects_kafka_case_only_when_requested(self) -> None:
        flink_only = select_eval_cases(include_kafka=False)
        with_kafka = select_eval_cases(include_kafka=True)

        self.assertEqual([case.case_id for case in flink_only], [
            "flink-rest-handler-controller-analogue",
            "flink-2-2-upgrade-checkpointing-guidance",
        ])
        self.assertEqual(with_kafka[-1].case_id, "kafka-connect-validation-rule")

        kafka_requests = build_live_eval_search_requests(_config(include_kafka=True))
        self.assertIn(
            "kafka-connect-validation-rule",
            {request.case_id for request in kafka_requests},
        )
        self.assertNotIn(
            "kafka-connect-validation-rule",
            {
                request.case_id
                for request in build_live_eval_search_requests(_config(include_kafka=False))
            },
        )

    def test_framework_specific_corpora_are_preferred_when_available(self) -> None:
        config = LiveEvalConfig(
            project_id="project-1",
            corpus_ids={
                "flink_docs": "flink-docs-1",
                "flink_code": "flink-code-1",
                "kafka_docs": "kafka-docs-1",
                "kafka_code": "kafka-code-1",
                "guides": "guides-1",
            },
            include_kafka=True,
        )

        requests = build_live_eval_search_requests(config)
        by_case_role = {
            (request.case_id, request.role, request.source_kind): request.corpus_id
            for request in requests
        }

        self.assertEqual(
            by_case_role[("flink-rest-handler-controller-analogue", "docs", "docs")],
            "flink-docs-1",
        )
        self.assertEqual(
            by_case_role[("flink-rest-handler-controller-analogue", "code", "code")],
            "flink-code-1",
        )
        self.assertEqual(
            by_case_role[("kafka-connect-validation-rule", "docs", "docs")],
            "kafka-docs-1",
        )
        self.assertEqual(
            by_case_role[("kafka-connect-validation-rule", "code", "code")],
            "kafka-code-1",
        )

    def test_code_corpus_shards_are_searched_when_declared(self) -> None:
        config = LiveEvalConfig(
            project_id="project-1",
            corpus_ids={
                "flink_docs": "flink-docs-1",
                "flink_code": "flink-code-1",
                "flink_code_part2": "flink-code-2",
                "flink_code_part3": "flink-code-3",
                "guides": "guides-1",
            },
        )

        requests = build_live_eval_search_requests(config, demo_eval_cases()[:1])
        code_request_ids = [
            request.corpus_id for request in requests if request.role == "code"
        ]

        self.assertEqual(
            code_request_ids,
            [
                "flink-code-1",
                "flink-code-2",
                "flink-code-3",
                "flink-code-1",
                "flink-code-2",
                "flink-code-3",
            ],
        )

    def test_namespace_search_client_is_supported(self) -> None:
        case = demo_eval_cases()[0]
        client = NamespaceSearchClient(_rows_by_kind(case))

        scorecard = run_live_eval(client, _config(execute=True), [case])

        self.assertEqual(
            [call["corpus_id"] for call in client.corpora.calls],
            ["docs-1", "code-1", "code-1", "guides-1"],
        )
        self.assertEqual(scorecard["baseline_run"], "baseline")
        self.assertEqual(scorecard["best_run"], "k2")


def _config(
    *,
    execute: bool = False,
    include_kafka: bool = False,
    top_k: int = 12,
) -> LiveEvalConfig:
    return LiveEvalConfig(
        project_id="project-1",
        corpus_ids={"docs": "docs-1", "code": "code-1", "guides": "guides-1"},
        include_kafka=include_kafka,
        top_k=top_k,
        execute=execute,
    )


def _rows_by_kind(case: EvalCase) -> dict[str, list[dict[str, Any]]]:
    rows: dict[str, list[dict[str, Any]]] = {"docs": [], "code": [], "test": [], "guide": []}
    for artifact in case.expected_artifacts:
        source_kind = artifact.source_kind or "code"
        metadata = {
            "source_kind": source_kind,
            "module": artifact.module,
            "api_surface": artifact.api_surface,
            "path": artifact.path_contains or (artifact.source_uri or "").rsplit("/", 1)[-1],
        }
        if artifact.class_name:
            metadata["class_name"] = artifact.class_name
        metadata.update(artifact.metadata_equals)
        rows[source_kind].append(
            {
                "source_uri": artifact.source_uri,
                "raw_text": " ".join([artifact.key, *artifact.text_contains, *case.must_mentions]),
                "metadata": metadata,
                "score": 0.95,
            }
        )
    rows["guide"].append(
        {
            "source_uri": "generated://guides/flink/rest-handler-checklist.md",
            "raw_text": " ".join(case.must_mentions),
            "metadata": {
                "source_kind": "guide",
                "module": "guides",
                "api_surface": case.required_api_surfaces[0],
                "path": "guides/flink/rest-handler-checklist.md",
            },
            "score": 0.9,
        }
    )
    return rows


def _filter_value(filters: dict[str, Any], key: str) -> str:
    found: list[str] = []

    def visit(item: Any) -> None:
        if isinstance(item, dict):
            if item.get("key") == key:
                value = item.get("value")
                if isinstance(value, list):
                    found.extend(str(part) for part in value)
                else:
                    found.append(str(value))
            for child in item.get("filters", []):
                visit(child)

    visit(filters)
    if not found:
        return ""
    for value in reversed(found):
        if value in {"docs", "code", "test", "guide"}:
            return value
    return found[-1]


if __name__ == "__main__":
    unittest.main()
