**Recommendation**
Anchor the answer on Kafka Connect 4.2.0’s runtime task abstraction, not on connector-specific subclasses. `WorkerTask` is the common lifecycle state machine for all Connect tasks, so the authoritative behavior should come from the 4.2.0 source plus the Connect docs that describe task startup, stop, and failure handling.

**Implementation anchors**
- Version-pinned docs: Kafka 4.2.0 Connect docs for worker/task lifecycle, especially the task execution and shutdown sections in the 4.2.0 documentation set.
- Implementation class: `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerTask.java`
- Closely related implementations, if you need concrete lifecycle examples:
  - `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSinkTask.java`
  - `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSourceTask.java`

**Tests to inspect or add**
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerTaskTest.java`
- Neighboring lifecycle tests in the same package, especially:
  - `WorkerSinkTaskTest`
  - `WorkerSourceTaskTest`
  - any `WorkerTest` / `AbstractWorkerTest` coverage around task assignment, stopping, and failure transitions
- If behavior is currently under-specified, add focused tests for:
  - start-to-running transitions
  - stop / shutdown idempotence
  - failure transitions and cleanup
  - interrupt / wakeup handling during task shutdown

**Citations**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerTask.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerTaskTest.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSinkTask.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSourceTask.java`

**Uncertainties**
- I’m confident about the core class and test locations, but not about the exact 4.2.0 docs page path without checking the published artifact set.
- If you need a fully version-pinned public doc URL, I’d want to verify the exact Kafka 4.2.0 docs location rather than guess it.