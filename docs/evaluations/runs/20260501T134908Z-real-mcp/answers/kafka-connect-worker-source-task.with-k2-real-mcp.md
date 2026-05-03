**Recommendation**
Anchor the answer on the Kafka 4.2.0 Connect docs plus the runtime commit scheduler, not just `WorkerSourceTask` itself. The clearest behavior split is:
- source tasks poll records in the task execution loop, and
- offset commits are driven by `SourceTaskOffsetCommitter`, which only calls `WorkerSourceTask.commitOffsets()` when `shouldCommitOffsets()` is true and logs/handles failures around the flush path [https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0010](https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0010), [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/SourceTaskOffsetCommitter.java](repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/SourceTaskOffsetCommitter.java).

**Implementation anchors**
- `WorkerSourceTask` is the implementation class to inspect for the source-task execution path, including the commit-flush path and timeout/cancel handling [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSourceTask.java](repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSourceTask.java).
- `SourceTaskOffsetCommitter` is the neighboring runtime class that schedules and gates commits; its `commit(WorkerSourceTask)` helper skips when there are no offsets to commit, otherwise invokes `workerTask.commitOffsets()` and catches unexpected exceptions so the scheduled executor keeps running [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/SourceTaskOffsetCommitter.java](repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/SourceTaskOffsetCommitter.java).
- Version-pinned docs to cite:
  - Kafka Connect landing page for 4.2 [https://kafka.apache.org/42/kafka-connect/](https://kafka.apache.org/42/kafka-connect/)
  - Connector Development Guide section describing `SourceTask` commit/commitRecord semantics [https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0010](https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0010)
  - Kafka API page for the Connect API [https://kafka.apache.org/42/apis/#part-0003](https://kafka.apache.org/42/apis/#part-0003)

**Tests to inspect or add**
- `WorkerSourceTaskTest` for the direct unit-level behavior around commit skipping and log assertions [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSourceTaskTest.java](repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSourceTaskTest.java).
- `SourceTaskOffsetCommitterTest` for scheduled commit gating, timeout, and failure handling [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/SourceTaskOffsetCommitterTest.java](repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/SourceTaskOffsetCommitterTest.java).
- `ErrorHandlingTaskTest` for an execution-path regression test showing `sourceTask.poll()` is invoked and `commitOffsets()` is reached after task execution [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ErrorHandlingTaskTest.java](repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ErrorHandlingTaskTest.java).
- `ExactlyOnceSourceIntegrationTest` if you want to contextualize offset behavior under exactly-once / per-connector offsets semantics, but it is not the first test to cite for basic poll/commit flow [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java](repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java).

**Citations**
- Docs:
  - [https://kafka.apache.org/42/kafka-connect/](https://kafka.apache.org/42/kafka-connect/)
  - [https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0010](https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0010)
  - [https://kafka.apache.org/42/apis/#part-0003](https://kafka.apache.org/42/apis/#part-0003)
- Code:
  - [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSourceTask.java](repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSourceTask.java)
  - [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/SourceTaskOffsetCommitter.java](repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/SourceTaskOffsetCommitter.java)
- Tests:
  - [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSourceTaskTest.java](repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSourceTaskTest.java)
  - [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/SourceTaskOffsetCommitterTest.java](repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/SourceTaskOffsetCommitterTest.java)
  - [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ErrorHandlingTaskTest.java](repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ErrorHandlingTaskTest.java)
  - [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java](repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java)

**Uncertainties**
- The K2 evidence included the `WorkerSourceTask` file and commit-related snippets, but not a full method-level dump of the `poll` implementation body. So I can anchor the commit behavior precisely, but any line-by-line claim about the exact `poll()` loop should be treated as incomplete unless you fetch the file directly.