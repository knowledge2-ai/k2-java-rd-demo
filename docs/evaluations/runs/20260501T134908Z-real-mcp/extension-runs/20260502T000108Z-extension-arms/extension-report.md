# Extended Benchmark Arms

Generated: `2026-05-02T00:25:37.510584+00:00`

## Summary

- Cases: `20`
- Source roots: `{"flink": "/tmp/k2-java-rd-demo-sources/apache-flink-release-2.2.0", "kafka": "/tmp/k2-java-rd-demo-sources/apache-kafka-4.2"}`

| Run | Combined | Retrieval | Answer | Safety | Passes |
| --- | ---: | ---: | ---: | ---: | ---: |
| codex_without_k2 | `0.175` | `0` | `0.35` | `1` | `0/20` |
| codex_with_k2_mcp_no_skill | `0.888333` | `0.901667` | `0.875` | `1` | `18/20` |
| codex_with_k2_mcp_filters_off | `0.898125` | `0.94` | `0.85625` | `1` | `19/20` |
| codex_with_k2_real_mcp | `0.891875` | `0.94` | `0.84375` | `1` | `18/20` |

## Pairwise Deltas vs No-Tool Baseline

| Run | Combined Delta | Retrieval Delta | Answer Delta |
| --- | ---: | ---: | ---: |
| codex_with_k2_mcp_no_skill | `0.713333` | `0.901667` | `0.525` |
| codex_with_k2_mcp_filters_off | `0.723125` | `0.94` | `0.50625` |
| codex_with_k2_real_mcp | `0.716875` | `0.94` | `0.49375` |

## Per-Case Results

### Flink REST pattern for DispatcherRestEndpoint (`flink-rest-dispatcher-rest-endpoint`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.841667`, retrieval `0.933333`, answer `0.75`, passed `true`, results `31`
- `codex_with_k2_mcp_filters_off`: combined `0.841667`, retrieval `0.933333`, answer `0.75`, passed `true`, results `49`
- `codex_with_k2_real_mcp`: combined `0.841667`, retrieval `0.933333`, answer `0.75`, passed `true`, results `22`

### Flink REST pattern for WebMonitorEndpoint (`flink-rest-web-monitor-endpoint`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `17`
- `codex_with_k2_mcp_filters_off`: combined `0.491667`, retrieval `0.733333`, answer `0.25`, passed `false`, results `48`
- `codex_with_k2_real_mcp`: combined `0.875`, retrieval `1`, answer `0.75`, passed `true`, results `24`

### Flink REST pattern for RestServerEndpoint (`flink-rest-rest-server-endpoint`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.875`, retrieval `1`, answer `0.75`, passed `true`, results `16`
- `codex_with_k2_mcp_filters_off`: combined `0.875`, retrieval `1`, answer `0.75`, passed `true`, results `51`
- `codex_with_k2_real_mcp`: combined `0.875`, retrieval `1`, answer `0.75`, passed `true`, results `15`

### Flink REST pattern for AbstractRestHandler (`flink-rest-abstract-rest-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `30`
- `codex_with_k2_mcp_filters_off`: combined `0.870833`, retrieval `0.866667`, answer `0.875`, passed `true`, results `76`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `21`

### Flink REST pattern for JobDetailsHandler (`flink-rest-job-details-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `25`
- `codex_with_k2_mcp_filters_off`: combined `0.875`, retrieval `1`, answer `0.75`, passed `true`, results `45`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `22`

### Flink REST pattern for JobConfigHandler (`flink-rest-job-config-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `18`
- `codex_with_k2_mcp_filters_off`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `52`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `21`

### Flink REST pattern for JobExceptionsHandler (`flink-rest-job-exceptions-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `41`
- `codex_with_k2_mcp_filters_off`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `51`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `23`

### Flink REST pattern for JobAccumulatorsHandler (`flink-rest-job-accumulators-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.870833`, retrieval `0.866667`, answer `0.875`, passed `true`, results `33`
- `codex_with_k2_mcp_filters_off`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `74`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `21`

### Flink REST pattern for JobPlanHandler (`flink-rest-job-plan-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `27`
- `codex_with_k2_mcp_filters_off`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `79`
- `codex_with_k2_real_mcp`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `23`

### Flink REST pattern for JobVertexDetailsHandler (`flink-rest-job-vertex-details-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.558333`, retrieval `0.366667`, answer `0.75`, passed `false`, results `1`
- `codex_with_k2_mcp_filters_off`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `58`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `19`

### Flink REST pattern for JobVertexTaskManagersHandler (`flink-rest-job-vertex-taskmanagers-handler`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `42`
- `codex_with_k2_mcp_filters_off`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `54`
- `codex_with_k2_real_mcp`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `20`

### Flink REST pattern for JobCancellationHandler (`flink-rest-job-cancellation-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `36`
- `codex_with_k2_mcp_filters_off`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `56`
- `codex_with_k2_real_mcp`: combined `1`, retrieval `1`, answer `1`, passed `true`, results `17`

### Flink REST pattern for SavepointHandlers (`flink-rest-savepoint-handlers`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.7875`, retrieval `0.7`, answer `0.875`, passed `false`, results `3`
- `codex_with_k2_mcp_filters_off`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `53`
- `codex_with_k2_real_mcp`: combined `0.808333`, retrieval `0.866667`, answer `0.75`, passed `false`, results `6`

### Flink REST pattern for CheckpointHandlers (`flink-rest-checkpoint-handlers`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `27`
- `codex_with_k2_mcp_filters_off`: combined `0.870833`, retrieval `0.866667`, answer `0.875`, passed `true`, results `57`
- `codex_with_k2_real_mcp`: combined `0.6125`, retrieval `0.6`, answer `0.625`, passed `false`, results `6`

### Flink REST pattern for JobResourceRequirementsUpdateHandler (`flink-rest-job-resource-requirements-update-handler`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.841667`, retrieval `0.933333`, answer `0.75`, passed `true`, results `33`
- `codex_with_k2_mcp_filters_off`: combined `0.841667`, retrieval `0.933333`, answer `0.75`, passed `true`, results `99`
- `codex_with_k2_real_mcp`: combined `0.841667`, retrieval `0.933333`, answer `0.75`, passed `true`, results `22`

### Flink REST pattern for JobSubmitHandler (`flink-rest-job-submit-handler`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.820833`, retrieval `0.766667`, answer `0.875`, passed `true`, results `2`
- `codex_with_k2_mcp_filters_off`: combined `0.875`, retrieval `1`, answer `0.75`, passed `true`, results `59`
- `codex_with_k2_real_mcp`: combined `0.875`, retrieval `1`, answer `0.75`, passed `true`, results `20`

### Flink REST pattern for FileUploads (`flink-rest-file-uploads`)

- `codex_without_k2`: combined `0.125`, retrieval `0`, answer `0.25`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.875`, retrieval `1`, answer `0.75`, passed `true`, results `28`
- `codex_with_k2_mcp_filters_off`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `57`
- `codex_with_k2_real_mcp`: combined `0.9375`, retrieval `1`, answer `0.875`, passed `true`, results `20`

### Flink REST pattern for DashboardConfigHandler (`flink-rest-dashboard-config-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `20`
- `codex_with_k2_mcp_filters_off`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `63`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `20`

### Flink REST pattern for ClusterOverviewHandler (`flink-rest-cluster-overview-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `19`
- `codex_with_k2_mcp_filters_off`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `53`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `19`

### Flink REST pattern for TaskManagersHandler (`flink-rest-taskmanagers-handler`)

- `codex_without_k2`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`
- `codex_with_k2_mcp_no_skill`: combined `0.870833`, retrieval `0.866667`, answer `0.875`, passed `true`, results `30`
- `codex_with_k2_mcp_filters_off`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `60`
- `codex_with_k2_real_mcp`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `18`
