**Recommendation**
Anchor the explanation on the Flink 2.2 checkpointing docs for resource lifecycle, then verify the runtime behavior in `CheckpointResourcesCleanupRunner`. The key question is whether cleanup is synchronous vs. asynchronous, what gets retained until completion, and when cleanup is skipped on failures/cancellation. If the exact 2.2.0 cleanup contract is unclear, treat the implementation as the source of truth and use tests to confirm edge cases.

**Implementation anchors**
- `org.apache.flink.runtime.checkpoint.CheckpointResourcesCleanupRunner`
- Its immediate call sites in checkpoint completion/failure paths in the runtime checkpoint coordinator code
- The surrounding cleanup-related code that decides:
  - whether checkpoint resources are still referenced
  - whether cleanup happens after completed checkpoints are acknowledged
  - how aborted / failed checkpoints are handled

**Tests to inspect or add**
- A direct unit test for `CheckpointResourcesCleanupRunner` if one exists in the same runtime checkpoint test package
- Neighboring checkpoint coordinator tests that cover:
  - successful checkpoint completion and resource release
  - failed or aborted checkpoint and no premature cleanup
  - repeated / concurrent cleanup invocation safety
  - externalized checkpoint retention behavior, if applicable
- If there is no direct runner test, add one focused on:
  - cleanup invoked exactly once
  - cleanup ordering relative to completion callbacks
  - failure path does not drop resources too early

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointResourcesCleanupRunner.java`
- Version-pinned Flink 2.2 checkpointing docs on the official docs site for the checkpointing/state backend lifecycle section

**Uncertainties**
- I cannot confirm the exact 2.2.0 docs URL or the exact neighboring test class names without repository access.
- I am confident about the implementation class name, but the exact package-local test anchors may differ slightly across the 2.2.0 codebase.