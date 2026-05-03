**Recommendation**
Use the 4.2.0 Kafka Connect docs plus the runtime lifecycle tracker as the anchor set. The K2 evidence points to the public Connect docs and, for implementation, to `AbstractHerder` as the class that handles connector/task lifecycle tracking; K2 did not surface a direct `Worker` source hit, so treat that as the nearest implementation anchor rather than guessing a file path [https://kafka.apache.org/42/kafka-connect/], [https://kafka.apache.org/42/kafka-connect/connector-development-guide/], [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/AbstractHerder.java].

**Implementation anchors**
- Version-pinned docs:
  - Kafka Connect landing page for 4.2.0 [https://kafka.apache.org/42/kafka-connect/]
  - Connector Development Guide for connector/task model and lifecycle concepts [https://kafka.apache.org/42/kafka-connect/connector-development-guide/]
  - Connect API overview for runtime-facing connector behavior [https://kafka.apache.org/42/apis/#part-0003]
- Implementation class:
  - `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/AbstractHerder.java` because its class comment explicitly says it “handles connector/task lifecycle tracking” and that extensions must invoke lifecycle hooks appropriately [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/AbstractHerder.java]

**Tests to inspect or add**
- Inspect `connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java` since it exercises connector/task restart behavior and offsets handling in a worker-managed lifecycle path [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java]
- If you want direct `Worker`-focused coverage, add or locate a runtime test that asserts start/stop/rebalance transitions for connectors and tasks; K2 did not surface a specific `Worker*Test` in the returned evidence.

**Citations**
- Kafka Connect 4.2 docs: [https://kafka.apache.org/42/kafka-connect/]
- Connector Development Guide: [https://kafka.apache.org/42/kafka-connect/connector-development-guide/]
- Connect API: [https://kafka.apache.org/42/apis/#part-0003]
- Lifecycle-tracking implementation anchor: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/AbstractHerder.java]
- Neighboring test anchor: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java]

**Uncertainties**
- K2 did not return a direct `Worker` class source hit, so the exact worker implementation file remains unconfirmed from this evidence alone.
- K2 also did not surface a dedicated `Worker` unit test; only a nearby integration test was returned.