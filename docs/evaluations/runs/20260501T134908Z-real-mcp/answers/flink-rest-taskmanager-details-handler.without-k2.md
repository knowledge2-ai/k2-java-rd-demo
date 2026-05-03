**Recommendation**
Anchor the explanation on the Flink 2.2.0 REST API reference for TaskManager details, then verify behavior in the `TaskManagerDetailsHandler` implementation and its package-local tests. The key question to answer is whether the handler resolves a TaskManager by the requested `ResourceID`/TaskManager ID and what it does when that lookup misses, because that is the behavior most likely to regress.

**Implementation anchors**
- Version-pinned docs:
  - Flink 2.2.0 REST API reference, TaskManager details section
  - Public path is typically the 2.2 docs site, for example the `rest_api` page under `flink-docs-release-2.2`
- Implementation class:
  - `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerDetailsHandler.java`
- Likely adjacent code path to inspect:
  - `TaskManagersHandler` in the same package, because it usually shares the TaskManager lookup model and response shaping

**Tests to inspect or add**
- Existing handler test to inspect:
  - `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerDetailsHandlerTest.java`
- Neighboring tests worth checking for shared assumptions:
  - `TaskManagersHandlerTest`
  - `TaskManagerMetricsHandlerTest`
  - Any other `taskmanager` REST handler tests in the same package that cover missing-ID and single-ID resolution paths
- Add or extend coverage for:
  - exact ID match returns details
  - unknown/missing TaskManager ID returns the expected REST error
  - response shape stays stable for the selected TaskManager

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerDetailsHandler.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerDetailsHandlerTest.java`
- Flink 2.2.0 REST API docs, TaskManager details section on the version-pinned docs site

**Uncertainties**
- I am confident about the handler class and the test package, but I cannot verify the exact docs URL fragment or the full test class list without repository access.
- I am also not fully certain whether the miss case is surfaced as a 404-style REST error or via another `RestHandlerException` variant in 2.2.0, so that should be checked directly in the handler and its test.