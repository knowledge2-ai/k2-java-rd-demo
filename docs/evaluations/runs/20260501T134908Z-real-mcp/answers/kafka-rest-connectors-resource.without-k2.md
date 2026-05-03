**Recommendation**
Use the Connect REST documentation as the contract, then trace the actual behavior in `ConnectorsResource` and verify it against the same-package unit tests. For CRUD specifically, focus on create/update/delete/list/get paths and the status/config error mappings.

**Implementation anchors**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/resources/ConnectorsResource.java`
- Key methods to trace: `createConnector`, `putConnectorConfig` / update path, `deleteConnector`, `getConnector`, `getConnectorConfig`, `getConnectorStatus`, and `listConnectors`
- The behavior is mediated through the Herder API, so follow the request/response translation there as well

**Tests to inspect or add**
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/resources/ConnectorsResourceTest.java`
- Add or tighten coverage for:
  - POST create success and duplicate/invalid config failures
  - PUT update semantics, including partial vs full config handling
  - GET list/detail/config/status responses
  - DELETE success, idempotency/error mapping, and not-found handling
  - HTTP-to-exception mapping for the Herder layer

**Citations**
- `docs/connect.html`
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/resources/ConnectorsResource.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/resources/ConnectorsResourceTest.java`

**Uncertainties**
- I’m not fully certain whether the published 4.2.0 site uses the exact same doc anchor as the source-tree `docs/connect.html`, but that is the right version-pinned doc file to anchor on in the repo.
- I’m also not certain whether there is an additional integration test class nearby beyond `ConnectorsResourceTest`; if you want, I can narrow the likely CRUD edge cases that should be asserted there.