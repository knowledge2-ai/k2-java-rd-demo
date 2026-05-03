**Recommendation**
- Anchor the answer on the Flink 2.2 version-pinned checkpointing docs, then verify the actual allocation contract in the runtime counter implementation rather than relying on API names alone.
- The key behavior to confirm is the `getAndIncrement()` contract: monotonic increase, whether the first id is `0` or `1`, and whether the counter survives restart/failover with the next unused id.

**Implementation anchors**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointIDCounter.java`
- The concrete counter used by your deployment mode, most likely `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/StandaloneCheckpointIDCounter.java`
- If HA/persistent recovery is in scope, also inspect the HA-backed counter implementation in the same package, if present in 2.2.0

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/StandaloneCheckpointIDCounterTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/ZooKeeperCheckpointIDCounterTest.java` if that class exists in 2.2.0
- Any neighboring `CheckpointCoordinator` tests that assert checkpoint numbering across recovery
- Add/strengthen tests for:
  - fresh counter start value
  - monotonic increment
  - no id reuse after shutdown/restart
  - recovery from persisted state resumes at the next id

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointIDCounter.java`
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/StandaloneCheckpointIDCounter.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/StandaloneCheckpointIDCounterTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/ZooKeeperCheckpointIDCounterTest.java`

**Uncertainties**
- I’m not certain whether Flink 2.2.0 starts checkpoint ids at `0` or `1` without checking the exact implementation.
- I’m also not certain which concrete counter class is active in your exact runtime mode, so confirm whether the relevant path is standalone or HA-backed.