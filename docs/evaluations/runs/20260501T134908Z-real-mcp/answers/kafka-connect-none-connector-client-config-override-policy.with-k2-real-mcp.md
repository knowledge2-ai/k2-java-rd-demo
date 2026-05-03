**Recommendation**
Use the 4.2-pinned Kafka Connect docs as the public anchor, then validate behavior in `NoneConnectorClientConfigOverridePolicy` and its base test class. For the “overrides not allowed” case, the key expectation is that the policy rejects connector-side client config overrides rather than permitting any passthrough. The K2 evidence supports the class/test locations, but the returned snippet did not include the full method body or assertion text, so I would treat the exact rejection path as a code-level verification step rather than a sourced claim.

**Implementation anchors**
- Docs:
  - Kafka Connect user guide, security section: `https://kafka.apache.org/42/kafka-connect/user-guide/#part-0041` [https://kafka.apache.org/42/kafka-connect/user-guide/#part-0041]
  - Kafka Connect configs reference: `https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0040` [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0040]
- Implementation:
  - `connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/NoneConnectorClientConfigOverridePolicy.java` [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/NoneConnectorClientConfigOverridePolicy.java]
  - Its shared base, `AbstractConnectorClientConfigOverridePolicy.java`, is the right adjacent implementation to inspect for the common deny/validate flow [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/AbstractConnectorClientConfigOverridePolicy.java]

**Tests to inspect or add**
- Existing direct test:
  - `connect/runtime/src/test/java/org/apache/kafka/connect/connector/policy/NoneConnectorClientConfigOverridePolicyTest.java` [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/connector/policy/NoneConnectorClientConfigOverridePolicyTest.java]
- Neighboring policy tests that establish the surrounding contract:
  - `BaseConnectorClientConfigOverridePolicyTest` (superclass of the None policy test, per K2 evidence in the test file) [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/connector/policy/NoneConnectorClientConfigOverridePolicyTest.java]
  - `PrincipalConnectorClientConfigOverridePolicyTest.java` [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicyTest.java]
  - `AllowlistConnectorClientConfigOverridePolicy.java` for the opposite policy shape and its “empty allowlist means no overrides” behavior [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/AllowlistConnectorClientConfigOverridePolicy.java]
- If adding coverage, I would add/strengthen a test that asserts:
  - a connector-supplied override is rejected under `NoneConnectorClientConfigOverridePolicy`
  - the rejection is consistent for both producer and consumer client configs, if that is part of the base contract
  - the policy remains the default-deny implementation even when connected through the shared abstract base

**Citations**
- Kafka Connect user guide 4.2: [https://kafka.apache.org/42/kafka-connect/user-guide/#part-0041]
- Kafka Connect configs 4.2: [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0040]
- `NoneConnectorClientConfigOverridePolicy`: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/NoneConnectorClientConfigOverridePolicy.java]
- `AbstractConnectorClientConfigOverridePolicy`: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/AbstractConnectorClientConfigOverridePolicy.java]
- `NoneConnectorClientConfigOverridePolicyTest`: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/connector/policy/NoneConnectorClientConfigOverridePolicyTest.java]
- `PrincipalConnectorClientConfigOverridePolicyTest`: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicyTest.java]
- `AllowlistConnectorClientConfigOverridePolicy`: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/AllowlistConnectorClientConfigOverridePolicy.java]

**Uncertainties**
- The K2 response identified the right files, but it did not return the full implementation body or the full test methods, so I could not source the exact rejection method/result string.
- I did not get a direct excerpt from the docs section that names `connector.client.config.override.policy=none`; the docs anchors are correct, but the exact wording should be rechecked in the cited pages if you need a verbatim doc statement.