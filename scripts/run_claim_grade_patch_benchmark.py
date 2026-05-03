#!/usr/bin/env python3
"""Run the full claim-grade patch benchmark and audit the resulting scorecard."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from k2_java_rd_demo.patch_benchmark import (  # noqa: E402
    render_patch_scorecard_audit,
    verify_patch_scorecard_evidence,
)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    preflight_cmd = _benchmark_command(args, preflight=True)
    execute_cmd = _benchmark_command(args, execute=True)
    if args.dry_run:
        print(
            json.dumps(
                {
                    "mode": "dry-run",
                    "preflight_command": preflight_cmd,
                    "execute_command": execute_cmd,
                    "audit_requires_focused_tests": not args.skip_focused_tests,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    preflight_payload = _run_json_command(preflight_cmd, label="preflight")
    execute_payload = _run_json_command(execute_cmd, label="execute")
    scorecard_path = Path(str(execute_payload["result_path"]))
    scorecard_payload = json.loads(scorecard_path.read_text(encoding="utf-8"))
    audit = verify_patch_scorecard_evidence(
        scorecard_payload,
        require_focused_tests=not args.skip_focused_tests,
    )
    audit_json_path = scorecard_path.parent / "patch-scorecard-audit.json"
    audit_report_path = scorecard_path.parent / "patch-scorecard-audit.md"
    _write_text(audit_json_path, json.dumps(audit, indent=2, sort_keys=True))
    _write_text(audit_report_path, render_patch_scorecard_audit(audit))
    print(
        json.dumps(
            {
                "generated_at": datetime.now(UTC).isoformat(),
                "preflight": preflight_payload,
                "scorecard_path": str(scorecard_path),
                "report_path": execute_payload.get("report_path"),
                "audit_json_path": str(audit_json_path),
                "audit_report_path": str(audit_report_path),
                "claim_ready": audit["claim_ready"],
                "verdict": audit["signal"]["verdict"],
                "issues": audit["issues"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if audit["claim_ready"] else 1


def _benchmark_command(args: argparse.Namespace, *, preflight: bool = False, execute: bool = False) -> list[str]:
    command = [
        sys.executable,
        str(ROOT / "scripts" / "run_patch_generation_benchmark.py"),
        "--probe-k2-sdk",
        "--arm",
        "codex_repo_plus_guides_dump",
        "--arm",
        "codex_with_k2_mcp",
        "--retrieval-profile",
        args.retrieval_profile,
        "--mcp-backend",
        args.mcp_backend,
        "--env-file",
        str(args.env_file),
        "--model",
        args.model,
        "--codex-timeout-s",
        str(args.codex_timeout_s),
        "--out-dir",
        str(args.out_dir),
    ]
    if args.api_host:
        command.extend(["--api-host", args.api_host])
    if args.source_base:
        command.extend(["--source-base", str(args.source_base)])
    if args.flink_root:
        command.extend(["--flink-root", str(args.flink_root)])
    if args.kafka_root:
        command.extend(["--kafka-root", str(args.kafka_root)])
    if args.keep_worktrees:
        command.append("--keep-worktrees")
    if preflight:
        command.append("--preflight-only")
    if execute:
        command.append("--execute")
        if not args.skip_focused_tests:
            command.append("--run-tests")
    return command


def _run_json_command(command: list[str], *, label: str) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(
            f"{label} command failed with exit code {completed.returncode}\n"
            f"stdout:\n{completed.stdout[-4000:]}\n"
            f"stderr:\n{completed.stderr[-4000:]}"
        )
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"{label} command did not return JSON\nstdout:\n{completed.stdout[-4000:]}\n"
            f"stderr:\n{completed.stderr[-4000:]}"
        ) from exc


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", type=Path, default=ROOT / ".env")
    parser.add_argument("--mcp-backend", choices=["sdk", "kubectl", "auto"], default="sdk")
    parser.add_argument("--retrieval-profile", default="java_exact")
    parser.add_argument("--model", default="gpt-5.4-mini")
    parser.add_argument("--codex-timeout-s", type=int, default=1800)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "docs" / "evaluations" / "patch-runs" / "claim-grade",
    )
    parser.add_argument("--api-host")
    parser.add_argument("--source-base", type=Path)
    parser.add_argument("--flink-root", type=Path)
    parser.add_argument("--kafka-root", type=Path)
    parser.add_argument("--keep-worktrees", action="store_true")
    parser.add_argument(
        "--skip-focused-tests",
        action="store_true",
        help="Do not pass --run-tests and do not require focused test evidence in the audit.",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser


if __name__ == "__main__":
    raise SystemExit(main())
