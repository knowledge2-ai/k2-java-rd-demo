**Recommendation**
- Anchor the answer on the 4.2.0 Connect docs, then trace behavior in `WorkerSourceTask`: polling and committing are separate phases.
- The practical point to verify is that `poll()` fetches `SourceRecord`s from the user `SourceTask`, while source-offset advancement/flush/commit happens through the offset storage path after records are accepted, not directly inside the poll call.

**Implementation anchors**
- Version-pinned docs: `https://kafka.apache.org/42/documentation.html` for Kafka Connect behavior/context.
- Main class: `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSourceTask.java`
- Closely related runtime code to inspect alongside it: `connect/runtime/src/main/java/org/apache/kafka/connect/storage/OffsetStorageWriter.java`

**Tests to inspect or add**
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSourceTaskTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/storage/OffsetStorageWriterTest.java`
- If present in the 4.2.0 tree, also inspect any `SourceTaskOffsetCommitterTest`-style coverage in `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/`
- Add or confirm tests for:
  - empty poll does not commit
  - successful poll followed by send/flush triggers offset write/commit
  - commit behavior on task stop/close
  - retry/failure paths do not advance offsets prematurely

**Citations**
- `https://kafka.apache.org/42/documentation.html`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSourceTask.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSourceTaskTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/storage/OffsetStorageWriterTest.java`

**Uncertainties**
- I’m not fully certain of the exact 4.2.0 docs subsection anchor for source-task behavior, so I’m citing the versioned documentation root.
- I’m not fully certain whether a `SourceTaskOffsetCommitterTest` exists under that exact name in 4.2.0; if not, the worker-task and offset-writer tests are the nearest anchors.