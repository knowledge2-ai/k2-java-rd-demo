**Recommendation**
Use the 4.2-pinned Kafka Connect docs as context, but anchor the actual behavior claim on `DelegatingClassLoader` itself. The class Javadoc says Connect uses a child-first delegation model for plugin classes and parent delegation for non-plugin classes, so that is the canonical implementation source for the answer [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/DelegatingClassLoader.java].

**Implementation anchors**
- Primary implementation: `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/DelegatingClassLoader.java` [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/DelegatingClassLoader.java]
- Nearby supporting code: `ClassLoaderFactory` and `LoaderSwap`, which sit in the same isolation package and frame how plugin classloaders are constructed and swapped [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/ClassLoaderFactory.java] [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/LoaderSwap.java]
- Version-pinned docs to cite for context:
  - Kafka Connect landing page for 4.2 [https://kafka.apache.org/42/kafka-connect/]
  - Connector Development Guide 4.2 [https://kafka.apache.org/42/kafka-connect/connector-development-guide/]
  - Kafka Connect User Guide 4.2 [https://kafka.apache.org/42/kafka-connect/user-guide/]
  - Kafka Connect configuration reference 4.2 [https://kafka.apache.org/42/configuration/kafka-connect-configs/]

**Tests to inspect or add**
- Existing focused unit test: `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/DelegatingClassLoaderTest.java` [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/DelegatingClassLoaderTest.java]
- Neighboring concurrency/integration coverage: `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/SynchronizationTest.java` [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/SynchronizationTest.java]
- If adding coverage, target:
  - child-first resolution for plugin classes
  - parent delegation for non-plugin classes
  - concurrent loading / parallel-capable behavior
  - plugin isolation across multiple plugin classloaders

**Citations**
- Docs: [https://kafka.apache.org/42/kafka-connect/]
- Docs: [https://kafka.apache.org/42/kafka-connect/connector-development-guide/]
- Docs: [https://kafka.apache.org/42/kafka-connect/user-guide/]
- Docs: [https://kafka.apache.org/42/configuration/kafka-connect-configs/]
- Implementation: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/DelegatingClassLoader.java]
- Neighboring code: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/ClassLoaderFactory.java]
- Neighboring code: [repo://apache/kafka@4.2/connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/LoaderSwap.java]
- Test: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/DelegatingClassLoaderTest.java]
- Test: [repo://apache/kafka@4.2/connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/SynchronizationTest.java]

**Uncertainties**
- The K2 evidence does not expose a docs page that explicitly documents `DelegatingClassLoader` by name, so the docs above are contextual anchors rather than direct behavioral specs.
- I did not inspect the full test bodies here, so any finer-grained assertions should be verified directly in `DelegatingClassLoaderTest` and `SynchronizationTest` before relying on them.