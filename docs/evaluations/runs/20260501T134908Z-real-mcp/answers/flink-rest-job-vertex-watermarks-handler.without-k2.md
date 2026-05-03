**Recommendation**
- Anchor the behavior on the Flink 2.2.0 REST API docs section for job-vertex watermarks, then verify the runtime handler’s request/response shape and error handling against that contract.
- If you are checking regressions, treat the handler test as the primary executable spec and the sibling job-vertex REST handlers as behavioral references.

**Implementation anchors**
- `JobVertexWatermarksHandler` in `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/`
- The Flink 2.2.0 REST API docs section that describes the job-vertex watermarks endpoint
- Any schema/DTO classes used by that handler in the same REST handler package

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobVertexWatermarksHandlerTest.java`
- Neighboring handler tests:
  - `JobVertexDetailsHandlerTest.java`
  - `JobVertexBackPressureHandlerTest.java`
  - `JobVertexAccumulatorsHandlerTest.java`
- Add coverage for:
  - successful watermark payload
  - empty or absent watermark data
  - missing job/vertex error paths
  - serialization stability of the returned JSON fields

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobVertexWatermarksHandler.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobVertexWatermarksHandlerTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobVertexDetailsHandlerTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobVertexBackPressureHandlerTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobVertexAccumulatorsHandlerTest.java`

**Uncertainties**
- I am not fully certain of the exact 2.2.0 docs file path from memory.
- I am also not fully certain of the exact response DTO names without checking the source.