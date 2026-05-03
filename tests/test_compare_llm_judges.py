from __future__ import annotations

import unittest

from scripts.compare_llm_judges import build_report


class CompareLlmJudgesTests(unittest.TestCase):
    def test_build_report_uses_compared_runs_for_deterministic_columns(self) -> None:
        left = _judge_payload("codex_grep_filesystem")
        right = _judge_payload("codex_with_k2_real_mcp")
        report = build_report(left, right, scorecard=_scorecard())

        self.assertIn("Deterministic `codex_grep_filesystem`", report)
        self.assertIn("Deterministic `codex_with_k2_real_mcp`", report)
        self.assertIn("| `case-1` | `codex_grep_filesystem` | `codex_with_k2_real_mcp` | `0.7` | `0.9` |", report)


def _judge_payload(winner: str) -> dict:
    return {
        "provider": "test",
        "model": "model",
        "compared_runs": ["codex_grep_filesystem", "codex_with_k2_real_mcp"],
        "results": [
            {
                "case_id": "case-1",
                "winner_run": winner,
                "scores_by_run": {
                    "codex_grep_filesystem": {"correctness": 4},
                    "codex_with_k2_real_mcp": {"correctness": 5},
                },
            }
        ],
    }


def _scorecard() -> dict:
    return {
        "scorecard": {
            "runs": [
                {
                    "run_name": "codex_grep_filesystem",
                    "cases": [{"case_id": "case-1", "score": 0.7}],
                },
                {
                    "run_name": "codex_with_k2_real_mcp",
                    "cases": [{"case_id": "case-1", "score": 0.9}],
                },
            ]
        }
    }


if __name__ == "__main__":
    unittest.main()
