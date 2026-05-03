**Recommendation**
Anchor the explanation on the version-pinned 2.2.0 checkpoint docs plus `CompletedCheckpoint` itself. The docs establish the user-facing semantics of checkpoints, while the implementation shows that a completed checkpoint is primarily metadata plus handles/pointers to state, persisted externally and retained in JobManager memory [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001], [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001], [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CompletedCheckpoint.java].

**Implementation anchors**
- `CompletedCheckpoint` is the core implementation class to inspect for metadata shape, external persistence, and lifecycle hooks [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CompletedCheckpoint.java].
- The class docs explicitly note:
  - completed checkpoint objects are usually small because state handles are pointers,
  - some backends may embed payload directly in metadata,
  - the checkpoint metadata is persisted in external storage via an external pointer,
  - retained completed checkpoints consume JobManager heap [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CompletedCheckpoint.java].
- For lifecycle behavior around storage and retention, `DefaultCompletedCheckpointStore` is the adjacent runtime class to inspect; it manages adding checkpoints and subsuming/removing old ones [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStore.java].

**Tests to inspect or add**
- `CompletedCheckpointTest` for:
  - restoring/registering shared states after recovery,
  - cleanup behavior when a checkpoint is subsumed [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CompletedCheckpointTest.java].
- `DefaultCompletedCheckpointStoreTest` for:
  - retention/subsumption ordering,
  - recovery of sorted completed checkpoints from the state handle store [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStoreTest.java].
- If adding coverage, focus on one test for metadata persistence/restore and one for old-checkpoint cleanup on subsume.

**Citations**
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001], [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001]
- Implementation: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CompletedCheckpoint.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStore.java]
- Tests: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CompletedCheckpointTest.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStoreTest.java]

**Uncertainties**
The K2 evidence is enough to anchor the answer, but not enough to give a full field-by-field lifecycle walkthrough of `CompletedCheckpoint` without guessing. In particular, the exact constructor fields, serialization format, and every transition method were not fully surfaced in the evidence, so those details should be verified directly in `CompletedCheckpoint.java` before making stronger claims.