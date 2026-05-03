**Recommendation**
Anchor the answer on the release-2.2.0 docs for checkpoints/state backends, then ground the behavior in `CheckpointResourcesCleanupRunner` itself and its direct test. The K2 evidence supports `CheckpointResourcesCleanupRunner` as the implementation class and `CheckpointResourcesCleanupRunnerTest` as the primary neighboring test; it also surfaced related checkpointing tests in the same module for context. [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001] [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001] [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/dispatcher/cleanup/CheckpointResourcesCleanupRunner.java] [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/dispatcher/cleanup/CheckpointResourcesCleanupRunnerTest.java]

**Implementation anchors**
- Version-pinned docs:
  - `Checkpoints` docs for 2.2.0. [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
  - `State Backends` docs for 2.2.0. [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001]
  - `Release Notes - Flink 2.0` if you need historical checkpointing behavior changes that can inform cleanup semantics. [https://nightlies.apache.org/flink/flink-docs-release-2.2/release-notes/flink-2.0/#part-0001]
- Implementation class:
  - `flink-runtime/src/main/java/org/apache/flink/runtime/dispatcher/cleanup/CheckpointResourcesCleanupRunner.java`
  - K2 identifies it as `org.apache.flink.runtime.dispatcher.cleanup.CheckpointResourcesCleanupRunner` and notes it implements `JobManagerRunner`. [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/dispatcher/cleanup/CheckpointResourcesCleanupRunner.java]
- Companion factory:
  - `CheckpointResourcesCleanupRunnerFactory.java` is the direct construction path to inspect alongside the runner. [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/dispatcher/cleanup/CheckpointResourcesCleanupRunnerFactory.java]

**Tests to inspect or add**
- Direct neighbor test:
  - `flink-runtime/src/test/java/org/apache/flink/runtime/dispatcher/cleanup/CheckpointResourcesCleanupRunnerTest.java` is the primary test anchor surfaced by K2. [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/dispatcher/cleanup/CheckpointResourcesCleanupRunnerTest.java]
- Nearby checkpointing tests K2 surfaced as adjacent context:
  - `CheckpointCoordinatorMasterHooksTest.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorMasterHooksTest.java]
  - `TestingCompletedCheckpointStore.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/TestingCompletedCheckpointStore.java]
  - `TestingCheckpointIDCounter.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/TestingCheckpointIDCounter.java]
- If you are adding coverage, prefer a focused regression test in `CheckpointResourcesCleanupRunnerTest` for cleanup success/failure and idempotency semantics; K2 did not return method-level behavior details, so that exact test shape is not fully evidenced here.

**Citations**
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001] [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001] [https://nightlies.apache.org/flink/flink-docs-release-2.2/release-notes/flink-2.0/#part-0001]
- Implementation: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/dispatcher/cleanup/CheckpointResourcesCleanupRunner.java] [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/dispatcher/cleanup/CheckpointResourcesCleanupRunnerFactory.java]
- Tests: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/dispatcher/cleanup/CheckpointResourcesCleanupRunnerTest.java] [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorMasterHooksTest.java] [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/TestingCompletedCheckpointStore.java] [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/TestingCheckpointIDCounter.java]

**Uncertainties**
- The K2 evidence is enough to anchor the relevant files, but it did not return the exact cleanup algorithm or method-level assertions for `CheckpointResourcesCleanupRunner`, so I’m not inferring those details.
- The docs returned are general checkpoint/state docs, not a runner-specific design note; if you need runner-specific semantics, the test file and implementation file are the authoritative anchors from this evidence set.