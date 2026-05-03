**Recommendation**
Use the 4.2-pinned Kafka Connect docs for the public contract, then anchor the behavior discussion in `WorkerSinkTask` itself and `WorkerSinkTaskTest`. The implementation class is the primary source for sink delivery/commit mechanics, especially the `recordBatch(...)` and `recordCommitSuccess(...)` overrides and the test-visible `getNextCommit()` hook [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSinkTask.java].

**Implementation anchors**
- Version-pinned docs:
  - Kafka Connect landing page for 4.2: [https://kafka.apache.org/42/kafka-connect/](https://kafka.apache.org/42/kafka-connect/)
  - Connector Development Guide for 4.2: [https://kafka.apache.org/42/kafka-connect/connector-development-guide/](https://kafka.apache.org/42/kafka-connect/connector-development-guide/)
- Runtime implementation:
  - `WorkerSinkTask`: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSinkTask.java]
- Nearby API surface:
  - `SinkTask`: [repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/sink/SinkTask.java]

**Tests to inspect or add**
- Primary neighboring test:
  - `WorkerSinkTaskTest`: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSinkTaskTest.java]
- Adjacent tests surfaced by K2, but they are not as directly on-point for sink delivery/commit:
  - `ConnectorValidationIntegrationTest`: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ConnectorValidationIntegrationTest.java]
  - `ExactlyOnceSourceIntegrationTest`: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java]

**Citations**
- Docs: [https://kafka.apache.org/42/kafka-connect/](https://kafka.apache.org/42/kafka-connect/), [https://kafka.apache.org/42/kafka-connect/connector-development-guide/](https://kafka.apache.org/42/kafka-connect/connector-development-guide/)
- Implementation: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSinkTask.java]
- Core test anchor: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSinkTaskTest.java]
- Adjacent tests: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ConnectorValidationIntegrationTest.java], [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java]

**Uncertainties**
- K2 surfaced `WorkerSinkTaskTest` as the direct neighboring test anchor, but did not return a deeper test inventory specifically centered on sink delivery/commit paths.
- The evidence snippet for `WorkerSinkTask` confirms the relevant overrides, but K2 did not return the full method bodies here, so any finer-grained behavioral claim should be verified directly in that class before stating it as fact.