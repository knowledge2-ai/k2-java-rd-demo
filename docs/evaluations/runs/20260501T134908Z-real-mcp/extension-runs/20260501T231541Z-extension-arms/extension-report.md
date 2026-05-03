# Extended Benchmark Arms

Generated: `2026-05-02T00:00:54.292937+00:00`

## Summary

- Cases: `100`
- Source roots: `{"flink": "/tmp/k2-java-rd-demo-sources/apache-flink-release-2.2.0", "kafka": "/tmp/k2-java-rd-demo-sources/apache-kafka-4.2"}`

| Run | Combined | Retrieval | Answer | Safety | Passes |
| --- | ---: | ---: | ---: | ---: | ---: |
| codex_without_k2 | `0.189375` | `0` | `0.37875` | `1` | `0/100` |
| codex_grep_filesystem | `0.754083` | `0.637333` | `0.870833` | `1` | `2/100` |
| codex_with_k2_real_mcp | `0.928875` | `0.954` | `0.90375` | `1` | `93/100` |

## Pairwise Deltas vs No-Tool Baseline

| Run | Combined Delta | Retrieval Delta | Answer Delta |
| --- | ---: | ---: | ---: |
| codex_grep_filesystem | `0.564708` | `0.637333` | `0.492083` |
| codex_with_k2_real_mcp | `0.7395` | `0.954` | `0.525` |

## LLM-Judge Check: K2 vs `rg`

Two partially blinded judge families scored the 100 K2-vs-`rg` answer pairs
from this extension run:

| Judge | K2 Wins | `rg` Wins | Ties | Mean Confidence |
| --- | ---: | ---: | ---: | ---: |
| Codex CLI / OpenAI-family | `44` | `56` | `0` | `0.8001` |
| Claude Code / Anthropic-family | `1` | `99` | `0` | `0.8308` |

This is a negative finding for any claim that the K2 answer text was preferred
over the fair retrieval-capable baseline. The deterministic scorecard still
shows stronger K2 source coverage, but answer preference and source-grounding
coverage should be reported separately.

## Per-Case Results

### Flink REST pattern for DispatcherRestEndpoint (`flink-rest-dispatcher-rest-endpoint`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.841667`, retrieval `0.933333`, answer `0.75`, passed `true`, results `22`

### Flink REST pattern for WebMonitorEndpoint (`flink-rest-web-monitor-endpoint`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.875`, retrieval `1`, answer `0.75`, passed `true`, results `24`

### Flink REST pattern for RestServerEndpoint (`flink-rest-rest-server-endpoint`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.629167`, retrieval `0.633333`, answer `0.625`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.875`, retrieval `1`, answer `0.75`, passed `true`, results `15`

### Flink REST pattern for AbstractRestHandler (`flink-rest-abstract-rest-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `21`

### Flink REST pattern for JobDetailsHandler (`flink-rest-job-details-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.629167`, retrieval `0.633333`, answer `0.625`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `22`

### Flink REST pattern for JobConfigHandler (`flink-rest-job-config-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `21`

### Flink REST pattern for JobExceptionsHandler (`flink-rest-job-exceptions-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `23`

### Flink REST pattern for JobAccumulatorsHandler (`flink-rest-job-accumulators-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `21`

### Flink REST pattern for JobPlanHandler (`flink-rest-job-plan-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.691667`, retrieval `0.633333`, answer `0.75`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `23`

### Flink REST pattern for JobVertexDetailsHandler (`flink-rest-job-vertex-details-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `19`

### Flink REST pattern for JobVertexTaskManagersHandler (`flink-rest-job-vertex-taskmanagers-handler`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `20`

### Flink REST pattern for JobCancellationHandler (`flink-rest-job-cancellation-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `17`

### Flink REST pattern for SavepointHandlers (`flink-rest-savepoint-handlers`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.808333`, retrieval `0.866667`, answer `0.75`, passed `false`, results `6`

### Flink REST pattern for CheckpointHandlers (`flink-rest-checkpoint-handlers`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.691667`, retrieval `0.633333`, answer `0.75`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.6125`, retrieval `0.6`, answer `0.625`, passed `false`, results `6`

### Flink REST pattern for JobResourceRequirementsUpdateHandler (`flink-rest-job-resource-requirements-update-handler`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.629167`, retrieval `0.633333`, answer `0.625`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.841667`, retrieval `0.933333`, answer `0.75`, passed `true`, results `22`

### Flink REST pattern for JobSubmitHandler (`flink-rest-job-submit-handler`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.875`, retrieval `1`, answer `0.75`, passed `true`, results `20`

### Flink REST pattern for FileUploads (`flink-rest-file-uploads`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.691667`, retrieval `0.633333`, answer `0.75`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `20`

### Flink REST pattern for DashboardConfigHandler (`flink-rest-dashboard-config-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `20`

### Flink REST pattern for ClusterOverviewHandler (`flink-rest-cluster-overview-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `19`

### Flink REST pattern for TaskManagersHandler (`flink-rest-taskmanagers-handler`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `18`

### Flink REST pattern for TaskManagerDetailsHandler (`flink-rest-taskmanager-details-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.629167`, retrieval `0.633333`, answer `0.625`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `20`

### Flink REST pattern for JobVertexBackPressureHandler (`flink-rest-job-vertex-back-pressure-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `15`

### Flink REST pattern for JobVertexWatermarksHandler (`flink-rest-job-vertex-watermarks-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.629167`, retrieval `0.633333`, answer `0.625`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `18`

### Flink REST pattern for SubtaskCurrentAttemptDetailsHandler (`flink-rest-subtask-current-attempt-details-handler`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `21`

### Flink REST pattern for JobVertexFlameGraphHandler (`flink-rest-job-vertex-flame-graph-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `21`

### Flink checkpointing pattern for CheckpointCoordinator (`flink-checkpointing-checkpoint-coordinator`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `17`

### Flink checkpointing pattern for PendingCheckpoint (`flink-checkpointing-pending-checkpoint`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `11`

### Flink checkpointing pattern for CompletedCheckpoint (`flink-checkpointing-completed-checkpoint`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `17`

### Flink checkpointing pattern for CompletedCheckpointStore (`flink-checkpointing-completed-checkpoint-store`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `21`

### Flink checkpointing pattern for DefaultCompletedCheckpointStore (`flink-checkpointing-default-completed-checkpoint-store`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `36`

### Flink checkpointing pattern for CheckpointStatsTracker (`flink-checkpointing-checkpoint-stats-tracker`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `23`

### Flink checkpointing pattern for CheckpointStatsSnapshot (`flink-checkpointing-checkpoint-stats-snapshot`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.691667`, retrieval `0.633333`, answer `0.75`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `19`

### Flink checkpointing pattern for CheckpointMetrics (`flink-checkpointing-checkpoint-metrics`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `17`

### Flink checkpointing pattern for CheckpointProperties (`flink-checkpointing-checkpoint-properties`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `16`

### Flink checkpointing pattern for CheckpointRetentionPolicy (`flink-checkpointing-checkpoint-retention-policy`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `19`

### Flink checkpointing pattern for CheckpointIDCounter (`flink-checkpointing-checkpoint-id-counter`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `21`

### Flink checkpointing pattern for StandaloneCheckpointIDCounter (`flink-checkpointing-standalone-checkpoint-id-counter`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `17`

### Flink checkpointing pattern for CheckpointFailureManager (`flink-checkpointing-checkpoint-failure-manager`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.875`, retrieval `1`, answer `0.75`, passed `true`, results `21`

### Flink checkpointing pattern for CheckpointPlanCalculator (`flink-checkpointing-checkpoint-plan-calculator`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `22`

### Flink checkpointing pattern for DefaultCheckpointPlanCalculator (`flink-checkpointing-default-checkpoint-plan-calculator`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.691667`, retrieval `0.633333`, answer `0.75`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `22`

### Flink checkpointing pattern for CheckpointRequestDecider (`flink-checkpointing-checkpoint-request-decider`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `13`

### Flink checkpointing pattern for CheckpointResourcesCleanupRunner (`flink-checkpointing-checkpoint-resources-cleanup-runner`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `18`

### Flink checkpointing pattern for CheckpointStorageLoader (`flink-checkpointing-checkpoint-storage-loader`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `12`

### Flink checkpointing pattern for CheckpointStorageCoordinatorView (`flink-checkpointing-checkpoint-storage-coordinator-view`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `19`

### Flink checkpointing pattern for StateBackend (`flink-checkpointing-state-backend`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `16`

### Flink checkpointing pattern for OperatorStateBackend (`flink-checkpointing-operator-state-backend`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `18`

### Flink checkpointing pattern for KeyedStateBackend (`flink-checkpointing-keyed-state-backend`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `21`

### Flink checkpointing pattern for SavepointRestoreSettings (`flink-checkpointing-savepoint-restore-settings`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `13`

### Flink checkpointing pattern for SavepointFormatType (`flink-checkpointing-savepoint-format-type`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.754167`, retrieval `0.633333`, answer `0.875`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `27`

### Flink checkpointing pattern for CheckpointCoordinatorConfiguration (`flink-checkpointing-checkpoint-coordinator-configuration`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `20`

### Kafka Connect pattern for ConnectorPluginsResource (`kafka-rest-connector-plugins-resource`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `11`

### Kafka Connect pattern for AbstractHerder (`kafka-connect-abstract-herder`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `15`

### Kafka Connect pattern for DistributedHerder (`kafka-connect-distributed-herder`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.65`, retrieval `0.633333`, answer `0.666667`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `17`

### Kafka Connect pattern for StandaloneHerder (`kafka-connect-standalone-herder`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `13`

### Kafka Connect pattern for Herder (`kafka-connect-herder`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.583333`, retrieval `0.666667`, answer `0.5`, passed `false`, results `24`

### Kafka Connect pattern for Worker (`kafka-connect-worker`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.583333`, retrieval `0.666667`, answer `0.5`, passed `false`, results `10`

### Kafka Connect pattern for WorkerConnector (`kafka-connect-worker-connector`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `15`

### Kafka Connect pattern for WorkerTask (`kafka-connect-worker-task`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `16`

### Kafka Connect pattern for WorkerSinkTask (`kafka-connect-worker-sink-task`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.65`, retrieval `0.633333`, answer `0.666667`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `15`

### Kafka Connect pattern for WorkerSourceTask (`kafka-connect-worker-source-task`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `18`

### Kafka Connect pattern for ConnectorConfig (`kafka-connect-connector-config`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `16`

### Kafka Connect pattern for SinkConnectorConfig (`kafka-connect-sink-connector-config`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `15`

### Kafka Connect pattern for SourceConnectorConfig (`kafka-connect-source-connector-config`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `16`

### Kafka Connect pattern for WorkerConfig (`kafka-connect-worker-config`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `17`

### Kafka Connect pattern for DistributedConfig (`kafka-connect-distributed-config`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `16`

### Kafka Connect pattern for StandaloneConfig (`kafka-connect-standalone-config`)

- `codex_without_k2`: combined `0.083333`, retrieval `0`, answer `0.166666`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.65`, retrieval `0.633333`, answer `0.666667`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `15`

### Kafka Connect pattern for ConfigDef (`kafka-connect-config-def`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.766667`, retrieval `0.7`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.55`, retrieval `0.6`, answer `0.5`, passed `false`, results `16`

### Kafka Connect pattern for ConfigValue (`kafka-connect-config-value`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.85`, retrieval `0.7`, answer `1`, passed `true`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `17`

### Kafka Connect pattern for ConfigTransformer (`kafka-connect-config-transformer`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.766667`, retrieval `0.7`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `20`

### Kafka Connect pattern for ConfigProvider (`kafka-connect-config-provider`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.85`, retrieval `0.7`, answer `1`, passed `true`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `15`

### Kafka Connect pattern for Plugins (`kafka-connect-plugins`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `13`

### Kafka Connect pattern for PluginDesc (`kafka-connect-plugin-desc`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `18`

### Kafka Connect pattern for PluginType (`kafka-connect-plugin-type`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `14`

### Kafka Connect pattern for DelegatingClassLoader (`kafka-connect-delegating-class-loader`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `16`

### Kafka Connect pattern for PluginClassLoader (`kafka-connect-plugin-class-loader`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.883333`, retrieval `0.933333`, answer `0.833333`, passed `true`, results `14`

### Kafka Connect pattern for PluginScanResult (`kafka-connect-plugin-scan-result`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `14`

### Kafka Connect pattern for PluginUtils (`kafka-connect-plugin-utils`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `16`

### Kafka Connect pattern for ConnectRestServer (`kafka-rest-connect-rest-server`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `12`

### Kafka Connect pattern for RestServerConfig (`kafka-rest-rest-server-config`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `14`

### Kafka Connect pattern for ConnectorsResource (`kafka-rest-connectors-resource`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `13`

### Kafka Connect pattern for ConnectorStateInfo (`kafka-rest-connector-state-info`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.766667`, retrieval `0.7`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.916667`, retrieval `1`, answer `0.833333`, passed `true`, results `13`

### Kafka Connect pattern for ConnectorInfo (`kafka-rest-connector-info`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.766667`, retrieval `0.7`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.916667`, retrieval `1`, answer `0.833333`, passed `true`, results `13`

### Kafka Connect pattern for CreateConnectorRequest (`kafka-rest-create-connector-request`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.916667`, retrieval `1`, answer `0.833333`, passed `true`, results `12`

### Kafka Connect pattern for ConnectorType (`kafka-rest-connector-type`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `13`

### Kafka Connect pattern for Connector (`kafka-connect-connector`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.691667`, retrieval `0.633333`, answer `0.75`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.933333`, retrieval `0.866667`, answer `1`, passed `true`, results `17`

### Kafka Connect pattern for SourceConnector (`kafka-connect-source-connector`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `13`

### Kafka Connect pattern for SinkConnector (`kafka-connect-sink-connector`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `13`

### Kafka Connect pattern for Transformation (`kafka-connect-transformation`)

- `codex_without_k2`: combined `0.083333`, retrieval `0`, answer `0.166666`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.933333`, retrieval `0.866667`, answer `1`, passed `true`, results `19`

### Kafka Connect pattern for HeaderConverter (`kafka-connect-header-converter`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `16`

### Kafka Connect pattern for Converter (`kafka-connect-converter`)

- `codex_without_k2`: combined `0.083333`, retrieval `0`, answer `0.166666`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.583333`, retrieval `0.666667`, answer `0.5`, passed `false`, results `13`

### Kafka Connect pattern for Schema (`kafka-connect-schemas`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.691667`, retrieval `0.633333`, answer `0.75`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.583333`, retrieval `0.666667`, answer `0.5`, passed `false`, results `24`

### Kafka Connect pattern for SchemaBuilder (`kafka-connect-schema-builder`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `13`

### Kafka Connect pattern for Struct (`kafka-connect-struct`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.933333`, retrieval `0.866667`, answer `1`, passed `true`, results `16`

### Kafka Connect pattern for SinkRecord (`kafka-connect-sink-record`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `13`

### Kafka Connect pattern for SourceRecord (`kafka-connect-source-record`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `14`

### Kafka Connect pattern for ConnectorClientConfigRequest (`kafka-connect-connector-client-config-request`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `18`

### Kafka Connect pattern for ConnectorClientConfigOverridePolicy (`kafka-connect-connector-client-config-override-policy`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.916667`, retrieval `1`, answer `0.833333`, passed `true`, results `18`

### Kafka Connect pattern for AbstractConnectorClientConfigOverridePolicy (`kafka-connect-abstract-connector-client-config-override-policy`)

- `codex_without_k2`: combined `0.083333`, retrieval `0`, answer `0.166666`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.65`, retrieval `0.633333`, answer `0.666667`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `0.883333`, retrieval `0.933333`, answer `0.833333`, passed `true`, results `16`

### Kafka Connect pattern for NoneConnectorClientConfigOverridePolicy (`kafka-connect-none-connector-client-config-override-policy`)

- `codex_without_k2`: combined `0.166667`, retrieval `0`, answer `0.333334`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `17`

### Kafka Connect pattern for PrincipalConnectorClientConfigOverridePolicy (`kafka-connect-principal-connector-client-config-override-policy`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.816667`, retrieval `0.633333`, answer `1`, passed `false`, results `1`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `16`
