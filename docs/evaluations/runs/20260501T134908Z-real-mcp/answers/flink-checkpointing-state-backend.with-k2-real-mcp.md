**Recommendation**
Use `StateBackend` as the primary implementation anchor for checkpointing semantics in Flink 2.2.0. The state backend is responsible for creating keyed and operator state backends and defining how that state is checkpointed, often by writing raw bytes through `CheckpointStreamFactory`; the docs frame this as persisting managed state so recovery can restore state and stream positions consistently [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/StateBackend.java], [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001], [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001].

**Implementation anchors**
- `flink-runtime/src/main/java/org/apache/flink/runtime/state/StateBackend.java` is the core contract for checkpointing responsibilities [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/StateBackend.java].
- `flink-runtime/src/main/java/org/apache/flink/runtime/state/AbstractStateBackend.java` is the legacy base class, but it is currently just a compatibility shell over `StateBackend` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/AbstractStateBackend.java].
- `flink-runtime/src/main/java/org/apache/flink/streaming/api/operators/sorted/state/BatchExecutionStateBackend.java` is a concrete implementation that shows how a backend wires keyed/operator state creation in practice [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/streaming/api/operators/sorted/state/BatchExecutionStateBackend.java].

**Tests to inspect or add**
- Inspect `flink-runtime/src/test/java/org/apache/flink/streaming/util/StateBackendUtils.java` for existing backend configuration helpers and patterns around state backend selection in tests [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/streaming/util/StateBackendUtils.java].
- K2 did not surface a dedicated `StateBackendTest` or similarly named direct regression test for `StateBackend` in 2.2.0, so the evidence is incomplete on the exact nearest test class set.
- If you need stronger coverage, add a focused test around `StateBackend#createKeyedStateBackend` and `createOperatorStateBackend` behavior, especially verifying checkpoint-related behavior for a backend that writes raw checkpoint bytes versus one that delegates storage elsewhere.

**Citations**
- [State backends docs](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/#part-0001)
- [Checkpoint docs](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/checkpoints/#part-0001)
- [StateBackend.java](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/StateBackend.java)
- [AbstractStateBackend.java](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/AbstractStateBackend.java)
- [BatchExecutionStateBackend.java](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/streaming/api/operators/sorted/state/BatchExecutionStateBackend.java)
- [StateBackendUtils.java](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/streaming/util/StateBackendUtils.java)

**Uncertainties**
- The K2 evidence is enough to anchor the contract and docs, but it does not expose the full surrounding test matrix for `StateBackend` in 2.2.0.
- I did not get a direct test class specifically named for `StateBackend`, so the exact “neighboring tests” beyond `StateBackendUtils` may need a second pass if you want exhaustive coverage.