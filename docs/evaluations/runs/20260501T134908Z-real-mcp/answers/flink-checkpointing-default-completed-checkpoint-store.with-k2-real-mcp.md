**Recommendation**
Use `DefaultCompletedCheckpointStore` as the implementation source of truth for retention semantics, and pair it with the Flink 2.2.0 checkpointing docs that describe the user-facing retained-checkpoints setting. The code shows the store keeps a bounded in-memory deque of completed checkpoints and, on recovery, prefers the latest checkpoint from the `StateHandleStore`, discarding older recovered entries [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStore.java] [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0013].

**Implementation anchors**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStore.java` is the key class. It explicitly defines `maxNumberOfCheckpointsToRetain` as “the maximum number of checkpoints to retain (at least 1)” and keeps a local `ArrayDeque<CompletedCheckpoint>` in parallel with the persisted state handle store [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStore.java].
- The class-level comment says that during recovery the latest checkpoint is read from `StateHandleStore`; if more than one is present, only the latest is used and older ones are discarded [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStore.java].
- The version-pinned docs that anchor the public configuration story are:
  - `docs/dev/datastream/fault-tolerance/checkpointing/index.html`, which lists `execution.checkpointing.max-retained-checkpoints` as “The maximum number of completed checkpoints to retain” [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0013].
  - `docs/ops/state/checkpoints/index.html`, which explains retained checkpoints are not kept by default unless configured and are cleaned up on cancellation unless externalized retention is enabled [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0003].

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStoreTest.java` for the direct retention and recovery contract [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStoreTest.java].
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CompletedCheckpointStoreTest.java` as the shared contract test base for store behavior [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CompletedCheckpointStoreTest.java].
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/StandaloneCompletedCheckpointStoreTest.java` for adjacent store semantics and retention-policy coverage [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/StandaloneCompletedCheckpointStoreTest.java].
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStoreUtilsTest.java` for recovery-ordering / retrieval helpers that feed the store’s restore path [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStoreUtilsTest.java].

**Citations**
- `DefaultCompletedCheckpointStore` implementation: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStore.java]
- Checkpointing docs, retained-checkpoints setting: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0013]
- Checkpoints docs, retained/externalized behavior: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0003]
- Direct test class: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStoreTest.java]
- Shared contract test base: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CompletedCheckpointStoreTest.java]
- Neighboring standalone store test: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/StandaloneCompletedCheckpointStoreTest.java]
- Utility test: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStoreUtilsTest.java]

**Uncertainties**
- K2 evidence confirms bounded retention and latest-only recovery, but it does not expose the exact numeric default for the global configuration value behind `execution.checkpointing.max-retained-checkpoints`.
- The docs and tests are enough to anchor behavior, but the exact default value should be verified from the config constant if you need to state it precisely.