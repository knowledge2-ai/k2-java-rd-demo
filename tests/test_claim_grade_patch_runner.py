from __future__ import annotations

import importlib.util
import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "scripts" / "run_claim_grade_patch_benchmark.py"


def _load_runner():
    spec = importlib.util.spec_from_file_location("run_claim_grade_patch_benchmark", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load run_claim_grade_patch_benchmark.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ClaimGradePatchRunnerTests(unittest.TestCase):
    def test_dry_run_prints_preflight_execute_and_audit_shape(self) -> None:
        runner = _load_runner()
        buffer = io.StringIO()

        with redirect_stdout(buffer):
            code = runner.main(
                [
                    "--dry-run",
                    "--env-file",
                    "/tmp/k2-demo.env",
                    "--out-dir",
                    "/tmp/k2-claim-grade",
                    "--skip-focused-tests",
                ]
            )

        payload = json.loads(buffer.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(payload["mode"], "dry-run")
        self.assertFalse(payload["audit_requires_focused_tests"])
        self.assertIn("--preflight-only", payload["preflight_command"])
        self.assertIn("--execute", payload["execute_command"])
        self.assertNotIn("--run-tests", payload["execute_command"])
        self.assertIn("--probe-k2-sdk", payload["preflight_command"])
        self.assertIn("--probe-k2-sdk", payload["execute_command"])

    def test_default_execute_command_runs_focused_tests(self) -> None:
        runner = _load_runner()
        args = runner._parser().parse_args(["--dry-run"])

        command = runner._benchmark_command(args, execute=True)

        self.assertIn("--run-tests", command)
        self.assertIn("codex_repo_plus_guides_dump", command)
        self.assertIn("codex_with_k2_mcp", command)


if __name__ == "__main__":
    unittest.main()
