Implemented the vertex watermark REST extension with backward-compatible optional missing-subtask reporting.

**What changed**
- Added a new optional boolean query parameter, `includeMissing`, for the watermark endpoint.
- Introduced `JobVertexWatermarksMessageParameters` so the endpoint can advertise and resolve that query parameter without touching the shared vertex parameter classes.
- Updated `JobVertexWatermarksHandler` so:
  - default behavior stays the same when `includeMissing` is absent or `false`
  - when `includeMissing=true`, it emits one `Metric` per subtask even if the watermark is missing, using the same metric id and a `null` value
- Updated `JobVertexWatermarksHeaders` to use the new message-parameters type.
- Extended `JobVertexWatermarksHandlerTest` with an include-missing case and a request helper for query parameters.

**Tests run**
- `mvn -pl flink-runtime -Dtest=JobVertexWatermarksHandlerTest -DfailIfNoTests=false -Dcheckstyle.skip=true -Denforcer.skip=true -Dsurefire.module.config.jdk21= test`
- Result: passed (`Tests run: 4, Failures: 0, Errors: 0, Skipped: 0`)

**Remaining uncertainty**
- I only ran the focused handler test, not the full `flink-runtime` suite.
- The local Maven invocation required `-Dsurefire.module.config.jdk21=` because this environment uses JDK 25 and Flink’s JDK 21+ test profile injects a SecurityManager flag that JDK 25 rejects.

**Sources consulted**
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/metrics/JobVertexWatermarksHandler.java`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/job/metrics/MetricCollectionResponseBody.java`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/job/metrics/JobVertexWatermarksHeaders.java`
- `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/metrics/JobVertexWatermarksHandlerTest.java`
- `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0047`
- `generated://guides/flink/rest-handler-checklist.md`