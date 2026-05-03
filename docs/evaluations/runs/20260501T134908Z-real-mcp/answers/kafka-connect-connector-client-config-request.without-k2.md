**Recommendation**
Anchor the answer on the Kafka 4.2.0 Connect config docs for `connector.client.config.override.policy`, then tie it back to the `ConnectorClientConfigRequest` API and the built-in override-policy implementations. The important point is that the policy is evaluated from request metadata plus the candidate client config map, not from worker runtime state.

**Implementation anchors**
- `docs/connect.html` for the version-pinned Connect configuration docs section covering `connector.client.config.override.policy`
- `connect/api/src/main/java/org/apache/kafka/connect/connector/policy/ConnectorClientConfigRequest.java`
- `connect/api/src/main/java/org/apache/kafka/connect/connector/policy/ConnectorClientConfigOverridePolicy.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/AllConnectorClientConfigOverridePolicy.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/NoneConnectorClientConfigOverridePolicy.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicy.java`

**Tests to inspect or add**
- `connect/api/src/test/java/org/apache/kafka/connect/connector/policy/ConnectorClientConfigRequestTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/connector/policy/AllConnectorClientConfigOverridePolicyTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/connector/policy/NoneConnectorClientConfigOverridePolicyTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicyTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ConnectorConfigTest.java` for wiring of the policy config
- If needed, add a focused test that asserts the request passed into `validate(...)` contains the connector identity/type and the exact client config overrides you expect

**Citations**
- `docs/connect.html`
- `connect/api/src/main/java/org/apache/kafka/connect/connector/policy/ConnectorClientConfigRequest.java`
- `connect/api/src/main/java/org/apache/kafka/connect/connector/policy/ConnectorClientConfigOverridePolicy.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/AllConnectorClientConfigOverridePolicy.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/NoneConnectorClientConfigOverridePolicy.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicy.java`

**Uncertainties**
- I’m not fully certain of the exact 4.2.0 `ConnectorClientConfigRequest` field list from memory, so I would not overstate the request schema beyond “request metadata + candidate client config map.”
- The exact doc anchor inside `docs/connect.html` may differ, but that file is the right version-pinned starting point.