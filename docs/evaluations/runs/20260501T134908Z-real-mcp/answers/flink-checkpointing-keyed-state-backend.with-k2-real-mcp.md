**Recommendation**
Use the Flink 2.2.0 docs plus the `KeyedStateBackend` interface as the primary anchors, and treat the neighboring state/checkpoint tests as supporting context. K2 did not surface a dedicated `KeyedStateBackendTest`, so do not claim one exists without further repo inspection.

**Implementation anchors**
- Version-pinned docs:
  - Checkpoints overview: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001)
  - State backends overview: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001)
  - Streaming fault-tolerance checkpointing: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001)
- Implementation class/interface:
  - `KeyedStateBackend` in `flink-runtime/src/main/java/org/apache/flink/runtime/state/KeyedStateBackend.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/KeyedStateBackend.java]
  - Adjacent checkpointing contract: `CheckpointableKeyedStateBackend` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointableKeyedStateBackend.java]
- What the evidence supports:
  - Checkpointing persists managed state for recovery semantics, and keyed backends participate in that checkpointing contract via the keyed-state backend interfaces [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001), [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/StateBackend.java]
  - `CheckpointableKeyedStateBackend` extends `KeyedStateBackend` and adds snapshot/savepoint responsibilities [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointableKeyedStateBackend.java]

**Tests to inspect or add**
- Inspect existing neighboring tests that exercise checkpoint/state machinery:
  - `StateBackendUtils` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/streaming/util/StateBackendUtils.java]
  - `TestingRetrievableStateStorageHelper` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/TestingRetrievableStateStorageHelper.java]
  - `MergedChannelStateHandleTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/MergedChannelStateHandleTest.java]
  - `TaskExecutorChannelStateExecutorFactoryManagerTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/TaskExecutorChannelStateExecutorFactoryManagerTest.java]
  - `TaskExecutorFileMergingManagerTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/TaskExecutorFileMergingManagerTest.java]
- Add a focused `KeyedStateBackend` regression test only if you need to pin down a specific checkpointing contract; K2 did not return an existing direct test class for it.

**Citations**
- Docs:
  - [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001)
  - [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001)
  - [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001)
- Code:
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/KeyedStateBackend.java]
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointableKeyedStateBackend.java]
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/StateBackend.java]
- Tests:
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/streaming/util/StateBackendUtils.java]
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/TestingRetrievableStateStorageHelper.java]
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/MergedChannelStateHandleTest.java]
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/TaskExecutorChannelStateExecutorFactoryManagerTest.java]
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/TaskExecutorFileMergingManagerTest.java]

**Uncertainties**
- K2’s `KeyedStateBackend` snippet was partial, so I am not claiming method-level responsibilities beyond the documented checkpointing contract.
- No direct `KeyedStateBackendTest` surfaced in the returned evidence; that absence is a K2 search result, not a proof the test does not exist.