from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tests import _paths  # noqa: F401

from k2_java_rd_demo.patch_benchmark import (
    assess_feature_development_signal,
    classify_codex_infra_failure,
    classify_patch_failure,
    extract_changed_files,
    extract_codex_usage_metrics,
    merge_patch_scorecard_payloads,
    patch_generation_prompt,
    patch_tasks,
    render_patch_report,
    render_patch_scorecard_audit,
    score_patch_run,
    summarize_patch_scorecard,
    validate_local_java_imports,
    verify_patch_scorecard_evidence,
)


class PatchBenchmarkTests(unittest.TestCase):
    def test_patch_tasks_include_flink_and_kafka_feature_tasks(self) -> None:
        tasks = patch_tasks(include_kafka=True)

        self.assertGreaterEqual(len(tasks), 10)
        self.assertEqual(len({task.task_id for task in tasks}), len(tasks))
        self.assertTrue(any(task.framework == "flink" for task in tasks))
        self.assertTrue(any(task.framework == "kafka" for task in tasks))
        self.assertGreaterEqual(sum(1 for task in tasks if task.requires_guides), 10)
        for task in tasks:
            self.assertTrue(task.expected_paths)
            self.assertTrue(task.allowed_path_prefixes)
            self.assertTrue(task.success_criteria)
            self.assertTrue(task.task_class)
            self.assertTrue(task.difficulty)
            self.assertTrue(task.verification_commands)

    def test_patch_generation_prompt_distinguishes_repo_only_and_k2_arms(self) -> None:
        task = patch_tasks(include_kafka=False)[0]

        repo_only = patch_generation_prompt(task, arm_name="codex_repo_only")
        repo_plus_docs = patch_generation_prompt(task, arm_name="codex_repo_plus_docs")
        repo_plus_guides = patch_generation_prompt(
            task,
            arm_name="codex_repo_plus_guides_dump",
        )
        with_k2 = patch_generation_prompt(task, arm_name="codex_with_k2_mcp")
        with_k2_no_guides = patch_generation_prompt(
            task,
            arm_name="codex_with_k2_mcp_no_guides",
        )

        self.assertIn("Do not use K2 or MCP tools", repo_only)
        self.assertIn("local repository inspection", repo_only)
        self.assertIn("local documentation directories", repo_plus_docs)
        self.assertIn("Version-pinned docs URLs", repo_plus_docs)
        self.assertIn("Confluence-style guide dump", repo_plus_guides)
        self.assertIn(".k2-demo-confluence-dump", repo_plus_guides)
        self.assertIn("Guide compliance line", repo_plus_guides)
        self.assertNotIn("CF-FLINK-REST-001", repo_plus_guides)
        self.assertNotIn(
            "generated://guides/flink/confluence-rest-handler-guardrails.md",
            repo_plus_guides,
        )
        self.assertIn("K2 MCP retrieval tool", with_k2)
        self.assertIn("exactly one `k2_answer_with_sources` call", with_k2)
        self.assertIn("must use", with_k2)
        self.assertIn("guide retrieval", with_k2_no_guides)
        self.assertIn(task.prompt, with_k2)
        self.assertIn("Final response requirements", with_k2)
        for expected_path in task.expected_paths:
            self.assertNotIn(expected_path, with_k2)
        self.assertIn("Allowed edit neighborhoods", with_k2)

    def test_extract_changed_files_from_git_diff(self) -> None:
        diff = """diff --git a/foo/A.java b/foo/A.java
index 111..222 100644
--- a/foo/A.java
+++ b/foo/A.java
diff --git a/bar/BTest.java b/bar/BTest.java
index 111..222 100644
--- a/bar/BTest.java
+++ b/bar/BTest.java
diff --git a/new/C.java b/new/C.java
new file mode 100644
index 0000000..3333333
--- /dev/null
+++ b/new/C.java
"""

        self.assertEqual(
            extract_changed_files(diff),
            ["foo/A.java", "bar/BTest.java", "new/C.java"],
        )

    def test_score_patch_run_covers_diff_scope_tests_time_and_tokens(self) -> None:
        task = patch_tasks(include_kafka=False)[0]
        diff = "\n".join(
            f"diff --git a/{path} b/{path}\nindex 111..222 100644"
            for path in task.expected_paths
        )

        score = score_patch_run(
            task,
            diff_text=diff,
            verification_results=[{"name": "test", "passed": True}],
            duration_s=12.3456,
            token_metrics={"total_tokens": 1234},
        )

        self.assertEqual(score["score"], 1.0)
        self.assertTrue(score["passed"])
        self.assertEqual(score["duration_s"], 12.346)
        self.assertEqual(score["token_metrics"]["total_tokens"], 1234)
        self.assertEqual(score["missing_expected_files"], [])

    def test_score_patch_run_gates_guide_guardrail_compliance_when_answer_present(self) -> None:
        task = patch_tasks(include_kafka=False)[0]
        diff = "\n".join(
            f"diff --git a/{path} b/{path}\nindex 111..222 100644"
            for path in task.expected_paths
        )

        missing = score_patch_run(
            task,
            diff_text=diff,
            answer_text="Implemented the files but found no internal guardrail.",
            verification_results=[{"name": "test", "passed": True}],
        )
        passing = score_patch_run(
            task,
            diff_text=diff,
            answer_text=(
                "Applied CF-FLINK-REST-001 from "
                "generated://guides/flink/confluence-rest-handler-guardrails.md."
            ),
            verification_results=[{"name": "test", "passed": True}],
        )

        self.assertFalse(missing["passed"])
        self.assertIn("guide_guardrail_failure", missing["failure_categories"])
        self.assertEqual(missing["score_breakdown"]["guide_guardrail_score"], 0.2)
        self.assertTrue(passing["passed"])
        self.assertEqual(passing["score_breakdown"]["guide_guardrail_score"], 1.0)
        local_dump_passing = score_patch_run(
            task,
            diff_text=diff,
            answer_text=(
                "Applied CF-FLINK-REST-001 from "
                ".k2-demo-confluence-dump/guides/flink/"
                "confluence-rest-handler-guardrails.md."
            ),
            verification_results=[{"name": "test", "passed": True}],
        )
        self.assertTrue(local_dump_passing["passed"])
        self.assertEqual(
            local_dump_passing["score_breakdown"]["guide_guardrail_score"],
            1.0,
        )

    def test_guide_compliance_can_name_forbidden_patterns_avoided(self) -> None:
        task = next(task for task in patch_tasks(include_kafka=True) if task.framework == "kafka")
        diff = "\n".join(
            f"diff --git a/{path} b/{path}\nindex 111..222 100644"
            for path in task.expected_paths
        )
        answer_text = (
            "Applied CF-KAFKA-CONNECT-007 from "
            "generated://guides/kafka/confluence-connect-rest-entity-guardrails.md. "
            "Avoided forbidden patterns: Spring Validator, Bean Validation, javax.validation."
        )

        passing = score_patch_run(
            task,
            diff_text=diff,
            answer_text=answer_text,
            verification_results=[{"name": "test", "passed": True}],
        )
        forbidden_diff = score_patch_run(
            task,
            diff_text=f"{diff}\n+import javax.validation.Valid;\n",
            answer_text=answer_text,
            verification_results=[{"name": "test", "passed": True}],
        )

        self.assertEqual(passing["score_breakdown"]["guide_guardrail_score"], 1.0)
        self.assertEqual(forbidden_diff["score_breakdown"]["guide_guardrail_score"], 0.8)

    def test_score_patch_run_penalizes_out_of_scope_files(self) -> None:
        task = patch_tasks(include_kafka=False)[0]
        diff = "diff --git a/README.md b/README.md\nindex 111..222 100644"

        score = score_patch_run(
            task,
            diff_text=diff,
            verification_results=[{"name": "test", "passed": True}],
        )

        self.assertLess(score["score"], 1.0)
        self.assertFalse(score["passed"])
        self.assertEqual(score["out_of_scope_files"], ["README.md"])

    def test_score_patch_run_requires_all_verification_checks_to_pass(self) -> None:
        task = patch_tasks(include_kafka=False)[0]
        diff = "\n".join(
            f"diff --git a/{path} b/{path}\nindex 111..222 100644"
            for path in task.expected_paths
        )

        score = score_patch_run(
            task,
            diff_text=diff,
            verification_results=[
                {"name": "git-diff-check", "passed": True},
                {"name": "local-java-import-resolution", "passed": False},
            ],
        )

        self.assertGreaterEqual(score["score"], 0.8)
        self.assertFalse(score["passed"])
        self.assertEqual(score["failure_categories"], ["static_import_failure"])

    def test_classify_patch_failure_tags_core_failure_modes(self) -> None:
        categories = classify_patch_failure(
            diff_text="",
            changed_files=["README.md"],
            verification_results=[
                {"name": "git-diff-check", "passed": False},
                {"name": "unit-test", "passed": False},
            ],
            missing_expected_files=["src/A.java"],
            out_of_scope_files=["README.md"],
        )

        self.assertEqual(
            categories,
            [
                "focused_test_failure",
                "missed_expected_files",
                "no_patch",
                "out_of_scope_changes",
                "patch_format_failure",
            ],
        )

    def test_validate_local_java_imports_flags_missing_project_imports(self) -> None:
        task = patch_tasks(include_kafka=False)[0]
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            source = (
                root
                / "flink-runtime/src/main/java/org/apache/flink/example/Changed.java"
            )
            existing = (
                root
                / "flink-runtime/src/main/java/org/apache/flink/example/Existing.java"
            )
            source.parent.mkdir(parents=True)
            source.write_text(
                "\n".join(
                    [
                        "package org.apache.flink.example;",
                        "import org.apache.flink.example.Existing;",
                        "import org.apache.flink.example.Missing;",
                        "class Changed {}",
                    ]
                ),
                encoding="utf-8",
            )
            existing.write_text(
                "package org.apache.flink.example; class Existing {}",
                encoding="utf-8",
            )

            result = validate_local_java_imports(
                task,
                root,
                ["flink-runtime/src/main/java/org/apache/flink/example/Changed.java"],
            )

        self.assertFalse(result["passed"])
        self.assertEqual(result["checked_imports"], 2)
        self.assertEqual(
            result["unresolved_imports"],
            [
                {
                    "file": "flink-runtime/src/main/java/org/apache/flink/example/Changed.java",
                    "import": "org.apache.flink.example.Missing",
                }
            ],
        )

    def test_extract_codex_usage_metrics_from_nested_json_events(self) -> None:
        events = "\n".join(
            [
                json.dumps(
                    {
                        "type": "response",
                        "usage": {
                            "input_tokens": 100,
                            "output_tokens": 25,
                            "total_tokens": 125,
                        },
                    }
                ),
                json.dumps(
                    {
                        "item": {
                            "type": "mcp_tool_call",
                            "tool": "k2_answer_with_sources",
                        },
                        "payload": {
                            "usage": {
                                "input_tokens": 110,
                                "output_tokens": 30,
                                "total_tokens": 140,
                            }
                        },
                    }
                ),
                json.dumps(
                    {
                        "item": {
                            "type": "mcp_tool_call",
                            "tool": "k2_search_code",
                            "status": "failed",
                            "result": {
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "K2 MCP tool failed: forbidden",
                                    }
                                ]
                            },
                        }
                    }
                ),
            ]
        )

        metrics = extract_codex_usage_metrics(events)

        self.assertEqual(metrics["input_tokens"], 110)
        self.assertEqual(metrics["output_tokens"], 30)
        self.assertEqual(metrics["total_tokens"], 140)
        self.assertEqual(metrics["tool_counts"]["k2_answer_with_sources"], 1)
        self.assertEqual(metrics["tool_counts"]["k2_search_code"], 1)
        self.assertEqual(metrics["mcp_tool_failures"]["k2_search_code"], 1)
        self.assertEqual(metrics["k2_tool_failure_count"], 1)

    def test_render_patch_report_includes_summary(self) -> None:
        run = {
            **score_patch_run(
                patch_tasks(include_kafka=False)[0],
                diff_text="",
                verification_results=[],
            ),
            "arm_name": "codex_repo_only",
        }
        payload = {
            "generated_at": "2026-05-02T00:00:00Z",
            "summary": summarize_patch_scorecard([run]),
            "runs": [run],
        }

        report = render_patch_report(payload)

        self.assertIn("# Patch-Generation Benchmark", report)
        self.assertIn("codex_repo_only", report)
        self.assertIn("Mean total tokens", report)
        self.assertIn("Mean guide score", report)
        self.assertIn("Decision Rule", report)

    def test_assess_feature_development_signal_requires_sample_size(self) -> None:
        task = patch_tasks(include_kafka=False)[0]
        runs = [
            {
                **score_patch_run(
                    task,
                    diff_text="\n".join(
                        f"diff --git a/{path} b/{path}\nindex 111..222 100644"
                        for path in task.expected_paths
                    ),
                    verification_results=[{"name": "test", "passed": True}],
                    token_metrics={"total_tokens": 2000},
                ),
                "arm_name": "codex_repo_plus_guides_dump",
            },
            {
                **score_patch_run(
                    task,
                    diff_text="\n".join(
                        f"diff --git a/{path} b/{path}\nindex 111..222 100644"
                        for path in task.expected_paths
                    ),
                    verification_results=[{"name": "test", "passed": True}],
                    token_metrics={"total_tokens": 1000},
                ),
                "arm_name": "codex_with_k2_mcp",
            },
        ]

        signal = assess_feature_development_signal(runs)

        self.assertEqual(signal["paired_task_count"], 1)
        self.assertEqual(signal["verdict"], "insufficient_sample")
        self.assertEqual(signal["token_ratio"], 0.5)

    def test_assess_feature_development_signal_requires_token_savings_for_win(self) -> None:
        token_saving_runs = _claim_runs(treatment_tokens=1000)
        high_token_runs = _claim_runs(treatment_tokens=2500)

        token_saving_signal = assess_feature_development_signal(token_saving_runs)
        high_token_signal = assess_feature_development_signal(high_token_runs)

        self.assertEqual(token_saving_signal["verdict"], "k2_wins")
        self.assertTrue(token_saving_signal["token_savings_ok"])
        self.assertEqual(
            high_token_signal["verdict"],
            "k2_quality_win_without_token_savings",
        )
        self.assertFalse(high_token_signal["token_savings_ok"])

    def test_assess_feature_development_signal_uses_accepted_patch_efficiency(self) -> None:
        runs = _claim_runs(baseline_pass_count=3, treatment_duration=20)

        signal = assess_feature_development_signal(runs)

        self.assertEqual(signal["verdict"], "k2_wins")
        self.assertFalse(signal["duration_ok"])
        self.assertTrue(signal["duration_per_accepted_patch_ok"])
        self.assertTrue(signal["usable_output_efficiency_ok"])

    def test_codex_transport_errors_are_infrastructure_failures(self) -> None:
        reason = classify_codex_infra_failure(
            "failed to connect to websocket wss://chatgpt.com/backend-api/codex/responses"
        )

        self.assertEqual(reason, "codex_websocket_failure")

    def test_signal_excludes_infrastructure_invalid_runs(self) -> None:
        runs = _claim_runs()
        k2_run = next(
            run
            for run in runs
            if run["arm_name"] == "codex_with_k2_mcp" and run["task_id"] == "task-0"
        )
        k2_run["run_status"] = "infra_invalid"
        k2_run["infra_failure_reason"] = "codex_websocket_failure"
        k2_run["failure_categories"] = ["codex_infra_failure"]

        signal = assess_feature_development_signal(runs)
        summary = summarize_patch_scorecard(runs)

        self.assertEqual(signal["paired_task_count"], 9)
        self.assertEqual(signal["infra_invalid_count"], 1)
        self.assertEqual(signal["verdict"], "insufficient_sample")
        k2_summary = next(
            row for row in summary["arms"] if row["arm_name"] == "codex_with_k2_mcp"
        )
        self.assertEqual(k2_summary["task_count"], 10)
        self.assertEqual(k2_summary["valid_task_count"], 9)
        self.assertEqual(k2_summary["infra_invalid_tasks"], 1)

    def test_verify_patch_scorecard_evidence_accepts_real_k2_claim_shape(self) -> None:
        payload = _claim_payload()

        audit = verify_patch_scorecard_evidence(payload, require_focused_tests=True)
        report = render_patch_scorecard_audit(audit)

        self.assertTrue(audit["claim_ready"])
        self.assertTrue(audit["checks"]["k2_sdk_probe"])
        self.assertTrue(audit["checks"]["k2_tool_calls"])
        self.assertIn("Claim ready: `true`", report)

    def test_verify_patch_scorecard_evidence_rejects_missing_k2_probe(self) -> None:
        payload = _claim_payload()
        payload["preflight"]["k2_probe"] = None

        audit = verify_patch_scorecard_evidence(payload)

        self.assertFalse(audit["claim_ready"])
        self.assertFalse(audit["checks"]["k2_sdk_probe"])
        self.assertIn("missing successful live K2 SDK preflight probe", audit["issues"])

    def test_verify_patch_scorecard_evidence_rejects_k2_tool_failures(self) -> None:
        payload = _claim_payload()
        k2_run = next(
            run
            for run in payload["runs"]
            if run["arm_name"] == "codex_with_k2_mcp"
        )
        k2_run["token_metrics"]["k2_tool_failure_count"] = 1

        audit = verify_patch_scorecard_evidence(payload)

        self.assertFalse(audit["claim_ready"])
        self.assertFalse(audit["checks"]["k2_tool_failures_absent"])

    def test_verify_patch_scorecard_evidence_rejects_infrastructure_invalid_runs(self) -> None:
        payload = _claim_payload()
        k2_run = next(
            run
            for run in payload["runs"]
            if run["arm_name"] == "codex_with_k2_mcp" and run["task_id"] == "task-0"
        )
        k2_run["run_status"] = "infra_invalid"
        k2_run["infra_failure_reason"] = "codex_websocket_failure"
        k2_run["failure_categories"] = ["codex_infra_failure"]

        audit = verify_patch_scorecard_evidence(payload)

        self.assertFalse(audit["claim_ready"])
        self.assertFalse(audit["checks"]["no_infra_invalid_runs"])
        self.assertIn("infrastructure-invalid", "\n".join(audit["issues"]))

    def test_merge_patch_scorecard_payloads_replaces_invalid_retry_rows(self) -> None:
        original = _claim_payload()
        retry = _claim_payload()
        original_k2 = next(
            run
            for run in original["runs"]
            if run["arm_name"] == "codex_with_k2_mcp" and run["task_id"] == "task-0"
        )
        original_k2["run_status"] = "infra_invalid"
        original_k2["infra_failure_reason"] = "codex_websocket_failure"
        original_k2["failure_categories"] = ["codex_infra_failure"]
        retry["runs"] = [
            run
            for run in retry["runs"]
            if run["arm_name"] == "codex_with_k2_mcp" and run["task_id"] == "task-0"
        ]
        retry["runs"][0]["token_metrics"]["total_tokens"] = 900

        merged = merge_patch_scorecard_payloads(
            [original, retry],
            prefer_later=False,
        )
        merged_k2 = next(
            run
            for run in merged["runs"]
            if run["arm_name"] == "codex_with_k2_mcp" and run["task_id"] == "task-0"
        )

        self.assertEqual(merged_k2["token_metrics"]["total_tokens"], 900)
        self.assertFalse(merged_k2.get("run_status") == "infra_invalid")

    def test_merge_patch_scorecard_payloads_preserves_later_k2_probe(self) -> None:
        baseline = _claim_payload()
        treatment = _claim_payload()
        baseline["preflight"]["k2_probe"] = None

        merged = merge_patch_scorecard_payloads([baseline, treatment])

        self.assertEqual(merged["preflight"]["k2_probe"]["result_count"], 1)

    def test_merge_patch_scorecard_payloads_preserves_earlier_k2_probe(self) -> None:
        probed = _claim_payload()
        retry_without_probe = _claim_payload()
        retry_without_probe["preflight"]["k2_probe"] = None

        merged = merge_patch_scorecard_payloads([probed, retry_without_probe])

        self.assertEqual(merged["preflight"]["k2_probe"]["result_count"], 1)


def _claim_runs(
    *,
    baseline_pass_count: int = 7,
    treatment_duration: int = 11,
    treatment_tokens: int = 1000,
) -> list[dict]:
    runs = []
    for index in range(10):
        baseline_passed = index < baseline_pass_count
        runs.append(
            {
                "task_id": f"task-{index}",
                "arm_name": "codex_repo_plus_guides_dump",
                "passed": baseline_passed,
                "duration_s": 10,
                "token_metrics": {"total_tokens": 2000},
                "score_breakdown": {"guide_guardrail_score": 1.0},
                "verification_results": [
                    {"name": "focused-test", "passed": baseline_passed}
                ],
            }
        )
        runs.append(
            {
                "task_id": f"task-{index}",
                "arm_name": "codex_with_k2_mcp",
                "passed": True,
                "duration_s": treatment_duration,
                "token_metrics": {
                    "event_count": 10,
                    "total_tokens": treatment_tokens,
                    "tool_counts": {"k2_answer_with_sources": 1},
                    "k2_tool_failure_count": 0,
                },
                "score_breakdown": {"guide_guardrail_score": 1.0},
                "failure_categories": [],
                "verification_results": [{"name": "focused-test", "passed": True}],
            }
        )
    return runs


def _claim_payload() -> dict:
    return {
        "method": "patch_generation_code_output_time_tokens",
        "preflight": {
            "k2_probe": {
                "framework": "flink",
                "result_count": 1,
                "first_source_uri": "repo://apache/flink@release-2.2.0/example.md",
                "retrieval_profile": "java_exact",
            }
        },
        "tasks": [
            {
                "task_id": f"task-{index}",
                "verification_commands": [{"name": "focused-test"}],
            }
            for index in range(10)
        ],
        "runs": _claim_runs(),
    }


if __name__ == "__main__":
    unittest.main()
