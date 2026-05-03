**Recommendation**
Anchor the answer on the 4.2-pinned Kafka Connect docs plus the runtime implementation of `ConnectorConfig`. The class is the shared connector-level config holder: it covers framework/system-level connector settings, not connector-specific settings, and is the right place to explain shared validation behavior [https://kafka.apache.org/42/kafka-connect/configuration/kafka-connect-configs/#part-0001] [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/ConnectorConfig.java].

**Implementation anchors**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/ConnectorConfig.java` is the primary implementation anchor; its class-level doc says it contains Kafka Connect system-level connector options and excludes connector-specific options [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/ConnectorConfig.java].
- The 4.2 docs page `Kafka Connect Configs` shows connector-related config entries using `ConnectorConfig$PluginVersionValidator`, which is a good public-facing anchor for version/plugin validation behavior [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0040] [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0047].
- The 4.2 `Connector Development Guide` is the docs-side anchor for how connector config validation is exposed to the framework via `config()` / `ConfigDef` [https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0019].

**Tests to inspect or add**
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ConnectorConfigTest.java` is the direct neighboring test class for `ConnectorConfig` [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ConnectorConfigTest.java].
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/SourceConnectorConfigTest.java` is a nearby test worth checking because it exercises connector-specific config plumbing built on top of the shared runtime config [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/SourceConnectorConfigTest.java].
- If coverage is missing, add focused tests in `ConnectorConfigTest` for any shared validation branches you care about, especially around plugin/version validation and required shared fields [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ConnectorConfigTest.java].

**Citations**
- Docs: [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0001]
- Docs: [https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0019]
- Docs: [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0040]
- Docs: [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0047]
- Code: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/ConnectorConfig.java]
- Test: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ConnectorConfigTest.java]
- Neighbor test: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/SourceConnectorConfigTest.java]

**Uncertainties**
- The K2 evidence did not expose the full bodies or individual method names for `ConnectorConfigTest`, so I can anchor the file but not cite specific test cases without deeper inspection.
- The search result was enough to confirm the implementation class and the relevant 4.2 docs, but not enough to enumerate every shared validation rule in `ConnectorConfig` without opening the source directly.