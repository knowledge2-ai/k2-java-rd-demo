from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from tests import _paths  # noqa: F401

from k2_java_rd_demo.assets import generate_seed_guides
from k2_java_rd_demo.cli import main


class FakeLiveClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def upload_documents_batch_and_wait(self, corpus_id: str, documents: list[dict], **kwargs):
        self.calls.append(("upload", {"corpus_id": corpus_id, "count": len(documents), **kwargs}))
        return {"batch_id": "batch-1"}

    def sync_indexes(self, corpus_id: str, **kwargs):
        self.calls.append(("sync", {"corpus_id": corpus_id, **kwargs}))
        return {"job_id": "job-1"}

    def search(self, corpus_id: str, query: str, **kwargs):
        self.calls.append(("search", {"corpus_id": corpus_id, "query": query, **kwargs}))
        return {"results": [{} for _ in range(5)]}

    def create_agent(self, **payload):
        self.calls.append(("create_agent", payload))
        return {"agent_id": f"agent-{len([call for call in self.calls if call[0] == 'create_agent'])}"}

    def activate_agent(self, **payload):
        self.calls.append(("activate_agent", payload))
        return {"status": "active"}

    def create_feed(self, **payload):
        self.calls.append(("create_feed", payload))
        return {"feed_id": "feed-1"}

    def run_feed(self, **payload):
        self.calls.append(("run_feed", payload))
        return {"status": "dry_run"}

    def list_agents(self):
        self.calls.append(("list_agents", {}))
        return []

    def list_feeds(self):
        self.calls.append(("list_feeds", {}))
        return []


class CliTests(unittest.TestCase):
    def test_show_config(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(["show-config"])
        self.assertEqual(code, 0)
        self.assertIn("metadata_sparse_enabled", buffer.getvalue())

    def test_build_guides_and_probe(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "guides.jsonl"
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                code = main(
                    [
                        "build-guides",
                        "--framework",
                        "flink",
                        "--version",
                        "2.2.0",
                        "--out",
                        str(out),
                    ]
                )
            self.assertEqual(code, 0)
            self.assertTrue(out.exists())

            buffer = io.StringIO()
            with redirect_stdout(buffer):
                code = main(["probe-jsonl", "--input", str(out)])
            self.assertEqual(code, 0)
            self.assertIn('"documents": 4', buffer.getvalue())

    def test_discover_and_build_docs_assets_use_source_catalog(self) -> None:
        with patch(
            "k2_java_rd_demo.cli.discover_docs_urls",
            return_value=["https://nightlies.apache.org/flink/flink-docs-release-2.2/rest.html"],
        ) as discover:
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                code = main(["discover-docs-urls", "--framework", "flink", "--max-pages", "1"])

        self.assertEqual(code, 0)
        self.assertEqual(discover.call_args.kwargs["max_pages"], 1)
        self.assertIn('"url_count": 1', buffer.getvalue())
        self.assertIn('"flink-docs-2.2"', buffer.getvalue())

        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "docs.jsonl"
            with patch(
                "k2_java_rd_demo.cli.build_docs_documents",
                return_value=generate_seed_guides("flink", "2.2.0"),
            ) as build_docs:
                buffer = io.StringIO()
                with redirect_stdout(buffer):
                    code = main(
                        [
                            "build-docs-assets",
                            "--framework",
                            "flink",
                            "--max-pages",
                            "2",
                            "--out",
                            str(out),
                        ]
                    )

            self.assertEqual(code, 0)
            self.assertEqual(build_docs.call_args.kwargs["max_pages"], 2)
            self.assertTrue(out.exists())
            self.assertIn('"written": 4', buffer.getvalue())

    def test_validate_agent_specs(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(
                [
                    "validate-agent-specs",
                    "--project-id",
                    "project-1",
                    "--flink-docs-corpus-id",
                    "docs-1",
                    "--flink-code-corpus-id",
                    "code-1",
                    "--guides-corpus-id",
                    "guides-1",
                ]
            )
        self.assertEqual(code, 0)
        self.assertIn('"valid": true', buffer.getvalue())

    def test_show_readiness_probes(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(["show-readiness-probes"])
        self.assertEqual(code, 0)
        self.assertIn("flink_rest_code", buffer.getvalue())

    def test_show_source_manifest_and_eval_cases(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(["show-source-manifest", "--include-kafka"])
        self.assertEqual(code, 0)
        self.assertIn('"flink-docs-2.2"', buffer.getvalue())
        self.assertIn('"kafka-docs-4.2"', buffer.getvalue())

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(["show-eval-cases", "--include-kafka"])
        self.assertEqual(code, 0)
        self.assertIn('"flink-rest-handler-controller-analogue"', buffer.getvalue())
        self.assertIn('"kafka-connect-validation-rule"', buffer.getvalue())

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(["show-eval-cases", "--suite", "benchmark"])
        self.assertEqual(code, 0)
        self.assertIn('"flink-rest-dispatcher-rest-endpoint"', buffer.getvalue())
        self.assertIn(
            '"kafka-connect-principal-connector-client-config-override-policy"',
            buffer.getvalue(),
        )

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(["show-mcp-contract", "--include-kafka"])
        self.assertEqual(code, 0)
        self.assertIn('"k2_search_docs"', buffer.getvalue())
        self.assertIn('"k2_present_answer"', buffer.getvalue())

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(["plan-repo-checkout", "--include-kafka", "--base-dir", "/tmp/sources"])
        self.assertEqual(code, 0)
        self.assertIn("apache-flink-release-2.2.0", buffer.getvalue())
        self.assertIn("apache-kafka-4.2", buffer.getvalue())
        self.assertIn('"sparse": true', buffer.getvalue())

    def test_plan_live_run_and_score_sample(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "guides.jsonl"
            with redirect_stdout(io.StringIO()):
                self.assertEqual(
                    main(
                        [
                            "build-guides",
                            "--framework",
                            "flink",
                            "--version",
                            "2.2.0",
                            "--out",
                            str(out),
                        ]
                    ),
                    0,
                )

            buffer = io.StringIO()
            with redirect_stdout(buffer):
                code = main(
                    [
                        "plan-live-run",
                        "--jsonl",
                        str(out),
                        "--project-id",
                        "project-1",
                        "--guides-corpus-id",
                        "guides-1",
                    ]
            )
            self.assertEqual(code, 0)
            self.assertIn('"guides": 4', buffer.getvalue())

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(["score-sample"])
        self.assertEqual(code, 0)
        self.assertIn('"best_run": "k2"', buffer.getvalue())

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(["score-demo-cases", "--include-kafka"])
        self.assertEqual(code, 0)
        self.assertIn('"case_count": 3', buffer.getvalue())
        self.assertIn('"best_run": "k2"', buffer.getvalue())

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(["score-demo-cases", "--suite", "benchmark"])
        self.assertEqual(code, 0)
        self.assertIn('"case_count": 100', buffer.getvalue())

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(["score-customer-value", "--include-kafka"])
        self.assertEqual(code, 0)
        self.assertIn('"method": "customer_value_guardrail_scorecard"', buffer.getvalue())
        self.assertIn('"k2_guides_docs_code_tests"', buffer.getvalue())

        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(["score-customer-value", "--format", "markdown"])
        self.assertEqual(code, 0)
        self.assertIn("# Customer-Value Guardrail Demo", buffer.getvalue())

    def test_plan_live_eval_and_run_guard(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(
                [
                    "plan-live-eval",
                    "--project-id",
                    "project-1",
                    "--flink-docs-corpus-id",
                    "flink-docs-1",
                    "--flink-code-corpus-id",
                    "flink-code-1",
                    "--guides-corpus-id",
                    "guides-1",
                    "--top-k",
                    "5",
                ]
            )
        self.assertEqual(code, 0)
        self.assertIn('"request_count": 8', buffer.getvalue())
        self.assertIn('"top_k": 5', buffer.getvalue())

        with redirect_stdout(io.StringIO()), patch("sys.stderr", new_callable=io.StringIO) as err:
            code = main(
                [
                    "run-live-eval",
                    "--project-id",
                    "project-1",
                    "--docs-corpus-id",
                    "docs-1",
                    "--code-corpus-id",
                    "code-1",
                    "--guides-corpus-id",
                    "guides-1",
                ]
            )
        self.assertEqual(code, 1)
        self.assertIn("--execute", err.getvalue())

    def test_live_commands_require_execute_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "guides.jsonl"
            with redirect_stdout(io.StringIO()):
                self.assertEqual(
                    main(
                        [
                            "build-guides",
                            "--framework",
                            "flink",
                            "--version",
                            "2.2.0",
                            "--out",
                            str(out),
                        ]
                    ),
                    0,
                )

            with redirect_stdout(io.StringIO()), patch("sys.stderr", new_callable=io.StringIO) as err:
                code = main(["run-live-k2", "--jsonl", str(out)])
            self.assertEqual(code, 1)
            self.assertIn("--execute", err.getvalue())

    def test_run_live_k2_uses_patched_client(self) -> None:
        fake = FakeLiveClient()
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "guides.jsonl"
            with redirect_stdout(io.StringIO()):
                self.assertEqual(
                    main(
                        [
                            "build-guides",
                            "--framework",
                            "flink",
                            "--version",
                            "2.2.0",
                            "--out",
                            str(out),
                        ]
                    ),
                    0,
                )

            buffer = io.StringIO()
            with patch.dict("os.environ", {"K2_API_KEY": "secret"}, clear=True):
                with patch("k2_java_rd_demo.cli.create_knowledge2_client", return_value=fake):
                    with redirect_stdout(buffer):
                        code = main(
                            [
                                "run-live-k2",
                                "--execute",
                                "--jsonl",
                                str(out),
                                "--project-id",
                                "project-1",
                                "--guides-corpus-id",
                                "guides-1",
                                "--skip-probes",
                                "--idempotency-prefix",
                                "demo",
                            ]
                        )

        self.assertEqual(code, 0)
        self.assertIn('"api_key_present": true', buffer.getvalue())
        self.assertIn('"document_count": 4', buffer.getvalue())
        self.assertEqual([call[0] for call in fake.calls], ["upload", "sync"])

    def test_deploy_live_agents_uses_patched_client(self) -> None:
        fake = FakeLiveClient()
        buffer = io.StringIO()
        with patch.dict("os.environ", {"K2_API_KEY": "secret"}, clear=True):
            with patch("k2_java_rd_demo.cli.create_knowledge2_client", return_value=fake):
                with redirect_stdout(buffer):
                    code = main(
                        [
                            "deploy-live-agents",
                            "--execute",
                            "--project-id",
                            "project-1",
                            "--flink-docs-corpus-id",
                            "docs-1",
                            "--flink-code-corpus-id",
                            "code-1",
                            "--guides-corpus-id",
                            "guides-1",
                            "--run-feed-dry-run",
                        ]
                    )

        self.assertEqual(code, 0)
        self.assertIn('"flink_docs_agent"', buffer.getvalue())
        self.assertEqual(
            [call[0] for call in fake.calls],
            [
                "list_agents",
                "create_agent",
                "create_agent",
                "create_agent",
                "create_agent",
                "activate_agent",
                "activate_agent",
                "activate_agent",
                "activate_agent",
                "list_feeds",
                "create_feed",
                "run_feed",
            ],
        )

    def test_run_live_eval_uses_patched_client(self) -> None:
        fake = FakeLiveClient()
        buffer = io.StringIO()
        with patch.dict("os.environ", {"K2_API_KEY": "secret"}, clear=True):
            with patch("k2_java_rd_demo.cli.create_knowledge2_client", return_value=fake):
                with redirect_stdout(buffer):
                    code = main(
                        [
                            "run-live-eval",
                            "--execute",
                            "--project-id",
                            "project-1",
                            "--docs-corpus-id",
                            "docs-1",
                            "--code-corpus-id",
                            "code-1",
                            "--guides-corpus-id",
                            "guides-1",
                            "--top-k",
                            "2",
                        ]
                    )

        self.assertEqual(code, 0)
        self.assertIn('"api_key_present": true', buffer.getvalue())
        self.assertIn('"scorecard"', buffer.getvalue())
        search_calls = [call for call in fake.calls if call[0] == "search"]
        self.assertEqual(len(search_calls), 8)


if __name__ == "__main__":
    unittest.main()
