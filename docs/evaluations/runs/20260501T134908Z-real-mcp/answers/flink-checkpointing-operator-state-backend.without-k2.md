**Recommendation**
- Treat `OperatorStateBackend` as the checkpoint contract for **non-keyed, operator-scoped state**.
- Its responsibilities are to:
  - register and own operator state entries
  - snapshot that state into checkpointed handles
  - restore state on recovery
  - clean up/dispose state on close
- For Flink 2.2.0, anchor the behavior in the **runtime implementation**, not the interface alone.

**Implementation anchors**
- Version-pinned docs:
  - `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/`
  - `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/`
- Implementation class:
  - `flink-runtime/src/main/java/org/apache/flink/runtime/state/OperatorStateBackend.java`
  - `flink-runtime/src/main/java/org/apache/flink/runtime/state/DefaultOperatorStateBackend.java`
- Related runtime types to read alongside it:
  - `OperatorStateStore`
  - `OperatorStateHandle`
  - `OperatorSubtaskState`

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/state/DefaultOperatorStateBackendTest.java`
- Neighboring state checkpoint/restore tests in the same package, especially for:
  - `OperatorStateHandle`
  - `OperatorSubtaskState`
- Add or verify coverage for:
  - snapshot and restore of partitionable list state
  - union/list state redistribution semantics
  - empty-state checkpoints
  - duplicate state registration / illegal lifecycle transitions

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/state/OperatorStateBackend.java`
- `flink-runtime/src/main/java/org/apache/flink/runtime/state/DefaultOperatorStateBackend.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/state/DefaultOperatorStateBackendTest.java`
- `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/`
- `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/`

**Uncertainties**
- I did not live-verify the 2.2.0 docs permalink, so treat the URL as the best-known release anchor.
- If your 2.2.0 tree has a renamed or split backend implementation, the safe anchor is still the `org.apache.flink.runtime.state` runtime backend path.
- I’m confident about `DefaultOperatorStateBackendTest` as the primary neighbor, but I’m not asserting the full exact set of adjacent test filenames without tree verification.