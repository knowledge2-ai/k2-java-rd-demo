**Recommendation**
- Anchor the lifecycle explanation on the Flink 2.2.0 REST API page and `RestServerEndpoint` itself.
- The abstract lifecycle to trace is: construction from config, `start()` bootstraps handlers/file-upload plumbing and binds the server, then `closeAsync()` tears it down.

**Implementation anchors**
- Version-pinned docs: `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/deployment/advanced/rest_api/`
- Core class: `flink-runtime/src/main/java/org/apache/flink/runtime/rest/RestServerEndpoint.java`
- Follow the concrete JobManager/Dispatcher-side subclass that wires this endpoint into the runtime, if you need the full call chain.

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/RestServerEndpointTest.java`
- Nearby tests in `flink-runtime/src/test/java/org/apache/flink/runtime/rest/` that cover handler wiring, config, and shutdown behavior
- Add coverage for start-failure cleanup and idempotent shutdown if those paths are not already explicit

**Citations**
- `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/deployment/advanced/rest_api/`
- `flink-runtime/src/main/java/org/apache/flink/runtime/rest/RestServerEndpoint.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/RestServerEndpointTest.java`

**Uncertainties**
- I am not fully certain whether the 2.2.0 docs source file is named `rest_api.md` in the repo tree; the version-pinned REST API page above is the right public anchor, but the source filename may differ slightly.