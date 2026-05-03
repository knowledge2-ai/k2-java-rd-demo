**Recommendation**
Anchor the answer on the 4.2-pinned Kafka Connect user guide/security docs plus the 4.2 implementation and its dedicated policy test. The policy is deprecated in 4.2 and is the principal-only override path for SASL-related client configs, so the answer should frame it as a legacy/compatibility mechanism rather than the preferred option.

**Implementation anchors**
- Version-pinned docs:
  - Kafka Connect guide root for 4.2: [https://kafka.apache.org/42/kafka-connect/](https://kafka.apache.org/42/kafka-connect/)
  - Connect user guide security section mentioning connector client config overrides: [https://kafka.apache.org/42/kafka-connect/user-guide/#part-0041](https://kafka.apache.org/42/kafka-connect/user-guide/#part-0041)
  - Connect config reference: [https://kafka.apache.org/42/configuration/kafka-connect-configs/](https://kafka.apache.org/42/configuration/kafka-connect-configs/)
- Implementation class:
  - `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicy.java` (`repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicy.java`)
  - K2 evidence shows it is `@Deprecated(since = " 4.2", forRemoval = true)` and its allowlist is the SASL trio: `SASL_JAAS_CONFIG`, `SASL_MECHANISM`, and `SECURITY_PROTOCOL_CONFIG` (`repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicy.java`)
- Neighboring runtime anchor:
  - `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/AbstractConnectorClientConfigOverridePolicy.java` (`repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/AbstractConnectorClientConfigOverridePolicy.java`)
  - This shows validation is implemented by mapping each client prop to a `ConfigValue` and delegating to `validate(...)`, which is the right adjacent code for behavior context.

**Tests to inspect or add**
- Existing focused test:
  - `connect/runtime/src/test/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicyTest.java` (`repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicyTest.java`)
  - K2 shows it extends `BaseConnectorClientConfigOverridePolicyTest`, so that base class is the key neighboring test fixture to inspect for shared expectations.
- Also inspect/add:
  - `connect/runtime/src/test/java/org/apache/kafka/connect/connector/policy/BaseConnectorClientConfigOverridePolicyTest.java` if you need the shared assertion matrix for allowed vs disallowed client overrides.
  - If the current test does not explicitly pin the “principal-only” behavior, add a regression case that asserts only the SASL-related configs are accepted and non-SASL overrides are rejected.

**Citations**
- Docs root: [https://kafka.apache.org/42/kafka-connect/](https://kafka.apache.org/42/kafka-connect/)
- User guide security section: [https://kafka.apache.org/42/kafka-connect/user-guide/#part-0041](https://kafka.apache.org/42/kafka-connect/user-guide/#part-0041)
- Config reference: [https://kafka.apache.org/42/configuration/kafka-connect-configs/](https://kafka.apache.org/42/configuration/kafka-connect-configs/)
- Implementation: `repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicy.java`
- Adjacent abstract policy: `repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/AbstractConnectorClientConfigOverridePolicy.java`
- Dedicated test: `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicyTest.java`

**Uncertainties**
- K2 surfaced the class and test locations, but not the full body of `PrincipalConnectorClientConfigOverridePolicyTest` or `BaseConnectorClientConfigOverridePolicyTest`, so I cannot cite exact assertion names or edge-case coverage from the tests themselves.
- The evidence snippet for the implementation was truncated before the full `validate` method, so I’m only stating the allowlist and deprecation details that were visible in K2 output.