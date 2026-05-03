**Recommendation**
Use the 4.2-pinned Kafka Connect docs plus the `Struct` implementation as the primary anchors, and treat the absence of a surfaced `Struct`-specific test as a gap to verify in-repo.

**Implementation anchors**
- Kafka Connect 4.2 overview for the versioned Connect entry point: [https://kafka.apache.org/42/kafka-connect/](https://kafka.apache.org/42/kafka-connect/)
- Connector Development Guide section that explicitly introduces `Schema` and `Struct` for structured records: [https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0021](https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0021)
- Connect API docs landing page for the versioned API surface: [https://kafka.apache.org/42/apis/#part-0003](https://kafka.apache.org/42/apis/#part-0003)
- Implementation class to inspect: `org.apache.kafka.connect.data.Struct` at `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/data/Struct.java`
- Adjacent data-validation helper surfaced by K2: `SchemaBuilder.field(...)` in `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/data/SchemaBuilder.java`

**Tests to inspect or add**
- Existing Connect test anchor surfaced by K2: `ConnectorValidationIntegrationTest` at `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ConnectorValidationIntegrationTest.java`
- Another nearby Connect integration test surfaced by K2: `ExactlyOnceSourceIntegrationTest` at `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java`
- Add or locate a focused unit test class for `Struct` validation if one exists but was not surfaced by K2; the returned evidence did not include a direct `Struct`-specific test file.

**Citations**
- Docs: [https://kafka.apache.org/42/kafka-connect/](https://kafka.apache.org/42/kafka-connect/), [https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0021](https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0021), [https://kafka.apache.org/42/apis/#part-0003](https://kafka.apache.org/42/apis/#part-0003)
- Code: `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/data/Struct.java`, `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/data/SchemaBuilder.java`
- Tests: `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ConnectorValidationIntegrationTest.java`, `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java`

**Uncertainties**
- K2 did not surface a `Struct`-specific test class or method-level validation assertions, so I cannot claim the exact neighboring unit tests without guessing.
- The evidence supports `Struct` as the implementation anchor, but the precise validation behavior should be confirmed directly in that file if you need method-level claims.