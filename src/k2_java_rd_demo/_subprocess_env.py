"""Subprocess environment sanitization to prevent credential leakage."""

from __future__ import annotations

import os


_REDACT_KEYS = frozenset({
    "ANTHROPIC_API_KEY",
    "K2_API_KEY",
    "OPENAI_API_KEY",
    "TAVILY_API_KEY",
})


def safe_subprocess_env(
    *,
    allow: frozenset[str] | set[str] | None = None,
    extra_redact: frozenset[str] | set[str] | None = None,
) -> dict[str, str]:
    """Build a sanitized copy of the environment for subprocess calls.

    By default, strips ``K2_API_KEY`` and ``TAVILY_API_KEY``.  Pass *allow*
    to explicitly re-include specific keys that would otherwise be stripped.
    Pass *extra_redact* to strip additional keys beyond the default set.
    """
    redact = _REDACT_KEYS | (extra_redact or set())
    if allow:
        redact = redact - allow

    return {
        key: value
        for key, value in os.environ.items()
        if key not in redact
    }
