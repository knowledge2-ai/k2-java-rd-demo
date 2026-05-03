from __future__ import annotations

import csv
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tests import _paths  # noqa: F401

from k2_java_rd_demo.evaluation import EvalCase, EvalRun, ExpectedArtifact, compare_runs
from k2_java_rd_demo.question_stats import (
    build_question_stats,
    render_question_stats_markdown,
    write_question_stats,
)


class QuestionStatsTests(unittest.TestCase):
    def test_build_question_stats_captures_question_scores_and_mcp_counts(self) -> None:
        payload = _payload()

        stats = build_question_stats(payload)

        self.assertEqual(len(stats), 1)
        row = stats[0]
        self.assertEqual(row["case_id"], "case-1")
        self.assertEqual(row["question"], "How do I add a Flink REST handler?")
        self.assertGreater(row["score_delta"], 0)
        self.assertEqual(row["mcp_tool_call_count"], 2)
        self.assertEqual(
            row["metric_scores"]["artifact_matches"]["k2"],
            1.0,
        )
        self.assertEqual(row["baseline_score_components"]["retrieval_score"], 0.0)
        self.assertGreater(row["k2_score_components"]["retrieval_score"], 0.0)
        self.assertGreater(row["score_component_deltas"]["retrieval_score"], 0.0)
        self.assertEqual(row["k2_missing"]["artifacts"], [])
        self.assertIn("REST handler", row["baseline_missing"]["must_mentions"])

    def test_render_question_stats_markdown_includes_full_question_details(self) -> None:
        payload = _payload()
        stats = build_question_stats(payload)

        markdown = render_question_stats_markdown(payload, stats)

        self.assertIn("# Per-Question Benchmark Statistics", markdown)
        self.assertIn("How do I add a Flink REST handler?", markdown)
        self.assertIn("Baseline C/R/A", markdown)
        self.assertIn("Score components", markdown)
        self.assertIn("K2 metric scores", markdown)

    def test_write_question_stats_outputs_csv_markdown_and_json(self) -> None:
        with self.subTest("write files"):
            with TemporaryDirectory() as raw_dir:
                paths = write_question_stats(_payload(), out_dir=Path(raw_dir))

                self.assertTrue(paths["csv"].exists())
                self.assertTrue(paths["md"].exists())
                self.assertTrue(paths["json"].exists())

                with paths["csv"].open(encoding="utf-8", newline="") as handle:
                    rows = list(csv.DictReader(handle))

        self.assertEqual(rows[0]["case_id"], "case-1")
        self.assertIn("baseline_retrieval_score", rows[0])
        self.assertIn("k2_answer_score", rows[0])
        self.assertIn("delta_artifact_matches", rows[0])
        self.assertEqual(rows[0]["mcp_tool_call_count"], "2")


def _payload() -> dict:
    case = EvalCase(
        case_id="case-1",
        title="Flink REST handler",
        query="How do I add a Flink REST handler?",
        expected_artifacts=(
            ExpectedArtifact(
                key="handler",
                source_uri="repo://apache/flink@release-2.2.0/Foo.java",
                source_kind="code",
                module="flink-runtime",
                api_surface="rest",
                class_name="Foo",
                text_contains=("AbstractRestHandler",),
            ),
        ),
        expected_source_kinds=("code",),
        required_modules=("flink-runtime",),
        required_api_surfaces=("rest",),
        must_mentions=("AbstractRestHandler", "REST handler"),
        hallucination_markers=("@RestController",),
    )
    rows = [_row()]
    scorecard = compare_runs(
        [case],
        [
            EvalRun(
                name="codex_without_k2",
                results_by_case={case.case_id: []},
                answers_by_case={case.case_id: "Use Spring @RestController."},
            ),
            EvalRun(
                name="codex_with_k2_real_mcp",
                results_by_case={case.case_id: rows},
                answers_by_case={
                    case.case_id: (
                        "Use AbstractRestHandler for the REST handler. Cite "
                        "repo://apache/flink@release-2.2.0/Foo.java"
                    )
                },
            ),
        ],
    )
    return {
        "cases": [case.to_dict()],
        "rows_by_case": {case.case_id: rows},
        "tool_counts_by_case": {case.case_id: {"k2_answer_with_sources": 2}},
        "scorecard": scorecard,
    }


def _row() -> dict:
    return {
        "source_uri": "repo://apache/flink@release-2.2.0/Foo.java",
        "raw_text": "class Foo extends AbstractRestHandler",
        "metadata": {
            "source_kind": "code",
            "module": "flink-runtime",
            "api_surface": "rest",
            "class_name": "Foo",
            "path": "Foo.java",
        },
        "score": 1.0,
    }


if __name__ == "__main__":
    unittest.main()
