#!/usr/bin/env python3
"""Merge patch-generation scorecards after selective retry runs."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from k2_java_rd_demo.patch_benchmark import (  # noqa: E402
    merge_patch_scorecard_payloads,
    render_patch_report,
)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    payloads = [
        json.loads(scorecard.read_text(encoding="utf-8"))
        for scorecard in args.scorecards
    ]
    merged = merge_patch_scorecard_payloads(payloads, prefer_later=not args.keep_first_valid)
    merged["generated_at"] = datetime.now(UTC).isoformat()
    merged["run_id"] = args.run_id or f"{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}-merged"
    merged["merged_scorecards"] = [str(scorecard) for scorecard in args.scorecards]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(merged, indent=2, sort_keys=True), encoding="utf-8")
    report_path = args.report or args.output.with_name("patch-report.md")
    report_path.write_text(render_patch_report(merged), encoding="utf-8")
    print(
        json.dumps(
            {
                "scorecard_path": str(args.output),
                "report_path": str(report_path),
                "summary": merged["summary"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scorecards", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument(
        "--keep-first-valid",
        action="store_true",
        help=(
            "Only replace an earlier row when it is infrastructure-invalid and the "
            "later retry is valid. By default, later valid rows replace earlier rows."
        ),
    )
    return parser


if __name__ == "__main__":
    raise SystemExit(main())
