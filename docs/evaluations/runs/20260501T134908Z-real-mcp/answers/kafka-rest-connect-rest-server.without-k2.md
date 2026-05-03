**Recommendation**
Anchor the writeup on the Kafka 4.2.0 Connect docs, then trace the runtime wiring through `ConnectRestServer` and confirm behavior with the closest REST-server unit tests. If you need one narrow path, start at the REST server constructor/bootstrap path and follow how it builds the embedded `RestServer`, config, and handlers.

**Implementation anchors**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/ConnectRestServer.java`
- Likely adjacent wiring helpers in the same area, especially `ConnectRestConfig` and `RestServer`
- Version-pinned docs: Kafka 4.2.0 Connect documentation on the 4.2 release docs site, likely `https://kafka.apache.org/42/documentation.html`

**Tests to inspect or add**
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/ConnectRestServerTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/RestServerTest.java`
- If you need broader coverage, add or inspect an integration-style test in the same `connect/runtime` area that boots a full Connect runtime and exercises REST startup/shutdown wiring

**Citations**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/ConnectRestServer.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/ConnectRestServerTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/RestServerTest.java`
- `https://kafka.apache.org/42/documentation.html`

**Uncertainties**
- I’m not fully certain of the exact Connect docs section anchor inside the 4.2.0 documentation page without checking the tree.
- I expect `ConnectRestServerTest` and `RestServerTest` to be the nearest unit tests, but the exact neighboring integration test names can vary slightly across the 4.2.0 branch.