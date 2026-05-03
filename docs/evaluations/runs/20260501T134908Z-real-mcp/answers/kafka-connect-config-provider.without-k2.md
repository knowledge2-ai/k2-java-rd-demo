**Recommendation**
- Anchor the explanation on Kafka Connect 4.2.0’s version-pinned Connect docs for **Config Providers**.
- For code, anchor on the SPI `org.apache.kafka.common.config.provider.ConfigProvider` and the built-in concrete provider `org.apache.kafka.common.config.provider.FileConfigProvider`.
- If you need one implementation class to cite for externalized secrets behavior, `FileConfigProvider` is the safest anchor.

**Implementation anchors**
- `org.apache.kafka.common.config.provider.ConfigProvider` is the contract: `configure(...)`, `get(...)`, `close()`.
- `org.apache.kafka.common.config.provider.FileConfigProvider` is the reference implementation used by Connect-style externalized config substitution.
- `org.apache.kafka.common.config.ConfigTransformer` is the resolution path worth mentioning if you explain how `${provider:path:key}` gets expanded.

**Tests to inspect or add**
- `ConfigTransformer` tests for placeholder resolution and error paths.
- `FileConfigProvider` tests for file lookup, missing keys, and lifecycle/close behavior.
- Connector/worker config tests covering substitution in real Connect configs, including nested or repeated placeholders.
- If the contract is documented as supporting TTL or refresh semantics in 4.2.0, add coverage for that explicitly; I am not fully certain that behavior is relevant in this release.

**Citations**
- Apache Kafka 4.2.0 Connect documentation, section **Config Providers**.
- Source path: `clients/src/main/java/org/apache/kafka/common/config/provider/ConfigProvider.java`
- Source path: `clients/src/main/java/org/apache/kafka/common/config/provider/FileConfigProvider.java`

**Uncertainties**
- I am confident about the SPI and `FileConfigProvider`, but I am not fully certain of the exact version-pinned doc URL fragment for the 4.2.0 docs.
- If you need a single “official answer” sentence, I would phrase it as: “Kafka Connect externalized secrets are defined by the `ConfigProvider` SPI and demonstrated by `FileConfigProvider` in the 4.2.0 Connect Config Providers docs.”