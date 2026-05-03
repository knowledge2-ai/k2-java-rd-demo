**Recommendation**
Use the Flink `release-2.2.0` docs plus the `flink-runtime` REST handler and its direct test as the anchor set for checkpoint trigger/status behavior. K2 surfaced the version-pinned checkpointing docs, the `CheckpointHandlers` implementation, and `CheckpointHandlersTest` as the direct evidence trail, but it did not return method-level details for the trigger/status endpoints, so don’t infer beyond those anchors.

**Implementation anchors**
- Version-pinned docs:
  - Checkpoints overview: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
  - Checkpointing guide: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001]
- REST implementation class:
  - `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/checkpoints/CheckpointHandlers.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/checkpoints/CheckpointHandlers.java]
- Package scope to keep the answer grounded:
  - `org.apache.flink.runtime.rest.handler.job.checkpoints` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/checkpoints/CheckpointHandlers.java]

**Tests to inspect or add**
- Start with the direct regression test:
  - `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/checkpoints/CheckpointHandlersTest.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/checkpoints/CheckpointHandlersTest.java]
- K2 did not return additional neighboring checkpoint-handler test files, so if you need broader coverage, inspect the same package for nearby REST handler tests and add focused cases there.
- The surfaced test file already suggests trigger-path coverage via `CheckpointHandlers.CheckpointTriggerHandler`, but K2 did not expose the exact assertions or status-path methods, so those remain to be verified in-source.

**Citations**
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001]
- Implementation: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/checkpoints/CheckpointHandlers.java]
- Test: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/checkpoints/CheckpointHandlersTest.java]

**Uncertainties**
- K2 evidence did not expose the concrete REST sub-operations for trigger vs. status, only the handler class and its direct test.
- No adjacent test classes were returned, so I can’t name additional neighboring tests with confidence from this evidence alone.
