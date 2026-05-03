**Recommendation**
Use the Kafka Connect 4.2.0 docs for `connector.client.config.override.policy` as the behavioral contract, then verify the `PrincipalConnectorClientConfigOverridePolicy` implementation and its sibling policy tests. The key question is whether the policy accepts only principal/auth-related overrides and rejects everything else; treat that as the baseline expectation unless the source shows a narrower allowlist.

**Implementation anchors**
- `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicy.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/ConnectorClientConfigOverridePolicy.java`
- If the class delegates validation helpers, inspect nearby code in the same package for shared allowlist logic or config-key filtering.

**Tests to inspect or add**
- `connect/runtime/src/test/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicyTest.java`
- Sibling policy tests in the same package, especially:
  - `AllConnectorClientConfigOverridePolicyTest.java`
  - `NoneConnectorClientConfigOverridePolicyTest.java`
- Add/confirm cases for:
  - accepted principal-only overrides
  - rejected non-principal overrides
  - empty input
  - mixed valid + invalid overrides
  - per-client behavior if producer/consumer/admin overrides are treated differently

**Citations**
- Kafka Connect 4.2.0 docs for `connector.client.config.override.policy`:
  - `https://kafka.apache.org/42/documentation.html#connectconfigs`
- Implementation:
  - `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicy.java`
- Tests:
  - `connect/runtime/src/test/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicyTest.java`

**Uncertainties**
- I’m not fully certain of the exact principal-override allowlist in 4.2.0 without opening the source.
- The public docs URL above is the version-pinned Kafka 4.2 docs anchor I’d use, but the exact generated page may differ by release packaging.