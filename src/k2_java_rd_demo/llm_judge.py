"""Blinded LLM-as-judge comparison for generated benchmark answers."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import urllib.error
import urllib.request
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from ._subprocess_env import safe_subprocess_env
from .source_links import repo_web_url


JUDGE_SCHEMA = {
    "winner": "A | B | tie",
    "confidence": "number between 0 and 1",
    "scores": {
        "A": {
            "correctness": "integer 0-5",
            "grounding": "integer 0-5",
            "specificity": "integer 0-5",
            "usefulness": "integer 0-5",
            "risk": "integer 0-5, where 5 means low hallucination/deprecation risk",
        },
        "B": {
            "correctness": "integer 0-5",
            "grounding": "integer 0-5",
            "specificity": "integer 0-5",
            "usefulness": "integer 0-5",
            "risk": "integer 0-5, where 5 means low hallucination/deprecation risk",
        },
    },
    "rationale": "short technical explanation, 80 words max",
    "critical_issues": {"A": ["strings"], "B": ["strings"]},
}

DIMENSIONS = ("correctness", "grounding", "specificity", "usefulness", "risk")
IDENTITY_REPLACEMENTS = (
    (re.compile(r"\bK2 MCP evidence\b", re.IGNORECASE), "retrieved evidence"),
    (re.compile(r"\bK2 MCP context\b", re.IGNORECASE), "retrieved context"),
    (re.compile(r"\bK2 evidence\b", re.IGNORECASE), "retrieved evidence"),
    (re.compile(r"\bK2 search\b", re.IGNORECASE), "retrieval"),
    (re.compile(r"\bK2 result set\b", re.IGNORECASE), "retrieval result set"),
    (re.compile(r"\bK2 results\b", re.IGNORECASE), "retrieval results"),
    (re.compile(r"\bK2 returned\b", re.IGNORECASE), "retrieval returned"),
    (re.compile(r"\bK2 did not return\b", re.IGNORECASE), "retrieval did not return"),
    (re.compile(r"\bK2\b", re.IGNORECASE), "retrieval system"),
    (re.compile(r"\bMCP tool\b", re.IGNORECASE), "retrieval tool"),
    (re.compile(r"\bMCP context\b", re.IGNORECASE), "retrieved context"),
    (re.compile(r"\bMCP evidence\b", re.IGNORECASE), "retrieved evidence"),
    (re.compile(r"\bMCP\b", re.IGNORECASE), "retrieval tool"),
    (re.compile(r"\bCodex\b", re.IGNORECASE), "the assistant"),
)


@dataclass(frozen=True)
class JudgeCase:
    """One blinded pairwise judging item."""

    case_id: str
    title: str
    question: str
    reference: Mapping[str, Any]
    answer_a: str
    answer_b: str
    evidence_a: Sequence[Mapping[str, Any]]
    evidence_b: Sequence[Mapping[str, Any]]
    label_to_run: Mapping[str, str]


class JudgeClient(Protocol):
    """Client capable of returning one judge JSON object for a prompt."""

    def judge(self, prompt: str, *, output_path: Path | None = None) -> Mapping[str, Any]:
        """Return parsed judge output."""


@dataclass(frozen=True)
class CodexCliJudgeClient:
    """Run an isolated ``codex exec`` process as the judge."""

    codex_bin: str = "codex"
    model: str | None = None
    timeout_s: int = 600
    cwd: str = "/tmp"

    def judge(self, prompt: str, *, output_path: Path | None = None) -> Mapping[str, Any]:
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            return self._judge_to_path(prompt, output_path)
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "judge-output.json"
            return self._judge_to_path(prompt, target)

    def _judge_to_path(self, prompt: str, target: Path) -> Mapping[str, Any]:
        cmd = [
            self.codex_bin,
            "-s",
            "read-only",
            "-a",
            "never",
            "-C",
            self.cwd,
            "-c",
            "features.shell_tool=false",
            "-c",
            "features.browser_use=false",
            "-c",
            "features.web_search_request=false",
        ]
        if self.model:
            cmd.extend(["--model", self.model])
        cmd.extend(
            [
                "exec",
                "--skip-git-repo-check",
                "--ephemeral",
                "--ignore-rules",
                "--ignore-user-config",
                "--output-last-message",
                str(target),
                "-",
            ]
        )
        subprocess.run(
            cmd,
            input=prompt,
            text=True,
            capture_output=True,
            check=True,
            timeout=self.timeout_s,
            env=safe_subprocess_env(allow={"OPENAI_API_KEY"}),
        )
        return parse_judge_json(target.read_text(encoding="utf-8"))


@dataclass(frozen=True)
class ClaudeCliJudgeClient:
    """Run an isolated Claude Code process as the judge."""

    claude_bin: str = "claude"
    model: str | None = None
    timeout_s: int = 600
    cwd: str = "/tmp"

    def judge(self, prompt: str, *, output_path: Path | None = None) -> Mapping[str, Any]:
        cmd = [
            self.claude_bin,
            "--print",
            "--no-session-persistence",
            "--tools",
            "",
            "--output-format",
            "text",
        ]
        if self.model:
            cmd.extend(["--model", self.model])
        cmd.append(prompt)
        completed = subprocess.run(
            cmd,
            text=True,
            capture_output=True,
            check=True,
            timeout=self.timeout_s,
            cwd=self.cwd,
            env=safe_subprocess_env(allow={"ANTHROPIC_API_KEY"}),
        )
        raw = completed.stdout.strip()
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(raw, encoding="utf-8")
        return parse_judge_json(raw)


@dataclass(frozen=True)
class OpenAIResponsesJudgeClient:
    """Call the OpenAI Responses API using stdlib HTTP."""

    model: str
    api_key: str | None = None
    timeout_s: int = 120
    api_url: str = "https://api.openai.com/v1/responses"

    def judge(self, prompt: str, *, output_path: Path | None = None) -> Mapping[str, Any]:
        api_key = self.api_key or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is required for provider=openai")
        body = json.dumps(
            {
                "model": self.model,
                "input": prompt,
                "text": {"format": {"type": "json_object"}},
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            self.api_url,
            data=body,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_s) as response:
                response_body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenAI judge request failed: {exc.code} {detail}") from exc
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(response_body, encoding="utf-8")
        return parse_judge_json(_responses_text(response_body))


@dataclass(frozen=True)
class HeuristicJudgeClient:
    """Deterministic offline judge useful for tests and dry runs."""

    def judge(self, prompt: str, *, output_path: Path | None = None) -> Mapping[str, Any]:
        answer_a = _between(prompt, "ANSWER A", "ANSWER B")
        answer_b = prompt.split("ANSWER B", 1)[-1]
        score_a = _heuristic_answer_score(answer_a)
        score_b = _heuristic_answer_score(answer_b)
        if abs(score_a - score_b) < 0.01:
            winner = "tie"
        else:
            winner = "A" if score_a > score_b else "B"
        result = {
            "winner": winner,
            "confidence": round(min(0.95, 0.55 + abs(score_a - score_b)), 3),
            "scores": {
                "A": _dimension_scores(score_a),
                "B": _dimension_scores(score_b),
            },
            "rationale": "Deterministic dry-run score based on citations and version-specific markers.",
            "critical_issues": {"A": [], "B": []},
        }
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        return result


def build_judge_cases(
    payload: Mapping[str, Any],
    *,
    seed: str = "k2-llm-judge-v1",
    baseline_run: str | None = None,
    candidate_run: str | None = None,
    sanitize_system_identity: bool = True,
    include_evidence: bool = False,
) -> list[JudgeCase]:
    """Build blinded judge cases from a benchmark scorecard payload."""

    scorecard = _scorecard(payload)
    runs = {str(run["run_name"]): run for run in scorecard.get("runs", [])}
    if len(runs) < 2:
        raise ValueError("scorecard must contain at least two runs")
    baseline_name = baseline_run or str(scorecard.get("baseline_run") or next(iter(runs)))
    if baseline_name not in runs:
        raise ValueError(f"baseline run not found in scorecard: {baseline_name}")
    candidate_name = candidate_run or _comparison_run_name(scorecard, runs, baseline_name)
    if candidate_name not in runs:
        raise ValueError(f"candidate run not found in scorecard: {candidate_name}")
    if candidate_name == baseline_name:
        raise ValueError("candidate run must differ from baseline run")
    answers = payload.get("answers")
    if not isinstance(answers, Mapping):
        raise ValueError("payload must contain answers by run")
    baseline_answers = _answers_for_run(answers, baseline_name)
    candidate_answers = _answers_for_run(answers, candidate_name)
    catalog = {
        str(case["case_id"]): case
        for case in payload.get("cases", [])
        if isinstance(case, Mapping) and case.get("case_id")
    }
    case_ids = _ordered_case_ids(runs[baseline_name], runs[candidate_name], catalog)

    judge_cases = []
    for case_id in case_ids:
        catalog_case = catalog.get(case_id, {})
        baseline_answer = str(baseline_answers.get(case_id, "")).strip()
        candidate_answer = str(candidate_answers.get(case_id, "")).strip()
        if not baseline_answer or not candidate_answer:
            continue
        if sanitize_system_identity:
            baseline_answer = sanitize_answer_for_judge(baseline_answer)
            candidate_answer = sanitize_answer_for_judge(candidate_answer)
        label_to_run = _label_mapping(seed, case_id, baseline_name, candidate_name)
        run_to_answer = {
            baseline_name: baseline_answer,
            candidate_name: candidate_answer,
        }
        run_to_evidence = {
            baseline_name: _evidence_for_run(payload, baseline_name, case_id) if include_evidence else (),
            candidate_name: _evidence_for_run(payload, candidate_name, case_id) if include_evidence else (),
        }
        judge_cases.append(
            JudgeCase(
                case_id=case_id,
                title=str(catalog_case.get("title") or case_id),
                question=str(catalog_case.get("query") or _query_from_runs(runs, case_id)),
                reference=_judge_context_from_case(catalog_case),
                answer_a=run_to_answer[label_to_run["A"]],
                answer_b=run_to_answer[label_to_run["B"]],
                evidence_a=run_to_evidence[label_to_run["A"]],
                evidence_b=run_to_evidence[label_to_run["B"]],
                label_to_run=label_to_run,
            )
        )
    return judge_cases


def sanitize_answer_for_judge(answer: str) -> str:
    """Remove explicit system identity tokens from answers before blinded judging."""

    sanitized = answer
    for pattern, replacement in IDENTITY_REPLACEMENTS:
        sanitized = pattern.sub(replacement, sanitized)
    return sanitized


def build_judge_prompt(case: JudgeCase) -> str:
    """Return one strict JSON prompt for blinded pairwise answer judging."""

    return (
        "You are an independent senior Java and distributed-systems evaluator. "
        "Judge two answers to the same Apache Flink/Kafka R&D question.\n\n"
        "Rules:\n"
        "- The answer labels are randomized. Do not infer system identity from style, citations, "
        "or tool references.\n"
        "- Prefer the answer that is more correct, version-specific, grounded in concrete source "
        "artifacts, and useful for an engineer changing Java code.\n"
        "- Penalize fabricated APIs, deprecated or unsupported claims, vague guidance, missing "
        "uncertainty, and citations that do not support the claim.\n"
        "- If evidence snippets are provided, use them to verify cited methods/classes. Do not "
        "call a cited method fabricated when the evidence snippet contains that method.\n"
        "- If a cited claim is not supported by either the answer text or provided evidence, "
        "treat that as risk. Do not rely on general prior expectations over concrete evidence.\n"
        "- Use the evaluation context to understand topic scope; it is not a scoring rubric.\n"
        "- Return JSON only. No markdown, no prose outside JSON.\n\n"
        "Rubric dimensions, each integer 0-5:\n"
        "- correctness: technically correct for the named Flink/Kafka version and API surface.\n"
        "- grounding: cites or names relevant docs, implementation classes, tests, or source URIs.\n"
        "- specificity: gives concrete classes, methods, modules, tests, and implementation anchors.\n"
        "- usefulness: helps an engineer decide what to change or inspect next.\n"
        "- risk: avoids hallucinated classes, deprecated patterns, and overconfident unsupported claims.\n\n"
        f"Required output schema:\n{json.dumps(JUDGE_SCHEMA, indent=2)}\n\n"
        f"CASE ID: {case.case_id}\n"
        f"TITLE: {case.title}\n"
        f"QUESTION:\n{case.question}\n\n"
        f"EVALUATION CONTEXT:\n{json.dumps(case.reference, indent=2, sort_keys=True)}\n\n"
        f"ANSWER A:\n{case.answer_a}\n\n"
        f"EVIDENCE FOR ANSWER A:\n{json.dumps(_compact_evidence(case.evidence_a), indent=2, sort_keys=True)}\n\n"
        f"ANSWER B:\n{case.answer_b}\n"
        f"\nEVIDENCE FOR ANSWER B:\n{json.dumps(_compact_evidence(case.evidence_b), indent=2, sort_keys=True)}\n"
    )


def judge_case(case: JudgeCase, client: JudgeClient, *, raw_output_path: Path | None = None) -> dict[str, Any]:
    """Judge one case and map the blinded result back to run names."""

    raw_result = dict(client.judge(build_judge_prompt(case), output_path=raw_output_path))
    normalized = normalize_judge_result(raw_result)
    winner_label = normalized["winner"]
    winner_run = "tie" if winner_label == "tie" else case.label_to_run[winner_label]
    scores_by_run = {
        case.label_to_run[label]: normalized["scores"].get(label, {})
        for label in ("A", "B")
    }
    return {
        "case_id": case.case_id,
        "title": case.title,
        "question": case.question,
        "winner_label": winner_label,
        "winner_run": winner_run,
        "confidence": normalized["confidence"],
        "label_to_run": dict(case.label_to_run),
        "scores_by_label": normalized["scores"],
        "scores_by_run": scores_by_run,
        "rationale": normalized["rationale"],
        "critical_issues_by_label": normalized["critical_issues"],
        "critical_issues_by_run": {
            case.label_to_run[label]: normalized["critical_issues"].get(label, [])
            for label in ("A", "B")
        },
    }


def summarize_judge_results(results: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Aggregate mapped judge results."""

    winners = Counter(str(result.get("winner_run") or "invalid") for result in results)
    run_names = sorted(
        {
            run_name
            for result in results
            for run_name in (result.get("scores_by_run") or {})
            if isinstance(run_name, str)
        }
    )
    dimension_averages = {
        run_name: _average_dimensions(
            [
                result.get("scores_by_run", {}).get(run_name, {})
                for result in results
                if isinstance(result.get("scores_by_run"), Mapping)
            ]
        )
        for run_name in run_names
    }
    total = len(results)
    non_ties = total - winners.get("tie", 0)
    return {
        "case_count": total,
        "winner_counts": dict(sorted(winners.items())),
        "win_rates_excluding_ties": {
            run_name: round(winners.get(run_name, 0) / non_ties, 6) if non_ties else 0.0
            for run_name in run_names
        },
        "tie_rate": round(winners.get("tie", 0) / total, 6) if total else 0.0,
        "mean_confidence": round(
            sum(float(result.get("confidence") or 0.0) for result in results) / total,
            6,
        )
        if total
        else 0.0,
        "dimension_averages": dimension_averages,
    }


def render_judge_report(payload: Mapping[str, Any], judge_payload: Mapping[str, Any]) -> str:
    """Render a concise Markdown report for the judge run."""

    summary = judge_payload["summary"]
    scorecard = _scorecard(payload)
    deterministic_runs = {
        str(run["run_name"]): run for run in scorecard.get("runs", []) if isinstance(run, Mapping)
    }
    lines = [
        "# Blinded LLM-as-Judge Comparison",
        "",
        f"Generated: `{judge_payload.get('generated_at')}`",
        "",
        "## Method",
        "",
        "- The judge saw answer labels `A` and `B`; labels were deterministically randomized per case.",
        "- The judge did not see which answer came from K2 or the baseline until results were mapped back.",
        "- Explicit system identity tokens in answer text were normalized before judging.",
        "- The deterministic evidence-grounding scorecard remains the primary benchmark metric; this is a secondary qualitative preference check.",
        "- The reference checklist came from the published benchmark case metadata, not from either answer.",
        "",
        "## Aggregate Judge Results",
        "",
        f"- Cases judged: `{summary['case_count']}`",
        f"- Winner counts: `{json.dumps(summary['winner_counts'], sort_keys=True)}`",
        f"- Win rates excluding ties: `{json.dumps(summary['win_rates_excluding_ties'], sort_keys=True)}`",
        f"- Tie rate: `{summary['tie_rate']}`",
        f"- Mean confidence: `{summary['mean_confidence']}`",
        "",
        "## Deterministic Scorecard Context",
        "",
    ]
    for run_name, run in deterministic_runs.items():
        lines.append(
            f"- `{run_name}`: {_score_component_summary(run)}, "
            f"passed `{run.get('passed_cases')}/{run.get('case_count')}`"
        )
    lines.extend(
        [
            "",
            "## Dimension Averages",
            "",
            "| Run | Correctness | Grounding | Specificity | Usefulness | Risk |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for run_name, averages in summary["dimension_averages"].items():
        lines.append(
            "| {run} | `{correctness}` | `{grounding}` | `{specificity}` | `{usefulness}` | `{risk}` |".format(
                run=run_name,
                correctness=averages.get("correctness", 0),
                grounding=averages.get("grounding", 0),
                specificity=averages.get("specificity", 0),
                usefulness=averages.get("usefulness", 0),
                risk=averages.get("risk", 0),
            )
        )
    lines.extend(["", "## Per-Question Judge Decisions", ""])
    for index, result in enumerate(judge_payload["results"], start=1):
        lines.extend(
            [
                f"### {index}. {result['title']} (`{result['case_id']}`)",
                "",
                f"- Winner: `{result['winner_run']}`",
                f"- Confidence: `{result['confidence']}`",
                f"- Blinded label mapping: `{json.dumps(result['label_to_run'], sort_keys=True)}`",
                f"- Scores by run: `{json.dumps(result['scores_by_run'], sort_keys=True)}`",
                f"- Rationale: {result['rationale']}",
                "",
            ]
        )
    return "\n".join(lines)


def _score_component_summary(run: Mapping[str, Any]) -> str:
    components = run.get("score_components")
    if not isinstance(components, Mapping):
        metric_averages = run.get("metric_averages")
        if not isinstance(metric_averages, Mapping):
            metric_averages = {}
        components = {
            "combined_score": run.get("score"),
            "retrieval_score": metric_averages.get("retrieval_score_avg"),
            "answer_score": metric_averages.get("answer_score_avg"),
            "safety_score": metric_averages.get("hallucination_markers"),
        }
    return (
        f"combined `{_format_float(components.get('combined_score'))}`, "
        f"retrieval `{_format_float(components.get('retrieval_score'))}`, "
        f"answer `{_format_float(components.get('answer_score'))}`, "
        f"safety `{_format_float(components.get('safety_score'))}`"
    )


def _format_float(value: Any) -> str:
    if isinstance(value, (int, float)):
        return f"{float(value):.6f}".rstrip("0").rstrip(".")
    return ""


def parse_judge_json(raw: str) -> dict[str, Any]:
    """Parse JSON output, accepting occasional fenced JSON."""

    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    try:
        loaded = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end <= start:
            raise
        loaded = json.loads(text[start : end + 1])
    if not isinstance(loaded, dict):
        raise ValueError("judge output must be a JSON object")
    return loaded


def normalize_judge_result(result: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize and validate a judge JSON object."""

    winner = str(result.get("winner") or "").strip()
    if winner not in {"A", "B", "tie"}:
        raise ValueError(f"invalid judge winner: {winner!r}")
    confidence = float(result.get("confidence") or 0.0)
    if confidence < 0 or confidence > 1:
        raise ValueError("judge confidence must be between 0 and 1")
    scores = result.get("scores")
    if not isinstance(scores, Mapping):
        raise ValueError("judge result must contain scores")
    normalized_scores = {label: _normalized_dimension_scores(scores.get(label, {})) for label in ("A", "B")}
    issues = result.get("critical_issues")
    if not isinstance(issues, Mapping):
        issues = {}
    return {
        "winner": winner,
        "confidence": round(confidence, 6),
        "scores": normalized_scores,
        "rationale": str(result.get("rationale") or "").strip(),
        "critical_issues": {
            "A": _string_list(issues.get("A", [])),
            "B": _string_list(issues.get("B", [])),
        },
    }


def _scorecard(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    scorecard = payload.get("scorecard", payload)
    if not isinstance(scorecard, Mapping):
        raise ValueError("scorecard payload must be a JSON object")
    return scorecard


def _comparison_run_name(
    scorecard: Mapping[str, Any], runs: Mapping[str, Any], baseline_name: str
) -> str:
    comparisons = scorecard.get("comparisons")
    if isinstance(comparisons, Sequence) and not isinstance(comparisons, (str, bytes)):
        for comparison in comparisons:
            if isinstance(comparison, Mapping) and comparison.get("run_name"):
                name = str(comparison["run_name"])
                if name in runs:
                    return name
    for name in runs:
        if name != baseline_name:
            return name
    raise ValueError("could not find non-baseline run")


def _answers_for_run(answers: Mapping[str, Any], run_name: str) -> Mapping[str, Any]:
    run_answers = answers.get(run_name)
    if not isinstance(run_answers, Mapping):
        raise ValueError(f"answers missing for run {run_name}")
    return run_answers


def _evidence_for_run(
    payload: Mapping[str, Any],
    run_name: str,
    case_id: str,
) -> Sequence[Mapping[str, Any]]:
    rows_by_run = payload.get("rows_by_run")
    if isinstance(rows_by_run, Mapping):
        run_rows = rows_by_run.get(run_name)
        if isinstance(run_rows, Mapping):
            rows = run_rows.get(case_id)
            if isinstance(rows, Sequence) and not isinstance(rows, (str, bytes)):
                return [row for row in rows if isinstance(row, Mapping)]
    if run_name == "codex_with_k2_real_mcp":
        rows_by_case = payload.get("rows_by_case")
        if isinstance(rows_by_case, Mapping):
            rows = rows_by_case.get(case_id)
            if isinstance(rows, Sequence) and not isinstance(rows, (str, bytes)):
                return [row for row in rows if isinstance(row, Mapping)]
    return ()


def _compact_evidence(rows: Sequence[Mapping[str, Any]], *, max_rows: int = 16) -> list[dict[str, Any]]:
    compact = []
    for row in rows[:max_rows]:
        metadata = row.get("metadata") if isinstance(row.get("metadata"), Mapping) else {}
        text = str(row.get("line_snippet") or row.get("raw_text") or row.get("text") or "")
        compact.append(
            {
                "source_uri": row.get("source_uri"),
                "web_source_url": row.get("web_source_url") or repo_web_url(row.get("source_uri")),
                "line_source_uri": row.get("line_source_uri"),
                "web_line_url": row.get("web_line_url") or repo_web_url(row.get("line_source_uri")),
                "source_kind": metadata.get("source_kind") or row.get("source_kind"),
                "module": metadata.get("module") or row.get("module"),
                "api_surface": metadata.get("api_surface") or row.get("api_surface"),
                "class_name": metadata.get("class_name") or row.get("class_name"),
                "path": metadata.get("path") or row.get("path"),
                "snippet": text[:700],
            }
        )
    return compact


def _ordered_case_ids(
    baseline_run: Mapping[str, Any],
    candidate_run: Mapping[str, Any],
    catalog: Mapping[str, Any],
) -> list[str]:
    ordered = []
    for run in (candidate_run, baseline_run):
        cases = run.get("cases", [])
        if isinstance(cases, Sequence) and not isinstance(cases, (str, bytes)):
            for case in cases:
                if isinstance(case, Mapping) and case.get("case_id"):
                    ordered.append(str(case["case_id"]))
    ordered.extend(catalog)
    return list(dict.fromkeys(ordered))


def _label_mapping(seed: str, case_id: str, baseline_name: str, candidate_name: str) -> dict[str, str]:
    digest = hashlib.sha256(f"{seed}:{case_id}".encode("utf-8")).hexdigest()
    if int(digest[:8], 16) % 2 == 0:
        return {"A": baseline_name, "B": candidate_name}
    return {"A": candidate_name, "B": baseline_name}


def _query_from_runs(runs: Mapping[str, Any], case_id: str) -> str:
    for run in runs.values():
        if not isinstance(run, Mapping):
            continue
        for case in run.get("cases", []):
            if isinstance(case, Mapping) and case.get("case_id") == case_id:
                return str(case.get("query") or "")
    return ""


def _judge_context_from_case(case: Mapping[str, Any]) -> dict[str, Any]:
    """Build evaluation context for the LLM judge WITHOUT answer-key artifacts.

    This deliberately excludes source_uri, class_name, path_contains, and
    required_source_uris — those are answer-key fields that would make the
    judge oracle-assisted.  Only topic-level context is provided.
    """
    return {
        "expected_source_kinds": list(case.get("expected_source_kinds") or []),
        "required_modules": list(case.get("required_modules") or []),
        "required_api_surfaces": list(case.get("required_api_surfaces") or []),
        "hallucination_markers": list(case.get("hallucination_markers") or []),
    }


def _responses_text(response_body: str) -> str:
    loaded = json.loads(response_body)
    if isinstance(loaded, Mapping):
        output_text = loaded.get("output_text")
        if isinstance(output_text, str):
            return output_text
        fragments: list[str] = []
        for item in loaded.get("output", []):
            if not isinstance(item, Mapping):
                continue
            for content in item.get("content", []):
                if isinstance(content, Mapping) and isinstance(content.get("text"), str):
                    fragments.append(content["text"])
        if fragments:
            return "\n".join(fragments)
    return response_body


def _normalized_dimension_scores(value: Any) -> dict[str, int]:
    if not isinstance(value, Mapping):
        value = {}
    return {dimension: _score_0_to_5(value.get(dimension)) for dimension in DIMENSIONS}


def _score_0_to_5(value: Any) -> int:
    try:
        score = int(round(float(value)))
    except (TypeError, ValueError):
        return 0
    return max(0, min(5, score))


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        return []
    return [str(item) for item in value if item is not None]


def _average_dimensions(rows: Sequence[Mapping[str, Any]]) -> dict[str, float]:
    averages = {}
    for dimension in DIMENSIONS:
        values = [
            float(row.get(dimension))
            for row in rows
            if isinstance(row, Mapping) and isinstance(row.get(dimension), (int, float))
        ]
        averages[dimension] = round(sum(values) / len(values), 6) if values else 0.0
    return averages


def _between(text: str, start_marker: str, end_marker: str) -> str:
    if start_marker not in text:
        return ""
    remainder = text.split(start_marker, 1)[1]
    if end_marker not in remainder:
        return remainder
    return remainder.split(end_marker, 1)[0]


def _heuristic_answer_score(answer: str) -> float:
    lowered = answer.lower()
    return min(
        1.0,
        0.1 * (lowered.count("repo://") + lowered.count("github.com/apache/"))
        + 0.08 * lowered.count("release-")
        + 0.06 * lowered.count("test")
        + 0.06 * lowered.count("class")
        + 0.04 * lowered.count("uncertain"),
    )


def _dimension_scores(score: float) -> dict[str, int]:
    scaled = max(0, min(5, round(score * 5)))
    return {dimension: scaled for dimension in DIMENSIONS}


__all__ = [
    "ClaudeCliJudgeClient",
    "CodexCliJudgeClient",
    "HeuristicJudgeClient",
    "JudgeCase",
    "OpenAIResponsesJudgeClient",
    "build_judge_cases",
    "build_judge_prompt",
    "judge_case",
    "normalize_judge_result",
    "parse_judge_json",
    "render_judge_report",
    "sanitize_answer_for_judge",
    "summarize_judge_results",
]
