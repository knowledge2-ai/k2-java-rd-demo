**Recommendation**
Anchor the answer on the Flink 2.2.0 REST API docs and the `DispatcherRestEndpoint` implementation. The K2 evidence shows dispatcher REST is part of `flink-runtime`, and the docs say new REST handlers are registered via `WebMonitorEndpoint#initializeHandlers()` rather than being added ad hoc elsewhere. [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002] [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/dispatcher/DispatcherRestEndpoint.java]

**Implementation anchors**
- Version-pinned docs: `flink/flink-docs-release-2.2/docs/ops/rest_api/index.html` for the 2.2.0 REST API contract and handler registration guidance. [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001]
- Implementation class: `flink-runtime/src/main/java/org/apache/flink/runtime/dispatcher/DispatcherRestEndpoint.java`, which K2 identifies as `DispatcherRestEndpoint extends WebMonitorEndpoint<DispatcherGateway>`. [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/dispatcher/DispatcherRestEndpoint.java]
- Registration point to inspect: `WebMonitorEndpoint#initializeHandlers()` per the REST docs, because that is where new request handlers are added in the runtime REST backend. [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002]

**Tests to inspect or add**
- No direct `DispatcherRestEndpointTest` surfaced in the K2 evidence.
- Neighboring tests that show the same REST-handler registration/testing pattern:
  - `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/checkpoints/CheckpointHandlersTest.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/checkpoints/CheckpointHandlersTest.java]
  - `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointHandlersTest.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointHandlersTest.java]
  - `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandlerTest.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandlerTest.java]
  - `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/cluster/JobManagerLogListHandlerTest.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/cluster/JobManagerLogListHandlerTest.java]
- If you add coverage, make it verify the dispatcher endpoint registers the expected handlers through the endpoint initialization path, not just individual handler logic.

**Citations**
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001], [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002]
- Implementation: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/dispatcher/DispatcherRestEndpoint.java]
- Neighboring tests: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/checkpoints/CheckpointHandlersTest.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointHandlersTest.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandlerTest.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/cluster/JobManagerLogListHandlerTest.java]

**Uncertainties**
- The K2 evidence did not include the exact `DispatcherRestEndpoint` method body, so I cannot name the concrete handler classes it registers without guessing.
- K2 surfaced SQL Gateway REST docs as well, but that is a different REST surface and should not be treated as the primary anchor for `DispatcherRestEndpoint`.