**Recommendation**
Use the 2.2.0 checkpointing docs plus `CheckpointStorageCoordinatorView` itself as the anchor, and treat the coordinator-facing contract as the piece of checkpoint storage that the JobManager/coordinator uses to create and manage checkpoint locations, while the worker side stays separate. The K2 evidence is enough to confirm the surrounding storage model, but it does not expose the full class body, so any finer-grained behavioral claim should be treated as an inference, not a verified fact.

**Implementation anchors**
- Version-pinned docs:
  - Checkpoints overview and storage model: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001)
  - State backend / checkpoint storage context: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001)
  - Developer-facing checkpointing/storage selection: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0016](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0016)
- Implementation class:
  - `CheckpointStorageCoordinatorView`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageCoordinatorView.java](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageCoordinatorView.java)
- Closely related runtime classes surfaced by K2:
  - `CheckpointStorageWorkerView`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageWorkerView.java](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageWorkerView.java)
  - `CheckpointStorageAccess`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageAccess.java](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageAccess.java)
  - `FileSystemCheckpointStorage`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/storage/FileSystemCheckpointStorage.java](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/storage/FileSystemCheckpointStorage.java)

**Tests to inspect or add**
- Inspect existing nearby tests:
  - `MemoryCheckpointStorageAccessTest`: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/memory/MemoryCheckpointStorageAccessTest.java](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/memory/MemoryCheckpointStorageAccessTest.java)
  - `CheckpointCoordinatorTest`: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java)
- Add, if missing, a focused regression test for:
  - coordinator-created checkpoint storage location creation
  - persistence/HA capability propagation to the coordinator view
  - failure behavior when coordinator storage is unavailable or non-HA
- K2 did not surface a dedicated `CheckpointStorageCoordinatorViewTest`, so that looks like a gap worth filling if this contract matters operationally.

**Citations**
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001)
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001)
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0016](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0016)
- Code: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageCoordinatorView.java](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageCoordinatorView.java)
- Code: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageWorkerView.java](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageWorkerView.java)
- Test: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/memory/MemoryCheckpointStorageAccessTest.java](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/memory/MemoryCheckpointStorageAccessTest.java)
- Test: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java)

**Uncertainties**
- K2 returned the class path for `CheckpointStorageCoordinatorView`, but not the full source body, so the exact method-level contract is not fully verified here.
- No dedicated `CheckpointStorageCoordinatorViewTest` was surfaced in the evidence, so the recommendation to add one is an inference based on the missing coverage, not a confirmed repository fact.
- The precise relationship between coordinator and worker views should be confirmed directly in the source before making a stronger API guarantee claim.