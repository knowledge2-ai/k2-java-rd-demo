**Recommendation**
- Treat `CheckpointStatsTracker` as the runtime-side aggregator for checkpoint lifecycle statistics: it consumes checkpoint events, maintains counts/history/latest state, and publishes a snapshot used by the Web UI and REST stats endpoints.
- For Flink 2.2.0, anchor the answer on the 2.2 checkpointing docs, the tracker implementation itself, and the unit tests in the same package plus adjacent snapshot/history tests.

**Implementation anchors**
- Docs: Apache Flink 2.2 checkpointing docs, likely under `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpointing/`
- Implementation: `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointStatsTracker.java`
- Related runtime types to inspect: `CheckpointStatsSnapshot`, `CheckpointStatsHistory`, `CheckpointStatsCounts`, `PendingCheckpointStats`, `CompletedCheckpointStats`, `FailedCheckpointStats`, `RestoredCheckpointStats`
- Behavior to describe: it tracks lifecycle transitions, updates per-checkpoint and aggregate counters, retains a bounded history, and exposes the latest snapshot for reporting/metrics.

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointStatsTrackerTest.java`
- Nearby tests in the same package for the supporting data model, especially snapshot/history/count semantics
- Add or extend coverage for:
  - pending -> completed / failed / aborted transitions
  - history retention and “latest checkpoint” selection
  - restored checkpoint handling
  - behavior when no checkpoints have occurred yet
  - concurrency or synchronization-sensitive updates if the tracker is updated from multiple callbacks

**Citations**
- `org.apache.flink.runtime.checkpoint.CheckpointStatsTracker`
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointStatsTracker.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointStatsTrackerTest.java`
- `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpointing/`

**Uncertainties**
- I am not fully certain the 2.2 docs slug is exactly `checkpointing`; it may be `checkpoints` in that release line.
- I am not fully certain of the exact neighboring test class names beyond `CheckpointStatsTrackerTest`; verify the package for the snapshot/history tests before citing them as exact artifacts.