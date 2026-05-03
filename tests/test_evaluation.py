from __future__ import annotations

import json
import unittest

from tests import _paths  # noqa: F401

from k2_java_rd_demo.evaluation import (
    EvalCase,
    EvalRun,
    ExpectedArtifact,
    compare_runs,
    normalize_result_row,
    score_case,
)


DOC_URI = "repo://apache/flink@release-2.2.0/docs/rest.md"
CODE_URI = (
    "repo://apache/flink@release-2.2.0/"
    "flink-runtime/src/main/java/org/apache/flink/runtime/rest/JobCheckpointHandler.java"
)
TEST_URI = (
    "repo://apache/flink@release-2.2.0/"
    "flink-runtime/src/test/java/org/apache/flink/runtime/rest/JobCheckpointHandlerTest.java"
)


def docs_row() -> dict[str, object]:
    return {
        "source_uri": DOC_URI,
        "raw_text": "REST endpoint docs describe route registration and response body classes.",
        "metadata": {
            "source_kind": "docs",
            "module": "docs",
            "api_surface": "rest",
            "path": "docs/rest.md",
        },
        "score": 0.91,
    }


def code_row() -> dict[str, object]:
    return {
        "document": {
            "source_uri": CODE_URI,
            "text": (
                "public class JobCheckpointHandler extends AbstractRestHandler { "
                "public void handleRequest() {} }"
            ),
            "metadata": {
                "source_kind": "code",
                "module": "flink-runtime",
                "api_surface": "rest",
                "path": "flink-runtime/src/main/java/JobCheckpointHandler.java",
                "class_name": "JobCheckpointHandler",
            },
        },
        "rerank_score": 0.88,
    }


def test_row() -> dict[str, object]:
    return {
        "source_uri": TEST_URI,
        "chunk_text": "JobCheckpointHandlerTest verifies handler wiring and validation failures.",
        "metadata": {
            "source_kind": "test",
            "module": "flink-runtime",
            "api_surface": "rest",
            "path": "flink-runtime/src/test/java/JobCheckpointHandlerTest.java",
            "class_name": "JobCheckpointHandlerTest",
        },
    }


def rest_case() -> EvalCase:
    return EvalCase(
        case_id="flink-rest-handler",
        title="Flink REST handler implementation",
        query="How should I add a Flink REST handler?",
        expected_artifacts=[
            ExpectedArtifact(
                key="rest handler source",
                source_uri=CODE_URI,
                source_kind="code",
                module="flink-runtime",
                api_surface="rest",
                class_name="JobCheckpointHandler",
                text_contains=["handleRequest"],
            ),
            ExpectedArtifact(
                key="neighboring handler test",
                source_kind="test",
                module="flink-runtime",
                api_surface="rest",
                path_contains="JobCheckpointHandlerTest.java",
            ),
        ],
        expected_source_kinds=["docs", "code", "test"],
        required_modules=["flink-runtime"],
        required_api_surfaces=["rest"],
        must_mentions=["route registration", "AbstractRestHandler"],
        required_source_uris=[DOC_URI],
        hallucination_markers=["MagicPlanner"],
    )


class EvaluationTests(unittest.TestCase):
    def test_normalize_nested_k2_result_row(self) -> None:
        result = normalize_result_row(code_row(), index=3)
        self.assertEqual(result.index, 3)
        self.assertEqual(result.source_uri, CODE_URI)
        self.assertEqual(result.metadata["class_name"], "JobCheckpointHandler")
        self.assertIn("AbstractRestHandler", result.text)
        self.assertEqual(result.score, 0.88)

    def test_normalize_live_k2_chunk_row(self) -> None:
        result = normalize_result_row(
            {
                "text": "class JobDetailsHandler extends AbstractRestHandler {}",
                "custom_metadata": {
                    "source_kind": "code",
                    "module": "flink-runtime",
                    "api_surface": "rest",
                    "path": "flink-runtime/src/main/java/JobDetailsHandler.java",
                    "class_name": "JobDetailsHandler",
                },
                "system_metadata": {
                    "provenance": {
                        "source_uri": (
                            "repo://apache/flink@release-2.2.0/"
                            "flink-runtime/src/main/java/JobDetailsHandler.java"
                        )
                    }
                },
                "score": 0.9,
            }
        )

        self.assertEqual(result.metadata["class_name"], "JobDetailsHandler")
        self.assertEqual(
            result.source_uri,
            "repo://apache/flink@release-2.2.0/"
            "flink-runtime/src/main/java/JobDetailsHandler.java",
        )

    def test_score_case_matches_expected_artifacts_and_metrics(self) -> None:
        answer = (
            "Use route registration from the REST docs, then mirror "
            "AbstractRestHandler in the source. Cite "
            f"{DOC_URI} and {CODE_URI}."
        )
        summary = score_case(rest_case(), [docs_row(), code_row(), test_row()], answer_text=answer)

        self.assertEqual(summary["score"], 1.0)
        self.assertTrue(summary["passed"])
        self.assertEqual(summary["metrics"]["artifact_matches"]["missing"], [])
        self.assertEqual(
            summary["metrics"]["source_kind_coverage"]["matched"],
            ["docs", "code", "test"],
        )
        self.assertEqual(summary["metrics"]["citation_coverage"]["score"], 1.0)

        json.dumps(summary)

    def test_score_case_reports_missing_artifacts_and_hallucination_markers(self) -> None:
        answer = "Use MagicPlanner and ignore neighboring tests."
        summary = score_case(rest_case(), [docs_row()], answer_text=answer)

        self.assertFalse(summary["passed"])
        self.assertEqual(summary["metrics"]["artifact_matches"]["missing"], [
            "rest handler source",
            "neighboring handler test",
        ])
        self.assertEqual(summary["metrics"]["source_kind_coverage"]["missing"], ["code", "test"])
        self.assertEqual(summary["metrics"]["hallucination_markers"]["present"], ["MagicPlanner"])
        self.assertEqual(summary["metrics"]["hallucination_markers"]["score"], 0.0)
        self.assertEqual(summary["score"], 0.0)

    def test_score_breakdown_present(self) -> None:
        answer = (
            "Use route registration from the REST docs, then mirror "
            "AbstractRestHandler in the source. Cite "
            f"{DOC_URI} and {CODE_URI}."
        )
        summary = score_case(rest_case(), [docs_row(), code_row(), test_row()], answer_text=answer)

        self.assertIn("score_breakdown", summary)
        breakdown = summary["score_breakdown"]
        self.assertIn("retrieval_score", breakdown)
        self.assertIn("answer_score", breakdown)
        self.assertIn("safety_score", breakdown)
        self.assertIsNotNone(breakdown["retrieval_score"])
        self.assertIsNotNone(breakdown["answer_score"])
        json.dumps(summary)

    def test_citation_coverage_accepts_clickable_github_urls(self) -> None:
        answer = (
            "Use route registration and AbstractRestHandler. Cite "
            "https://github.com/apache/flink/blob/"
            "5a336892424a9458653ead89610bf60d771ab8d7/"
            "flink-runtime/src/main/java/org/apache/flink/runtime/rest/JobCheckpointHandler.java."
        )
        case = EvalCase(
            case_id="clickable-citation",
            query="How should I add a Flink REST handler?",
            must_mentions=["route registration", "AbstractRestHandler"],
            required_source_uris=[CODE_URI],
        )

        summary = score_case(case, [code_row()], answer_text=answer)

        self.assertEqual(summary["metrics"]["citation_coverage"]["score"], 1.0)

    def test_no_answer_marks_answer_metrics_not_applicable(self) -> None:
        summary = score_case(rest_case(), [docs_row(), code_row(), test_row()])

        self.assertFalse(summary["metrics"]["must_mention_coverage"]["applicable"])
        self.assertFalse(summary["metrics"]["citation_coverage"]["applicable"])
        self.assertIsNone(summary["score_breakdown"]["answer_score"])
        self.assertIsNotNone(summary["score_breakdown"]["retrieval_score"])

    def test_empty_retrieval_does_not_zero_answer_quality(self) -> None:
        answer = (
            "Use route registration and AbstractRestHandler. Cite "
            f"{DOC_URI} and {CODE_URI}."
        )
        summary = score_case(rest_case(), [], answer_text=answer)

        # Retrieval score is 0 (applicable metrics exist but nothing retrieved)
        self.assertEqual(summary["score_breakdown"]["retrieval_score"], 0.0)
        # Answer quality is scored independently and should be positive
        self.assertIsNotNone(summary["score_breakdown"]["answer_score"])
        self.assertGreater(summary["score_breakdown"]["answer_score"], 0)
        # Overall score reflects both, not just retrieval zeros
        self.assertGreater(summary["score"], 0)

    def test_compare_runs_scores_k2_above_baseline(self) -> None:
        case = rest_case()
        baseline = EvalRun(
            name="baseline",
            results_by_case={case.case_id: [docs_row()]},
            answers_by_case={case.case_id: "Only cite the docs: " + DOC_URI},
        )
        k2 = EvalRun(
            name="k2",
            results_by_case={case.case_id: [docs_row(), code_row(), test_row()]},
            answers_by_case={
                case.case_id: (
                    "Use route registration and AbstractRestHandler. Cite "
                    f"{DOC_URI} and {CODE_URI}."
                )
            },
        )

        scorecard = compare_runs([case], [baseline, k2])

        self.assertEqual(scorecard["baseline_run"], "baseline")
        self.assertEqual(scorecard["best_run"], "k2")
        self.assertEqual(
            set(scorecard["runs"][0]["score_components"]),
            {"combined_score", "retrieval_score", "answer_score", "safety_score"},
        )
        self.assertGreater(scorecard["comparisons"][0]["score_delta_vs_baseline"], 0)
        self.assertIn(
            "retrieval_score",
            scorecard["comparisons"][0]["score_component_deltas_vs_baseline"],
        )
        self.assertGreater(
            scorecard["comparisons"][0]["metric_deltas_vs_baseline"]["artifact_matches"],
            0,
        )

        json.dumps(scorecard)


if __name__ == "__main__":
    unittest.main()
