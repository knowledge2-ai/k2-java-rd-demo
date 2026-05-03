**Recommendation**
- Anchor the answer on the Kafka 4.2.0 version-pinned Javadocs for `org.apache.kafka.connect.data.SchemaBuilder` and the Connect data-model docs for that release.
- Treat `SchemaBuilder` as the construction API and `ConnectSchema` as the materialized implementation that `build()` returns.

**Implementation anchors**
- `connect/api/src/main/java/org/apache/kafka/connect/data/SchemaBuilder.java`
- `connect/api/src/main/java/org/apache/kafka/connect/data/ConnectSchema.java`
- If you need field/default semantics, also inspect `Schema.java` and `Field.java` in the same package.

**Tests to inspect or add**
- `connect/api/src/test/java/org/apache/kafka/connect/data/SchemaBuilderTest.java`
- `connect/api/src/test/java/org/apache/kafka/connect/data/ConnectSchemaTest.java`
- Add a focused regression test for the behavior you care about most:
  - required vs optional schemas
  - default values
  - nested list/map schemas
  - logical types
  - builder immutability after `build()`

**Citations**
- `https://kafka.apache.org/42/javadoc/org/apache/kafka/connect/data/SchemaBuilder.html`
- `connect/api/src/main/java/org/apache/kafka/connect/data/SchemaBuilder.java`
- `connect/api/src/test/java/org/apache/kafka/connect/data/SchemaBuilderTest.java`

**Uncertainties**
- I’m confident about the implementation and test anchors above.
- I’m less certain of the exact Connect docs section anchor without checking the 4.2.0 docs site, so I would not overstate that path here.