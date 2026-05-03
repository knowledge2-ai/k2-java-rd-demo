**Recommendation**
- Anchor the answer on the Flink 2.2 release docs, then defer to the runtime source for the actual allocation semantics.
- For `StandaloneCheckpointIDCounter`, the key question is whether it is purely local/monotonic and how the first checkpoint ID is seeded; confirm that directly in source rather than inferring from docs.

**Implementation anchors**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/StandaloneCheckpointIDCounter.java`
- Neighboring runtime classes in the same package, especially `CheckpointIDCounter` and checkpoint-coordinator code that calls into the counter.
- If you need a contrast case, also inspect the HA-backed counter implementation in the same subsystem.

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/`
- Look for a dedicated `StandaloneCheckpointIDCounter` unit test in that package.
- If coverage is thin, add tests for:
  - initial ID seed
  - monotonic increments
  - behavior after `start/stop` or `shutdown`
  - concurrent allocation if the implementation is thread-safe
  - any restart/reset semantics specific to standalone mode

**Citations**
- Apache Flink 2.2 checkpointing docs: `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/`
- Implementation class: `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/StandaloneCheckpointIDCounter.java`
- Test package to inspect: `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/`

**Uncertainties**
- I cannot verify the exact first checkpoint ID value or any 2.2.0-specific edge behavior without source access.
- I cannot confirm the exact neighboring test filenames in that tree, only the package and the likely class name pattern.