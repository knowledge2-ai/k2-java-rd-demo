**Recommendation**
Use the 2.2.0 REST API reference for `GET /jobs/:jobid/config` as the spec, and verify it against the runtime handler and its unit test. The endpoint exposes a job’s effective configuration over REST as structured JSON key/value data.

**Implementation anchors**
- Version-pinned docs: `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api.html`  
- Handler implementation: `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandler.java`
- Likely adjacent implementation types in the same area: `JobConfigHeaders` and the response DTO used by that handler

**Tests to inspect or add**
- Existing unit test: `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandlerTest.java`
- Neighboring tests in the same package: other `.../handler/job/` REST handler tests for job-level GET endpoints
- Add or confirm coverage for:
  - missing/unknown job id
  - empty configuration
  - serialization edge cases in keys/values

**Citations**
- `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api.html`
- `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandler.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandlerTest.java`

**Uncertainties**
- I’m not fully certain of the exact rendered docs anchor for the `/jobs/:jobid/config` section without checking the 2.2.0 site directly.
- I’m also not certain of the exact response POJO name from memory; verify the handler’s return type in source before quoting it.