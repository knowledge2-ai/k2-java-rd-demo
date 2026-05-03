**Recommendation**
Explain `GET /jobs/:jobid/plan` as a thin REST wrapper over the execution graph’s stored plan. `JobPlanHandler` pulls the `AccessExecutionGraph`, calls `executionGraph.getPlan()`, wraps that in `JobPlanInfo`, and returns it as the response body. The JSON payload is a single top-level `plan` object with job metadata plus per-node plan metadata. `JobPlanHeaders` is the contract for the endpoint, and `JobPlanInfo` is the serialized response model.

**Implementation anchors**
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java#L43-L78`  
  Handler implementation; `handleRequest()` returns `new JobPlanInfo(executionGraph.getPlan())`, and `archiveJsonWithPath()` uses the same response for archived REST JSON.
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobPlanHeaders.java#L26-L73`  
  Endpoint contract: `GET`, status `200 OK`, URL `/jobs/:jobid/plan`, description `"Returns the dataflow plan of a job."`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobPlanInfo.java#L51-L60` and `#L176-L197`  
  Response model: top-level `plan`, then `Plan` fields `jid`, `name`, `type`, `nodes`; nested nodes carry `id`, `parallelism`, `operator`, `operator_strategy`, `description`, `optimizer_properties`, and `inputs`.
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/jobgraph/jsonplan/JsonPlanGenerator.java#L51-L147`  
  Source of the plan object: converts `JobGraph` into `JobPlanInfo.Plan`, including node/input metadata.
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/RuntimeMessageHeaders.java#L41-L44`  
  Version default for runtime REST headers is `V1`; `JobPlanHeaders` inherits this.
- `repo://apache/flink@release-2.2.0/flink-docs/src/main/java/org/apache/flink/docs/rest/RuntimeRestAPIDocGenerator.java#L72-L83` and `repo://apache/flink@release-2.2.0/flink-docs/src/main/java/org/apache/flink/docs/rest/RuntimeOpenApiSpecGenerator.java#L48-L60`  
  Version-pinned doc generation for the runtime API: production docs emit `V1` and skip `V0`.

**Tests to inspect or add**
- `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/JobPlanInfoTest.java#L28-L40`  
  Marshalling/unmarshalling coverage for the response model.
- `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/jobgraph/jsonplan/JsonGeneratorTest.java#L53-L147`  
  Verifies plan generation from a `JobGraph`, including job metadata and node list contents.
- `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/job/JobDetailsInfoTest.java#L40-L89`  
  Confirms `JobDetailsInfo` carries a `JobPlanInfo.Plan`, which is the neighboring data path.
- `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java#L112-L118`  
  Checks related handler wiring for the stream-graph JSON; useful as the nearest handler-level pattern.
- Add if you want direct endpoint coverage: `JobPlanHandlerTest`  
  I did not find an existing handler-specific unit test for `JobPlanHandler`, so a focused test would be the natural gap.

**Citations**
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java#L43-L78`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobPlanHeaders.java#L26-L73`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobPlanInfo.java#L51-L60`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobPlanInfo.java#L176-L197`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/jobgraph/jsonplan/JsonPlanGenerator.java#L51-L147`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/RuntimeMessageHeaders.java#L41-L44`
- `repo://apache/flink@release-2.2.0/flink-docs/src/main/java/org/apache/flink/docs/rest/RuntimeRestAPIDocGenerator.java#L72-L83`
- `repo://apache/flink@release-2.2.0/flink-docs/src/main/java/org/apache/flink/docs/rest/RuntimeOpenApiSpecGenerator.java#L48-L60`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/JobPlanInfoTest.java#L28-L40`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/jobgraph/jsonplan/JsonGeneratorTest.java#L53-L147`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/job/JobDetailsInfoTest.java#L40-L89`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java#L112-L118`

**Uncertainties**
- I did not find a direct `JobPlanHandlerTest`; the closest coverage is model marshalling plus `JsonPlanGenerator` and neighboring job-details tests.
- The repo’s docs generator is version-aware, but the endpoint itself is not version-specialized in `JobPlanHeaders`; it inherits the runtime default `V1`.