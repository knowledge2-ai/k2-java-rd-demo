**Recommendation**
Implement the handler as a version-pinned Flink REST endpoint in `flink-runtime` using `AbstractRestHandler` and a concrete `ResponseBody` subtype. The 2.2.0 docs explicitly say new requests should be added by defining `MessageHeaders`, implementing a matching `AbstractRestHandler`, and registering it in `WebMonitorEndpoint#initializeHandlers()` [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002].

**Implementation anchors**
- Version-pinned docs: REST API 2.2.0 overview and developer guidance [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001], [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002]
- Implementation class: `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/AbstractRestHandler.java` in `release-2.2.0` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/AbstractRestHandler.java]
- Closest concrete example handler in the same module: `JobResourceRequirementsHandler` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobResourceRequirementsHandler.java]
- Contract clue from the base type: `AbstractRestHandler` is the superclass for handlers that work with `RequestBody` and `ResponseBody` [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/AbstractRestHandler.java]

**Tests to inspect or add**
- Inspect `TestRestHandler` for the local test harness pattern around request/response handling [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/util/TestRestHandler.java]
- Inspect `RestServerEndpointITCase` for endpoint wiring, request dispatch, and error-path behavior [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/RestServerEndpointITCase.java]
- Inspect `MultipartUploadExtension` if the new handler needs custom REST endpoint setup or extension registration [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/MultipartUploadExtension.java]
- Add a focused regression test if none exists for your specific handler, especially one that asserts the concrete `ResponseBody` type returned by the handler

**Citations**
- REST API docs, 2.2.0: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001]
- REST API developer guidance for adding handlers: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002]
- Base implementation class: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/AbstractRestHandler.java]
- Concrete nearby handler: [repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobResourceRequirementsHandler.java]
- Neighboring tests: [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/util/TestRestHandler.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/RestServerEndpointITCase.java], [repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/MultipartUploadExtension.java]

**Uncertainties**
- The K2 search did not surface a dedicated `AbstractRestHandlerTest`, so the exact response-body contract should be confirmed from the source before codifying it.
- The `AbstractRestHandler` text returned by K2 was truncated, so I can anchor the type relationship to `RequestBody`/`ResponseBody`, but not quote every generic/constructor detail with full certainty.
