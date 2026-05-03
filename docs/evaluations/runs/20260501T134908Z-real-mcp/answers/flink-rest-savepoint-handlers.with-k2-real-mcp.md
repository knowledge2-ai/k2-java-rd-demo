**Recommendation**
Anchor the answer on the release-2.2.0 Flink runtime savepoint REST handler and the nearest tests, with only broad checkpointing/state docs as supporting context. K2 did not surface a savepoint-specific version-pinned doc page, so do not overclaim beyond the evidence.

**Implementation anchors**
- Primary implementation class: `SavepointHandlers` in `flink-runtime` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointHandlers.java]
- The returned K2 snippet shows `SavepointHandlerBase` extends `AbstractRestHandler<..., TriggerResponse, SavepointTriggerMessageParameters>`, which is the correct anchor for trigger/poll REST behavior, but K2 did not include the method bodies in the excerpt [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointHandlers.java]
- Version-pinned docs to cite for surrounding checkpoint/savepoint semantics:
  - Checkpoints docs [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
  - State Processor API docs, which explicitly mention savepoints and checkpoints [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/libs/state_processor_api/#part-0001]
  - State Backends docs for checkpoint/state context [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001]

**Tests to inspect or add**
- Existing neighbor test: `SavepointHandlersTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointHandlersTest.java]
- Adjacent behavior test: `StopWithSavepointHandlersTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/savepoints/StopWithSavepointHandlersTest.java]
- If you are adding coverage, focus on:
  - Trigger response shape and operation key propagation
  - Polling path behavior after trigger
  - Success vs in-progress vs failure transitions

**Citations**
- `SavepointHandlers`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointHandlers.java]
- `SavepointHandlersTest`: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointHandlersTest.java]
- `StopWithSavepointHandlersTest`: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/savepoints/StopWithSavepointHandlersTest.java]
- Checkpoints docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
- State Processor API docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/libs/state_processor_api/#part-0001]
- State Backends docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001]

**Uncertainties**
- K2 evidence did not include the specific `SavepointHandlers` methods that implement trigger and polling, so exact REST status transitions and endpoint semantics should be verified directly in the source file.
- K2 did not surface a savepoint-REST-specific version-pinned doc page for Flink 2.2.0, so the docs above are contextual anchors rather than direct API references.