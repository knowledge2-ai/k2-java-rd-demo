**Recommendation**
Use the version-pinned checkpointing docs plus `CheckpointStatsTracker` implementation as the primary anchor. The 2.2.0 docs show the user-facing checkpoint model, while the runtime code shows that checkpoint stats are tracked as live-updated pending stats that are finalized into completed or failed stats and then reported outward. For traces, Flink also treats the tracker as the span/event source for checkpoint lifecycle metadata [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001] [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/traces/#part-0003] [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointStatsTracker.java].

**Implementation anchors**
- Version-pinned docs:
  - Checkpoints overview and recovery semantics [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
  - Checkpointing guide under DataStream fault tolerance [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001]
  - Traces doc section that maps checkpoint spans/events to `CheckpointStatsTracker` and fields like start/end timestamps, checkpoint id, size, status, and type [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/traces/#part-0003]
- Implementation class:
  - `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointStatsTracker.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointStatsTracker.java]
  - Supporting lifecycle object: `PendingCheckpointStats`, which is live-updated, receives subtask acknowledgements, and converts into completed/failed stats [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/PendingCheckpointStats.java]
  - Related concrete tracker implementation: `DefaultCheckpointStatsTracker`, which emits checkpoint events/spans from the collected stats [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointStatsTracker.java]

**Tests to inspect or add**
- Inspect first:
  - `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointStatsTrackerTest.java` for completed/failed checkpoint listener behavior [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointStatsTrackerTest.java]
  - `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java` for coordinator/checkpoint lifecycle interactions [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java]
  - `flink-runtime/src/test/java/org/apache/flink/runtime/state/TestTaskStateManager.java` for state-manager-side checkpoint plumbing [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/TestTaskStateManager.java]
- Add if coverage is thin:
  - A focused `CheckpointStatsTracker` regression test for pending-to-completed and pending-to-failed transitions if no direct coverage exists.
  - A trace/metrics assertion test if the intent is to lock down emitted span/event attributes.

**Citations**
- Checkpoints overview: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
- DataStream checkpointing guide: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001]
- Traces mapping for `CheckpointStatsTracker`: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/traces/#part-0003]
- Implementation: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointStatsTracker.java]
- Supporting runtime stats lifecycle: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/PendingCheckpointStats.java]
- Concrete tracker implementation: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointStatsTracker.java]
- Neighboring tests: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointStatsTrackerTest.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/TestTaskStateManager.java]

**Uncertainties**
- K2 did not surface a direct `CheckpointStatsTrackerTest`, so I cannot claim there is dedicated unit coverage for that class.
- The evidence is strong for the lifecycle and emitted trace fields, but it does not expose every method on `CheckpointStatsTracker`; if you need exact method-by-method behavior, that would require a deeper code read.