**Recommendation**
Use the 2.2.0 REST API reference for the Job Vertex flame-graph endpoint as the contract, then verify the handler’s request/response wiring against the runtime REST implementation. The key question is whether `JobVertexFlameGraphHandler` returns flame graphs for a specific job vertex only, and how it behaves on missing vertex IDs, missing samples, or invalid query parameters.

**Implementation anchors**
- Version-pinned docs: the Flink 2.2.x REST API docs section for the Job Vertex Flame Graph endpoint.
- Implementation class: `org.apache.flink.runtime.rest.handler.job.JobVertexFlameGraphHandler`
- Related message/parameter types: the job-vertex flame-graph REST message and parameter classes in `org.apache.flink.runtime.rest.messages.job`

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobVertexFlameGraphHandlerTest.java`
- Neighboring job-vertex handler tests in the same package, especially:
  - `JobVertexBackPressureHandlerTest`
  - `JobVertexDetailsHandlerTest`
  - `JobVertexAccumulatorsHandlerTest`
- Add/extend tests for:
  - valid flame-graph generation for a vertex
  - unknown job vertex ID
  - empty/no-sample response path
  - invalid request parameters, if the endpoint exposes any

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobVertexFlameGraphHandler.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobVertexFlameGraphHandlerTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobVertexBackPressureHandlerTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobVertexDetailsHandlerTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobVertexAccumulatorsHandlerTest.java`

**Uncertainties**
- I’m confident about the handler class and the test location, but I’m not fully certain of the exact version-pinned public docs URL/path from memory.
- I’m also not certain which neighboring job-vertex handler tests exist in 2.2.0 beyond the flame-graph test, so treat the adjacent test list as the most likely set to check first.