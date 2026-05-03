**Changes**
- Added a local watermark-specific message-parameters subclass to register the new optional query flag: [`JobVertexWatermarksMessageParameters.java`](/tmp/k2-patch-generation-e2e-compare-v2/20260502T085752Z-patch-generation/worktrees/flink-rest-job-vertex-watermarks-include-missing/codex_repo_only/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/job/metrics/JobVertexWatermarksMessageParameters.java).
- Added the new optional boolean query parameter `includeMissing`, defaulting to `false`, in [`IncludeMissingQueryParameter.java`](/tmp/k2-patch-generation-e2e-compare-v2/20260502T085752Z-patch-generation/worktrees/flink-rest-job-vertex-watermarks-include-missing/codex_repo_only/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/job/metrics/IncludeMissingQueryParameter.java).
- Updated [`JobVertexWatermarksHandler.java`](/tmp/k2-patch-generation-e2e-compare-v2/20260502T085752Z-patch-generation/worktrees/flink-rest-job-vertex-watermarks-include-missing/codex_repo_only/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/metrics/JobVertexWatermarksHandler.java) to:
  - read `includeMissing` from the request,
  - preserve the existing behavior when it is absent or `false`,
  - emit one `Metric` per subtask even when the watermark metric is missing, using the existing metric id and a `null` value, when `includeMissing=true`.
- Updated [`JobVertexWatermarksHeaders.java`](/tmp/k2-patch-generation-e2e-compare-v2/20260502T085752Z-patch-generation/worktrees/flink-rest-job-vertex-watermarks-include-missing/codex_repo_only/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/job/metrics/JobVertexWatermarksHeaders.java) so the endpoint advertises the new behavior.
- Expanded [`JobVertexWatermarksHandlerTest.java`](/tmp/k2-patch-generation-e2e-compare-v2/20260502T085752Z-patch-generation/worktrees/flink-rest-job-vertex-watermarks-include-missing/codex_repo_only/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/metrics/JobVertexWatermarksHandlerTest.java) to cover:
  - default behavior,
  - partial availability,
  - explicit `includeMissing=true`,
  - explicit `includeMissing=false`.

**Tests**
- `mvn -pl flink-runtime -P!java21 -Dtest=JobVertexWatermarksHandlerTest -Dcheckstyle.skip=true -Denforcer.skip=true test` نتي passed.

**Remaining uncertainty**
- Validation was limited to the focused handler test in this JDK 25 environment. I did not run broader `flink-runtime` or end-to-end REST tests, so wider integration behavior remains unverified.