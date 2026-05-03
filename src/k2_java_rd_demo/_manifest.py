"""Reproducibility manifest for scorecard and evaluation outputs."""

from __future__ import annotations

import os
import platform
import subprocess
from datetime import datetime, timezone
from typing import Any

from ._subprocess_env import safe_subprocess_env


def build_reproducibility_manifest() -> dict[str, Any]:
    """Build a manifest capturing the environment used to produce results."""
    return {
        "git_sha": _git_sha(),
        "git_dirty": _git_dirty(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "env_flags": _env_presence_flags(),
    }


def _git_sha() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
            env=safe_subprocess_env(),
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def _git_dirty() -> bool | None:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
            env=safe_subprocess_env(),
        )
        if result.returncode == 0:
            return bool(result.stdout.strip())
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


_ENV_FLAG_KEYS = (
    "K2_API_KEY",
    "OPENAI_API_KEY",
    "TAVILY_API_KEY",
    "K2_PROJECT_ID",
    "K2_API_HOST",
)


def _env_presence_flags() -> dict[str, bool]:
    return {key: bool(os.environ.get(key)) for key in _ENV_FLAG_KEYS}
