**Recommendation**
Anchor your 4.2.0 analysis on the versioned Kafka Connect admin docs plus the `ConnectorsResource` implementation and its dedicated test class. The K2 evidence is enough to identify the right files, but it is truncated before the full method-level CRUD trace, so don’t infer endpoint details beyond what is explicitly verified here.

**Implementation anchors**
- Version-pinned docs: Kafka 4.2 Connect Administration, which describes the REST layer used to view and alter connector state [https://kafka.apache.org/42/kafka-connect/administration/#part-0001].
- Primary implementation: `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/resources/ConnectorsResource.java` [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/resources/ConnectorsResource.java].
- Broader REST context: `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/ConnectRestServer.java` and `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/resources/InternalConnectResource.java` [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/ConnectRestServer.java], [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/resources/InternalConnectResource.java].

**Tests to inspect or add**
- Primary neighboring test: `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/resources/ConnectorsResourceTest.java` [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/resources/ConnectorsResourceTest.java].
- Adjacent REST tests worth checking for shared wiring and regressions: `InternalConnectResourceTest`, `ConnectorPluginsResourceTest`, `RootResourceTest`, `LoggingResourceTest` [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/resources/InternalConnectResourceTest.java], [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/resources/ConnectorPluginsResourceTest.java], [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/resources/RootResourceTest.java], [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/resources/LoggingResourceTest.java].
- If you are adding coverage, add or extend `ConnectorsResourceTest` around the CRUD paths directly; the returned evidence confirms that class is the dedicated anchor, but not the full method inventory.

**Citations**
- Docs: [https://kafka.apache.org/42/kafka-connect/administration/#part-0001]
- Implementation: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/resources/ConnectorsResource.java]
- Primary test: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/resources/ConnectorsResourceTest.java]
- Related tests: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/resources/InternalConnectResourceTest.java], [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/resources/ConnectorPluginsResourceTest.java], [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/resources/RootResourceTest.java], [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/resources/LoggingResourceTest.java]

**Uncertainties**
- The K2 payload for `ConnectorsResourceTest` is truncated, so I cannot safely name the exact CRUD methods, REST verbs, or assertions without guessing.
- The evidence confirms the correct anchor files, but not a complete method-by-method CRUD trace.