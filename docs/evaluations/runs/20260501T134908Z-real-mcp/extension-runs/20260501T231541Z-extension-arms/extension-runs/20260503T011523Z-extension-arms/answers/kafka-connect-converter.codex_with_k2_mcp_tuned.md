**Recommendation**

Anchor the answer on the `Converter` interface contract plus the runtime wiring in `Plugins.newConverter(...)`. The key/value split is not handled by one shared converter instance: Connect selects a converter for `key.converter` and `value.converter`, treats absence of the property as “no override,” and configures the chosen plugin with the old-style prefix `key.converter.` or `value.converter.` [repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/Converter.java], [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/Plugins.java#L455-L497], [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/Worker.java#L692-L726].

**Implementation anchors**

- `Converter` is the public interface to cite first for the contract itself: it is the target abstraction for value/key conversion behavior [repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/Converter.java].
- `Plugins.newConverter(...)` is the concrete selection path: it checks whether the config contains the converter property, infers key vs value from `WorkerConfig.KEY_CONVERTER_CLASS_CONFIG`, and builds `converterConfig` with `classPropertyName + "."` before instantiating the plugin [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/Plugins.java#L455-L497].
- `WorkerConfig` is the version-pinned docs anchor for the public keys: `KEY_CONVERTER_CLASS_CONFIG`/`VALUE_CONVERTER_CLASS_CONFIG` and their docs explain that these control serialization format for record keys and values [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConfig.java#L73-L103].
- `ConnectorConfig` adds the versioned-plugin side of the story with `KEY_CONVERTER_VERSION_CONFIG` and `VALUE_CONVERTER_VERSION_CONFIG`, plus validators that require a concrete `Converter` implementation [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/ConnectorConfig.java#L99-L129].
- `ConverterConfig` and `ConverterType` define the implementation-level type switch: `converter.type` is limited to `key`, `value`, or `header`, and `ConverterType.KEY/VALUE/HEADER` is the exact enum source [repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/ConverterConfig.java#L21-L51], [repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/ConverterType.java#L20-L50].

**Tests to inspect or add**

- `MultiVersionTest` is the strongest neighboring test for versioned converter loading; it asserts separate key and value converters are resolved and that each exposes the expected versioned plugin behavior [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/MultiVersionTest.java#L270-L292].
- `WorkerSinkTaskTest` exercises `toConnectData(...)` for key/value conversion in the sink path, so it is the closest runtime consumer-side neighbor [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSinkTaskTest.java].
- `AbstractWorkerSourceTaskTest` exercises `fromConnectData(...)` for source records, so it is the closest producer-side neighbor [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/AbstractWorkerSourceTaskTest.java].
- `NumberConverterTest` is the best template if you need to add or tighten converter-specific behavior tests around schemas, null handling, and round trips [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/converters/NumberConverterTest.java].

**Citations**

- `Converter`: [repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/Converter.java]
- `Plugins.newConverter(...)`: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/Plugins.java#L455-L497]
- `WorkerConfig`: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConfig.java#L73-L103]
- `ConnectorConfig`: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/ConnectorConfig.java#L99-L129]
- `ConverterConfig`: [repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/ConverterConfig.java#L21-L51]
- `ConverterType`: [repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/ConverterType.java#L20-L50]
- `Worker.java` consumer wiring: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/Worker.java#L692-L726]
- `MultiVersionTest`: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/MultiVersionTest.java#L270-L292]
- `WorkerSinkTaskTest`: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSinkTaskTest.java]
- `AbstractWorkerSourceTaskTest`: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/AbstractWorkerSourceTaskTest.java]
- `NumberConverterTest`: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/converters/NumberConverterTest.java]

**Uncertainties**

- I did not retrieve a separate prose docs page for `Converter`; the retrieved evidence anchors the public contract through code and config docs instead.
