# Blinded LLM-as-Judge Comparison

Generated: `2026-05-02T21:52:18.650823+00:00`

## Method

- The judge saw answer labels `A` and `B`; labels were deterministically randomized per case.
- The judge did not see which answer came from K2 or the baseline until results were mapped back.
- Explicit system identity tokens in answer text were normalized before judging.
- The deterministic evidence-grounding scorecard remains the primary benchmark metric; this is a secondary qualitative preference check.
- The reference checklist came from the published benchmark case metadata, not from either answer.

## Aggregate Judge Results

- Cases judged: `100`
- Winner counts: `{"codex_grep_filesystem": 99, "codex_with_k2_real_mcp": 1}`
- Win rates excluding ties: `{"codex_grep_filesystem": 0.99, "codex_with_k2_real_mcp": 0.01}`
- Tie rate: `0.0`
- Mean confidence: `0.8308`

## Deterministic Scorecard Context

- `codex_without_k2`: combined `0.189375`, retrieval `0`, answer `0.37875`, safety `1`, passed `0/100`
- `codex_grep_filesystem`: combined `0.754083`, retrieval `0.637333`, answer `0.870833`, safety `1`, passed `2/100`
- `codex_with_k2_real_mcp`: combined `0.928875`, retrieval `0.954`, answer `0.90375`, safety `1`, passed `93/100`

## Dimension Averages

| Run | Correctness | Grounding | Specificity | Usefulness | Risk |
| --- | ---: | ---: | ---: | ---: | ---: |
| codex_grep_filesystem | `4.74` | `4.79` | `4.99` | `4.98` | `4.12` |
| codex_with_k2_real_mcp | `3.43` | `3.02` | `2.7` | `2.95` | `3.68` |

## Per-Question Judge Decisions

### 1. Flink REST pattern for DispatcherRestEndpoint (`flink-rest-dispatcher-rest-endpoint`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: B names the exact override method (`DispatcherRestEndpoint.initializeHandlers`), a concrete dispatcher-specific handler (`JobSubmitHandler`), and traces the full registration chain through `RestServerEndpoint.start()` and `registerHandler()`. It pins line numbers and surfaces the most directly relevant test fixtures (`DocumentingDispatcherRestEndpoint`, `RestAPIStabilityTestUtils`). A correctly identifies the class hierarchy but explicitly admits it cannot name registered handlers and cites only handler-level tests unrelated to endpoint registration.

### 2. Flink REST pattern for WebMonitorEndpoint (`flink-rest-web-monitor-endpoint`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.92`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B correctly models the full class hierarchy: RestServerEndpoint base → WebMonitorEndpoint → DispatcherRestEndpoint/MiniDispatcherRestEndpoint, with line-pinned source refs covering start(), initializeHandlers(), factories, versioning, and doc generators. A stops at WebMonitorEndpoint without the concrete subclasses, cites a nightlies URL that is a generic REST overview (not an implementation anchor), and omits RestServerEndpoint entirely. B also correctly surfaces config-flag-conditional handler registration, which A misses.

### 3. Flink REST pattern for RestServerEndpoint (`flink-rest-rest-server-endpoint`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.68`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides a complete ordered lifecycle trace (constructor → start → initializeHandlers → Netty bootstrap → startInternal → closeAsync → shutDownInternal), names concrete runtime subclasses (WebMonitorEndpoint, DispatcherRestEndpoint), and correctly anchors the docs pipeline in flink-docs generators. B correctly identifies abstract hooks but omits shutdown/Netty detail, and the SQL Gateway REST docs citation is tangential to RestServerEndpoint in flink-runtime. B adds TestRestServerEndpoint and RuntimeRestAPIVersionTest that A misses, but the lifecycle coverage gap matters more for the question asked.

### 4. Flink REST pattern for AbstractRestHandler (`flink-rest-abstract-rest-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B states the response-body contract precisely (CompletableFuture<P extends ResponseBody>, status from headers not body), supplies line-number-pinned citations across all required artifacts, covers the flink-docs module via RuntimeRestAPIDocGenerator, and names AbstractHandlerTest as the direct base-class test. A uses a less canonical example handler, omits flink-docs entirely, provides no line numbers, and uses speculative fragment anchors (#part-0001/0002) on docs URLs.

### 5. Flink REST pattern for JobDetailsHandler (`flink-rest-job-details-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 3, "usefulness": 4}}`
- Rationale: A names JobVertexDetailsHandler as analogue — structurally the closest match in handler/job/ — and pins specific line ranges for JobDetailsHandler, its Headers class, and the doc generators in flink-docs. B's real nightlies URLs are genuinely useful, but the claim that JobExceptionsHandler is 'called out as the good example' in the auto-generated REST API docs is unsupported and likely fabricated. B also introduces CheckpointHandlersTest and SavepointHandlersTest whose exact names are uncertain.

### 6. Flink REST pattern for JobConfigHandler (`flink-rest-job-config-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.87`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: Answer B critically conflates two distinct endpoints: `JobConfigHandler` serves `GET /jobs/:jobid/config` returning `JobConfigInfo` (jid, name, execution-config), while `/jobs/:jobid/jobmanager/config` returning `ConfigurationInfoEntry[]` belongs to `JobManagerJobConfigurationHandler`. Answer A correctly identifies the handler, URL, and response type, and provides line-pinned anchors across handler, headers, response model, endpoint wiring, and version infrastructure.

### 7. Flink REST pattern for JobExceptionsHandler (`flink-rest-job-exceptions-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.87`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: B names every concrete artifact an engineer needs: response-body class (JobExceptionsInfoWithHistory), both query-parameter classes, WebMonitorEndpoint wiring, and line-anchored citations for handler logic, marshalling tests, and doc generators. It also describes the actual response-handling semantics (default max=20, truncation flag, failureLabelFilter, global vs local paths). A identifies the top-level handler and test but never reaches the message-parameter or response-body layer, making it far less actionable.

### 8. Flink REST pattern for JobAccumulatorsHandler (`flink-rest-job-accumulators-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B provides line-pinned source references for every named artifact, describes the exact accumulator construction logic (getAccumulatorResultsStringified, getAccumulatorsSerialized, includeSerializedValue toggle), names JobAccumulatorsInfoTest as an existing test, and correctly identifies WebMonitorEndpoint wiring and RuntimeRestAPIVersion.V1. A names the right classes but cites only nightlies doc anchors without line numbers and misses JobAccumulatorsInfoTest entirely, reducing actionability.

### 9. Flink REST pattern for JobPlanHandler (`flink-rest-job-plan-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B traces the full data path: AccessExecutionGraph.getPlan() → JobPlanInfo wrapping → response, and correctly identifies JsonPlanGenerator as the plan serializer. It also surfaces the flink-docs module generators as the true doc anchor (generated, not hand-written), adds JobPlanInfoTest and JsonGeneratorTest as more directly relevant tests, and names archiveJsonWithPath() as a concrete archiving hook. A is accurate at the type-signature level but stops short of the actual method-level flow and cites less relevant neighboring tests (SavepointHandlersTest).

### 10. Flink REST pattern for JobVertexDetailsHandler (`flink-rest-job-vertex-details-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.87`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B is strictly more useful: it supplies line-pinned source refs for handler registration (WebMonitorEndpoint:658-666), API versioning (RuntimeRestAPIVersion:30-34), the docs-generation pipeline (RuntimeRestAPIDocGenerator, RuntimeOpenApiSpecGenerator), and the missing but critical JobVertexDetailsInfoTest. It also names four vertex-scoped sibling tests (BackPressure, FlameGraph, SubtaskCurrentAttempt, SubtaskExecutionAttempt) that A omits. A's nightlies doc URLs are valid anchors but add no implementation depth, and it misses JobVertexDetailsInfoTest entirely.

### 11. Flink REST pattern for JobVertexTaskManagersHandler (`flink-rest-job-vertex-taskmanagers-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B provides line-pinned source anchors for the handler, headers, WebMonitorEndpoint wiring, and the doc generator—covering the full routing chain. It correctly identifies JobVertexTaskManagersInfoTest and adjacent job-vertex handler tests (BackPressure, FlameGraph) as the closest test patterns. A names the right classes but omits wiring proof, cites no line numbers, and its neighboring tests (JobConfigHandler, JobsOverviewHandler) are weaker analogues for job-vertex-scoped routing.

### 12. Flink REST pattern for JobCancellationHandler (`flink-rest-job-cancellation-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.87`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B names the actual HTTP contract (PATCH /jobs/:jobid, 202/409/408/404/500), traces the internal flow (gateway.cancelJob → error mapping), identifies TerminationModeQueryParameter and WebMonitorEndpoint wiring with line numbers, and correctly anchors docs on the generator pipeline rather than static fragments. A names the right files but provides no behavioral detail; its doc fragment anchors (part-0001–0003) point at generic REST overview sections, not cancellation specifics.

### 13. Flink REST pattern for SavepointHandlers (`flink-rest-savepoint-handlers`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.95`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: B names the exact inner classes (SavepointTriggerHandler, SavepointStatusHandler), their gateway calls, HTTP verb/status codes via SavepointTriggerHeaders/SavepointStatusHeaders, WebMonitorEndpoint registration lines, and three additional message-marshalling tests. A correctly identifies the top-level class and two tests but provides no method-level detail, no endpoint shape, and no registration anchor. B's extra risk deduction is for line-number claims that could drift, partially offset by its honest Javadoc-inconsistency note.

### 14. Flink REST pattern for CheckpointHandlers (`flink-rest-checkpoint-handlers`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: A names concrete message classes (CheckpointTriggerHeaders, CheckpointStatusHeaders, CheckpointTriggerRequestBody), the versioning class, the doc generator, and multiple neighboring tests with specific coverage gaps identified. B hedges on method-level detail, cites ops/state/checkpoints docs that cover configuration not REST handler behavior, and fails to name the message or versioning classes at all. A's V0/V1 versioning note and IN_PROGRESS coverage gap are actionable; B's guidance is too vague to act on.

### 15. Flink REST pattern for JobResourceRequirementsUpdateHandler (`flink-rest-job-resource-requirements-update-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: A correctly identifies two-layer validation (empty-body 400 in the handler, semantic validation via Dispatcher.validateMaxParallelism/JobResourceRequirements.validate), names all directly relevant classes, and cites DispatcherTest ranges that exercise the update path. B's neighbor tests (JobDetailsHandlerTest, JobStatusHandlerTest) test unrelated handlers and add no insight into resource-requirements validation. A's specific line numbers and doc-generator class names are unverifiable and likely fabricated, but the architectural description is structurally sound.

### 16. Flink REST pattern for JobSubmitHandler (`flink-rest-job-submit-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides line-precise anchors for every relevant class (JobSubmitHandler, JobSubmitRequestBody, JobSubmitHeaders, DispatcherRestEndpoint), names the executionPlanFileName/jobGraphFileName alias, states the 202 response code, and identifies the highest-value missing test branch. B correctly names the primary file and test but omits field-level detail, response codes, and validation branches, and cites WebMonitorEndpoint as the registration model where DispatcherRestEndpoint is the direct anchor for job submission.

### 17. Flink REST pattern for FileUploads (`flink-rest-file-uploads`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A maps the full lifecycle: FileUploadHandler -> FileUploads -> AbstractHandler -> HandlerRequest, with version-pinned repo URIs for every class and test. It names FileUploadsTest, AbstractHandlerTest, FileUploadHandlerITCase, RestServerEndpointITCase, and MultipartRoutesTest with line ranges. B correctly identifies FileUploads and FileUploadsTest but stops there; its nightlies.apache.org URLs do not name FileUploads and WebMonitorEndpoint is a real class but not an upload-path anchor. B is narrower and less actionable.

### 18. Flink REST pattern for DashboardConfigHandler (`flink-rest-dashboard-config-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B provides line-range-anchored citations for every artifact, identifies the cached-snapshot behavior in handleRequest(), names the DashboardConfiguration.from() factory, pins the stable API version via RuntimeRestAPIVersion.V1, and surfaces DashboardConfigurationTest as an existing regression anchor. A omits DashboardConfiguration.java entirely, substitutes weaker neighboring handler tests, and provides no line-level precision. B's one risk is that line numbers may be approximate, but all structural claims are internally consistent and Flink-idiomatic.

### 19. Flink REST pattern for ClusterOverviewHandler (`flink-rest-cluster-overview-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B names the actual construction chain: gateway.requestClusterOverview(timeout) → ClusterOverviewWithVersion.fromStatusOverview(statusOverview, version, commitID), places ClusterOverviewWithVersion in the correct handler/legacy/messages package, identifies WebMonitorEndpoint as the registration site, and surfaces directly relevant tests (ClusterOverviewWithVersionTest, WebMonitorMessagesTest). A correctly states the generic type signature but stops there, and its 'neighboring' test citations (JobManagerLogListHandlerTest) are tangential rather than structurally related.

### 20. Flink REST pattern for TaskManagersHandler (`flink-rest-taskmanagers-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A provides deeper implementation anchors: `TaskManagersInfo`, `TaskManagersHeaders`, `RuntimeRestAPIVersion.V1`, the doc generator class, and marshalling tests (`TaskManagersInfoTest`, `TaskManagerInfoTest`). B adds live nightlies URLs for docs but omits the response wrapper class, headers class, and marshalling tests entirely. A's call-chain description (`requestTaskManagerInfo -> TaskManagersInfo::new`) is more actionable. Both correctly avoid hallucinated frameworks. B's neighboring tests (profiling handlers) are less relevant than A's marshalling and details-handler tests.

### 21. Flink REST pattern for TaskManagerDetailsHandler (`flink-rest-taskmanager-details-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.92`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B names the actual lookup mechanism (ResourceManagerGateway.requestTaskManagerDetailsInfo), the exception-to-404 mapping (UnknownTaskExecutorException → RestHandlerException), version pinning via RuntimeRestAPIVersion.V1, and the flink-docs generator classes. It provides line-number anchors, sibling 404 tests, upstream contract tests, and identifies the specific gap in TaskManagerDetailsHandlerTest. A correctly names the right files but describes no behavior, provides no line numbers, and offers no actionable gap analysis.

### 22. Flink REST pattern for JobVertexBackPressureHandler (`flink-rest-job-vertex-back-pressure-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 4}}`
- Rationale: B covers both required modules (flink-docs and flink-runtime), surfaces the docs generation pipeline (RuntimeRestAPIDocGenerator, RuntimeOpenApiSpecGenerator), adds the response-shape anchor (JobVertexBackPressureInfo.java), and names the serialization/enum tests (JobVertexBackPressureInfoTest, VertexBackPressureLevelTest, VertexBackPressureStatusTest). It also provides the concrete behavioral claim about DEPRECATED vs OK responses. A omits flink-docs entirely and its neighboring tests (JobConfigHandler, JobDetailsHandler) are less relevant than B's SubtaskCurrentAttemptDetailsHandlerTest.

### 23. Flink REST pattern for JobVertexWatermarksHandler (`flink-rest-job-vertex-watermarks-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A names the exact metric (MetricNames.IO_CURRENT_INPUT_WATERMARK), the correct REST path, the handler/headers pair, WebMonitorEndpoint registration, the flink-docs generator pipeline, and adjacent metric test bases — all architecturally consistent with real Flink REST patterns. The risk is fabricated line numbers. B correctly cites verifiable nightlies docs and avoids overspecification, but recommends AbstractAsynchronousOperationHandlersTest as a neighbor to a simple synchronous GET handler — a weak pattern match — and delivers less actionable guidance overall.

### 24. Flink REST pattern for SubtaskCurrentAttemptDetailsHandler (`flink-rest-subtask-current-attempt-details-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 3, "usefulness": 2}}`
- Rationale: Answer A misidentifies the route: SubtaskCurrentAttemptDetailsHandler serves GET .../subtasks/:subtaskindex (current/latest attempt), not .../attempts/:attempt — that is SubtaskExecutionAttemptDetailsHandler. This is a fundamental correctness failure that would misdirect an engineer. Answer B correctly distinguishes the two sibling routes, names SubtaskCurrentAttemptDetailsHeaders as the route definer, pins WebMonitorEndpoint.java#L603 as the registration site, and contrasts SubtaskMessageParameters vs SubtaskAttemptMessageParameters — all actionable and technically sound.

### 25. Flink REST pattern for JobVertexFlameGraphHandler (`flink-rest-job-vertex-flame-graph-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B provides line-pinned source citations, names the RestOptions.ENABLE_FLAMEGRAPH gate, VertexFlameGraphFactory, VertexThreadInfoTracker, and the doc-generator chain — all concrete, verifiable anchors. A gives correct high-level guidance and valid file paths but lacks line numbers, misses the feature-flag wiring, and omits the sampling/factory layer. B's uncertainty disclosure about the missing WebMonitorEndpoint test branch is honest and actionable.

### 26. Flink checkpointing pattern for CheckpointCoordinator (`flink-checkpointing-checkpoint-coordinator`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides line-range-pinned anchors for every coordinator responsibility (PendingCheckpoint creation, storage init, operator-coordinator snapshotting, master hooks, trigger loop) and names five specialized test classes. No hallucination markers appear. B cites valid nightlies docs URLs and correct neighboring classes but stays at class-level granularity, names only one test class, and explicitly declines to describe internals—making it correct but much less actionable. A's main risk is that specific line numbers may drift; B's caution is disciplined but over-limits usefulness.

### 27. Flink checkpointing pattern for PendingCheckpoint (`flink-checkpointing-pending-checkpoint`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: A gives a precise state-transition narrative (notYetAcknowledged flags, dispose(bool), TaskAcknowledgeResult enum values, savepoint canBeSubsumed edge case) with pinned line ranges across PendingCheckpoint and CheckpointCoordinator plus multiple test classes. B correctly identifies the high-level pending→completed arc and links nightlies docs, but provides no line anchors, omits the abort/discard path, and names only PendingCheckpointTest. B's nightlies URLs use a fragment (#part-0001) that is not a stable anchor.

### 28. Flink checkpointing pattern for CompletedCheckpoint (`flink-checkpointing-completed-checkpoint`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B provides line-range-pinned citations covering the full lifecycle: constructor fields, shared-state re-registration, subsume/shutdown hooks, discard path, and the store contract. It also surfaces CompletedCheckpointStoreTest and StandaloneCompletedCheckpointStoreTest as additional test anchors, and identifies the untested async-discard branch as a coverage gap. A is correct at a high level but generic — no line ranges, fewer test anchors, and the nightlies doc URLs are unverifiable fragment anchors.

### 29. Flink checkpointing pattern for CompletedCheckpointStore (`flink-checkpointing-completed-checkpoint-store`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A names every relevant class with pinned line ranges: CheckpointSubsumeHelper, DefaultCompletedCheckpointStoreUtils, StandaloneCompletedCheckpointStore, and the ZK integration test — all critical for understanding the full retention path. It also correctly distinguishes store retention from externalized checkpoint cleanup. B adds FileSystemCheckpointStorage (tangential) and nightlies.apache.org URLs with fragment anchors that cannot be verified as stable, reducing grounding quality. Neither answer hallucinates forbidden markers.

### 30. Flink checkpointing pattern for DefaultCompletedCheckpointStore (`flink-checkpointing-default-completed-checkpoint-store`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.76`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A names CheckpointSubsumeHelper as the eviction mechanism, provides line-pinned references, and lists specific test method names — all directly actionable for an engineer reading the 2.2.0 source. B stays at file-level granularity and omits CheckpointSubsumeHelper entirely. B's reference to StandaloneCompletedCheckpointStoreTest is risky because that class was folded into the default store in 2.x. Both answers have a potential config-key name discrepancy, but A's honest uncertainty note on the ZK recovery divergence improves credibility.

### 31. Flink checkpointing pattern for CheckpointStatsTracker (`flink-checkpointing-checkpoint-stats-tracker`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B provides exhaustive class coverage (CheckpointStatsCounts, CheckpointStatsHistory, CompletedCheckpointStatsSummary, CheckpointStatsSnapshot, REST layer) with precise line-number ranges, seven anchored tests, and a honest acknowledgment that standalone markdown docs were not found. A's nightlies.apache.org fragment anchors (#part-0001, #part-0003) are unverifiable and likely fabricated; citing TestTaskStateManager as a checkpoint-stats test is a stretch. B's specificity on the dirty-snapshot path and reportFailedCheckpointsWithoutInProgress gap is directly actionable.

### 32. Flink checkpointing pattern for CheckpointStatsSnapshot (`flink-checkpointing-checkpoint-stats-snapshot`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A names the full producer chain (DefaultCheckpointStatsTracker → snapshot creation), pins line ranges, includes REST handler and ArchivedExecutionGraph tests, and correctly identifies docs as REST metadata classes rather than fabricating prose pages. B adds nightlies URLs that cannot be verified as correct anchors (fragment #part-0001 is likely auto-generated and unstable) and omits the tracker class entirely, leaving the snapshot creation path unexplained. A's coverage of neighboring tests is substantially deeper and more actionable.

### 33. Flink checkpointing pattern for CheckpointMetrics (`flink-checkpointing-checkpoint-metrics`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 3}}`
- Rationale: B more accurately targets the coordinator-side reporting path (DefaultCheckpointStatsTracker, PendingCheckpoint, SubtaskStateStats) rather than the task-side acknowledgement path (CheckpointResponder, Environment) that A names. For 'reporting code,' B's consumers are the right anchors. B also adds CheckpointMetricsBuilder and more targeted tests. However, B's claim that unalignedCheckpoint is derived from bytesPersistedDuringAlignment > 0 is likely fabricated; the field is explicitly set via the builder.

### 34. Flink checkpointing pattern for CheckpointProperties (`flink-checkpointing-checkpoint-properties`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: A names every flag by exact identifier (forced, discardSubsumed, discardFinished, discardCancelled, discardFailed, discardSuspended, unclaimed), ties each to its behavioral contract, and pins all claims to line-ranged source URIs across six runtime classes. B gestures at a 'delete/retain matrix' without naming flags, offers doc URLs with meaningless #part-0001 anchors, and attributes savepoint non-queuing to 'time-trigger limits' — imprecise phrasing not grounded in the source. A also surfaces SavepointType, MetadataV4Serializer, RecoveryClaimMode, and a concrete regression gap.

### 35. Flink checkpointing pattern for CheckpointRetentionPolicy (`flink-checkpointing-checkpoint-retention-policy`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: A correctly names all three enum values, explains the ExternalizedCheckpointRetention→CheckpointRetentionPolicy mapping chain, cites pinned source paths with line ranges across docs, runtime, and test modules, and identifies a concrete coverage gap. B hedges so aggressively it fails to name a single enum constant or describe any semantic, making it near-useless for an engineer. B's nightlies URLs are legitimate but the state_backends link is tangential and low-signal.

### 36. Flink checkpointing pattern for CheckpointIDCounter (`flink-checkpointing-checkpoint-id-counter`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A provides pinned line-range anchors for every claim: INITIAL_CHECKPOINT_ID=1, getAndIncrement() usage in CheckpointCoordinator, setCount() restore path, and a complete test inventory including CheckpointIDCounterTestBase and ZKCheckpointIDCounterMultiServersTest. B covers the same interface/impl trio but omits line numbers, misses CheckpointIDCounterTestBase (the primary shared test base), and falsely implies no dedicated counter test exists while A names it explicitly.

### 37. Flink checkpointing pattern for StandaloneCheckpointIDCounter (`flink-checkpointing-standalone-checkpoint-id-counter`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 5, "specificity": 2, "usefulness": 2}}`
- Rationale: B surfaces the actual allocation semantics (AtomicLong, INITIAL_CHECKPOINT_ID=1, getAndIncrement/getLast contract), HA-mode wiring via StandaloneCheckpointRecoveryFactory, and line-level source anchors across implementation, factory, and coordinator tests. A correctly identifies the right files but over-hedges into near-uselessness, never stating what the counter does. Neither answer uses the flagged hallucination markers. B's only risk is that cited line numbers could drift, but the behavioral claims are consistent with the known implementation.

### 38. Flink checkpointing pattern for CheckpointFailureManager (`flink-checkpointing-checkpoint-failure-manager`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B supplies line-number-anchored citations, internal method names (handleJobLevelCheckpointException, checkFailureAgainstCounter, handleCheckpointSuccess), five named test cases, and covers sync-savepoint/JM-vs-task routing edge cases. A names only one test method, omits internal method detail, and references CheckpointCoordinatorFailureTest which likely does not exist as a standalone file in release-2.2.0, introducing hallucination risk.

### 39. Flink checkpointing pattern for CheckpointPlanCalculator (`flink-checkpointing-checkpoint-plan-calculator`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B names the full API surface: CheckpointPlanCalculatorContext, ExecutionGraphCheckpointPlanCalculatorContext, and the DefaultExecutionGraph wiring point — all missing from A. B also describes concrete behavioral logic (async on JobMaster executor, ALL_TO_ALL/POINTWISE branch, calculateAfterTasksFinished, allowCheckpointsAfterTasksFinished flag) and cites line-number-anchored source references. A identifies the right classes but stops at the interface/implementation pair without tracing the coordinator integration or context contract.

### 40. Flink checkpointing pattern for DefaultCheckpointPlanCalculator (`flink-checkpointing-default-checkpoint-plan-calculator`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 5, "specificity": 3, "usefulness": 3}}`
- Rationale: A names the production wiring site (DefaultExecutionGraph), both context types (CheckpointPlanCalculatorContext + ExecutionGraphCheckpointPlanCalculatorContext), the allowCheckpointsAfterTasksFinished gate, and four distinct test classes with line anchors — giving a complete navigation map. B adds real versioned docs URLs (genuine value) but omits context implementations, the production instantiation site, and the finished-tasks behavioral branch. A's specific line numbers are unverifiable and could be fabricated, which is its primary risk.

### 41. Flink checkpointing pattern for CheckpointRequestDecider (`flink-checkpointing-checkpoint-request-decider`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 3}}`
- Rationale: B enumerates the actual priority comparator rules (savepoints > forced > non-periodic > periodic, timestamp then identityHashCode tiebreaker), queue eviction semantics, max-concurrent gating, and min-pause reschedule path with specific line numbers. A identifies the three-way model and correct failure reasons but stays too abstract to drive code changes. Neither answer uses the hallucination markers. B loses one grounding point for omitting public docs URLs; A loses specificity and usefulness points for class-level rather than line-level anchoring.

### 42. Flink checkpointing pattern for CheckpointResourcesCleanupRunner (`flink-checkpointing-checkpoint-resources-cleanup-runner`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 5, "specificity": 3, "usefulness": 3}}`
- Rationale: B names the actual cleanup algorithm: closeAsync waits on resultFuture, cleanupCheckpoints recreates CompletedCheckpointStore and CheckpointIDCounter, RecoveryClaimMode.CLAIM governs shared-state discard. It also adds DispatcherCleanupITCase, AbstractDispatcherTest, and TestingCleanupRunnerFactory as wiring/regression anchors. A is correctly conservative but its adjacent tests (CheckpointCoordinatorMasterHooksTest, TestingCompletedCheckpointStore) are less directly relevant than B's dispatcher-layer tests.

### 43. Flink checkpointing pattern for CheckpointStorageLoader (`flink-checkpointing-checkpoint-storage-loader`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: B names the actual loading precedence chain (legacy StateBackend → application storage → fromConfig → FileSystemCheckpointStorage/JobManagerCheckpointStorage), specific test method names (testLegacyStateBackendTakesPrecedence, testModernStateBackendDoesNotTakePrecedence, etc.), real callers (DefaultExecutionGraphBuilder, StreamTask), and the ConfigurableCheckpointStorage.configure() branch. A correctly identifies classes and avoids hallucination markers but never describes the algorithm or names a single test case or method, limiting its utility to pointer-level guidance.

### 44. Flink checkpointing pattern for CheckpointStorageCoordinatorView (`flink-checkpointing-checkpoint-storage-coordinator-view`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A enumerates the actual coordinator-facing method responsibilities (HA capability, savepoint resolution, location initialization), names the correct implementation hierarchy (AbstractFsCheckpointStorageAccess → FsCheckpointStorageAccess, MemoryBackendCheckpointStorageAccess), and supplies line-pinned test anchors including TestingCheckpointStorageAccessCoordinatorView. B hedges that it never saw the full class body, and its nightlies URLs carry suspicious #part-0001 fragments inconsistent with Flink's actual anchor scheme, reducing grounding trust. Neither answer uses hallucination markers.

### 45. Flink checkpointing pattern for StateBackend (`flink-checkpointing-state-backend`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A names the right concrete backend (HashMapStateBackend) for checkpointing context and supplies the canonical test hierarchy (StateBackendTestBase, HashMapStateBackendTest, StateBackendMigrationTestBase). B's primary concrete example—BatchExecutionStateBackend—is the batch-mode backend and is a misleading anchor for checkpointing semantics. B also admits it could not surface a dedicated StateBackend test class, leaving the test requirement largely unmet. B's nightlies.apache.org doc URLs add marginal value but do not offset the weaker test and implementation choices.

### 46. Flink checkpointing pattern for OperatorStateBackend (`flink-checkpointing-operator-state-backend`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.92`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 2, "usefulness": 2}}`
- Rationale: B correctly names the full implementation stack: OperatorStateBackend (interface), DefaultOperatorStateBackend (concrete owner), DefaultOperatorStateBackendSnapshotStrategy (checkpoint write path emitting OperatorStateHandles), and OperatorStateRestoreOperation (restore counterpart). A omits all three concrete classes, making it insufficient for engineers changing Java code. A's StateBackendUtils citation path is likely fabricated. B provides line-level source anchors and a richer test matrix without invoking any hallucination markers.

### 47. Flink checkpointing pattern for KeyedStateBackend (`flink-checkpointing-keyed-state-backend`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 2, "usefulness": 2}}`
- Rationale: A correctly traces the full class hierarchy (KeyedStateBackend → CheckpointableKeyedStateBackend → AbstractKeyedStateBackend → HeapKeyedStateBackend), names directly relevant test anchors (StateBackendTestBase, KeyedStateCheckpointOutputStreamTest, StateBackendMigrationTestBase), and identifies the SnapshotStrategyRunner delegation path. B's doc URLs use a non-standard #part-0001 anchor format, and its test selections (MergedChannelStateHandleTest, TaskExecutorFileMergingManagerTest) target channel/file-merge state rather than keyed-state checkpointing.

### 48. Flink checkpointing pattern for SavepointRestoreSettings (`flink-checkpointing-savepoint-restore-settings`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.7`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 5, "specificity": 3, "usefulness": 3}}`
- Rationale: B adds concrete value: recoveryClaimMode/NO_CLAIM semantics, StateRecoveryOptions config-key serialization path, and additional CheckpointCoordinator restore tests. A is conservative and safe but lacks method-signature depth and misses the config-key layer entirely. B's risk comes from the unverified three-arg forPath signature and from including CheckpointCoordinatorTriggeringTest, which is not primarily a restore-path test. Neither answer hits hallucination markers.

### 49. Flink checkpointing pattern for SavepointFormatType (`flink-checkpointing-savepoint-format-type`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B correctly identifies the three-member enum including DEFAULT as a CANONICAL alias, covers the full call chain (enum → JobClient → REST request bodies defaulting to DEFAULT → handlers → StreamTask compatibility gate → StateBackend contract), and cites specific line numbers. A misses the DEFAULT variant entirely and names `EventSerializer.decodeSavepointType(...)` — a suspicious method that does not exist under that signature — as a primary anchor, introducing hallucination risk.

### 50. Flink checkpointing pattern for CheckpointCoordinatorConfiguration (`flink-checkpointing-checkpoint-coordinator-configuration`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides line-numbered source anchors across the full chain: CheckpointingOptions, CheckpointConfig, CheckpointCoordinatorConfiguration, CheckpointCoordinator, REST handler, and seven concrete test classes. It also correctly identifies the docs-generator path and its package-discovery scope limitation. B cites the same implementation class and nightlies docs URLs but cannot enumerate fields/methods, names only two tests (one tangential: OperatorCoordinatorHolderTest), and adds no line references.

### 51. Kafka Connect pattern for ConnectorPluginsResource (`kafka-rest-connector-plugins-resource`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: B names the actual endpoint path, specific test-case methods (testValidateConfigWithSimpleName, testValidateConfigWithAlias, etc.), AbstractHerder delegation with line numbers, and the EmbeddedConnect integration helper. A stays class-level only — no method names, no line numbers, no specific test-case names — making it far less actionable. Neither answer triggers the hallucination markers. B's concession that no separate docs artifact exists is honest and correct.

### 52. Kafka Connect pattern for AbstractHerder (`kafka-connect-abstract-herder`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.9`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: B traces the full validation chain: Herder interface contract → AbstractHerder async wrapper (connectorExecutor) → core validateConnectorConfig overload → ConnectorPluginsResource REST entrypoint, with precise line-number citations. It names five test classes with specific coverage descriptions. A identifies the correct top-level files but omits the Herder interface, the REST layer, and integration tests, and provides no line numbers, leaving an engineer without a navigable call chain.

### 53. Kafka Connect pattern for DistributedHerder (`kafka-connect-distributed-herder`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.92`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B names specific line ranges, concrete method names (onConnectorConfigUpdate, processConnectorConfigUpdates, needsReconfigRebalance), the connector-vs-task config update split, KafkaConfigBackingStore semantics, and exact test method names. A provides only structural anchors (file paths, doc URLs) with no method-level specificity and admits it cannot identify the config-update path. B's behavioral claim about local restart vs rebalance is the core semantic distinction an engineer needs.

### 54. Kafka Connect pattern for StandaloneHerder (`kafka-connect-standalone-herder`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.87`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 3, "usefulness": 3}}`
- Rationale: B provides line-number-pinned citations for every method (putConnectorConfig:204-257, patchConnectorConfig:263-281, updateConnectorTasks:523-587) and names specific test methods (testPutConnectorConfig, testPatchConnectorConfig, testRequestTaskReconfigurationDoesNotDeadlock) with line ranges. A omits line numbers entirely and its docs URLs (kafka.apache.org/42/kafka-connect/user-guide/#part-0001) do not match standard Kafka versioned-doc URL patterns, raising fabrication risk. B honestly acknowledges missing prose docs.

### 55. Kafka Connect pattern for Herder (`kafka-connect-herder`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B names the actual `Herder` interface with line-pinned citations, lists concrete method signatures (`connectorInfo`, `patchConnectorConfig`, `deleteConnectorConfig`), covers `StandaloneHerder` alongside `DistributedHerder`, maps the REST bridge via `ConnectorsResource`, and provides line-numbered test anchors for every implementation class. A conflates the REST API docs with the Java interface, admits it never located `Herder.java`, and supplies only one adjacent test hit with no line numbers.

### 56. Kafka Connect pattern for Worker (`kafka-connect-worker`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 2, "usefulness": 3}}`
- Rationale: A directly anchors on Worker.java with precise line-range citations covering the full connector/task lifecycle (start, startConnector, startSinkTask, startSourceTask, stopAndAwaitTask), plus WorkerTest and integration test line ranges. B deflects to AbstractHerder as the primary implementation anchor without surfacing Worker.java, misses WorkerTest entirely, and links to external docs URLs that may not be version-stable. AbstractHerder handles lifecycle state tracking but is not the class responsible for connector/task instantiation and execution—that is Worker.

### 57. Kafka Connect pattern for WorkerConnector (`kafka-connect-worker-connector`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides line-precise source anchors for every lifecycle method (initialize, doStart, onFailure, doShutdown, raiseError), names the exact test methods covering each failure scenario, and correctly identifies Worker.startConnector() as the construction/failure-conversion callsite. B's public kafka.apache.org/42/ URLs are plausible but unverifiable and may not exist; its test method citations (testStopFailure, testFailConnectorThatIsNeitherSourceNorSink) are plausible but lack line anchors, and ExactlyOnceSourceIntegrationTest is a weak adjacent reference with no demonstrated connection to WorkerConnector startup.

### 58. Kafka Connect pattern for WorkerTask (`kafka-connect-worker-task`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides concrete method-level anchors (doStart, doClose, cancel, awaitStop), precise line ranges across the full hierarchy (Task → WorkerTask → AbstractWorkerSourceTask/WorkerSinkTask), and names five targeted test classes with specific test-scenario descriptions. B identifies correct classes but omits method names and line references; its kafka.apache.org/42/kafka-connect/connector-development-guide/ URL is a plausible fabrication not matching known Kafka docs URL structure, adding citation risk without grounding benefit.

### 59. Kafka Connect pattern for WorkerSinkTask (`kafka-connect-worker-sink-task`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 2, "usefulness": 3}}`
- Rationale: A provides precise line-range anchors for WorkerSinkTask covering the main loop, commit execution, preCommit filtering, redelivery, and rebalance. It names specific test methods (testRequestCommit, testPreCommit, testCommitWithOutOfOrderCallback, threaded variants) with line ranges. B cites unverifiable external URLs, invents method names (recordBatch, recordCommitSuccess, getNextCommit) not present in WorkerSinkTask, and recommends off-topic integration tests. A's only risk is unverified line numbers; B's fabricated API names are a harder failure.

### 60. Kafka Connect pattern for WorkerSourceTask (`kafka-connect-worker-source-task`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A correctly identifies that the poll loop lives in AbstractWorkerSourceTask, not WorkerSourceTask itself — a structurally critical distinction B omits entirely. A names specific methods (beginSendIteration, recordSent, commitTaskRecord), individual test cases, and provides line-range anchors. B's public doc URLs (kafka.apache.org/42/...) are unverified and potentially fabricated; its test references lack method-level precision. B's ErrorHandlingTaskTest addition is useful but insufficient to close the gap.

### 61. Kafka Connect pattern for ConnectorConfig (`kafka-connect-connector-config`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A names real inner classes (EnrichablePlugin, PluginVersionValidator), the correct transform/predicate enrichment path, and enumerates six test files with line ranges — directly actionable for code navigation. B is architecturally correct but file-level only, omitting method names and line anchors. A's risk is that precise line ranges and ConnectorValidationIntegrationTest may be partially fabricated; B avoids this by being deliberately vague, which lowers usefulness.

### 62. Kafka Connect pattern for SinkConnectorConfig (`kafka-connect-sink-connector-config`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.87`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 3}}`
- Rationale: B names the exact method signature validate(Map<String,String>, Map<String,ConfigValue>), enumerates helper methods (hasTopicsConfig, hasDlqTopicConfig, parseTopicsList), and provides actionable line numbers across SinkConnectorConfig, AbstractHerder, WorkerSinkTask, WorkerConnector, build.gradle, and four test files with described scenarios. A covers the same conceptual ground but without line numbers or the build-system docs-generation anchor, making it less actionable. Neither answer introduces hallucination markers.

### 63. Kafka Connect pattern for SourceConnectorConfig (`kafka-connect-source-connector-config`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A correctly identifies the two-layer validation chain: SourceConnectorConfig for config-def validation and DistributedHerder.validateSourceConnectorConfig() for source-specific runtime checks (exactly-once, transaction boundaries). B omits DistributedHerder entirely, missing the primary source-connector-specific preflight path. A names concrete config keys and explains what each test covers. B's external URL anchors (e.g., #part-0019) are likely fabricated fragments, adding hallucination risk.

### 64. Kafka Connect pattern for WorkerConfig (`kafka-connect-worker-config`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A names exact line ranges for WorkerConfig, StandaloneConfig, DistributedConfig, and five test classes with concrete method-level anchors. It correctly identifies parse-time warnings, originals() stripping, and plugin.discovery. B cites external kafka.apache.org URLs (unverifiable in a repo snapshot) and skips DistributedConfig/DistributedConfigTest entirely, leaving a significant gap. Neither answer introduces hallucinated validators, keeping risk scores high for both.

### 65. Kafka Connect pattern for DistributedConfig (`kafka-connect-distributed-config`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides line-level anchors across DistributedConfig.java, DistributedConfigTest, backing store tests, and InternalTopicsIntegrationTest — all plausible for the 4.2 tree — and honestly disclaims missing versioned docs. B fabricates kafka.apache.org/42/kafka-connect/* URLs not known to exist in that form, which is the primary hallucination risk. B's code references are real but coarse; it names far fewer neighboring test files.

### 66. Kafka Connect pattern for StandaloneConfig (`kafka-connect-standalone-config`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides line-number-pinned anchors across five real Kafka Connect source files and honestly admits the rendered docs tree was absent. B introduces external URLs with a suspicious path scheme (kafka.apache.org/42/...) and fragment anchors (#part-0001) that do not match actual Kafka documentation URL patterns, creating hallucination risk. A's broader test coverage inventory (FileOffsetBackingStoreTest, WorkerTest, ConnectRestServerTest alongside StandaloneConfigTest) is more actionable for an engineer investigating config wiring.

### 67. Kafka Connect pattern for ConfigDef (`kafka-connect-config-def`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.92`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 2, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B accurately explains the parse() (strict, throws) vs validate() (soft, returns ConfigValue list) distinction, the full Type enum, ValidList deduplication, and the ConnectorConfig/Connector.validate() layering—all with line-specific source anchors. A names ConfigDef correctly but provides no method-level semantics and hedges every claim into near-uselessness. B's only risk is that specific line numbers cannot be independently verified here.

### 68. Kafka Connect pattern for ConfigValue (`kafka-connect-config-value`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.74`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B adds the critical REST projection layer (ConfigValue → ConfigValueInfo via AbstractHerder) that A omits entirely, making the full validation-result lifecycle traceable. B also correctly anchors ConfigDef.java as the validation driver. A's #part-0019 docs fragment anchor is unverifiable and likely fabricated; its ExactlyOnceSourceIntegrationTest citation for ConfigValue.errorMessages() is a poor fit. Both answers avoid hallucination markers and correctly describe the five ConfigValue fields.

### 69. Kafka Connect pattern for ConfigTransformer (`kafka-connect-config-transformer`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 5}}`
- Rationale: Both answers correctly anchor on ConfigTransformer + WorkerConfigTransformer and cite WorkerConfigTransformerTest. B adds AbstractHerder (where transformConnectorConfig is invoked during validation) and ClusterConfigState (transformed-vs-raw config storage), giving a more complete transformation chain. B also supplies public docs URLs (/42/ scheme), satisfying the question's explicit docs requirement. A's line-number anchors add false precision — line numbers shift between commits and cannot be verified, raising hallucination risk.

### 70. Kafka Connect pattern for ConfigProvider (`kafka-connect-config-provider`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.92`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B traces the full resolution chain: ConfigProvider interface → AbstractConfig config.providers keys and ${provider:[path:]key} syntax → ConfigTransformer substitution semantics → WorkerConfigTransformer Connect-side wiring, all with line-pinned source anchors and relevant test files. A identifies the interface and FileConfigProvider correctly but omits AbstractConfig, ConfigTransformer, and the Connect runtime wiring entirely, leaving an engineer with only half the picture.

### 71. Kafka Connect pattern for Plugins (`kafka-connect-plugins`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.9`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B correctly surfaces the 4.2-era dual-scanner architecture (ReflectionScanner vs ServiceLoaderScanner), PluginDiscoveryMode enum, and maybeReportHybridDiscoveryIssue — all real, version-specific artifacts. It names the correct primary test class (PluginsTest.java), MultiVersionTest, and DelegatingClassLoaderTest with actionable line ranges. A is conceptually sound but misses the scanner split, cites TestPlugins.java (a fixture helper, not the behavioral test class), and lacks line-level anchors.

### 72. Kafka Connect pattern for PluginDesc (`kafka-connect-plugin-desc`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.87`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B identifies the full descriptor surface: PluginDesc fields, UNDEFINED_VERSION, Jackson annotations, and the PluginInfo REST bridge that maps PluginDesc to /connector-plugins output. It names six specific test methods in PluginDescTest, adds PluginInfoTest and ConnectorPluginsResourceTest for serialization/version filtering, and correctly observes that the authoritative version-pinned docs are inline ConfigDef strings in WorkerConfig/ConnectorConfig, not a separate markdown page. A is correct but shallow — no line numbers, no test method names, no REST layer.

### 73. Kafka Connect pattern for PluginType (`kafka-connect-plugin-type`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 3, "specificity": 2, "usefulness": 3}}`
- Rationale: A names all nine PluginType enum values, correctly identifies superClass()/toString() behavior, and provides line-level anchors across five implementation classes and four test files. B's external URL fragments (#part-0040, #part-0001) look like placeholder anchors unlikely to resolve to real sections, and it adds no line-level specificity. A honestly flags missing dedicated docs rather than fabricating URLs, and covers PluginDesc/PluginInfo/scanner integration that B omits entirely.

### 74. Kafka Connect pattern for DelegatingClassLoader (`kafka-connect-delegating-class-loader`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B provides line-range-pinned citations across DelegatingClassLoader, PluginClassLoader, WorkerConfig, and Plugins.java, naming concrete methods (findPluginLoader, loadVersionedPluginClass) and specific test ranges. A names the same files but without line anchors or method names, making it harder for an engineer to navigate. B also adds PluginsTest and PluginUtilsTest as end-to-end coverage layers that A omits. Both correctly describe child-first delegation; neither hallucinates forbidden APIs.

### 75. Kafka Connect pattern for PluginClassLoader (`kafka-connect-plugin-class-loader`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B provides line-range anchors across seven source and nine test files, names the real `PluginUtils.shouldLoadInIsolation` predicate, and honestly admits finding no standalone docs tree. A introduces `ClassLoaderFactory.java` as a neighbor—no such class exists in Kafka Connect's isolation package; that logic lives in `PluginUtils`—and its kafka.apache.org/42 doc URLs are unverifiable and structurally suspect. B's test coverage (PluginsTest, PluginDescTest, PluginScannerTest) is richer and more actionable.

### 76. Kafka Connect pattern for PluginScanResult (`kafka-connect-plugin-scan-result`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A provides pinned line-range anchors for every referenced source file, names all four scanner/result classes plus PluginDiscoveryMode, and identifies four distinct neighboring tests with specific line ranges. B cites kafka.apache.org/42 docs URLs that are plausible but unverifiable at this depth, surfaces only PluginScanResult and Plugins.java as implementation anchors, and omits ReflectionScanner, ServiceLoaderScanner, and DelegatingClassLoaderTest. A's KIP-898 attribution is also a useful correctness anchor. Neither answer introduces hallucinated validators.

### 77. Kafka Connect pattern for PluginUtils (`kafka-connect-plugin-utils`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.92`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 3, "specificity": 2, "usefulness": 2}}`
- Rationale: B names concrete methods (pluginLocations, pluginUrls, simpleName, prunedName, computeAliases) with line-level anchors across four source files including DelegatingClassLoader as alias consumer. It describes actual behavioral semantics (comma-separated roots, symlink following, collision dropping). A identifies only the top-level class and test file with no method names or line numbers; its kafka.apache.org/42/ doc URLs use a suspicious path format and add no behavioral grounding.

### 78. Kafka Connect pattern for ConnectRestServer (`kafka-rest-connect-rest-server`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B delivers a complete lifecycle trace (AbstractConnectCli → RestServer Jetty start → Connect.initializeResources → Jersey bindings) with specific line anchors, correctly names RestServerConfig and the Jersey DI surface, and adds RestForwardingIntegrationTest and AbstractConnectCliTest as high-value anchors. A lists more test files but provides no lifecycle narrative, omits RestServerConfig and the CLI call site, and cites unverified kafka.apache.org/42 URLs without confirming they exist.

### 79. Kafka Connect pattern for RestServerConfig (`kafka-rest-rest-server-config`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B provides precise line-range citations into actual source files, names concrete factory methods (forPublic/forInternal), and expands test coverage to SSLUtilsTest, ConnectRestServerTest, and two integration tests covering CORS, SSL, and forwarding. A's citations are real but coarser, relying on rendered web docs URLs that may not resolve and lacking line anchors or method-level specificity. Neither answer touches hallucination markers (Spring Validator, javax.validation). B's acknowledgment that no rendered docs dir exists is a useful and honest uncertainty.

### 80. Kafka Connect pattern for ConnectorsResource (`kafka-rest-connectors-resource`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 5, "specificity": 3, "usefulness": 4}}`
- Rationale: A provides line-level anchors for every CRUD method, names the test line numbers for list/create/delete/put/patch/restart/offsets, and includes the forwarding integration test and EmbeddedConnect helper — all version-pinned to 4.2. B is more cautious and correctly avoids guessing method names, and adds a live docs URL, but its specificity is materially lower. B's adjacent test list (LoggingResourceTest, RootResourceTest) adds noise without CRUD relevance. A's line numbers carry some hallucination risk but are internally consistent.

### 81. Kafka Connect pattern for ConnectorStateInfo (`kafka-rest-connector-state-info`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.87`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B traces the full call chain: ConnectorsResource#getConnectorStatus → AbstractHerder#connectorStatus → ConnectorStateInfo, with line-pinned citations for each hop plus the build.gradle genConnectOpenAPIDocs task. A names the correct entity class but routes engineers to InternalConnectResourceTest, which covers internal endpoints—not the public status endpoint—making it a misleading test anchor. B's citations are actionable and verifiable; A's doc URLs are generic and unanchored to the specific response shape.

### 82. Kafka Connect pattern for ConnectorInfo (`kafka-rest-connector-info`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 3, "specificity": 2, "usefulness": 3}}`
- Rationale: B provides line-pinned source anchors for ConnectorInfo fields, the REST endpoint, AbstractHerder assembly logic, and named test methods with line ranges. A cites kafka.apache.org URLs that are not verifiable repo artifacts and offers no line-level specificity. B's uncertainty disclosure about missing docs/ tree is honest and correct. A's URL citations cannot be validated as real 4.2 doc pages and may be fabricated paths.

### 83. Kafka Connect pattern for CreateConnectorRequest (`kafka-rest-create-connector-request`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A correctly identifies that CreateConnectorRequest is a DTO with no embedded validation, names ConnectorsResource#createConnector as the actual validation site, includes ConnectStandaloneTest, and anchors line ranges in source. B recommends neighboring tests (InternalConnectResource, RootResource, ConnectorPlugins) that are not relevant to connector creation validation, and cites kafka.apache.org/42 docs URLs whose existence is unverified for this exact path.

### 84. Kafka Connect pattern for ConnectorType (`kafka-rest-connector-type`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: B names the exact classification logic (SINK/SOURCE/UNKNOWN via AbstractHerder.connectorType), provides line-anchored citations for the enum, herder, REST entities, and test methods, and correctly distinguishes the REST enum from the health enum. A lists the same top-level files but offers no classification semantics, no herder linkage, and no line anchors—making it a file index rather than an actionable answer. Neither answer hallucinates forbidden APIs.

### 85. Kafka Connect pattern for Connector (`kafka-connect-connector`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides line-number-anchored citations to real, navigable source artifacts (Connector.java, Versioned.java, BlockingConnectorTest, WorkerConnectorTest) and correctly surfaces the Versioned interface as the version contract. B introduces unverifiable external URLs (kafka.apache.org/42/kafka-connect/connector-development-guide/), a likely-fabricated ConnectorValidationIntegrationTest.java, and the tangential ExactlyOnceSourceIntegrationTest. B also leaks 'retrieval system' tooling language.

### 86. Kafka Connect pattern for SourceConnector (`kafka-connect-source-connector`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A anchors every claim to line-ranged source artifacts in the 4.2 tree, covers the full responsibility surface (exactly-once, transaction boundaries, alterOffsets, offset reset, runtime preflight), and names concrete test classes with specific line ranges. B cites external URLs that may not resolve or may not exist as stated (kafka.apache.org/42/kafka-connect/connector-development-guide), undersells the API surface, and surfaces only one integration test with no line anchors.

### 87. Kafka Connect pattern for SinkConnector (`kafka-connect-sink-connector`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.92`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 3, "specificity": 2, "usefulness": 3}}`
- Rationale: A provides precise line-range anchors across six source files and six test files, covers the full lifecycle including alterOffsets (@since 3.6), Worker offset-reset flow, REST entity shapes, and concrete integration tests. B cites unverifiable kafka.apache.org/42 URLs (non-standard path format), admits it never saw the SinkConnector class body, and surfaces only a source-oriented test as its nearest neighbor—thin coverage for a sink-specific question.

### 88. Kafka Connect pattern for Transformation (`kafka-connect-transformation`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.83`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B names the complete runtime execution path: `TransformationStage` (predicate gating, negate, close), `TransformationChain` (serial application, null short-circuit, RetryWithToleranceOperator), and `TransformationDoc` with its build task. A omits these entirely, leaving the engineer without the classes that actually implement SMT behavior. B also cites line-anchored source references and five targeted tests including end-to-end coverage. A's `ConnectorValidationIntegrationTest` is a peripheral anchor for transform semantics.

### 89. Kafka Connect pattern for HeaderConverter (`kafka-connect-header-converter`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.62`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 5, "specificity": 3, "usefulness": 4}}`
- Rationale: A wins on specificity and usefulness: it names concrete methods (toConnectHeader, fromConnectHeader, Values.parseString), behavioral semantics (UTF-8, null pass-through, BYTES_SCHEMA fallback), and more test anchors including Plugins.java and WorkerConfig. B wins on grounding with version-pinned external docs URLs and correctly surfaces SampleHeaderConverter.java as a concrete test fixture — a real artifact A missed. Neither answer uses the hallucination markers. A's behavioral claims about SimpleHeaderConverter internals carry some fabrication risk.

### 90. Kafka Connect pattern for Converter (`kafka-connect-converter`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.87`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B correctly identifies the `Converter` interface contract including `isKey` parameter in `configure()`, names `Plugins.newConverter()` as the dispatch site, and provides line-pinned citations for concrete implementations (`StringConverter`, `NumberConverter`, `ByteArrayConverter`) plus a comprehensive test matrix across source/sink/worker paths. A stays at the config layer only, never reaches the actual `Converter` interface, and its cited test (`ConnectorValidationIntegrationTest`) is tangential to converter key/value behavior.

### 91. Kafka Connect pattern for Schema (`kafka-connect-schemas`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B anchors on Schema.java (the interface itself) before ConnectSchema, which directly answers 'inspect Schema.' It provides line-anchored URIs throughout, cites package-info.java as a high-level entry, names SchemaProjector as adjacent type, and uniquely calls out PluginUtilsTest L130-L151 as explicitly verifying Schema/ConnectSchema/SchemaBuilder/SchemaProjector class presence. A omits Schema.java entirely, uses unverifiable docs URLs, and picks less targeted converter tests (Float/Double/Long vs Byte/Boolean/Integer).

### 92. Kafka Connect pattern for SchemaBuilder (`kafka-connect-schema-builder`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides pinned line-range source anchors for SchemaBuilder, ConnectSchema, Schema, and package-info, plus multiple concrete test files. B cites external kafka.apache.org URLs whose fragment IDs (#part-0001, #part-0003) are unverifiable and likely generated, and names only one irrelevant integration test. A's only risk is the suggested SchemaBuilderTest.java may not exist; B's external URL fragments are a stronger hallucination risk.

### 93. Kafka Connect pattern for Struct (`kafka-connect-struct`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: B correctly traces the validation chain: Struct.put() -> ConnectSchema.validateValue(), names Schema.Type.STRUCT, and distinguishes validate() behavior for optional vs required fields. A identifies the right files but stops short of method-level detail and cites ExactlyOnceSourceIntegrationTest, which is irrelevant to Struct validation. B's line-number claims carry some fabrication risk, but the described architecture is accurate for Kafka Connect.

### 94. Kafka Connect pattern for SinkRecord (`kafka-connect-sink-record`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A enumerates the full SinkRecord API surface (kafkaOffset, timestampType, original* accessors), pins specific line ranges in source and tests, explains the ConsumerRecord→SinkRecord→InternalSinkRecord conversion path, and surfaces ErrantRecordSinkConnector as a real usage example. B's kafka.apache.org/42/ URLs are fabricated (that URL structure does not exist for 4.2), ConnectorConfigTest is irrelevant to SinkRecord metadata, and it lacks accessor-level detail.

### 95. Kafka Connect pattern for SourceRecord (`kafka-connect-source-record`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A provides precise line-range citations across SourceRecord, ConnectRecord, SubmittedRecords, WorkerSourceTaskTest, ExactlyOnceWorkerSourceTaskTest, and SubmittedRecordsTest — all repo-pinned to @4.2. It also surfaces the non-obvious null/null edge case and missing defensive copy. B cites kafka.apache.org/42/ URLs whose existence is unverified and leans on SamplePredicate as a test anchor, which is a helper not a behavioral test, reducing its usefulness and raising hallucination risk.

### 96. Kafka Connect pattern for ConnectorClientConfigRequest (`kafka-connect-connector-client-config-request`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B adds the critical call-site anchor AbstractHerder.validateClientOverrides() with line ranges, identifies prefix-stripping behavior, and includes AbstractHerderTest and ConnectorClientPolicyIntegrationTest for full coverage tiers. A omits the call site entirely and uses kafka.apache.org fragment anchors (#part-0041, #part-0040) that appear fabricated. B honestly acknowledges no separate docs tree rather than inventing URLs.

### 97. Kafka Connect pattern for ConnectorClientConfigOverridePolicy (`kafka-connect-connector-client-config-override-policy`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B covers the full enforcement chain (AbstractHerder#L925, Worker#L991) that A omits entirely, names all four policy modes including deprecated Principal and the Allowlist policy A misses, anchors the config default correctly in WorkerConfig#L159, cites the more specifically named ConnectorClientPolicyIntegrationTest, and provides line numbers throughout. A's external doc fragment anchors are uncertain and its integration test reference (ConnectorValidationIntegrationTest) is not specific to client override policy.

### 98. Kafka Connect pattern for AbstractConnectorClientConfigOverridePolicy (`kafka-connect-abstract-connector-client-config-override-policy`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: A names concrete internals (isAllowed() template method, ConfigValue construction, AppInfoParser.getVersion(), validate() iteration), pinned source paths with line ranges, and a full test inventory including BaseConnectorClientConfigOverridePolicyTest and ConnectorClientPolicyIntegrationTest. B is honest about retrieval gaps but provides almost no implementation detail, misses the base test class, and relies on external web URLs rather than in-tree anchors. A's specific line numbers carry hallucination risk, but the class/method names are structurally consistent.

### 99. Kafka Connect pattern for NoneConnectorClientConfigOverridePolicy (`kafka-connect-none-connector-client-config-override-policy`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.92`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 3, "specificity": 2, "usefulness": 3}}`
- Rationale: B provides line-pinned source refs for every claim: the exact rejection message text, WorkerConfig doc string, API Javadoc contract, unit test assertions (SaslConfigs/ProducerConfig keys), and WorkerTest runtime enforcement. A names the right files but hedges all behavioral claims as unverified and offers no concrete method signatures, message text, or test assertions. A's external doc URLs are plausible but unverifiable; B correctly anchors to source strings that generate those docs.

### 100. Kafka Connect pattern for PrincipalConnectorClientConfigOverridePolicy (`kafka-connect-principal-connector-client-config-override-policy`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B provides line-anchored source citations across implementation, API contract, package-info, unit tests, herder-level tests, and integration tests, and correctly identifies the sasl.mechanism coverage gap. A's class-level file paths are correct but the specific doc-site URL fragment (#part-0041) is unverifiable and likely fabricated. B avoids external URL claims, correctly anchors docs in WorkerConfig Javadoc, and surfaces ConnectorClientPolicyIntegrationTest as an additional behavioral anchor A misses entirely.
