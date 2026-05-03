**Recommendation**
Anchor the behavior discussion on the 2.2.0 checkpointing docs, then verify against `CheckpointStatsSnapshot` itself. Treat it as the immutable, point-in-time aggregate over checkpoint counters, summaries, history, and “latest” checkpoint state.

**Implementation anchors**
- Version-pinned docs: the Flink 2.2.x checkpointing / fault-tolerance docs, especially the sections on checkpoint statistics, checkpoint history, and the Web UI / REST checkpoint views.
- Core implementation class: `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointStatsSnapshot.java`
- Closely related production types to read alongside it:
  - `CheckpointStatsTracker`
  - `CheckpointStatsCounts`
  - `CheckpointStatsSummary`
  - `CheckpointStatsHistory`
  - `CompletedCheckpointStats`
  - `FailedCheckpointStats`
  - `PendingCheckpointStats`
  - `RestoredCheckpointStats`

**Tests to inspect or add**
- Neighboring tests in `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/`:
  - `CheckpointStatsTrackerTest`
  - `CheckpointStatsHistoryTest`
  - Any existing `CheckpointStatsSnapshot*Test` if present in 2.2.0
- Add or extend tests for:
  - snapshot immutability
  - counts/history consistency across updates
  - propagation of latest completed / failed / restored checkpoints
  - behavior when new checkpoints arrive after a snapshot is taken

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointStatsSnapshot.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointStatsTrackerTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointStatsHistoryTest.java`

**Uncertainties**
- I can name the code anchors confidently, but I cannot verify the exact 2.2.0 docs URL or whether a dedicated `CheckpointStatsSnapshot` test file exists without browsing.