**Recommendation**
Use `CompletedCheckpointStore` as the contract, `DefaultCompletedCheckpointStore` as the main retention implementation, and `CompletedCheckpointStoreTest` plus the store-specific subclasses as the behavioral anchor. For docs, anchor on the Flink 2.2.0 checkpointing/state-backend docs that explain retained completed checkpoint metadata and checkpoint storage behavior. The evidence shows retention is implemented as a bounded history: older checkpoints are subsumed/removed when new ones are added, and on recovery only the latest persisted checkpoint is kept if multiple are present.

**Implementation anchors**
- Contract: [`CompletedCheckpointStore`](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CompletedCheckpointStore.java)
- Primary retention implementation: [`DefaultCompletedCheckpointStore`](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStore.java)
- HA-off variant with explicit max retention: [`StandaloneCompletedCheckpointStore`](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/StandaloneCompletedCheckpointStore.java)
- Related persistence/storage context: [`FileSystemCheckpointStorage`](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/storage/FileSystemCheckpointStorage.java)

**Tests to inspect or add**
- Base contract coverage: [`CompletedCheckpointStoreTest`](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CompletedCheckpointStoreTest.java)
- Default store behavior and recovery ordering: [`DefaultCompletedCheckpointStoreTest`](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStoreTest.java)
- Store-specific retention behavior: [`ZooKeeperCompletedCheckpointStoreTest`](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/ZooKeeperCompletedCheckpointStoreTest.java)
- Test helper / fake implementation if you need to extend coverage: [`TestingCompletedCheckpointStore`](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/TestingCompletedCheckpointStore.java)

**Citations**
- Version-pinned docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001)
- Version-pinned docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001)
- Implementation: [`CompletedCheckpointStore`](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CompletedCheckpointStore.java)
- Implementation: [`DefaultCompletedCheckpointStore`](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStore.java)
- Test: [`CompletedCheckpointStoreTest`](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CompletedCheckpointStoreTest.java)
- Test: [`DefaultCompletedCheckpointStoreTest`](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStoreTest.java)
- Test: [`ZooKeeperCompletedCheckpointStoreTest`](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/ZooKeeperCompletedCheckpointStoreTest.java)

**Uncertainties**
- The K2 evidence clearly surfaced the contract, main implementation, and neighboring tests, but it did not expose the full `DefaultCompletedCheckpointStore` retention method body. I can anchor the answer, but I cannot quote exact retention logic beyond what the surfaced evidence states.
- The docs returned are relevant checkpointing/state-backend anchors, but they are indirect; the evidence did not surface a doc page dedicated specifically to `CompletedCheckpointStore` retention.