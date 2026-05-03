**Recommendation**
Checkpoint retention in Flink 2.2.0 is about what happens to checkpoint artifacts after job termination, especially externalized checkpoints. The public docs anchor the behavior as a retain-vs-delete-on-cancellation choice for externalized checkpoints, while the implementation class is the authoritative source for the exact enum/constant names and semantics. Based on the K2 evidence, do not infer extra policy variants beyond what the source surfaces.

**Implementation anchors**
- Version-pinned docs:
  - Checkpoints guide, externalized retention section: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0004](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0004)
  - Checkpointing guide: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001)
  - State backends overview: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001)
- Implementation class:
  - `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointRetentionPolicy.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointRetentionPolicy.java]

**Tests to inspect or add**
- Existing neighboring tests that likely cover policy wiring and downstream effects:
  - `PendingCheckpointTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/PendingCheckpointTest.java]
  - `CheckpointPropertiesTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointPropertiesTest.java]
  - `CompletedCheckpointStoreTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CompletedCheckpointStoreTest.java]
  - `CheckpointFailureManagerTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointFailureManagerTest.java]
- Add or tighten a focused unit test only if the enum body or retention semantics are ambiguous in source, especially around cancellation/termination cleanup behavior.

**Citations**
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0004](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0004)
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001)
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001)
- Code: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointRetentionPolicy.java]
- Tests: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/PendingCheckpointTest.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointPropertiesTest.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CompletedCheckpointStoreTest.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointFailureManagerTest.java]

**Uncertainties**
- The K2 result did not surface the full body of `CheckpointRetentionPolicy.java`, so I cannot state the exact enum constants or all branches with certainty from this lookup alone.
- The docs snippet clearly shows retain-vs-delete behavior for externalized checkpoints, but the precise mapping from `CheckpointRetentionPolicy` values to those behaviors should be confirmed directly in the class source before making a definitive claim.