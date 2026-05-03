**Recommendation**
Anchor the routing discussion on the Flink 2.2.0 REST API docs entry for subtask execution-attempt details, then verify behavior in `SubtaskCurrentAttemptDetailsHandler` and its dedicated test. The endpoint documented in 2.2.0 is `GET /jobs/:jobid/vertices/:vertexid/subtasks/:subtaskindex/attempts/:attempt`, which returns details for a specific execution attempt [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0043] [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0042].

**Implementation anchors**
- Version-pinned REST docs: `flink/flink-docs-release-2.2/docs/ops/rest_api/index.html` with the subtask-attempt endpoint and response schema [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0042] [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0043].
- Implementation class: `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/SubtaskCurrentAttemptDetailsHandler.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/SubtaskCurrentAttemptDetailsHandler.java].
- The handler is in the `org.apache.flink.runtime.rest.handler.job` package and is the concrete class to inspect for routing/attempt-details behavior [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/SubtaskCurrentAttemptDetailsHandler.java].

**Tests to inspect or add**
- Direct neighbor test: `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/SubtaskCurrentAttemptDetailsHandlerTest.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/SubtaskCurrentAttemptDetailsHandlerTest.java].
- Same-package handler tests that are good routing/shape references:
  - `JobDetailsHandlerTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java].
  - `JobConfigHandlerTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandlerTest.java].
- If you are adding coverage, mirror the direct handler test and add a route/mapping assertion for the `attempts/:attempt` path plus a response-shape assertion for `SubtaskExecutionAttemptDetailsInfo`.

**Citations**
- REST API docs and endpoint schema: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0042]
- REST API docs and endpoint path: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0043]
- Implementation class: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/SubtaskCurrentAttemptDetailsHandler.java]
- Direct test: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/SubtaskCurrentAttemptDetailsHandlerTest.java]
- Neighboring tests: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandlerTest.java]

**Uncertainties**
- The K2 evidence surfaced the implementation class and the direct test, but not the exact handler registration site in `WebMonitorEndpoint#initializeHandlers()`. If you need the full routing chain, that registration point should be verified separately.
- I did not get a dedicated routing test name beyond `SubtaskCurrentAttemptDetailsHandlerTest`; if you want stricter route-level coverage, it likely needs to be added rather than just inspected.