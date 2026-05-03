**Recommendation**
Anchor the answer on the release-2.2.0 docs plus the `CheckpointMetrics` implementation and its direct checkpointing call sites. The reporting path in K2 passes `CheckpointMetrics` through task/runtime acknowledgement APIs rather than exposing a separate reporting DTO, so the safest field list is the one defined on the class itself [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001], [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001], [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointMetrics.java].

**Implementation anchors**
- `CheckpointMetrics` in `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointMetrics.java` is the implementation class to cite [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointMetrics.java].
- Reporting/acknowledgement call sites that carry the metrics object:
  - `TaskStateManager.reportTaskStateSnapshots(...)` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/TaskStateManager.java]
  - `Environment.acknowledgeCheckpoint(...)` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/execution/Environment.java]
  - `CheckpointResponder.acknowledgeCheckpoint(...)` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/taskmanager/CheckpointResponder.java]
- The metric fields surfaced in the `CheckpointMetrics` implementation snippet are:
  - `bytesProcessedDuringAlignment`
  - `bytesPersistedDuringAlignment`
  - `alignmentDurationNanos`
  - `syncDurationMillis`
  - `asyncDurationMillis`
  - `checkpointStartDelayNanos`
  - `unalignedCheckpoint`
  - `bytesPersistedOfThisCheckpoint`
  - `totalBytesPersisted`
  [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointMetrics.java]

**Tests to inspect or add**
- Primary neighbor: `CheckpointMetricsTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointMetricsTest.java]
- Nearby checkpointing tests that exercise the same reporting/ack path:
  - `TestTaskStateManager` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/TestTaskStateManager.java]
  - `CheckpointCoordinatorTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java]
  - `NoOpCheckpointResponder` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/taskmanager/NoOpCheckpointResponder.java]
- If you need a regression guard, add a test that asserts the full metric set is preserved across the reporting/acknowledgement path, not just construction/serialization [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointMetricsTest.java].

**Citations**
- Docs:
  - [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
  - [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001]
  - [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpointing_under_backpressure/#part-0001]
- Code:
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointMetrics.java]
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/TaskStateManager.java]
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/execution/Environment.java]
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/taskmanager/CheckpointResponder.java]
- Tests:
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointMetricsTest.java]
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/TestTaskStateManager.java]
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java]
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/taskmanager/NoOpCheckpointResponder.java]

**Uncertainties**
- K2 returned the class-level field names, but not a full getter-to-caller map, so I cannot prove from this evidence alone which exact reporting call site reads each field.
- The neighboring test bodies were not fully surfaced, so I can name the right tests to inspect, but not claim their exact assertions without more source.