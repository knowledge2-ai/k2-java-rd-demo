**Recommendation**
Use the 2.2.x release docs for the REST checkpointing section as the user-facing contract, then trace behavior in the runtime handler implementation and its package-level tests. For this question, the key behavior split is:
- checkpoint trigger: the POST/trigger path
- checkpoint status: the GET/status path that surfaces checkpoint state/statistics

**Implementation anchors**
- `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/checkpoints/CheckpointHandlers.java`
- If the code in 2.2.0 delegates per-endpoint, also inspect the neighboring handler classes in the same package, especially the trigger/status handlers that `CheckpointHandlers` wires together.

**Tests to inspect or add**
- Existing tests in the same package under `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/checkpoints/`
- Specifically look for tests covering:
  - checkpoint trigger request/response
  - checkpoint status/summary response
  - error mapping for missing job, failed trigger, and unavailable checkpoint stats
- If coverage is thin, add a focused regression test for:
  - a trigger request hitting the handler
  - a status request returning the expected serialized checkpoint state

**Citations**
- Apache Flink 2.2.x REST API docs for job/checkpointing behavior: `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/`
- Implementation class: `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/checkpoints/CheckpointHandlers.java`
- Neighboring test package: `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/checkpoints/`

**Uncertainties**
- I am not fully certain of the exact handler class split inside `CheckpointHandlers` in 2.2.0 without inspecting the source.
- I am also not certain of the exact test class names in that package; the package path above is the reliable anchor.
- The public docs anchor is correct at the release-doc level, but the exact section anchor for checkpointing may differ slightly in the rendered HTML.