**Recommendation**
`JobPlanHandler` should be treated as a thin REST adapter: it serves `GET /jobs/:jobid/plan`, resolves the job’s graph state, and returns the serialized plan payload in the REST response DTO rather than exposing internal graph objects. For Flink 2.2.0, anchor the behavior on the version-pinned REST API docs, the handler implementation, and the plan response model.

**Implementation anchors**
- Version-pinned docs: Apache Flink 2.2 REST API docs, job-plan section  
  `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/`
- Handler implementation: `flink-runtime-web/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java`
- Response model: `flink-runtime-web/src/main/java/org/apache/flink/runtime/rest/messages/job/JobPlanInfo.java` or the equivalent 2.2.0 message package
- Request/response wiring: the corresponding plan-endpoint headers class, likely `JobPlanHeaders`

**Tests to inspect or add**
- `flink-runtime-web/src/test/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandlerTest.java`
- Nearby job REST handler tests in the same package for the same request/response and error-handling patterns
- Add assertions that:
  - the handler returns the exact plan JSON/metadata produced by the job graph
  - unknown job IDs map to the documented REST error path
  - the response shape stays stable across serialization

**Citations**
- `flink-runtime-web/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java`
- `flink-runtime-web/src/test/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandlerTest.java`
- `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/`

**Uncertainties**
- I am not fully certain of the exact 2.2.0 package path for the response DTO and headers class without inspecting the tree.
- The handler may read from `ArchivedExecutionGraph` or `JobGraph` depending on the exact 2.2.0 wiring, but the external behavior is the same: return the serialized plan payload through REST.