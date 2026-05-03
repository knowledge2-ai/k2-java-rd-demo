**Recommendation**
- Anchor the check on the Flink 2.2-pinned REST API docs for the `/taskmanagers` endpoint, then verify the handler’s collection-building path against the response DTOs and the existing handler tests.
- For this specific issue, focus on whether the handler correctly serializes the task-manager collection response, including empty and multi-entry cases.

**Implementation anchors**
- `TaskManagersHandler` in Flink’s REST handler code for the cluster/task-manager listing endpoint.
- The collection response DTO it produces, likely a `TaskManagersInfo`-style wrapper plus per-entry `TaskManagerInfo` records.
- If you are tracing the exact wiring, also check the REST headers/route registration for `/taskmanagers`.

**Tests to inspect or add**
- `TaskManagersHandlerTest`
- Nearby REST handler tests in the same package, especially other cluster/listing handlers that validate collection responses
- Add or verify cases for:
  - empty task-manager list
  - multiple task-managers
  - field preservation in each entry
  - response shape/ordering if the API promises either

**Citations**
- Flink 2.2 REST API docs: `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/` (taskmanagers section)

**Uncertainties**
- I cannot confirm the exact Java package/file path or the exact DTO class names without repo access.
- Flink 2.2.0 may place the handler under a cluster REST handler package, and the surrounding test names may differ slightly from the likely ones above.