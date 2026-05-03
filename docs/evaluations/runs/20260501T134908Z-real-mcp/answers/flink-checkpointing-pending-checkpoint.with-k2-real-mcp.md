**Recommendation**
`PendingCheckpoint` is the right anchor for the in-flight checkpoint state machine in Flink 2.2.0: it represents a checkpoint that has started but is still waiting for all required task acknowledgments, and it transitions to `CompletedCheckpoint` once those acknowledgments are complete [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/PendingCheckpoint.java].

For the docs side, anchor the explanation in the version-pinned 2.2.0 checkpointing docs, especially the checkpoint overview and user-facing checkpointing guide [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001], [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001].

**Implementation anchors**
- `PendingCheckpoint` is the implementation class to inspect for the state transitions, acknowledgment handling, and terminal transition to completed state [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/PendingCheckpoint.java].
- The class-level contract in the returned evidence is explicit: the checkpoint is started, awaits acknowledgments, and becomes `CompletedCheckpoint` when all required tasks have acknowledged it [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/PendingCheckpoint.java].
- The version-pinned docs to cite are:
  - Checkpoints overview [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
  - Datastream checkpointing guide [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001]

**Tests to inspect or add**
- `PendingCheckpointTest` is the neighboring regression test class and should be the first test anchor [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/PendingCheckpointTest.java].
- The evidence already shows coverage for:
  - non-null subtask state making the task stateful
  - cancellation / abort handling via `testSetCanceller`
- If you want stronger state-machine coverage, add or inspect tests that explicitly verify:
  - successful transition from pending to completed after all acknowledgments
  - duplicate acknowledgment behavior
  - abort path and cleanup of a pending checkpoint
  - mixed stateful/stateless task acknowledgment handling

**Citations**
- [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/PendingCheckpoint.java]
- [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/PendingCheckpointTest.java]
- [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
- [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001]

**Uncertainties**
- The K2 evidence returned only the class header/Javadoc and a partial test snippet, so I can confirm the high-level pending-to-completed transition but not enumerate every exact branch in `PendingCheckpoint` without deeper source extraction.
- I did not get neighboring test class names beyond `PendingCheckpointTest` from the returned evidence, so any broader test list would be speculative.