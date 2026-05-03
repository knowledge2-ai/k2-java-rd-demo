**Recommendation**
- Anchor the implementation on Flink’s REST handler contract: `AbstractRestHandler` should return a concrete `ResponseBody` type that matches the `MessageHeaders` declaration.
- If the endpoint has no payload, use `EmptyResponseBody` rather than `null` or an ad hoc placeholder.
- The safest mental model is: request in, typed response body out, with the handler’s declared response type being the source of truth.

**Implementation anchors**
- Version-pinned docs:
  - Flink 2.2.0 REST API docs for the endpoint family you are touching.
  - The 2.2.0 Javadocs for `AbstractRestHandler` and the related REST message types.
- Implementation class:
  - `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/AbstractRestHandler.java`
- Supporting type to check:
  - `org.apache.flink.runtime.rest.messages.EmptyResponseBody`
  - The handler’s `MessageHeaders` implementation, especially its declared response-body type.

**Tests to inspect or add**
- Inspect neighboring tests in:
  - `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/`
- Prefer tests that already cover:
  - typed response serialization,
  - empty-body responses,
  - handler error paths and status codes.
- If this is a new or changed concrete handler, add one focused test that asserts:
  - the happy-path response body type matches the header contract,
  - the no-content case returns `EmptyResponseBody` or the equivalent expected contract.

**Citations**
- I can’t provide verified external citations without browsing in this run.
- Exact source anchors I would use, if you want to verify locally, are the file paths above in the Flink 2.2.0 source tree.

**Uncertainties**
- I am not fully certain of the exact neighboring test class names without inspecting the tree.
- I am also not fully certain whether the specific endpoint should return a domain DTO or `EmptyResponseBody`; that depends on the concrete `MessageHeaders` contract for the handler you are implementing.