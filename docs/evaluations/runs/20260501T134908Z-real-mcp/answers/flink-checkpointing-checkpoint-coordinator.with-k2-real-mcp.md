**Recommendation**
- Anchor the answer on the Flink 2.2.0 checkpointing docs and the runtime implementation of `CheckpointCoordinator` in `flink-runtime`. The version-pinned docs are the checkpoints overview and the DataStream checkpointing guide: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/) and [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/).
- For implementation claims, use the 2.2.0 source for `CheckpointCoordinator` itself: `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinator.java`.
- The surrounding runtime flow shown in K2 indicates the coordinator participates in scheduling and restore paths, including `startCheckpointScheduler()` and `getCheckpointCoordinator()` access patterns in adjacent classes: `CheckpointCoordinatorDeActivator`, `CheckpointSchedulingProvider`, and `SchedulerBase`.

**Implementation anchors**
- Main class: `CheckpointCoordinator` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinator.java]
- Scheduler activation path: `CheckpointCoordinatorDeActivator` starts the scheduler when the job enters `RUNNING` and all task outputs are non-blocking [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorDeActivator.java]
- Scheduler facade: `CheckpointSchedulingProvider` delegates `startCheckpointScheduler()` to the execution graph’s coordinator [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/scheduler/adaptive/CheckpointSchedulingProvider.java]
- Restore interaction: `SchedulerBase` reads `executionGraph.getCheckpointCoordinator()` during state restore [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/scheduler/SchedulerBase.java]
- From the evidence, the safest concrete statement is that the coordinator is responsible for checkpoint scheduling/trigger coordination and participates in restore-state handling; I would not claim more without reading the class body directly.

**Tests to inspect or add**
- Inspect `CheckpointCoordinatorTest` first: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java]
- Existing neighbor coverage already exercises trigger/ack flow; K2 surfaced a test that calls `coordinator.triggerCheckpoint(true)` and then waits until a pending checkpoint has a storage location before acknowledging it.
- If you need stronger coverage around trigger orchestration, add or tighten tests for:
  - checkpoint trigger enqueues a pending checkpoint before acknowledgements arrive
  - scheduler start only happens when the job is `RUNNING` and outputs are non-blocking
  - restore path behavior when `executionGraph.getCheckpointCoordinator()` is null vs present

**Citations**
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/)
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/)
- Implementation: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinator.java]
- Neighboring runtime flow: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorDeActivator.java]
- Neighboring runtime flow: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/scheduler/adaptive/CheckpointSchedulingProvider.java]
- Neighboring runtime flow: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/scheduler/SchedulerBase.java]
- Test anchor: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java]

**Uncertainties**
- The K2 evidence clearly identifies the right docs, class, and neighboring tests, but it does not expose the full `CheckpointCoordinator` body in this response. So I can anchor the answer, but I should not speculate about exact internal methods beyond what the evidence shows.