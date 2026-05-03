**Recommendation**
Anchor the explanation on the 2.2.0 REST API docs for the job-vertex back-pressure endpoint, then tie it to the handler implementation and the handler-level unit test that exercises the request/response path. For this area, the most defensible read is: the endpoint is a job-vertex-scoped REST handler, not a cluster-wide metric, and the handler/test pair should be the primary source of truth.

**Implementation anchors**
- Version-pinned docs: Flink 2.2 REST API docs, back-pressure section for job vertices, under the 2.2 docs branch. Public docs path is typically `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/`.
- Implementation class: `flink-runtime/src/main/java/org/apache/flink/runtime/webmonitor/handlers/JobVertexBackPressureHandler.java`
- Likely neighboring handler classes worth reading for behavior and routing context:
  - `JobVertexDetailsHandler`
  - `JobVertexTaskManagersHandler`
  - any shared base/request-parameter handler in the same `webmonitor/handlers` package

**Tests to inspect or add**
- Primary test: `flink-runtime/src/test/java/org/apache/flink/runtime/webmonitor/handlers/JobVertexBackPressureHandlerTest.java`
- Nearby tests to compare conventions and endpoint wiring:
  - `JobVertexDetailsHandlerTest`
  - `JobVertexTaskManagersHandlerTest`
  - any back-pressure stats/request tests in the same package if present
- If you are adding coverage, check for:
  - correct job-vertex path parameter handling
  - 200 vs error behavior for missing/unknown job vertex IDs
  - JSON schema/fields returned by the handler
  - any caching, sampling, or “latest stats” semantics

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/webmonitor/handlers/JobVertexBackPressureHandler.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/webmonitor/handlers/JobVertexBackPressureHandlerTest.java`
- `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/`

**Uncertainties**
- I’m not fully certain whether the 2.2.0 code path still lives exactly under `org.apache.flink.runtime.webmonitor.handlers` versus a newer REST package in every downstream branch, but that is the likely 2.2.x location.
- I’m also not fully certain of the exact docs subsection anchor for the back-pressure endpoint without checking the published page.