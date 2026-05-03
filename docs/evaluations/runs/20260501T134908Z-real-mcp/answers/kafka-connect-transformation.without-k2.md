**Recommendation**
- Anchor the answer on the 4.2.0 Connect SMT docs and the runtime SMT chain, not on built-in transform examples.
- Treat `Transformation.apply(record)` as a per-record contract, so any behavior claim should be framed as single-record, not batch, processing.

**Implementation anchors**
- Version-pinned docs: `https://kafka.apache.org/42/documentation.html#connect_transforms`
- Core interface: `connect/api/src/main/java/org/apache/kafka/connect/transforms/Transformation.java`
- Runtime application path: `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/TransformationChain.java`
- If predicates / stage ordering matter, also inspect the adjacent runtime stage code in the same package.

**Tests to inspect or add**
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/TransformationChainTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSourceTaskTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSinkTaskTest.java`
- Add or extend coverage for:
  - transform ordering
  - null-record short-circuit behavior
  - exception propagation and tolerance handling
  - source vs sink wiring consistency

**Citations**
- Apache Kafka 4.2.0 Connect docs: `https://kafka.apache.org/42/documentation.html#connect_transforms`
- `connect/api/src/main/java/org/apache/kafka/connect/transforms/Transformation.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/TransformationChain.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/TransformationChainTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSourceTaskTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSinkTaskTest.java`

**Uncertainties**
- I’m confident about the versioned docs page and the main runtime class, but the exact SMT section fragment on the 4.2.0 docs site may differ slightly.
- The task-level test files above are the right neighborhoods to inspect, but I’m less certain they are the only or closest tests in every 4.2.0 branch layout.