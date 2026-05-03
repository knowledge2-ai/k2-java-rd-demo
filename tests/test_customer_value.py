from __future__ import annotations

import json
import unittest

from tests import _paths  # noqa: F401

from k2_java_rd_demo.assets import generate_seed_guides
from k2_java_rd_demo.customer_value import (
    customer_value_prompt,
    customer_value_scorecard,
    customer_value_scenarios,
    render_customer_value_report,
    score_customer_value_answer,
)


class CustomerValueTests(unittest.TestCase):
    def test_seed_guides_include_confluence_style_guardrail_ids(self) -> None:
        flink_guides = generate_seed_guides("flink", "2.2.0")
        kafka_guides = generate_seed_guides("kafka", "4.2.0")
        text = "\n".join(document.raw_text for document in (*flink_guides, *kafka_guides))

        self.assertIn("CF-FLINK-REST-001", text)
        self.assertIn("CF-FLINK-CKPT-004", text)
        self.assertIn("CF-KAFKA-CONNECT-007", text)
        self.assertIn("Do not add Spring MVC", text)
        self.assertIn("Do not introduce Spring Validator", text)

    def test_customer_value_prompt_hides_guardrails_from_repo_only(self) -> None:
        scenario = customer_value_scenarios(include_kafka=False)[0]

        repo_only = customer_value_prompt(scenario, arm_name="repo_only")
        with_k2 = customer_value_prompt(scenario, arm_name="k2_guides_docs_code_tests")

        self.assertIn("local repository search", repo_only)
        self.assertIn("Do not use K2", repo_only)
        self.assertNotIn("CF-FLINK-REST-001", repo_only)
        self.assertIn("Retrieve guide pages first", with_k2)
        self.assertNotIn("CF-FLINK-REST-001", with_k2)

    def test_customer_value_scorecard_shows_k2_guardrail_advantage(self) -> None:
        scorecard = customer_value_scorecard(include_kafka=True)
        summary_by_arm = {row["arm_name"]: row for row in scorecard["summary"]["arms"]}

        self.assertEqual(summary_by_arm["baseline_no_retrieval"]["passed_scenarios"], 0)
        self.assertEqual(summary_by_arm["repo_only"]["passed_scenarios"], 0)
        self.assertEqual(
            summary_by_arm["k2_guides_docs_code_tests"]["passed_scenarios"],
            summary_by_arm["k2_guides_docs_code_tests"]["scenario_count"],
        )
        self.assertGreater(
            summary_by_arm["k2_guides_docs_code_tests"]["mean_score"],
            summary_by_arm["repo_only"]["mean_score"],
        )
        json.dumps(scorecard)

    def test_score_customer_value_answer_penalizes_forbidden_patterns(self) -> None:
        scenario = customer_value_scenarios(include_kafka=False)[0]

        score = score_customer_value_answer(
            scenario,
            answer_text=(
                "Use Spring MVC, but cite CF-FLINK-REST-001 and "
                "generated://guides/flink/confluence-rest-handler-guardrails.md."
            ),
            retrieved_rows=[],
        )

        self.assertFalse(score["passed"])
        self.assertIn("Spring MVC", score["forbidden_hits"])
        self.assertEqual(score["score_breakdown"]["forbidden_marker_safety"], 0.0)

    def test_render_customer_value_report_is_customer_readable(self) -> None:
        report = render_customer_value_report(customer_value_scorecard(include_kafka=False))

        self.assertIn("# Customer-Value Guardrail Demo", report)
        self.assertIn("Repo-only search can find implementation classes", report)
        self.assertIn("k2_guides_docs_code_tests", report)


if __name__ == "__main__":
    unittest.main()
