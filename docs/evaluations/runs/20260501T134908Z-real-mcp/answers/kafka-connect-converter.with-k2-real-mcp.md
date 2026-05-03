**Recommendation**
Use the Kafka 4.2.0 Connect docs for the public contract, then anchor the implementation discussion in `ConnectorConfig.java`, because that is where `key.converter` and `value.converter` are defined and validated. For behavior-specific claims about actual conversion, K2 did not return the concrete `Converter` implementation, so do not infer beyond the config wiring.

**Implementation anchors**
- Public docs home for Kafka Connect 4.2.0: [https://kafka.apache.org/42/kafka-connect/]
- Version-pinned config reference for `key.converter` and `value.converter`: [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0002] and [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0047]
- Code anchor: `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/ConnectorConfig.java` [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/ConnectorConfig.java]

**Tests to inspect or add**
- Existing neighboring integration test: `connect/runtime/src/test/java/org/apache/kafka/connect/integration/ConnectorValidationIntegrationTest.java` [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ConnectorValidationIntegrationTest.java]
- Inspect the converter validation cases there, especially missing/invalid converter class coverage.
- Add or verify a regression test that separately exercises `key.converter` vs `value.converter` selection and ensures the worker does not cross-wire them.

**Citations**
- Kafka Connect 4.2 docs landing page: [https://kafka.apache.org/42/kafka-connect/]
- Config docs for `value.converter`: [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0040]
- Config docs for `key.converter`: [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0002]
- Config docs showing `key.converter.plugin.version` / `value.converter.plugin.version`: [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0047]
- Implementation anchor: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/ConnectorConfig.java]
- Neighboring test anchor: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ConnectorValidationIntegrationTest.java]

**Uncertainties**
- K2 evidence did not return the actual `org.apache.kafka.connect.storage.Converter` interface or a concrete converter class that directly demonstrates key-vs-value conversion behavior.
- The returned evidence is enough to anchor the config contract and validation path, but not enough to make exact claims about the conversion algorithm itself without a follow-up search.