**Recommendation**
Anchor the answer on `connect/api/src/main/java/org/apache/kafka/connect/storage/Converter.java` for the public conversion contract, then on `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/Plugins.java` for the worker-side `isKey` wiring. Use the 4.2 Connect config docs for `key.converter` and `value.converter` as the version-pinned public context, but keep the implementation explanation code-first. [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0002] [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0040]

**Implementation anchors**
- `Converter.java` is the core interface: it exposes the shared `toConnectData(String, byte[])` and `fromConnectData(String, Schema, Object)` conversion API, and its header-aware `fromConnectData(String, Headers, Schema, Object)` default just delegates to the 3-arg form. That is the cleanest anchor for “value/key conversion behavior” at the contract level. [repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/Converter.java]
- `Plugins.java` is the worker-side instantiation point: `newInternalConverter(boolean isKey, String className, Map<String, String> converterConfig)` explicitly carries the key/value discriminator into converter loading/configuration. [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/Plugins.java]
- Concrete implementations show where the key/value split becomes real behavior: `ByteArrayConverter` ignores the boolean `isKey`, while `NumberConverter` computes `isKey` from `ConverterType.KEY` before configuring serializer/deserializer. That makes `configure(Map<String, ?>, boolean isKey)` the hook to inspect for diverging key vs value semantics. [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/converters/ByteArrayConverter.java] [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/converters/NumberConverter.java]

**Tests to inspect or add**
- `BooleanConverterTest.java` for schema/value round-trips and invalid/null handling around `fromConnectData` and `toConnectData`. [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/converters/BooleanConverterTest.java]
- `ByteArrayConverterTest.java` for pass-through behavior, `ByteBuffer` handling, and null handling. [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/converters/ByteArrayConverterTest.java]
- `NumberConverterTest.java` for serializer/deserializer type checks and failure cases when the schema/value is wrong. [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/converters/NumberConverterTest.java]
- `WorkerTest.java` for the `newInternalConverter(true/false, ...)` wiring path; it is the nearest test anchor for asserting key vs value converter instantiation behavior. [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerTest.java]

**Citations**
- Docs: [https://kafka.apache.org/42/kafka-connect/](https://kafka.apache.org/42/kafka-connect/)
- Docs: [https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0001](https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0001)
- Docs: [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0002](https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0002)
- Docs: [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0040](https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0040)
- Code: [repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/Converter.java](repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/Converter.java)
- Code: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/Plugins.java](repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/Plugins.java)
- Code: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/converters/ByteArrayConverter.java](repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/converters/ByteArrayConverter.java)
- Code: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/converters/NumberConverter.java](repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/converters/NumberConverter.java)
- Tests: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/converters/BooleanConverterTest.java](repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/converters/BooleanConverterTest.java)
- Tests: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/converters/ByteArrayConverterTest.java](repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/converters/ByteArrayConverterTest.java)
- Tests: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/converters/NumberConverterTest.java](repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/converters/NumberConverterTest.java)
- Tests: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerTest.java](repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerTest.java)

**Uncertainties**
- I did not retrieve a dedicated test that directly asserts `configure(Map<String, ?>, boolean isKey)` receives the expected boolean for a custom converter; that behavior is inferred from `Plugins.java` plus the concrete converter tests above.