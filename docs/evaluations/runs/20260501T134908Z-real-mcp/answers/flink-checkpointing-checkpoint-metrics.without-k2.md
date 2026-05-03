**Recommendation**
- Anchor the answer on the Flink 2.2.0 checkpointing docs and on `org.apache.flink.runtime.checkpoint.CheckpointMetrics`.
- For reporting, the fields to treat as observable are the checkpoint timing and size metrics exposed by `CheckpointMetrics`: `alignmentDurationNanos`, `checkpointStartDelayNanos`, `syncDurationMillis`, `asyncDurationMillis`, `bytesPersistedOfThisCheckpoint`, and `totalBytesPersisted`.
- I would treat any other field as non-reporting unless a consumer test proves it is propagated end-to-end.

**Implementation anchors**
- Version-pinned docs: the Flink 2.2 release checkpointing page on the `flink-docs-release-2.2` docs site.
- Implementation class: `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointMetrics.java`.
- Reporting path to inspect next: the checkpoint stats/reporting code in the same runtime checkpoint package, especially the classes that convert `CheckpointMetrics` into tracked checkpoint statistics.

**Tests to inspect or add**
- Inspect any package-local tests beside `CheckpointMetrics`, especially a focused `CheckpointMetricsTest` if it exists.
- Inspect the checkpoint stats tests that consume the metrics, such as `CheckpointStatsTrackerTest` and nearby checkpoint-coordinator tests.
- Add or strengthen one test that creates a `CheckpointMetrics`, passes it through the reporting path, and asserts each consumed getter survives unchanged.

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointMetrics.java`
- `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/`

**Uncertainties**
- I am not fully certain whether `bytesBufferedInAlignment` is consumed by the 2.2.0 reporting path or just carried on the object.
- I cannot पुष्टि the exact neighboring test filenames in your 2.2.0 tree without inspection, so treat the test names above as the likely anchors, not a guarantee.