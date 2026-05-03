**Recommendation**
Use the Kafka Connect 4.2.0 standalone-mode docs as the user-facing anchor, then validate behavior directly in `StandaloneHerder`. For config updates in standalone mode, the key question is whether an update replaces the existing connector config and triggers the expected stop/restart path, rather than distributed-mode rebalance semantics.

**Implementation anchors**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/standalone/StandaloneHerder.java`
- If you need the full path of effect, also inspect the standalone config/storage and worker restart path in the same runtime area.

**Tests to inspect or add**
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/standalone/StandaloneHerderTest.java`
- Any other tests in `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/standalone/` that cover connector lifecycle or config replacement
- If config-update behavior is not already covered, add a regression test in that package for repeated `putConnectorConfig` / update semantics

**Citations**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/standalone/StandaloneHerder.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/standalone/StandaloneHerderTest.java`

**Uncertainties**
- I cannot pin the exact 4.2.0 public docs URL from memory without browsing.
- I am confident about `StandaloneHerder`; I am less certain about the exact names of any additional neighboring test classes beyond `StandaloneHerderTest`.