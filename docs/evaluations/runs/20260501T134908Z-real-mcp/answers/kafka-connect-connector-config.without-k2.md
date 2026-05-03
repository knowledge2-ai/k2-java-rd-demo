**Recommendation**
Anchor the explanation on `ConnectorConfig` as the shared base validator for connector-level settings in Kafka Connect 4.2.0: it validates the common connector configuration surface once, and connector-specific rules should stay in the connector’s own config definition or herder-side validation. If you are documenting this, describe it as “shared base validation” rather than source- or sink-only logic.

**Implementation anchors**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/ConnectorConfig.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/AbstractHerder.java` if you want the call path that consumes the validation result

**Tests to inspect or add**
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ConnectorConfigTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/standalone/StandaloneHerderTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/distributed/DistributedHerderTest.java`

Add or tighten a regression test in `ConnectorConfigTest` for the shared validation rule, then verify the same behavior is surfaced end-to-end in one herder test.

**Citations**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/ConnectorConfig.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ConnectorConfigTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/standalone/StandaloneHerderTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/distributed/DistributedHerderTest.java`

**Uncertainties**
- I am not confident about the exact published 4.2.0 docs URL without checking, so I am not giving a precise documentation link.
- I am also not fully certain whether the validation is enforced directly in `ConnectorConfig` only or is split between `ConnectorConfig` and herder-side validation in the 4.2.0 branch; the class above is still the right anchor point.