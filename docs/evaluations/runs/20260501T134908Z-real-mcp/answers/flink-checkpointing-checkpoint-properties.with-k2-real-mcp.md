## Recommendation
Use `CheckpointProperties` in `flink-runtime` as the implementation anchor, and keep the explanation tied to the 2.2.0 docs for checkpoints/savepoints. The class models checkpoint retention and cleanup semantics, while savepoints are handled as a distinct manual path, not as queued time-triggered checkpoints [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointProperties.java].

## Implementation anchors
- `CheckpointProperties` is the source of truth for the property flags and retention behavior, including the delete/retain matrix for success, cancellation, failure, and suspension [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointProperties.java].
- The docs anchor is the 2.2 release checkpointing docs, especially the checkpoints overview and the checkpointing guide, which point readers to the checkpoints-vs-savepoints distinction [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001] [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001].
- Savepoint behavior should be described as manual-triggered and separate from checkpoint queuing/trigger limits; the retrieved class text explicitly notes savepoints are not queued due to time-trigger limits and require separate garbage-collection handling [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointProperties.java].

## Tests to inspect or add
- `CheckpointPropertiesTest` for direct flag/behavior coverage [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointPropertiesTest.java].
- `PendingCheckpointTest` for forced-checkpoint subsumption and lifecycle edge cases [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/PendingCheckpointTest.java].
- `CompletedCheckpointTest` for garbage-collection and cleanup behavior on subsume [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CompletedCheckpointTest.java].
- `CheckpointMetadataLoadingTest` for savepoint loading behavior and savepoint-format interactions [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointMetadataLoadingTest.java].
- `CheckpointFailureManagerTest` if you need coverage for how retention policy affects failure handling [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointFailureManagerTest.java].

## Citations
- Docs: checkpoints overview [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
- Docs: checkpointing guide [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001]
- Implementation: `CheckpointProperties` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointProperties.java]
- Test: `CheckpointPropertiesTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointPropertiesTest.java]
- Neighbor tests: `PendingCheckpointTest`, `CompletedCheckpointTest`, `CheckpointMetadataLoadingTest`, `CheckpointFailureManagerTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/PendingCheckpointTest.java] [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CompletedCheckpointTest.java] [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointMetadataLoadingTest.java] [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointFailureManagerTest.java]

## Uncertainties
- The K2 evidence clearly identifies the correct class and neighboring tests, but the returned source snippet is truncated, so I cannot safely enumerate every constructor argument or every flag name beyond the visible retention/delete semantics.
- If you need a byte-accurate flag-by-flag description, the next step is to inspect the full `CheckpointProperties.java` source and `CheckpointPropertiesTest.java` together.