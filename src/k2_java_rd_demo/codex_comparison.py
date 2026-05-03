"""Codex answer comparison helpers for the Java R&D demo."""

from __future__ import annotations

import json
import subprocess
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ._subprocess_env import safe_subprocess_env
from .evaluation import EvalCase, EvalRun, compare_runs, normalize_result_row
from .source_links import REPO_WEB_REFS, repo_relative_path, repo_web_url


@dataclass(frozen=True)
class CodexCliConfig:
    """Non-interactive Codex execution settings."""

    codex_bin: str = "codex"
    model: str | None = None
    timeout_s: int = 900
    cwd: str = "/tmp"
    config_overrides: Sequence[str] = ()
    ignore_user_config: bool = True
    dangerously_bypass_approvals_and_sandbox: bool = False
    json_events_path: Path | None = None


def baseline_prompt(case: EvalCase) -> str:
    """Build the no-K2 prompt for one case."""

    return (
        "You are Codex in a controlled evaluation WITHOUT K2, MCP tools, web search, "
        "or local repository access.\n"
        "Do not run commands. Do not browse. Answer from your internal model knowledge only.\n"
        "If exact version-specific implementation details are uncertain, say so explicitly.\n\n"
        f"Customer question:\n{case.query}\n\n"
        "Return a concise engineering answer with these headings:\n"
        "Recommendation\nImplementation anchors\nTests to inspect or add\nCitations\nUncertainties\n"
        "Only put a source in Citations if you know the exact artifact or public path."
    )


def k2_context_prompt(
    case: EvalCase,
    rows: Sequence[Mapping[str, Any]],
    *,
    max_rows: int = 14,
    max_text_chars: int = 900,
) -> str:
    """Build the K2-assisted prompt for one case from retrieved evidence rows."""

    evidence = compact_evidence_rows(rows, max_rows=max_rows, max_text_chars=max_text_chars)
    return (
        "You are Codex in a controlled evaluation WITH K2 MCP context.\n"
        "Do not run commands. Do not browse. Treat the K2 results below as the MCP tool "
        "output for this turn.\n"
        "Use only these K2 sources for exact implementation claims. Make each important claim "
        "self-verifying from the final answer text. Prefer web_line_url or "
        "web_source_url citations when present; otherwise cite source_uri values inline in brackets. "
        "Omit broader related evidence unless it directly proves the answer. If evidence is "
        "incomplete, state the gap instead of guessing.\n"
        f"{_concise_k2_answer_contract()}\n\n"
        f"Customer question:\n{case.query}\n\n"
        "K2 MCP tool results:\n"
        f"{json.dumps(evidence, indent=2, sort_keys=True)}\n\n"
        "Return a concise engineering answer with these headings:\n"
        "Recommendation\nImplementation anchors\nTests to inspect or add\nCitations\nUncertainties\n"
    )


def k2_mcp_prompt(case: EvalCase) -> str:
    """Build the real-MCP prompt for one case.

    The prompt deliberately excludes ``target_class_names`` derived from
    ``ExpectedArtifact`` so that the benchmark does not leak answer-key
    class names into the eval prompt.  The LLM must discover relevant
    classes via retrieval alone.
    """

    framework = _case_framework(case)
    api_surface = _case_api_surface(case, framework)
    return (
        "You are Codex in a controlled evaluation WITH a real K2 stdio MCP server.\n"
        "Do not run shell commands. Do not browse. Before answering, call the available K2 MCP "
        "tool `k2_answer_with_sources` with exactly these arguments:\n"
        f"- query: {json.dumps(case.query)}\n"
        f"- framework: {json.dumps(framework)}\n"
        f"- api_surface: {json.dumps(api_surface)}\n"
        "- top_k: 8\n"
        "Use the returned K2 evidence for exact implementation claims. Make each important claim "
        "self-verifying from the final answer text. Prefer web_line_url or "
        "web_source_url citations when present; otherwise cite source_uri values inline in brackets. "
        "Omit broader related evidence unless it directly proves the answer. If the K2 evidence "
        "is incomplete, state the gap instead of guessing.\n"
        "Follow the tool's answer_style and preferred_sources fields when present.\n"
        f"{_concise_k2_answer_contract()}\n\n"
        f"Customer question:\n{case.query}\n\n"
        "Return a concise engineering answer with these headings:\n"
        "Recommendation\nImplementation anchors\nTests to inspect or add\nCitations\nUncertainties\n"
    )


def k2_mcp_uncoached_prompt(case: EvalCase) -> str:
    """Build a K2 MCP prompt without explicit retrieval choreography."""

    return (
        "You are Codex in a controlled evaluation. You may use the available retrieval "
        "tool if it helps answer the question, but do not run shell commands, browse, or "
        "use web search.\n"
        "Answer with concrete version-specific source evidence where available. If exact "
        "implementation details are uncertain, say so explicitly.\n\n"
        f"Customer question:\n{case.query}\n\n"
        "Return a concise engineering answer with these headings:\n"
        "Recommendation\nImplementation anchors\nTests to inspect or add\nCitations\nUncertainties\n"
    )


def grep_baseline_prompt(
    case: EvalCase,
    *,
    flink_root: str,
    kafka_root: str,
) -> str:
    """Build a local filesystem retrieval baseline prompt for Codex."""

    return (
        "You are Codex in a controlled evaluation with local repository access, but WITHOUT "
        "K2 or MCP tools.\n"
        "Use shell/file reads only for local retrieval. Do not browse and do not use web search. "
        "Prefer `rg` for search, inspect source/tests before answering, and cite exact "
        "repo-relative paths you verified.\n\n"
        "Available source checkouts:\n"
        f"- Apache Flink 2.2.0 root: {flink_root}\n"
        "  Citation prefix: repo://apache/flink@release-2.2.0/\n"
        f"  Public GitHub prefix: {REPO_WEB_REFS['flink@release-2.2.0'].github_blob_base}/\n"
        f"- Apache Kafka 4.2 root: {kafka_root}\n"
        "  Citation prefix: repo://apache/kafka@4.2/\n"
        f"  Public GitHub prefix: {REPO_WEB_REFS['kafka@4.2'].github_blob_base}/\n\n"
        "When citing a file in the final answer, prefer the public GitHub prefix plus the "
        "repo-relative path and line fragment when available. Keep repo:// citations only as "
        "internal fallback identifiers.\n\n"
        f"Customer question:\n{case.query}\n\n"
        "Return a concise engineering answer with these headings:\n"
        "Recommendation\nImplementation anchors\nTests to inspect or add\nCitations\nUncertainties\n"
    )


def _concise_k2_answer_contract() -> str:
    return (
        "Answer style: match a strong local `rg`/file-read answer. Start with the concrete "
        "implementation class/file and behavior, not a docs overview. Prefer code/test anchors "
        "over docs for implementation questions. When evidence includes web_line_url or "
        "web_source_url, cite that clickable URL. If not, cite line_source_uri or source_uri. "
        "Make every important claim self-verifying for a reader who only sees the final answer. "
        "Use line_snippet fields to name exact methods, "
        "config keys, enum values, helper return expressions, and registration paths. For Java "
        "config APIs, use code constants/enums as the exact key source and use docs only as "
        "version-pinned support. Always cite the requested target class or interface source "
        "when it appears in the tool output. When a helper is cited, state both the wrapper call "
        "and the concrete expression inside that helper. Do not cite broader related classes, docs, "
        "or tests unless they directly prove the answer. Do not put a missing-evidence note in Uncertainties "
        "until you have checked preferred_sources line_snippet values. Use 2-4 implementation bullets, "
        "1-3 direct test bullets, and cite only the sources you actually use. Do not mention K2, MCP, "
        "retrieval internals, scores, filters, or tool calls in the final answer. Put missing "
        "evidence only in the Uncertainties section."
    )


def compact_evidence_rows(
    rows: Sequence[Mapping[str, Any]],
    *,
    max_rows: int = 14,
    max_text_chars: int = 900,
) -> list[dict[str, Any]]:
    """Reduce K2 rows to prompt-sized evidence while preserving source diversity."""

    selected: list[Mapping[str, Any]] = []
    seen_keys: set[tuple[str, str]] = set()

    for row in rows:
        result = normalize_result_row(row, index=len(selected))
        key = (str(result.metadata.get("source_kind") or ""), result.source_uri)
        if key in seen_keys:
            continue
        seen_keys.add(key)
        selected.append(row)
        if len(selected) >= max_rows:
            break

    compact: list[dict[str, Any]] = []
    for index, row in enumerate(selected):
        result = normalize_result_row(row, index=index)
        metadata = result.metadata
        compact.append(
            {
                "rank": index + 1,
                "source_uri": result.source_uri,
                "web_source_url": row.get("web_source_url") or repo_web_url(result.source_uri),
                "line_source_uri": row.get("line_source_uri"),
                "web_line_url": row.get("web_line_url") or repo_web_url(row.get("line_source_uri")),
                "line_snippet": row.get("line_snippet"),
                "score": result.score,
                "source_kind": metadata.get("source_kind"),
                "module": metadata.get("module"),
                "api_surface": metadata.get("api_surface"),
                "class_name": metadata.get("class_name"),
                "path": metadata.get("path"),
                "text": result.text[:max_text_chars],
            }
        )
    return compact


def run_codex_answer(
    prompt: str,
    output_path: Path,
    config: CodexCliConfig | None = None,
    *,
    env_allow: frozenset[str] | set[str] | None = None,
) -> str:
    """Run ``codex exec`` and return the final assistant message."""

    selected = config or CodexCliConfig()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [selected.codex_bin]
    if selected.dangerously_bypass_approvals_and_sandbox:
        cmd.append("--dangerously-bypass-approvals-and-sandbox")
    else:
        cmd.extend(["-s", "read-only", "-a", "never"])
    cmd.extend(["-C", selected.cwd])
    for override in selected.config_overrides:
        cmd.extend(["-c", override])
    if selected.model:
        cmd.extend(["--model", selected.model])
    cmd.extend(
        [
            "exec",
            "--skip-git-repo-check",
            "--ephemeral",
            "--ignore-rules",
        ]
    )
    if selected.ignore_user_config:
        cmd.append("--ignore-user-config")
    if selected.json_events_path:
        selected.json_events_path.parent.mkdir(parents=True, exist_ok=True)
        cmd.append("--json")
    cmd.extend(
        [
            "--output-last-message",
            str(output_path),
        ]
    )
    cmd.append("-")
    completed = subprocess.run(
        cmd,
        input=prompt,
        text=True,
        capture_output=True,
        check=True,
        timeout=selected.timeout_s,
        env=safe_subprocess_env(allow={"OPENAI_API_KEY"} | (env_allow or set())),
    )
    if selected.json_events_path:
        selected.json_events_path.write_text(completed.stdout, encoding="utf-8")
    return output_path.read_text(encoding="utf-8").strip()


def evidence_rows_from_answer_citations(case: EvalCase, answer_text: str) -> list[dict[str, Any]]:
    """Build scorer rows from exact expected artifacts cited by a non-K2 baseline."""

    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for artifact in case.expected_artifacts:
        if not artifact.source_uri or artifact.source_uri in seen:
            continue
        if not _answer_cites_source(answer_text, artifact.source_uri):
            continue
        seen.add(artifact.source_uri)
        metadata = {
            key: value
            for key, value in {
                "source_kind": artifact.source_kind,
                "module": artifact.module,
                "api_surface": artifact.api_surface,
                "class_name": artifact.class_name,
                "path": repo_relative_path(artifact.source_uri),
                **artifact.metadata_equals,
            }.items()
            if value is not None
        }
        rows.append(
            {
                "source_uri": artifact.source_uri,
                "raw_text": "\n".join(artifact.text_contains),
                "metadata": metadata,
                "score": 1.0,
            }
        )
    return rows


def _case_framework(case: EvalCase) -> str:
    text = case.query.lower()
    return "kafka" if "kafka" in text else "flink"


def _case_api_surface(case: EvalCase, framework: str) -> str:
    if framework == "kafka":
        return "rest" if " rest " in f" {case.query.lower()} " else "connect"
    text = case.query.lower()
    return "checkpointing" if "checkpoint" in text or "savepoint" in text else "rest"


def _answer_cites_source(answer_text: str, source_uri: str) -> bool:
    if not answer_text:
        return False
    if source_uri in answer_text:
        return True
    web_url = repo_web_url(source_uri)
    if web_url and web_url in answer_text:
        return True
    path = repo_relative_path(source_uri)
    return bool(path and path in answer_text)


def build_answer_scorecard(
    cases: Sequence[EvalCase],
    *,
    baseline_answers: Mapping[str, str],
    k2_rows_by_case: Mapping[str, Sequence[Mapping[str, Any]]],
    k2_answers: Mapping[str, str],
    k2_run_name: str = "codex_with_k2_mcp_context",
) -> dict[str, Any]:
    """Score baseline and K2-assisted answer runs with the existing rubric."""

    return compare_runs(
        cases,
        [
            EvalRun(
                name="codex_without_k2",
                results_by_case={case.case_id: [] for case in cases},
                answers_by_case=dict(baseline_answers),
            ),
            EvalRun(
                name=k2_run_name,
                results_by_case={
                    case.case_id: list(k2_rows_by_case.get(case.case_id, ()))
                    for case in cases
                },
                answers_by_case=dict(k2_answers),
            ),
        ],
    )


__all__ = [
    "CodexCliConfig",
    "baseline_prompt",
    "build_answer_scorecard",
    "compact_evidence_rows",
    "evidence_rows_from_answer_citations",
    "grep_baseline_prompt",
    "k2_context_prompt",
    "k2_mcp_prompt",
    "k2_mcp_uncoached_prompt",
    "run_codex_answer",
]
