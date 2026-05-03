**Recommendation**
- Treat `JobPlanHandler` as the REST source of truth for job plan metadata. It serves `GET /jobs/:jobid/plan`, reads the plan from `AccessExecutionGraph.getPlan()`, wraps it in `JobPlanInfo`, and also archives the same payload for history.
- For docs, anchor on Flink’s generated runtime REST/OpenAPI docs, not a handwritten page. In this tree those docs are generated per `RuntimeRestAPIVersion`, and the docs README explicitly says to regenerate when a REST handler or its message classes change.

**Implementation anchors**
- [`JobPlanHandler.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java#L43) is the key implementation: `handleRequest()` returns `new JobPlanInfo(executionGraph.getPlan())`, and `archiveJsonWithPath()` emits the same response under the job-specific path.
- [`JobPlanHeaders.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobPlanHeaders.java#L26) pins the contract: `GET`, `200 OK`, URL `/jobs/:jobid/plan`, and the endpoint description.
- [`JobPlanInfo.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobPlanInfo.java#L51) defines the JSON shape: a top-level `plan` object with `jid`, `name`, `type`, and `nodes`; each node carries the operator and edge metadata.
- [`WebMonitorEndpoint.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-runtime/src/main/java/org/apache/flink/runtime/webmonitor/WebMonitorEndpoint.java#L411) shows where the handler is registered in the JobManager REST endpoint wiring.
- Versioned docs anchor: [`RuntimeRestAPIDocGenerator.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-docs/src/main/java/org/apache/flink/docs/rest/RuntimeRestAPIDocGenerator.java#L31) and [`RuntimeOpenApiSpecGenerator.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-docs/src/main/java/org/apache/flink/docs/rest/RuntimeOpenApiSpecGenerator.java#L31) generate per-version docs; [`flink-docs/README.md`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-docs/README.md#L24) says docs must be regenerated when handlers or message classes change.

**Tests to inspect or add**
- [`JobPlanInfoTest.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/JobPlanInfoTest.java#L28) covers marshalling/unmarshalling of the response body.
- [`JsonGeneratorTest.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-runtime/src/test/java/org/apache/flink/runtime/jobgraph/jsonplan/JsonGeneratorTest.java#L53) verifies `JsonPlanGenerator.generatePlan()` fills the `JobPlanInfo.Plan` fields and nodes correctly.
- [`JobDetailsInfoTest.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/job/JobDetailsInfoTest.java#L40) is a good neighboring serialization test because it embeds `JobPlanInfo.Plan` in the larger job-details payload.
- For runtime/lifecycle coverage, also inspect [`ArchivedExecutionGraphTest.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-runtime/src/test/java/org/apache/flink/runtime/executiongraph/ArchivedExecutionGraphTest.java#L242) and [`AdaptiveSchedulerTest.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-runtime/src/test/java/org/apache/flink/runtime/scheduler/adaptive/AdaptiveSchedulerTest.java#L358).
- If you want endpoint-specific coverage, add a handler/integration test for `GET /jobs/:jobid/plan`; I did not find an existing dedicated `JobPlanHandler` test in the local tree.

**Citations**
- [`JobPlanHandler.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java#L43)
- [`JobPlanHeaders.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobPlanHeaders.java#L26)
- [`JobPlanInfo.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobPlanInfo.java#L51)
- [`RuntimeRestAPIDocGenerator.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-docs/src/main/java/org/apache/flink/docs/rest/RuntimeRestAPIDocGenerator.java#L31)
- [`RuntimeOpenApiSpecGenerator.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-docs/src/main/java/org/apache/flink/docs/rest/RuntimeOpenApiSpecGenerator.java#L31)
- [`flink-docs/README.md`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-docs/README.md#L24)
- [`JobPlanInfoTest.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/JobPlanInfoTest.java#L28)
- [`JsonGeneratorTest.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-runtime/src/test/java/org/apache/flink/runtime/jobgraph/jsonplan/JsonGeneratorTest.java#L53)
- [`JobDetailsInfoTest.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/job/JobDetailsInfoTest.java#L40)
- [`ArchivedExecutionGraphTest.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-runtime/src/test/java/org/apache/flink/runtime/executiongraph/ArchivedExecutionGraphTest.java#L242)
- [`AdaptiveSchedulerTest.java`](https://github.com/apache/flink/blob/5a336892424a9458653ead89610bf60d771ab8d7/flink-runtime/src/test/java/org/apache/flink/runtime/scheduler/adaptive/AdaptiveSchedulerTest.java#L358)

**Uncertainties**
- There is no dedicated `JobPlanHandler` endpoint test in the nearby test set, so the strongest existing evidence is the message-marshalling and plan-generation coverage.
- I did not locate a checked-in handwritten REST docs page for this endpoint; the repo appears to rely on generated runtime REST/OpenAPI artifacts instead.