**Recommendation**
- Treat `DispatcherRestEndpoint` itself as the registration point. In Flink 2.2.0, the dispatcher REST handlers are assembled in the endpoint’s handler-initialization hook and then handed to the `RestServerEndpoint` lifecycle for registration during startup.
- Practically, that means you should anchor on the endpoint override that builds the handler collection, not on the individual handler implementations.

**Implementation anchors**
- `DispatcherRestEndpoint` as the implementation class.
- The endpoint’s handler-registration override, likely `initializeHandlers(...)` or the equivalent startup hook in that 2.2.0 branch.
- The surrounding REST server wiring in `RestServerEndpoint`, because that is what actually installs the returned handler set.
- Version-pinned docs anchor: the Flink 2.2 REST API docs page for dispatcher endpoints on the `release-2.2` docs line, likely the REST API page under `docs/ops/rest_api`.

**Tests to inspect or add**
- `DispatcherRestEndpointTest` for direct coverage of which handler specs are exposed by the endpoint.
- `RestServerEndpointTest` or the nearest REST-server lifecycle test, to confirm registration happens through the base endpoint contract.
- Any `DispatcherRestEndpointITCase` or same-package integration test that exercises the live REST surface.
- If coverage is thin, add a focused test that asserts the endpoint returns the expected dispatcher handler set from its initialization hook.

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/legacy/dispatcher/DispatcherRestEndpoint.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/legacy/dispatcher/DispatcherRestEndpointTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/legacy/RestServerEndpointTest.java`
- Flink 2.2 REST API docs, dispatcher section on the `release-2.2` docs line

**Uncertainties**
- I’m confident about the architectural anchor, but the exact method name in 2.2.0 could be `initializeHandlers(...)` or a nearby variant depending on the final packaging of that release.
- I’m also not certain of the exact published docs URL path without checking the repo/site, so I’d treat the docs citation above as the intended anchor rather than a verbatim path.