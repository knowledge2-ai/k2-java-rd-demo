from __future__ import annotations

import json
import unittest

from tests import _paths  # noqa: F401

from k2_java_rd_demo.eval_cases import (
    demo_eval_case_dicts,
    demo_eval_cases,
    evaluation_case_dicts,
    evaluation_cases,
)
from k2_java_rd_demo.evaluation import EvalCase, EvalRun, compare_runs


class DemoEvalCasesTests(unittest.TestCase):
    def test_default_catalog_is_flink_only(self) -> None:
        cases = demo_eval_cases()

        self.assertEqual(
            [case.case_id for case in cases],
            [
                "flink-rest-handler-controller-analogue",
                "flink-2-2-upgrade-checkpointing-guidance",
            ],
        )
        self.assertTrue(all(case.case_id.startswith("flink-") for case in cases))
        self.assertTrue(all(case.expected_source_kinds for case in cases))
        self.assertTrue(all(case.required_modules for case in cases))
        self.assertTrue(all(case.required_api_surfaces for case in cases))
        self.assertTrue(all(case.must_mentions for case in cases))
        self.assertTrue(all(case.hallucination_markers for case in cases))
        self.assertTrue(
            all(
                artifact.source_uri is None or artifact.source_uri.startswith("repo://")
                for case in cases
                for artifact in case.expected_artifacts
            )
        )

    def test_include_kafka_adds_connect_case_and_serializes(self) -> None:
        cases = demo_eval_cases(include_kafka=True)

        self.assertEqual(len(cases), 3)
        self.assertEqual(cases[-1].case_id, "kafka-connect-validation-rule")
        self.assertIn("connect", cases[-1].required_api_surfaces)
        self.assertIn("clients", cases[-1].required_modules)
        kafka_uris = [
            artifact.source_uri
            for artifact in cases[-1].expected_artifacts
            if artifact.source_uri is not None
        ]
        self.assertTrue(all("@4.2/" in uri for uri in kafka_uris))
        self.assertTrue(all("@3.8.0/" not in uri for uri in kafka_uris))

        payload = demo_eval_case_dicts(include_kafka=True)
        self.assertEqual([item["case_id"] for item in payload], [case.case_id for case in cases])
        self.assertIn("expected_artifacts", payload[-1])
        json.dumps(payload)

    def test_catalog_cases_are_compatible_with_compare_runs(self) -> None:
        cases = demo_eval_cases(include_kafka=True)
        k2_rows = {case.case_id: _rows_for_case(case) for case in cases}
        k2_answers = {case.case_id: _answer_for_case(case) for case in cases}
        baseline_rows = {case.case_id: k2_rows[case.case_id][:1] for case in cases}

        scorecard = compare_runs(
            cases,
            [
                EvalRun(name="baseline", results_by_case=baseline_rows),
                EvalRun(name="k2", results_by_case=k2_rows, answers_by_case=k2_answers),
            ],
        )

        self.assertEqual(scorecard["case_count"], 3)
        self.assertEqual(scorecard["baseline_run"], "baseline")
        self.assertEqual(scorecard["best_run"], "k2")
        self.assertGreater(scorecard["comparisons"][0]["score_delta_vs_baseline"], 0)
        self.assertTrue(
            all(case_summary["passed"] for case_summary in scorecard["runs"][1]["cases"])
        )
        json.dumps(scorecard)

    def test_named_benchmark_suite_is_available(self) -> None:
        cases = evaluation_cases(suite="benchmark")

        self.assertEqual(len(cases), 100)
        self.assertEqual(len(evaluation_case_dicts(suite="benchmark")), 100)
        self.assertEqual(
            [case.case_id for case in evaluation_cases(suite="demo", include_kafka=True)],
            [case.case_id for case in demo_eval_cases(include_kafka=True)],
        )


def _rows_for_case(case: EvalCase) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for artifact in case.expected_artifacts:
        path = artifact.path_contains or (artifact.source_uri or "").rsplit("/", maxsplit=1)[-1]
        text_parts = [
            artifact.key,
            *artifact.text_contains,
            *case.must_mentions,
            *(str(value) for value in artifact.metadata_equals.values()),
        ]
        metadata = {
            "source_kind": artifact.source_kind,
            "module": artifact.module,
            "api_surface": artifact.api_surface,
            "path": path,
        }
        if artifact.class_name:
            metadata["class_name"] = artifact.class_name
        metadata.update(artifact.metadata_equals)
        rows.append(
            {
                "source_uri": artifact.source_uri,
                "raw_text": " ".join(text_parts),
                "metadata": metadata,
                "score": 1.0,
            }
        )
    return rows


def _answer_for_case(case: EvalCase) -> str:
    citations = [
        artifact.source_uri for artifact in case.expected_artifacts if artifact.source_uri is not None
    ]
    return " ".join([*case.must_mentions, *citations])


if __name__ == "__main__":
    unittest.main()
