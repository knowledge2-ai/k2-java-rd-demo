**Recommendation**
Anchor the answer on the Flink 2.2.0 checkpointing docs, the `DefaultCheckpointPlanCalculator` implementation, and the direct unit test for that calculator. For behavior questions, the implementation and its test should be treated as primary; the docs are the semantic contract.

**Implementation anchors**
- Version-pinned docs: the Flink 2.2.0 checkpointing / fault-tolerance docs page for checkpointing behavior.
- Implementation class: `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointPlanCalculator.java`
- Supporting types in the same area: `CheckpointPlan`, `DefaultCheckpointPlan`, and `CheckpointPlanCalculator`

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointPlanCalculatorTest.java`
- Other same-package checkpoint-plan tests that exercise plan construction, alignment mode selection, subsumed/aborted checkpoint handling, and barrier-related edge cases
- Add a regression test for any newly identified branch in the default plan calculation path

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointPlanCalculator.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointPlanCalculatorTest.java`

**Uncertainties**
- I cannot verify the exact Flink 2.2.0 docs URL without repository or web access.
- I am confident about the calculator class path, but not fully certain about the complete set of neighboring test class names beyond the direct calculator test.