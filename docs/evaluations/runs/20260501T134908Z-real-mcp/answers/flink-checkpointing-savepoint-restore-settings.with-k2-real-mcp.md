**Recommendation**
Use `SavepointRestoreSettings` as the job-graph-level switch for upgrade restores: it stores the savepoint path plus whether non-restored state is allowed, and `DefaultExecutionGraphFactory` consumes it when checkpointing is enabled to restore an `ExecutionGraph` from a savepoint [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/jobgraph/SavepointRestoreSettings.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/scheduler/DefaultExecutionGraphFactory.java]. For upgrade guidance, anchor the explanation in Flink 2.2.0’s version-pinned checkpoints and state-backends docs, plus the 2.0 release notes upgrade section [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001], [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001], [https://nightlies.apache.org/flink/flink-docs-release-2.2/release-notes/flink-2.0/#part-0001].

**Implementation anchors**
- `flink-runtime/src/main/java/org/apache/flink/runtime/jobgraph/SavepointRestoreSettings.java` is the implementation class to describe the restore settings API and its serialization shape [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/jobgraph/SavepointRestoreSettings.java].
- `flink-runtime/src/main/java/org/apache/flink/runtime/scheduler/DefaultExecutionGraphFactory.java` is where those settings are actually applied during job graph creation and savepoint restore [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/scheduler/DefaultExecutionGraphFactory.java].

**Tests to inspect or add**
- Inspect `flink-runtime/src/test/java/org/apache/flink/runtime/jobgraph/SavepointRestoreSettingsTest.java` for constructor/factory behavior and any serialization or validation expectations [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/jobgraph/SavepointRestoreSettingsTest.java].
- Inspect `flink-runtime/src/test/java/org/apache/flink/runtime/scheduler/DefaultExecutionGraphFactoryTest.java` for upgrade-path behavior; it already builds a job graph with `SavepointRestoreSettings.forPath(..., allowNonRestoredState)` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/scheduler/DefaultExecutionGraphFactoryTest.java].
- If you add coverage, prefer a test that asserts upgrade restore behavior with and without `allowNonRestoredState`, since that is the key operational toggle surfaced by the class and used by the scheduler [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/jobgraph/SavepointRestoreSettingsTest.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/scheduler/DefaultExecutionGraphFactoryTest.java].

**Citations**
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001]
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001]
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/release-notes/flink-2.0/#part-0001]
- Implementation: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/jobgraph/SavepointRestoreSettings.java]
- Execution path: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/scheduler/DefaultExecutionGraphFactory.java]
- Neighbor test: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/jobgraph/SavepointRestoreSettingsTest.java]
- Neighbor test: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/scheduler/DefaultExecutionGraphFactoryTest.java]

**Uncertainties**
- The K2 evidence did not surface a dedicated 2.2.0 doc page specifically for `SavepointRestoreSettings`; the strongest anchors are the general checkpoints/state-backends docs and the upgrade-related release notes.
- I did not verify the full method-level surface of `SavepointRestoreSettings` beyond the evidence returned here, so if you need exact factory methods or defaults, that should be confirmed directly from the class.