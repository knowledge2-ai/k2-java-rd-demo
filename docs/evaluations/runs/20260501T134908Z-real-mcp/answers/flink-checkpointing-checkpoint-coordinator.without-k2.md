**Recommendation**
- Anchor the write-up on the Flink 2.2 checkpointing docs, then trace the JobManager-side flow through `CheckpointCoordinator` as the checkpoint lifecycle orchestrator: trigger gating, pending checkpoint creation, task fan-out, acknowledgements, completion, abort/decline handling, periodic scheduling, and cleanup.

**Implementation anchors**
- Version-pinned docs: Flink 2.2 checkpointing docs on the release-2.2 site.
- Core class: `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinator.java`
- Related runtime types to keep nearby: `PendingCheckpoint`, `CompletedCheckpoint`, `CheckpointProperties`, `CheckpointException`, `CheckpointIDCounter`

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java`
- Other same-package checkpoint coordinator tests that cover:
  - trigger gating / repeated trigger rejection
  - periodic scheduling
  - ack and completion paths
  - abort / decline / failure cleanup
- Add a focused regression test for:
  - successful trigger -> pending checkpoint creation -> completion
  - rejected trigger when coordinator preconditions are not met

**Citations**
- `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/`
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinator.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java`

**Uncertainties**
- I am not fully certain the exact 2.2.0 docs slug is unchanged from the path above, but the `flink-docs-release-2.2` site is the correct version anchor.
- I am certain about the coordinator class path; neighboring test class names beyond `CheckpointCoordinatorTest` may vary slightly across 2.2.x branches.