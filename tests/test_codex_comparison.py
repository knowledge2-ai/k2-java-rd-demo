from __future__ import annotations

import unittest

from tests import _paths  # noqa: F401

from k2_java_rd_demo.codex_comparison import (
    baseline_prompt,
    build_answer_scorecard,
    compact_evidence_rows,
    evidence_rows_from_answer_citations,
    grep_baseline_prompt,
    k2_context_prompt,
    k2_mcp_prompt,
    k2_mcp_uncoached_prompt,
)
from k2_java_rd_demo.eval_cases import evaluation_cases
from k2_java_rd_demo.evaluation import EvalCase, ExpectedArtifact
from k2_java_rd_demo.k2_mcp_server import _answer_queries


class CodexComparisonTests(unittest.TestCase):
    def test_prompts_separate_no_context_from_k2_context(self) -> None:
        case = _case()
        row = _row()

        without_k2 = baseline_prompt(case)
        with_k2 = k2_context_prompt(case, [row], max_rows=3, max_text_chars=50)

        self.assertIn("WITHOUT K2", without_k2)
        self.assertIn(case.query, without_k2)
        self.assertIn("WITH K2 MCP context", with_k2)
        self.assertIn("repo://apache/flink@release-2.2.0/Foo.java", with_k2)
        self.assertIn("AbstractRestHandler", with_k2)

        real_mcp = k2_mcp_prompt(case)
        self.assertIn("real K2 stdio MCP server", real_mcp)
        self.assertIn("k2_answer_with_sources", real_mcp)
        self.assertIn("top_k: 8", real_mcp)
        self.assertIn('api_surface: "rest"', real_mcp)
        self.assertIn("local `rg`/file-read answer", real_mcp)
        self.assertIn("Prefer code/test anchors", real_mcp)
        self.assertIn("line_source_uri", real_mcp)
        self.assertIn("web_line_url", real_mcp)
        self.assertIn("self-verifying", real_mcp)
        self.assertIn("Omit broader related evidence", real_mcp)
        # target_class_names must NOT appear -- that would leak answer keys
        self.assertNotIn("target_class_names", real_mcp)
        self.assertNotIn("Foo", real_mcp)

    def test_compact_evidence_rows_dedupes_source_kind_uri_pairs(self) -> None:
        rows = [_row(), _row(score=0.5), _row(source_uri="repo://other")]

        compact = compact_evidence_rows(rows, max_rows=10, max_text_chars=12)

        self.assertEqual(len(compact), 2)
        self.assertEqual(compact[0]["rank"], 1)
        self.assertEqual(compact[0]["text"], "class Foo ex")
        self.assertIn("line_snippet", compact[0])
        self.assertEqual(
            compact[0]["web_source_url"],
            (
                "https://github.com/apache/flink/blob/"
                "5a336892424a9458653ead89610bf60d771ab8d7/Foo.java"
            ),
        )

    def test_k2_mcp_prompt_excludes_expected_artifact_classes(self) -> None:
        """The MCP prompt must not leak class names from ExpectedArtifact."""
        case = EvalCase(
            case_id="case-leak",
            query="How do I add a Flink REST handler?",
            expected_artifacts=(
                ExpectedArtifact(
                    key="handler",
                    source_uri="repo://apache/flink@release-2.2.0/DispatcherRestEndpoint.java",
                    source_kind="code",
                    module="flink-runtime",
                    api_surface="rest",
                    class_name="DispatcherRestEndpoint",
                    text_contains=("initializeHandlers",),
                ),
                ExpectedArtifact(
                    key="details",
                    source_uri="repo://apache/flink@release-2.2.0/JobDetailsHandler.java",
                    source_kind="code",
                    module="flink-runtime",
                    api_surface="rest",
                    class_name="JobDetailsHandler",
                    text_contains=("handleRequest",),
                ),
            ),
            expected_source_kinds=("code",),
            required_modules=("flink-runtime",),
            required_api_surfaces=("rest",),
            must_mentions=("AbstractRestHandler",),
            hallucination_markers=("@RestController",),
        )

        prompt = k2_mcp_prompt(case)

        # None of the expected artifact class names should appear
        for artifact in case.expected_artifacts:
            if artifact.class_name:
                self.assertNotIn(
                    artifact.class_name,
                    prompt,
                    f"Answer-key class {artifact.class_name!r} leaked into MCP prompt",
                )
        # The target_class_names argument itself should not appear
        self.assertNotIn("target_class_names", prompt)

    def test_uncoached_k2_prompt_omits_explicit_tool_choreography(self) -> None:
        prompt = k2_mcp_uncoached_prompt(_case())

        self.assertIn("available retrieval tool", prompt)
        self.assertIn("Implementation anchors", prompt)
        self.assertNotIn("k2_answer_with_sources", prompt)
        self.assertNotIn("target_class_names", prompt)

    def test_grep_baseline_prompt_points_to_local_repos_and_disables_k2(self) -> None:
        prompt = grep_baseline_prompt(
            _case(),
            flink_root="/tmp/src/flink",
            kafka_root="/tmp/src/kafka",
        )

        self.assertIn("WITHOUT K2 or MCP tools", prompt)
        self.assertIn("/tmp/src/flink", prompt)
        self.assertIn("/tmp/src/kafka", prompt)
        self.assertIn("repo://apache/flink@release-2.2.0/", prompt)
        self.assertIn("https://github.com/apache/flink/blob/", prompt)
        self.assertIn("https://github.com/apache/kafka/blob/", prompt)
        self.assertIn("repo-relative paths", prompt)

    def test_evidence_rows_from_answer_citations_uses_cited_expected_artifacts_only(self) -> None:
        case = _case()
        answer = (
            "Use AbstractRestHandler and cite "
            "repo://apache/flink@release-2.2.0/Foo.java."
        )

        rows = evidence_rows_from_answer_citations(case, answer)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["source_uri"], "repo://apache/flink@release-2.2.0/Foo.java")
        self.assertEqual(rows[0]["metadata"]["class_name"], "Foo")
        self.assertEqual(rows[0]["metadata"]["path"], "Foo.java")
        self.assertEqual(rows[0]["raw_text"], "AbstractRestHandler")

    def test_evidence_rows_from_answer_citations_accepts_repo_relative_path(self) -> None:
        rows = evidence_rows_from_answer_citations(_case(), "See Foo.java for details.")

        self.assertEqual(len(rows), 1)

    def test_evidence_rows_from_answer_citations_accepts_clickable_github_url(self) -> None:
        answer = (
            "See https://github.com/apache/flink/blob/"
            "5a336892424a9458653ead89610bf60d771ab8d7/Foo.java for details."
        )

        rows = evidence_rows_from_answer_citations(_case(), answer)

        self.assertEqual(len(rows), 1)

    def test_k2_mcp_prompt_infers_surface_from_visible_query_only(self) -> None:
        case = EvalCase(
            case_id="kafka-case-id-should-not-win",
            title="Kafka title should not win",
            query="For Flink checkpointing 2.2.0, how should I inspect state recovery?",
            required_api_surfaces=("connect",),
            expected_artifacts=(
                ExpectedArtifact(
                    key="kafka-only-answer-key",
                    source_uri="repo://apache/kafka@4.2/connect/runtime/AbstractHerder.java",
                    source_kind="code",
                    module="connect",
                    api_surface="connect",
                    class_name="AbstractHerder",
                ),
            ),
        )

        prompt = k2_mcp_prompt(case)

        self.assertIn('framework: "flink"', prompt)
        self.assertIn('api_surface: "checkpointing"', prompt)
        self.assertNotIn("AbstractHerder", prompt)
        self.assertNotIn("connect", prompt)

    def test_benchmark_mcp_inputs_do_not_leak_answer_key_values(self) -> None:
        leaks = []
        for case in evaluation_cases(suite="benchmark", include_kafka=True):
            prompt = k2_mcp_prompt(case)
            query = case.query
            framework = "kafka" if "kafka" in query.lower() else "flink"
            if framework == "kafka":
                api_surface = "rest" if " rest " in f" {query.lower()} " else "connect"
            else:
                api_surface = (
                    "checkpointing"
                    if "checkpoint" in query.lower() or "savepoint" in query.lower()
                    else "rest"
                )
            role_queries = str(
                _answer_queries(framework=framework, api_surface=api_surface, query=query)
            )
            answer_key_values = {
                value
                for artifact in case.expected_artifacts
                for value in (
                    artifact.source_uri,
                    artifact.class_name,
                    _specific_path_fragment(artifact.path_contains),
                )
                if value
            }
            for value in answer_key_values:
                if value in query:
                    continue
                if value in prompt:
                    leaks.append((case.case_id, "prompt", value))
                if value in role_queries:
                    leaks.append((case.case_id, "role_queries", value))

        self.assertEqual(leaks, [])

    def test_build_answer_scorecard_scores_k2_above_empty_baseline(self) -> None:
        case = _case()
        scorecard = build_answer_scorecard(
            [case],
            baseline_answers={case.case_id: "Use Spring MVC @RestController."},
            k2_rows_by_case={case.case_id: [_row()]},
            k2_answers={
                case.case_id: (
                    "Use AbstractRestHandler and route registration. Cite "
                    "repo://apache/flink@release-2.2.0/Foo.java"
                )
            },
        )

        self.assertEqual(scorecard["best_run"], "codex_with_k2_mcp_context")
        self.assertGreater(scorecard["comparisons"][0]["score_delta_vs_baseline"], 0)


def _case() -> EvalCase:
    return EvalCase(
        case_id="case-1",
        query="How do I add a Flink REST handler?",
        expected_artifacts=(
            ExpectedArtifact(
                key="handler",
                source_uri="repo://apache/flink@release-2.2.0/Foo.java",
                source_kind="code",
                module="flink-runtime",
                api_surface="rest",
                class_name="Foo",
                text_contains=("AbstractRestHandler",),
            ),
        ),
        expected_source_kinds=("code",),
        required_modules=("flink-runtime",),
        required_api_surfaces=("rest",),
        must_mentions=("AbstractRestHandler", "route registration"),
        hallucination_markers=("@RestController",),
    )


def _row(
    *,
    source_uri: str = "repo://apache/flink@release-2.2.0/Foo.java",
    score: float = 0.9,
) -> dict:
    return {
        "source_uri": source_uri,
        "raw_text": "class Foo extends AbstractRestHandler",
        "metadata": {
            "source_kind": "code",
            "module": "flink-runtime",
            "api_surface": "rest",
            "class_name": "Foo",
            "path": "Foo.java",
        },
        "score": score,
    }


def _specific_path_fragment(value: str | None) -> str | None:
    if not value:
        return None
    if "/" in value or value.endswith(".java") or value.startswith("repo://"):
        return value
    return None


if __name__ == "__main__":
    unittest.main()
