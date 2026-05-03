**Recommendation**

`flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java` is the implementation to anchor on for Flink 2.2.0. The public contract is `GET /jobs/:jobid/plan`, and the response is the `JobPlanInfo` JSON payload that carries the plan metadata, including the nested `plan` object described in the 2.2.0 REST API docs [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0030].

**Implementation anchors**

- `JobPlanHandler` is the concrete REST handler class for the job plan endpoint in `flink-runtime` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java].
- The handler is wired against the REST message layer through `JobPlanInfo`, `EmptyRequestBody`, `JobIDPathParameter`, `JobMessageParameters`, and `MessageHeaders`, so the endpoint is defined as a typed REST handler rather than ad hoc JSON assembly [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java].
- The docs pin the response schema for `/jobs/:jobid/plan` to `JobPlanInfo`, with a nested `plan` object and fields such as `jid`, `name`, `nodes`, and `optimizer_properties` [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0030].
- The REST API docs also state the implementation pattern for new requests: add `MessageHeaders`, add an `AbstractRestHandler`, and register it in `WebMonitorEndpoint`, which is the right framing for how `JobPlanHandler` fits the REST stack [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002].
- The retrieved class excerpt also imports `ArchivedJson` and `OnlyExecutionGraphJsonArchivist`, which suggests the handler participates in the execution-graph JSON archival path for plan metadata, but the exact body-building logic was not visible in the evidence returned [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java].

**Tests to inspect or add**

- Inspect `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java` as the closest neighboring job-handler test in the same package [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java].
- Inspect `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobsOverviewHandlerTest.java` for the same REST-handler patterns around job-scoped response shaping [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobsOverviewHandlerTest.java].
- Inspect `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandlerTest.java` as another direct neighbor in the same package and a likely template for request/response assertions [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandlerTest.java].
- If coverage is missing, add a focused `JobPlanHandlerTest` that asserts the endpoint returns `JobPlanInfo` and that the JSON shape matches the documented nested `plan` schema for `/jobs/:jobid/plan` [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0030].

**Citations**

- Implementation: `JobPlanHandler.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java]
- Docs: Flink 2.2 REST API `/jobs/:jobid/plan` [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0030]
- Docs: Flink 2.2 REST API development guidance [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002]
- Tests: `JobDetailsHandlerTest.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java]
- Tests: `JobsOverviewHandlerTest.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobsOverviewHandlerTest.java]
- Tests: `JobConfigHandlerTest.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandlerTest.java]

**Uncertainties**

- The retrieved code excerpt did not include the full `JobPlanHandler` method bodies, so I cannot state the exact data extraction path beyond the typed-handler contract and the archival-related imports.
- No dedicated `JobPlanHandlerTest` was surfaced in the retrieved evidence, so I cannot confirm whether one already exists outside the neighboring tests above.