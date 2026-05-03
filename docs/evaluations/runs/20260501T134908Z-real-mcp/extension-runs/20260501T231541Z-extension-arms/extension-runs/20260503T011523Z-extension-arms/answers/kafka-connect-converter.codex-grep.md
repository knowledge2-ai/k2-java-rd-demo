**Recommendation**
- Anchor the explanation on source Javadocs, not a separate rendered docs tree. In this checkout, the authoritative version-pinned docs for converter behavior are the API comments in `Converter`, `ConverterConfig`, `StringConverterConfig`, and `StringConverter`.
- The key/value split is config-time, not conversion-time: `Converter.configure(Map, boolean)` marks a converter as key or value, and `StringConverter.configure(Map, boolean)` just stores `converter.type` before delegating. The actual `fromConnectData` / `toConnectData` logic is identical for key and value and ignores schema.
- For runtime wiring, `Worker` creates key and value converters separately, first from connector config and then falling back to worker config.

**Implementation anchors**
- `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/Converter.java` for the interface contract, including the header-aware defaults delegating to the 3-arg methods.
- `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/ConverterConfig.java` for `converter.type` and the allowed `key` / `value` / `header` modes.
- `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/StringConverterConfig.java` for the encoding config and inherited type config.
- `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/StringConverter.java` for the actual key/value behavior.
- `repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/Worker.java` for the key/value converter resolution path.

**Tests to inspect or add**
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSourceTaskTest.java` for direct assertions that key and value converters are invoked separately with headers and schemas.
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/AbstractWorkerSourceTaskTest.java` for the shared helper coverage around key/value conversion and failure paths.
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ConnectWorkerIntegrationTest.java` for end-to-end source-connector behavior using `StringConverter` and alias resolution.
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ConnectorValidationIntegrationTest.java` and `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ErrorHandlingTaskTest.java` for connector config and error-handling scenarios that still wire `StringConverter` on both sides.
- If you want a fast unit regression, add a dedicated `StringConverterTest`; there is no existing `StringConverterTest.java` in this checkout. The nearest converter-test patterns are `ByteArrayConverterTest.java` and `NumberConverterTest.java`.

**Citations**
- `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/Converter.java#L28-L98`
- `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/ConverterConfig.java#L28-L57`
- `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/StringConverterConfig.java#L27-L60`
- `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/StringConverter.java#L33-L117`
- `repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/Worker.java#L699-L724`
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSourceTaskTest.java#L602-L620`
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/AbstractWorkerSourceTaskTest.java#L902-L918`
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ConnectWorkerIntegrationTest.java#L1333-L1376`
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ConnectorValidationIntegrationTest.java#L566-L590`
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ErrorHandlingTaskTest.java#L200-L202`
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/converters/ByteArrayConverterTest.java#L1-L110`
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/converters/NumberConverterTest.java#L1-L100`

**Uncertainties**
- I did not find a separate rendered docs tree in this checkout, so I used source Javadocs as the version-pinned documentation anchor.
- I did not find a dedicated `StringConverterTest.java`; if you want direct unit coverage, that test would need to be added.