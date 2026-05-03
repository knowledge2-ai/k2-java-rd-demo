**Recommendation**
Use the version-pinned Flink 2.2.0 REST docs as the contract, then anchor implementation review on `JobVertexFlameGraphHandler` and its dedicated test. The endpoint is documented as `GET /jobs/:jobid/vertices/:vertexid/flamegraph`, returning flame-graph information for a vertex and potentially triggering sampling first [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0039].

**Implementation anchors**
- Docs contract: Flink 2.2.0 REST API, flame-graph endpoint section, including path, query params `type` (`FULL`, `ON_CPU`, `OFF_CPU`) and optional `subtaskindex`, and the note that sampling may be initiated on demand [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0039].
- REST backend architecture: the 2.2.0 REST docs say the backend lives in `flink-runtime`, is routed by `WebMonitorEndpoint`, and new handlers are wired through `initializeHandlers()` [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002].
- Implementation class: `JobVertexFlameGraphHandler` in `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobVertexFlameGraphHandler.java`, which is the handler to inspect for exact runtime behavior [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobVertexFlameGraphHandler.java].
- Related message headers: `JobVertexFlameGraphHeaders` defines the route `/jobs/:jobid/vertices/:vertexid/flamegraph` and the request/response types [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobVertexFlameGraphHeaders.java].

**Tests to inspect or add**
- Primary regression test: `JobVertexFlameGraphHandlerTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobVertexFlameGraphHandlerTest.java].
- Neighboring REST handler tests for patterns and fixture style:
  - `JobStatusHandlerTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobStatusHandlerTest.java]
  - `JobExecutionResultHandlerTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobExecutionResultHandlerTest.java]
  - `JobsOverviewHandlerTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobsOverviewHandlerTest.java]
  - `CheckpointHandlersTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/checkpoints/CheckpointHandlersTest.java]
  - `SavepointHandlersTest` [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointHandlersTest.java]

**Citations**
- REST API docs, flame-graph endpoint: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0039]
- REST API docs, handler architecture: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002]
- `JobVertexFlameGraphHandler`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobVertexFlameGraphHandler.java]
- `JobVertexFlameGraphHeaders`: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/JobVertexFlameGraphHeaders.java]
- `JobVertexFlameGraphHandlerTest`: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobVertexFlameGraphHandlerTest.java]

**Uncertainties**
- The K2 snippet included the relevant doc section and file anchors, but not the full handler or test bodies. So I can confirm the endpoint contract and the exact files to inspect, but I am not asserting method-level behavior beyond what the version-pinned docs explicitly state.