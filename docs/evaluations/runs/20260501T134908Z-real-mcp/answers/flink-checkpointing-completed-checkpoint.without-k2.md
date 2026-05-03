**Recommendation**
- Treat `CompletedCheckpoint` as the immutable checkpoint record that survives after a checkpoint finishes, not as the state payload itself.
- Explain it as:
  - the finished checkpoint’s metadata wrapper
  - references to operator/master state handles
  - checkpoint properties that determine retention and restore behavior
  - the object the coordinator/store uses for later recovery or cleanup
- Lifecycle summary: `PendingCheckpoint` becomes `CompletedCheckpoint` after all required acknowledgements and completion hooks finish; it is then registered in the checkpoint store, used for restore, and eventually discarded or retained based on checkpoint retention/externalization settings.

**Implementation anchors**
- Version-pinned docs: the Flink 2.2.0 checkpointing / fault-tolerance docs page in the versioned docs tree is the right user-facing anchor.
- Implementation class: `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CompletedCheckpoint.java`
- Neighboring code to read alongside it: `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/` plus the checkpoint coordinator/store code in the same module.
- The most relevant neighboring tests are in `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/`, especially the `CompletedCheckpoint*`, `PendingCheckpoint*`, and `CheckpointCoordinator*` test classes.

**Tests to inspect or add**
- Inspect tests that cover:
  - creation from pending to completed checkpoint
  - discard / subsume / cleanup behavior
  - restore path from the latest completed checkpoint
  - retention differences for regular checkpoints vs externally retained checkpoints / savepoints
- If coverage is thin, add one focused regression test for:
  - completed checkpoint metadata surviving creation and restore
  - completed checkpoint discard semantics after subsumption or shutdown

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CompletedCheckpoint.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/`

**Uncertainties**
- I’m not fully certain of the exact markdown path for the Flink 2.2.0 docs page without checking the release tree.
- I’m also not fully certain which exact neighboring test class names exist in the 2.2.0 tag versus nearby branches, so I’d anchor on the package and the `CompletedCheckpoint*` / `CheckpointCoordinator*` / `PendingCheckpoint*` families rather than a single test file name.