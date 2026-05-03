**Recommendation**
- Treat `DefaultCompletedCheckpointStore` as the source of truth for completed-checkpoint retention.
- The default behavior is bounded FIFO retention: it keeps only a fixed number of the newest completed checkpoints and discards the oldest once the cap is exceeded.
- For Flink 2.2.0, the practical default is typically `1` retained completed checkpoint unless the checkpointing config overrides it.

**Implementation anchors**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStore.java`
- Use the checkpointing config path that feeds the store’s `maxNumberOfRetainedCheckpoints` setting.
- If you need the behavioral contract, follow the concrete store subclasses in the same package as well, because they usually inherit or wrap this retention logic.

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStoreTest.java` if present
- Neighboring store-contract tests in the same package, especially any `*CompletedCheckpointStoreTest` subclasses
- Add or verify a regression that:
  - inserts `N + 1` completed checkpoints,
  - confirms the oldest one is evicted,
  - confirms the newest checkpoint remains the recovery candidate,
  - and confirms the retained-count cap is enforced exactly.

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStore.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStoreTest.java` if that file exists in 2.2.0

**Uncertainties**
- I am confident about the retention shape and the runtime class, but I am not certain of the exact 2.2.0 docs page slug for the checkpoint-retention config.
- I am also not certain whether `DefaultCompletedCheckpointStoreTest` exists verbatim in 2.2.0 or whether the coverage is only in nearby shared store tests.