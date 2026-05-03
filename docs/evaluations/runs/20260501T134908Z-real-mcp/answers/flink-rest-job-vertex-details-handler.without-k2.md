**Recommendation**
Use the Flink 2.2.0 REST API docs as the normative contract for the vertex-scoped endpoint, then anchor the implementation around `JobVertexDetailsHandler` and the adjacent vertex-level handler tests in `flink-runtime`.

**Implementation anchors**
- Version-pinned docs: Flink 2.2 REST API page for the `Job Vertex Details` endpoint.
- Handler class: `org.apache.flink.runtime.rest.handler.job.JobVertexDetailsHandler`
- Response/model companions to inspect alongside it: `JobVertexDetailsMessageParameters` and the vertex-details response DTO used by that handler.

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobVertexDetailsHandlerTest.java`
- Nearby vertex-scoped handler tests in the same package, especially the `JobVertex*HandlerTest` cases that exercise the same path-parameter pattern and serialization/validation flow.
- If you are adding coverage, mirror the existing test style for path parameters, request validation, and response shape rather than adding a new bespoke harness.

**Citations**
- `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/`
- `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobVertexDetailsHandler.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobVertexDetailsHandlerTest.java`

**Uncertainties**
- I’m confident about the handler name and the general package shape, but I can’t verify the exact 2.2.0 doc anchor text or any nearby test filenames beyond the obvious `JobVertexDetailsHandlerTest` without checking the repository.
- Flink’s REST handler package layout can shift slightly across minor branches, so treat the exact path as “verify against the 2.2.0 tag” if you need patch-level certainty.