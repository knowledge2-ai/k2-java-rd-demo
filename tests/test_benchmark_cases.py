from __future__ import annotations

import json
import unittest

from tests import _paths  # noqa: F401

from k2_java_rd_demo.benchmark_cases import benchmark_eval_case_dicts, benchmark_eval_cases
from k2_java_rd_demo.evaluation import EvalRun, compare_runs


class BenchmarkEvalCasesTests(unittest.TestCase):
    def test_benchmark_catalog_has_one_hundred_unique_cases(self) -> None:
        cases = benchmark_eval_cases()

        self.assertEqual(len(cases), 100)
        self.assertEqual(len({case.case_id for case in cases}), 100)
        self.assertEqual(
            sum(1 for case in cases if case.case_id.startswith("flink-")),
            50,
        )
        self.assertEqual(
            sum(1 for case in cases if case.case_id.startswith("kafka-")),
            50,
        )
        self.assertTrue(all(case.expected_artifacts for case in cases))
        self.assertTrue(all(case.must_mentions for case in cases))
        self.assertTrue(all(case.hallucination_markers for case in cases))
        for case in cases:
            code_artifact = next(
                artifact for artifact in case.expected_artifacts if artifact.source_kind == "code"
            )
            self.assertIn(code_artifact.class_name, case.query)
        by_id = {case.case_id: case for case in cases}
        self.assertIn(
            "Kafka Connect REST 4.2.0",
            by_id["kafka-rest-connector-type"].query,
        )
        corrected_uris = [
            artifact.source_uri
            for artifact in by_id[
                "kafka-connect-connector-client-config-request"
            ].expected_artifacts
            if artifact.source_kind == "code"
        ]
        self.assertEqual(
            corrected_uris,
            [
                "repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/connector/policy/ConnectorClientConfigRequest.java"
            ],
        )
        json.dumps(benchmark_eval_case_dicts())

    def test_benchmark_cases_are_compatible_with_scorecard(self) -> None:
        cases = benchmark_eval_cases()
        k2_rows = {case.case_id: _rows_for_case(case) for case in cases}
        k2_answers = {case.case_id: _answer_for_case(case) for case in cases}

        scorecard = compare_runs(
            cases,
            [
                EvalRun(name="baseline", results_by_case={case.case_id: [] for case in cases}),
                EvalRun(name="k2", results_by_case=k2_rows, answers_by_case=k2_answers),
            ],
        )

        self.assertEqual(scorecard["case_count"], 100)
        self.assertEqual(scorecard["best_run"], "k2")
        k2_run = next(run for run in scorecard["runs"] if run["run_name"] == "k2")
        self.assertEqual(k2_run["passed_cases"], 100)


def _rows_for_case(case):
    rows = []
    for artifact in case.expected_artifacts:
        metadata = {
            "source_kind": artifact.source_kind,
            "module": artifact.module,
            "api_surface": artifact.api_surface,
            "path": artifact.path_contains
            or (artifact.source_uri or artifact.key).rsplit("/", maxsplit=1)[-1],
        }
        if artifact.class_name:
            metadata["class_name"] = artifact.class_name
        metadata.update(artifact.metadata_equals)
        rows.append(
            {
                "source_uri": artifact.source_uri,
                "raw_text": " ".join(
                    [
                        artifact.key,
                        artifact.class_name or "",
                        *artifact.text_contains,
                        *case.must_mentions,
                        *(str(value) for value in artifact.metadata_equals.values()),
                    ]
                ),
                "metadata": metadata,
                "score": 1.0,
            }
        )
    return rows


def _answer_for_case(case) -> str:
    citations = [
        artifact.source_uri for artifact in case.expected_artifacts if artifact.source_uri
    ]
    return " ".join([*case.must_mentions, *citations])


if __name__ == "__main__":
    unittest.main()
