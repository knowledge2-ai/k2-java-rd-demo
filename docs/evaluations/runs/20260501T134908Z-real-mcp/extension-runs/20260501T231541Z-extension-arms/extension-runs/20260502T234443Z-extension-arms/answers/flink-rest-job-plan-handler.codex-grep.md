**Recommendation**
`JobPlanHandler` is a thin REST adapter: `GET /jobs/:jobid/plan` resolves the job’s `AccessExecutionGraph`, reads `executionGraph.getPlan()`, and returns it as `JobPlanInfo`. The returned payload is the plan metadata object, not a recomputed plan, so the handler’s job is serialization and endpoint wiring.

**Implementation anchors**
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java#L44-L79` for the handler flow: `handleRequest(...) -> new JobPlanInfo(executionGraph.getPlan())`, plus archived JSON path emission.
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobPlanHeaders.java#L27-L73` for the REST contract: `GET`, `/jobs/:jobid/plan`, `200 OK`, and the “Returns the dataflow plan of a job” description.
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobPlanInfo.java#L52-L417` for the response schema: top-level `plan`, then `jid`, `name`, `type`, `nodes`, and node/input metadata.
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/jobgraph/jsonplan/JsonPlanGenerator.java#L51-L147` for how the plan metadata is populated from the job graph.
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/webmonitor/WebMonitorEndpoint.java#L411-L418` for endpoint registration.
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/versioning/RuntimeRestAPIVersion.java#L19-L59` plus `repo://apache/flink@release-2.2.0/flink-docs/src/main/java/org/apache/flink/docs/rest/RuntimeRestAPIDocGenerator.java#L62-L83` and `repo://apache/flink@release-2.2.0/flink-docs/src/main/java/org/apache/flink/docs/rest/RuntimeOpenApiSpecGenerator.java#L62-L83` for the version-pinned docs path. In 2.2.0, the doc generator emits `rest_v1_dispatcher.html` and `rest_v1_dispatcher.yml`.

**Tests to inspect or add**
- `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/JobPlanInfoTest.java#L28-L41` for marshal/unmarshal coverage of the response body.
- `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/jobgraph/jsonplan/JsonGeneratorTest.java#L106-L139` for the core plan fields (`jobId`, `name`, `type`, node count, node IDs/descriptions).
- `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java#L57-L118` for a nearby pattern that verifies plan/stream-graph metadata propagation through a REST handler.
- `repo://apache/flink@release-2.2.0/flink-docs/src/test/java/org/apache/flink/docs/rest/RestAPIDocGeneratorTest.java#L28-L67` and `repo://apache/flink@release-2.2.0/flink-docs/src/test/java/org/apache/flink/docs/rest/OpenApiSpecGeneratorTest.java#L28-L106` for versioned REST-doc generation behavior.
- Add a dedicated `JobPlanHandlerTest` if you want direct handler-level coverage; I did not find one in 2.2.0.

**Citations**
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java#L44-L79`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobPlanHeaders.java#L27-L73`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobPlanInfo.java#L52-L417`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/jobgraph/jsonplan/JsonPlanGenerator.java#L51-L147`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/webmonitor/WebMonitorEndpoint.java#L411-L418`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/versioning/RuntimeRestAPIVersion.java#L19-L59`
- `repo://apache/flink@release-2.2.0/flink-docs/src/main/java/org/apache/flink/docs/rest/RuntimeRestAPIDocGenerator.java#L62-L83`
- `repo://apache/flink@release-2.2.0/flink-docs/src/main/java/org/apache/flink/docs/rest/RuntimeOpenApiSpecGenerator.java#L62-L83`
- `repo://apache/flink@release-2.2.0/flink-docs/README.md#L24-L36`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/JobPlanInfoTest.java#L28-L41`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/jobgraph/jsonplan/JsonGeneratorTest.java#L106-L139`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java#L57-L118`
- `repo://apache/flink@release-2.2.0/flink-docs/src/test/java/org/apache/flink/docs/rest/RestAPIDocGeneratorTest.java#L28-L67`
- `repo://apache/flink@release-2.2.0/flink-docs/src/test/java/org/apache/flink/docs/rest/OpenApiSpecGeneratorTest.java#L28-L106`

**Uncertainties**
- I did not find a rendered, checked-in markdown/HTML page for this exact endpoint in the checkout, so the safest version-pinned docs anchor is the generator output path (`rest_v1_dispatcher.*`) plus the generator/README, not a concrete source doc page.
- There is no obvious dedicated `JobPlanHandlerTest` in 2.2.0, so handler-level behavior is currently inferred from the implementation and neighboring serialization/generator tests.