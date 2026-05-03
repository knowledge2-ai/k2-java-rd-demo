**Recommendation**
Anchor the answer on the Flink 2.2.0 REST API docs for the `PUT /jobs/:jobid/resource-requirements` endpoint, then inspect the handler together with the request-body model. In this code path, body validation is likely split between JSON/model construction and the REST handler’s explicit checks, so you want both.

**Implementation anchors**
- `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobResourceRequirementsUpdateHandler.java`
- The request-body DTO used by that handler in `flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/...` for job resource requirement updates
- `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobResourceRequirementsHandler.java` for the adjacent read path and symmetry

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobResourceRequirementsUpdateHandlerTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobResourceRequirementsHandlerTest.java`
- Any adjacent `*ResourceRequirements*Test.java` in the same package that covers DTO serialization/deserialization
- Add negative cases for:
  - missing or null body
  - empty resource-requirements payload
  - malformed or duplicate job-vertex identifiers
  - invalid constraint combinations enforced by the request DTO

**Citations**
- [`JobResourceRequirementsUpdateHandler.java`](https://github.com/apache/flink/blob/release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobResourceRequirementsUpdateHandler.java)
- [`JobResourceRequirementsUpdateHandlerTest.java`](https://github.com/apache/flink/blob/release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/JobResourceRequirementsUpdateHandlerTest.java)
- [`Flink 2.2 REST API docs`](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/)

**Uncertainties**
- I am not fully certain of the exact DTO class name without source in front of me.
- I am not fully certain of the exact REST docs section slug for this endpoint, only the version-pinned docs page.
- The precise validation rules may live in the DTO/deserializer rather than directly in `JobResourceRequirementsUpdateHandler`.