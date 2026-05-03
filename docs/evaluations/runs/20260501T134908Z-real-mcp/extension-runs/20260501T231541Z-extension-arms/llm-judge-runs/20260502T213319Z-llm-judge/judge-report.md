# Blinded LLM-as-Judge Comparison

Generated: `2026-05-02T21:40:38.777139+00:00`

## Method

- The judge saw answer labels `A` and `B`; labels were deterministically randomized per case.
- The judge did not see which answer came from K2 or the baseline until results were mapped back.
- Explicit system identity tokens in answer text were normalized before judging.
- The deterministic evidence-grounding scorecard remains the primary benchmark metric; this is a secondary qualitative preference check.
- The reference checklist came from the published benchmark case metadata, not from either answer.

## Aggregate Judge Results

- Cases judged: `100`
- Winner counts: `{"codex_grep_filesystem": 56, "codex_with_k2_real_mcp": 44}`
- Win rates excluding ties: `{"codex_grep_filesystem": 0.56, "codex_with_k2_real_mcp": 0.44}`
- Tie rate: `0.0`
- Mean confidence: `0.8001`

## Deterministic Scorecard Context

- `codex_without_k2`: combined `0.189375`, retrieval `0`, answer `0.37875`, safety `1`, passed `0/100`
- `codex_grep_filesystem`: combined `0.754083`, retrieval `0.637333`, answer `0.870833`, safety `1`, passed `2/100`
- `codex_with_k2_real_mcp`: combined `0.928875`, retrieval `0.954`, answer `0.90375`, safety `1`, passed `93/100`

## Dimension Averages

| Run | Correctness | Grounding | Specificity | Usefulness | Risk |
| --- | ---: | ---: | ---: | ---: | ---: |
| codex_grep_filesystem | `3.49` | `4.04` | `4.75` | `4.33` | `3.03` |
| codex_with_k2_real_mcp | `3.33` | `3.49` | `2.93` | `3.16` | `3.48` |

## Per-Question Judge Decisions

### 1. Flink REST pattern for DispatcherRestEndpoint (`flink-rest-dispatcher-rest-endpoint`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.74`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B is more useful for an engineer because it points to the concrete registration path in `DispatcherRestEndpoint.initializeHandlers(...)`, the parent `RestServerEndpoint` registration flow, and test fixtures close to the dispatcher surface. A is safer but too vague and leans on generic handler tests that are not clearly adjacent to `DispatcherRestEndpoint`.

### 2. Flink REST pattern for WebMonitorEndpoint (`flink-rest-web-monitor-endpoint`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.66`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B better answers the wiring question with the actual registration path (`RestServerEndpoint` -> `WebMonitorEndpoint.initializeHandlers()` -> concrete subclasses) and cites more concrete source anchors plus neighboring tests. A is safer but mostly stops at pointers and omits the handler-registration flow the question asks for.

### 3. Flink REST pattern for RestServerEndpoint (`flink-rest-rest-server-endpoint`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.86`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A is better anchored to Flink 2.2.0 source artifacts in `flink-runtime` and `flink-docs`, names the key implementation class plus adjacent concrete subclasses and tests, and avoids off-target docs. B includes some real anchors but leans on broad/nightly docs, adds an unrelated SQL Gateway REST doc, and is less precise about the source tree and neighboring tests.

### 4. Flink REST pattern for AbstractRestHandler (`flink-rest-abstract-rest-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.84`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B better captures the actual AbstractRestHandler contract for Flink REST: versioned headers own status, handlers return ResponseBody futures, and it anchors the pattern in concrete runtime classes and tests. A is plausible but vaguer, less contract-specific, and includes a weaker neighboring-test set. B’s main downside is using generator/source anchors instead of a rendered docs page.

### 5. Flink REST pattern for JobDetailsHandler (`flink-rest-job-details-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.8`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 4, "risk": 2, "specificity": 3, "usefulness": 3}}`
- Rationale: A is better anchored in concrete Flink source artifacts: versioned doc generators, `JobDetailsHandler`, the adjacent `JobVertexDetailsHandler`, and in-repo tests. B leans on the published docs and adds `JobExceptionsHandler` as the analogue, which is less directly aligned with a neighboring job REST handler and looks more inferential. A still has some test-selection uncertainty, but it is materially more source-grounded.

### 6. Flink REST pattern for JobConfigHandler (`flink-rest-job-config-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.77`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 4, "risk": 2, "specificity": 3, "usefulness": 3}}`
- Rationale: A better matches a Flink `JobConfigHandler` anchor set: concrete runtime classes, the REST message/header pair, versioning/doc-generator anchors, and a relevant handler test. B likely conflates this with the `/jobs/:jobid/jobmanager/config` path and a generic `ConfigurationInfoEntry[]` shape, which is weaker for JobConfigHandler specifically.

### 7. Flink REST pattern for JobExceptionsHandler (`flink-rest-job-exceptions-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.96`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 2, "grounding": 4, "risk": 2, "specificity": 4, "usefulness": 3}, "codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 4, "usefulness": 4}}`
- Rationale: A directly anchors the 2.2.0 REST docs page for `/jobs/:jobid/exceptions`, the concrete handler class, and the nearby handler test. B shifts to docs-generator internals, adds unsupported versioning claims, and cites likely invented or unverified test names, which raises hallucination risk and makes it less aligned to the question.

### 8. Flink REST pattern for JobAccumulatorsHandler (`flink-rest-job-accumulators-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.74`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 2, "grounding": 4, "risk": 2, "specificity": 5, "usefulness": 3}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A is better aligned to Flink 2.2.0: it anchors on the release docs, the actual `JobAccumulatorsHandler`, and nearby handler/subtask tests without asserting unsupported internals. B is more detailed but leans on dubious versioning/generator claims and overconfident response-shape/method assertions that are not well supported.

### 9. Flink REST pattern for JobPlanHandler (`flink-rest-job-plan-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 4, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A is safer and better grounded in the version-pinned REST docs plus the actual handler/header classes. B is more specific, but it overcommits to unsupported implementation details like `AccessExecutionGraph.getPlan()` and `JobPlanInfo.Plan`, and it misses the exact docs anchor the question asked for.

### 10. Flink REST pattern for JobVertexDetailsHandler (`flink-rest-job-vertex-details-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.74`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B is more useful for an engineer: it names the implementation class, the response-body test, and the closest sibling vertex-scoped handler tests. A is safer on the version-pinned docs anchor, but it leans on broader or less relevant neighboring tests and is less actionable. B’s main weakness is framing the docs via the generator pipeline instead of the exact release-2.2 REST docs page.

### 11. Flink REST pattern for JobVertexTaskManagersHandler (`flink-rest-job-vertex-taskmanagers-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.67`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 4, "risk": 2, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A better matches the question by anchoring on the version-pinned 2.2.0 REST docs page plus the handler and message classes. B is more specific, but it shifts the docs anchor to generator/version-enum internals and makes unsupported claims about V0/V1 doc generation, increasing hallucination risk for a Flink code-change context.

### 12. Flink REST pattern for JobCancellationHandler (`flink-rest-job-cancellation-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.84`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 3, "risk": 2, "specificity": 4, "usefulness": 3}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A better matches the question by anchoring on the versioned Flink 2.2 docs, the runtime handler, and direct neighboring tests, while staying cautious about unverified internals. B is more specific but shifts to generator internals and adds stronger behavioral claims about request/response handling and redirects without equally solid version-pinned doc grounding.

### 13. Flink REST pattern for SavepointHandlers (`flink-rest-savepoint-handlers`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.93`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 2, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B better matches the asked Flink 2.2.0 REST savepoint flow: it names the concrete handler, trigger/poll status classes, REST headers, and adjacent tests. A is safer but too generic, leaning on unrelated checkpoint/state docs and omitting the actual REST behavior anchors the question asked for.

### 14. Flink REST pattern for CheckpointHandlers (`flink-rest-checkpoint-handlers`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A is closer to the real Flink 2.2 REST surface: it names the checkpoint REST handler area, concrete message/header classes, and the relevant neighboring tests. B anchors on checkpoint state docs rather than the REST API page and stays too vague on implementation/testing. A still overreaches slightly on some behavior and doc-version details, but it is materially better grounded and more actionable.

### 15. Flink REST pattern for JobResourceRequirementsUpdateHandler (`flink-rest-job-resource-requirements-update-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.87`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 2, "risk": 3, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better anchored to the actual validation path: handler, request-body type, dispatcher-side semantic checks, and nearby tests. It also distinguishes body parsing from semantic validation and names version-pinned source artifacts. B is mostly generic, cites broad docs sections, and misses the relevant body/dispatcher/test anchors for request-body validation.

### 16. Flink REST pattern for JobSubmitHandler (`flink-rest-job-submit-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.86`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A is better anchored to the actual Flink 2.2 runtime surface: it names the handler, request/response bodies, endpoint class, and the submit-specific tests. B is directionally right about the release docs and handler, but its citations are generic and it drifts to broad neighboring tests instead of the submit path. A has slightly more internal-version framing than needed, but it is still more grounded and actionable.

### 17. Flink REST pattern for FileUploads (`flink-rest-file-uploads`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A is better anchored to the Flink REST implementation path and names the neighboring handler/IT tests most likely to explain uploaded-file tracking. B is cleaner on version-pinned docs, but it is too generic, omits the adjacent REST handler tests, and does not ground the tracking behavior as well as A.

### 18. Flink REST pattern for DashboardConfigHandler (`flink-rest-dashboard-config-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B is more engineer-useful: it names the handler, response contract, wiring site, and a direct `DashboardConfigurationTest`, with line-level anchors. A is safer on the rendered docs, but its neighboring tests are weaker and less directly relevant. B is slightly riskier because it adds doc-generator internals, but overall it is more concrete and actionable.

### 19. Flink REST pattern for ClusterOverviewHandler (`flink-rest-cluster-overview-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.74`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A stays closer to the asked anchor set: version-pinned docs, the handler implementation, and nearby tests, without extra speculative machinery. B is more specific but shifts to doc-generator internals, includes malformed/inconsistent repo URIs, and makes more unsupported claims about versioning and response construction, increasing hallucination risk.

### 20. Flink REST pattern for TaskManagersHandler (`flink-rest-taskmanagers-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A is better anchored to the actual Flink 2.2.0 implementation path, the collection response wrapper, and the closest serialization/handler tests. B has acceptable docs and implementation links, but its test anchors are less relevant to TaskManagers collection handling and it is more generic about the contract.

### 21. Flink REST pattern for TaskManagerDetailsHandler (`flink-rest-taskmanager-details-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.79`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 2, "grounding": 4, "risk": 2, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 5, "specificity": 4, "usefulness": 4}}`
- Rationale: A stays aligned to the asked anchor set: version-pinned REST docs, `TaskManagerDetailsHandler`, header metadata, and the direct handler test, while explicitly avoiding unsupported behavior claims. B is more concrete but overreaches by asserting exact lookup/404 behavior and by using doc-generator classes instead of the version-pinned rendered docs, which is riskier for Flink 2.2.0.

### 22. Flink REST pattern for JobVertexBackPressureHandler (`flink-rest-job-vertex-back-pressure-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.93`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 4, "usefulness": 3}, "codex_with_k2_real_mcp": {"correctness": 5, "grounding": 4, "risk": 5, "specificity": 4, "usefulness": 4}}`
- Rationale: A stays aligned to the asked anchor set: version-pinned docs, `JobVertexBackPressureHandler`, and the dedicated handler test. B adds likely unsupported docs-generator internals and makes behavioral claims about OK/DEPRECATED responses that are not well grounded here. A is safer, more directly usable for engineering work, and has lower hallucination risk.

### 23. Flink REST pattern for JobVertexWatermarksHandler (`flink-rest-job-vertex-watermarks-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.96`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 3, "usefulness": 3}}`
- Rationale: A is better grounded in Flink’s actual runtime REST implementation and docs-generation path, with the handler, headers, endpoint wiring, version enum, and adjacent tests all named concretely. B relies on broad public docs links and generic neighboring tests, with weaker version-specific anchoring and less evidence for the exact watermark endpoint path or doc-generation chain.

### 24. Flink REST pattern for SubtaskCurrentAttemptDetailsHandler (`flink-rest-subtask-current-attempt-details-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.9`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 1, "grounding": 3, "risk": 1, "specificity": 3, "usefulness": 2}}`
- Rationale: B better matches the current-attempt handler’s non-attempt-numbered route and anchors the answer in concrete handler, headers, parameters, and neighboring tests. A appears to confuse this handler with the attempt-specific endpoint and therefore points at the wrong REST path, reducing its value for code changes.

### 25. Flink REST pattern for JobVertexFlameGraphHandler (`flink-rest-job-vertex-flame-graph-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.87`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 4, "risk": 2, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A better matches the question: it anchors on the version-pinned 2.2.0 REST docs page, the concrete `JobVertexFlameGraphHandler` implementation, and the dedicated handler test. B is more detailed, but it shifts the doc anchor to generator internals and adds unsupported claims about handler gating and endpoint behavior, which raises hallucination risk.

### 26. Flink checkpointing pattern for CheckpointCoordinator (`flink-checkpointing-checkpoint-coordinator`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.71`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: A is stronger for an engineer because it names the coordinator's trigger/restore paths, neighboring runtime classes, and multiple concrete tests in flink-runtime. B has better version-pinned docs URLs, but it is too cautious and too vague about the actual checkpoint-trigger trace and nearby tests, so it is less useful for code changes.

### 27. Flink checkpointing pattern for PendingCheckpoint (`flink-checkpointing-pending-checkpoint`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.77`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 3}}`
- Rationale: A is more engineer-useful: it names the runtime class, coordinator flow, and multiple neighboring tests, and it explicitly flags uncertainty about the docs source. B is safer at a high level but is thinner, relies on less-grounded doc anchors, and omits most of the surrounding test surface the question asked for.

### 28. Flink checkpointing pattern for CompletedCheckpoint (`flink-checkpointing-completed-checkpoint`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.77`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A better matches the question by naming the version-pinned 2.2.0 docs, the `CompletedCheckpoint` implementation, and the key neighboring tests. B is more granular, but it leans on Javadoc-only anchoring, adds many extra classes/tests beyond the asked anchors, and is more likely to overstate unsupported lifecycle details from line references.

### 29. Flink checkpointing pattern for CompletedCheckpointStore (`flink-checkpointing-completed-checkpoint-store`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.92`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 3, "usefulness": 3}}`
- Rationale: A is better anchored to Flink 2.2.0 source and API docs, and it names the core retention path plus adjacent tests. B includes relevant classes, but its doc citations look fabricated/unsupported and it adds an unrelated `FileSystemCheckpointStorage` anchor instead of the retention helper path. A is more version-specific, concrete, and safer for an engineer changing the Java code.

### 30. Flink checkpointing pattern for DefaultCompletedCheckpointStore (`flink-checkpointing-default-completed-checkpoint-store`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.67`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A is more actionable and better anchored in the actual runtime code and adjacent tests (`DefaultCompletedCheckpointStore`, `CheckpointSubsumeHelper`, direct unit tests, and ZooKeeper IT cases). B points at the public docs more directly, but it is weaker on implementation anchors and test selection, and it avoids the default-value question instead of resolving it. A’s main flaw is a likely wrong config key and some overconfident retention claims.

### 31. Flink checkpointing pattern for CheckpointStatsTracker (`flink-checkpointing-checkpoint-stats-tracker`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.84`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 2, "grounding": 4, "risk": 2, "specificity": 5, "usefulness": 3}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A better matches the ask: it anchors on version-pinned Flink docs, the runtime tracker class, and neighboring tests without inventing an alternate documentation basis. B is more specific in code terms, but its claim that REST message classes are the safest version-pinned docs is off-target and weakly supported for this question.

### 32. Flink checkpointing pattern for CheckpointStatsSnapshot (`flink-checkpointing-checkpoint-stats-snapshot`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.77`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 4, "usefulness": 2}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: B better matches the question by naming version-pinned checkpointing docs, the `CheckpointStatsSnapshot` implementation, and nearby tests directly tied to snapshot behavior. A is more repo-local but drifts into REST metadata classes and unrelated tests, which weakens the anchor set and increases the chance of misleading an engineer. B is still imperfect, but it is more on-target and safer overall.

### 33. Flink checkpointing pattern for CheckpointMetrics (`flink-checkpointing-checkpoint-metrics`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.89`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 2, "grounding": 2, "risk": 1, "specificity": 3, "usefulness": 2}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A stays closer to the Flink 2.2 API surface, names the right runtime class and plausible neighboring tests, and is appropriately uncertain. B is hurt by a likely fabricated builder derivation for `unalignedCheckpoint`, a weaker docs anchor, and overconfident claims about reporting semantics. Both list the nine metric fields, but A is less misleading for an engineer.

### 34. Flink checkpointing pattern for CheckpointProperties (`flink-checkpointing-checkpoint-properties`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better grounded in concrete Flink runtime artifacts, names the key implementation class, neighboring tests, and savepoint-specific paths. It is also more actionable for a Java engineer. B is too generic, leans on broad docs references, and adds less relevant test guidance without enough implementation detail.

### 35. Flink checkpointing pattern for CheckpointRetentionPolicy (`flink-checkpointing-checkpoint-retention-policy`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A is the better engineer-facing answer: it gives concrete retention choices, the likely enum-to-config mapping, and anchors in flink-runtime classes plus neighboring tests. B is safer but too vague, omits the actual policy semantics, and leans on generic docs/test names without enough implementation detail. A still has some verification risk on exact enum wording, but it is materially more actionable.

### 36. Flink checkpointing pattern for CheckpointIDCounter (`flink-checkpointing-checkpoint-id-counter`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A is more version-pinned and engineer-useful: it names the runtime interface, concrete counter implementations, coordinator call sites, and several adjacent tests. B is less grounded, leans on web doc URLs instead of repo artifacts, and appears to miss direct counter test coverage while adding uncertainty around the available test surface.

### 37. Flink checkpointing pattern for StandaloneCheckpointIDCounter (`flink-checkpointing-standalone-checkpoint-id-counter`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 5, "specificity": 3, "usefulness": 3}}`
- Rationale: B is more actionable and version-specific: it names the implementation, shared test base, and related checkpointing tests that actually constrain `StandaloneCheckpointIDCounter`. A is safer, but it stays too generic and avoids the allocation behavior the question asks to inspect. B has some overreach, but its anchors are closer to the code path and test surface.

### 38. Flink checkpointing pattern for CheckpointFailureManager (`flink-checkpointing-checkpoint-failure-manager`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.79`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 4, "risk": 2, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A is more conservative and better anchored to version-pinned docs, the `CheckpointFailureManager` class, and nearby tests, with clear uncertainty. B is more detailed, but it asserts several internal methods and behavior branches that may be partially fabricated or unsupported, which raises hallucination risk for a Flink 2.2.0 engineering answer.

### 39. Flink checkpointing pattern for CheckpointPlanCalculator (`flink-checkpointing-checkpoint-plan-calculator`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.83`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 2, "grounding": 4, "risk": 2, "specificity": 5, "usefulness": 3}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A is better anchored to the requested 2.2.0 docs pages, the `CheckpointPlanCalculator`/`DefaultCheckpointPlanCalculator` runtime classes, and the nearest test class. B is more specific but overclaims internal behavior and uses a weaker docs anchor (module-level evidence instead of version-pinned checkpointing docs), increasing hallucination risk.

### 40. Flink checkpointing pattern for DefaultCheckpointPlanCalculator (`flink-checkpointing-default-checkpoint-plan-calculator`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.61`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 4, "usefulness": 4}}`
- Rationale: B better matches the question by including version-pinned Flink 2.2.0 docs plus the concrete implementation and direct test anchor. A is more concrete in code/test references, but it misses the docs requirement and overstates the absence of documentation support. B is weaker on grounding and overclaims some neighbor tests, but it is closer to the requested answer shape.

### 41. Flink checkpointing pattern for CheckpointRequestDecider (`flink-checkpointing-checkpoint-request-decider`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.74`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 3, "risk": 2, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A is safer and better aligned with the prompt: it uses 2.2.0 release docs, the exact `CheckpointRequestDecider` implementation, and the neighboring test class without overclaiming branch logic. B is more specific, but it treats source comments/configs as docs and makes many detailed scheduling assertions that are not sufficiently grounded, increasing hallucination risk.

### 42. Flink checkpointing pattern for CheckpointResourcesCleanupRunner (`flink-checkpointing-checkpoint-resources-cleanup-runner`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 4, "usefulness": 3}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A better matches the request by anchoring on version-pinned Flink 2.2 docs plus the exact runtime class and direct test. B invents detailed cleanup behavior and replaces requested docs pages with source Javadocs, which is less version-specific and more hallucination-prone.

### 43. Flink checkpointing pattern for CheckpointStorageLoader (`flink-checkpointing-checkpoint-storage-loader`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 4, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A stays closer to the asked anchor set: version-pinned docs, the runtime loader class, and direct neighboring tests, while explicitly flagging uncertainty. B is more detailed, but it overcommits to exact loading precedence/default behavior and leans on a docs README instead of version-pinned rendered docs, which raises hallucination risk.

### 44. Flink checkpointing pattern for CheckpointStorageCoordinatorView (`flink-checkpointing-checkpoint-storage-coordinator-view`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.66`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A is better grounded in concrete flink-runtime source and nearby tests, which is what an engineer needs to inspect or change. B is more version-specific on docs, but it stays generic, leans on inference, and does not anchor the contract in enough implementation or test detail.

### 45. Flink checkpointing pattern for StateBackend (`flink-checkpointing-state-backend`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.93`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A better matches Flink 2.2.0 by anchoring StateBackend in flink-runtime and naming neighboring tests that plausibly exercise checkpointing behavior. B is weaker: it cites less relevant or likely off-target classes, gives incomplete test coverage guidance, and is less reliable on the exact 2.2.0 API surface.

### 46. Flink checkpointing pattern for OperatorStateBackend (`flink-checkpointing-operator-state-backend`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.86`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 4, "risk": 2, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A better matches the question by anchoring on version-pinned Flink 2.2.0 docs, the runtime implementation, and nearby tests. B is more code-specific but drops the required docs anchor and leans on extra classes/tests that may be accurate yet are less directly tied to the asked checkpointing responsibility framing. B also has higher hallucination risk from broad, overconfident claims.

### 47. Flink checkpointing pattern for KeyedStateBackend (`flink-checkpointing-keyed-state-backend`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better anchored in Flink 2.2.0 source artifacts: it names the right contract (`CheckpointableKeyedStateBackend`), implementation (`AbstractKeyedStateBackend`, `HeapKeyedStateBackend`), and nearby `flink-runtime` tests. B relies on generic docs links and mostly unrelated tests, with weaker keyed-state checkpointing grounding and more retrieval-style uncertainty.

### 48. Flink checkpointing pattern for SavepointRestoreSettings (`flink-checkpointing-savepoint-restore-settings`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.93`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 1, "grounding": 2, "risk": 1, "specificity": 3, "usefulness": 3}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A is closer to the likely Flink 2.2.0 API surface and anchors the answer in the right implementation class, runtime path, and neighboring tests with explicit uncertainty. B overstates unsupported internals, likely fabricates an overload/config serialization flow, and mis-anchors the answer in non-doc runtime classes instead of version-pinned docs.

### 49. Flink checkpointing pattern for SavepointFormatType (`flink-checkpointing-savepoint-format-type`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.79`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 4, "usefulness": 3}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A is more conservative and better aligned with the likely 2.2.0 API surface: it anchors `SavepointFormatType` in `flink-core`, ties behavior to backend support and checkpoint properties, and includes version-pinned docs plus adjacent tests. B introduces a likely unsupported `DEFAULT` alias claim, adds speculative performance guidance, and relies on several anchors that look less directly relevant or potentially fabricated.

### 50. Flink checkpointing pattern for CheckpointCoordinatorConfiguration (`flink-checkpointing-checkpoint-coordinator-configuration`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.86`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 3}}`
- Rationale: A is better anchored to Flink 2.2.0 source artifacts, includes the runtime class, config surface, and several relevant neighboring tests. B is more vague, uses weaker doc anchors, and includes an unrelated test that does not help locate checkpoint-coordinator configuration behavior. A still has some overreach, but it is materially more useful and grounded.

### 51. Kafka Connect pattern for ConnectorPluginsResource (`kafka-rest-connector-plugins-resource`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.84`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B better traces the 4.2 REST validation path from `ConnectorPluginsResource.validateConfigs()` to `Herder.validateConnectorConfig()` and names concrete regression tests, which is more actionable for code changes. A has the pinned docs pages, but is broader and less explicit about the actual validation flow. B’s docs anchoring is weaker, but overall it is more specific and engineer-useful.

### 52. Kafka Connect pattern for AbstractHerder (`kafka-connect-abstract-herder`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.77`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A better matches the question by naming the Kafka 4.2-pinned docs plus the core `AbstractHerder` and `AbstractHerderTest` anchors. B is more detailed, but it misses the requested version-pinned docs and adds extra call-chain/test claims that are plausible but less clearly grounded for this prompt.

### 53. Kafka Connect pattern for DistributedHerder (`kafka-connect-distributed-herder`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.74`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: B is more actionable for a Java engineer: it names the concrete `DistributedHerder` update paths and neighboring tests that likely exercise config-update behavior. A is safer on version-pinned docs, but stays too generic and admits it cannot identify the exact update path. B’s main weakness is weaker doc anchoring and some risk from very specific line claims, but overall it is the stronger engineering answer.

### 54. Kafka Connect pattern for StandaloneHerder (`kafka-connect-standalone-herder`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.77`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A better matches the question by anchoring on version-pinned Kafka docs plus `StandaloneHerder` and nearby standalone tests. B is more granular, but it omits the requested docs anchor, leans on source Javadocs instead, and makes very specific line/method claims that are harder to trust without direct support.

### 55. Kafka Connect pattern for Herder (`kafka-connect-herder`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.67`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 4, "risk": 2, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B is closer to the requested Herder-centered answer: it names the interface and gives concrete runtime and test anchors. But it likely overstates the exact API surface and substitutes source Javadocs/annotations for version-pinned docs. A has better version-pinned doc links, yet it misses the interface question and its test anchor is weak and partly irrelevant.

### 56. Kafka Connect pattern for Worker (`kafka-connect-worker`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.95`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A anchors the answer on `Worker` and nearby `WorkerTest`/integration tests, which matches the question and gives concrete lifecycle methods and inspection points. B shifts the implementation anchor to `AbstractHerder`, which is adjacent but not the requested class, and its test guidance is too generic. A is still imperfect on exact versioned docs, but it is materially more grounded and actionable.

### 57. Kafka Connect pattern for WorkerConnector (`kafka-connect-worker-connector`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A is better anchored to the actual Kafka Connect 4.2 code path: `WorkerConnector`, `Worker`, `Connector`, and neighboring unit/integration tests directly relevant to startup and failure handling. B relies on broad public docs and a less convincing neighboring integration test, and it is less precise about the concrete methods to inspect.

### 58. Kafka Connect pattern for WorkerTask (`kafka-connect-worker-task`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A is better anchored for an engineer changing Java code: it ties `WorkerTask` to concrete Connect API javadocs/source, the runtime implementation, and several adjacent tests with exact repo paths. B has valid 4.2 docs URLs, but its neighboring test anchors are thinner and less directly aligned to `WorkerTask` lifecycle behavior, with less concrete source-level grounding.

### 59. Kafka Connect pattern for WorkerSinkTask (`kafka-connect-worker-sink-task`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.89`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A stays close to the Connect API and runtime test surface, names the right implementation and several directly relevant WorkerSinkTask tests, and flags uncertainty about docs. B has plausible versioned docs, but its test anchors are mostly off-topic and it introduces unverified WorkerSinkTask method names that look overconfident. For an engineer changing sink commit behavior, A is materially more actionable and lower risk.

### 60. Kafka Connect pattern for WorkerSourceTask (`kafka-connect-worker-source-task`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.79`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A is better anchored to the actual Connect runtime shape: it names AbstractWorkerSourceTask, WorkerSourceTask, SourceTask/TransactionContext, and the direct unit tests around commit skipping and poll failures. B cites useful docs but misses the shared poll implementation class and drifts into less neighboring integration/error-handling tests. A is slightly noisy with EOS material, but overall it is more version-specific and engineer-actionable.

### 61. Kafka Connect pattern for ConnectorConfig (`kafka-connect-connector-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: B is safer and more version-anchored: it names the 4.2 docs, the `ConnectorConfig` implementation, and the nearest test files without inventing deep internal details. A is more specific, but it likely overclaims internal behavior and cites many suspicious line ranges and unrelated build/docs anchors, increasing hallucination risk.

### 62. Kafka Connect pattern for SinkConnectorConfig (`kafka-connect-sink-connector-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 4, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A is more cautious and better aligned to the asked anchors: version-pinned docs, the `SinkConnectorConfig` implementation, and a relevant neighboring integration test. B is more specific, but it likely overstates the API surface with a possibly fabricated `validate(...)` anchor and drifts into unrelated runtime/tests, increasing hallucination risk.

### 63. Kafka Connect pattern for SourceConnectorConfig (`kafka-connect-source-connector-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.71`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 4, "risk": 2, "specificity": 4, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: B is more version-pinned and conservative: it anchors on Kafka 4.2 docs, `SourceConnectorConfig`, and nearby tests without asserting extra implementation details that may be wrong. A is more specific, but it likely overreaches with method names and extra test/file claims not clearly supported, which raises hallucination risk.

### 64. Kafka Connect pattern for WorkerConfig (`kafka-connect-worker-config`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.79`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 2, "usefulness": 3}}`
- Rationale: A is better anchored to the Connect runtime source tree and names the most relevant neighboring tests for worker parsing across standalone and distributed modes. B has plausible version-pinned docs URLs, but it is thinner on concrete implementation/test anchors and includes an unrelated integration test, making it less useful for an engineer changing `WorkerConfig`.

### 65. Kafka Connect pattern for DistributedConfig (`kafka-connect-distributed-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.67`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 2, "grounding": 2, "risk": 1, "specificity": 4, "usefulness": 3}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 3, "usefulness": 4}}`
- Rationale: B better matches the question’s need for version-pinned docs plus implementation and neighboring tests. A is more specific but overreaches with source-only substitutes for docs and many line-precise anchors that are not clearly justified. B is less detailed, but its versioned Kafka docs anchors are more appropriate for Kafka Connect 4.2.0 and lower-risk for an engineer.

### 66. Kafka Connect pattern for StandaloneConfig (`kafka-connect-standalone-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.67`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B better matches the prompt by pinning Kafka 4.2 docs and naming the direct StandaloneConfig/StandaloneConfigTest anchors, while staying cautious about unverified assertions. A is richer in source refs, but it misses the requested version-pinned docs and broadens into less clearly neighboring tests.

### 67. Kafka Connect pattern for ConfigDef (`kafka-connect-config-def`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.67`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 2, "specificity": 4, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B is more actionable for an engineer: it names the canonical `ConfigDef` class, distinguishes `parse()` from `validate()`, and points to Connect integration points and tests. A is safer but too vague and explicitly declines to ground the key source class. B’s main weakness is higher hallucination risk from very specific file/line/test claims that may not all be verified.

### 68. Kafka Connect pattern for ConfigValue (`kafka-connect-config-value`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.89`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 4, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 4, "usefulness": 5}}`
- Rationale: A answers the asked anchor question directly with version-pinned Kafka Connect docs plus the correct implementation class, and its description of validation state on ConfigValue is accurate. B is partially correct but weakly grounded: it treats source files as docs, adds extra REST-layer claims not asked for, and misses the requested version-pinned documentation anchor.

### 69. Kafka Connect pattern for ConfigTransformer (`kafka-connect-config-transformer`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.73`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 4, "usefulness": 3}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: B better matches the question by using Kafka 4.2-pinned docs and the primary implementation class `org.apache.kafka.common.config.ConfigTransformer`. A is more detailed, but it anchors docs on source Javadocs rather than version-pinned docs pages and adds extra, less necessary test and runtime claims. B is slightly broader, but safer and more directly useful for an engineer inspecting the transformation path.

### 70. Kafka Connect pattern for ConfigProvider (`kafka-connect-config-provider`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B is better grounded in Kafka 4.2 source artifacts and Connect runtime tests, and it identifies the concrete implementation anchor `FileConfigProvider` plus the contract path through `AbstractConfig` and `WorkerConfigTransformer`. A is directionally correct but more generic, less version-specific, and less useful for an engineer validating or changing Connect secret resolution.

### 71. Kafka Connect pattern for Plugins (`kafka-connect-plugins`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B is more grounded in the actual Kafka Connect 4.2 code path: `Plugins`, `ReflectionScanner`, `ServiceLoaderScanner`, `Worker`, and the neighboring test classes are concrete anchors for discovery and connector loading. A has versioned docs URLs, but it is less precise about the runtime trace and likely overstates the most relevant tests. B is better for an engineer changing Java code, though it under-delivers on published docs URLs.

### 72. Kafka Connect pattern for PluginDesc (`kafka-connect-plugin-desc`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A better matches the question by anchoring on Kafka 4.2 Connect docs, the `PluginDesc` implementation, and the direct `PluginDescTest`. B is more specific, but it drifts into secondary surfaces (`PluginInfo`, broader loader tests, inline config docs) and makes stronger claims about source-of-truth behavior that are less clearly tied to the asked anchor set.

### 73. Kafka Connect pattern for PluginType (`kafka-connect-plugin-type`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.79`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 3, "specificity": 2, "usefulness": 2}}`
- Rationale: A gives the right kind of anchors: concrete Connect runtime classes, nearby tests, and explicit repo paths. It is more actionable for an engineer changing Java code. B is cautious but too generic, leans on broad docs URLs, and only names one test, so it under-anchors the answer. A does carry some hallucination risk in the exact enum count and line refs, but it is still stronger overall.

### 74. Kafka Connect pattern for DelegatingClassLoader (`kafka-connect-delegating-class-loader`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.71`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B is more engineer-useful and better anchored to concrete source artifacts: it names the implementation path, related classes, and neighboring tests with version-specific references. A is safer on uncertainty, but its docs anchors are broader website pages and it is less specific about the exact code paths and test coverage that should be inspected for DelegatingClassLoader behavior.

### 75. Kafka Connect pattern for PluginClassLoader (`kafka-connect-plugin-class-loader`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 2, "usefulness": 3}}`
- Rationale: B is more actionable for a Java engineer because it anchors the actual implementation path and adjacent tests with concrete source locations. It is weaker on version-pinned docs, but overall it is better grounded in code and test artifacts than A. A has the right doc intent, but it is less specific and more likely to miss the key neighboring isolation tests.

### 76. Kafka Connect pattern for PluginScanResult (`kafka-connect-plugin-scan-result`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.86`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 2, "usefulness": 3}}`
- Rationale: A is better anchored to the Kafka Connect code path the question asks about: `PluginScanResult`, the scanner classes, and neighboring tests. B leans on broad top-level docs and the surrounding `Plugins` entry point, which is less directly tied to `PluginScanResult` and more likely to mislead an engineer changing the result object itself.

### 77. Kafka Connect pattern for PluginUtils (`kafka-connect-plugin-utils`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.67`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 4, "risk": 2, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A is safer and better aligned with the prompt’s request for version-pinned docs plus the actual `PluginUtils` class and nearby test. B is more specific, but it leans on source-comments as “docs” and makes several detailed behavior claims that are more likely to overreach without direct evidence.

### 78. Kafka Connect pattern for ConnectRestServer (`kafka-rest-connect-rest-server`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 3, "risk": 2, "specificity": 4, "usefulness": 3}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 5}}`
- Rationale: A matches the prompt’s requested anchor set: version-pinned docs, the `ConnectRestServer` implementation, and adjacent tests. B has useful wiring detail, but it omits standalone version-pinned docs and introduces more unsupported call-chain/binding claims, which raises hallucination risk for a code-change task.

### 79. Kafka Connect pattern for RestServerConfig (`kafka-rest-rest-server-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 4, "risk": 2, "specificity": 5, "usefulness": 3}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A better matches the ask: it anchors on version-pinned Kafka 4.2 docs, the exact `RestServerConfig` implementation, and nearby REST tests. B is more detailed, but it substitutes source Javadocs for version-pinned docs and broadens into extra tests and behaviors that are not the immediate anchor set.

### 80. Kafka Connect pattern for ConnectorsResource (`kafka-rest-connectors-resource`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 4, "risk": 2, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: B is better anchored to a version-pinned Kafka 4.2 docs page and stays conservative about what the retrieved evidence supports. A is more specific, but it leans on likely fabricated line numbers and weaker docs anchoring, plus extra tests that are not clearly adjacent to CRUD behavior.

### 81. Kafka Connect pattern for ConnectorStateInfo (`kafka-rest-connector-state-info`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.67`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 5, "risk": 2, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A answers the asked anchor question more directly with a version-pinned docs URL and the exact implementation class. B is more detailed and better grounded in code, but it shifts to a build-generated OpenAPI story and adds several unsupported wire-shape claims, increasing hallucination risk.

### 82. Kafka Connect pattern for ConnectorInfo (`kafka-rest-connector-info`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.66`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: A better matches the question by anchoring on version-pinned Kafka 4.2 docs plus the `ConnectorInfo` implementation class. B is more concrete on code and tests, but its claim that source annotations are the best docs anchor does not satisfy the request for version-pinned docs and may overstate the absence of checked-in docs.

### 83. Kafka Connect pattern for CreateConnectorRequest (`kafka-rest-create-connector-request`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.86`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 3, "usefulness": 2}}`
- Rationale: A is closer to the real Kafka Connect REST flow: it anchors the DTO, the REST resource that handles create requests, and nearby tests that actually exercise request handling. B is weaker because most of its neighboring tests are unrelated to connector creation validation, and it omits the REST resource path that engineers would inspect first. A still has some indirect anchors, but it is materially more grounded and actionable.

### 84. Kafka Connect pattern for ConnectorType (`kafka-rest-connector-type`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 5, "usefulness": 3}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A stays aligned with the prompt: version-pinned Connect docs, the REST `ConnectorType` implementation, and nearby tests, while explicitly limiting uncertainty. B is more concrete but overreaches with unsupported classification and lookup details, and it misses the requested docs anchor in favor of source-level substitutes.

### 85. Kafka Connect pattern for Connector (`kafka-connect-connector`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B better matches the request for version-pinned Kafka 4.2 docs and anchors the contract in `ConnectorConfig.java`, which is the key registration/validation site. A has stronger neighboring test suggestions, but it misses the requested public docs anchor and relies on source Javadocs as a substitute. B is less complete on tests, but overall closer to the asked source set.

### 86. Kafka Connect pattern for SourceConnector (`kafka-connect-source-connector`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.66`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 5, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: B better matches the ask by naming version-pinned Kafka 4.2.0 docs plus the `SourceConnector` class and a nearby test anchor. A is stronger on code/test specificity, but it misses the requested docs anchor and leans on version-sensitive SourceConnector hooks without proving the 4.2.0 surface.

### 87. Kafka Connect pattern for SinkConnector (`kafka-connect-sink-connector`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 3, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better anchored to Kafka 4.2 source artifacts: SinkConnector Javadocs, runtime classes, and multiple neighboring tests that an engineer can inspect directly. B is thinner, less version-specific in practice, and its only test anchor is source-oriented and not SinkConnector-neighboring, so it is less useful and more likely to mislead.

### 88. Kafka Connect pattern for Transformation (`kafka-connect-transformation`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.67`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B is more actionable for a Java engineer because it names the runtime classes that actually govern SMT execution and the neighboring tests that exercise them. A is safer on version-pinned docs but stays too high level and points at weaker test anchors. B’s main weakness is that it treats doc-generation sources as the doc anchor rather than the rendered 4.2 docs.

### 89. Kafka Connect pattern for HeaderConverter (`kafka-connect-header-converter`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.73`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 2, "specificity": 3, "usefulness": 3}}`
- Rationale: A better matches the asked anchor set: it names the concrete implementation class `SimpleHeaderConverter`, the Connect config docs, and several adjacent runtime tests. B leans on the interface and unrelated MirrorMaker docs, and its test anchor is a fixture rather than a neighboring regression test. A still has some likely overreach around versioned plugin wiring and test coverage, but it is closer to an engineer-usable map.

### 90. Kafka Connect pattern for Converter (`kafka-connect-converter`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 4, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B is closer to the actual Kafka Connect 4.2 API surface: it names the `Converter` contract, concrete converters, worker/connector config anchors, and direct tests for key/value handling. A is safer but mostly stops at config wiring plus one indirect integration test, so it misses the behavior-specific implementation path the question asks for.

### 91. Kafka Connect pattern for Schema (`kafka-connect-schemas`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.83`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: B is better anchored in the actual Connect API surface: `Schema.java`, `SchemaBuilder.java`, and `ConnectSchema.java`, plus nearer behavioral tests like converter tests and `PluginUtilsTest`. A has the version-pinned docs URLs, but its test choices are looser and it omits `Schema.java`, which is the primary contract surface for this question.

### 92. Kafka Connect pattern for SchemaBuilder (`kafka-connect-schema-builder`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.87`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better anchored in Kafka Connect source artifacts: it names the core implementation class, related API docs, and concrete neighboring tests, while explicitly noting uncertainty about a dedicated SchemaBuilder unit test. B is too generic, uses weaker doc anchors, and points to an unrelated integration test instead of nearby schema-construction coverage.

### 93. Kafka Connect pattern for Struct (`kafka-connect-struct`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.74`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: B is better because it traces the actual validation path (`Struct` -> `ConnectSchema.validateValue`) and names more relevant neighboring tests. A is safer but too vague, and its test anchors are weakly related to Struct validation. B still has some risk because the exact line ranges and test relevance are not independently verified.

### 94. Kafka Connect pattern for SinkRecord (`kafka-connect-sink-record`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better anchored to the actual 4.2 Connect API surface: SinkRecord Javadocs, implementation, runtime wrapper, and relevant sink-runtime tests. B leans on generic Connect docs and unrelated tests, and it incorrectly implies there is no dedicated SinkRecord unit test even though one exists in connect/api.

### 95. Kafka Connect pattern for SourceRecord (`kafka-connect-source-record`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.93`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A is better anchored to Kafka Connect 4.2 source code and the runtime tests that actually exercise sourcePartition/sourceOffset handling. B relies more on generic public docs and cites weaker neighboring artifacts, including a helper that is not a test. A is more actionable for an engineer inspecting SourceRecord construction and metadata flow.

### 96. Kafka Connect pattern for ConnectorClientConfigRequest (`kafka-connect-connector-client-config-request`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.73`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A better anchors the answer in version-pinned Kafka 4.2 docs plus the request/policy classes and nearby unit tests. B is more detailed on call paths and integration tests, but it weakens the required doc anchoring by substituting inline Javadocs/WorkerConfig and makes a misleading source-tree claim. A is safer and more directly aligned with the question.

### 97. Kafka Connect pattern for ConnectorClientConfigOverridePolicy (`kafka-connect-connector-client-config-override-policy`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.86`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 2, "grounding": 4, "risk": 1, "specificity": 5, "usefulness": 3}, "codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A is safer and better anchored: it cites versioned Connect docs, the interface, the abstract validation path, and neighboring tests without inventing APIs. B is more specific, but it likely hallucinates `AllowlistConnectorClientConfigOverridePolicy` and overstates runtime anchors, which makes it less trustworthy for a 4.2.0 code-change answer.

### 98. Kafka Connect pattern for AbstractConnectorClientConfigOverridePolicy (`kafka-connect-abstract-connector-client-config-override-policy`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.74`
- Blinded label mapping: `{"A": "codex_grep_filesystem", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better anchored to in-repo Kafka 4.2 artifacts: the API contract, WorkerConfig docs, the abstract policy implementation, and concrete neighboring policy tests. B is safer but too thin, leans on web docs over source artifacts, and misses the most relevant test classes for the shared policy behavior.

### 99. Kafka Connect pattern for NoneConnectorClientConfigOverridePolicy (`kafka-connect-none-connector-client-config-override-policy`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.84`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B better anchors the answer in versioned Connect docs, the concrete policy implementation, and adjacent tests that exercise denial behavior. It is more actionable for an engineer changing Java code. A is safer but too vague and less complete. B’s main weakness is higher hallucination risk from very specific assertions and line references, but it is still the stronger answer overall.

### 100. Kafka Connect pattern for PrincipalConnectorClientConfigOverridePolicy (`kafka-connect-principal-connector-client-config-override-policy`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.66`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 5, "usefulness": 4}, "codex_with_k2_real_mcp": {"correctness": 5, "grounding": 4, "risk": 5, "specificity": 3, "usefulness": 4}}`
- Rationale: A is more aligned with the question: it anchors on version-pinned Kafka 4.2 docs, the policy implementation, and the key unit/base tests, while staying cautious about uncertainty. B is more specific, but it leans on source-doc strings and extra tests with exact line claims that look less reliably grounded and more likely to overreach.
