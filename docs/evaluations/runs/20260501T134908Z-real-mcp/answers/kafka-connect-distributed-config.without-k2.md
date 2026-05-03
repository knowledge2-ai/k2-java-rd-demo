**Recommendation**
Anchor the answer on the 4.2.0 Connect distributed-worker config docs, but treat the implementation class and unit tests as the primary source of truth. For distributed-mode behavior, `DistributedConfig` is the config boundary; follow its validation/defaulting into the distributed herder startup path.

**Implementation anchors**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/distributed/DistributedConfig.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConfig.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/distributed/DistributedHerder.java`
- Version-pinned docs: the Kafka 4.2.0 Connect configuration docs for distributed workers, plus the `connect-distributed.properties` sample config

**Tests to inspect or add**
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/distributed/DistributedConfigTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerConfigTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/distributed/DistributedHerderTest.java`
- If behavior changed, add a focused regression test for the exact distributed-only config key or precedence rule in question

**Citations**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/distributed/DistributedConfig.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/distributed/DistributedConfigTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/distributed/DistributedHerderTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerConfigTest.java`
- `config/connect-distributed.properties`

**Uncertainties**
- I’m not fully certain whether the 4.2.0 docs expose this as a standalone distributed-worker page or as part of the general Connect config section.
- I’m not fully certain whether 4.2.0 has additional neighboring distributed startup tests beyond the three test classes above, but these are the right anchors.