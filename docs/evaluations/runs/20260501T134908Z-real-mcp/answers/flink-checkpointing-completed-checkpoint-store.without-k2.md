**Recommendation**
`CompletedCheckpointStore` in Flink 2.2.0 should be read as the retention boundary for *completed* checkpoints: when a new checkpoint is added, the store keeps only the configured maximum number of recent completed checkpoints and discards older ones. For the answer, anchor on the 2.2.0 checkpointing docs, the runtime store implementation, and the store-specific retention tests in the same package.

**Implementation anchors**
- Version-pinned docs: the Flink 2.2.0 checkpointing/fault-tolerance docs that describe checkpoint retention and the “number of retained checkpoints” setting.
- Implementation class: `org.apache.flink.runtime.checkpoint.CompletedCheckpointStore`
- Concrete retention logic is typically in the concrete store implementation used by the deployment, most likely `StandaloneCompletedCheckpointStore` or the HA-backed sibling store in the same package.
- Behavior to verify: newest checkpoint is retained, older completed checkpoints are pruned once the retention limit is exceeded, and recovery reads from the latest retained checkpoint.

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/StandaloneCompletedCheckpointStoreTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/ZooKeeperCompletedCheckpointStoreTest.java`
- Any shared `CompletedCheckpointStore` test in the same package, if present
- Add or tighten a regression test that asserts eviction order when adding checkpoint `N+1` with a retention limit of `N`

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CompletedCheckpointStore.java`
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/StandaloneCompletedCheckpointStore.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/StandaloneCompletedCheckpointStoreTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/ZooKeeperCompletedCheckpointStoreTest.java`

**Uncertainties**
- I’m not certain whether Flink 2.2.0 uses exactly `StandaloneCompletedCheckpointStore` as the primary concrete class in your code path, or whether a newer helper/adapter class sits in front of it.
- I’m also not certain of the exact version-pinned docs URL without checking the release site.