**Recommendation**
Anchor the answer on the Apache Kafka Connect REST API for **4.2.0**, not the moving latest docs. For the response shape, use the **`ConnectorInfo` entity** that backs `GET /connectors/{connector}`.

**Implementation anchors**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/entities/ConnectorInfo.java`
- Version-pinned 4.2.0 Connect REST API docs for `GET /connectors/{connector}`
- If you need the JSON shape rationale, also check the REST entity package around `org.apache.kafka.connect.runtime.rest.entities`

**Tests to inspect or add**
- Unit test for `ConnectorInfo` JSON serialization/deserialization round-trip
- REST resource test for `GET /connectors/{name}` asserting the exact response fields and `type`
- Regression test for any edge cases you care about, such as empty task lists or connector type mapping

**Citations**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/entities/ConnectorInfo.java`

**Uncertainties**
- I am confident about the implementation class and package path.
- I am not fully certain of the exact published 4.2.0 docs URL layout without browsing, so I’m naming the version-pinned docs at the endpoint level rather than guessing a URL.