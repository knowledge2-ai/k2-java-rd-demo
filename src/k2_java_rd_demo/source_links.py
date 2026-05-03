"""Public links for version-pinned Apache source artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote


@dataclass(frozen=True)
class RepoWebRef:
    """Mapping from an internal repo URI ref to a public immutable GitHub URL."""

    repo_uri_ref: str
    github_blob_base: str


REPO_WEB_REFS: dict[str, RepoWebRef] = {
    "flink@release-2.2.0": RepoWebRef(
        repo_uri_ref="flink@release-2.2.0",
        github_blob_base=(
            "https://github.com/apache/flink/blob/"
            "5a336892424a9458653ead89610bf60d771ab8d7"
        ),
    ),
    "kafka@4.2": RepoWebRef(
        repo_uri_ref="kafka@4.2",
        github_blob_base=(
            "https://github.com/apache/kafka/blob/"
            "ba74c3a289456f7346f2bece2cf76fcae55be9a4"
        ),
    ),
}


def repo_web_url(source_uri: object) -> str | None:
    """Convert a ``repo://apache/...`` URI to an immutable GitHub URL."""

    text = str(source_uri or "").strip()
    if not text.startswith("repo://apache/"):
        return None
    source, separator, fragment = text.partition("#")
    _prefix, _sep, rest = source.partition("repo://apache/")
    repo_ref, _path_sep, rel_path = rest.partition("/")
    if not rel_path:
        return None
    web_ref = REPO_WEB_REFS.get(repo_ref)
    if web_ref is None:
        return None
    url = f"{web_ref.github_blob_base}/{quote(rel_path, safe='/')}"
    if separator:
        url = f"{url}#{fragment}"
    return url


def repo_relative_path(source_uri: str) -> str:
    """Return the repository-relative path for a repo URI or URL-like source."""

    if not source_uri.startswith("repo://"):
        return source_uri
    _prefix, _sep, rest = source_uri.partition("@")
    _repo_ref, _path_sep, path = rest.partition("/")
    return path


__all__ = ["REPO_WEB_REFS", "repo_relative_path", "repo_web_url"]
