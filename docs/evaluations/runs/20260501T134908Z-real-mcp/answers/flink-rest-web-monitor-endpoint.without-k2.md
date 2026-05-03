**Recommendation**

For Flink REST API `2.2.0`, treat `WebMonitorEndpoint` as the assembly point that:

- collects the REST handler implementations needed by the web subsystem,
- maps each handler to its request specification and HTTP method/path,
- registers them with the underlying REST server endpoint during startup,
- and wires shared dependencies like gateway retrievers, executors, serializers, and error handling into those handlers via constructor injection.

The answer should be framed around the concrete `WebMonitorEndpoint` implementation in the `2.2.0` tag, not generic “REST server” behavior.

**Implementation anchors**

- Version-pinned docs:
  - `docs/content/docs/releases/` or the `docs/content/docs/2.2/` area for the `2.2.0` release notes and REST/API docs, if present in that tag.
  - The REST API reference pages for the web monitor / job manager endpoint, if they are versioned under the `2.2.0` docs tree.
- Implementation class:
  - `org.apache.flink.runtime.webmonitor.WebMonitorEndpoint`
  - Also inspect the base REST server classes it delegates to, typically `RestServerEndpoint` and handler factory/specification types in the REST module.
- Wiring points to describe:
  - Handler registration happens by building a handler list from the endpoint’s constructor inputs or overridden factory methods.
  - Each handler is bound to a REST route via a `RestHandlerSpecification`-style contract.
  - Shared services are injected once into the endpoint and then forwarded into individual handlers.

**Tests to inspect or add**

- Neighboring tests for the endpoint class itself, especially:
  - `WebMonitorEndpointTest`
  - any `RestServerEndpointTest` or `RestHandler*Test` in the same module
- Tests that verify:
  - handler registration order or presence,
  - route-to-handler mapping,
  - endpoint startup/shutdown with injected dependencies,
  - failure behavior when a handler factory or dependency is missing.
- If coverage is thin, add a focused test that asserts the endpoint exposes the expected handler set for `2.2.0` startup configuration.

**Citations**

- `org.apache.flink.runtime.webmonitor.WebMonitorEndpoint` in the Apache Flink `2.2.0` source tree
- `org.apache.flink.runtime.rest.RestServerEndpoint` in the Apache Flink `2.2.0` source tree
- The Flink `2.2.0` docs page for REST/web monitor endpoint behavior, if present in the `2.2.0` docs directory

**Uncertainties**

- I cannot verify the exact `2.2.0` file paths or doc page names without browsing the repository.
- Flink has moved REST wiring across versions, so the precise handler factory method names and package layout may differ slightly in `2.2.0`.
- If you need a line-by-line explanation, I would want the exact tag or source file contents to avoid guessing.