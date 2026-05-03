**Recommendation**
Use `CANONICAL` as the safe/default savepoint format when you want portability across state backends. Treat `NATIVE` as a backend-specific format that is serialized/deserialized in the runtime, but is not the default supported path for all backends. That matches the backend gate in `StateBackend.supportsSavepointFormat(...)`, which returns true only for `CANONICAL` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/StateBackend.java]. The docs also say Flink unified the binary savepoint format starting in 1.13, which is the portability baseline to cite [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0006].

**Implementation anchors**
- `SavepointFormatType` itself: the version-pinned enum in `flink-core` [repo://apache/flink@release-2.2.0/flink-core/src/main/java/org/apache/flink/core/execution/SavepointFormatType.java].
- `StateBackend.supportsSavepointFormat(...)`: default support is only `CANONICAL` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/StateBackend.java].
- `EventSerializer.decodeSavepointType(...)`: runtime wire decoding accepts both `CANONICAL` and `NATIVE` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/io/network/api/serialization/EventSerializer.java].
- `CheckpointProperties.forSyncSavepoint(...)` and `forUnclaimedSnapshot()`: savepoint creation flows thread the format type through, and unclaimed snapshots are forced to `CANONICAL` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointProperties.java].
- Version-pinned docs to cite alongside the code:
  - Checkpoints overview [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
  - State backends / savepoint format unification note [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0006]

**Tests to inspect or add**
- `EventSerializerTest`: exercises both `SavepointType.terminate(SavepointFormatType.CANONICAL)` and `SavepointType.savepoint/suspend(SavepointFormatType.NATIVE)` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/io/network/api/serialization/EventSerializerTest.java].
- `PendingCheckpointTest`: verifies savepoint-related checkpoint properties with `CANONICAL` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/PendingCheckpointTest.java].
- `CheckpointMetadataLoadingTest`: validates savepoint loading using `CANONICAL` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointMetadataLoadingTest.java].
- If you want tighter coverage, add a dedicated `SavepointFormatTypeTest` or extend `EventSerializerTest` to assert any enum-to-wire mapping explicitly. K2 did not surface a dedicated `SavepointFormatTypeTest`.

**Citations**
- `SavepointFormatType`: [repo://apache/flink@release-2.2.0/flink-core/src/main/java/org/apache/flink/core/execution/SavepointFormatType.java]
- `StateBackend.supportsSavepointFormat(...)`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/StateBackend.java]
- `EventSerializer`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/io/network/api/serialization/EventSerializer.java]
- `CheckpointProperties`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointProperties.java]
- `EventSerializerTest`: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/io/network/api/serialization/EventSerializerTest.java]
- `PendingCheckpointTest`: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/PendingCheckpointTest.java]
- `CheckpointMetadataLoadingTest`: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointMetadataLoadingTest.java]
- Docs:
  - [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
  - [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0006]

**Uncertainties**
- The K2 snippets did not expose the full body of `SavepointFormatType.java`, so I’m relying on the runtime call sites and tests for the exact behavior rather than enumerating every enum member from the file itself.
- I did not find a dedicated `SavepointFormatTypeTest`; if one exists outside the surfaced results, K2 didn’t return it.