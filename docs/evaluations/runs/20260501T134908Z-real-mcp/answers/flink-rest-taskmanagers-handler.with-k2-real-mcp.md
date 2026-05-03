**Recommendation**
Use the Flink 2.2.0 REST docs for the `/taskmanagers` collection endpoint and the `TaskManagersHandler` implementation in `flink-runtime` as the primary anchors. K2 did not surface a dedicated `TaskManagersHandlerTest`, so the nearest test patterns come from adjacent taskmanager handler tests in the same module.

**Implementation anchors**
- Version-pinned REST API docs:
  - REST API overview, including the statement that the REST API is versioned and defaults to the oldest supported version when no version is specified: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001)
  - `/taskmanagers` endpoint section, which says it "Returns an overview over all task managers": [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0049](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0049)
- Implementation class:
  - `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagersHandler.java`, class `TaskManagersHandler`, which returns an overview over registered TaskManagers and extends `AbstractResourceManagerHandler<RestfulGateway, EmptyRequestBody, TaskManagersInfo, EmptyMessageParameters>`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagersHandler.java](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagersHandler.java)

**Tests to inspect or add**
- Inspect these neighboring tests for request/response and error-handling patterns:
  - `TaskManagerLogListHandlerTest`: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerLogListHandlerTest.java](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerLogListHandlerTest.java)
  - `TaskManagerProfilingListHandlerTest`: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerProfilingListHandlerTest.java](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerProfilingListHandlerTest.java)
  - `TaskManagerProfilingHandlerTest`: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerProfilingHandlerTest.java](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerProfilingHandlerTest.java)
- If there is no direct `TaskManagersHandlerTest`, add one to cover the collection response contract for `/taskmanagers`, especially empty-body handling, response type, and any null/serialization edge cases.

**Citations**
- REST API docs root and versioning: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001)
- `/taskmanagers` endpoint docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0049](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0049)
- `TaskManagersHandler`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagersHandler.java](repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagersHandler.java)
- Neighboring tests:
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerLogListHandlerTest.java](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerLogListHandlerTest.java)
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerProfilingListHandlerTest.java](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerProfilingListHandlerTest.java)
  - [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerProfilingHandlerTest.java](repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerProfilingHandlerTest.java)

**Uncertainties**
- K2 did not return a dedicated `TaskManagersHandlerTest`, so the test recommendation is based on nearby taskmanager handler tests rather than a direct existing test for this class.
- The docs snippet surfaced the endpoint description, but not the full response schema in the returned excerpt; if you need exact field-by-field contract text, that part still needs a narrower lookup.