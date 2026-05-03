from __future__ import annotations

import unittest
from typing import Any

from tests import _paths  # noqa: F401

from k2_java_rd_demo.agent_specs import build_agent_specs
from k2_java_rd_demo.live_agents import (
    create_agents,
    deploy_agents_and_feeds,
    ensure_agents,
    ensure_feeds,
    resolve_source_agent_keys,
)


class FakeK2Client:
    def __init__(self) -> None:
        self.created_agents: list[dict[str, Any]] = []
        self.activated_agents: list[dict[str, Any]] = []
        self.created_feeds: list[dict[str, Any]] = []
        self.feed_runs: list[dict[str, Any]] = []
        self.existing_agents: list[dict[str, Any]] = []
        self.existing_feeds: list[dict[str, Any]] = []

    def list_agents(self) -> list[dict[str, Any]]:
        return list(self.existing_agents)

    def list_feeds(self) -> list[dict[str, Any]]:
        return list(self.existing_feeds)

    def create_agent(self, **payload: Any) -> dict[str, str]:
        self.created_agents.append(payload)
        return {"agent_id": f"agent-{len(self.created_agents)}"}

    def activate_agent(self, **payload: Any) -> dict[str, str]:
        self.activated_agents.append(payload)
        return {"status": "activated"}

    def create_feed(self, **payload: Any) -> dict[str, str]:
        self.created_feeds.append(payload)
        return {"feed_id": f"feed-{len(self.created_feeds)}"}

    def run_feed(self, **payload: Any) -> dict[str, Any]:
        self.feed_runs.append(payload)
        return {"status": "dry_run", "feed_id": payload["feed_id"]}


class LiveAgentRuntimeTests(unittest.TestCase):
    def test_deploys_agents_feed_and_runs_feed_dry_run(self) -> None:
        client = FakeK2Client()

        summary = deploy_agents_and_feeds(
            client,
            project_id="project-1",
            corpus_ids={
                "flink_docs": "docs-1",
                "flink_code": "code-1",
                "java_rd_guides": "guides-1",
            },
            run_feed_dry_run=True,
        )

        self.assertEqual(
            list(summary["agents"]),
            [
                "flink_docs_agent",
                "flink_code_agent",
                "java_rd_guides_agent",
                "java_architect_agent",
            ],
        )
        self.assertEqual(len(client.created_agents), 4)
        architect_payload = client.created_agents[-1]
        self.assertNotIn("source_agent_keys", architect_payload)
        self.assertEqual(
            [source["agent_id"] for source in architect_payload["source_agents"]],
            ["agent-1", "agent-2", "agent-3"],
        )
        self.assertEqual(
            [source["mode"] for source in architect_payload["source_agents"]],
            ["retrieve", "retrieve", "retrieve"],
        )

        self.assertEqual(
            client.activated_agents,
            [
                {"agent_id": "agent-1"},
                {"agent_id": "agent-2"},
                {"agent_id": "agent-3"},
                {"agent_id": "agent-4"},
            ],
        )

        self.assertEqual(len(client.created_feeds), 1)
        feed_payload = client.created_feeds[0]
        self.assertNotIn("source_agent_key", feed_payload)
        self.assertEqual(feed_payload["source_agent_id"], "agent-4")
        self.assertEqual(feed_payload["target_corpus"]["existing"], "guides-1")
        self.assertEqual(feed_payload["target_corpus_id"], "guides-1")
        self.assertEqual(client.feed_runs, [{"feed_id": "feed-1", "dry_run": True}])

        feed_summary = summary["feeds"]["flink_rest_guides_feed"]
        self.assertEqual(feed_summary["source_agent_id"], "agent-4")
        self.assertEqual(feed_summary["target_corpus_id"], "guides-1")
        self.assertEqual(
            feed_summary["dry_run"],
            {"status": "dry_run", "feed_id": "feed-1"},
        )

    def test_rejects_missing_required_corpus_ids_before_creating_agents(self) -> None:
        client = FakeK2Client()

        with self.assertRaisesRegex(ValueError, "java_rd_guides"):
            deploy_agents_and_feeds(
                client,
                project_id="project-1",
                corpus_ids={"flink_docs": "docs-1", "flink_code": "code-1"},
            )

        self.assertEqual(client.created_agents, [])
        self.assertEqual(client.created_feeds, [])

    def test_create_agents_respects_source_dependencies_even_if_specs_are_unordered(self) -> None:
        specs = build_agent_specs(
            project_id="project-1",
            corpus_ids={
                "flink_docs": "docs-1",
                "flink_code": "code-1",
                "java_rd_guides": "guides-1",
            },
        )
        unordered_agents = {
            "java_architect_agent": specs["agents"]["java_architect_agent"],
            "java_rd_guides_agent": specs["agents"]["java_rd_guides_agent"],
            "flink_code_agent": specs["agents"]["flink_code_agent"],
            "flink_docs_agent": specs["agents"]["flink_docs_agent"],
        }
        client = FakeK2Client()

        created = create_agents(client, unordered_agents)

        self.assertEqual(
            [payload["name"] for payload in client.created_agents],
            [
                "Flink Docs Agent",
                "Flink Code Agent",
                "Java R&D Guides Agent",
                "Java R&D Architect Agent",
            ],
        )
        self.assertEqual(
            created["java_architect_agent"]["source_agent_ids"],
            ["agent-1", "agent-2", "agent-3"],
        )

    def test_resolve_source_agent_keys_reports_unknown_logical_agent(self) -> None:
        specs = build_agent_specs(
            project_id="project-1",
            corpus_ids={
                "flink_docs": "docs-1",
                "flink_code": "code-1",
                "java_rd_guides": "guides-1",
            },
        )

        with self.assertRaisesRegex(ValueError, "flink_docs_agent"):
            resolve_source_agent_keys(specs["agents"]["java_architect_agent"], {})


    def test_ensure_reuses_existing_agent(self) -> None:
        specs = build_agent_specs(
            project_id="project-1",
            corpus_ids={
                "flink_docs": "docs-1",
                "flink_code": "code-1",
                "java_rd_guides": "guides-1",
            },
        )
        client = FakeK2Client()
        client.existing_agents = [
            {"id": "existing-agent-1", "name": "Flink Docs Agent"},
            {"id": "existing-agent-2", "name": "Flink Code Agent"},
            {"id": "existing-agent-3", "name": "Java R&D Guides Agent"},
            {"id": "existing-agent-4", "name": "Java R&D Architect Agent"},
        ]

        result = ensure_agents(client, specs["agents"])

        self.assertEqual(client.created_agents, [])
        self.assertEqual(len(result), 4)
        for agent_key, agent in result.items():
            self.assertTrue(agent["reused"], f"{agent_key} should be reused")
            self.assertTrue(agent["activated"])
        self.assertEqual(result["flink_docs_agent"]["id"], "existing-agent-1")
        self.assertEqual(result["java_architect_agent"]["id"], "existing-agent-4")

    def test_ensure_creates_when_missing(self) -> None:
        specs = build_agent_specs(
            project_id="project-1",
            corpus_ids={
                "flink_docs": "docs-1",
                "flink_code": "code-1",
                "java_rd_guides": "guides-1",
            },
        )
        client = FakeK2Client()
        client.existing_agents = [
            {"id": "existing-agent-1", "name": "Flink Docs Agent"},
        ]

        result = ensure_agents(client, specs["agents"])

        self.assertEqual(len(client.created_agents), 3)
        self.assertTrue(result["flink_docs_agent"]["reused"])
        self.assertEqual(result["flink_docs_agent"]["id"], "existing-agent-1")
        self.assertFalse(result["flink_code_agent"]["reused"])
        self.assertFalse(result["java_architect_agent"]["reused"])
        architect = result["java_architect_agent"]
        self.assertIn("existing-agent-1", architect["source_agent_ids"])
        self.assertEqual(len(architect["source_agent_ids"]), 3)

    def test_ensure_feeds_reuses_existing(self) -> None:
        feed_specs = {
            "test_feed": {
                "name": "Test Feed",
                "source_agent_key": "agent_a",
                "target_corpus": {"existing": "corpus-1"},
            },
        }
        client = FakeK2Client()
        client.existing_feeds = [{"id": "existing-feed-1", "name": "Test Feed"}]

        result = ensure_feeds(client, feed_specs, {"agent_a": "agent-id-1"})

        self.assertEqual(client.created_feeds, [])
        self.assertTrue(result["test_feed"]["reused"])
        self.assertEqual(result["test_feed"]["id"], "existing-feed-1")

    def test_ensure_feeds_creates_when_missing(self) -> None:
        feed_specs = {
            "test_feed": {
                "name": "Test Feed",
                "source_agent_key": "agent_a",
                "target_corpus": {"existing": "corpus-1"},
            },
        }
        client = FakeK2Client()

        result = ensure_feeds(client, feed_specs, {"agent_a": "agent-id-1"})

        self.assertEqual(len(client.created_feeds), 1)
        self.assertFalse(result["test_feed"]["reused"])
        self.assertEqual(result["test_feed"]["source_agent_id"], "agent-id-1")
        self.assertEqual(result["test_feed"]["target_corpus_id"], "corpus-1")

    def test_deploy_ensure_mode_reuses_and_skips_activation(self) -> None:
        client = FakeK2Client()
        client.existing_agents = [
            {"id": "existing-1", "name": "Flink Docs Agent"},
            {"id": "existing-2", "name": "Flink Code Agent"},
            {"id": "existing-3", "name": "Java R&D Guides Agent"},
            {"id": "existing-4", "name": "Java R&D Architect Agent"},
        ]
        client.existing_feeds = [
            {"id": "existing-feed-1", "name": "Flink REST Guide Feed"},
        ]

        summary = deploy_agents_and_feeds(
            client,
            project_id="project-1",
            corpus_ids={
                "flink_docs": "docs-1",
                "flink_code": "code-1",
                "java_rd_guides": "guides-1",
            },
            create_mode="ensure",
        )

        self.assertEqual(client.created_agents, [])
        self.assertEqual(client.activated_agents, [])
        self.assertEqual(client.created_feeds, [])
        for agent in summary["agents"].values():
            self.assertTrue(agent["reused"])

    def test_deploy_create_mode_always_creates(self) -> None:
        client = FakeK2Client()

        summary = deploy_agents_and_feeds(
            client,
            project_id="project-1",
            corpus_ids={
                "flink_docs": "docs-1",
                "flink_code": "code-1",
                "java_rd_guides": "guides-1",
            },
            create_mode="create",
        )

        self.assertEqual(len(client.created_agents), 4)
        self.assertEqual(len(client.activated_agents), 4)
        for agent in summary["agents"].values():
            self.assertNotIn("reused", agent)


if __name__ == "__main__":
    unittest.main()
