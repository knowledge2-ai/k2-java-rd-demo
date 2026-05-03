**Recommendation**
Anchor the behavior on the 4.2.0 Connect docs for `connector.client.config.override.policy` and on the shared base implementation in `AbstractConnectorClientConfigOverridePolicy`. The behavior should be read as: the abstract policy owns the common validation path, while concrete policies decide which client config overrides are permitted.

**Implementation anchors**
- Version-pinned docs: Kafka 4.2.0 Connect worker config docs for `connector.client.config.override.policy`.
- Shared implementation: `org.apache.kafka.connect.connector.policy.AbstractConnectorClientConfigOverridePolicy`.
- Nearby concrete policies to read alongside it:
  - `AllConnectorClientConfigOverridePolicy`
  - `PrincipalConnectorClientConfigOverridePolicy`
  - `NoneConnectorClientConfigOverridePolicy`

**Tests to inspect or add**
- Existing unit tests in the same policy package for:
  - `AbstractConnectorClientConfigOverridePolicy`
  - the concrete policy subclasses above
- Connector/worker config wiring tests that prove the configured override policy is actually enforced end-to-end.
- Add regression coverage for:
  - shared overrides accepted by allowed policies
  - shared overrides rejected by disallowing policies
  - consistent validation/error messages across policy subclasses

**Citations**
- Kafka 4.2.0 Connect docs: `https://kafka.apache.org/42/documentation/#connectconfigs_connector.client.config.override.policy`
- Javadoc for the shared class: `https://kafka.apache.org/42/javadoc/org/apache/kafka/connect/connector/policy/AbstractConnectorClientConfigOverridePolicy.html`
- Javadoc for the policy interface: `https://kafka.apache.org/42/javadoc/org/apache/kafka/connect/connector/policy/ConnectorClientConfigOverridePolicy.html`

**Uncertainties**
- I’m not fully certain of the exact 4.2.0 test class names without checking the source tree, but they should be the policy tests in the same package plus the worker/config wiring tests that exercise the policy end-to-end.