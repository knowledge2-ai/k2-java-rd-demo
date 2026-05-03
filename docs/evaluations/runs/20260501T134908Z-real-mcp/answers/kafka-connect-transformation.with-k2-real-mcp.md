**Recommendation**
Use the 4.2-pinned Kafka Connect docs for high-level contract, then anchor the behavior discussion on the `Transformation` SPI itself and the Connect runtime tests that exercise transform wiring. The K2 evidence does not include a direct 4.2.0 Javadoc page for `Transformation`, so any claim about single-message transform semantics should be tied back to the interface source and treated as incomplete if it needs exact lifecycle wording.

**Implementation anchors**
- Version-pinned docs:
  - Kafka Connect overview: [https://kafka.apache.org/42/kafka-connect/](https://kafka.apache.org/42/kafka-connect/)
  - Connector Development Guide: [https://kafka.apache.org/42/kafka-connect/connector-development-guide/](https://kafka.apache.org/42/kafka-connect/connector-development-guide/)
  - The Connect user guide explicitly lists `org.apache.kafka.connect.transforms.Transformation` as an expected plugin type: [https://kafka.apache.org/42/kafka-connect/user-guide/#part-0040](https://kafka.apache.org/42/kafka-connect/user-guide/#part-0040)
- Implementation class / SPI:
  - `org.apache.kafka.connect.transforms.Transformation` in `connect/api/src/main/java/org/apache/kafka/connect/transforms/Transformation.java` is the interface to anchor single-message transform behavior: [repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/transforms/Transformation.java]
- Nearby transform code for context:
  - `Filter`: [repo://apache/kafka@4.2/connect/transforms/src/main/java/org/apache/kafka/connect/transforms/Filter.java]
  - `RegexRouter`: [repo://apache/kafka@4.2/connect/transforms/src/main/java/org/apache/kafka/connect/transforms/RegexRouter.java]
  - `RecordIsTombstone` predicate nearby in the same transforms area: [repo://apache/kafka@4.2/connect/transforms/src/main/java/org/apache/kafka/connect/transforms/predicates/RecordIsTombstone.java]

**Tests to inspect or add**
- Inspect:
  - `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/TransformationConfigTest.java` for transform configuration composition and connector config interaction: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/TransformationConfigTest.java]
  - `connect/runtime/src/test/java/org/apache/kafka/connect/integration/ConnectorValidationIntegrationTest.java` for duplicate transformation validation and runtime wiring: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ConnectorValidationIntegrationTest.java]
- Add if missing:
  - A focused unit test around `Transformation.apply(...)` semantics for one record at a time, especially null/tombstone handling and record immutability.
  - A regression test covering transform chaining order and failure propagation if that behavior matters for your change.

**Citations**
- Kafka Connect 4.2 docs: [https://kafka.apache.org/42/kafka-connect/](https://kafka.apache.org/42/kafka-connect/)
- Connector Development Guide 4.2: [https://kafka.apache.org/42/kafka-connect/connector-development-guide/](https://kafka.apache.org/42/kafka-connect/connector-development-guide/)
- User guide plugin types including `Transformation`: [https://kafka.apache.org/42/kafka-connect/user-guide/#part-0040](https://kafka.apache.org/42/kafka-connect/user-guide/#part-0040)
- `Transformation` interface source: [repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/transforms/Transformation.java]
- `TransformationConfigTest`: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/TransformationConfigTest.java]
- `ConnectorValidationIntegrationTest`: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ConnectorValidationIntegrationTest.java]

**Uncertainties**
- The K2 evidence did not return the `Transformation` Javadoc or an implementation class beyond the interface, so I cannot cite exact single-message lifecycle wording from docs.
- The evidence also did not surface a direct unit test that exercises `Transformation.apply()` end-to-end; the neighboring tests only cover config validation and connector wiring.