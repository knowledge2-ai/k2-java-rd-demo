# Blinded LLM-as-Judge Comparison

Generated: `2026-05-01T23:27:48.706120+00:00`

## Method

- The judge saw answer labels `A` and `B`; labels were deterministically randomized per case.
- The judge did not see which answer came from K2 or the baseline until results were mapped back.
- Explicit system identity tokens in answer text were normalized before judging.
- The deterministic evidence-grounding scorecard remains the primary benchmark metric; this is a secondary qualitative preference check.
- The reference checklist came from the published benchmark case metadata, not from either answer.

## Aggregate Judge Results

- Cases judged: `100`
- Winner counts: `{"codex_with_k2_real_mcp": 74, "codex_without_k2": 26}`
- Win rates excluding ties: `{"codex_with_k2_real_mcp": 0.74, "codex_without_k2": 0.26}`
- Tie rate: `0.0`
- Mean confidence: `0.7424`

## Deterministic Scorecard Context

- `codex_without_k2`: combined `0.189375`, retrieval `0`, answer `0.37875`, safety `1`, passed `0/100`
- `codex_with_k2_real_mcp`: combined `0.928875`, retrieval `0.954`, answer `0.90375`, safety `1`, passed `93/100`

## Dimension Averages

| Run | Correctness | Grounding | Specificity | Usefulness | Risk |
| --- | ---: | ---: | ---: | ---: | ---: |
| codex_with_k2_real_mcp | `4.0` | `4.16` | `4.23` | `4.14` | `3.79` |
| codex_without_k2 | `3.7` | `2.88` | `3.32` | `3.64` | `4.02` |

## Per-Question Judge Decisions

### 1. Flink REST pattern for DispatcherRestEndpoint (`flink-rest-dispatcher-rest-endpoint`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 3, "usefulness": 3}}`
- Rationale: A correctly places DispatcherRestEndpoint in org.apache.flink.runtime.dispatcher and identifies WebMonitorEndpoint#initializeHandlers() as the registration hook with plausible neighboring test paths. B's citations are undermined by a fabricated legacy/dispatcher package path — DispatcherRestEndpoint is not under rest/handler/legacy/dispatcher — making all three cited source paths likely wrong. B's architectural reasoning is sound but the concrete anchors cannot be trusted.

### 2. Flink REST pattern for WebMonitorEndpoint (`flink-rest-web-monitor-endpoint`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A names the concrete wiring method (`initializeHandlers()`), `MessageHeaders`, `AbstractRestHandler`, `RestHandlerSpecification`, and version-pinned source paths — all plausible and free of the hallucination markers. Its specific test file paths are unverified but structurally sound. B correctly surfaces `RestServerEndpoint` as the delegation target but hedges every claim into vagueness and gives doc locations as guesses, making it less actionable despite lower fabrication risk.

### 3. Flink REST pattern for RestServerEndpoint (`flink-rest-rest-server-endpoint`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B provides substantially more concrete anchors: `initializeHandlers()` as the abstract lifecycle hook, `TestRestServerEndpoint`, `DocumentingRestEndpoint`, and `RuntimeRestAPIVersionTest` as neighboring test fixtures — all with release-2.2.0-pinned repo URIs. A's doc URL points to a path (`advanced/rest_api/`) that differs from the actual 2.2 docs path (`ops/rest_api/`), weakening its grounding. B correctly identifies the Netty-based implementation detail absent in A.

### 4. Flink REST pattern for AbstractRestHandler (`flink-rest-abstract-rest-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides version-pinned source paths, named concrete handler examples (JobResourceRequirementsHandler), named test classes (TestRestHandler, RestServerEndpointITCase), and specific doc anchors. B gives correct conceptual guidance (EmptyResponseBody, MessageHeaders contract) but explicitly lacks verifiable citations and test class names, making it less actionable. A's uncertainties are honestly scoped. Neither fabricates Spring MVC or JAX-RS patterns.

### 5. Flink REST pattern for JobDetailsHandler (`flink-rest-job-details-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: B adds concrete anchors A lacks: JobDetailsHeaders, WebMonitorEndpoint registration, and version-pinned nightlies URLs. The broader test surface (JobStatusHandlerTest, JobExecutionResultHandlerTest, checkpoint/savepoint handlers) is more actionable. B's main risk is citing docs as explicitly naming JobExceptionsHandler as 'the good example' — that specific claim is unverifiable and likely overstated. A is more conservative and honest about uncertainty but thinner on grounding.

### 6. Flink REST pattern for JobConfigHandler (`flink-rest-job-config-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B names the endpoint path (`/jobs/:jobid/jobmanager/config`), the response type (`ConfigurationInfoEntry[]`), and anchor fragment IDs in the 2.2 docs. It also names `WebMonitorEndpoint` and `AbstractRestHandler` as concrete extension points. A is vaguer—no endpoint path, no response type, and softer uncertainty disclosure. B's risk demerit is the unverifiable `#part-0029` fragment and `repo://` URIs, which may be invented anchors.

### 7. Flink REST pattern for JobExceptionsHandler (`flink-rest-job-exceptions-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.75`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides versioned nightlies.apache.org URLs, full package paths for JobExceptionsHandler and JobExceptionsHeaders, and names four concrete neighboring test files. B names the same core classes but omits URLs entirely, explicitly admitting uncertainty about the 2.2.0 docs slug. B is marginally safer on risk (more conservative claims), but A's grounding and specificity advantages are decisive for an engineer needing concrete navigation anchors.

### 8. Flink REST pattern for JobAccumulatorsHandler (`flink-rest-job-accumulators-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides version-pinned nightlies URLs, exact release-2.2.0 repo paths, and names the full message-plumbing chain (JobAccumulatorsHeaders, JobAccumulatorsMessageParameters, AccumulatorsIncludeSerializedValueQueryParameter). It honestly flags the missing dedicated test and points to analogous tests. B omits version-pinned URLs, misses the message-plumbing classes entirely, and presents JobVertexAccumulatorsHandlerTest as a primary anchor without verification—raising hallucination risk.

### 9. Flink REST pattern for JobPlanHandler (`flink-rest-job-plan-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 3, "usefulness": 3}}`
- Rationale: A correctly places JobPlanHandler and JobPlanHeaders in flink-runtime (not flink-runtime-web), names the exact RuntimeMessageHeaders<EmptyRequestBody, JobPlanInfo, JobMessageParameters> signature, provides version-anchored doc fragment URLs, and honestly flags the missing JobPlanHandlerTest. B confidently places the handler in flink-runtime-web — a wrong module that would misdirect any engineer — and asserts a JobPlanHandlerTest exists without evidence, both high-risk fabrication patterns.

### 10. Flink REST pattern for JobVertexDetailsHandler (`flink-rest-job-vertex-details-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides pinned doc section anchors (#part-0035, #part-0036), exact repo paths at release-2.2.0 tag, names JobVertexDetailsHeaders as the contract class, and honestly discloses that no JobVertexDetailsHandlerTest was found. B asserts that test file exists without verification—a hallucination risk—and cites only the base doc URL without section anchors. B's JobVertexDetailsMessageParameters naming is unverified and likely imprecise.

### 11. Flink REST pattern for JobVertexTaskManagersHandler (`flink-rest-job-vertex-taskmanagers-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: A names the correct endpoint, all three artifact layers (handler, headers, response DTO), and concrete neighboring tests with version-pinned paths. The `repo://` URI scheme is non-standard and cannot be dereferenced, slightly increasing hallucination risk, but the class names and package paths match Flink's actual layout. B is technically honest but so vague that it offers an engineer almost no actionable anchor beyond the handler class name itself.

### 12. Flink REST pattern for JobCancellationHandler (`flink-rest-job-cancellation-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.62`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: Both correctly identify JobCancellationHandler, its headers companion, the primary test, and avoid all hallucination markers. A wins on grounding: it names JobCancellationHeaders.java, WebMonitorEndpoint wiring, and provides release-2.2.0-tagged source paths with nightlies docs anchors. B adds useful behavioral insight (ack vs. termination semantics, dispatcher/gateway path) and specific test-coverage scenarios, but supplies no versioned URIs and explicitly admits it cannot verify doc URLs.

### 13. Flink REST pattern for SavepointHandlers (`flink-rest-savepoint-handlers`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.74`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 3, "risk": 2, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides version-pinned nightlies URLs, a concrete supertype reference (AbstractRestHandler with TriggerResponse/SavepointTriggerMessageParameters type parameters), and limits test citations to SavepointHandlersTest and StopWithSavepointHandlersTest, both plausible for release-2.2.0. B introduces TriggerSavepointHandlerTest and SavepointStatusHandlerTest, which do not match Flink's known test-class naming in that package, and explicitly disclaims not verifying against the 2.2.0 tag—compounding fabrication risk.

### 14. Flink REST pattern for CheckpointHandlers (`flink-rest-checkpoint-handlers`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B names the concrete test class `CheckpointHandlersTest.java` and inner class `CheckpointTriggerHandler` with version-pinned repo URIs, giving an engineer a direct source anchor. A correctly identifies the package and implementation path but stays at the directory level without naming the test class. Both appropriately avoid hallucinated frameworks. B's explicit uncertainty about method-level details is better calibrated than A's vaguer caveats.

### 15. Flink REST pattern for JobResourceRequirementsUpdateHandler (`flink-rest-job-resource-requirements-update-handler`)

- Winner: `codex_without_k2`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A names the symmetrical read handler (JobResourceRequirementsHandler), its dedicated test class, and concrete negative-case categories — all directly actionable for an engineer inspecting validation. B supplies more citation anchors including a specific doc fragment (#part-0032) but falls back to unrelated neighbor tests (JobDetailsHandlerTest, JobStatusHandlerTest) rather than the resource-requirements-specific test that A correctly names, reducing specificity and usefulness for this exact handler.

### 16. Flink REST pattern for JobSubmitHandler (`flink-rest-job-submit-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B provides version-pinned nightlies.apache.org doc URLs and repo:// source refs at release-2.2.0, making every claim immediately verifiable. B correctly names same-package neighbors (JobConfigHandlerTest, JobDetailsHandlerTest, etc.) and references WebMonitorEndpoint handler-registration, which is the actual Flink REST model. A omits all URLs, and its suggested neighbors (JarUploadHandlerTest, JarRunHandlerTest) are from a different handler context, not the job-handler package.

### 17. Flink REST pattern for FileUploads (`flink-rest-file-uploads`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 1, "risk": 4, "specificity": 1, "usefulness": 2}}`
- Rationale: B pins the exact class path (flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/FileUploads.java), the direct test file (FileUploadsTest.java), version-pinned nightlies URLs, and concrete behavioral anchors (EMPTY singleton, close() cleanup, WebMonitorEndpoint). A offers only conceptual paraphrasing with no source artifacts and admits it cannot cite any specific path, making it unactionable for an engineer inspecting the codebase.

### 18. Flink REST pattern for DashboardConfigHandler (`flink-rest-dashboard-config-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides version-pinned fragment URLs, names both DashboardConfigHandler and DashboardConfigurationHeaders with full package paths, lists concrete neighboring tests with repo-anchored URIs, and honestly discloses the missing DashboardConfigHandlerTest. B names the same primary class but hedges every artifact with 'likely' or 'cannot verify', cites only the top-level REST API page without a fragment, and incorrectly asserts DashboardConfigHandlerTest exists when A's retrieval found none.

### 19. Flink REST pattern for ClusterOverviewHandler (`flink-rest-cluster-overview-handler`)

- Winner: `codex_without_k2`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A's generic type signature and ClusterOverviewHeaders citation are accurate and specific, but A falsely declares no ClusterOverviewHandlerTest exists—a material error since that test does exist in flink-runtime. This misdirects engineers away from the primary test anchor the question explicitly requires. B correctly names ClusterOverviewHandlerTest and honestly withholds the docs URL it cannot verify, avoiding a false confidence trap. B's lower specificity on type hierarchy is a lesser defect than A's fabricated coverage gap.

### 20. Flink REST pattern for TaskManagersHandler (`flink-rest-taskmanagers-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: B names the exact file path, package, superclass (`AbstractResourceManagerHandler<RestfulGateway, EmptyRequestBody, TaskManagersInfo, EmptyMessageParameters>`), and version-pinned repo URIs for both the handler and neighboring tests. A stays vague ('likely a TaskManagersInfo-style wrapper') and admits it cannot confirm package paths. Neither answer hallucinates Spring/JAX-RS. B's specific test neighbors and honest gap disclosure about missing `TaskManagersHandlerTest` make it more actionable.

### 21. Flink REST pattern for TaskManagerDetailsHandler (`flink-rest-taskmanager-details-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A provides pinned URLs to nightlies.apache.org/flink/flink-docs-release-2.2 and repo-pinned paths to TaskManagerDetailsHandler.java, TaskManagerDetailsHeaders.java, and TaskManagerDetailsHandlerTest.java — all version-anchored. B covers the same conceptual ground but never commits to a URL fragment or full path, only prose descriptions. A's explicit citations to TaskManagerDetailsHeaders is a meaningful additional anchor B omits. Neither answer fabricates Spring/JAX-RS. B's uncertainty is appropriate but the vagueness reduces engineer utility.

### 22. Flink REST pattern for JobVertexBackPressureHandler (`flink-rest-job-vertex-back-pressure-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A correctly places the handler in `org.apache.flink.runtime.rest.handler.job` and names the companion `JobVertexBackPressureHeaders` (MessageHeaders pattern), which is accurate for Flink 2.x. B points to `org.apache.flink.runtime.webmonitor.handlers`, the pre-REST-refactoring location deprecated since ~1.5; this would send an engineer to a non-existent or dead path in 2.2.0. A also names the exact endpoint path and version-pinned doc anchors.

### 23. Flink REST pattern for JobVertexWatermarksHandler (`flink-rest-job-vertex-watermarks-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B correctly places the handler in the `job/metrics` subpackage, which matches the actual Flink source layout — watermarks are exposed via the metric subsystem. A drops the `metrics` level entirely, producing a wrong import path that would mislead any engineer trying to locate the class. B also provides version-pinned nightlies URLs; A only describes docs generically. Both answers' neighboring-test selections are weakly justified, but B's correct package anchors outweigh that weakness.

### 24. Flink REST pattern for SubtaskCurrentAttemptDetailsHandler (`flink-rest-subtask-current-attempt-details-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 3, "specificity": 2, "usefulness": 3}}`
- Rationale: A names the correct package (handler/job), provides pinned nightlies URLs and file paths, and explicitly surfaces WebMonitorEndpoint registration as a gap. Its main error is conflating the current-attempt handler with the numbered-attempt endpoint URL. B places the handler in a non-existent handler/job/vertex sub-package and admits it cannot verify any URL or route string, making it less actionable despite honest uncertainty.

### 25. Flink REST pattern for JobVertexFlameGraphHandler (`flink-rest-job-vertex-flame-graph-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A names the exact query parameters (type: FULL/ON_CPU/OFF_CPU, subtaskindex), correctly identifies JobVertexFlameGraphHeaders, and correctly describes Flink's netty-based REST routing via WebMonitorEndpoint.initializeHandlers() — no Spring MVC/JAX-RS contamination. It provides version-pinned nightlies.apache.org URLs and full repo paths. B omits parameter details, admits it cannot pin the docs URL, and lists unverified neighboring tests without version anchoring.

### 26. Flink checkpointing pattern for CheckpointCoordinator (`flink-checkpointing-checkpoint-coordinator`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B names the full activation call chain — CheckpointCoordinatorDeActivator, CheckpointSchedulingProvider, SchedulerBase — with version-pinned repo URIs and a concrete test assertion (triggerCheckpoint(true) + storage location wait). A lists companion types (PendingCheckpoint, CompletedCheckpoint, etc.) but omits the scheduler activation path. Both correctly avoid hallucination markers and hedge appropriately; B's additional specificity is the decisive gap.

### 27. Flink checkpointing pattern for PendingCheckpoint (`flink-checkpointing-pending-checkpoint`)

- Winner: `codex_without_k2`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 4, "risk": 5, "specificity": 4, "usefulness": 5}}`
- Rationale: Both answers are technically sound and avoid hallucination markers. A edges out B by naming CheckpointCoordinator as the essential neighboring class (critical for understanding the full orchestration path) and explicitly listing subsumption as an abort trigger (a Flink-specific correctness detail). B provides a specific test method (testSetCanceller) and claims source retrieval via repo:// URIs, but omits CheckpointCoordinator entirely and uses suspicious #part-0001 URL fragments not matching real Flink doc anchors.

### 28. Flink checkpointing pattern for CompletedCheckpoint (`flink-checkpointing-completed-checkpoint`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 4}}`
- Rationale: A provides version-pinned URLs, exact class paths for CompletedCheckpoint and DefaultCompletedCheckpointStore, and names specific test files with concrete behavioral anchors. B is accurate but deliberately vague on test names and doc paths, hedging uncertainty into imprecision. For an engineer modifying Java code, A's concrete file paths and test names are immediately actionable. Neither answer mentions hallucination markers (FsStateBackend, MemoryStateBackend). B's caution is honest but reduces utility.

### 29. Flink checkpointing pattern for CompletedCheckpointStore (`flink-checkpointing-completed-checkpoint-store`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B correctly identifies DefaultCompletedCheckpointStore as the primary retention implementation in Flink 2.2.0 — a class A omits entirely. B also surfaces CompletedCheckpointStoreTest and DefaultCompletedCheckpointStoreTest as contract-level anchors, and provides version-pinned nightlies.apache.org URLs. A guesses StandaloneCompletedCheckpointStore as primary (incorrect for 2.2.0), names only two tests, and provides no versioned doc URLs. Both appropriately hedge on unverified internals.

### 30. Flink checkpointing pattern for DefaultCompletedCheckpointStore (`flink-checkpointing-default-completed-checkpoint-store`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B names the exact field `maxNumberOfCheckpointsToRetain`, the `ArrayDeque<CompletedCheckpoint>` internal structure, the config key `execution.checkpointing.max-retained-checkpoints`, version-pinned nightlies URLs, and four specific test classes including `DefaultCompletedCheckpointStoreUtilsTest`. A gives correct general shape but hedges on test file existence, misstates the field name as `maxNumberOfRetainedCheckpoints`, and provides no version-pinned doc URLs or internal data-structure specifics.

### 31. Flink checkpointing pattern for CheckpointStatsTracker (`flink-checkpointing-checkpoint-stats-tracker`)

- Winner: `codex_without_k2`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 2, "risk": 2, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: Answer A uses a fabricated `repo://apache/flink@release-2.2.0/...` URL scheme that does not exist, inflating apparent grounding. It also incorrectly states no `CheckpointStatsTrackerTest` exists, when this class is the canonical test anchor for the tracker. Answer B correctly cites `CheckpointStatsTrackerTest`, names the full data-model hierarchy (`CheckpointStatsSnapshot`, `CheckpointStatsHistory`, `CheckpointStatsCounts`, `CompletedCheckpointStats`, `FailedCheckpointStats`, `RestoredCheckpointStats`), and honestly hedges on the exact docs slug.

### 32. Flink checkpointing pattern for CheckpointStatsSnapshot (`flink-checkpointing-checkpoint-stats-snapshot`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: B provides concrete version-pinned nightlies URLs, repo-anchored source paths at release-2.2.0, and names the direct test class `CheckpointStatsSnapshotTest` plus `DefaultCheckpointStatsTrackerTest` with the specific method `testCreateSnapshot`. A lists correct neighboring types but offers no verifiable URLs and hedges on whether a snapshot test file exists. B's explicit uncertainty about method-level internals is well-calibrated. Neither hallucinates deprecated backends.

### 33. Flink checkpointing pattern for CheckpointMetrics (`flink-checkpointing-checkpoint-metrics`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: Answer A names all nine CheckpointMetrics fields with version-pinned repo URIs, identifies the correct acknowledgement path (CheckpointResponder, Environment, TaskStateManager), and names four concrete test anchors. Answer B lists only six fields, introduces the non-existent field name 'bytesBufferedInAlignment' in its uncertainty section, and uses vague doc references without version-pinned URIs. B's mention of CheckpointStatsTrackerTest is a valid addition A lacks, but insufficient to close the gap.

### 34. Flink checkpointing pattern for CheckpointProperties (`flink-checkpointing-checkpoint-properties`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 4, "usefulness": 3}}`
- Rationale: B adds meaningful test anchors (PendingCheckpointTest, CompletedCheckpointTest, CheckpointFailureManagerTest) and version-pinned repo URIs. A has a concrete advantage enumerating the actual flag names (discardSubsumed, discardFinished, etc.) which B omits. Neither introduces hallucination markers. B's #part-0001 URL fragments are suspicious fabrications and the repo:// URI scheme is non-standard, slightly increasing hallucination risk versus A's conservative-but-accurate approach.

### 35. Flink checkpointing pattern for CheckpointRetentionPolicy (`flink-checkpointing-checkpoint-retention-policy`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 5, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: Both answers are technically sound and acknowledge uncertainty about exact enum constants. B wins on grounding: it supplies version-pinned nightlies URLs and repo:// URIs with release-2.2.0 tags that an engineer can navigate immediately. B also names a broader test corpus (PendingCheckpointTest, CompletedCheckpointStoreTest, CheckpointFailureManagerTest) alongside the shared CheckpointPropertiesTest. A gives only file paths with no navigable anchors and names fewer tests.

### 36. Flink checkpointing pattern for CheckpointIDCounter (`flink-checkpointing-checkpoint-id-counter`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B names concrete API methods (getAndIncrement, get, setCount), the INITIAL_CHECKPOINT_ID constant, and version-pinned paths (release-2.2.0) with real nightlies.apache.org URLs. It also surfaces TestingCheckpointIDCounter and CheckpointCoordinatorMasterHooksTest — artifacts A omits — and explicitly flags the absence of a dedicated CheckpointIDCounterTest. A names the right files but stays surface-level with no method-level anchors or doc URLs.

### 37. Flink checkpointing pattern for StandaloneCheckpointIDCounter (`flink-checkpointing-standalone-checkpoint-id-counter`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A names exact version-pinned artifact paths for the implementation class, its direct test, and the inherited base test class, then explicitly flags what was not retrieved. B gives the correct package paths and a useful test checklist but stops short of naming the base test class or full artifact URIs. A's explicit uncertainty handling and concrete file anchors make it more actionable for an engineer; B's test scenarios are useful but not uniquely superior.

### 38. Flink checkpointing pattern for CheckpointFailureManager (`flink-checkpointing-checkpoint-failure-manager`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A provides version-pinned nightlies URLs, concrete repo paths at release-2.2.0, names CheckpointConfig#getTolerableCheckpointFailureNumber, identifies testIgnoresPastCheckpoints, and adds CheckpointCoordinatorFailureTest. B covers the same conceptual ground but lacks pinned URLs, uses an uncertain docs path, names no specific test methods, and relies on hedged descriptions instead of anchored artifacts.

### 39. Flink checkpointing pattern for CheckpointPlanCalculator (`flink-checkpointing-checkpoint-plan-calculator`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 5, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 4, "usefulness": 4}}`
- Rationale: A provides actual version-pinned nightlies URLs and explicit repo paths at release-2.2.0, and crucially it flags that no standalone CheckpointPlanCalculatorTest was found, redirecting to DefaultCheckpointPlanCalculatorTest. B confidently names CheckpointPlanCalculatorTest as a file to inspect without hedging—if that file does not exist, B's primary test anchor is fabricated. B's coverage scenarios are useful, but the unverified test citation and absent doc URLs weigh against it.

### 40. Flink checkpointing pattern for DefaultCheckpointPlanCalculator (`flink-checkpointing-default-checkpoint-plan-calculator`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.8`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 5, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 3}}`
- Rationale: Both answers name the correct class and test paths with no hallucinated APIs. B wins on grounding and specificity: it supplies version-pinned nightlies URLs and repo URIs locked to release-2.2.0, names concrete test scenarios (all-running / not-running tasks), and adds the adjacent TestSubtaskCheckpointCoordinator with appropriate hedging. A's paths are correct but unanchored — no URLs, no version tag, no scenario detail.

### 41. Flink checkpointing pattern for CheckpointRequestDecider (`flink-checkpointing-checkpoint-request-decider`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A names the exact three-way decision (execute/drop/postpone), pins specific CheckpointFailureReason enum values (MINIMUM_TIME_BETWEEN_CHECKPOINTS, TOO_MANY_CHECKPOINT_REQUESTS), cites version-pinned repo URIs and nightlies docs, and names actual test method coverage (testForce, chooseRequestToExecute, chooseQueuedRequestToExecute). B describes plausible behavior but hedges on method names, introduces unverified concepts (coalescing, scheduler enabled/disabled), and lacks version-pinned grounding.

### 42. Flink checkpointing pattern for CheckpointResourcesCleanupRunner (`flink-checkpointing-checkpoint-resources-cleanup-runner`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.95`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 1, "usefulness": 2}}`
- Rationale: Answer A correctly places the class in `org.apache.flink.runtime.dispatcher.cleanup`, names `CheckpointResourcesCleanupRunnerFactory`, identifies the `JobManagerRunner` interface, and provides version-pinned repo URIs and doc URLs. Answer B puts the class in `org.apache.flink.runtime.checkpoint` — the wrong package — which would send an engineer to a nonexistent location. B also admits it cannot confirm test names or URLs, adding no concrete anchors.

### 43. Flink checkpointing pattern for CheckpointStorageLoader (`flink-checkpointing-checkpoint-storage-loader`)

- Winner: `codex_without_k2`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 5, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 5, "grounding": 3, "risk": 4, "specificity": 5, "usefulness": 5}}`
- Rationale: B correctly describes the three-branch loading precedence (explicit storage config → state.checkpoints.dir → JobManagerCheckpointStorage fallback) with concrete config key names and both storage implementation classes. This is the operationally critical insight an engineer needs to inspect or modify the loader. A has stronger URL grounding with versioned nightlies links but self-reports truncated source and cannot confirm the algorithm, limiting usefulness. Neither answer introduces hallucination markers.

### 44. Flink checkpointing pattern for CheckpointStorageCoordinatorView (`flink-checkpointing-checkpoint-storage-coordinator-view`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: B provides version-pinned repo URIs (`@release-2.2.0`) for all code references, explicitly contrasts `CheckpointStorageWorkerView`, and names `CheckpointCoordinatorTest` as a live coordinator-path test. A names the same classes but without version anchoring, and only cites the docs root. B's `#part-0001` fragment anchors on doc URLs are suspicious (non-standard Flink anchor format) and represent a mild fabrication risk, preventing a stronger win.

### 45. Flink checkpointing pattern for StateBackend (`flink-checkpointing-state-backend`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.7`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 3}}`
- Rationale: B names specific methods (createKeyedStateBackend, createOperatorStateBackend), cites AbstractStateBackend as a compat shell, identifies BatchExecutionStateBackend as a concrete implementation anchor, and provides version-pinned repo URIs. A is conceptually correct and avoids hallucination markers but leaves test citations vague and names no method-level surfaces. B's slightly lower risk score reflects unverified BatchExecutionStateBackend module path (may belong to flink-streaming-java, not flink-runtime).

### 46. Flink checkpointing pattern for OperatorStateBackend (`flink-checkpointing-operator-state-backend`)

- Winner: `codex_without_k2`
- Confidence: `0.76`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 5, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 5}}`
- Rationale: B correctly identifies DefaultOperatorStateBackend as the concrete implementation (OperatorStateBackend is an interface), names DefaultOperatorStateBackendTest as the primary test anchor, and lists substantive related types (OperatorStateStore, OperatorSubtaskState). A omits DefaultOperatorStateBackend entirely—a critical gap—and introduces StateBackendUtils at a suspicious path that appears fabricated. B's uncertainty disclosures are appropriately scoped.

### 47. Flink checkpointing pattern for KeyedStateBackend (`flink-checkpointing-keyed-state-backend`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.62`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: B correctly identifies CheckpointableKeyedStateBackend as the interface that adds snapshot/savepoint responsibilities on top of KeyedStateBackend — the critical split for a checkpointing question. A omits this interface entirely, misattributing the snapshot contract to AbstractKeyedStateBackend. B also provides real, verifiable nightlies docs URLs. A recovers points with more direct test suggestions and method-level detail, while B's test list (channel state, file merging) is largely tangential to keyed-state checkpointing.

### 48. Flink checkpointing pattern for SavepointRestoreSettings (`flink-checkpointing-savepoint-restore-settings`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.68`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 4}}`
- Rationale: A names the critical consumer class DefaultExecutionGraphFactory and provides version-pinned repo paths with exact test file references, making it more actionable for a Java engineer. B correctly points to the savepoints doc (more appropriate than checkpoints) and adds JobGraphTest.java, but omits the execution-path consumer and leaves factory methods unnamed. A's #part-0001 URL fragments appear fabricated, which is a grounding concern, but its overall specificity advantage is decisive.

### 49. Flink checkpointing pattern for SavepointFormatType (`flink-checkpointing-savepoint-format-type`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: A provides concrete repo-tagged paths, real test class names, and the StateBackend.supportsSavepointFormat gating detail that directly answers format-choice semantics. EventSerializer encoding SavepointType as part of CheckpointBarrier is plausible but the specific method name decodeSavepointType is unverified. B is safer but vaguer—no repo-tagged paths, speculative test file, and weaker grounding. Neither answer invokes the hallucination markers. A is more actionable despite the EventSerializer uncertainty.

### 50. Flink checkpointing pattern for CheckpointCoordinatorConfiguration (`flink-checkpointing-checkpoint-coordinator-configuration`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 3, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B correctly identifies the class package as org.apache.flink.runtime.jobgraph.tasks, whereas A incorrectly places it in org.apache.flink.runtime.checkpoint. B provides version-pinned repo URIs (release-2.2.0) and nightlies doc URLs, making grounding verifiable. A lists useful config fields but anchors them to a wrong path. Neither enumerates actual class members, but B's honest uncertainty scoping and correct location give an engineer a reliable starting point.

### 51. Kafka Connect pattern for ConnectorPluginsResource (`kafka-rest-connector-plugins-resource`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A provides version-pinned repo URIs at 4.2 tag, actual kafka.apache.org/42 doc URLs, concrete imported types (ConfigInfos, ConfigKeyInfo, PluginInfo, ConnectRestException), and a precise test assertion `herder.validateConnectorConfig(eq(PROPS), any(), anyBoolean())`. B lacks version-pinned citations entirely, admits it cannot supply doc URLs, stops at route-level description, and uses the vague phrase 'Connect validation stack' without naming any delegated class or method.

### 52. Kafka Connect pattern for AbstractHerder (`kafka-connect-abstract-herder`)

- Winner: `codex_without_k2`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 4, "usefulness": 5}}`
- Rationale: B names the concrete entry point `validateConnectorConfig(...)`, traces REST→herder→plugin loading→ConfigDef validation, and supplies real verifiable GitHub URLs at the `4.2.0` tag. A omits the key method entirely, uses internal `repo://` URIs that are not publicly verifiable, and skips `Plugins`, `DistributedHerderTest`, and the REST resource layer. Both avoid the hallucination markers. A's specific test method names are plausible but unverified.

### 53. Kafka Connect pattern for DistributedHerder (`kafka-connect-distributed-herder`)

- Winner: `codex_without_k2`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 5, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: B names `KafkaConfigBackingStore` and `putConnectorConfig` as the write-path anchors and flags leader/non-leader divergence and backing-store tests — all real, relevant implementation surfaces for distributed config updates. A provides better versioned doc URLs but stays at file-level granularity without naming the config-update method or backing store, limiting actionability. Neither answer contains the hallucination markers. A's doc citations are more precisely versioned; B's single root URL is weaker there.

### 54. Kafka Connect pattern for StandaloneHerder (`kafka-connect-standalone-herder`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 4}}`
- Rationale: A names the exact `updateConnectorTasks` method, describes the stop/skip/recompute/recreate logic, pins version-specific doc URLs, and names concrete test scenarios. B is directionally correct but provides only file paths without method-level detail or version-pinned doc URLs, making it less actionable. B's risk score is higher because it avoids fabrication by staying vague, while A's specific URL fragments (e.g., `#part-0001`) are unverifiable and may be synthetic.

### 55. Kafka Connect pattern for Herder (`kafka-connect-herder`)

- Winner: `codex_without_k2`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 5, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: B correctly names Herder.java as the actual interface — the central artifact the question asks about — while A admits it could not locate the interface and anchors only on implementations. B also correctly names StandaloneHerder and both DistributedHerderTest/StandaloneHerderTest, which are real files. A's kafka.apache.org/42/kafka-connect/ URLs with #part-0025 anchors and repo:// URIs look fabricated; B acknowledges URL uncertainty rather than inventing anchors.

### 56. Kafka Connect pattern for Worker (`kafka-connect-worker`)

- Winner: `codex_without_k2`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 2}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 5, "usefulness": 5}}`
- Rationale: A correctly anchors on Worker.java as the orchestration class and names the exact adjacent wrappers (WorkerConnector, WorkerSinkTask, WorkerSourceTask) and their unit tests. B substitutes AbstractHerder as the primary anchor because its retrieval missed Worker — a misleading deflection since AbstractHerder handles herder-side coordination, not worker-side thread/lifecycle management. B's integration test pointer (ExactlyOnceSourceIntegrationTest) is weaker than A's direct unit test references.

### 57. Kafka Connect pattern for WorkerConnector (`kafka-connect-worker-connector`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B names concrete methods (initialize(), transitionTo()), specific test cases (testFailConnectorThatIsNeitherSourceNorSink, testStopFailure), version-pinned doc URLs, and repo-anchored source paths. A gives correct file paths but lacks method-level specificity and test case names. Neither answer hallucinates validation APIs. B's uncertainty disclosures are appropriately scoped. The doc URLs in B may not resolve exactly but are structurally plausible for 4.2.

### 58. Kafka Connect pattern for WorkerTask (`kafka-connect-worker-task`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 4}}`
- Rationale: Both answers identify the correct implementation anchors. B adds meaningful breadth: WorkerConnector.java, AbstractHerder.java, and ExactlyOnceSourceIntegrationTest as an integration-level lifecycle oracle. The version-pinned doc URLs (/42/kafka-connect/) follow Kafka's documented URL pattern and are plausible; the repo:// URIs are clearly pseudo-references. A is more conservative and honest about uncertainty but provides no doc URLs and omits the integration test layer.

### 59. Kafka Connect pattern for WorkerSinkTask (`kafka-connect-worker-sink-task`)

- Winner: `codex_without_k2`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 4, "risk": 5, "specificity": 4, "usefulness": 4}}`
- Rationale: A uses real, pinned GitHub URLs (4.2.0 tag), names verified public API methods (put/flush/preCommit), and honestly disclaims uncertainty. B claims internal method names recordBatch, recordCommitSuccess, and getNextCommit as WorkerSinkTask overrides—these are unverified and likely belong to a metrics helper class, not the delivery/commit path. B's doc URLs use a non-standard path format and its repo:// URIs are retrieval-system notation, not verifiable links.

### 60. Kafka Connect pattern for WorkerSourceTask (`kafka-connect-worker-source-task`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B correctly identifies SourceTaskOffsetCommitter as the external scheduler driving commits, names the shouldCommitOffsets() gate, explains the exception-isolation pattern keeping the executor alive, and cites SourceTaskOffsetCommitterTest and ErrorHandlingTaskTest. A omits SourceTaskOffsetCommitter entirely (substituting OffsetStorageWriter, a lower-level detail), uses a generic doc root URL, and expresses uncertainty about tests that do exist.

### 61. Kafka Connect pattern for ConnectorConfig (`kafka-connect-connector-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B provides version-pinned doc URLs, names PluginVersionValidator as a concrete public anchor, adds SourceConnectorConfigTest as a meaningful neighbor test, and cites repo-tagged source paths. A is technically sound but offers no doc links, no version-specific class members, and the herder tests are less targeted than SourceConnectorConfigTest. B's unverified URLs introduce some risk but the grounding payoff exceeds A's omission.

### 62. Kafka Connect pattern for SinkConnectorConfig (`kafka-connect-sink-connector-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A names concrete methods (configDef, enrichedConfigDef), specific validation rules (topics/topics.regex, DLQ overlap), the AbstractHerder runtime path, and an actual test method testSinkConnectorHasNeitherTopicsListNorTopicsRegex. It also honestly flags that SinkConnectorConfigTest was not found. B points to a likely-invalid public Javadoc URL for a connect/runtime-internal class, asserts SinkConnectorConfigTest.java exists while admitting it cannot verify, and never names actual validation rules or methods.

### 63. Kafka Connect pattern for SourceConnectorConfig (`kafka-connect-source-connector-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.6`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 3}}`
- Rationale: B correctly adds AbstractHerder.java as the runtime call site where source-connector-specific validation is applied—a genuine and useful anchor A omits entirely. Both share the same core SourceConnectorConfig/SourceConnectorConfigTest paths. B's doc subdirectory URLs (/kafka-connect/connector-development-guide/, /configuration/kafka-connect-configs/) are suspect—Kafka versioned docs canonically live at /42/documentation.html, not those subpaths. ConnectorValidationIntegrationTest.java existence is unverified. A is safer but less actionable for an engineer inspecting validation call sites.

### 64. Kafka Connect pattern for WorkerConfig (`kafka-connect-worker-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 4, "usefulness": 4}}`
- Rationale: B correctly places StandaloneConfig under the `standalone/` sub-package path and supplies explicit version-pinned doc URLs. A gives wrong file paths for both DistributedConfig and StandaloneConfig (missing their `distributed/` and `standalone/` subdirectories), which is a concrete accuracy failure. B's inclusion of ExactlyOnceSourceIntegrationTest is tangential but not harmful. A earns credit for covering DistributedConfig, which B omits entirely.

### 65. Kafka Connect pattern for DistributedConfig (`kafka-connect-distributed-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.62`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 4, "usefulness": 4}}`
- Rationale: Both answers are technically sound and avoid hallucination markers. B edges ahead by pinning repo URIs to @4.2, surfacing EmbeddedConnectCluster as a real end-to-end usage anchor for DistributedConfig constants, and providing versioned doc URLs. A compensates with broader neighbor coverage (WorkerConfig, DistributedHerder chain) but lacks URI-level grounding. B's doc URL paths (e.g., /42/kafka-connect/) are plausible but not verified, slightly elevating its risk.

### 66. Kafka Connect pattern for StandaloneConfig (`kafka-connect-standalone-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B correctly places StandaloneConfig under the standalone/ subpackage, which is the actual location in the Kafka codebase. A places it directly under runtime/, which is wrong. B also cites the specific Connect user guide and config reference URLs with correct 4.2 anchors, and names the standalone-specific offset.storage.file.filename config as a concrete example. Both answers appropriately express uncertainty about unread source bodies.

### 67. Kafka Connect pattern for ConfigDef (`kafka-connect-config-def`)

- Winner: `codex_without_k2`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 5, "grounding": 4, "risk": 5, "specificity": 4, "usefulness": 5}}`
- Rationale: B correctly identifies ConfigDef as living in the clients module (org.apache.kafka.common.config), names AbstractConfig as the parse/validation consumer, and explains the actual semantics (type coercion before validation, defaults before validation, ConfigException on failure, dependents as UI-only). A's citations lean on Connect HTML docs rather than the canonical Javadoc and misses AbstractConfig entirely. B's uncertainty disclosures are precise and calibrated; A's are vaguer.

### 68. Kafka Connect pattern for ConfigValue (`kafka-connect-config-value`)

- Winner: `codex_without_k2`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 5, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: Both answers correctly identify ConfigValue fields and avoid hallucination markers. B edges ahead by correctly naming ConfigDef.validate() as the primary producer of ConfigValue results in the clients module—more fundamental than A's AbstractConnectorClientConfigOverridePolicy focus. B's Javadoc URL pattern is the canonical version-pinned anchor for the API surface. A's ExactlyOnceSourceIntegrationTest citation is a stretch for ConfigValue validation specifically, slightly elevating its hallucination risk.

### 69. Kafka Connect pattern for ConfigTransformer (`kafka-connect-config-transformer`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B correctly identifies that the core `ConfigTransformer` lives in `clients/` under `org.apache.kafka.common.config`, not `connect/runtime/` as A implies. B also names `WorkerConfigTransformer` as the Connect-layer wrapper, `AbstractHerder` for the validation path, and `ClusterConfigState` for config storage — all real, relevant classes. A's module placement is wrong and its citations are sparse. B provides version-pinned doc URLs and repo-anchored source paths.

### 70. Kafka Connect pattern for ConfigProvider (`kafka-connect-config-provider`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.62`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: Both correctly anchor on ConfigProvider SPI and FileConfigProvider in clients/. A edges out on grounding by supplying explicit /42/ version-pinned doc URLs (the question explicitly asks for these). B adds ConfigTransformer and the ${provider:path:key} expansion path, which is genuinely useful, but admits uncertainty about the doc URL rather than providing it. Neither hallucinates markers. The delta is narrow and purely on fulfilling the version-pinned docs requirement.

### 71. Kafka Connect pattern for Plugins (`kafka-connect-plugins`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A provides versioned doc URLs, method-level anchors (pluginClassFromConfig, validateConnectorConfig, ConnectException path), and supporting classes (AbstractHerder, ConnectorConfig). B correctly names PluginsTest.java as the primary test — more direct than A's TestPlugins.java (a fixture file, not the behavioral test) — and properly elevates DelegatingClassLoader. A wins on grounding and implementor utility despite the TestPlugins/PluginsTest confusion.

### 72. Kafka Connect pattern for PluginDesc (`kafka-connect-plugin-desc`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 4}}`
- Rationale: A names actual accessor methods (`className()`, `version()`, `type()`, `typeName()`, `location()`, `loader()`), states equality/hash contract, and provides version-pinned `@4.2` repo URIs plus docs URLs. B omits method-level detail and introduces `PluginScannerTest.java` with self-declared uncertainty about its existence — a mild hallucination risk. B's docs anchor is vague ('version-pinned section') while A supplies specific URLs.

### 73. Kafka Connect pattern for PluginType (`kafka-connect-plugin-type`)

- Winner: `codex_without_k2`
- Confidence: `0.58`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 3}}`
- Rationale: A is conservative but clean: correct isolation package path, honest uncertainty, no fabricated artifacts. B adds specificity (version-pinned URLs, test class name) but introduces risk: `MultiVersionTest` is a questionable primary anchor for PluginType classification (PluginsTest or a dedicated PluginTypeTest is more direct), the `#part-0040` doc fragment is unverifiable, and leaking 'retrieval system' references is sloppy. A's lower specificity is less harmful than B's likely-wrong test anchor.

### 74. Kafka Connect pattern for DelegatingClassLoader (`kafka-connect-delegating-class-loader`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides version-pinned source paths, concrete filenames (DelegatingClassLoaderTest, SynchronizationTest, ClassLoaderFactory, LoaderSwap), and explicit doc URLs anchored to 4.2. B describes the same concepts correctly but gives only generic package-level pointers and explicitly admits uncertainty about exact filenames and URLs. For an engineer changing Java code, A's concrete artifacts are immediately actionable; B requires a follow-up source-tree inspection.

### 75. Kafka Connect pattern for PluginClassLoader (`kafka-connect-plugin-class-loader`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.6`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 4}}`
- Rationale: A provides repo-pinned URIs at @4.2 for all three artifact types, names ClassLoaderFactory as a real wiring neighbor, describes child-first loadClass semantics concretely, and explicitly flags the PluginClassLoaderTest gap rather than fabricating confidence. B correctly names PluginClassLoaderTest (which does exist) — a meaningful win — but gives only a generic /42/documentation/ doc anchor and omits ClassLoaderFactory. A's doc-fragment specificity and explicit uncertainty disclosure outweigh B's test-naming advantage.

### 76. Kafka Connect pattern for PluginScanResult (`kafka-connect-plugin-scan-result`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.74`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: B names the actual contents of PluginScanResult (sorted sets for sink connectors, source connectors, converters, header converters, transformations, predicates, config providers, REST extensions, connector client config override policies), calls out initLoaders() as the entry point in Plugins.java, and uses versioned repo URIs. It is also more honest about test existence—explicitly stating retrieval found no PluginScanResultTest. A hedges the same gap but still lists it as a 'data-shape seam,' which is weaker. B's doc URLs (kafka.apache.org/42/...) are unverified but non-injurious.

### 77. Kafka Connect pattern for PluginUtils (`kafka-connect-plugin-utils`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: Both correctly anchor on connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/PluginUtils.java and the same-package test. A is more specific with versioned doc URLs and repo-pinned paths, giving an engineer a direct navigation target. However, A's fragment IDs (#part-0038, #part-0001, #part-0040) are unverifiable and likely fabricated, which erodes trust. B is more conservative and honest about its uncertainty, reducing hallucination risk at the cost of doc-anchor specificity.

### 78. Kafka Connect pattern for ConnectRestServer (`kafka-rest-connect-rest-server`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A names exact constructor signature, superclass, initializeResources delegation, pinned doc URLs with fragment anchors, and a full set of neighboring resource tests with version-pinned repo URIs. B gestures at the same files but lacks constructor details, uses a generic docs URL, and cites RestServerTest without confirming it exists in 4.2. A's declared uncertainty about truncated file body is honest. Neither answer invokes the hallucination markers.

### 79. Kafka Connect pattern for RestServerConfig (`kafka-rest-rest-server-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A supplies version-pinned doc URLs (kafka.apache.org/42/...), repo-anchored source URIs at the 4.2 tag, the correct runtime inheritance chain (ConnectRestServer→RestServer), and three named neighboring test files. B names the same primary class and test but cites only bare relative paths and the vague 'docs/connect.html', explicitly admitting it cannot supply a version-pinned URL. Neither answer introduces the hallucination markers. A is uniformly more actionable.

### 80. Kafka Connect pattern for ConnectorsResource (`kafka-rest-connectors-resource`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: Both answers correctly identify ConnectorsResource.java and ConnectorsResourceTest.java as the primary anchors. B adds version-pinned URLs, names adjacent test classes (InternalConnectResourceTest, ConnectorPluginsResourceTest, RootResourceTest, LoggingResourceTest) useful for regression checks, and cites ConnectRestServer.java for broader REST wiring context. B also honestly scopes its uncertainty to truncated retrieval rather than naming specific methods it cannot verify. A names methods (createConnector, putConnectorConfig) without confirming their exact signatures, which slightly elevates fabrication risk.

### 81. Kafka Connect pattern for ConnectorStateInfo (`kafka-rest-connector-state-info`)

- Winner: `codex_without_k2`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: B correctly names ConnectorsResource as the status-endpoint producer and identifies the GET /connectors/{connector}/status contract plus specific ConnectorStateInfo fields (state, worker_id, trace). A's InternalConnectResourceTest reference is misleading—InternalConnectResource handles inter-worker forwarding, not the user-facing status path; the correct test anchor is ConnectorsResourceTest. B loses grounding points for omitting concrete file paths and verified doc URLs, but its honesty about URL uncertainty is preferable to A's potentially fabricated doc path fragment.

### 82. Kafka Connect pattern for ConnectorInfo (`kafka-rest-connector-info`)

- Winner: `codex_without_k2`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 2, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: Both correctly anchor on `org.apache.kafka.connect.runtime.rest.entities.ConnectorInfo`. B wins on risk: it names the correct REST endpoint (`GET /connectors/{connector}`) and explicitly refuses to fabricate doc URLs. A introduces hallucination risk via a non-standard `repo://` URL scheme and suspicious `#part-0001` URL fragments that do not match Kafka's actual documentation URL structure.

### 83. Kafka Connect pattern for CreateConnectorRequest (`kafka-rest-create-connector-request`)

- Winner: `codex_without_k2`
- Confidence: `0.62`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 3, "specificity": 4, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 4}}`
- Rationale: A correctly anchors validation to both CreateConnectorRequest and ConnectorsResource (the actual split), mentions initialState, and discloses uncertainty without fabricating URIs. B names CreateConnectorRequestTest directly (a genuine advantage) but uses a fabricated repo:// URI scheme, suspicious #part-0001 doc fragments, and pads the test list with tangential files (RootResourceTest, ConnectorPluginsResourceTest) while omitting the more relevant ConnectorsResourceTest.

### 84. Kafka Connect pattern for ConnectorType (`kafka-rest-connector-type`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.62`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A's key advantage is identifying both ConnectorType definitions — the REST entities class and the health API counterpart — which is accurate and directly useful for an engineer auditing classification semantics. A also names ConnectorTypeTest.java directly rather than hedging. B adds value by naming ConnectorsResource.java for REST wiring, but its doc anchor (docs/connect.html) is less precise, and listing tangential tests (RootResource, LoggingResource) in A is offset by the dual-class insight.

### 85. Kafka Connect pattern for Connector (`kafka-connect-connector`)

- Winner: `codex_without_k2`
- Confidence: `0.62`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 4, "usefulness": 4}}`
- Rationale: A correctly names the lifecycle surface (initialize, start, stop, taskClass, taskConfigs) and hedges honestly on test file names. B adds useful runtime artifacts (ConnectorValidationIntegrationTest, ConnectorConfig.java) but introduces two risk vectors: the docs URLs (kafka.apache.org/42/kafka-connect/connector-development-guide/) do not match Kafka's real documentation URL structure, and the repo:// URI scheme is a non-standard internal retrieval artifact, not a publicly verifiable reference.

### 86. Kafka Connect pattern for SourceConnector (`kafka-connect-source-connector`)

- Winner: `codex_without_k2`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 5, "usefulness": 5}}`
- Rationale: A names four concrete test files with actionable per-scenario coverage gaps (taskConfigs partitioning, start/stop lifecycle, invalid task-class) and correctly separates connector vs. runtime responsibilities. B adds valid details (ConnectorContext reconfiguration signaling, ServiceLoader manifest) and supplies kafka.apache.org/42/ version-pinned URLs, but surfaces only one neighboring test and is less actionable for an engineer writing coverage. Neither answer introduces the hallucination markers.

### 87. Kafka Connect pattern for SinkConnector (`kafka-connect-sink-connector`)

- Winner: `codex_without_k2`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 4, "usefulness": 4}}`
- Rationale: A gives more actionable test anchors (WorkerSinkTaskTest, SinkTaskTest) and concrete method-level responsibilities without overreaching. B cites version-pinned URLs and the parent Connector.java which adds grounding value, but the surfaced test anchor (ExactlyOnceSourceIntegrationTest) is source-oriented and weak for sink coverage. B's repo:// URIs are non-standard and unverifiable, introducing citation risk. Neither fabricates validation APIs.

### 88. Kafka Connect pattern for Transformation (`kafka-connect-transformation`)

- Winner: `codex_without_k2`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: B identifies `TransformationChain.java` and `TransformationChainTest.java` as the critical runtime execution path — the actual class where `Transformation.apply()` is invoked per record. This is the most actionable anchor for anyone inspecting SMT behavior. A omits `TransformationChain` entirely, anchoring only on config/validation tests. B's `WorkerSourceTaskTest`/`WorkerSinkTaskTest` additions cover real wiring. Both have acceptable uncertainty disclosures; neither fabricates APIs.

### 89. Kafka Connect pattern for HeaderConverter (`kafka-connect-header-converter`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B cites version-pinned URLs, repo-anchored source paths, and names concrete artifacts (ConnectorConfig.HEADER_CONVERTER_CLASS_VALIDATOR, SampleHeaderConverter, ServiceLoader discoverability, plugin.version config). A correctly identifies SimpleHeaderConverter but offers no version-pinned doc URLs and places SimpleHeaderConverter in connect/runtime/src/main rather than connect/api, which is a module-location error. B's gap acknowledgment on missing HeaderConverterTest is honest and useful.

### 90. Kafka Connect pattern for Converter (`kafka-connect-converter`)

- Winner: `codex_without_k2`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 2}, "codex_without_k2": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}}`
- Rationale: B correctly identifies the actual Converter interface, concrete JsonConverter implementation, and the isKey split in configure() — the core behavioral mechanism. It names WorkerSourceTask/WorkerSinkTask as the call sites that separate key from value conversion, which is precisely what an engineer modifying conversion behavior needs. A stops at config wiring in ConnectorConfig and never reaches the Converter interface itself, making it useful only for config validation, not conversion behavior.

### 91. Kafka Connect pattern for Schema (`kafka-connect-schemas`)

- Winner: `codex_without_k2`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 2}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 5, "usefulness": 5}}`
- Rationale: B correctly names the canonical test files — ConnectSchemaTest, SchemaBuilderTest, SchemaProjectorTest, StructTest — in the right package (connect/api/src/test/java/org/apache/kafka/connect/data/). A incorrectly claims no ConnectSchemaTest exists, then substitutes PluginUtilsTest and converter tests as anchors, which is a significant misdirection. B also adds SchemaProjector, a behaviorally relevant neighbor A omits. B's uncertainty disclosures are calibrated; A's false negative on a well-known test file is the critical failure.

### 92. Kafka Connect pattern for SchemaBuilder (`kafka-connect-schema-builder`)

- Winner: `codex_without_k2`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}}`
- Rationale: A names all correct artifacts: SchemaBuilder.java, ConnectSchema.java, SchemaBuilderTest.java, ConnectSchemaTest.java, and a valid 4.2 Javadoc URL. B artificially claims SchemaBuilderTest was not surfaced by retrieval, which is misleading since that file is well-known and discoverable. B also cites doc fragment #part-0001 which appears fabricated, and surfaces an irrelevant ExactlyOnceSourceIntegrationTest as 'gap evidence'.

### 93. Kafka Connect pattern for Struct (`kafka-connect-struct`)

- Winner: `codex_without_k2`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}}`
- Rationale: B names the directly relevant unit tests (StructTest.java, SchemaBuilderTest.java, ConnectSchemaTest.java) and ConnectSchema.java as the schema-enforcement implementation — all real artifacts in the connect/api module. A points to integration tests (ConnectorValidationIntegrationTest, ExactlyOnceSourceIntegrationTest) that are unrelated to Struct data validation, and admits it couldn't find Struct-specific tests. B's test list is precisely what an engineer needs; A's is a distraction.

### 94. Kafka Connect pattern for SinkRecord (`kafka-connect-sink-record`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.62`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 4}}`
- Rationale: B adds the runtime-side `InternalSinkRecord` and `InternalSinkRecordTest` anchors, which are real artifacts and meaningfully extend the answer beyond the public API. It also provides version-pinned doc URLs and explicitly flags the absence of a dedicated `SinkRecordTest`. A is cleaner and hallucination-free but under-specifies. B loses risk points for suspicious URL anchor fragments (`#part-0001`, `#part-0050`) and the tangential `ConnectorConfigTest` recommendation.

### 95. Kafka Connect pattern for SourceRecord (`kafka-connect-source-record`)

- Winner: `codex_without_k2`
- Confidence: `0.62`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 4, "usefulness": 4}}`
- Rationale: Both answers correctly identify the dual metadata planes and key class paths. B cites more specific URLs and test files but introduces risk via suspicious `#part-0001` URL fragments (non-standard Kafka doc anchors), non-verifiable `repo://` URIs, and an overconfident characterization of `SamplePredicate.java` as a Predicate<SourceRecord> helper. A's explicit uncertainty acknowledgments and absence of fabricated identifiers make its grounding more trustworthy, narrowly winning on risk.

### 96. Kafka Connect pattern for ConnectorClientConfigRequest (`kafka-connect-connector-client-config-request`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.68`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A names AbstractConnectorClientConfigOverridePolicy and pinpoints clientProps() as the input surface, giving engineers a concrete method-level entry point. It also supplies version-pinned repo URIs and doc URLs. B adds ConnectorClientConfigRequestTest and ConnectorConfigTest (wiring) which A missed, and is more conservative. A loses risk points for unverifiable doc fragment anchors; B loses grounding/specificity points for relative-path-only citations and no method-level detail.

### 97. Kafka Connect pattern for ConnectorClientConfigOverridePolicy (`kafka-connect-connector-client-config-override-policy`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 5, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A correctly names AbstractConnectorClientConfigOverridePolicy in connect/runtime, the validate(ConnectorClientConfigRequest) flow, ConfigValue mapping, and pinned test classes (BaseConnectorClientConfigOverridePolicyTest, NoneConnectorClientConfigOverridePolicyTest, PrincipalConnectorClientConfigOverridePolicyTest). B correctly places concrete policies in connect/api but offers no version-pinned paths, no method-level detail, and mislocates tests to connect/api/src/test. A loses risk points for suspicious doc URL fragments (#part-0041, #part-0004) which are likely fabricated anchors.

### 98. Kafka Connect pattern for AbstractConnectorClientConfigOverridePolicy (`kafka-connect-abstract-connector-client-config-override-policy`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B names concrete repo paths at the 4.2 tag, identifies AllowlistConnectorClientConfigOverridePolicy (absent from A), correctly notes the Versioned interface, and surfaces PluginUtilsTest as a real neighboring test anchor with an explicit repo URI. A omits AllowlistConnectorClientConfigOverridePolicy, uses only Javadoc URLs without source paths, and provides no concrete test class. Both correctly disclaim missing a dedicated abstract-policy unit test.

### 99. Kafka Connect pattern for NoneConnectorClientConfigOverridePolicy (`kafka-connect-none-connector-client-config-override-policy`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 4}}`
- Rationale: A wins on grounding and specificity: version-pinned repo URIs, named AbstractConnectorClientConfigOverridePolicy base class, BaseConnectorClientConfigOverridePolicyTest, and specific section-anchored doc URLs. B is safer—it correctly names AllConnectorClientConfigOverridePolicy—but cites only a package directory for tests and the root docs page, giving an engineer less to act on. A's AllowlistConnectorClientConfigOverridePolicy reference is a hallucinated class name and a genuine risk, but its overall specificity advantage still carries.

### 100. Kafka Connect pattern for PrincipalConnectorClientConfigOverridePolicy (`kafka-connect-principal-connector-client-config-override-policy`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A names the exact SASL allowlist (SASL_JAAS_CONFIG, SASL_MECHANISM, SECURITY_PROTOCOL_CONFIG), deprecation annotation, AbstractConnectorClientConfigOverridePolicy, and BaseConnectorClientConfigOverridePolicyTest — all consistent with the actual codebase. Version-pinned repo URIs are concrete anchors. The deprecation 'since = 4.2' is the main risk: the class may have been deprecated in an earlier minor. B is safer but gives no allowlist, no abstract base, no test base class, and weaker version pinning.
