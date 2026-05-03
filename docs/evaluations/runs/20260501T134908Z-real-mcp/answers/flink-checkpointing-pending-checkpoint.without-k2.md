**Recommendation**
- Model `PendingCheckpoint` as the in-flight checkpoint holder, not as a rich explicit state machine.
- Lifecycle summary:
  - created when the coordinator triggers a checkpoint
  - stays pending while task acknowledgements arrive
  - transitions to completed when the coordinator successfully finalizes it into a `CompletedCheckpoint`
  - transitions to terminal discard/abort on timeout, cancellation, subsumption by a newer checkpoint, decline, or other failure
- After completion or abort, it should be terminal: no more acknowledgements, and retained state must be cleaned up exactly once.

**Implementation anchors**
- Version-pinned docs: Flink 2.2 checkpointing guide
  - `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/`
- Implementation class: `org.apache.flink.runtime.checkpoint.PendingCheckpoint`
- Orchestrator neighbor to read alongside it: `org.apache.flink.runtime.checkpoint.CheckpointCoordinator`

**Tests to inspect or add**
- Inspect:
  - `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/PendingCheckpointTest.java`
  - `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java`
- Add or tighten coverage for:
  - all-acks -> finalize -> completed checkpoint
  - duplicate / late acknowledgements are ignored or rejected
  - abort paths: timeout, subsumption, cancellation, decline
  - cleanup/disposal happens once, and no acks are accepted after terminal transition

**Citations**
- Apache Flink 2.2 checkpointing docs: `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/`
- Flink runtime source: `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/PendingCheckpoint.java`
- Flink runtime test: `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/PendingCheckpointTest.java`
- Flink runtime test: `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java`

**Uncertainties**
- I’m confident in the lifecycle description, but I’m not asserting exact 2.2.0 helper-method names without the source in front of me.
- `PendingCheckpoint` is best understood as a lifecycle-backed object; if the 2.2.0 code uses slightly different internal terminology for “finalize” vs “complete,” the behavioral transitions above still hold.