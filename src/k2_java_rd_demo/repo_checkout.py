"""Pure checkout planning helpers for OSS Java R&D demo repositories."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, fields, is_dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from .source_catalog import CodeSourceManifest, code_source_manifests

DEFAULT_CHECKOUT_BASE_DIR = "/tmp/k2-java-rd-demo-sources"

Command = list[str]


@dataclass(frozen=True, kw_only=True)
class RepoCheckoutPlan:
    """A deterministic git checkout plan that callers may execute elsewhere."""

    repo: str
    repo_ref: str
    clone_url: str
    target_name: str
    target_dir: str
    sparse: bool
    include_paths: tuple[str, ...]
    exclude_paths: tuple[str, ...]
    commands: tuple[Command, ...]

    def to_dict(self) -> dict[str, Any]:
        return _jsonable(self)

    def to_json(self, *, indent: int | None = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)


def build_checkout_plan(
    source: CodeSourceManifest,
    base_dir: str | Path,
    *,
    sparse: bool = True,
) -> RepoCheckoutPlan:
    """Build a deterministic checkout plan for one code source manifest."""

    if not isinstance(source, CodeSourceManifest):
        raise TypeError("source must be a CodeSourceManifest")

    clone_url = _first_clone_url(source)
    target_name = _target_dir_name(source)
    target_dir = _target_dir(base_dir, target_name)
    include_paths = _string_tuple(source.include_paths)
    exclude_paths = _string_tuple(source.exclude_paths)
    commands = _checkout_commands(
        clone_url=clone_url,
        repo_ref=source.repo_ref,
        target_dir=target_dir,
        include_paths=include_paths,
        sparse=sparse,
    )
    return RepoCheckoutPlan(
        repo=source.repo,
        repo_ref=source.repo_ref,
        clone_url=clone_url,
        target_name=target_name,
        target_dir=target_dir,
        sparse=sparse,
        include_paths=include_paths,
        exclude_paths=exclude_paths,
        commands=commands,
    )


def build_checkout_plans(
    *,
    include_kafka: bool = False,
    base_dir: str | Path = DEFAULT_CHECKOUT_BASE_DIR,
    sparse: bool = True,
) -> tuple[RepoCheckoutPlan, ...]:
    """Build checkout plans for Flink by default, plus Kafka when requested."""

    return tuple(
        build_checkout_plan(source, base_dir=base_dir, sparse=sparse)
        for source in code_source_manifests(include_kafka=include_kafka)
    )


def checkout_plan_to_dict(plan: RepoCheckoutPlan) -> dict[str, Any]:
    """Return a CLI-friendly JSON-serializable dictionary for one plan."""

    return plan.to_dict()


def checkout_plans_to_dict(plans: Iterable[RepoCheckoutPlan]) -> list[dict[str, Any]]:
    """Return a CLI-friendly JSON-serializable list for multiple plans."""

    return [plan.to_dict() for plan in plans]


def checkout_plans_to_json(
    plans: Iterable[RepoCheckoutPlan],
    *,
    indent: int | None = 2,
) -> str:
    """Serialize checkout plans in a stable CLI-friendly JSON shape."""

    return json.dumps(checkout_plans_to_dict(plans), indent=indent, sort_keys=True)


def _checkout_commands(
    *,
    clone_url: str,
    repo_ref: str,
    target_dir: str,
    include_paths: tuple[str, ...],
    sparse: bool,
) -> tuple[Command, ...]:
    if sparse:
        if not include_paths:
            raise ValueError("sparse checkout plans require at least one include path")
        return (
            [
                "git",
                "clone",
                "--filter=blob:none",
                "--no-checkout",
                "--branch",
                repo_ref,
                clone_url,
                target_dir,
            ],
            ["git", "-C", target_dir, "sparse-checkout", "init", "--no-cone"],
            [
                "git",
                "-C",
                target_dir,
                "sparse-checkout",
                "set",
                "--no-cone",
                "--",
                *include_paths,
            ],
            ["git", "-C", target_dir, "checkout", repo_ref],
        )

    return (
        [
            "git",
            "clone",
            "--branch",
            repo_ref,
            "--single-branch",
            clone_url,
            target_dir,
        ],
    )


def _first_clone_url(source: CodeSourceManifest) -> str:
    if not source.clone_urls:
        raise ValueError(f"{source.repo} has no clone URL")
    return source.clone_urls[0]


def _target_dir(base_dir: str | Path, target_name: str) -> str:
    return (Path(base_dir) / target_name).as_posix()


def _target_dir_name(source: CodeSourceManifest) -> str:
    return _slugify(f"{source.repo}-{source.repo_ref}")


def _slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-")
    return slug.lower() or "source"


def _string_tuple(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(str(value).strip() for value in values if str(value).strip())


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {
            field.name: _jsonable(getattr(value, field.name))
            for field in fields(value)
        }
    if isinstance(value, tuple | list):
        return [_jsonable(item) for item in value]
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    return value


__all__ = [
    "DEFAULT_CHECKOUT_BASE_DIR",
    "RepoCheckoutPlan",
    "build_checkout_plan",
    "build_checkout_plans",
    "checkout_plan_to_dict",
    "checkout_plans_to_dict",
    "checkout_plans_to_json",
]
