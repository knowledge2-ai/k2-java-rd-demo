**Recommendation**
Anchor the answer on the 4.2.0 Connect converter contract, then back it with one concrete implementation and the task-level call sites that actually separate key from value handling. The important behavior is the `isKey` split in `configure(...)`, plus the fact that key and value are converted through distinct converter instances.

**Implementation anchors**
- `connect/api/src/main/java/org/apache/kafka/connect/storage/Converter.java`
- Representative concrete implementation: `connect/json/src/main/java/org/apache/kafka/connect/json/JsonConverter.java`
- End-to-end flow: `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSourceTask.java`
- End-to-end flow: `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSinkTask.java`

**Tests to inspect or add**
- Neighboring converter tests under `connect/api/src/test/java/org/apache/kafka/connect/storage/`, especially `StringConverterTest` and `ByteArrayConverterTest`
- `connect/json/src/test/java/org/apache/kafka/connect/json/JsonConverterTest.java`
- Runtime integration tests around the conversion boundary:
  - `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSourceTaskTest.java`
  - `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSinkTaskTest.java`
- Add/adjust coverage for:
  - `configure(..., true)` vs `configure(..., false)` isolation
  - key/value round-trip independence
  - null and schema-preserving behavior for each side

**Citations**
- Apache Kafka 4.2.0 docs: `https://kafka.apache.org/42/documentation/`
- `connect/api/src/main/java/org/apache/kafka/connect/storage/Converter.java`
- `connect/json/src/main/java/org/apache/kafka/connect/json/JsonConverter.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSourceTask.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSinkTask.java`
- `connect/api/src/test/java/org/apache/kafka/connect/storage/StringConverterTest.java`
- `connect/api/src/test/java/org/apache/kafka/connect/storage/ByteArrayConverterTest.java`
- `connect/json/src/test/java/org/apache/kafka/connect/json/JsonConverterTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSourceTaskTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSinkTaskTest.java`

**Uncertainties**
- I’m confident about the contract and the worker call sites, but not every exact neighboring test class name in 4.2.0 without checking the tree.
- If you need a strictly version-pinned doc fragment, the exact section anchor may differ; the stable top-level docs URL above is the safest public path.