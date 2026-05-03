**Recommendation**
- Anchor the answer on the Kafka Connect 4.2.0 docs for the user-facing contract, but treat `DistributedHerder` as the source of truth for distributed connector config update behavior.
- For the behavior itself, follow the config-write path, then the async reconfigure/rebalance path. That is the part most likely to matter for distributed updates.

**Implementation anchors**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/distributed/DistributedHerder.java`
- The key update path is the connector-config write/update flow in `DistributedHerder` itself, including the callback/reconfigure handoff after the backing store update.
- If you need the storage side of the behavior, also inspect the backing store implementation used by the herder, typically `KafkaConfigBackingStore`.

**Tests to inspect or add**
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/distributed/DistributedHerderTest.java`
- Neighboring coverage worth checking:
  - tests around `putConnectorConfig(...)` / update-vs-create behavior
  - tests that assert leader/non-leader handling
  - tests that verify reconfiguration or rebalance after config changes
- If the bug/behavior crosses the storage boundary, also inspect backing-store tests under `connect/runtime/src/test/java/org/apache/kafka/connect/storage/`, especially config store tests.

**Citations**
- Apache Kafka 4.2.0 documentation root: `https://kafka.apache.org/42/documentation/`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/distributed/DistributedHerder.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/distributed/DistributedHerderTest.java`

**Uncertainties**
- I’m not fully certain of the exact `DistributedHerder` method names in 4.2.0 without the tree in front of me, but the update/reconfigure path is the right place to anchor the analysis.
- The docs are split across multiple Connect sections in the 4.2.0 site, so the root versioned docs URL is the safest pinned public citation.