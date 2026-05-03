**Recommendation**
Use the 2.2.0 REST API docs as the top-level contract, then anchor the implementation on `JobDetailsHandler` plus its header registration in `WebMonitorEndpoint`. For a neighboring handler analogue, K2’s docs explicitly point to `JobExceptionsHandler` as the example pattern, and the nearest job-handler tests to inspect are `JobStatusHandlerTest` and `JobExecutionResultHandlerTest` alongside `JobDetailsHandlerTest`.

**Implementation anchors**
- Version-pinned REST API docs: the Flink 2.2.0 REST API overview and developing notes [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001), [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002)
- Implementation class: `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandler.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandler.java]
- Route registration context: `WebMonitorEndpoint` wires `JobDetailsHandler` into REST handler initialization [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/webmonitor/WebMonitorEndpoint.java]
- Message header contract: `JobDetailsHeaders` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/job/JobDetailsHeaders.java]
- Neighboring handler analogue from docs: `JobExceptionsHandler` is called out as the good example in the 2.2.0 REST docs [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002)

**Tests to inspect or add**
- Primary test: `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java]
- Nearby job REST tests surfaced by K2:
  - `JobStatusHandlerTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobStatusHandlerTest.java]
  - `JobExecutionResultHandlerTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobExecutionResultHandlerTest.java]
  - `JobsOverviewHandlerTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobsOverviewHandlerTest.java]
- If you are validating shared job-endpoint patterns, also inspect the handler families for checkpoints and savepoints as broader REST analogues [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/checkpoints/CheckpointHandlersTest.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointHandlersTest.java]

**Citations**
- REST API overview and versioning rules: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001), [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0003](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0003)
- REST backend / handler development guidance: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002)
- `JobDetailsHandler`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandler.java]
- `JobDetailsHeaders`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/job/JobDetailsHeaders.java]
- `WebMonitorEndpoint`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/webmonitor/WebMonitorEndpoint.java]
- `JobDetailsHandlerTest`: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java]
- `JobStatusHandlerTest`: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobStatusHandlerTest.java]
- `JobExecutionResultHandlerTest`: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobExecutionResultHandlerTest.java]
- `JobsOverviewHandlerTest`: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobsOverviewHandlerTest.java]

**Uncertainties**
- K2 did not surface a direct “this is the intended neighboring analogue” class for `JobDetailsHandler`; the analogue callout to `JobExceptionsHandler` comes from the version-pinned docs, not from a direct code relationship.
- I am inferring `JobStatusHandlerTest` and `JobExecutionResultHandlerTest` as the closest neighboring tests from the surfaced results; that is a reasonable anchor, but not an explicit K2 statement.