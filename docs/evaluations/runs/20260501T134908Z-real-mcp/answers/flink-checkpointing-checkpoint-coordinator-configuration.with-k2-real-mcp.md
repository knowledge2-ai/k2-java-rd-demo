**Recommendation**
Anchor the answer on the version-pinned Flink 2.2.0 checkpointing docs plus the runtime implementation of `CheckpointCoordinatorConfiguration`. The strongest nearby test anchor found is `CheckpointCoordinatorTest`; K2 did not surface a dedicated `CheckpointCoordinatorConfigurationTest` in 2.2.0.

**Implementation anchors**
- `CheckpointCoordinatorConfiguration` in `flink-runtime/src/main/java/org/apache/flink/runtime/jobgraph/tasks/CheckpointCoordinatorConfiguration.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/jobgraph/tasks/CheckpointCoordinatorConfiguration.java]
- Checkpointing docs in the 2.2.0 docs tree:
  - Advanced Configuration [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/configuration/advanced/#part-0001]
  - Checkpoints [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
  - DataStream checkpointing guide [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001]

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java]
- `flink-runtime/src/test/java/org/apache/flink/runtime/operators/coordination/OperatorCoordinatorHolderTest.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/operators/coordination/OperatorCoordinatorHolderTest.java]
- If you want direct coverage for configuration semantics, add a focused `CheckpointCoordinatorConfiguration` test class; K2 did not find one in the 2.2.0 tree.

**Citations**
- Implementation class: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/jobgraph/tasks/CheckpointCoordinatorConfiguration.java]
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/configuration/advanced/#part-0001], [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001], [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001]
- Neighboring tests: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/operators/coordination/OperatorCoordinatorHolderTest.java]

**Uncertainties**
- K2 evidence did not expose the specific option fields/methods on `CheckpointCoordinatorConfiguration`; I can only anchor the class location, not enumerate its members from this response.
- No dedicated `CheckpointCoordinatorConfigurationTest` was found in the surfaced 2.2.0 test set, so the neighboring tests are the best available anchors rather than a direct spec test.