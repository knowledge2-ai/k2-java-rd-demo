**Recommendation**
- Anchor the review on the 2.2.x REST API docs for job submission, then trace the handler’s request parsing, validation, and submission wiring in `JobSubmitHandler`.
- Use the matching handler unit test as the executable spec, and compare it with nearby jar/submission handler tests for edge-case coverage.

**Implementation anchors**
- Docs: Flink 2.2.0 REST API docs for `POST /jobs/submit` in the `flink-docs-release-2.2` docs line.
- Code: `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobSubmitHandler.java`
- Same area, if you need the request contract: `JobSubmitHeaders` and the request body type used by the handler.

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobSubmitHandlerTest.java`
- Neighboring tests in the same package, especially:
  - `JarUploadHandlerTest`
  - `JarRunHandlerTest`
- Add or extend coverage for:
  - malformed submit payloads
  - missing jar references
  - invalid or duplicate parameters
  - the happy path that proves the submission request is constructed and dispatched correctly

**Citations**
- `org.apache.flink.runtime.rest.handler.job.JobSubmitHandler` (`flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobSubmitHandler.java`)
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobSubmitHandlerTest.java`

**Uncertainties**
- I’m not fully certain of the exact versioned docs filename or URL for the 2.2.0 docs without browsing.
