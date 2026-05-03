**Recommendation**
- Anchor the answer on the 4.2.0 Connect configuration docs, then confirm behavior in `RestServerConfig` and the same-package REST tests.
- If you need a precise user-facing contract, treat the docs as authoritative and the tests as the behavioral spec.

**Implementation anchors**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/RestServerConfig.java`
- `docs/connect.html` for the Connect worker/REST configuration docs in the 4.2.0 source tree

**Tests to inspect or add**
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/RestServerConfigTest.java`
- Other same-package neighbors under `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/`, especially any `RestServer*Test` coverage
- If config parsing or validation changed, add/extend a focused unit test in that package rather than only relying on broader Connect integration tests

**Citations**
- `connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/RestServerConfig.java`
- `connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/RestServerConfigTest.java`
- `docs/connect.html`

**Uncertainties**
- I am not certain of the exact version-pinned public URL/anchor for the 4.2.0 docs from memory.
- I’m also not certain whether the nearest sibling test is exactly named `RestServerTest` or a similarly named REST test in the same package.