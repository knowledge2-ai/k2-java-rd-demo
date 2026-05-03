"""Shared K2 project and corpus configuration.

All project and corpus identifiers live here so that ``k2_mcp_server``,
``live_k2``, and comparison scripts share a single source of truth.
Environment variables take precedence over the built-in defaults.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType


class K2ConfigError(RuntimeError):
    """Raised when required K2 configuration is missing or invalid."""


# ---------------------------------------------------------------------------
# Default identifiers (current demo environment, used as fallbacks)
# ---------------------------------------------------------------------------

_DEFAULT_PROJECT_ID = "8fb08a32-24e9-431f-8250-5a0a619b7232"

_DEFAULT_CORPUS_IDS: dict[str, str] = {
    "flink_docs": "e87160e6-c5e8-4bee-81eb-7f7d7b8cd331",
    "flink_code": "30876048-9127-4a6d-901e-a1bfd59fe7cc",
    "flink_code_part2": "a449a831-6600-41f2-a952-ba56a94de0fe",
    "flink_code_part3": "05ba36bb-3fac-4d61-90e4-afbd5f4c5a02",
    "kafka_docs": "6276668f-acff-4036-8c1e-a81ef48107cb",
    "kafka_code": "c9fb3bff-5527-4907-9eb3-cc5fa48ec01f",
    "guides": "09b34e8f-81a6-4b13-8f1b-9e92ac7eea40",
}

# ---------------------------------------------------------------------------
# Environment variable mapping (env var name → corpus role)
# ---------------------------------------------------------------------------

_CORPUS_ENV_VARS: dict[str, str] = {
    "K2_FLINK_DOCS_CORPUS_ID": "flink_docs",
    "K2_FLINK_CODE_CORPUS_ID": "flink_code",
    "K2_FLINK_CODE_PART2_CORPUS_ID": "flink_code_part2",
    "K2_FLINK_CODE_PART3_CORPUS_ID": "flink_code_part3",
    "K2_KAFKA_DOCS_CORPUS_ID": "kafka_docs",
    "K2_KAFKA_CODE_CORPUS_ID": "kafka_code",
    "K2_GUIDES_CORPUS_ID": "guides",
}


@dataclass(frozen=True)
class K2ProjectConfig:
    """Resolved K2 project and corpus identifiers."""

    project_id: str
    corpus_ids: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "corpus_ids", MappingProxyType(dict(self.corpus_ids)))

    def require_corpus(self, role: str) -> str:
        """Return the corpus ID for *role*, raising on missing."""
        corpus_id = self.corpus_ids.get(role)
        if not corpus_id:
            raise K2ConfigError(
                f"missing corpus ID for role {role!r}; "
                f"set the corresponding environment variable or check K2 config"
            )
        return corpus_id


def load_k2_config(environ: Mapping[str, str] | None = None) -> K2ProjectConfig:
    """Load K2 project config from environment variables, falling back to defaults.

    Environment variables override built-in defaults::

        K2_PROJECT_ID            → project_id
        K2_FLINK_DOCS_CORPUS_ID  → corpus_ids["flink_docs"]
        K2_FLINK_CODE_CORPUS_ID  → corpus_ids["flink_code"]
        ...etc (see _CORPUS_ENV_VARS)
    """
    env: Mapping[str, str] = os.environ if environ is None else environ

    project_id = _clean(env.get("K2_PROJECT_ID")) or _DEFAULT_PROJECT_ID

    corpus_ids = dict(_DEFAULT_CORPUS_IDS)
    for env_var, role in _CORPUS_ENV_VARS.items():
        value = _clean(env.get(env_var))
        if value:
            corpus_ids[role] = value

    return K2ProjectConfig(project_id=project_id, corpus_ids=corpus_ids)


def _clean(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    return cleaned if cleaned else None


__all__ = [
    "K2ConfigError",
    "K2ProjectConfig",
    "load_k2_config",
]
