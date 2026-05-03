**Recommendation**
Anchor the analysis on the Kafka Connect 4.2.0 public docs for lifecycle context, then treat `WorkerTask` as the primary implementation source and `WorkerTaskTest` as the direct behavioral oracle. Use `WorkerSinkTaskTest` and `ExactlyOnceSourceIntegrationTest` as neighboring regression coverage for task startup, rebalance, restart, and recovery paths.

**Implementation anchors**
- Version-pinned docs:
  - Kafka Connect landing page for 4.2: [https://kafka.apache.org/42/kafka-connect/](https://kafka.apache.org/42/kafka-connect/)
  - Connector Development Guide for 4.2: [https://kafka.apache.org/42/kafka-connect/connector-development-guide/](https://kafka.apache.org/42/kafka-connect/connector-development-guide/)
  - General 4.2 API index with Connect API entry: [https://kafka.apache.org/42/apis/](https://kafka.apache.org/42/apis/)
- Implementation class:
  - `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerTask.java` ([repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerTask.java])
- Lifecycle-related nearby runtime code surfaced in the same search:
  - `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConnector.java` ([repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConnector.java])
  - `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/AbstractHerder.java` ([repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/AbstractHerder.java])

**Tests to inspect or add**
- Direct unit coverage:
  - `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerTaskTest.java` ([repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerTaskTest.java])
- Neighboring runtime behavior:
  - `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSinkTaskTest.java` ([repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSinkTaskTest.java])
- Integration/lifecycle recovery:
  - `connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java` ([repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java])

**Citations**
- Docs: [https://kafka.apache.org/42/kafka-connect/](https://kafka.apache.org/42/kafka-connect/), [https://kafka.apache.org/42/kafka-connect/connector-development-guide/](https://kafka.apache.org/42/kafka-connect/connector-development-guide/), [https://kafka.apache.org/42/apis/](https://kafka.apache.org/42/apis/)
- Impl: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerTask.java]
- Tests: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerTaskTest.java], [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSinkTaskTest.java], [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java]

**Uncertainties**
- The K2 evidence did not surface a WorkerTask-specific version-pinned design doc; the best anchors are the public 4.2 Connect docs plus the runtime class and tests.
- The evidence is enough to identify the right files, but not enough by itself to claim every lifecycle edge case without reading those files directly.