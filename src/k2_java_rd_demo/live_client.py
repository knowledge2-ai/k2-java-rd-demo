"""Guarded Knowledge2 SDK client factory for live demo commands."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from typing import Any

from .live_k2 import LiveK2ConfigError


@dataclass(frozen=True)
class LiveClientConfig:
    api_key_present: bool
    api_host: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def live_client_config_from_env(environ: Mapping[str, str] | None = None) -> LiveClientConfig:
    env = os.environ if environ is None else environ
    return LiveClientConfig(
        api_key_present=bool(_clean(env.get("K2_API_KEY"))),
        api_host=_clean(env.get("K2_API_HOST")) or _clean(env.get("K2_BASE_URL")),
    )


def create_knowledge2_client(
    environ: Mapping[str, str] | None = None,
    *,
    knowledge2_cls: type | None = None,
) -> Any:
    """Create a real Knowledge2 client from environment variables.

    The API key is read only for client construction and is never stored in the
    returned config summaries. Tests pass ``knowledge2_cls`` to avoid importing
    the optional SDK or making network calls.
    """

    env = os.environ if environ is None else environ
    api_key = _clean(env.get("K2_API_KEY"))
    if not api_key:
        raise LiveK2ConfigError("missing required environment variable: K2_API_KEY")

    api_host = _clean(env.get("K2_API_HOST")) or _clean(env.get("K2_BASE_URL"))
    selected_cls = knowledge2_cls or _import_knowledge2_class()
    kwargs: dict[str, Any] = {"api_key": api_key}
    if api_host:
        kwargs["api_host"] = api_host
    return selected_cls(**kwargs)


def _import_knowledge2_class() -> type:
    try:
        from sdk import Knowledge2  # type: ignore
    except ImportError as exc:
        raise LiveK2ConfigError(
            "Knowledge2 SDK is not installed. Install with `pip install '.[live]'` "
            "or provide a fake client in tests."
        ) from exc
    return Knowledge2


def _clean(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None
