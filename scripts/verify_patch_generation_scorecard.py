#!/usr/bin/env python3
"""Audit whether a patch-generation scorecard supports a K2 customer claim."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

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
    payload = json.loads(args.scorecard_json.read_text(encoding="utf-8"))
    audit = verify_patch_scorecard_evidence(
        payload,
        baseline_arm=args.baseline_arm,
        treatment_arm=args.treatment_arm,
        min_tasks_for_claim=args.min_tasks_for_claim,
        require_k2_probe=not args.allow_missing_k2_probe,
        require_k2_tools=not args.allow_missing_k2_tool_calls,
        require_focused_tests=args.require_focused_tests,
    )
    if args.format == "json":
        print(json.dumps(audit, indent=2, sort_keys=True))
    else:
        print(render_patch_scorecard_audit(audit))
    return 0 if audit["claim_ready"] else 1


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scorecard_json", type=Path)
    parser.add_argument("--baseline-arm", default="codex_repo_plus_guides_dump")
    parser.add_argument("--treatment-arm", default="codex_with_k2_mcp")
    parser.add_argument("--min-tasks-for-claim", type=int, default=10)
    parser.add_argument("--require-focused-tests", action="store_true")
    parser.add_argument("--allow-missing-k2-probe", action="store_true")
    parser.add_argument("--allow-missing-k2-tool-calls", action="store_true")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    return parser


if __name__ == "__main__":
    raise SystemExit(main())
