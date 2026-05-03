#!/usr/bin/env python3
"""Generate per-question benchmark statistics from a scorecard payload."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from k2_java_rd_demo.question_stats import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
