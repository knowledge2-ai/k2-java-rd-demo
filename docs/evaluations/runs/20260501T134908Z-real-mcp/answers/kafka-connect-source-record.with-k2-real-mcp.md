**Recommendation**
Use the 4.2-pinned Kafka Connect docs to frame the API contract, then anchor implementation details in `SourceRecord` itself. The key behavior to verify is that `SourceRecord.newRecord(...)` preserves `sourcePartition` and `sourceOffset` when constructing a new record, while also carrying topic, Kafka partition, schema/value, timestamp, and headers [https://kafka.apache.org/42/kafka-connect/] [https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0001] [repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/source/SourceRecord.java].

**Implementation anchors**
- Public, version-pinned docs:
  - Kafka Connect landing page for 4.2.0 [https://kafka.apache.org/42/kafka-connect/]
  - Connector Development Guide for 4.2.0 [https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0001]
  - Kafka API page pointing to Connect javadocs [https://kafka.apache.org/42/apis/#part-0003]
- Implementation class:
  - `connect/api/src/main/java/org/apache/kafka/connect/source/SourceRecord.java` [repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/source/SourceRecord.java]
- Code path to cite:
  - `newRecord(... headers)` delegates to the `SourceRecord(sourcePartition, sourceOffset, topic, kafkaPartition, ...)` constructor, so partition metadata is not recomputed or dropped at that layer [repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/source/SourceRecord.java]

**Tests to inspect or add**
- Inspect neighboring source-connect tests that may exercise the same record/offset flow:
  - `connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java` [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java]
  - `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/SamplePredicate.java` as a nearby `Predicate<SourceRecord>` helper used in source-side runtime tests [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/SamplePredicate.java]
- Add or look for a focused unit test that asserts:
  - `sourcePartition` is preserved through `newRecord(...)`
  - `sourceOffset` is preserved through `newRecord(...)`
  - `kafkaPartition` is set only on the emitted record, not conflated with source partition metadata

**Citations**
- Docs: [https://kafka.apache.org/42/kafka-connect/]
- Docs: [https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0001]
- Docs: [https://kafka.apache.org/42/apis/#part-0003]
- Implementation: [repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/source/SourceRecord.java]
- Neighboring tests/helpers: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java], [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/SamplePredicate.java]

**Uncertainties**
- K2 did not surface a dedicated `SourceRecordTest` or a direct unit test specifically asserting partition-metadata preservation, so I would not claim one exists.
- The evidence is enough to anchor the implementation claim, but not enough to prove the full surrounding test coverage for `SourceRecord` construction.