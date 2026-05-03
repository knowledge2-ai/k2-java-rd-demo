**Recommendation**
Use the 2.2.0 REST API docs for the job-vertex task-manager listing as the contract, then anchor the implementation to `JobVertexTaskManagersHandler` and its request/response model. The routing you want is the job-vertex-scoped task-manager detail endpoint, not the broader job or task-manager handler.

**Implementation anchors**
- Version-pinned REST API docs page for Flink 2.2.0 job/vertex task-manager details.
- `org.apache.flink.runtime.rest.handler.job.JobVertexTaskManagersHandler`
- The corresponding headers/model classes for the same endpoint, typically in the same `job` REST handler package.
- The route should be the job vertex path that resolves from `jobId` + `vertexId` to per-task-manager details.

**Tests to inspect or add**
- `JobVertexTaskManagersHandlerTest`
- Neighboring job-vertex REST handler tests in the same package, especially ones covering:
  - path parameter validation
  - empty / missing vertex cases
  - aggregation across subtasks per TaskManager
  - serialization of the REST response
- If missing, add a focused test for the exact task-manager routing path and a regression test for a vertex with multiple TaskManagers.

**Citations**
- `org.apache.flink.runtime.rest.handler.job.JobVertexTaskManagersHandler`
- Flink 2.2.0 REST API documentation for job vertex task-manager details, published under the Flink 2.2 docs site

**Uncertainties**
- I am not confident enough to give the exact published docs URL or the exact neighboring test class names beyond the handler test without checking the repository.
- I am also not certain whether the handler returns a dedicated response type or reuses an existing vertex-details DTO in 2.2.0.