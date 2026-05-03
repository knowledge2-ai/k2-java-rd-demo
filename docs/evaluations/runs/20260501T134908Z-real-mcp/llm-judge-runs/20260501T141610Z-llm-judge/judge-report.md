# Blinded LLM-as-Judge Comparison

Generated: `2026-05-01T14:26:12.612753+00:00`

## Method

- The judge saw answer labels `A` and `B`; labels were deterministically randomized per case.
- The judge did not see which answer came from K2 or the baseline until results were mapped back.
- Explicit system identity tokens in answer text were normalized before judging.
- The deterministic evidence-grounding scorecard remains the primary benchmark metric; this is a secondary qualitative preference check.
- The reference checklist came from the published benchmark case metadata, not from either answer.

## Aggregate Judge Results

- Cases judged: `100`
- Winner counts: `{"codex_with_k2_real_mcp": 71, "codex_without_k2": 29}`
- Win rates excluding ties: `{"codex_with_k2_real_mcp": 0.71, "codex_without_k2": 0.29}`
- Tie rate: `0.0`
- Mean confidence: `0.8573`

## Deterministic Scorecard Context

- `codex_without_k2`: combined `0.189375`, retrieval `0`, answer `0.37875`, safety `1`, passed `0/100`
- `codex_with_k2_real_mcp`: combined `0.928875`, retrieval `0.954`, answer `0.90375`, safety `1`, passed `93/100`

## Dimension Averages

| Run | Correctness | Grounding | Specificity | Usefulness | Risk |
| --- | ---: | ---: | ---: | ---: | ---: |
| codex_with_k2_real_mcp | `3.7` | `4.24` | `4.16` | `3.93` | `3.57` |
| codex_without_k2 | `2.9` | `2.18` | `2.61` | `2.83` | `2.79` |

## Per-Question Judge Decisions

### 1. Flink REST pattern for DispatcherRestEndpoint (`flink-rest-dispatcher-rest-endpoint`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.94`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 1, "risk": 1, "specificity": 2, "usefulness": 2}}`
- Rationale: A names the right Flink 2.2.0 implementation class, pins to release docs, and points to the handler-initialization path plus relevant neighboring tests. B is weaker and likely wrong on package paths and test names, and it hedges instead of anchoring to concrete source artifacts. A is better for an engineer changing Java code.

### 2. Flink REST pattern for WebMonitorEndpoint (`flink-rest-web-monitor-endpoint`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.92`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 1, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A is more version-specific and anchored to concrete Flink 2.2.0 artifacts: the REST docs, `WebMonitorEndpoint`, and nearby tests. B stays generic, hedges heavily, and names likely-but-unverified paths and patterns without concrete evidence. A still has some risk around exact handler lists, but it is materially more grounded for an engineer changing Flink code.

### 3. Flink REST pattern for RestServerEndpoint (`flink-rest-rest-server-endpoint`)

- Winner: `codex_without_k2`
- Confidence: `0.84`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 2, "grounding": 4, "risk": 2, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A stays aligned with the Flink 2.2.0 `RestServerEndpoint` lifecycle and uses a plausible version-pinned REST docs anchor plus the core runtime test. B is more specific, but its `docs/ops/rest_api` and SQL Gateway anchors look off-target for this class, and it overclaims source evidence from a truncated excerpt.

### 4. Flink REST pattern for AbstractRestHandler (`flink-rest-abstract-rest-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 1, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: A is materially better anchored: it names version-pinned Flink 2.2.0 docs, the `AbstractRestHandler` implementation file, a nearby concrete handler, and adjacent tests. B is cautious but too generic, lacks verified source anchors, and does not identify concrete neighboring tests or module-specific implementation points. A still carries some uncertainty in the exact neighboring test names, but it is far more actionable and grounded.

### 5. Flink REST pattern for JobDetailsHandler (`flink-rest-job-details-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.61`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B is more actionable and version-anchored: it names the 2.2.0 docs, `JobDetailsHandler`, `JobDetailsHeaders`, `WebMonitorEndpoint`, and nearby tests. A is safer but too vague on the version-pinned docs and less grounded. B does overstate one docs connection, but overall it is the better engineer-facing anchor set.

### 6. Flink REST pattern for JobConfigHandler (`flink-rest-job-config-handler`)

- Winner: `codex_without_k2`
- Confidence: `0.95`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 1, "grounding": 4, "risk": 1, "specificity": 4, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A is closer to the likely Flink 2.2.0 surface: it anchors the `JobConfigHandler` class and the matching handler test, and it avoids overclaiming about route/POJO details. B is more detailed but appears to conflate the endpoint with a `jobmanager/config` route and asserts a return type and doc anchors too confidently, which is a high-risk mismatch for this API surface.

### 7. Flink REST pattern for JobExceptionsHandler (`flink-rest-job-exceptions-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.94`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 1, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A is materially better: it pins the Flink 2.2 docs, names the implementation class, and gives a direct test anchor plus same-package comparators. B is vague, explicitly uncertain about the docs slug, and does not provide a versioned docs anchor or concrete neighboring tests, which makes it less reliable for an engineer changing Java code.

### 8. Flink REST pattern for JobAccumulatorsHandler (`flink-rest-job-accumulators-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.96`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 1, "risk": 1, "specificity": 2, "usefulness": 2}}`
- Rationale: A is anchored to the Flink 2.2 REST docs, the actual `JobAccumulatorsHandler` implementation, and nearby handler tests, while explicitly noting uncertainty about a dedicated handler test. B is much vaguer, omits a version-pinned doc anchor, and likely hallucinates test names plus the response DTO. A is therefore more reliable for an engineer changing Java code.

### 9. Flink REST pattern for JobPlanHandler (`flink-rest-job-plan-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.93`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 1, "grounding": 2, "risk": 1, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better anchored to Flink 2.2.0 artifacts: version-pinned REST docs, the likely correct `flink-runtime` handler and headers classes, and neighboring REST tests. B has likely-wrong module paths (`flink-runtime-web`) and only generic behavior claims, so it is less reliable for an engineer editing the code.

### 10. Flink REST pattern for JobVertexDetailsHandler (`flink-rest-job-vertex-details-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.89`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 1, "specificity": 2, "usefulness": 2}}`
- Rationale: A is more version-aware and concretely anchored: it names the 2.2.0 docs, the handler class, the headers class, and adjacent tests, while explicitly flagging uncertainty. B is vaguer, omits the version-pinned doc anchors, and asserts a specific test file and companion types without grounding. For an engineer modifying Flink REST code, A is materially more actionable and less hallucinatory.

### 11. Flink REST pattern for JobVertexTaskManagersHandler (`flink-rest-job-vertex-taskmanagers-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.96`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 1, "risk": 1, "specificity": 1, "usefulness": 2}}`
- Rationale: A is tightly version-pinned to Flink 2.2.0, names the concrete handler, header, and response classes, and points to adjacent tests with exact paths. B stays generic, omits exact docs and implementation anchors, and speculates about tests and DTO reuse without evidence. For an engineer changing Java code, A is materially more actionable and lower risk.

### 12. Flink REST pattern for JobCancellationHandler (`flink-rest-job-cancellation-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.95`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A names the version-pinned REST docs, the exact 2.2.0 runtime handler, and concrete neighboring tests, with uncertainty noted. B stays generic, omits exact versioned doc/test anchors, and introduces weaker speculation about async-style response semantics that does not fit the documented cancel endpoint.

### 13. Flink REST pattern for SavepointHandlers (`flink-rest-savepoint-handlers`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.86`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 1, "specificity": 2, "usefulness": 2}}`
- Rationale: A is more cautious and better anchored to concrete repo paths and neighboring tests, with explicit uncertainty instead of invented API details. B is more speculative: it asserts a savepoints docs path and extra test classes without verification, which raises hallucination risk. A still misses the exact version-pinned savepoints doc page, but it is safer and more engineer-useful overall.

### 14. Flink REST pattern for CheckpointHandlers (`flink-rest-checkpoint-handlers`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.83`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B is better anchored to Flink 2.2.0 by naming the release-pinned docs, the exact `CheckpointHandlers` implementation, and a concrete neighboring test file. A is safer but too generic, with only a package path and vague neighboring-test guidance. B has some risk from extra claims like surfaced evidence and fragment URLs, but it is still more actionable and version-specific.

### 15. Flink REST pattern for JobResourceRequirementsUpdateHandler (`flink-rest-job-resource-requirements-update-handler`)

- Winner: `codex_without_k2`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 3, "usefulness": 2}, "codex_without_k2": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A anchors the right Flink 2.2.0 docs, the exact `JobResourceRequirementsUpdateHandler`, and feature-adjacent tests for resource-requirements. B drifts to generic job-handler tests and adds unsupported “retrieval system” claims. A is still slightly uncertain about the exact DTO/test names, but it is closer to the relevant API surface and safer for implementation work.

### 16. Flink REST pattern for JobSubmitHandler (`flink-rest-job-submit-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.89`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 1, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: B is better anchored to version-pinned docs, the concrete `JobSubmitHandler` class, and the dedicated test file. A is directionally right but too vague, explicitly uncertain about the docs target, and gives weaker implementation/test anchors. B still has some generic neighboring-test noise, but it is materially more grounded and actionable.

### 17. Flink REST pattern for FileUploads (`flink-rest-file-uploads`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 1, "grounding": 0, "risk": 2, "specificity": 1, "usefulness": 1}}`
- Rationale: B is closer because it gives concrete Flink 2.2.0 anchors for docs, `FileUploadsTest`, and a repo path, while A stays generic and explicitly lacks citations. B still appears to misstate the `FileUploads` package path and uses weak doc fragments, so its correctness is only moderate.

### 18. Flink REST pattern for DashboardConfigHandler (`flink-rest-dashboard-config-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.89`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better anchored in concrete Flink 2.2.0 artifacts: it names the handler, headers class, repo paths, and neighboring tests, while explicitly noting uncertainty about a dedicated handler test. B is mostly speculative, with repeated "likely" wording and an unverified test anchor, so it is less reliable for engineering changes.

### 19. Flink REST pattern for ClusterOverviewHandler (`flink-rest-cluster-overview-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.83`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 1, "specificity": 2, "usefulness": 2}}`
- Rationale: A is more version-specific and source-anchored: it names the 2.2.0 REST docs, the concrete `ClusterOverviewHandler`, and adjacent message headers/tests. B is too vague, omits the pinned docs URL, and speculates about `ClusterOverviewHandlerTest` without evidence. A still has some uncertainty about exact test coverage, but it is materially more reliable for an engineer changing Flink REST code.

### 20. Flink REST pattern for TaskManagersHandler (`flink-rest-taskmanagers-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 1, "risk": 2, "specificity": 1, "usefulness": 2}}`
- Rationale: B is better anchored to version-pinned Flink 2.2.0 docs, the concrete `TaskManagersHandler` class path, and neighboring test classes in `flink-runtime`. A is directionally right but too vague, hedges on basic identifiers, and lacks concrete source anchors an engineer can inspect or change confidently.

### 21. Flink REST pattern for TaskManagerDetailsHandler (`flink-rest-taskmanager-details-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.93`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 3}}`
- Rationale: A is better anchored to Flink 2.2.0 with a concrete REST docs URL, the exact handler class, the message headers class, and the direct test file. B is mostly generic, omits version-pinned source anchors, and names neighboring tests/speculation without concrete evidence. A still has slight risk around exact doc fragment semantics, but it is materially more grounded and actionable.

### 22. Flink REST pattern for JobVertexBackPressureHandler (`flink-rest-job-vertex-back-pressure-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.98`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 1, "grounding": 2, "risk": 1, "specificity": 2, "usefulness": 2}}`
- Rationale: Answer A matches Flink 2.2's actual REST package layout (`org.apache.flink.runtime.rest.handler.job` / `...rest.messages`) and cites the dedicated `JobVertexBackPressureHandlerTest`, plus the version-pinned REST docs. Answer B is materially wrong on the implementation/test package (`webmonitor/handlers`), which is a strong hallucination signal, and its neighboring tests are generic/speculative.

### 23. Flink REST pattern for JobVertexWatermarksHandler (`flink-rest-job-vertex-watermarks-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.74`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 2, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B is closer to the actual Flink source layout: `JobVertexWatermarksHandler` and its test live under `flink-runtime/.../job/metrics/`. A misplaces the handler under `job/` and stays too generic. B’s docs anchors are weak and some neighboring tests are off-target, but it still names the correct implementation and regression surfaces.

### 24. Flink REST pattern for SubtaskCurrentAttemptDetailsHandler (`flink-rest-subtask-current-attempt-details-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.92`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 1, "risk": 1, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better grounded in Flink 2.2.0 artifacts: it names the version-pinned REST docs, the concrete handler class, and a direct test plus neighboring tests. B is weaker because it cannot verify the docs URL, uses a likely wrong package path (`job/vertex`), and stays too vague to guide code changes.

### 25. Flink REST pattern for JobVertexFlameGraphHandler (`flink-rest-job-vertex-flame-graph-handler`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better anchored to the version-pinned 2.2.0 docs, names the exact implementation class and message header class, and points to the dedicated handler test plus adjacent REST tests. B is much vaguer, weak on 2.2.0 specificity, and explicitly admits uncertainty about the docs path and neighboring tests.

### 26. Flink checkpointing pattern for CheckpointCoordinator (`flink-checkpointing-checkpoint-coordinator`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.68`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 2, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B is better anchored to version-pinned Flink 2.2.0 docs, the exact `flink-runtime` class path, and adjacent tests/classes, which is what an engineer needs. It is still somewhat risky because it states internal scheduler/restore behavior and test details without enough direct evidence. A is safer but too generic and less actionable.

### 27. Flink checkpointing pattern for PendingCheckpoint (`flink-checkpointing-pending-checkpoint`)

- Winner: `codex_without_k2`
- Confidence: `0.84`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A better matches the question’s intent: it explains the pending-to-completed/abort lifecycle and anchors it with both `PendingCheckpointTest` and the neighboring `CheckpointCoordinatorTest`. B is more version-tagged, but it is narrower, less useful for an engineer, and its `#part-0001` anchors add little. Neither answer is deeply source-backed, but A is the more complete engineering guide.

### 28. Flink checkpointing pattern for CompletedCheckpoint (`flink-checkpointing-completed-checkpoint`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.96`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 3, "specificity": 2, "usefulness": 3}}`
- Rationale: A is tightly anchored to Flink 2.2.0 artifacts: version-pinned docs, `CompletedCheckpoint`, `DefaultCompletedCheckpointStore`, and concrete tests. It also states uncertainty instead of overclaiming. B stays generic, lacks precise docs anchoring, and hedges on test names, making it weaker for an engineer changing Java code.

### 29. Flink checkpointing pattern for CompletedCheckpointStore (`flink-checkpointing-completed-checkpoint-store`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.93`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: B matches the Flink 2.2 API surface better: `DefaultCompletedCheckpointStore` is the main retention implementation, and the cited docs/API page explicitly describe bounded retention and recovery behavior. A is weaker because it treats `StandaloneCompletedCheckpointStore` as the likely primary implementation and misses the key 2.2 anchor, `DefaultCompletedCheckpointStore` plus its tests.

### 30. Flink checkpointing pattern for DefaultCompletedCheckpointStore (`flink-checkpointing-default-completed-checkpoint-store`)

- Winner: `codex_without_k2`
- Confidence: `0.76`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 2, "grounding": 4, "risk": 2, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 2, "risk": 4, "specificity": 2, "usefulness": 3}}`
- Rationale: A is safer and more accurate overall. B has better concrete anchors, but it cites the wrong 2.2 config key (`execution.checkpointing.max-retained-checkpoints` instead of `execution.checkpointing.num-retained`) and likely invents `DefaultCompletedCheckpointStoreUtilsTest`. A is vaguer, but its retention summary and main class anchor are consistent with Flink 2.2.0.

### 31. Flink checkpointing pattern for CheckpointStatsTracker (`flink-checkpointing-checkpoint-stats-tracker`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.74`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 3, "usefulness": 3}}`
- Rationale: A is better anchored to version-pinned Flink 2.2 docs and concrete `flink-runtime` source/tests, and it states uncertainty where coverage is incomplete. B is more generic, uses a likely-wrong docs slug, and gives weaker source anchoring. A still has some risk from possibly over-specific test/class names, but it is materially more engineer-usable.

### 32. Flink checkpointing pattern for CheckpointStatsSnapshot (`flink-checkpointing-checkpoint-stats-snapshot`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 3, "specificity": 2, "usefulness": 3}}`
- Rationale: B is stronger because it names version-pinned Flink 2.2.0 docs, the exact `CheckpointStatsSnapshot` implementation path, and concrete neighboring tests. A is directionally right but too vague on docs and test anchors. B has a small risk of overclaiming test existence, but overall it is far more actionable and grounded for an engineer inspecting checkpoint stats behavior.

### 33. Flink checkpointing pattern for CheckpointMetrics (`flink-checkpointing-checkpoint-metrics`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.84`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better anchored in Flink runtime classes, names concrete call sites and neighboring tests, and enumerates the full metric set with an explicit uncertainty note. B is too vague for an engineer and appears to speculate about which fields are reporting-relevant, while also missing specific test anchors and overfocusing on a subset of metrics.

### 34. Flink checkpointing pattern for CheckpointProperties (`flink-checkpointing-checkpoint-properties`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.86`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 1, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B is better anchored to Flink 2.2.0 with concrete docs URLs, implementation path, and neighboring tests. A is safer but too generic and omits the version-pinned artifacts the question explicitly asks for. B has some risk from slightly overconfident savepoint wording, but it is still more actionable and source-grounded overall.

### 35. Flink checkpointing pattern for CheckpointRetentionPolicy (`flink-checkpointing-checkpoint-retention-policy`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.84`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 1, "risk": 2, "specificity": 2, "usefulness": 3}}`
- Rationale: B is better anchored to Flink 2.2.0 with version-pinned docs, the exact runtime class, and neighboring tests, while explicitly limiting claims it cannot verify. A is broader and more speculative, with weaker version grounding and a dubious “equivalent internal path” framing. Both are imperfect, but B is more actionable and lower risk for an engineer inspecting the codebase.

### 36. Flink checkpointing pattern for CheckpointIDCounter (`flink-checkpointing-checkpoint-id-counter`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.76`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: B is more anchored to version-pinned Flink 2.2.0 artifacts, names the interface, concrete implementation, and neighboring test classes, and includes uncertainty about coverage gaps. A is more cautious, but it is vaguer and relies on speculative test/class names without as much source anchoring.

### 37. Flink checkpointing pattern for StandaloneCheckpointIDCounter (`flink-checkpointing-standalone-checkpoint-id-counter`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 3}}`
- Rationale: A is better anchored to Flink 2.2.0 with exact runtime class and dedicated test filename, and it explicitly notes uncertainty about behavior. B is vaguer, omits the concrete neighboring test, and adds speculative test cases and semantics not grounded in source artifacts.

### 38. Flink checkpointing pattern for CheckpointFailureManager (`flink-checkpointing-checkpoint-failure-manager`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.83`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 3}}`
- Rationale: A is better anchored to the Flink 2.2.0 docs, the concrete `CheckpointFailureManager` implementation, and adjacent runtime tests. It also states uncertainty instead of overclaiming. B is more generic, weak on version-pinned documentation, and admits it cannot verify the exact docs path, which lowers its value for an engineer changing Java code.

### 39. Flink checkpointing pattern for CheckpointPlanCalculator (`flink-checkpointing-checkpoint-plan-calculator`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.94`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 1, "specificity": 2, "usefulness": 2}}`
- Rationale: A anchors the answer on the version-pinned 2.2 docs, the real `CheckpointPlanCalculator`/`DefaultCheckpointPlanCalculator` runtime seam, and concrete test files, while noting uncertainty. B is vaguer, omits the concrete implementation class, and cites a likely unverified `CheckpointPlanCalculatorTest`, which raises hallucination risk.

### 40. Flink checkpointing pattern for DefaultCheckpointPlanCalculator (`flink-checkpointing-default-checkpoint-plan-calculator`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.74`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: B is better anchored to version-pinned Flink 2.2.0 docs, the concrete `DefaultCheckpointPlanCalculator` class, and direct neighboring tests. A is cautious but too vague on the actual doc pages and neighboring test anchors. B is more actionable for an engineer, though it includes one somewhat adjacent test (`TestSubtaskCheckpointCoordinator`) that is not clearly direct coverage.

### 41. Flink checkpointing pattern for CheckpointRequestDecider (`flink-checkpointing-checkpoint-request-decider`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.86`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better anchored to Flink 2.2.0 by naming the runtime class, version-pinned docs, and the direct neighboring unit test. It also states uncertainty where source detail is not fully verified. B is much vaguer, adds unsupported scheduling claims and extra test targets without grounding, and admits it has not inspected the source. A is still somewhat speculative on branch details, but materially safer.

### 42. Flink checkpointing pattern for CheckpointResourcesCleanupRunner (`flink-checkpointing-checkpoint-resources-cleanup-runner`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.95`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 1, "risk": 1, "specificity": 2, "usefulness": 2}}`
- Rationale: A is much better anchored to version-pinned Flink 2.2.0 docs, the concrete runtime class, and a direct neighboring test file. B is too vague, gives an apparently wrong package for the class, and lacks verifiable test or doc anchors. A has some mild overreach in adjacent-test suggestions, but it is still the only answer that is concretely source-grounded.

### 43. Flink checkpointing pattern for CheckpointStorageLoader (`flink-checkpointing-checkpoint-storage-loader`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.92`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 3, "usefulness": 3}}`
- Rationale: A is better anchored to Flink 2.2.0 docs and the loader/test classes the question asks for. B contains a concrete config-key error (`state.checkpoints.dir` instead of `execution.checkpointing.dir`) and adds unsupported claims about savepoint influence. A is still somewhat speculative on neighboring tests, but it is more version-specific and less hallucinatory.

### 44. Flink checkpointing pattern for CheckpointStorageCoordinatorView (`flink-checkpointing-checkpoint-storage-coordinator-view`)

- Winner: `codex_without_k2`
- Confidence: `0.66`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A is closer to the likely 2.2.0 engineering anchors: it names the coordinator-view class and the most relevant runtime tests for filesystem/jobmanager storage. B is more version-pinned on docs, but its doc anchors look unverified and its test selection is less adjacent to the coordinator-view contract. Neither is perfect; A is less risky and more actionable.

### 45. Flink checkpointing pattern for StateBackend (`flink-checkpointing-state-backend`)

- Winner: `codex_without_k2`
- Confidence: `0.86`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 4, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 4}}`
- Rationale: A is safer and better aligned with Flink 2.2: it cites the versioned docs, the `StateBackend` contract, and the right concrete backends while explicitly flagging uncertainty. B is more specific, but its `repo://` citations are not verifiable, `StateBackendUtils.java` is a utility not a neighboring test, and `BatchExecutionStateBackend` is a distracting batch-specific anchor.

### 46. Flink checkpointing pattern for OperatorStateBackend (`flink-checkpointing-operator-state-backend`)

- Winner: `codex_without_k2`
- Confidence: `0.9`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 2, "usefulness": 2}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: B is closer to the Flink 2.2 runtime layout: `DefaultOperatorStateBackend` is the concrete backend to inspect, and `DefaultOperatorStateBackendTest` is the more plausible adjacent regression anchor. A likely invents `OperatorStateBackendTest` and over-centers the interface, which weakens correctness and raises hallucination risk. B is still slightly broad on neighboring tests, but it is more actionable overall.

### 47. Flink checkpointing pattern for KeyedStateBackend (`flink-checkpointing-keyed-state-backend`)

- Winner: `codex_without_k2`
- Confidence: `0.83`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 2, "specificity": 3, "usefulness": 2}, "codex_without_k2": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A better matches the requested keyed-state checkpointing scope and points to the likely relevant runtime classes and nearby keyed-backend tests. B is more source-heavy but drifts into unrelated channel/file-merging tests and uses weaker, partially fabricated-looking anchors, including odd doc fragments and unsupported retrieval claims.

### 48. Flink checkpointing pattern for SavepointRestoreSettings (`flink-checkpointing-savepoint-restore-settings`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.67`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 4}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A is more grounded: it names the exact runtime class, the scheduler path that consumes it, and two concrete neighboring flink-runtime tests. B is directionally right but vaguer on version-pinned docs and less precise on the relevant test surface. A’s doc choices are not ideal for savepoints, but its artifact-level anchors are stronger overall.

### 49. Flink checkpointing pattern for SavepointFormatType (`flink-checkpointing-savepoint-format-type`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.9`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A is materially better grounded: it names the version-pinned 2.2.0 source file, relevant runtime call sites, and concrete neighboring tests. B is mostly generic, speculates about files/tests, and omits the runtime anchors needed to change Java code confidently. A still has one potentially overstrong claim about backend support, but it is far less hallucinatory overall.

### 50. Flink checkpointing pattern for CheckpointCoordinatorConfiguration (`flink-checkpointing-checkpoint-coordinator-configuration`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.89`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 1, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: B is better anchored: it pins Flink 2.2.0 docs, gives a repo URI for the implementation class, and names neighboring tests. A is vaguer and appears to place `CheckpointCoordinatorConfiguration` in the wrong package, which is a concrete correctness risk for an engineer inspecting the codebase.

### 51. Kafka Connect pattern for ConnectorPluginsResource (`kafka-rest-connector-plugins-resource`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.87`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A better matches the ask: it gives version-pinned 4.2 docs, the exact `ConnectorPluginsResource` implementation, and the neighboring test class that exercises `validateConfigs(...)`. B is more tentative and omits the concrete 4.2 docs anchor, so it is less useful for an engineer tracing the validation path.

### 52. Kafka Connect pattern for AbstractHerder (`kafka-connect-abstract-herder`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.79`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A is better anchored to Kafka Connect-specific, version-pinned docs and gives concrete nearby tests plus a cautious uncertainty note. B has some plausible implementation detail, but its doc anchors are broader and less topic-specific, and several test suggestions are more generic/less verified. A is more useful for an engineer tracing validation in the herder layer with lower hallucination risk.

### 53. Kafka Connect pattern for DistributedHerder (`kafka-connect-distributed-herder`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.92`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 3}}`
- Rationale: A names version-pinned Kafka 4.2 Connect docs, the exact `DistributedHerder` source, and the neighboring `DistributedHerderTest`, which matches the requested anchor set. B is vaguer, uses a non-pinned docs root, and speculates about extra classes/tests without concrete support. A is more grounded and safer for an engineer inspecting the update path.

### 54. Kafka Connect pattern for StandaloneHerder (`kafka-connect-standalone-herder`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.92`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 1, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better anchored for Kafka Connect 4.2.0: it names version-pinned docs, the concrete implementation class, and the nearest test file. B is directionally right but too vague, omits the doc anchors, and adds less actionable guidance for an engineer changing standalone config-update behavior.

### 55. Kafka Connect pattern for Herder (`kafka-connect-herder`)

- Winner: `codex_without_k2`
- Confidence: `0.67`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: B better answers the actual Herder question by naming the `Herder` interface and the concrete distributed/standalone implementation and test classes. A is stronger on version-pinned docs, but it shifts the anchor to the REST API and gives a weaker, likely incorrect neighboring-test recommendation. B is missing the pinned docs URL, but is the more accurate code-oriented answer.

### 56. Kafka Connect pattern for Worker (`kafka-connect-worker`)

- Winner: `codex_without_k2`
- Confidence: `0.95`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 1, "grounding": 3, "risk": 1, "specificity": 2, "usefulness": 2}, "codex_without_k2": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A correctly centers Kafka Connect 4.2.0 on `Worker` and names the expected runtime neighbors and unit tests. B misanchors the answer on `AbstractHerder` instead of `Worker`, and its integration-test recommendation is not the right neighboring test surface for tracing worker lifecycle responsibilities. A is slightly less precise on docs, but materially more aligned with the question.

### 57. Kafka Connect pattern for WorkerConnector (`kafka-connect-worker-connector`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.84`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 1, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B is better anchored for a Kafka 4.2.0 code-change task: it names version-pinned Connect docs, the exact `WorkerConnector` class, and concrete test files. A is mostly generic, lacks pinned docs, and explicitly says it is uncertain about the relevant anchors. B does overreach slightly with extra method/test claims, but it is still the more version-specific and actionable answer.

### 58. Kafka Connect pattern for WorkerTask (`kafka-connect-worker-task`)

- Winner: `codex_without_k2`
- Confidence: `0.66`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A is safer and more aligned with WorkerTask lifecycle inspection: it names the right runtime class and the closest sibling tests, and it explicitly flags uncertainty about the pinned docs URL. B is more concrete on paper, but it overcommits to unverified doc URLs and includes an integration test that is not a direct WorkerTask lifecycle neighbor.

### 59. Kafka Connect pattern for WorkerSinkTask (`kafka-connect-worker-sink-task`)

- Winner: `codex_without_k2`
- Confidence: `0.68`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 2, "specificity": 4, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A is better aligned to the ask: it anchors on `WorkerSinkTask`, cites the relevant 4.2.0 source/test files, and names the most plausible neighboring tests for sink delivery/commit behavior. B is more precise on links, but it drifts into likely unsupported internal method names and cites irrelevant integration tests, increasing hallucination risk.

### 60. Kafka Connect pattern for WorkerSourceTask (`kafka-connect-worker-source-task`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B is better anchored to Kafka 4.2 Connect docs, names the runtime scheduler class that actually gates source offset commits, and points to concrete neighboring tests. A is mostly generic, cites only the docs root, and misses the commit scheduler path that matters for WorkerSourceTask behavior. B still overstates some exact test/class existence and method details, but it is materially more useful and grounded.

### 61. Kafka Connect pattern for ConnectorConfig (`kafka-connect-connector-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.86`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 1, "risk": 4, "specificity": 2, "usefulness": 2}}`
- Rationale: B is better anchored for Kafka Connect 4.2.0: it names version-pinned docs, the `ConnectorConfig` implementation, and nearby tests, which is what an engineer needs. A is cautious but too generic, omits the doc anchors the question explicitly asks for, and relies on hedged uncertainty instead of concrete source artifacts.

### 62. Kafka Connect pattern for SinkConnectorConfig (`kafka-connect-sink-connector-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better anchored to version-pinned Connect docs, the actual `SinkConnectorConfig` implementation, and a neighboring integration test with a named sink-validation case. B is more speculative: its docs URLs are less precise, it points to a likely-nonexistent or unverified unit test, and it offers weaker evidence for the exact 4.2.0 validation surface.

### 63. Kafka Connect pattern for SourceConnectorConfig (`kafka-connect-source-connector-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.83`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 3, "usefulness": 3}}`
- Rationale: B is better anchored to Kafka 4.2.0 by citing versioned Connect docs, the `SourceConnectorConfig` implementation, and a real validation call site in `AbstractHerder`. A is weaker because it only points at the docs root and includes a likely-unsubstantiated `TopicCreationConfigTest` anchor. B still has one somewhat tangential integration test, but overall it is more version-specific and actionable.

### 64. Kafka Connect pattern for WorkerConfig (`kafka-connect-worker-config`)

- Winner: `codex_without_k2`
- Confidence: `0.9`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 2, "grounding": 2, "risk": 1, "specificity": 3, "usefulness": 2}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A stays cautious and mostly correct: it anchors on `WorkerConfig`, the mode-specific subclasses, and relevant neighboring tests without overclaiming exact URLs or file existence. B is more concrete but likely fabricates or misstates anchors: the standalone config path is probably wrong, the integration test is irrelevant, and the repo/doc URLs look unsupported. For an engineer changing Java code, A is safer and more usable.

### 65. Kafka Connect pattern for DistributedConfig (`kafka-connect-distributed-config`)

- Winner: `codex_without_k2`
- Confidence: `0.66`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A is safer and better aligned with the requested anchors: it centers `DistributedConfig`, the adjacent worker/herder classes, and neighboring config tests. B has nicer versioned URLs, but it widens scope with a broad guide and an adjacent cluster fixture, and it makes more unsupported claims about what the tests cover.

### 66. Kafka Connect pattern for StandaloneConfig (`kafka-connect-standalone-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.95`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 3, "usefulness": 2}}`
- Rationale: B matches the 4.2.0 Connect docs and the actual source layout: `StandaloneConfig` is in `org/apache/kafka/connect/runtime/standalone/`, with a direct neighboring `StandaloneConfigTest`. A misplaces the class/test under `runtime/`, uses a generic docs URL, and adds less-relevant tests. B is more version-specific and lower risk for an engineer changing Java code.

### 67. Kafka Connect pattern for ConfigDef (`kafka-connect-config-def`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.86`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 3, "specificity": 2, "usefulness": 3}}`
- Rationale: A better matches the question’s ask: it names version-pinned Kafka Connect docs and the `org.apache.kafka.common.config.ConfigDef` anchor, and it gives concrete repo paths for Connect validator usage. B has plausible ConfigDef semantics, but it anchors on `AbstractConfig`, omits version-pinned Connect docs, and is less grounded in concrete source artifacts for Kafka 4.2.0.

### 68. Kafka Connect pattern for ConfigValue (`kafka-connect-config-value`)

- Winner: `codex_without_k2`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 5, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: B is better anchored for Kafka Connect 4.2.0 because it points to version-pinned Javadocs for `ConfigValue`/`ConfigDef` and the `clients` implementation class, which directly explain the representation fields. A is broadly plausible, but its docs are more indirect and its extra test anchors are less clearly relevant to the asked representation question.

### 69. Kafka Connect pattern for ConfigTransformer (`kafka-connect-config-transformer`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 3, "usefulness": 3}}`
- Rationale: B is closer to the Kafka 4.2.0 surface: `org.apache.kafka.common.config.ConfigTransformer` is the actual transformer class, and the Connect runtime wrapper/related paths are concrete. A misplaces the implementation in `connect/runtime` and is vaguer about the version-pinned docs anchor. B is still broader than necessary, but it is materially more grounded and actionable.

### 70. Kafka Connect pattern for ConfigProvider (`kafka-connect-config-provider`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: A is more version-specific and better anchored to Kafka 4.2 docs plus the `clients` module. It names the exact concrete class `FileConfigProvider` and cites the relevant 4.2 configuration pages. B is directionally right, but it is less grounded, omits version-pinned URLs, and introduces `ConfigTransformer` as extra context rather than the requested anchor.

### 71. Kafka Connect pattern for Plugins (`kafka-connect-plugins`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.93`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 1, "risk": 1, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better anchored to Kafka Connect 4.2.0 with versioned docs, the concrete `Plugins` runtime class, and nearby test files that plausibly exercise plugin discovery and class loading. B is much vaguer, omits version-pinned docs, and names unverified tests and classes (`PluginsTest`, `PluginClassLoader`) without support. A still has some uncertainty about exact doc section semantics, but it is materially more grounded.

### 72. Kafka Connect pattern for PluginDesc (`kafka-connect-plugin-desc`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.92`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 5, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 1, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better anchored: it names a concrete implementation class, a real test, and version-pinned Kafka 4.2 docs, while explicitly noting uncertainty. B is weaker because its docs path is vague and it names adjacent tests that may not exist, which raises hallucination risk. For engineer use, A gives actionable files and surrounding code paths.

### 73. Kafka Connect pattern for PluginType (`kafka-connect-plugin-type`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.69`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 1, "risk": 4, "specificity": 1, "usefulness": 2}}`
- Rationale: B is more version-specific and actionable: it pins docs, names the implementation class, and points to a concrete neighboring test file. A is safer but too generic, with no exact doc anchor and only package-level test guidance. B still has some uncertainty around the relevance of `MultiVersionTest`, but overall it is more grounded for an engineer inspecting `PluginType`.

### 74. Kafka Connect pattern for DelegatingClassLoader (`kafka-connect-delegating-class-loader`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.96`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 1, "risk": 2, "specificity": 1, "usefulness": 2}}`
- Rationale: A is materially better grounded: it names the exact 4.2-pinned docs, the implementation class, and adjacent tests in `connect/runtime`. B stays generic, omits version-pinned URLs, and gives no concrete test or source anchors. A still has minor uncertainty where some docs are contextual rather than direct specs, but it is much more actionable for a Java engineer.

### 75. Kafka Connect pattern for PluginClassLoader (`kafka-connect-plugin-class-loader`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.92`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 3, "usefulness": 3}}`
- Rationale: A is better grounded in Kafka 4.2.x-specific docs and concrete source paths, and it names plausible neighboring isolation tests with an explicit uncertainty note. B is weaker: its docs are generic, and `PluginClassLoaderTest` may be fabricated or at least unconfirmed, so the answer is less reliable for a Java engineer targeting Connect internals.

### 76. Kafka Connect pattern for PluginScanResult (`kafka-connect-plugin-scan-result`)

- Winner: `codex_without_k2`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A is better anchored to the exact implementation package and the most relevant neighboring tests, and it explicitly flags uncertainty about `PluginScanResultTest`. B has nicer-looking citations, but it leans on broader docs and makes stronger unsupported claims about `PluginScanResult` internals and retrieved evidence.

### 77. Kafka Connect pattern for PluginUtils (`kafka-connect-plugin-utils`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.84`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A gives concrete version-pinned docs, the exact implementation class, and the neighboring unit test, which is what an engineer needs. It is still slightly risky because the exact doc fragment IDs and the alias-helper characterization may not be fully verified. B is too vague, lacks pinned anchors, and adds speculative neighboring tests and helper behavior without support.

### 78. Kafka Connect pattern for ConnectRestServer (`kafka-rest-connect-rest-server`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.96`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better grounded for Kafka Connect 4.2.0: it names version-pinned docs, the exact `ConnectRestServer` implementation path, and neighboring tests in the same package. B is too vague on docs, uses a likely-wrong generic docs URL, and speculates about nearby tests instead of anchoring them to concrete source artifacts.

### 79. Kafka Connect pattern for RestServerConfig (`kafka-rest-rest-server-config`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.98`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 1, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A names version-pinned Kafka 4.2 docs, the exact `RestServerConfig` implementation, and concrete neighboring tests, with explicit uncertainty. B is much weaker: it uses a generic `docs/connect.html`, omits version-pinned URLs, and hand-waves at sibling tests. For an engineer changing Java code, A is the safer and more actionable anchor set.

### 80. Kafka Connect pattern for ConnectorsResource (`kafka-rest-connectors-resource`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 4, "grounding": 2, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B is better grounded in a version-pinned Kafka 4.2 Connect docs URL, names the exact implementation and primary test, and adds plausible neighboring REST tests without inventing bean-validation or Spring claims. A is reasonable but less version-specific and less grounded, with weaker doc anchoring and fewer adjacent test anchors.

### 81. Kafka Connect pattern for ConnectorStateInfo (`kafka-rest-connector-state-info`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.84`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 3, "usefulness": 3}}`
- Rationale: A answers the asked anchoring question directly with a version-pinned Kafka 4.2 docs URL and the concrete `ConnectorStateInfo` implementation class. B is directionally plausible but too generic on docs, adds weaker implementation guesses, and is less grounded for a version-specific engineering lookup.

### 82. Kafka Connect pattern for ConnectorInfo (`kafka-rest-connector-info`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.81`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 3, "specificity": 2, "usefulness": 3}}`
- Rationale: A is better anchored: it names version-pinned Kafka Connect docs and the concrete `ConnectorInfo` implementation class in `connect/runtime`. B is safer about URL guessing, but it is less grounded and less specific, which matters here because the question asks for the exact doc and code anchors. A still has some URL-verification risk, but it is more actionable for an engineer.

### 83. Kafka Connect pattern for CreateConnectorRequest (`kafka-rest-create-connector-request`)

- Winner: `codex_without_k2`
- Confidence: `0.8`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 2, "usefulness": 2}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A anchors the right REST entity and the closest resource test, which is what an engineer needs for request-validation work. B uses versioned URLs, but its test anchors are mostly peripheral and it omits the main resource class, making it less useful and more likely to mislead. Both are somewhat speculative on exact validation branches, but A is closer to the relevant source surface.

### 84. Kafka Connect pattern for ConnectorType (`kafka-rest-connector-type`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.89`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 3, "usefulness": 3}}`
- Rationale: A is better anchored to the requested 4.2 version-pinned docs, the actual REST entity `ConnectorType`, and the dedicated `ConnectorTypeTest`, while explicitly flagging uncertainty. B is vaguer, leans on a generic `docs/connect.html` anchor, and shifts focus to `ConnectorsResource` without clearly supporting the asked classification anchor.

### 85. Kafka Connect pattern for Connector (`kafka-connect-connector`)

- Winner: `codex_without_k2`
- Confidence: `0.78`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A better matches the actual Kafka Connect 4.2.0 base contract: `Connector` Javadoc plus direct `connect/api` unit tests (`ConnectorTest`, `SourceConnectorTest`, `SinkConnectorTest`) are the right anchors. B has good version-pinned docs, but it misses the direct api-module tests and instead leans on runtime integration tests that are adjacent rather than contract-defining.

### 86. Kafka Connect pattern for SourceConnector (`kafka-connect-source-connector`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.82`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 4, "usefulness": 4}}`
- Rationale: B is more version-pinned and better grounded in concrete repo/doc anchors, with clearer uncertainty about missing tests. A is useful but likely overreaches on validation/config responsibilities and may invent or overstate neighboring tests such as SourceConnectorTest. B’s test coverage is thinner, but its claims are safer and more defensible for a Kafka 4.2.0 evaluation.

### 87. Kafka Connect pattern for SinkConnector (`kafka-connect-sink-connector`)

- Winner: `codex_without_k2`
- Confidence: `0.79`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A better matches SinkConnector’s actual contract: connector-level metadata, task factory/config generation, and sink-runtime neighbors like SinkTask/WorkerSinkTask. B is more URL-grounded, but its test anchor is clearly off-target (ExactlyOnceSourceIntegrationTest) and it leans on a generic Connector framing instead of the sink-specific API surface.

### 88. Kafka Connect pattern for Transformation (`kafka-connect-transformation`)

- Winner: `codex_without_k2`
- Confidence: `0.71`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 3, "specificity": 4, "usefulness": 4}}`
- Rationale: B is closer to the actual Connect SMT execution path: it names the runtime transformation chain and task-level tests that are more likely to exercise single-message transform behavior. A is safer and better caveated, but it anchors mostly config-validation tests and misses the core runtime class. B still has some uncertainty around exact test filenames and should be verified against the 4.2.0 tree.

### 89. Kafka Connect pattern for HeaderConverter (`kafka-connect-header-converter`)

- Winner: `codex_without_k2`
- Confidence: `0.88`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 3, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 5, "usefulness": 5}}`
- Rationale: A is closer to the asked anchor set: 4.2.0 Connect docs, the concrete `SimpleHeaderConverter` implementation, and a plausible neighboring test. B over-centers the interface/config wiring and a test helper (`SampleHeaderConverter`) instead of the production converter and direct regression tests, so it is less useful for changing Java code.

### 90. Kafka Connect pattern for Converter (`kafka-connect-converter`)

- Winner: `codex_without_k2`
- Confidence: `0.87`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 2, "usefulness": 2}, "codex_without_k2": {"correctness": 4, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}}`
- Rationale: B is closer to the actual 4.2.0 Connect conversion path: `Converter`, concrete `JsonConverter`, and the worker call sites that split key vs value handling. A mostly anchors config validation (`ConnectorConfig`) and misses the runtime conversion behavior the question asks for. B is slightly less precise on version-pinned docs and some test names, but it is materially more actionable and better grounded.

### 91. Kafka Connect pattern for Schema (`kafka-connect-schemas`)

- Winner: `codex_without_k2`
- Confidence: `0.94`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 3, "usefulness": 2}, "codex_without_k2": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: B is better anchored to the actual 4.2.0 Connect API surface: `ConnectSchema`, `SchemaBuilder`, `SchemaProjector`, `Struct`, and the `connect/api/src/test/java/org/apache/kafka/connect/data/*Test.java` neighbors that do exist in 4.2.0. A’s test anchors are mostly off-module and its claim that no direct schema test was surfaced is false.

### 92. Kafka Connect pattern for SchemaBuilder (`kafka-connect-schema-builder`)

- Winner: `codex_without_k2`
- Confidence: `0.97`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 2, "usefulness": 2}, "codex_without_k2": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}}`
- Rationale: A names the version-pinned 4.2 Javadocs and the actual connect/api implementation and test anchors that exist in Kafka, including SchemaBuilderTest and ConnectSchemaTest. B is less accurate: it relies on broader Connect docs, cites an unrelated integration test, and incorrectly claims SchemaBuilder-specific tests were not surfaced even though they exist.

### 93. Kafka Connect pattern for Struct (`kafka-connect-struct`)

- Winner: `codex_without_k2`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 3, "usefulness": 2}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: B is closer to the actual Kafka Connect 4.2.0 validation surface: `Struct`, `ConnectSchema`, `SchemaBuilderTest`, and `StructTest` are the right anchors. A’s versioned docs are good, but its test guidance is mis-anchored to unrelated integration tests and incorrectly implies no Struct-specific test exists, which reduces trust.

### 94. Kafka Connect pattern for SinkRecord (`kafka-connect-sink-record`)

- Winner: `codex_without_k2`
- Confidence: `0.91`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 2, "grounding": 3, "risk": 1, "specificity": 4, "usefulness": 2}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 5, "specificity": 3, "usefulness": 4}}`
- Rationale: A stays aligned with the public `SinkRecord`/`ConnectRecord` API and names the right neighboring tests, while being appropriately cautious about uncertainty. B adds some versioned links, but mixes in irrelevant docs/tests, incorrectly claims a dedicated `SinkRecordTest` was not surfaced, and elevates `InternalSinkRecord` over the public API anchor the question asked for.

### 95. Kafka Connect pattern for SourceRecord (`kafka-connect-source-record`)

- Winner: `codex_without_k2`
- Confidence: `0.87`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 2, "grounding": 4, "risk": 2, "specificity": 3, "usefulness": 2}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A better matches the requested anchor set: version-pinned docs, the actual `SourceRecord` implementation, and nearby unit tests (`SourceRecordTest`, `ConnectRecordTest`). B has more concrete URLs and paths, but its “neighboring tests” are off-target runtime/integration helpers and its `newRecord` preservation claim is less well-grounded for the asked source/partition inspection.

### 96. Kafka Connect pattern for ConnectorClientConfigRequest (`kafka-connect-connector-client-config-request`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.93`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 2}}`
- Rationale: A is better grounded in Kafka Connect 4.2.0 docs, names the concrete runtime implementation that consumes `ConnectorClientConfigRequest.clientProps()`, and points to plausible neighboring tests. B is weaker because it relies on a generic docs page, omits the key abstract policy class, and likely invents a `ConnectorClientConfigRequestTest` path without support.

### 97. Kafka Connect pattern for ConnectorClientConfigOverridePolicy (`kafka-connect-connector-client-config-override-policy`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.93`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 1, "specificity": 2, "usefulness": 2}}`
- Rationale: A anchors the answer in the interface, the abstract runtime validator, version-pinned 4.2 docs, and adjacent tests, which matches the requested source kinds. B likely misplaces built-in policy classes under `connect/api`, overstates runtime details without a concrete anchor, and stays vague about the validation path and exact tests. A is materially more useful for an engineer changing Java code.

### 98. Kafka Connect pattern for AbstractConnectorClientConfigOverridePolicy (`kafka-connect-abstract-connector-client-config-override-policy`)

- Winner: `codex_without_k2`
- Confidence: `0.84`
- Blinded label mapping: `{"A": "codex_without_k2", "B": "codex_with_k2_real_mcp"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 2, "grounding": 4, "risk": 2, "specificity": 4, "usefulness": 3}, "codex_without_k2": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A is safer and more likely correct for Kafka 4.2.0: it names the documented policy surface and avoids dubious class claims. B is more concrete on paths, but it likely hallucinates `AllowlistConnectorClientConfigOverridePolicy` and leans on `PluginUtilsTest`, which is not a strong behavioral anchor for override-policy logic. A is less complete on tests, but materially lower risk.

### 99. Kafka Connect pattern for NoneConnectorClientConfigOverridePolicy (`kafka-connect-none-connector-client-config-override-policy`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.9`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 3, "grounding": 2, "risk": 3, "specificity": 2, "usefulness": 3}}`
- Rationale: A is better anchored for Kafka Connect 4.2.0: it names the exact runtime class, version-pinned docs, and concrete neighboring tests, and it explicitly marks uncertainty. B gets the behavior mostly right, but its doc anchor is too generic and its test guidance is non-specific, making it less useful for an engineer changing the Java code.

### 100. Kafka Connect pattern for PrincipalConnectorClientConfigOverridePolicy (`kafka-connect-principal-connector-client-config-override-policy`)

- Winner: `codex_with_k2_real_mcp`
- Confidence: `0.94`
- Blinded label mapping: `{"A": "codex_with_k2_real_mcp", "B": "codex_without_k2"}`
- Scores by run: `{"codex_with_k2_real_mcp": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}, "codex_without_k2": {"correctness": 2, "grounding": 2, "risk": 2, "specificity": 2, "usefulness": 3}}`
- Rationale: A is version-specific and anchored to the right Kafka 4.2 docs, the exact `PrincipalConnectorClientConfigOverridePolicy` class, and the adjacent test/base-test structure. B is too generic, cites a non-pinned docs page, and drifts to broader policy classes and speculative test coverage. A also explicitly notes uncertainty and deprecation, which matches the source surface better.
