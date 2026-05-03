**Recommendation**
Use the 2.2.0 public checkpointing docs to define the contract, then anchor the behavior on `CheckpointFailureManager` and its unit test. The documented rule is: `execution.checkpointing.tolerable-failed-checkpoints` counts consecutive eligible checkpoint failures, default `0`, and once the tolerated threshold is exceeded Flink fails the job; the docs also restrict which failure reasons count toward this budget and say some failures are always handled differently [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0014].

**Implementation anchors**
- Public config/docs entrypoint: `execution.checkpointing.tolerable-failed-checkpoints` in the 2.2.0 checkpointing guide [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0014].
- Internal implementation class: `CheckpointFailureManager` in `flink-runtime` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointFailureManager.java].
- Related config surface that feeds the same concept: `CheckpointConfig#getTolerableCheckpointFailureNumber` / checkpointing options, from the runtime config layer [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/streaming/api/environment/CheckpointConfig.java].

**Tests to inspect or add**
- `CheckpointFailureManagerTest`, especially the visible `testIgnoresPastCheckpoints` case, which shows the manager should not count expired/past checkpoints toward the failure budget [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointFailureManagerTest.java].
- `CheckpointCoordinatorTest`, because it exercises coordinator-level checkpoint failure flow and validates the surrounding checkpoint lifecycle [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java].
- `CheckpointCoordinatorFailureTest`, for failure-path regression coverage around checkpoint orchestration [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorFailureTest.java].
- If adding coverage, a good gap-filler is a test that proves the threshold is counted only for eligible failure reasons and that a successful checkpoint resets the consecutive-failure tracking.

**Citations**
- Docs: `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0014`
- Docs overview: `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001`
- Implementation: `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointFailureManager.java`
- Config surface: `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/streaming/api/environment/CheckpointConfig.java`
- Unit test: `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointFailureManagerTest.java`
- Neighbor tests: `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java`, `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorFailureTest.java`

**Uncertainties**
- The K2 code snippet for `CheckpointFailureManager.java` was truncated, so I can anchor the class and the public behavior, but I cannot safely quote line-level implementation details from the body without more source text.
- I did not fetch the full `CheckpointFailureManagerTest` file, so I can name the visible case (`testIgnoresPastCheckpoints`) but not all test methods with certainty.