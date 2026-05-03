**Recommendation**
Use `Herder` as the connector management interface to anchor the answer. In Kafka Connect 4.2.0, it is the control-plane abstraction for creating, updating, restarting, pausing, resuming, and deleting connectors; `DistributedHerder` is the primary production implementation.

**Implementation anchors**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/Herder.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/distributed/DistributedHerder.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/standalone/StandaloneHerder.java`

**Tests to inspect or add**
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/distributed/DistributedHerderTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/standalone/StandaloneHerderTest.java`
- Add or extend focused lifecycle tests around connector create/update/delete/restart/pause/resume paths in `DistributedHerderTest` if the behavior you care about is missing.

**Citations**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/Herder.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/distributed/DistributedHerder.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/distributed/DistributedHerderTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/standalone/StandaloneHerderTest.java`

**Uncertainties**
- I’m confident about the interface and implementation class names, but I can’t verify the exact version-pinned public docs URL without browsing.
- If you need a precise 4.2.0 docs link, the safest anchor is the 4.2.0 Kafka Connect Javadocs entry for `org.apache.kafka.connect.runtime.Herder`.