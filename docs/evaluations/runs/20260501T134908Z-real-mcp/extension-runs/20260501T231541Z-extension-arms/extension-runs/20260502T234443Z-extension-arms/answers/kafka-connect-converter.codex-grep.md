**Recommendation**
Anchor the answer on the worker/connector config docs plus the runtime wiring that turns `key.converter` vs `value.converter` into the `isKey` flag. In 4.2.0, the behavior is not in `Converter` alone; it is the combination of `Plugins.newConverter(...)` deciding key/value, and the concrete converter implementation reading `converter.type` or the `boolean isKey` overload.

**Implementation anchors**
- `Converter` defines the contract and the key/value-aware overloads, but not the policy itself: `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/Converter.java#L28-L98`
- `StringConverter` is the concrete implementation that maps `configure(Map, boolean)` to `converter.type=key|value`, then branches on `ConverterConfig.type()`: `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/StringConverter.java#L33-L83`
- `Plugins.newConverter(...)` is the runtime decision point that infers `isKeyConverter` from the config property name and passes it into `plugin.configure(...)`: `repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/Plugins.java#L457-L476`
- The version-pinned config docs live in source here:
  - `WorkerConfig` docs for `key.converter`, `value.converter`, and `*.plugin.version`: `repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConfig.java#L74-L94`
  - `ConnectorConfig` mirrors those docs for connector-scoped overrides and version pinning: `repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/ConnectorConfig.java#L97-L123`

**Tests to inspect or add**
- `PluginsTest.shouldInstantiateAndConfigureConverters` and `shouldInstantiateAndConfigureInternalConverters` verify the worker passes the right config prefix and that internal converters get `converter.type`: `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/PluginsTest.java#L129-L146`
- `PluginsTest` also contains the local test double that requires `converter.type` to be set, which is useful for asserting the contract: `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/PluginsTest.java#L693-L739`
- `WorkerTest.testAddRemoveSourceTask`, `testCleanupTasksOnStop`, and `testConverterOverrides` cover the connector-vs-worker fallback and versioned key/value converter loading: `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerTest.java#L604-L650` and `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerTest.java#L961-L1070`
- `MultiVersionTest.testVersionedConverter` is the best neighbor for pinned converter versions on key vs value: `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/MultiVersionTest.java#L260-L285`
- `ErrorHandlingTaskTest` shows the explicit `converter.type=value` setup when the same converter instance is used on both sides: `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ErrorHandlingTaskTest.java#L419-L457`
- If you want an end-to-end check, `ConnectWorkerIntegrationTest` also exercises `StringConverter` in a real worker flow: `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ConnectWorkerIntegrationTest.java#L1020-L1045`

**Citations**
- `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/Converter.java#L28-L98`
- `repo://apache/kafka@4.2/connect/api/src/main/java/org/apache/kafka/connect/storage/StringConverter.java#L33-L83`
- `repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/Plugins.java#L457-L476`
- `repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConfig.java#L74-L94`
- `repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/ConnectorConfig.java#L97-L123`
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/PluginsTest.java#L129-L146`
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/PluginsTest.java#L693-L739`
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerTest.java#L604-L650`
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerTest.java#L961-L1070`
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/MultiVersionTest.java#L260-L285`
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/ErrorHandlingTaskTest.java#L419-L457`
- `repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/integration/ConnectWorkerIntegrationTest.java#L1020-L1045`

**Uncertainties**
- This checkout does not include a separate top-level docs tree, so I anchored on source-level docs/comments in `WorkerConfig` and `ConnectorConfig`.
- The `JsonConverter` source itself is not present here, so JSON-specific converter internals cannot be cited directly from this checkout; the behavior is inferred from the worker/tests that configure it.