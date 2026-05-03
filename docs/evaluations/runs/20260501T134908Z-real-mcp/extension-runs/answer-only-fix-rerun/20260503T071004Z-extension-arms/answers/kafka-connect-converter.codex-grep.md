**Recommendation**
Anchor the answer on the source Javadocs and loader path, not on a separate docs page.

- For version-pinned docs, use the `key.converter.version` and `value.converter.version` docs in `WorkerConfig` and the connector-scoped mirrors in `ConnectorConfig`.
- For implementation behavior, use `Plugins.newConverter(...)` as the class that decides key vs value and passes `isKey` into `configure(...)`.
- For concrete converter behavior, `NumberConverter` is the clearest exemplar, with `BooleanConverter` and `ByteArrayConverter` as adjacent companions.

**Implementation anchors**
- `Converter` defines the contract, including the `configure(Map<String, ?>, boolean isKey)` split and the default header-aware overloads.
- `Plugins.newConverter(...)` derives `isKeyConverter` from `key.converter` vs `value.converter` and calls `plugin.configure(converterConfig, isKeyConverter)`.
- `WorkerConfig` and `ConnectorConfig` carry the version-pinned docs for the worker- and connector-level converter version properties.
- `NumberConverter`, `BooleanConverter`, and `ByteArrayConverter` show the actual runtime patterns: `configure(..., boolean)` either maps to `ConverterType.KEY/VALUE` or no-ops, while `fromConnectData`/`toConnectData` stay symmetric.

**Tests to inspect or add**
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/PluginsTest.java`
  - `shouldInstantiateAndConfigureConverters`
  - `shouldInstantiateAndConfigureInternalConverters`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/MultiVersionTest.java`
  - `testVersionedConverter`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/PluginRecommenderTest.java`
  - `testConverterVersionRecommenders`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerTest.java`
  - the converter selection paths around `verifyVersionedTaskConverterFromConnector(...)` / `verifyVersionedTaskConverterFromWorker(...)`
- `connect/runtime/src/test/java/org/apache/kafka/connect/converters/NumberConverterTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/converters/BooleanConverterTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/converters/ByteArrayConverterTest.java`

If you need a new regression test, the most useful one would assert that:
- key and value converters are configured independently,
- versioned key/value selection picks different plugin versions when both are present,
- and `isKey` is preserved when the worker instantiates the converter.

**Citations**
- `Converter` contract: [Converter.java](https://github.com/apache/kafka/blob/ba74c3a289456f7346f2bece2cf76fcae55be9a4/connect/api/src/main/java/org/apache/kafka/connect/storage/Converter.java#L40-L98)
- Worker-level version docs: [WorkerConfig.java](https://github.com/apache/kafka/blob/ba74c3a289456f7346f2bece2cf76fcae55be9a4/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConfig.java#L74-L94)
- Connector-level version docs: [ConnectorConfig.java](https://github.com/apache/kafka/blob/ba74c3a289456f7346f2bece2cf76fcae55be9a4/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/ConnectorConfig.java#L105-L122)
- Key/value loader logic: [Plugins.java](https://github.com/apache/kafka/blob/ba74c3a289456f7346f2bece2cf76fcae55be9a4/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/Plugins.java#L457-L505)
- Concrete key/value converter pattern: [NumberConverter.java](https://github.com/apache/kafka/blob/ba74c3a289456f7346f2bece2cf76fcae55be9a4/connect/runtime/src/main/java/org/apache/kafka/connect/converters/NumberConverter.java#L44-L115)
- Boolean converter companion: [BooleanConverter.java](https://github.com/apache/kafka/blob/ba74c3a289456f7346f2bece2cf76fcae55be9a4/connect/runtime/src/main/java/org/apache/kafka/connect/converters/BooleanConverter.java#L38-L110)
- Byte-array converter companion: [ByteArrayConverter.java](https://github.com/apache/kafka/blob/ba74c3a289456f7346f2bece2cf76fcae55be9a4/connect/runtime/src/main/java/org/apache/kafka/connect/converters/ByteArrayConverter.java#L35-L99)
- Versioned key/value test: [MultiVersionTest.java](https://github.com/apache/kafka/blob/ba74c3a289456f7346f2bece2cf76fcae55be9a4/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/MultiVersionTest.java#L260-L287)
- Version recommender test: [PluginRecommenderTest.java](https://github.com/apache/kafka/blob/ba74c3a289456f7346f2bece2cf76fcae55be9a4/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/PluginRecommenderTest.java#L66-L79)
- Converter instantiation/config tests: [PluginsTest.java](https://github.com/apache/kafka/blob/ba74c3a289456f7346f2bece2cf76fcae55be9a4/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/PluginsTest.java#L90-L146)
- Worker-side selection tests: [WorkerTest.java](https://github.com/apache/kafka/blob/ba74c3a289456f7346f2bece2cf76fcae55be9a4/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerTest.java#L704-L718)
- Converter behavior tests: [NumberConverterTest.java](https://github.com/apache/kafka/blob/ba74c3a289456f7346f2bece2cf76fcae55be9a4/connect/runtime/src/test/java/org/apache/kafka/connect/converters/NumberConverterTest.java#L58-L113), [BooleanConverterTest.java](https://github.com/apache/kafka/blob/ba74c3a289456f7346f2bece2cf76fcae55be9a4/connect/runtime/src/test/java/org/apache/kafka/connect/converters/BooleanConverterTest.java#L45-L110), [ByteArrayConverterTest.java](https://github.com/apache/kafka/blob/ba74c3a289456f7346f2bece2cf76fcae55be9a4/connect/runtime/src/test/java/org/apache/kafka/connect/converters/ByteArrayConverterTest.java#L38-L81)

**Uncertainties**
- This checkout does not include a `connect/json` source tree, so I did not anchor on `JsonConverter` even though some tests reference it.
- The “docs” here are source Javadocs/config docs in `WorkerConfig` and `ConnectorConfig`, not a separate published markdown or AsciiDoc page.