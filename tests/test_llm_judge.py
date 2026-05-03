from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tests import _paths  # noqa: F401

from k2_java_rd_demo.llm_judge import (
    ClaudeCliJudgeClient,
    HeuristicJudgeClient,
    build_judge_cases,
    build_judge_prompt,
    judge_case,
    normalize_judge_result,
    parse_judge_json,
    sanitize_answer_for_judge,
    summarize_judge_results,
)


class LlmJudgeTests(unittest.TestCase):
    def test_build_judge_cases_blinds_and_maps_answers(self) -> None:
        cases = build_judge_cases(_payload(), seed="seed")

        self.assertEqual(len(cases), 1)
        case = cases[0]
        self.assertEqual(set(case.label_to_run), {"A", "B"})
        self.assertEqual(set(case.label_to_run.values()), {"codex_without_k2", "codex_with_k2"})
        self.assertIn("How do I add a Flink REST handler?", case.question)
        self.assertNotIn("expected_artifacts", case.reference)
        self.assertNotIn("must_mentions", case.reference)

    def test_build_judge_cases_accepts_explicit_compared_runs(self) -> None:
        payload = _payload()
        payload["answers"]["codex_grep_filesystem"] = {
            "case-1": "Use rg and inspect Foo.java."
        }
        payload["scorecard"]["runs"].append(
            {"run_name": "codex_grep_filesystem", "cases": [{"case_id": "case-1"}]}
        )

        cases = build_judge_cases(
            payload,
            seed="seed",
            baseline_run="codex_grep_filesystem",
            candidate_run="codex_with_k2",
        )

        self.assertEqual(len(cases), 1)
        self.assertEqual(
            set(cases[0].label_to_run.values()),
            {"codex_grep_filesystem", "codex_with_k2"},
        )

    def test_build_judge_prompt_is_blinded_and_requests_json(self) -> None:
        case = build_judge_cases(_payload(), seed="seed")[0]

        prompt = build_judge_prompt(case)

        self.assertIn("answer labels are randomized", prompt)
        self.assertIn("Return JSON only", prompt)
        self.assertIn("ANSWER A", prompt)
        self.assertIn("ANSWER B", prompt)
        self.assertNotIn("codex_with_k2", prompt)
        self.assertNotIn("codex_without_k2", prompt)

    def test_judge_context_excludes_answer_key_fields(self) -> None:
        cases = build_judge_cases(_payload(), seed="seed")
        reference = cases[0].reference

        self.assertNotIn("expected_artifacts", reference)
        self.assertNotIn("required_source_uris", reference)
        for key in ("source_uri", "class_name", "path_contains"):
            ref_text = json.dumps(reference)
            self.assertNotIn(key, ref_text, f"{key} should not appear in judge context")

    def test_judge_prompt_contains_no_repo_uris(self) -> None:
        case = build_judge_cases(_payload(), seed="seed")[0]
        prompt = build_judge_prompt(case)

        evaluation_context_start = prompt.index("EVALUATION CONTEXT:")
        answer_a_start = prompt.index("ANSWER A:")
        context_section = prompt[evaluation_context_start:answer_a_start]
        self.assertNotIn("repo://", context_section)

    def test_judge_context_preserves_topic_level_fields(self) -> None:
        cases = build_judge_cases(_payload(), seed="seed")
        reference = cases[0].reference

        self.assertEqual(reference["expected_source_kinds"], ["code"])
        self.assertEqual(reference["required_modules"], ["flink-runtime"])
        self.assertEqual(reference["required_api_surfaces"], ["rest"])
        self.assertNotIn("must_mentions", reference)
        self.assertEqual(reference["hallucination_markers"], ["@RestController"])

    def test_sanitize_answer_for_judge_removes_system_identity_terms(self) -> None:
        sanitized = sanitize_answer_for_judge(
            "The K2 MCP evidence says Codex used an MCP tool. K2 did not return tests."
        )

        self.assertNotIn("K2", sanitized)
        self.assertNotIn("MCP", sanitized)
        self.assertNotIn("Codex", sanitized)
        self.assertIn("retrieved evidence", sanitized)

    def test_parse_judge_json_accepts_fences(self) -> None:
        parsed = parse_judge_json(
            """```json
{"winner":"A","confidence":0.8,"scores":{"A":{"correctness":5},"B":{"correctness":2}}}
```"""
        )

        self.assertEqual(parsed["winner"], "A")

    def test_normalize_judge_result_clamps_dimension_scores(self) -> None:
        normalized = normalize_judge_result(
            {
                "winner": "B",
                "confidence": 0.9,
                "scores": {
                    "A": {"correctness": 7, "grounding": "3"},
                    "B": {"correctness": 4.4, "risk": -1},
                },
                "critical_issues": {"A": ["missing citations"], "B": "bad"},
            }
        )

        self.assertEqual(normalized["scores"]["A"]["correctness"], 5)
        self.assertEqual(normalized["scores"]["A"]["grounding"], 3)
        self.assertEqual(normalized["scores"]["B"]["correctness"], 4)
        self.assertEqual(normalized["scores"]["B"]["risk"], 0)
        self.assertEqual(normalized["critical_issues"]["B"], [])

    def test_judge_case_maps_winner_back_to_run(self) -> None:
        case = build_judge_cases(_payload(), seed="seed")[0]

        result = judge_case(case, HeuristicJudgeClient())

        self.assertIn(result["winner_run"], {"codex_without_k2", "codex_with_k2", "tie"})
        self.assertEqual(set(result["scores_by_run"]), {"codex_without_k2", "codex_with_k2"})
        json.dumps(result)

    def test_summarize_judge_results_counts_wins_and_dimensions(self) -> None:
        results = [
            {
                "winner_run": "codex_with_k2",
                "confidence": 0.8,
                "scores_by_run": {
                    "codex_with_k2": {"correctness": 5, "grounding": 5},
                    "codex_without_k2": {"correctness": 2, "grounding": 1},
                },
            },
            {
                "winner_run": "tie",
                "confidence": 0.6,
                "scores_by_run": {
                    "codex_with_k2": {"correctness": 4, "grounding": 4},
                    "codex_without_k2": {"correctness": 4, "grounding": 4},
                },
            },
        ]

        summary = summarize_judge_results(results)

        self.assertEqual(summary["winner_counts"]["codex_with_k2"], 1)
        self.assertEqual(summary["winner_counts"]["tie"], 1)
        self.assertEqual(summary["win_rates_excluding_ties"]["codex_with_k2"], 1.0)
        self.assertEqual(summary["dimension_averages"]["codex_with_k2"]["correctness"], 4.5)

    def test_claude_cli_judge_client_invokes_print_mode_and_parses_json(self) -> None:
        class Completed:
            stdout = '{"winner":"A","confidence":0.7,"scores":{"A":{"correctness":5}}}'

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "judge.json"
            with patch("k2_java_rd_demo.llm_judge.subprocess.run", return_value=Completed()) as run:
                result = ClaudeCliJudgeClient(
                    claude_bin="claude",
                    model="sonnet",
                    cwd=temp_dir,
                ).judge("judge prompt", output_path=output_path)
            self.assertTrue(output_path.exists())

        cmd = run.call_args.args[0]
        self.assertEqual(cmd[:2], ["claude", "--print"])
        self.assertIn("--no-session-persistence", cmd)
        self.assertIn("--model", cmd)
        self.assertIn("sonnet", cmd)
        self.assertEqual(cmd[-1], "judge prompt")
        self.assertEqual(result["winner"], "A")


def _payload() -> dict:
    return {
        "cases": [
            {
                "case_id": "case-1",
                "title": "REST handler",
                "query": "How do I add a Flink REST handler?",
                "expected_artifacts": [
                    {
                        "key": "handler",
                        "source_uri": "repo://apache/flink@release-2.2.0/Foo.java",
                        "source_kind": "code",
                        "module": "flink-runtime",
                        "api_surface": "rest",
                        "class_name": "Foo",
                        "text_contains": ["AbstractRestHandler"],
                    }
                ],
                "expected_source_kinds": ["code"],
                "required_modules": ["flink-runtime"],
                "required_api_surfaces": ["rest"],
                "must_mentions": ["AbstractRestHandler"],
                "required_source_uris": ["repo://apache/flink@release-2.2.0/Foo.java"],
                "hallucination_markers": ["@RestController"],
            }
        ],
        "answers": {
            "codex_without_k2": {"case-1": "Use @RestController and guess a route."},
            "codex_with_k2": {
                "case-1": (
                    "K2 evidence says use AbstractRestHandler from "
                    "repo://apache/flink@release-2.2.0/Foo.java and add tests."
                )
            },
        },
        "scorecard": {
            "baseline_run": "codex_without_k2",
            "runs": [
                {"run_name": "codex_without_k2", "cases": [{"case_id": "case-1"}]},
                {"run_name": "codex_with_k2", "cases": [{"case_id": "case-1"}]},
            ],
            "comparisons": [{"run_name": "codex_with_k2"}],
        },
    }


if __name__ == "__main__":
    unittest.main()
