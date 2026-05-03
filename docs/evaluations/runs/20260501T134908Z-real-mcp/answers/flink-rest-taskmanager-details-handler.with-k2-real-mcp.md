**Recommendation**
Use the version-pinned Flink 2.2.0 REST API docs for `/taskmanagers/:taskmanagerid`, then trace the behavior in `TaskManagerDetailsHandler` and its direct test `TaskManagerDetailsHandlerTest`. The K2 evidence does not show a separate lookup-specific spec beyond those anchors, so don’t infer behavior beyond what the implementation/test confirms.

**Implementation anchors**
- REST API 2.2.0 overview and versioning rules: [`https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001`](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001) and [`https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0003`](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0003)
- TaskManager details endpoint docs: [`https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0051`](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0051)
- Core implementation class: [`repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerDetailsHandler.java`](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerDetailsHandler.java)
- Request/response header contract: [`repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/taskmanager/TaskManagerDetailsHeaders.java`](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/taskmanager/TaskManagerDetailsHeaders.java)

**Tests to inspect or add**
- Direct neighbor test: [`repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerDetailsHandlerTest.java`](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerDetailsHandlerTest.java)
- Secondary neighboring REST handler tests surfaced by K2, if you need pattern context:
  - [`repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/metrics/TaskManagerMetricsHandlerTestBase.java`](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/metrics/TaskManagerMetricsHandlerTestBase.java)
  - [`repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TestUntypedMessageHeaders.java`](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TestUntypedMessageHeaders.java)

**Citations**
- REST API docs and endpoint docs: [`https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001`](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001), [`https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0003`](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0003), [`https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0051`](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0051)
- Implementation: [`repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerDetailsHandler.java`](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerDetailsHandler.java)
- Headers: [`repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/taskmanager/TaskManagerDetailsHeaders.java`](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/taskmanager/TaskManagerDetailsHeaders.java)
- Tests: [`repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerDetailsHandlerTest.java`](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerDetailsHandlerTest.java)

**Uncertainties**
- K2 surfaced only one directly relevant test, `TaskManagerDetailsHandlerTest`; it did not provide a second lookup-specific regression test to cite.
- I did not verify the handler’s exact lookup edge cases from the source body here, so any claim about missing-ID or null-ID behavior would need a deeper source read.