**Recommendation**
Anchor the answer on the Flink 2.2.0 release checkpointing docs and confirm behavior against `CheckpointCoordinatorConfiguration`, since that class is the runtime normalization point for coordinator-level checkpoint settings.

**Implementation anchors**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorConfiguration.java`
- The surrounding config flow should be traced from checkpoint-related config options into that class, especially where interval, timeout, min-pause, concurrent checkpoints, tolerable failures, and aligned/unaligned flags are materialized.
- Use the 2.2.0 release docs for checkpointing, not current `main` docs, to avoid version drift.

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorConfigurationTest.java` if it exists in 2.2.0.
- Nearby same-package coverage, especially `CheckpointCoordinatorTest.java`.
- If coverage is thin, add assertions for option-to-field mapping and defaults for:
  - checkpoint interval
  - checkpoint timeout
  - min pause
  - max concurrent checkpoints
  - tolerable failed checkpoints
  - aligned vs unaligned checkpoint behavior

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorConfiguration.java`

**Uncertainties**
- I cannot verify the exact 2.2.0 docs path without browsing.
- I cannot confirm from memory whether `CheckpointCoordinatorConfigurationTest` exists in that release, so `CheckpointCoordinatorTest` is the safer neighboring anchor if it does not.