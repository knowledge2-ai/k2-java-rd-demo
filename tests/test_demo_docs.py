from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "runbooks" / "customer-demo-runbook.md"
SKILL = ROOT / "skills" / "k2-java-rd-demo" / "SKILL.md"


class DemoDocsTests(unittest.TestCase):
    def test_runbook_contains_customer_demo_story_and_commands(self) -> None:
        text = RUNBOOK.read_text(encoding="utf-8")
        required_phrases = [
            "Baseline Claude/Codex without K2",
            "Repo-only Claude/Codex",
            "K2-assisted Claude/Codex",
            "metadata filters",
            "K2 Agents",
            "Knowledge Feeds",
            "Confluence-style",
            "guardrail",
            "Rotate any credential",
            "K2 credentials must come from environment variables",
        ]
        required_commands = [
            "build-guides",
            "build-docs-assets",
            "discover-docs-urls",
            "plan-repo-checkout",
            "plan-live-run",
            "run-live-k2",
            "validate-agent-specs",
            "deploy-live-agents",
            "show-mcp-contract",
            "plan-live-eval",
            "run-live-eval",
            "score-sample",
            "score-customer-value",
        ]
        for phrase in required_phrases + required_commands:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_skill_contains_actionable_k2_usage_rules(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        required_phrases = [
            "Search guides first",
            "guardrail ID",
            "docs second",
            "code third",
            "tests fourth",
            "Do not edit code until the plan cites",
            "framework=flink",
            "source_kind in [docs, guide]",
            "source_kind=code",
            "source_kind=test",
            "class_name text_match",
            "framework=kafka",
            "java_rd_guides_agent",
            "flink_docs_agent",
            "flink_code_agent",
            "Knowledge Feeds",
            "K2 credentials must come from",
        ]
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_markdown_contains_no_literal_k2_key_material(self) -> None:
        combined = "\n".join(
            [
                RUNBOOK.read_text(encoding="utf-8"),
                SKILL.read_text(encoding="utf-8"),
            ]
        )
        forbidden_literals: tuple[str, ...] = ()
        for literal in forbidden_literals:
            with self.subTest(kind="literal"):
                self.assertNotIn(literal, combined)

        forbidden_patterns = [
            re.compile(r"K2_API_KEY\s*=\s*['\"]?(?!\.\.\.|<)[A-Za-z0-9_.-]{20,}"),
            re.compile(r"\bk2_[A-Za-z0-9_-]{24,}\b", re.IGNORECASE),
            re.compile(r"\bsk-[A-Za-z0-9_-]{24,}\b"),
        ]
        for pattern in forbidden_patterns:
            with self.subTest(pattern=pattern.pattern):
                self.assertIsNone(pattern.search(combined))


if __name__ == "__main__":
    unittest.main()
