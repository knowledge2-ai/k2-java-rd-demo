**Recommendation**
Anchor the answer on the Kafka 4.2.0 `SourceRecord` Javadoc and the `connect/api` implementation. The key behavior is that `SourceRecord` carries two separate metadata planes:

- Kafka destination metadata: topic, Kafka partition, key/value, timestamp, headers
- Source-side metadata: `sourcePartition` and `sourceOffset` maps

For your question, the source-side partition metadata is the `sourcePartition` map, not the Kafka topic partition.

**Implementation anchors**
- Version-pinned docs: Kafka 4.2.0 Javadoc for `org.apache.kafka.connect.source.SourceRecord`
- Implementation class: `connect/api/src/main/java/org/apache/kafka/connect/source/SourceRecord.java`
- Base behavior to cross-check: `connect/api/src/main/java/org/apache/kafka/connect/ConnectRecord.java`

**Tests to inspect or add**
- `connect/api/src/test/java/org/apache/kafka/connect/source/SourceRecordTest.java`
- `connect/api/src/test/java/org/apache/kafka/connect/ConnectRecordTest.java`
- If you need stronger coverage, add/extend tests for:
  - constructor overloads preserving `sourcePartition` and `sourceOffset`
  - `sourcePartition()` / `sourceOffset()` accessors
  - `newRecord(...)` or equivalent copy/replace paths preserving source metadata while changing Kafka topic/partition fields
  - null/empty map handling for source metadata

**Citations**
- Apache Kafka 4.2.0 Javadoc for `org.apache.kafka.connect.source.SourceRecord`
- Apache Kafka source file `connect/api/src/main/java/org/apache/kafka/connect/source/SourceRecord.java`
- Apache Kafka test file `connect/api/src/test/java/org/apache/kafka/connect/source/SourceRecordTest.java`
- Apache Kafka test file `connect/api/src/test/java/org/apache/kafka/connect/ConnectRecordTest.java`

**Uncertainties**
- I’m confident about the implementation class and package layout, but I’m not fully certain whether the 4.2.0 branch’s neighboring test filenames are exactly `SourceRecordTest` and `ConnectRecordTest` or whether one of the relevant assertions lives in a nearby source-task test instead.
- I’m also not certain of the exact 4.2.0 public Javadoc URL pattern without checking the site, so I’m naming the artifact precisely rather than guessing the URL.