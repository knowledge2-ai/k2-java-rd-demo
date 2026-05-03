from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"


def run_cli(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = (
        str(SRC)
        if not existing_pythonpath
        else os.pathsep.join([str(SRC), existing_pythonpath])
    )
    result = subprocess.run(
        [sys.executable, "-m", "k2_java_rd_demo.cli", *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
        timeout=60,
    )
    if check and result.returncode != 0:
        raise AssertionError(
            "\n".join(
                [
                    f"command failed: {' '.join(args)}",
                    f"returncode: {result.returncode}",
                    f"stdout:\n{result.stdout}",
                    f"stderr:\n{result.stderr}",
                ]
            )
        )
    return result


def json_stdout(result: subprocess.CompletedProcess[str]) -> dict:
    return json.loads(result.stdout)


class CliPipelineE2ETests(unittest.TestCase):
    def test_cli_module_help_starts(self) -> None:
        result = run_cli("--help")

        self.assertEqual(result.returncode, 0)
        self.assertIn("score-demo-cases", result.stdout)
        self.assertIn("run-live-eval", result.stdout)

    def test_offline_asset_pipeline_end_to_end(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            repo = work / "flink"
            source = (
                repo
                / "flink-runtime"
                / "src"
                / "main"
                / "java"
                / "org"
                / "apache"
                / "flink"
                / "runtime"
                / "rest"
                / "handler"
                / "DemoHandler.java"
            )
            source.parent.mkdir(parents=True)
            source.write_text(
                "package org.apache.flink.runtime.rest.handler;\n"
                "public class DemoHandler extends AbstractRestHandler {\n"
                "  public String handleRequest() { return \"ok\"; }\n"
                "}\n",
                encoding="utf-8",
            )
            test_source = (
                repo
                / "flink-runtime"
                / "src"
                / "test"
                / "java"
                / "org"
                / "apache"
                / "flink"
                / "runtime"
                / "rest"
                / "handler"
                / "DemoHandlerTest.java"
            )
            test_source.parent.mkdir(parents=True)
            test_source.write_text(
                "package org.apache.flink.runtime.rest.handler;\n"
                "public class DemoHandlerTest {\n"
                "  public void verifiesRouteRegistration() {}\n"
                "}\n",
                encoding="utf-8",
            )

            code_jsonl = work / "code.jsonl"
            code_build = json_stdout(
                run_cli(
                    "build-code-assets",
                    "--repo-root",
                    str(repo),
                    "--framework",
                    "flink",
                    "--version",
                    "2.2.0",
                    "--repo",
                    "apache/flink",
                    "--repo-ref",
                    "release-2.2.0",
                    "--out",
                    str(code_jsonl),
                )
            )
            self.assertEqual(code_build["written"], 2)

            code_probe = json_stdout(run_cli("probe-jsonl", "--input", str(code_jsonl)))
            self.assertEqual(code_probe["documents"], 2)
            self.assertEqual(code_probe["source_kind"]["code"], 1)
            self.assertEqual(code_probe["source_kind"]["test"], 1)
            self.assertEqual(code_probe["api_surface"]["rest"], 2)

            guides_jsonl = work / "guides.jsonl"
            guide_build = json_stdout(
                run_cli(
                    "build-guides",
                    "--framework",
                    "flink",
                    "--version",
                    "2.2.0",
                    "--out",
                    str(guides_jsonl),
                )
            )
            self.assertEqual(guide_build["written"], 4)

            guide_probe = json_stdout(run_cli("probe-jsonl", "--input", str(guides_jsonl)))
            self.assertEqual(guide_probe["documents"], 4)
            self.assertEqual(guide_probe["source_kind"]["guide"], 4)

            plan = json_stdout(
                run_cli(
                    "plan-live-run",
                    "--jsonl",
                    str(code_jsonl),
                    "--jsonl",
                    str(guides_jsonl),
                    "--project-id",
                    "project-1",
                    "--code-corpus-id",
                    "code-1",
                    "--guides-corpus-id",
                    "guides-1",
                )
            )
            self.assertEqual(plan["project_id"], "project-1")
            self.assertEqual(plan["document_counts_by_role"]["code"], 2)
            self.assertEqual(plan["document_counts_by_role"]["guides"], 4)

    def test_eval_and_mcp_contract_end_to_end(self) -> None:
        manifest = json_stdout(run_cli("show-source-manifest", "--include-kafka"))
        self.assertTrue(manifest["include_kafka"])
        self.assertIn("kafka", manifest["frameworks"])
        self.assertIn(
            "kafka-code-4.2",
            {source["corpus_name"] for source in manifest["code_sources"]},
        )

        contract = json_stdout(run_cli("show-mcp-contract", "--include-kafka"))
        tool_names = {tool["name"] for tool in contract["tools"]}
        self.assertIn("k2_search_docs", tool_names)
        self.assertIn("k2_present_answer", tool_names)

        scorecard = json_stdout(run_cli("score-demo-cases", "--include-kafka"))
        self.assertEqual(scorecard["case_count"], 3)
        self.assertEqual(scorecard["best_run"], "k2")
        self.assertGreater(scorecard["comparisons"][0]["score_delta_vs_baseline"], 0.45)
        k2_run = next(run for run in scorecard["runs"] if run["run_name"] == "k2")
        self.assertEqual(k2_run["passed_cases"], 3)

        plan = json_stdout(
            run_cli(
                "plan-live-eval",
                "--project-id",
                "project-1",
                "--flink-docs-corpus-id",
                "docs-1",
                "--flink-code-corpus-id",
                "code-1",
                "--guides-corpus-id",
                "guides-1",
                "--top-k",
                "3",
            )
        )
        self.assertFalse(plan["config"]["execute"])
        self.assertEqual(plan["request_count"], 8)
        self.assertEqual(plan["requests"][0]["top_k"], 3)

    def test_live_commands_are_guarded_end_to_end(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            guides_jsonl = Path(tmp) / "guides.jsonl"
            run_cli(
                "build-guides",
                "--framework",
                "flink",
                "--version",
                "2.2.0",
                "--out",
                str(guides_jsonl),
            )

            live_run = run_cli("run-live-k2", "--jsonl", str(guides_jsonl), check=False)
            self.assertNotEqual(live_run.returncode, 0)
            self.assertIn("--execute", live_run.stderr)

            live_agents = run_cli(
                "deploy-live-agents",
                "--project-id",
                "project-1",
                "--flink-docs-corpus-id",
                "docs-1",
                "--flink-code-corpus-id",
                "code-1",
                "--guides-corpus-id",
                "guides-1",
                check=False,
            )
            self.assertNotEqual(live_agents.returncode, 0)
            self.assertIn("--execute", live_agents.stderr)

            live_eval = run_cli(
                "run-live-eval",
                "--project-id",
                "project-1",
                "--flink-docs-corpus-id",
                "docs-1",
                "--flink-code-corpus-id",
                "code-1",
                "--guides-corpus-id",
                "guides-1",
                check=False,
            )
            self.assertNotEqual(live_eval.returncode, 0)
            self.assertIn("--execute", live_eval.stderr)


if __name__ == "__main__":
    unittest.main()
