**Recommendation**
- Anchor the answer on Kafka Connect’s 4.2.0 docs and the runtime `Worker` class.
- Treat `Worker` as the orchestration layer: it owns connector/task start-stop sequencing, status transitions, callbacks, and failure handling, while the connector/task implementations own their own business logic.
- For a lifecycle trace, follow `Worker` into the connector wrappers and task runners rather than trying to infer behavior from the herder alone.

**Implementation anchors**
- Version-pinned docs: Apache Kafka 4.2.0 docs root, `https://kafka.apache.org/42/documentation/`  
- Implementation class: `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/Worker.java`
- Adjacent runtime classes worth reading alongside it:
  - `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConnector.java`
  - `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSinkTask.java`
  - `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSourceTask.java`

**Tests to inspect or add**
- Inspect first:
  - `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerTest.java`
  - `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSinkTaskTest.java`
  - `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSourceTaskTest.java`
- If present in the 4.2.0 tree, also inspect connector-facing worker tests such as `WorkerConnectorTest.java`.
- Good regression coverage to add:
  - connector start/stop success and failure transitions
  - task start/stop/restart sequencing
  - shutdown ordering and callback propagation
  - error-path behavior when connector/task init fails partway through lifecycle

**Citations**
- `https://kafka.apache.org/42/documentation/`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/Worker.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSinkTaskTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSourceTaskTest.java`

**Uncertainties**
- I cannot verify the exact Connect-doc section anchor for 4.2.0 without browsing.
- I’m confident about `Worker` and the task tests above, but I’m not certain whether `WorkerConnectorTest.java` exists in the 4.2.0 branch, so treat that one as “check if present.”