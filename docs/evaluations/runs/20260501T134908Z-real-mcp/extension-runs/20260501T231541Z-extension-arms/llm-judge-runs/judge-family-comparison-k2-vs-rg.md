# LLM Judge Family Comparison

Generated: `2026-05-02T21:53:40.484923+00:00`

## Summary

- Shared cases: `100`
- Left judge: `codex-cli:gpt-5.4-mini`
- Right judge: `claude-cli:sonnet`
- Simple agreement: `0.570`
- Cohen's kappa: `0.025`

| Winner | Left count | Right count |
| --- | ---: | ---: |
| `codex_grep_filesystem` | `56` | `99` |
| `codex_with_k2_real_mcp` | `44` | `1` |

## Disagreements

- Disagreement count: `43`

| Case | Left winner | Right winner | Deterministic `codex_grep_filesystem` | Deterministic `codex_with_k2_real_mcp` |
| --- | --- | --- | ---: | ---: |
| `flink-checkpointing-checkpoint-failure-manager` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.816667` | `0.875` |
| `flink-checkpointing-checkpoint-metrics` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.754167` | `0.9375` |
| `flink-checkpointing-checkpoint-plan-calculator` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.754167` | `0.9375` |
| `flink-checkpointing-checkpoint-request-decider` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.754167` | `0.9375` |
| `flink-checkpointing-checkpoint-resources-cleanup-runner` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.754167` | `0.9375` |
| `flink-checkpointing-checkpoint-stats-snapshot` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.691667` | `0.9375` |
| `flink-checkpointing-checkpoint-stats-tracker` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.754167` | `0.9375` |
| `flink-checkpointing-checkpoint-storage-loader` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.754167` | `0.9375` |
| `flink-checkpointing-completed-checkpoint` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.754167` | `0.9375` |
| `flink-checkpointing-default-checkpoint-plan-calculator` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.691667` | `0.9375` |
| `flink-checkpointing-operator-state-backend` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.754167` | `0.9375` |
| `flink-checkpointing-savepoint-format-type` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.754167` | `0.904167` |
| `flink-checkpointing-savepoint-restore-settings` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.754167` | `1.0` |
| `flink-rest-cluster-overview-handler` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.754167` | `0.904167` |
| `flink-rest-job-accumulators-handler` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.754167` | `0.904167` |
| `flink-rest-job-cancellation-handler` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.754167` | `1.0` |
| `flink-rest-job-exceptions-handler` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.816667` | `0.9375` |
| `flink-rest-job-plan-handler` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.691667` | `0.966667` |
| `flink-rest-job-vertex-back-pressure-handler` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.754167` | `1.0` |
| `flink-rest-job-vertex-flame-graph-handler` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.754167` | `1.0` |
| `flink-rest-job-vertex-taskmanagers-handler` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.816667` | `0.966667` |
| `flink-rest-taskmanager-details-handler` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.629167` | `0.9375` |
| `kafka-connect-abstract-herder` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.733333` | `1.0` |
| `kafka-connect-config-value` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.85` | `1.0` |
| `kafka-connect-connector` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.691667` | `0.933333` |
| `kafka-connect-connector-client-config-override-policy` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.733333` | `0.916667` |
| `kafka-connect-connector-client-config-request` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.733333` | `0.966667` |
| `kafka-connect-connector-config` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.816667` | `1.0` |
| `kafka-connect-distributed-config` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.816667` | `1.0` |
| `kafka-connect-plugin-desc` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.733333` | `1.0` |
| `kafka-connect-plugin-utils` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.733333` | `1.0` |
| `kafka-connect-principal-connector-client-config-override-policy` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.816667` | `1.0` |
| `kafka-connect-sink-connector-config` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.816667` | `0.966667` |
| `kafka-connect-source-connector` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.733333` | `0.966667` |
| `kafka-connect-source-connector-config` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.816667` | `1.0` |
| `kafka-connect-standalone-config` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.65` | `1.0` |
| `kafka-connect-standalone-herder` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.816667` | `1.0` |
| `kafka-rest-connect-rest-server` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.733333` | `1.0` |
| `kafka-rest-connector-info` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.766667` | `0.916667` |
| `kafka-rest-connector-state-info` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.766667` | `0.916667` |
| `kafka-rest-connector-type` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.816667` | `1.0` |
| `kafka-rest-connectors-resource` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.733333` | `1.0` |
| `kafka-rest-rest-server-config` | `codex_with_k2_real_mcp` | `codex_grep_filesystem` | `0.733333` | `1.0` |

Agreement is computed after each judge's randomized A/B labels are mapped back to run names. The judges still see answer fingerprints such as citations and file paths, so this is a second-family robustness check rather than full human-blind validation.