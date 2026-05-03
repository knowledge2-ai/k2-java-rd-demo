**Recommendation**
- Anchor the explanation on the 2.2.0 checkpointing docs for behavior, then trace into `CheckpointPlanCalculator` as the class that decides the checkpoint participant set and plan shape.
- Keep the distinction clear: this class calculates the plan; it does not execute the snapshot itself.

**Implementation anchors**
- Version-pinned docs: the Flink 2.2.0 checkpointing guide page for DataStream fault tolerance. I would use the release-2.2 checkpointing doc page as the behavioral reference.
- Core implementation: `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointPlanCalculator.java`
- Adjacent runtime types worth reading alongside it: `CheckpointPlan`, `DefaultCheckpointPlan`, and the coordinator path that consumes the resulting plan.

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointPlanCalculatorTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java`
- If present in the same package, any `DefaultCheckpointPlan` tests that validate the calculator’s output contract.
- Add or extend coverage for:
  - all subtasks running normally
  - partially finished/terminated subtasks
  - any invalid or declined plan path

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointPlanCalculator.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointPlanCalculatorTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java`

**Uncertainties**
- I am confident about the runtime class and the nearby test locations, but I did not verify the exact 2.2.0 docs URL here.
- If you want a fully pinned docs citation, the exact release-site path should be checked against the Flink 2.2.0 documentation build.