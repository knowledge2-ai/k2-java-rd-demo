**Recommendation**
Use the Kafka 4.2.0 Connect docs plus the `SinkRecord` API implementation as the primary anchors. For neighbor coverage, inspect `InternalSinkRecordTest` first; K2 did not surface a dedicated `SinkRecordTest`, so treat that gap explicitly.

**Implementation anchors**
- Version-pinned docs:
  - Kafka Connect landing page: [https://kafka.apache.org/42/kafka-connect/](https://kafka.apache.org/42/kafka-connect/)
  - Connector Development Guide: [https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0001](https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0001)
  - Kafka Connect config docs for sink-record logging context: [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0050](https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0050)
- Implementation class:
  - `SinkRecord` in the Kafka 4.2 branch: `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/sink/SinkRecord.java`
  - Related runtime wrapper: `repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/InternalSinkRecord.java`

**Tests to inspect or add**
- Existing neighboring test:
  - `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/InternalSinkRecordTest.java`
- Also inspect:
  - `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java`
  - `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ConnectorConfigTest.java`
- If you need direct coverage for sink metadata accessors, add a focused `SinkRecord` unit test because K2 did not return one.

**Citations**
- [https://kafka.apache.org/42/kafka-connect/](https://kafka.apache.org/42/kafka-connect/)
- [https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0001](https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0001)
- [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0050](https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0050)
- `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/sink/SinkRecord.java`
- `repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/InternalSinkRecord.java`
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/InternalSinkRecordTest.java`
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java`
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ConnectorConfigTest.java`

**Uncertainties**
- K2 did not surface a dedicated `SinkRecordTest`, so test coverage for the public `SinkRecord` API may be indirect.
- The returned code excerpt confirms the implementation location and class hierarchy, but not the full accessor list in the visible snippet; verify the full file if you need an exhaustive metadata-field inventory.