# Patch-Generation Benchmark

Generated: `2026-05-02T09:05:28.516763+00:00`

## Summary

| Arm | Tasks | Passed | Mean score | Mean duration s | Mean total tokens |
| --- | ---: | ---: | ---: | ---: | ---: |
| codex_repo_only | `1` | `1` | `1` | `201.849` | `2624225` |
| codex_with_k2_mcp | `1` | `1` | `1` | `201.09` | `3393421` |

## Per-Task Results

### Add optional missing-subtask reporting to Flink vertex watermark REST output (`flink-rest-job-vertex-watermarks-include-missing`)

- Arm: `codex_repo_only`
- Score: `1`
- Passed: `true`
- Duration seconds: `201.849`
- Token metrics: `{"cached_input_tokens": 2520576, "event_count": 123, "input_tokens": 2607619, "output_tokens": 16606, "tool_counts": {}, "total_tokens": 2624225}`
- Changed files: `["flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/metrics/JobVertexWatermarksHandler.java", "flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/job/metrics/IncludeMissingQueryParameter.java", "flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/job/metrics/JobVertexWatermarksHeaders.java", "flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/job/metrics/JobVertexWatermarksMessageParameters.java", "flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/metrics/JobVertexWatermarksHandlerTest.java"]`
- Score breakdown: `{"diff_present": 1.0, "expected_file_coverage": 1.0, "scope_score": 1.0, "verification_score": 1.0}`

### Add optional missing-subtask reporting to Flink vertex watermark REST output (`flink-rest-job-vertex-watermarks-include-missing`)

- Arm: `codex_with_k2_mcp`
- Score: `1`
- Passed: `true`
- Duration seconds: `201.09`
- Token metrics: `{"cached_input_tokens": 3263360, "event_count": 136, "input_tokens": 3376092, "output_tokens": 17329, "tool_counts": {"k2_search_code": 8, "k2_search_docs": 2, "k2_search_guides": 2, "k2_search_tests": 2}, "total_tokens": 3393421}`
- Changed files: `["flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/metrics/JobVertexWatermarksHandler.java", "flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/job/metrics/IncludeMissingQueryParameter.java", "flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/job/metrics/JobVertexWatermarksHeaders.java", "flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/job/metrics/JobVertexWatermarksMessageParameters.java", "flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/metrics/JobVertexWatermarksHandlerTest.java"]`
- Score breakdown: `{"diff_present": 1.0, "expected_file_coverage": 1.0, "scope_score": 1.0, "verification_score": 1.0}`

## Interpretation Notes

- This benchmark compares generated patches, wall-clock time, and token usage.
- Deterministic patch scores are not a substitute for human code review.
- Test results should be treated as first-order evidence when task-specific tests are run.