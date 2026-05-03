**Recommendation**
- Anchor the explanation on the Kafka Connect 4.2.0 docs section for `plugin.path`, plugin isolation, and classloader separation.
- Then trace `org.apache.kafka.connect.runtime.isolation.Plugins` as the orchestration point for discovery and connector instantiation, and follow the handoff into the delegating/plugin classloaders.

**Implementation anchors**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/Plugins.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/DelegatingClassLoader.java`
- Inspect `PluginClassLoader` in the same package if you need the actual plugin-bound load boundary.
- The flow to document is: scan plugin locations -> build plugin index/map -> resolve connector class name -> load through the plugin-specific classloader -> instantiate the connector.

**Tests to inspect or add**
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/PluginsTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/DelegatingClassLoaderTest.java`
- If you add a regression, make it about classpath-vs-`plugin.path` shadowing, ambiguous plugin resolution, and connector loading from the plugin classloader rather than the worker classpath.

**Citations**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/Plugins.java`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/DelegatingClassLoader.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/PluginsTest.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/DelegatingClassLoaderTest.java`

**Uncertainties**
- I cannot verify the exact 4.2.0 docs URL here, so I’m anchoring on the versioned Kafka Connect docs topic rather than a hard link.
- I’m confident about `Plugins` and `DelegatingClassLoader`; I would want repo access to confirm the exact neighboring scanner test filenames if you need a complete file list.