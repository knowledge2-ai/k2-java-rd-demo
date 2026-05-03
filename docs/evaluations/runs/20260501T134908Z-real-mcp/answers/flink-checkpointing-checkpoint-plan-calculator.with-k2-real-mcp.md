**Recommendation**
Use the version-pinned checkpointing docs as the conceptual anchor, then read the `CheckpointPlanCalculator` interface plus its concrete default implementation, and finally validate behavior against the nearest checkpoint-plan test coverage.

**Implementation anchors**
- Docs: checkpointing overview and process docs for Flink 2.2.0:
  - `Checkpointing` guide `[https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001]`
  - `Checkpoints` ops doc `[https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]`
  - `Checkpointing under backpressure` `[https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpointing_under_backpressure/#part-0001]`
- Implementation seam: `CheckpointPlanCalculator` in `flink-runtime` `[repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointPlanCalculator.java]`
- Concrete implementation to inspect for the actual calculation flow: `DefaultCheckpointPlanCalculator` `[repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointPlanCalculator.java]`

**Tests to inspect or add**
- Primary nearby test anchor: `DefaultCheckpointPlanCalculatorTest` `[repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointPlanCalculatorTest.java]`
- Adjacent checkpointing runtime tests that may capture coordinator/task-state interactions:
  - `CheckpointCoordinatorMasterHooksTest` `[repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorMasterHooksTest.java]`
  - `TestingRetrievableStateStorageHelper` `[repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/TestingRetrievableStateStorageHelper.java]`
  - `TestTaskStateManager` `[repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/TestTaskStateManager.java]`
  - `TestSubtaskCheckpointCoordinator` `[repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/streaming/runtime/tasks/TestSubtaskCheckpointCoordinator.java]`
- If you need a missing regression test, add one beside `DefaultCheckpointPlanCalculatorTest` rather than creating a standalone `CheckpointPlanCalculatorTest`; K2 did not surface a dedicated test file with that exact name.

**Citations**
- `CheckpointPlanCalculator` implementation `[repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointPlanCalculator.java]`
- `DefaultCheckpointPlanCalculator` implementation `[repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointPlanCalculator.java]`
- `DefaultCheckpointPlanCalculatorTest` `[repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointPlanCalculatorTest.java]`
- Flink 2.2.0 checkpointing docs `[https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001]`, `[https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]`, `[https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpointing_under_backpressure/#part-0001]`

**Uncertainties**
- The K2 evidence did not expose the full body of `CheckpointPlanCalculator` or `DefaultCheckpointPlanCalculator`, so I am not claiming exact algorithmic steps beyond the anchored class relationship.
- K2 did not return a dedicated `CheckpointPlanCalculatorTest`; the nearest concrete coverage is `DefaultCheckpointPlanCalculatorTest`.