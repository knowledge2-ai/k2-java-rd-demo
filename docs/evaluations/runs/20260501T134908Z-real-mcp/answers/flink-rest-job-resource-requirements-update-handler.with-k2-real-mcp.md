**Recommendation**
Anchor the review on the 2.2.0 REST API docs for `PUT /jobs/:jobid/resource-requirements` and the `JobResourceRequirementsUpdateHandler` implementation in `flink-runtime`. K2 did not surface a dedicated handler test, so use neighboring job REST handler tests as the closest regression anchors. [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0032] [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobResourceRequirementsUpdateHandler.java]

**Implementation anchors**
- Version-pinned REST docs for the endpoint `PUT /jobs/:jobid/resource-requirements` in `flink/flink-docs-release-2.2/docs/ops/rest_api/index.html`. [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0032]
- Version-pinned REST docs describing REST backend wiring in `flink-runtime` and handler registration. [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002]
- Production class: `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobResourceRequirementsUpdateHandler.java`. [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobResourceRequirementsUpdateHandler.java]

**Tests to inspect or add**
- Inspect `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java` as the nearest job-handler neighbor. [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java]
- Inspect `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobStatusHandlerTest.java`. [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobStatusHandlerTest.java]
- Inspect `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobsOverviewHandlerTest.java`. [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobsOverviewHandlerTest.java]
- Inspect `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobExecutionResultHandlerTest.java`. [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobExecutionResultHandlerTest.java]
- Add a dedicated `JobResourceRequirementsUpdateHandlerTest` if none exists, focused on invalid or malformed request bodies for resource requirement updates.

**Citations**
- Docs endpoint section: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0032]
- Docs backend guidance: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002]
- Handler class: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobResourceRequirementsUpdateHandler.java]
- Neighbor test: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandlerTest.java]
- Neighbor test: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobStatusHandlerTest.java]
- Neighbor test: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobsOverviewHandlerTest.java]
- Neighbor test: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobExecutionResultHandlerTest.java]

**Uncertainties**
- K2 did not return a dedicated `JobResourceRequirementsUpdateHandlerTest`, so I cannot confirm existing request-body validation coverage from this evidence alone.
- The handler source snippet was truncated, so I am not asserting the exact validation branches without opening the file directly.