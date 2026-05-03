**Recommendation**
Anchor the answer on the 4.2.0 Kafka Connect user guide plus the standalone runtime implementation. For this topic, the most relevant sources are the version-pinned docs at `https://kafka.apache.org/42/kafka-connect/user-guide/#part-0001`, `https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0001`, and `https://kafka.apache.org/42/kafka-connect/` for the Connect overview, with config reference context from `https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0040`.

**Implementation anchors**
- `StandaloneHerder` is the implementation class to inspect: `repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/standalone/StandaloneHerder.java`.
- The returned snippet shows the standalone task-update path in `updateConnectorTasks(String connName)`: it skips updates when the connector is not running or not `TargetState.STARTED`, recomputes task configs, reverse-transforms them, checks `taskConfigsChanged(...)`, then removes tasks, persists new task configs, and recreates connector tasks.
- `StandaloneConfig` is the adjacent runtime config anchor for standalone mode: `repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/standalone/StandaloneConfig.java`.

**Tests to inspect or add**
- Existing neighbor test to inspect first: `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/standalone/StandaloneHerderTest.java`.
- K2 also surfaced `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java`, but that is only a loose neighboring Connect integration test, not a direct standalone config-update regression test.
- If you need coverage for connector config updates in standalone mode, add or extend a focused regression in `StandaloneHerderTest` around:
  - skipping updates when the connector is stopped,
  - no-op behavior when configs are unchanged,
  - task recreation when configs change.

**Citations**
- Docs: `https://kafka.apache.org/42/kafka-connect/user-guide/#part-0001`
- Docs: `https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0001`
- Docs: `https://kafka.apache.org/42/kafka-connect/`
- Docs: `https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0040`
- Code: `repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/standalone/StandaloneHerder.java`
- Code: `repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/standalone/StandaloneConfig.java`
- Test: `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/standalone/StandaloneHerderTest.java`
- Test: `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java`

**Uncertainties**
- K2 did not return the specific `StandaloneHerderTest` methods or assertions, so I cannot name the exact existing regression cases without guessing.
- The docs returned are version-pinned and relevant, but K2 did not surface a standalone-specific doc section that directly explains config-update semantics.