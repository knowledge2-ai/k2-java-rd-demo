from __future__ import annotations

import unittest

from tests import _paths  # noqa: F401

from k2_java_rd_demo.agent_specs import build_agent_specs


class AgentSpecTests(unittest.TestCase):
    def test_specs_include_agents_and_feed(self) -> None:
        specs = build_agent_specs(
            project_id="project-1",
            corpus_ids={"flink_docs": "docs-1", "flink_code": "code-1", "java_rd_guides": "guides-1"},
        )
        self.assertEqual(specs["agents"]["flink_docs_agent"]["corpus_id"], "docs-1")
        self.assertEqual(specs["agents"]["java_architect_agent"]["corpus_id"], "guides-1")
        self.assertIn("source_agent_keys", specs["agents"]["java_architect_agent"])
        self.assertEqual(
            specs["feeds"]["flink_rest_guides_feed"]["target_corpus"]["existing"], "guides-1"
        )


if __name__ == "__main__":
    unittest.main()
