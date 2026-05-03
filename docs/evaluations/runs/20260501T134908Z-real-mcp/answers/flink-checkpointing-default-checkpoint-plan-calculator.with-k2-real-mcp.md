**Recommendation**
Anchor the explanation on the version-pinned Flink 2.2.0 docs plus the concrete runtime class:
- Docs: the 2.2.0 checkpointing pages for user-facing context, especially [Checkpoints](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001) and [Checkpointing](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001).
- Implementation: [DefaultCheckpointPlanCalculator](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointPlanCalculator.java), which K2 identifies as implementing `CheckpointPlanCalculator`.
- Tests: start with [DefaultCheckpointPlanCalculatorTest](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointPlanCalculatorTest.java), since it is the direct declarative test for the class.

**Implementation anchors**
- [DefaultCheckpointPlanCalculator](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointPlanCalculator.java)  
  K2 marks this as the 2.2.0 implementation class and says it implements `CheckpointPlanCalculator`.
- [CheckpointPlanCalculator](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointPlanCalculator.java)  
  Use this as the interface/context anchor for the plan-calculation contract.
- [Checkpoints docs](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001)  
  Version-pinned user docs for checkpoint behavior.
- [Checkpointing docs](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001)  
  Version-pinned developer docs for checkpointing semantics.
- [State backends docs](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001)  
  Useful if the answer needs to connect plan calculation to backend/storage behavior.

**Tests to inspect or add**
- [DefaultCheckpointPlanCalculatorTest](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointPlanCalculatorTest.java)  
  Direct test coverage for the calculator; K2 shows it contains declarative scenarios such as all-running and not-running task cases.
- [TestSubtaskCheckpointCoordinator](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/streaming/runtime/tasks/TestSubtaskCheckpointCoordinator.java)  
  Not direct coverage of the calculator, but adjacent checkpoint coordination test infrastructure surfaced by K2.
- If you need to add coverage, add cases around plan calculation edge conditions already implied by the existing test style: non-running vertices, mixed source/non-source vertices, and plan failure paths.

**Citations**
- [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001)
- [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/#part-0001)
- [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointPlanCalculator.java](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointPlanCalculator.java)
- [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointPlanCalculatorTest.java](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointPlanCalculatorTest.java)
- [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/streaming/runtime/tasks/TestSubtaskCheckpointCoordinator.java](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/streaming/runtime/tasks/TestSubtaskCheckpointCoordinator.java)

**Uncertainties**
- K2 evidence confirms the direct class and direct test, but it does not expose the full method-level behavior of `DefaultCheckpointPlanCalculator` in the returned snippet.
- The “neighboring tests” signal is partial: `DefaultCheckpointPlanCalculatorTest` is the only direct adjacent test class clearly tied to the calculator; the other surfaced checkpointing tests are nearby, not proven as direct coverage for this class.