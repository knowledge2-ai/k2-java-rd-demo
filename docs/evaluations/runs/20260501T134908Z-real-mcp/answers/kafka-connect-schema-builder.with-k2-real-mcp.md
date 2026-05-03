**Recommendation**
Use the version-pinned Kafka 4.2 docs for Connect schema construction context, then anchor any behavioral claim in `SchemaBuilder` itself. The K2 evidence does not surface a `SchemaBuilder`-specific regression test, so treat the test anchor as incomplete rather than inferred.

**Implementation anchors**
- `SchemaBuilder` implementation: `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/data/SchemaBuilder.java`
- Version-pinned Connect docs:
  - Kafka Connect landing page: `https://kafka.apache.org/42/kafka-connect/`
  - Connector Development Guide section showing `SchemaBuilder.struct()` usage: `https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0001`
  - Kafka 4.2 API page for Connect API entry point: `https://kafka.apache.org/42/apis/#part-0003`

**Tests to inspect or add**
- K2 did not return a `SchemaBuilderTest` or a nearby Connect schema-construction test to anchor the behavior claim.
- The only surfaced test artifact was `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java`, which is not clearly relevant to `SchemaBuilder` behavior.
- If you need a solid regression anchor, add or locate a focused `connect/api` unit test around schema-building semantics, especially for nested types and default/version/doc/name handling.

**Citations**
- Docs: `https://kafka.apache.org/42/kafka-connect/`
- Docs: `https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0001`
- Docs: `https://kafka.apache.org/42/apis/#part-0003`
- Code: `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/data/SchemaBuilder.java`
- Test gap evidence: `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ExactlyOnceSourceIntegrationTest.java`

**Uncertainties**
- K2 evidence is incomplete on neighboring `SchemaBuilder`-specific tests.
- I can confirm the implementation anchor and version-pinned docs, but I cannot name a precise existing regression test for `SchemaBuilder` from the returned evidence.