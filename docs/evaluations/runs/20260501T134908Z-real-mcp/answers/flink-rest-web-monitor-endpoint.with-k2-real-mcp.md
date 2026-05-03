**Recommendation**
Anchor the answer on the Flink 2.2.0 REST docs and the `flink-runtime` implementation. The docs explicitly say `WebMonitorEndpoint` is the core class for the REST backend and that new handlers are wired in `WebMonitorEndpoint#initializeHandlers()` [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002]. The endpoint class itself is `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/webmonitor/WebMonitorEndpoint.java`.

**Implementation anchors**
- Version-pinned REST docs: Flink 2.2.0 REST API overview and “Developing” section, which states that the backend lives in `flink-runtime`, the core class is `WebMonitorEndpoint`, and new requests are added by creating `MessageHeaders`, `AbstractRestHandler`, and registering the handler in `initializeHandlers()` [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002].
- Implementation class: `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/webmonitor/WebMonitorEndpoint.java`.
- Related internal contract: `RestHandlerSpecification` in `flink-runtime` is the handler-spec abstraction used by the endpoint wiring path [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/RestHandlerSpecification.java].

**Tests to inspect or add**
- Primary neighboring test: `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/webmonitor/WebMonitorEndpointTest.java`.
- Additional nearby REST-handler tests that are good anchors for handler-registration behavior and patterns:
  - `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobsOverviewHandlerTest.java`
  - `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointHandlersTest.java`
  - `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/savepoints/StopWithSavepointHandlersTest.java`
  - `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/async/AbstractAsynchronousOperationHandlersTest.java`
- If adding coverage, target assertions that `WebMonitorEndpoint` registers the expected handler specs in `initializeHandlers()` and that endpoint lifecycle behavior still works.

**Citations**
- REST docs, “Developing” section: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002]
- REST docs, API overview: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001]
- `WebMonitorEndpoint`: `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/webmonitor/WebMonitorEndpoint.java`
- `WebMonitorEndpointTest`: `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/webmonitor/WebMonitorEndpointTest.java`
- `RestHandlerSpecification`: `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/RestHandlerSpecification.java`

**Uncertainties**
- The K2 evidence confirms the registration pattern and the endpoint class, but it does not fully enumerate every handler added by `initializeHandlers()`. I would treat any handler-by-handler list as incomplete unless verified directly from the source file.