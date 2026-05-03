"""Customer-value scorecard for Java shops with Confluence guardrails."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CustomerValueScenario:
    """A demo scenario where private guides matter as much as code lookup."""

    scenario_id: str
    title: str
    framework: str
    api_surface: str
    feature_request: str
    guide_source_uris: Sequence[str]
    code_source_uris: Sequence[str]
    test_source_uris: Sequence[str]
    required_terms: Sequence[str]
    guardrail_ids: Sequence[str]
    forbidden_patterns: Sequence[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        for attr in (
            "guide_source_uris",
            "code_source_uris",
            "test_source_uris",
            "required_terms",
            "guardrail_ids",
            "forbidden_patterns",
        ):
            object.__setattr__(self, attr, tuple(str(value) for value in getattr(self, attr)))

    def to_dict(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "title": self.title,
            "framework": self.framework,
            "api_surface": self.api_surface,
            "feature_request": self.feature_request,
            "guide_source_uris": list(self.guide_source_uris),
            "code_source_uris": list(self.code_source_uris),
            "test_source_uris": list(self.test_source_uris),
            "required_terms": list(self.required_terms),
            "guardrail_ids": list(self.guardrail_ids),
            "forbidden_patterns": list(self.forbidden_patterns),
        }


ARMS = (
    "baseline_no_retrieval",
    "repo_only",
    "k2_guides_docs_code_tests",
)


def customer_value_scenarios(*, include_kafka: bool = True) -> tuple[CustomerValueScenario, ...]:
    """Return scenarios that model a legacy Java shop with internal guide pages."""

    scenarios = [
        CustomerValueScenario(
            scenario_id="flink-rest-controller-guardrails",
            title="Flink controller-like REST endpoint with internal guardrails",
            framework="flink",
            api_surface="rest",
            feature_request=(
                "Add a REST endpoint for a running job checkpoint summary. Produce the "
                "implementation plan before editing."
            ),
            guide_source_uris=(
                "generated://guides/flink/confluence-rest-handler-guardrails.md",
            ),
            code_source_uris=(
                "repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/"
                "org/apache/flink/runtime/rest/handler/AbstractRestHandler.java",
                "repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/"
                "org/apache/flink/runtime/webmonitor/WebMonitorEndpoint.java",
            ),
            test_source_uris=(
                "repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/"
                "org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java",
            ),
            required_terms=(
                "MessageHeaders",
                "AbstractRestHandler",
                "WebMonitorEndpoint",
                "serialization tests",
            ),
            guardrail_ids=("CF-FLINK-REST-001",),
            forbidden_patterns=("Spring MVC", "JAX-RS", "servlet controller"),
        ),
        CustomerValueScenario(
            scenario_id="flink-checkpointing-upgrade-guardrails",
            title="Flink checkpointing change with upgrade guardrails",
            framework="flink",
            api_surface="checkpointing",
            feature_request=(
                "Add checkpoint summary behavior without regressing Flink 2.2 upgrade "
                "and savepoint compatibility."
            ),
            guide_source_uris=(
                "generated://guides/flink/confluence-checkpoint-upgrade-guardrails.md",
            ),
            code_source_uris=(
                "repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/"
                "org/apache/flink/runtime/checkpoint/CheckpointCoordinator.java",
            ),
            test_source_uris=(
                "repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/"
                "org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java",
            ),
            required_terms=(
                "checkpointing",
                "savepoint",
                "migration risk",
                "focused checkpointing tests",
            ),
            guardrail_ids=("CF-FLINK-CKPT-004",),
            forbidden_patterns=("FsStateBackend", "MemoryStateBackend"),
        ),
    ]
    if include_kafka:
        scenarios.append(
            CustomerValueScenario(
                scenario_id="kafka-connect-rest-entity-guardrails",
                title="Kafka Connect REST entity with compatibility guardrails",
                framework="kafka",
                api_surface="connect",
                feature_request=(
                    "Add an optional JSON field to a Kafka Connect REST entity while "
                    "preserving backwards compatibility."
                ),
                guide_source_uris=(
                    "generated://guides/kafka/confluence-connect-rest-entity-guardrails.md",
                ),
                code_source_uris=(
                    "repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/"
                    "kafka/connect/runtime/rest/entities/CreateConnectorRequest.java",
                ),
                test_source_uris=(
                    "repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/"
                    "kafka/connect/runtime/rest/entities/CreateConnectorRequestTest.java",
                ),
                required_terms=(
                    "backwards-compatible",
                    "optional JSON field",
                    "Jackson",
                    "serialization/deserialization test",
                ),
                guardrail_ids=("CF-KAFKA-CONNECT-007",),
                forbidden_patterns=("Spring Validator", "Bean Validation", "javax.validation"),
            )
        )
    return tuple(scenarios)


def customer_value_prompt(scenario: CustomerValueScenario, *, arm_name: str) -> str:
    """Build a side-by-side demo prompt for one arm."""

    if arm_name not in ARMS:
        raise ValueError(f"unknown customer-value arm: {arm_name}")
    if arm_name == "baseline_no_retrieval":
        context_clause = (
            "Use only the feature request. Do not use repository search, docs, K2, "
            "MCP, or Confluence-style guides."
        )
    elif arm_name == "repo_only":
        context_clause = (
            "Use local repository search and file reads only. Do not use K2, MCP, "
            "or Confluence-style guide pages."
        )
    else:
        context_clause = (
            "Use K2 MCP retrieval before planning. Retrieve guide pages first, then "
            "version-pinned docs, production code, and neighboring tests. Your plan "
            "must cite the retrieved guide, code, and test sources."
        )
    return (
        "You are running a controlled customer-value demo for a legacy Java R&D team.\n"
        f"{context_clause}\n\n"
        f"Framework/API: {scenario.framework} {scenario.api_surface}\n"
        f"Task: {scenario.title}\n\n"
        f"Feature request:\n{scenario.feature_request}\n\n"
        "Final response requirements:\n"
        "- Provide an implementation plan, not a full patch.\n"
        "- Cite every source used.\n"
        "- List tests to add or inspect.\n"
        "- State any internal guardrails you found. If none are available, say so.\n"
    )


def customer_value_scorecard(*, include_kafka: bool = True) -> dict[str, Any]:
    """Return a deterministic dry-run scorecard for the customer demo story."""

    scenarios = customer_value_scenarios(include_kafka=include_kafka)
    runs = []
    for scenario in scenarios:
        for arm_name in ARMS:
            answer = _synthetic_answer(scenario, arm_name)
            retrieved_rows = _synthetic_rows(scenario, arm_name)
            runs.append(
                {
                    **score_customer_value_answer(
                        scenario,
                        answer_text=answer,
                        retrieved_rows=retrieved_rows,
                    ),
                    "arm_name": arm_name,
                    "answer": answer,
                    "retrieved_source_uris": [
                        str(row.get("source_uri")) for row in retrieved_rows if row.get("source_uri")
                    ],
                }
            )
    return {
        "method": "customer_value_guardrail_scorecard",
        "claim": (
            "K2 is evaluated as a governed cross-corpus context layer, not as a "
            "replacement for local grep."
        ),
        "scenarios": [scenario.to_dict() for scenario in scenarios],
        "summary": _summarize_runs(runs),
        "runs": runs,
    }


def score_customer_value_answer(
    scenario: CustomerValueScenario,
    *,
    answer_text: str,
    retrieved_rows: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Score answer quality for guide-governed Java feature planning."""

    evidence_text = _combined_text(answer_text, retrieved_rows)
    guide_score = _coverage(evidence_text, (*scenario.guardrail_ids, *scenario.guide_source_uris))
    code_score = _coverage(evidence_text, scenario.code_source_uris)
    test_score = _coverage(evidence_text, scenario.test_source_uris)
    implementation_score = _coverage(evidence_text, scenario.required_terms)
    forbidden_hits = _matched_patterns(evidence_text, scenario.forbidden_patterns)
    safety_score = 0.0 if forbidden_hits else 1.0
    cross_corpus_score = (guide_score + code_score + test_score) / 3
    score = (
        guide_score * 0.35
        + cross_corpus_score * 0.25
        + implementation_score * 0.25
        + safety_score * 0.15
    )
    return {
        "scenario_id": scenario.scenario_id,
        "title": scenario.title,
        "framework": scenario.framework,
        "api_surface": scenario.api_surface,
        "score": round(score, 6),
        "passed": score >= 0.8,
        "score_breakdown": {
            "guide_guardrail_score": round(guide_score, 6),
            "code_evidence_score": round(code_score, 6),
            "test_evidence_score": round(test_score, 6),
            "cross_corpus_score": round(cross_corpus_score, 6),
            "implementation_pattern_score": round(implementation_score, 6),
            "forbidden_marker_safety": safety_score,
        },
        "forbidden_hits": forbidden_hits,
    }


def render_customer_value_report(payload: Mapping[str, Any]) -> str:
    """Render a compact customer-facing guardrail scorecard."""

    lines = [
        "# Customer-Value Guardrail Demo",
        "",
        "This dry-run scorecard models a legacy Java shop where internal guide pages "
        "govern how code should be changed. It is not a claim that K2 beats `rg` "
        "for exact local file lookup.",
        "",
        "## Summary",
        "",
        "| Arm | Scenarios | Passed | Mean score |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in payload.get("summary", {}).get("arms", []):
        lines.append(
            "| {arm} | `{count}` | `{passed}` | `{score}` |".format(
                arm=row.get("arm_name"),
                count=row.get("scenario_count"),
                passed=row.get("passed_scenarios"),
                score=_format_float(row.get("mean_score")),
            )
        )
    lines.extend(
        [
            "",
            "## What This Demonstrates",
            "",
            "- Baseline can produce plausible Java plans without knowing company rules.",
            "- Repo-only search can find implementation classes but still miss Confluence-style guardrails.",
            "- K2 is valuable when the agent must combine guides, docs, code, and tests with citations.",
            "",
            "## Per-Scenario Results",
            "",
        ]
    )
    for run in payload.get("runs", []):
        breakdown = json.dumps(run.get("score_breakdown") or {}, sort_keys=True)
        lines.extend(
            [
                f"### {run.get('title')} (`{run.get('scenario_id')}`)",
                "",
                f"- Arm: `{run.get('arm_name')}`",
                f"- Score: `{_format_float(run.get('score'))}`",
                f"- Passed: `{str(run.get('passed')).lower()}`",
                f"- Score breakdown: `{breakdown}`",
                f"- Forbidden hits: `{json.dumps(run.get('forbidden_hits') or [])}`",
                "",
            ]
        )
    return "\n".join(lines)


def _synthetic_rows(
    scenario: CustomerValueScenario,
    arm_name: str,
) -> list[dict[str, Any]]:
    if arm_name == "baseline_no_retrieval":
        return []
    uris: list[str] = []
    if arm_name == "repo_only":
        uris.extend((*scenario.code_source_uris, *scenario.test_source_uris))
    else:
        uris.extend(
            (
                *scenario.guide_source_uris,
                *scenario.code_source_uris,
                *scenario.test_source_uris,
            )
        )
    return [{"source_uri": uri, "raw_text": uri, "metadata": {}} for uri in uris]


def _synthetic_answer(scenario: CustomerValueScenario, arm_name: str) -> str:
    if arm_name == "baseline_no_retrieval":
        forbidden = scenario.forbidden_patterns[0] if scenario.forbidden_patterns else "generic Java"
        return (
            f"Implement this as a {forbidden} style Java endpoint and add basic unit tests. "
            "No internal guardrails were available."
        )
    if arm_name == "repo_only":
        return (
            "Use the nearest repository implementation and test pattern: "
            f"{' '.join(scenario.required_terms[:2])}. Cite "
            f"{' '.join((*scenario.code_source_uris, *scenario.test_source_uris))}."
        )
    return (
        f"Apply internal guardrail {' '.join(scenario.guardrail_ids)} before editing. "
        f"Use {' '.join(scenario.required_terms)}. Cite "
        f"{' '.join((*scenario.guide_source_uris, *scenario.code_source_uris, *scenario.test_source_uris))}."
    )


def _combined_text(answer_text: str, rows: Sequence[Mapping[str, Any]]) -> str:
    parts = [answer_text]
    for row in rows:
        for key in ("source_uri", "raw_text", "text"):
            value = row.get(key)
            if isinstance(value, str):
                parts.append(value)
    return "\n".join(parts)


def _coverage(haystack: str, needles: Sequence[str]) -> float:
    if not needles:
        return 1.0
    normalized = _normalize(haystack)
    hits = sum(1 for needle in needles if _normalize(needle) in normalized)
    return hits / len(needles)


def _matched_patterns(haystack: str, patterns: Sequence[str]) -> list[str]:
    matches = []
    for pattern in patterns:
        if re.search(re.escape(pattern), haystack, flags=re.IGNORECASE):
            matches.append(pattern)
    return matches


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def _summarize_runs(runs: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_arm: dict[str, list[Mapping[str, Any]]] = {}
    for run in runs:
        by_arm.setdefault(str(run.get("arm_name")), []).append(run)
    return {
        "arms": [
            {
                "arm_name": arm,
                "scenario_count": len(arm_runs),
                "passed_scenarios": sum(1 for run in arm_runs if run.get("passed")),
                "mean_score": _mean(float(run.get("score") or 0.0) for run in arm_runs),
            }
            for arm, arm_runs in sorted(by_arm.items())
        ]
    }


def _mean(values: Sequence[float] | Any) -> float:
    materialized = list(values)
    if not materialized:
        return 0.0
    return round(sum(materialized) / len(materialized), 6)


def _format_float(value: Any) -> str:
    if isinstance(value, (int, float)):
        return f"{float(value):.6f}".rstrip("0").rstrip(".")
    return ""


__all__ = [
    "ARMS",
    "CustomerValueScenario",
    "customer_value_prompt",
    "customer_value_scenarios",
    "customer_value_scorecard",
    "render_customer_value_report",
    "score_customer_value_answer",
]
