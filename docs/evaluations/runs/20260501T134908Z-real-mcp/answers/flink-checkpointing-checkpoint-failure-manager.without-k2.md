**Recommendation**
Treat tolerated checkpoint failures as a bounded retry budget, not as “ignore forever.” In Flink 2.2.0, `CheckpointFailureManager` should accumulate checkpoint failures until the configured tolerance is exceeded; once it is, the job should be failed. A successful checkpoint should reset the tolerated-failure streak/counter.

**Implementation anchors**
- Implementation class: `org.apache.flink.runtime.checkpoint.CheckpointFailureManager`
- Config surface to verify in docs/code: `execution.checkpointing.tolerable-failed-checkpoints` and related checkpoint-failure handling paths
- Version-pinned docs to anchor behavior: the Flink 2.2.0 checkpointing/fault-tolerance docs page for checkpoint configuration and failure tolerance
- Neighboring tests to inspect: `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointFailureManagerTest.java`
- Also inspect adjacent tests in `org.apache.flink.runtime.checkpoint` that cover checkpoint abort/failure classification and failure counter reset behavior

**Tests to inspect or add**
- A test that verifies failures are tolerated up to the configured limit
- A test that verifies the next failure after the limit triggers job failure
- A test that verifies a successful checkpoint resets the tolerated-failure counter
- A test that verifies non-tolerable failure types bypass the tolerance budget
- If missing, add one regression test around “failure count resets after success, then tolerates again”

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointFailureManager.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointFailureManagerTest.java`
- `docs/content/docs/dev/datastream/fault-tolerance/checkpointing.md`  
  - I’m not fully certain this is the exact 2.2.0 docs path without repository access, but this is the likely public docs anchor.

**Uncertainties**
- I could not verify the exact 2.2.0 docs file path or line-level wording without repo/web access.
- I’m confident about the implementation class and the neighboring test class name, but the precise set of adjacent tests may vary slightly by branch/tag.
- If you need a line-accurate answer, the safest next step is to pin it against the 2.2.0 tag in `CheckpointFailureManager` and `CheckpointFailureManagerTest`.