from __future__ import annotations

import importlib.util
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts" / "run_patch_generation_benchmark.py"


def _load_runner():
    spec = importlib.util.spec_from_file_location("run_patch_generation_benchmark", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load run_patch_generation_benchmark.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PatchGenerationRunnerTests(unittest.TestCase):
    def test_load_env_file_sets_missing_values_without_overwriting(self) -> None:
        runner = _load_runner()
        with tempfile.TemporaryDirectory() as tmp:
            env_path = Path(tmp) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "# ignored",
                        "K2_API_KEY='from-file'",
                        'K2_API_HOST="https://api.example"',
                        "MALFORMED",
                    ]
                ),
                encoding="utf-8",
            )

            with patch.dict(os.environ, {"K2_API_KEY": "already-set"}, clear=True):
                runner._load_env_file(env_path)

                self.assertEqual(os.environ["K2_API_KEY"], "already-set")
                self.assertEqual(os.environ["K2_API_HOST"], "https://api.example")

    def test_preflight_only_sdk_requires_key(self) -> None:
        runner = _load_runner()
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(SystemExit, "K2_API_KEY is required"):
                runner.main(
                    [
                        "--preflight-only",
                        "--arm",
                        "codex_with_k2_mcp",
                        "--mcp-backend",
                        "sdk",
                        "--env-file",
                        "/tmp/does-not-exist-k2-demo.env",
                    ]
                )

    def test_preflight_only_sdk_succeeds_with_key_without_launching_codex(self) -> None:
        runner = _load_runner()
        with patch.dict(os.environ, {"K2_API_KEY": "fake-key"}, clear=True):
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                code = runner.main(
                    [
                        "--preflight-only",
                        "--arm",
                        "codex_repo_plus_guides_dump",
                        "--arm",
                        "codex_with_k2_mcp",
                        "--mcp-backend",
                        "sdk",
                        "--env-file",
                        "/tmp/does-not-exist-k2-demo.env",
                    ]
                )

        payload = json.loads(buffer.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(payload["mode"], "preflight")
        self.assertEqual(payload["mcp_backend"], "sdk")
        self.assertTrue(payload["k2_api_key_present"])
        self.assertEqual(payload["status"], "ok")

    def test_preflight_only_can_probe_k2_sdk_retrieval(self) -> None:
        runner = _load_runner()

        class FakeK2McpServer:
            def __init__(self, config) -> None:
                self.config = config

            def _search_docs(self, payload):
                self.payload = payload
                return {
                    "retrieval_profile": self.config.retrieval_profile,
                    "results": [
                        {
                            "source_uri": (
                                "repo://apache/flink@release-2.2.0/"
                                "flink-docs/content/docs/ops/rest_api.md"
                            )
                        }
                    ],
                }

        with (
            patch.dict(os.environ, {"K2_API_KEY": "fake-key"}, clear=True),
            patch.object(runner, "K2McpServer", FakeK2McpServer),
        ):
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                code = runner.main(
                    [
                        "--preflight-only",
                        "--probe-k2-sdk",
                        "--arm",
                        "codex_with_k2_mcp",
                        "--mcp-backend",
                        "sdk",
                        "--retrieval-profile",
                        "java_exact",
                        "--env-file",
                        "/tmp/does-not-exist-k2-demo.env",
                    ]
                )

        payload = json.loads(buffer.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(payload["k2_probe"]["framework"], "flink")
        self.assertEqual(payload["k2_probe"]["result_count"], 1)
        self.assertEqual(payload["k2_probe"]["retrieval_profile"], "java_exact")
        self.assertTrue(payload["k2_probe"]["first_source_uri"].startswith("repo://apache/flink"))

    def test_preflight_only_probe_fails_on_empty_k2_results(self) -> None:
        runner = _load_runner()

        class EmptyK2McpServer:
            def __init__(self, config) -> None:
                self.config = config

            def _search_docs(self, payload):
                return {"retrieval_profile": self.config.retrieval_profile, "results": []}

        with (
            patch.dict(os.environ, {"K2_API_KEY": "fake-key"}, clear=True),
            patch.object(runner, "K2McpServer", EmptyK2McpServer),
        ):
            with self.assertRaisesRegex(SystemExit, "returned no Flink REST results"):
                runner.main(
                    [
                        "--preflight-only",
                        "--probe-k2-sdk",
                        "--arm",
                        "codex_with_k2_mcp",
                        "--mcp-backend",
                        "sdk",
                        "--env-file",
                        "/tmp/does-not-exist-k2-demo.env",
                    ]
                )


if __name__ == "__main__":
    unittest.main()
