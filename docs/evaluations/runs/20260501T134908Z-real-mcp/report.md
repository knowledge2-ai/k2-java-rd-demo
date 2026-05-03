# Codex With Real K2 MCP vs Without K2 E2E Comparison

Generated: `2026-05-01T14:15:56.841985+00:00`

## Summary

- Cases: `100`
- Codex without K2 answers generated: `100`
- Codex without K2: combined `0.189375`, retrieval `0`, answer `0.37875`, safety `1`; passed cases: `0`
- Codex with real K2 MCP answers generated: `100`
- Codex with real K2 MCP: combined `0.928875`, retrieval `0.954`, answer `0.90375`, safety `1`; passed cases: `93`
- Score delta: `0.7395`
- Retrieval score delta: `0.954`
- Answer score delta: `0.525`

`passed_cases` is an evidence-grounding threshold, not an answer-count metric. A run can generate an answer and still fail when it does not retrieve or cite the required version-pinned docs, source files, and tests.

## Method

- Baseline used `codex exec` with no K2 MCP server, no shell tool, no browser tool, and no web-search feature.
- Assisted run used `codex exec` with a real local stdio MCP server named `k2-java-rd`.
- The K2 MCP server used the `sdk` backend against the demo corpora and logged every tool payload used for scoring.
- Non-interactive Codex requires `--dangerously-bypass-approvals-and-sandbox` for external MCP tool calls; shell, browser, and web-search features were disabled in the same run.

## Retrieval Profiles

```json
{
  "code_tests_guides": {
    "dense_weight": 0.0,
    "enabled": true,
    "fusion_mode": "rrf",
    "metadata_sparse_enabled": true,
    "metadata_sparse_weight": 0.2,
    "rrf_k": 60,
    "sparse_weight": 0.8
  },
  "docs": {
    "dense_weight": 0.9,
    "enabled": true,
    "fusion_mode": "rrf",
    "metadata_sparse_enabled": true,
    "metadata_sparse_weight": 0.0,
    "rrf_k": 61,
    "sparse_weight": 0.1
  }
}
```

## Per-Case Results

### Flink REST pattern for DispatcherRestEndpoint

- Case ID: `flink-rest-dispatcher-rest-endpoint`
- Without K2: combined `0.125`, retrieval `0`, answer `0.25`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.841667`, retrieval `0.933333`, answer `0.75`, safety `1`, passed `True`, results `22`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for WebMonitorEndpoint

- Case ID: `flink-rest-web-monitor-endpoint`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.875`, retrieval `1`, answer `0.75`, safety `1`, passed `True`, results `24`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for RestServerEndpoint

- Case ID: `flink-rest-rest-server-endpoint`
- Without K2: combined `0.125`, retrieval `0`, answer `0.25`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.875`, retrieval `1`, answer `0.75`, safety `1`, passed `True`, results `15`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for AbstractRestHandler

- Case ID: `flink-rest-abstract-rest-handler`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.904167`, retrieval `0.933333`, answer `0.875`, safety `1`, passed `True`, results `21`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for JobDetailsHandler

- Case ID: `flink-rest-job-details-handler`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `22`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for JobConfigHandler

- Case ID: `flink-rest-job-config-handler`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `21`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for JobExceptionsHandler

- Case ID: `flink-rest-job-exceptions-handler`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `23`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for JobAccumulatorsHandler

- Case ID: `flink-rest-job-accumulators-handler`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.904167`, retrieval `0.933333`, answer `0.875`, safety `1`, passed `True`, results `21`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for JobPlanHandler

- Case ID: `flink-rest-job-plan-handler`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.966667`, retrieval `0.933333`, answer `1`, safety `1`, passed `True`, results `23`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for JobVertexDetailsHandler

- Case ID: `flink-rest-job-vertex-details-handler`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.904167`, retrieval `0.933333`, answer `0.875`, safety `1`, passed `True`, results `19`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for JobVertexTaskManagersHandler

- Case ID: `flink-rest-job-vertex-taskmanagers-handler`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.966667`, retrieval `0.933333`, answer `1`, safety `1`, passed `True`, results `20`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for JobCancellationHandler

- Case ID: `flink-rest-job-cancellation-handler`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `17`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for SavepointHandlers

- Case ID: `flink-rest-savepoint-handlers`
- Without K2: combined `0.125`, retrieval `0`, answer `0.25`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.808333`, retrieval `0.866667`, answer `0.75`, safety `1`, passed `False`, results `6`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for CheckpointHandlers

- Case ID: `flink-rest-checkpoint-handlers`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.6125`, retrieval `0.6`, answer `0.625`, safety `1`, passed `False`, results `6`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for JobResourceRequirementsUpdateHandler

- Case ID: `flink-rest-job-resource-requirements-update-handler`
- Without K2: combined `0.125`, retrieval `0`, answer `0.25`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.841667`, retrieval `0.933333`, answer `0.75`, safety `1`, passed `True`, results `22`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for JobSubmitHandler

- Case ID: `flink-rest-job-submit-handler`
- Without K2: combined `0.125`, retrieval `0`, answer `0.25`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.875`, retrieval `1`, answer `0.75`, safety `1`, passed `True`, results `20`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for FileUploads

- Case ID: `flink-rest-file-uploads`
- Without K2: combined `0.125`, retrieval `0`, answer `0.25`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `20`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for DashboardConfigHandler

- Case ID: `flink-rest-dashboard-config-handler`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.904167`, retrieval `0.933333`, answer `0.875`, safety `1`, passed `True`, results `20`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for ClusterOverviewHandler

- Case ID: `flink-rest-cluster-overview-handler`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.904167`, retrieval `0.933333`, answer `0.875`, safety `1`, passed `True`, results `19`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for TaskManagersHandler

- Case ID: `flink-rest-taskmanagers-handler`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.904167`, retrieval `0.933333`, answer `0.875`, safety `1`, passed `True`, results `18`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for TaskManagerDetailsHandler

- Case ID: `flink-rest-taskmanager-details-handler`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `20`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for JobVertexBackPressureHandler

- Case ID: `flink-rest-job-vertex-back-pressure-handler`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `15`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for JobVertexWatermarksHandler

- Case ID: `flink-rest-job-vertex-watermarks-handler`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `18`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for SubtaskCurrentAttemptDetailsHandler

- Case ID: `flink-rest-subtask-current-attempt-details-handler`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `21`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink REST pattern for JobVertexFlameGraphHandler

- Case ID: `flink-rest-job-vertex-flame-graph-handler`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `21`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for CheckpointCoordinator

- Case ID: `flink-checkpointing-checkpoint-coordinator`
- Without K2: combined `0.125`, retrieval `0`, answer `0.25`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `17`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for PendingCheckpoint

- Case ID: `flink-checkpointing-pending-checkpoint`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `11`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for CompletedCheckpoint

- Case ID: `flink-checkpointing-completed-checkpoint`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `17`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for CompletedCheckpointStore

- Case ID: `flink-checkpointing-completed-checkpoint-store`
- Without K2: combined `0.125`, retrieval `0`, answer `0.25`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `21`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for DefaultCompletedCheckpointStore

- Case ID: `flink-checkpointing-default-completed-checkpoint-store`
- Without K2: combined `0.125`, retrieval `0`, answer `0.25`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `36`
- MCP tool calls: `{"k2_answer_with_sources": 1, "k2_search_code": 5, "k2_search_docs": 1, "k2_search_tests": 4}`

### Flink checkpointing pattern for CheckpointStatsTracker

- Case ID: `flink-checkpointing-checkpoint-stats-tracker`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `23`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for CheckpointStatsSnapshot

- Case ID: `flink-checkpointing-checkpoint-stats-snapshot`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `19`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for CheckpointMetrics

- Case ID: `flink-checkpointing-checkpoint-metrics`
- Without K2: combined `0.125`, retrieval `0`, answer `0.25`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `17`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for CheckpointProperties

- Case ID: `flink-checkpointing-checkpoint-properties`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `16`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for CheckpointRetentionPolicy

- Case ID: `flink-checkpointing-checkpoint-retention-policy`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.904167`, retrieval `0.933333`, answer `0.875`, safety `1`, passed `True`, results `19`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for CheckpointIDCounter

- Case ID: `flink-checkpointing-checkpoint-id-counter`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.904167`, retrieval `0.933333`, answer `0.875`, safety `1`, passed `True`, results `21`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for StandaloneCheckpointIDCounter

- Case ID: `flink-checkpointing-standalone-checkpoint-id-counter`
- Without K2: combined `0.125`, retrieval `0`, answer `0.25`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `17`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for CheckpointFailureManager

- Case ID: `flink-checkpointing-checkpoint-failure-manager`
- Without K2: combined `0.125`, retrieval `0`, answer `0.25`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.875`, retrieval `1`, answer `0.75`, safety `1`, passed `True`, results `21`
- MCP tool calls: `{"k2_answer_with_sources": 1, "k2_search_code": 1, "k2_search_docs": 1, "k2_search_tests": 2}`

### Flink checkpointing pattern for CheckpointPlanCalculator

- Case ID: `flink-checkpointing-checkpoint-plan-calculator`
- Without K2: combined `0.125`, retrieval `0`, answer `0.25`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `22`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for DefaultCheckpointPlanCalculator

- Case ID: `flink-checkpointing-default-checkpoint-plan-calculator`
- Without K2: combined `0.125`, retrieval `0`, answer `0.25`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `22`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for CheckpointRequestDecider

- Case ID: `flink-checkpointing-checkpoint-request-decider`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `13`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for CheckpointResourcesCleanupRunner

- Case ID: `flink-checkpointing-checkpoint-resources-cleanup-runner`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `18`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for CheckpointStorageLoader

- Case ID: `flink-checkpointing-checkpoint-storage-loader`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `12`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for CheckpointStorageCoordinatorView

- Case ID: `flink-checkpointing-checkpoint-storage-coordinator-view`
- Without K2: combined `0.125`, retrieval `0`, answer `0.25`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.904167`, retrieval `0.933333`, answer `0.875`, safety `1`, passed `True`, results `19`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for StateBackend

- Case ID: `flink-checkpointing-state-backend`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.904167`, retrieval `0.933333`, answer `0.875`, safety `1`, passed `True`, results `16`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for OperatorStateBackend

- Case ID: `flink-checkpointing-operator-state-backend`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.9375`, retrieval `1`, answer `0.875`, safety `1`, passed `True`, results `18`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for KeyedStateBackend

- Case ID: `flink-checkpointing-keyed-state-backend`
- Without K2: combined `0.1875`, retrieval `0`, answer `0.375`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.966667`, retrieval `0.933333`, answer `1`, safety `1`, passed `True`, results `21`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for SavepointRestoreSettings

- Case ID: `flink-checkpointing-savepoint-restore-settings`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `13`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Flink checkpointing pattern for SavepointFormatType

- Case ID: `flink-checkpointing-savepoint-format-type`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.904167`, retrieval `0.933333`, answer `0.875`, safety `1`, passed `True`, results `27`
- MCP tool calls: `{"k2_answer_with_sources": 1, "k2_search_code": 4, "k2_search_docs": 1, "k2_search_tests": 2}`

### Flink checkpointing pattern for CheckpointCoordinatorConfiguration

- Case ID: `flink-checkpointing-checkpoint-coordinator-configuration`
- Without K2: combined `0.125`, retrieval `0`, answer `0.25`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.904167`, retrieval `0.933333`, answer `0.875`, safety `1`, passed `True`, results `20`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for ConnectorPluginsResource

- Case ID: `kafka-rest-connector-plugins-resource`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `11`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for AbstractHerder

- Case ID: `kafka-connect-abstract-herder`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `15`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for DistributedHerder

- Case ID: `kafka-connect-distributed-herder`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `17`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for StandaloneHerder

- Case ID: `kafka-connect-standalone-herder`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `13`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for Herder

- Case ID: `kafka-connect-herder`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.583333`, retrieval `0.666667`, answer `0.5`, safety `1`, passed `False`, results `24`
- MCP tool calls: `{"k2_answer_with_sources": 1, "k2_search_code": 9, "k2_search_docs": 2, "k2_search_tests": 9}`

### Kafka Connect pattern for Worker

- Case ID: `kafka-connect-worker`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.583333`, retrieval `0.666667`, answer `0.5`, safety `1`, passed `False`, results `10`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for WorkerConnector

- Case ID: `kafka-connect-worker-connector`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `15`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for WorkerTask

- Case ID: `kafka-connect-worker-task`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `16`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for WorkerSinkTask

- Case ID: `kafka-connect-worker-sink-task`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `15`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for WorkerSourceTask

- Case ID: `kafka-connect-worker-source-task`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `18`
- MCP tool calls: `{"k2_answer_with_sources": 1, "k2_search_code": 1, "k2_search_tests": 1}`

### Kafka Connect pattern for ConnectorConfig

- Case ID: `kafka-connect-connector-config`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `16`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for SinkConnectorConfig

- Case ID: `kafka-connect-sink-connector-config`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.966667`, retrieval `0.933333`, answer `1`, safety `1`, passed `True`, results `15`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for SourceConnectorConfig

- Case ID: `kafka-connect-source-connector-config`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `16`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for WorkerConfig

- Case ID: `kafka-connect-worker-config`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `17`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for DistributedConfig

- Case ID: `kafka-connect-distributed-config`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `16`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for StandaloneConfig

- Case ID: `kafka-connect-standalone-config`
- Without K2: combined `0.083333`, retrieval `0`, answer `0.166666`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `15`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for ConfigDef

- Case ID: `kafka-connect-config-def`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.55`, retrieval `0.6`, answer `0.5`, safety `1`, passed `False`, results `16`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for ConfigValue

- Case ID: `kafka-connect-config-value`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `17`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for ConfigTransformer

- Case ID: `kafka-connect-config-transformer`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `20`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for ConfigProvider

- Case ID: `kafka-connect-config-provider`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `15`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for Plugins

- Case ID: `kafka-connect-plugins`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.966667`, retrieval `0.933333`, answer `1`, safety `1`, passed `True`, results `13`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for PluginDesc

- Case ID: `kafka-connect-plugin-desc`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `18`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for PluginType

- Case ID: `kafka-connect-plugin-type`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.966667`, retrieval `0.933333`, answer `1`, safety `1`, passed `True`, results `14`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for DelegatingClassLoader

- Case ID: `kafka-connect-delegating-class-loader`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `16`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for PluginClassLoader

- Case ID: `kafka-connect-plugin-class-loader`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.883333`, retrieval `0.933333`, answer `0.833333`, safety `1`, passed `True`, results `14`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for PluginScanResult

- Case ID: `kafka-connect-plugin-scan-result`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.966667`, retrieval `0.933333`, answer `1`, safety `1`, passed `True`, results `14`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for PluginUtils

- Case ID: `kafka-connect-plugin-utils`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `16`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for ConnectRestServer

- Case ID: `kafka-rest-connect-rest-server`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `12`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for RestServerConfig

- Case ID: `kafka-rest-rest-server-config`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `14`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for ConnectorsResource

- Case ID: `kafka-rest-connectors-resource`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `13`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for ConnectorStateInfo

- Case ID: `kafka-rest-connector-state-info`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.916667`, retrieval `1`, answer `0.833333`, safety `1`, passed `True`, results `13`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for ConnectorInfo

- Case ID: `kafka-rest-connector-info`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.916667`, retrieval `1`, answer `0.833333`, safety `1`, passed `True`, results `13`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for CreateConnectorRequest

- Case ID: `kafka-rest-create-connector-request`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.916667`, retrieval `1`, answer `0.833333`, safety `1`, passed `True`, results `12`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for ConnectorType

- Case ID: `kafka-rest-connector-type`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `13`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for Connector

- Case ID: `kafka-connect-connector`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.933333`, retrieval `0.866667`, answer `1`, safety `1`, passed `True`, results `17`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for SourceConnector

- Case ID: `kafka-connect-source-connector`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.966667`, retrieval `0.933333`, answer `1`, safety `1`, passed `True`, results `13`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for SinkConnector

- Case ID: `kafka-connect-sink-connector`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.966667`, retrieval `0.933333`, answer `1`, safety `1`, passed `True`, results `13`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for Transformation

- Case ID: `kafka-connect-transformation`
- Without K2: combined `0.083333`, retrieval `0`, answer `0.166666`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.933333`, retrieval `0.866667`, answer `1`, safety `1`, passed `True`, results `19`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for HeaderConverter

- Case ID: `kafka-connect-header-converter`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.966667`, retrieval `0.933333`, answer `1`, safety `1`, passed `True`, results `16`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for Converter

- Case ID: `kafka-connect-converter`
- Without K2: combined `0.083333`, retrieval `0`, answer `0.166666`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.583333`, retrieval `0.666667`, answer `0.5`, safety `1`, passed `False`, results `13`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for Schema

- Case ID: `kafka-connect-schemas`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.583333`, retrieval `0.666667`, answer `0.5`, safety `1`, passed `False`, results `24`
- MCP tool calls: `{"k2_answer_with_sources": 1, "k2_search_code": 1, "k2_search_tests": 7}`

### Kafka Connect pattern for SchemaBuilder

- Case ID: `kafka-connect-schema-builder`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.966667`, retrieval `0.933333`, answer `1`, safety `1`, passed `True`, results `13`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for Struct

- Case ID: `kafka-connect-struct`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.933333`, retrieval `0.866667`, answer `1`, safety `1`, passed `True`, results `16`
- MCP tool calls: `{"k2_answer_with_sources": 1, "k2_search_tests": 1}`

### Kafka Connect pattern for SinkRecord

- Case ID: `kafka-connect-sink-record`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `13`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for SourceRecord

- Case ID: `kafka-connect-source-record`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.966667`, retrieval `0.933333`, answer `1`, safety `1`, passed `True`, results `14`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for ConnectorClientConfigRequest

- Case ID: `kafka-connect-connector-client-config-request`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.966667`, retrieval `0.933333`, answer `1`, safety `1`, passed `True`, results `18`
- MCP tool calls: `{"k2_answer_with_sources": 1, "k2_search_tests": 1}`

### Kafka Connect pattern for ConnectorClientConfigOverridePolicy

- Case ID: `kafka-connect-connector-client-config-override-policy`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.916667`, retrieval `1`, answer `0.833333`, safety `1`, passed `True`, results `18`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for AbstractConnectorClientConfigOverridePolicy

- Case ID: `kafka-connect-abstract-connector-client-config-override-policy`
- Without K2: combined `0.083333`, retrieval `0`, answer `0.166666`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `0.883333`, retrieval `0.933333`, answer `0.833333`, safety `1`, passed `True`, results `16`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for NoneConnectorClientConfigOverridePolicy

- Case ID: `kafka-connect-none-connector-client-config-override-policy`
- Without K2: combined `0.166667`, retrieval `0`, answer `0.333334`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `17`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

### Kafka Connect pattern for PrincipalConnectorClientConfigOverridePolicy

- Case ID: `kafka-connect-principal-connector-client-config-override-policy`
- Without K2: combined `0.25`, retrieval `0`, answer `0.5`, safety `1`, passed `False`, results `0`
- With real K2 MCP: combined `1`, retrieval `1`, answer `1`, safety `1`, passed `True`, results `16`
- MCP tool calls: `{"k2_answer_with_sources": 1}`

## Demo Interpretation

The real-MCP path demonstrates the customer-facing integration boundary: Codex calls a stdio MCP tool, the tool retrieves version-pinned evidence from K2, and the final answer cites exact docs, source classes, and neighboring tests. The baseline can give generic advice, but it cannot reliably name the same internal artifacts without the K2-backed tool call.
