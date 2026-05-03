**Recommendation**
- Use the retained policy only when you explicitly need post-cancellation inspection or manual recovery from the externalized checkpoint directory.
- For normal operation, prefer deleting externalized checkpoints on terminal job states and use savepoints for intentional, operator-managed restore points.
- In Flink terms, the practical choice is usually:
  - `RETAIN_ON_CANCELLATION`: keep the checkpoint after cancel/termination.
  - `DELETE_ON_CANCELLATION` or the equivalent internal “do not retain after termination” path: clean it up when the job ends.

**Implementation anchors**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointRetentionPolicy.java`
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointProperties.java`
- Version-pinned docs tree for Flink 2.2.0, especially the checkpointing / externalized checkpoints / savepoints material under `flink-docs-release-2.2`.

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointPropertiesTest.java`
- Nearby checkpoint-coordinator tests that cover terminal-state cleanup and property-to-policy mapping.
- If coverage is thin, add a regression test for:
  - retained checkpoints surviving cancellation, and
  - deleted checkpoints being discarded on termination.

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointRetentionPolicy.java`
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointProperties.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointPropertiesTest.java`

**Uncertainties**
- I cannot verify the exact 2.2.0 enum constant names without repository access; Flink has used both an internal retention policy type and a public externalized-checkpoint retention enum over time.
- The exact 2.2.0 docs subpath may vary, but it should be under the `flink-docs-release-2.2` docs tree.