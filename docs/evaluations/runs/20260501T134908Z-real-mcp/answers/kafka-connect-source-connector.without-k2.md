**Recommendation**
Treat `SourceConnector` as the connector-side contract, not the record-producing loop. In Kafka Connect 4.2.0 it should be responsible for:
- parsing and validating connector config
- starting/stopping connector-scoped resources
- declaring the `SourceTask` class
- splitting source work into per-task configs via `taskConfigs(int maxTasks)`
- exposing version/config metadata through the inherited `Connector` contract

The runtime owns task instantiation, scheduling, polling, offset commit flow, and restart behavior.

**Implementation anchors**
- Version-pinned docs: Kafka Connect 4.2.0 `SourceConnector` Javadocs and the 4.2.0 Connect docs section for source connectors
- Implementation class: `connect/api/src/main/java/org/apache/kafka/connect/source/SourceConnector.java`
- Base contract: `connect/api/src/main/java/org/apache/kafka/connect/connector/Connector.java`

**Tests to inspect or add**
- `connect/api/src/test/java/org/apache/kafka/connect/source/SourceConnectorTest.java`
- `connect/api/src/test/java/org/apache/kafka/connect/connector/ConnectorTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSourceTaskTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerConnectorTest.java`

Add or extend coverage for:
- `taskConfigs(maxTasks)` partitioning and edge cases
- config validation failures
- start/stop lifecycle behavior
- empty or invalid task-class/task-config scenarios
- boundary behavior between connector setup and worker-owned task execution

**Citations**
- Apache Kafka 4.2.0 source: `connect/api/src/main/java/org/apache/kafka/connect/source/SourceConnector.java`
- Apache Kafka 4.2.0 source: `connect/api/src/main/java/org/apache/kafka/connect/connector/Connector.java`
- Apache Kafka 4.2.0 tests: `connect/api/src/test/java/org/apache/kafka/connect/source/SourceConnectorTest.java`
- Apache Kafka 4.2.0 tests: `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSourceTaskTest.java`

**Uncertainties**
- I’m confident about the contract shape, but I cannot verify the exact 4.2.0 hosted docs URL or whether every suggested test file exists unchanged in that branch without repository access.
- If you need a strictly version-pinned public URL list, verify against the `4.2.0` tag/doc site before quoting links.