**Recommendation**
Use the Kafka 4.2-pinned Kafka Connect docs as the user-facing anchor, and `org.apache.kafka.common.config.ConfigTransformer` as the implementation anchor. For Connect runtime behavior, also anchor on `WorkerConfigTransformer` because it is the Connect wrapper that owns transformation and reload handling.

**Implementation anchors**
- Docs:
  - Kafka Connect landing page for 4.2: [https://kafka.apache.org/42/kafka-connect/](https://kafka.apache.org/42/kafka-connect/)
  - Kafka Connect configuration reference for 4.2: [https://kafka.apache.org/42/configuration/kafka-connect-configs/](https://kafka.apache.org/42/configuration/kafka-connect-configs/)
  - Connector Development Guide for 4.2: [https://kafka.apache.org/42/kafka-connect/connector-development-guide/](https://kafka.apache.org/42/kafka-connect/connector-development-guide/)
- Code:
  - Core transformer: [repo://apache/kafka@4.2/clients/src/main/java/org/apache/kafka/common/config/ConfigTransformer.java](repo://apache/kafka@4.2/clients/src/main/java/org/apache/kafka/common/config/ConfigTransformer.java)
  - Connect wrapper/runtime integration: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConfigTransformer.java](repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConfigTransformer.java)
  - Validation path that applies transformation: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/AbstractHerder.java](repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/AbstractHerder.java)
  - Transformed connector config storage/access: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/storage/ClusterConfigState.java](repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/storage/ClusterConfigState.java)

**Tests to inspect or add**
- Inspect existing Connect coverage for transformation and reload behavior:
  - [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerConfigTransformerTest.java](repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerConfigTransformerTest.java)
- Add or extend tests if needed for:
  - `${provider:[path:]key}` substitution
  - TTL-based reload scheduling
  - connector config validation path using `AbstractHerder.validateConnectorConfig`
  - transformed-vs-raw config exposure in `ClusterConfigState`

**Citations**
- Kafka Connect 4.2 docs landing page: [https://kafka.apache.org/42/kafka-connect/](https://kafka.apache.org/42/kafka-connect/)
- Kafka Connect 4.2 config reference: [https://kafka.apache.org/42/configuration/kafka-connect-configs/](https://kafka.apache.org/42/configuration/kafka-connect-configs/)
- Kafka Connect 4.2 connector development guide: [https://kafka.apache.org/42/kafka-connect/connector-development-guide/](https://kafka.apache.org/42/kafka-connect/connector-development-guide/)
- `ConfigTransformer`: [repo://apache/kafka@4.2/clients/src/main/java/org/apache/kafka/common/config/ConfigTransformer.java](repo://apache/kafka@4.2/clients/src/main/java/org/apache/kafka/common/config/ConfigTransformer.java)
- `WorkerConfigTransformer`: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConfigTransformer.java](repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConfigTransformer.java)

**Uncertainties**
- K2 did not surface a dedicated `ConfigTransformerTest` in the 4.2.0 tree, so the best visible test anchor is `WorkerConfigTransformerTest`.
- The retrieved evidence is enough to confirm the transformation path, but not enough to quote the full `ConfigTransformer` implementation body line-by-line without opening the file directly.
