**Recommendation**
`CheckpointStorageCoordinatorView` is the coordinator-side slice of Flink checkpoint storage: the JobManager/coordinator uses it to resolve durable checkpoint locations and recover checkpoint metadata, but it is not the task-side stream-writing API. For a 2.2.0 explanation, anchor the contract on the 2.2 docs plus the concrete storage backend you are actually discussing, most likely `FileSystemCheckpointStorage` or `JobManagerCheckpointStorage`.

**Implementation anchors**
- `flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageCoordinatorView.java`
- `flink-runtime/src/main/java/org/apache/flink/runtime/state/storage/FileSystemCheckpointStorage.java`
- `flink-runtime/src/main/java/org/apache/flink/runtime/state/storage/JobManagerCheckpointStorage.java`
- Related contract neighbors: `CheckpointStorageAccess`, `CheckpointStorageLocation`, `CheckpointStreamFactory`

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/state/storage/FileSystemCheckpointStorageTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/state/storage/JobManagerCheckpointStorageTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/state/CheckpointStorageLoaderTest.java`
- If missing, add a test that proves the coordinator view only covers checkpoint-location resolution and durable metadata handling, not task-owned state emission.

**Citations**
- `https://nightlies.apache.org/flink/flink-docs-release-2.2/`
- `flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageCoordinatorView.java`
- `flink-runtime/src/main/java/org/apache/flink/runtime/state/storage/FileSystemCheckpointStorage.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/state/storage/FileSystemCheckpointStorageTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/state/storage/JobManagerCheckpointStorageTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/state/CheckpointStorageLoaderTest.java`

**Uncertainties**
- I am not certain whether your specific 2.2.0 discussion should center on filesystem-backed storage or job-manager-backed storage; the coordinator contract is the same shape, but the concrete implementation anchor changes.
- I am not certain of the exact 2.2.0 doc subpage path without browsing, so I anchored the docs at the 2.2 release docs root.