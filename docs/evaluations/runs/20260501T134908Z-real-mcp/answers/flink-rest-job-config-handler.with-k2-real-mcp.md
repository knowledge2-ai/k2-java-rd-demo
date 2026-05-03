**Recommendation**
Use the 2.2.0 REST API docs as the public contract, then anchor implementation details on `JobConfigHandler` and `JobConfigHandlerTest`. The docs explicitly document `GET /jobs/:jobid/jobmanager/config` as returning the job manager configuration for a specific job [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0029]. The general REST API page also establishes that Flink’s REST API is versioned and that the backend lives in `flink-runtime` [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002].

**Implementation anchors**
- Public REST contract: `GET /jobs/:jobid/jobmanager/config` returning `ConfigurationInfoEntry[]` for a job [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0029].
- Implementation class: `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandler.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandler.java].
- Message/header wiring: `flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobConfigHeaders.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobConfigHeaders.java].
- REST backend guidance in docs: add `MessageHeaders`, an `AbstractRestHandler`, then register it in `WebMonitorEndpoint` [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002].

**Tests to inspect or add**
- Primary neighboring test: `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandlerTest.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandlerTest.java].
- Nearby job-handler patterns: `JobDetailsHandlerTest` and `JobsOverviewHandlerTest` are the closest adjacent REST handler tests surfaced by K2 for this area [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobsOverviewHandlerTest.java].

**Citations**
- REST API docs, version-pinned to 2.2.0: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001]
- REST API handler development guidance: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002]
- Job config endpoint docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0029]
- `JobConfigHandler`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandler.java]
- `JobConfigHeaders`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobConfigHeaders.java]
- `JobConfigHandlerTest`: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandlerTest.java]

**Uncertainties**
- K2 surfaced the handler and its test, but the returned evidence did not include the full method body of `JobConfigHandler`, so I am not claiming details beyond the documented route and the class/header wiring.
- I did not verify whether there are additional subtests or newer neighbors beyond the surfaced job-handler tests; the anchors above are the ones directly supported by K2 evidence.