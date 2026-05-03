**Recommendation**
Anchor the answer on the release-2.2 docs for savepoints and on the runtime REST savepoint handlers. The behavior to trace is:

- `POST` trigger starts an async savepoint operation and returns a request/trigger identifier.
- `GET` polling checks that identifier until the savepoint reaches a terminal state or fails.

**Implementation anchors**
- `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointHandlers.java`
- The neighboring handler classes in the same package, typically the trigger and status handlers for savepoints.
- The docs page for Flink 2.2 savepoints, which should describe the REST trigger/polling flow and the async savepoint lifecycle.

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointHandlersTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/savepoints/TriggerSavepointHandlerTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointStatusHandlerTest.java`
- If absent, add coverage for:
  - successful trigger returns the polling token/id
  - polling returns running/pending before completion
  - polling returns completed with location/path
  - polling returns failure for rejected or failed savepoint creation

**Citations**
- `flink-docs-release-2.2/docs/ops/state/savepoints/`
- `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointHandlers.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointHandlersTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/savepoints/TriggerSavepointHandlerTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointStatusHandlerTest.java`

**Uncertainties**
- I am not verifying the 2.2.0 tag here, so the exact handler/test class names may differ slightly in that release branch.
- The docs path above is the likely version-pinned public path, but I have not checked the live site in this session.
- The exact JSON field names for the trigger response and polling status can vary by minor version, so confirm against the tag before quoting them verbatim.