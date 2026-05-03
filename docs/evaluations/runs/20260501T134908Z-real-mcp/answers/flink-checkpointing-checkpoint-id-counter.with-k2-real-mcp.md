**Recommendation**
Use the version-pinned checkpointing docs for framing, but anchor the actual behavior on `CheckpointIDCounter` and its concrete implementations. The allocation behavior in 2.2.0 is implemented as a monotonically increasing counter: the standalone implementation starts from `INITIAL_CHECKPOINT_ID`, `getAndIncrement()` returns the current value and advances it, `get()` reads the current value, and `setCount()` overwrites it [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointIDCounter.java] [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/StandaloneCheckpointIDCounter.java].

**Implementation anchors**
- Version-pinned docs:
  - Checkpoints overview: `flink-docs-release-2.2/docs/ops/state/checkpoints/index.html` [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
  - DataStream checkpointing guide: `flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/index.html` [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001]
- Implementation class:
  - `CheckpointIDCounter` interface [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointIDCounter.java]
  - Concrete allocator behavior in `StandaloneCheckpointIDCounter` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/StandaloneCheckpointIDCounter.java]
- Related implementation to inspect for HA behavior:
  - `ZooKeeperCheckpointIDCounter` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/ZooKeeperCheckpointIDCounter.java]

**Tests to inspect or add**
- Inspect existing test support:
  - `TestingCheckpointIDCounter` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/TestingCheckpointIDCounter.java]
  - `CheckpointCoordinatorTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java]
  - `CheckpointCoordinatorMasterHooksTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorMasterHooksTest.java]
- Add if missing:
  - A focused `CheckpointIDCounter` unit test for `getAndIncrement()`, `get()`, and `setCount()` semantics.
  - A coordinator-level test proving checkpoint IDs are allocated monotonically and registered before hooks run.
- K2 did not surface a dedicated `CheckpointIDCounterTest` in 2.2.0, so that gap should be called out if you are trying to anchor behavior with a single direct regression test.

**Citations**
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001]
- Interface: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointIDCounter.java]
- Standalone implementation: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/StandaloneCheckpointIDCounter.java]
- HA implementation: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/ZooKeeperCheckpointIDCounter.java]
- Test support: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/TestingCheckpointIDCounter.java]
- Coordinator tests: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java] [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorMasterHooksTest.java]

**Uncertainties**
- K2 evidence did not include the full body of `CheckpointIDCounter` or `ZooKeeperCheckpointIDCounter`, so I am only making the allocation-semantics claim from the surfaced `StandaloneCheckpointIDCounter` snippet and the interface context.
- No dedicated `CheckpointIDCounterTest` was returned by K2, so the exact existing regression coverage may be broader and embedded in coordinator tests rather than a direct unit test.