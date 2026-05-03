**Recommendation**
`NoneConnectorClientConfigOverridePolicy` should be treated as a hard deny-list policy: if the connector supplies any client config overrides, validation should fail; if the override map is empty, validation should succeed. The important behavioral point is that it rejects the entire override set rather than selectively allowing keys.

**Implementation anchors**
- Version-pinned docs: Apache Kafka 4.2.0 documentation page for Kafka Connect client config override policies, at `https://kafka.apache.org/42/documentation/`
- Implementation class: `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/NoneConnectorClientConfigOverridePolicy.java`
- Nearby policy classes to compare behavior against:
  - `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/AllConnectorClientConfigOverridePolicy.java`
  - `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicy.java`

**Tests to inspect or add**
- Inspect the policy unit tests in `connect/runtime/src/test/java/org/apache/kafka/connect/connector/policy/`
- Anchor against the `NoneConnectorClientConfigOverridePolicy` test class, plus the sibling policy tests for `All` and `Principal`
- If coverage is missing, add a test that:
  - passes an empty override map and expects validation success
  - passes one or more overrides and expects validation failure for the full set

**Citations**
- `https://kafka.apache.org/42/documentation/`
- `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/NoneConnectorClientConfigOverridePolicy.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/AllConnectorClientConfigOverridePolicy.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicy.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/connector/policy/`

**Uncertainties**
- I’m confident about the policy behavior and implementation location.
- I’m less certain about the exact 4.2.0 doc anchor fragment and the exact unit-test filenames without checking the source tree, so I’ve cited the stable page and package path instead of guessing a brittle class name.