**Recommendation**
Use the Kafka 4.2.0 docs as the public anchor, then ground the implementation on `WorkerConnector` and its direct unit test coverage. The strongest evidence points to `WorkerConnector.initialize()` for startup and the state-transition path for failure handling, with `WorkerConnectorTest` as the primary regression anchor.

**Implementation anchors**
- Version-pinned docs:
  - Kafka Connect landing page [https://kafka.apache.org/42/kafka-connect/]
  - Connector Development Guide [https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0001]
  - User Guide [https://kafka.apache.org/42/kafka-connect/user-guide/#part-0001]
- Implementation class:
  - `WorkerConnector` [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConnector.java]
- Behavior to inspect in that class:
  - Startup entry path around `initialize()`
  - State transition / failure callback path around `transitionTo(...)`
  - The class-level responsibility is lifecycle management, including startup and shutdown [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConnector.java]

**Tests to inspect or add**
- Direct unit anchor:
  - `WorkerConnectorTest` [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerConnectorTest.java]
- Specific cases surfaced by K2:
  - `testFailConnectorThatIsNeitherSourceNorSink(...)` in `WorkerConnectorTest` for startup validation/failure routing
  - `testStopFailure(...)` in `WorkerConnectorTest` for failure handling during lifecycle transitions
- Neighboring runtime integration reference:
  - `ExactlyOnceSourceIntegrationTest` [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java]
- If you add coverage, target:
  - startup failure propagation when connector type is invalid
  - callback behavior when state transitions are pre-empted or fail
  - stop/retry failure handling

**Citations**
- [https://kafka.apache.org/42/kafka-connect/]
- [https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0001]
- [https://kafka.apache.org/42/kafka-connect/user-guide/#part-0001]
- [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConnector.java]
- [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerConnectorTest.java]
- [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java]

**Uncertainties**
- K2 returned the correct version-pinned anchors, but not line-precise excerpts for every startup/failure branch inside `WorkerConnector`, so I’m not claiming exact control-flow details beyond the class and the surfaced methods.
- `ExactlyOnceSourceIntegrationTest` is adjacent runtime coverage, but the evidence does not prove it directly exercises the same `WorkerConnector` startup path.