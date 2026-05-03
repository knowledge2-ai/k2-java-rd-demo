**Recommendation**
Anchor the answer on `JobPlanHandler` itself and trace the data path from `AccessExecutionGraph.getPlan()` to `JobPlanInfo`. The handler is a thin REST adapter: `handleRequest()` returns `createJobPlanInfo(executionGraph)`, and `archiveJsonWithPath()` archives the same `JobPlanInfo` under the job-specific endpoint path. The concrete plan data is produced earlier when the execution graph is built from `JsonPlanGenerator.generatePlan(jobGraph)` and stored via `executionGraph.setPlan(...)`. [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java#L60-L80] [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/executiongraph/DefaultExecutionGraphBuilder.java#L171-L197]

**Implementation anchors**
- `JobPlanHandler.handleRequest(...)` directly returns `createJobPlanInfo(executionGraph)`, so the REST response is just a wrapper around the execution graph’s stored plan. [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java#L60-L80]
- `createJobPlanInfo(...)` constructs `new JobPlanInfo(executionGraph.getPlan())`, which is the key handoff from runtime state to REST DTO. [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java#L77-L80]
- `archiveJsonWithPath(...)` uses `getTargetRestEndpointURL()` plus the job-id path parameter to archive the same response body at the REST endpoint path. [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java#L67-L75]
- `JobPlanHeaders` defines the contract: `GET`, empty request body, `JobPlanInfo` response, `200 OK`, and the endpoint description “Returns the dataflow plan of a job.” [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobPlanHeaders.java#L34-L72]
- `DefaultExecutionGraphBuilder` is where the plan metadata is populated, via `JsonPlanGenerator.generatePlan(jobGraph)`, with a fallback to an empty `JobPlanInfo.Plan` if generation fails. [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/executiongraph/DefaultExecutionGraphBuilder.java#L171-L197]

**Tests to inspect or add**
- `JobPlanInfoTest` should be the first serialization anchor for the REST DTO itself. [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/JobPlanInfoTest.java]
- `JsonGeneratorTest` covers the plan-generation side, including core fields like job id, name, type, and non-empty nodes. [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/jobgraph/jsonplan/JsonGeneratorTest.java#L110-L136]
- `JobDetailsHandlerTest` is a nearby REST-handler pattern worth mirroring if you want a handler-level regression test for a JSON-backed field. [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java#L99-L119]
- If you add coverage, a dedicated `JobPlanHandler` test should assert `handleRequest()` returns the wrapped plan and `archiveJsonWithPath()` uses the endpoint path built from the job ID. [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java#L60-L80]

**Citations**
- `JobPlanHandler`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java#L60-L80]
- `JobPlanHeaders`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobPlanHeaders.java#L34-L72]
- `DefaultExecutionGraphBuilder`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/executiongraph/DefaultExecutionGraphBuilder.java#L171-L197]
- `JobPlanInfo`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobPlanInfo.java#L181-L306]
- Version-pinned REST docs generators: [repo://apache/flink@release-2.2.0/flink-docs/src/main/java/org/apache/flink/docs/rest/RuntimeRestAPIDocGenerator.java#L64-L85] [repo://apache/flink@release-2.2.0/flink-docs/src/main/java/org/apache/flink/docs/rest/RuntimeOpenApiSpecGenerator.java#L40-L62]
- REST versioning: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/versioning/RuntimeRestAPIVersion.java#L26-L52]
- Neighboring tests: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/JobPlanInfoTest.java] [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/jobgraph/jsonplan/JsonGeneratorTest.java#L110-L136] [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java#L99-L119]

**Uncertainties**
- No dedicated `JobPlanHandlerTest` surfaced in the retrieved evidence; the nearest anchors are the DTO serialization test and the JSON plan generator test.