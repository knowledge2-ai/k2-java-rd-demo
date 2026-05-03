**Recommendation**
- Anchor the answer on the Kafka 4.2.0 docs root, then ground the behavior in `SourceConnectorConfig` and the adjacent runtime tests that exercise config validation.
- For source-connector-specific validation, prefer the exact `SourceConnectorConfig` path over generic Connect docs, since the class is the implementation of record for that logic.

**Implementation anchors**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/SourceConnectorConfig.java`
- If the validation delegates or shares rules, also inspect `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/ConnectorConfig.java`
- If the validation touches topic-creation settings, also inspect `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/TopicCreationConfig.java`

**Tests to inspect or add**
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/SourceConnectorConfigTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ConnectorConfigTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/TopicCreationConfigTest.java`
- Add a regression test in `SourceConnectorConfigTest` for the exact invalid source config shape you care about, if it is not already covered.

**Citations**
- `https://kafka.apache.org/42/documentation.html`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/SourceConnectorConfig.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/SourceConnectorConfigTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ConnectorConfigTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/TopicCreationConfigTest.java`

**Uncertainties**
- I am not fully certain whether the 4.2.0 docs expose this under a dedicated generated Connect config page or only through the main versioned documentation page, but `https://kafka.apache.org/42/documentation.html` is the safe version-pinned anchor.
- I am also not fully certain whether every validation branch lives directly in `SourceConnectorConfig` versus helper classes like `TopicCreationConfig`, so the neighboring tests above are the right places to confirm coverage.