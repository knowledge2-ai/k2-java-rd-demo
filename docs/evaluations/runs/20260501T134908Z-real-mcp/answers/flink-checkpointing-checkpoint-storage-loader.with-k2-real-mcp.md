**Recommendation**
Anchor the explanation on the 2.2.0 checkpointing docs and the `CheckpointStorageLoader` implementation, then validate behavior against `CheckpointStorageLoaderTest`. The safest documented framing is: checkpoint storage is configured via checkpointing/state-backend configuration, and the loader class is the runtime utility that resolves the configured storage from those configs [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001] [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001] [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageLoader.java].

**Implementation anchors**
- Docs:
  - `Checkpoints` docs page for the storage concept and user-facing configuration context [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
  - `State Backends` docs page for how checkpointed state is persisted [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001]
  - `Checkpointing` guide for config-level semantics [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001]
- Implementation class:
  - `CheckpointStorageLoader` in `flink-runtime`, which K2 identifies as the utility class that “load[s] checkpoint storage from configurations” [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageLoader.java]
- Nearby implementation context:
  - `FileSystemCheckpointStorage` as the storage backend class the loader can resolve to, for filesystem-backed checkpoint persistence [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/storage/FileSystemCheckpointStorage.java]
  - `Checkpoints` as a neighboring runtime entry point that also loads configured state backend/storage during checkpoint-related setup [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/Checkpoints.java]

**Tests to inspect or add**
- Inspect `CheckpointStorageLoaderTest` first; it is the direct regression test for this loader and is the strongest anchor for config-resolution behavior [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/CheckpointStorageLoaderTest.java]
- Also inspect `CheckpointCoordinatorMasterHooksTest` only as adjacent checkpointing coverage, not as the primary loader test [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorMasterHooksTest.java]
- If adding coverage, add tests around:
  - explicit storage selection from config
  - fallback/legacy precedence handling
  - error behavior for malformed or unloadable storage config

**Citations**
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001]
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001]
- Implementation: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageLoader.java]
- Related runtime class: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/storage/FileSystemCheckpointStorage.java]
- Related runtime class: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/Checkpoints.java]
- Direct test: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/CheckpointStorageLoaderTest.java]
- Neighboring test: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorMasterHooksTest.java]

**Uncertainties**
K2 returned the loader source and test file anchors, but the method body for `CheckpointStorageLoader` was truncated in the evidence, so I cannot safely claim the exact precedence/order of all configuration branches from this response alone. If you need the precise loading algorithm, the next step is to inspect that source file directly in K2.