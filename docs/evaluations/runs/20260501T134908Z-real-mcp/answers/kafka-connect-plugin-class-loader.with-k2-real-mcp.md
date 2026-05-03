**Recommendation**
- Use the version-pinned Kafka 4.2 docs as the behavior contract for Connect plugin isolation and packaging: the Connect user guide, the connector development guide, and the 4.2 config reference for plugin version settings. They frame the expected manifest-based plugin visibility and isolation model. [https://kafka.apache.org/42/kafka-connect/user-guide/#part-0040] [https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0001] [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0040]
- Treat `PluginClassLoader` as the primary implementation anchor for isolated plugin loading. The K2 evidence shows it is a child-first loader that loads from its own URLs first, delegates to parent when a class is missing or not meant for isolation, and is registered as parallel capable. [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/PluginClassLoader.java]

**Implementation anchors**
- Primary: `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/PluginClassLoader.java` for the `loadClass` path and isolation rules. [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/PluginClassLoader.java]
- Adjacent context: `DelegatingClassLoader.java` for how plugin classloaders are resolved, and `ClassLoaderFactory.java` for creation/wiring. [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/DelegatingClassLoader.java] [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/ClassLoaderFactory.java]

**Tests to inspect or add**
- Inspect `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/MultiVersionTest.java` for versioned plugin loading and isolated plugin loading across discovery modes. [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/MultiVersionTest.java]
- Inspect `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/SynchronizationTest.java` for concurrent classloading and deadlock-sensitive behavior around delegating loaders. [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/SynchronizationTest.java]
- If you need a new regression, add one that proves `PluginClassLoader` prefers the plugin-local class over the parent for isolation, and falls back to parent only when the class is absent or non-isolated. That specific test was not surfaced by K2, so it is a suggested gap rather than an existing anchor.

**Citations**
- Docs: [https://kafka.apache.org/42/kafka-connect/user-guide/#part-0040]
- Docs: [https://kafka.apache.org/42/kafka-connect/connector-development-guide/#part-0001]
- Docs: [https://kafka.apache.org/42/configuration/kafka-connect-configs/#part-0040]
- Implementation: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/PluginClassLoader.java]
- Neighboring code: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/DelegatingClassLoader.java]
- Neighboring code: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/ClassLoaderFactory.java]
- Tests: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/MultiVersionTest.java]
- Tests: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/SynchronizationTest.java]

**Uncertainties**
- K2 did not return a dedicated `PluginClassLoaderTest`; the neighboring tests surfaced are `MultiVersionTest` and `SynchronizationTest`.
- The exact line-level semantics inside `PluginClassLoader.loadClass` are only partially visible in the returned snippet, so I am limiting implementation claims to what K2 explicitly surfaced.