**Recommendation**
- Anchor the answer on Kafka Connect’s sink-task contract: records are handed to the sink task first, and offsets are committed only after successful processing. The behavior is at-least-once.
- For `Kafka Connect 4.2.0`, read the version-pinned docs/Javadocs together with `WorkerSinkTask` source, then validate against the unit tests that cover delivery, commit, error, and rebalance paths.

**Implementation anchors**
- Docs: Kafka 4.2.0 Connect docs and `SinkTask` Javadoc.
- Implementation class: `org.apache.kafka.connect.runtime.WorkerSinkTask`.
- Behavior to inspect: batch polling, `put(...)` delivery, `flush(...)` / `preCommit(...)`, scheduled offset commits, and retry behavior when delivery or commit fails.

**Tests to inspect or add**
- Existing: `WorkerSinkTaskTest` for delivery, commit, and failure handling.
- Existing: `WorkerSinkTaskThreadedTest` for poll-loop and commit-timing behavior.
- Add or extend cases for:
  - `put()` succeeds but offset commit fails and is retried.
  - `put()` throws and offsets are not committed.
  - partial-batch delivery semantics.
  - rebalance while records are in flight.

**Citations**
- Apache Kafka 4.2.0 docs: `https://kafka.apache.org/42/documentation.html`
- `SinkTask` Javadoc: `https://kafka.apache.org/42/javadoc/org/apache/kafka/connect/sink/SinkTask.html`
- Source: `https://github.com/apache/kafka/blob/4.2.0/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSinkTask.java`
- Test: `https://github.com/apache/kafka/blob/4.2.0/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSinkTaskTest.java`
- Test: `https://github.com/apache/kafka/blob/4.2.0/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSinkTaskThreadedTest.java`

**Uncertainties**
- I cannot verify exact method names or line numbers for 4.2.0 without repository access.
- If Kafka 4.2.0 moved or renamed any neighboring test class, `WorkerSinkTaskThreadedTest` is the most likely companion, but that is the one item I am least certain about.