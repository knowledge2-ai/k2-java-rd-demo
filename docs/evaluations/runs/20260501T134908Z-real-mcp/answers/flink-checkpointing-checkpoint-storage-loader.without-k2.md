**Recommendation**
- Anchor the explanation on the Flink 2.2.0 release docs for checkpointing and state backends, then verify against `CheckpointStorageLoader`.
- The loading flow is configuration-first: an explicitly configured checkpoint storage wins; otherwise Flink derives a default storage from checkpoint-related config, typically filesystem-backed when `state.checkpoints.dir` is set, and job-manager-backed when no checkpoint directory is configured.
- Treat savepoint config as separate from checkpoint storage selection; it influences defaults, but it is not the same decision point.

**Implementation anchors**
- `flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageLoader.java`
- `flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorage.java`
- `flink-runtime/src/main/java/org/apache/flink/runtime/state/storage/FileSystemCheckpointStorage.java`
- `flink-runtime/src/main/java/org/apache/flink/runtime/state/storage/JobManagerCheckpointStorage.java`

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/state/CheckpointStorageLoaderTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/state/storage/FileSystemCheckpointStorageTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/state/storage/JobManagerCheckpointStorageTest.java`
- Add or tighten a test that locks down precedence between explicit storage config, `state.checkpoints.dir`, and the no-checkpoint-dir fallback.

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageLoader.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/state/CheckpointStorageLoaderTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/state/storage/FileSystemCheckpointStorageTest.java`

**Uncertainties**
- I am not fully certain of the exact Flink 2.2.0 docs URL path from memory.
- Minor method signatures and exact config precedence details in `CheckpointStorageLoader` may differ slightly across 2.2.x point releases.