# LLM Judge Family Comparison

Generated: `2026-05-01T23:28:56.952278+00:00`

## Summary

- Shared cases: `100`
- Left judge: `codex-cli:gpt-5.4-mini`
- Right judge: `claude-cli:sonnet`
- Simple agreement: `0.770`
- Cohen's kappa: `0.424`

| Winner | Left count | Right count |
| --- | ---: | ---: |
| `codex_with_k2_real_mcp` | `71` | `74` |
| `codex_without_k2` | `29` | `26` |

## Disagreements

- Disagreement count: `23`

| Case | Left winner | Right winner | Deterministic baseline | Deterministic K2 |
| --- | --- | --- | ---: | ---: |
| `flink-checkpointing-checkpoint-stats-tracker` | `codex_with_k2_real_mcp` | `codex_without_k2` | `0.1875` | `0.9375` |
| `flink-checkpointing-checkpoint-storage-coordinator-view` | `codex_without_k2` | `codex_with_k2_real_mcp` | `0.125` | `0.904167` |
| `flink-checkpointing-checkpoint-storage-loader` | `codex_with_k2_real_mcp` | `codex_without_k2` | `0.25` | `0.9375` |
| `flink-checkpointing-default-completed-checkpoint-store` | `codex_without_k2` | `codex_with_k2_real_mcp` | `0.125` | `0.9375` |
| `flink-checkpointing-keyed-state-backend` | `codex_without_k2` | `codex_with_k2_real_mcp` | `0.1875` | `0.966667` |
| `flink-checkpointing-state-backend` | `codex_without_k2` | `codex_with_k2_real_mcp` | `0.1875` | `0.904167` |
| `flink-rest-cluster-overview-handler` | `codex_with_k2_real_mcp` | `codex_without_k2` | `0.1875` | `0.904167` |
| `flink-rest-job-config-handler` | `codex_without_k2` | `codex_with_k2_real_mcp` | `0.1875` | `0.9375` |
| `flink-rest-rest-server-endpoint` | `codex_without_k2` | `codex_with_k2_real_mcp` | `0.125` | `0.875` |
| `kafka-connect-abstract-connector-client-config-override-policy` | `codex_without_k2` | `codex_with_k2_real_mcp` | `0.083333` | `0.883333` |
| `kafka-connect-abstract-herder` | `codex_with_k2_real_mcp` | `codex_without_k2` | `0.166667` | `1.0` |
| `kafka-connect-config-def` | `codex_with_k2_real_mcp` | `codex_without_k2` | `0.25` | `0.55` |
| `kafka-connect-distributed-config` | `codex_without_k2` | `codex_with_k2_real_mcp` | `0.166667` | `1.0` |
| `kafka-connect-distributed-herder` | `codex_with_k2_real_mcp` | `codex_without_k2` | `0.25` | `1.0` |
| `kafka-connect-header-converter` | `codex_without_k2` | `codex_with_k2_real_mcp` | `0.166667` | `0.966667` |
| `kafka-connect-plugin-scan-result` | `codex_without_k2` | `codex_with_k2_real_mcp` | `0.25` | `0.966667` |
| `kafka-connect-plugin-type` | `codex_with_k2_real_mcp` | `codex_without_k2` | `0.25` | `0.966667` |
| `kafka-connect-sink-record` | `codex_without_k2` | `codex_with_k2_real_mcp` | `0.25` | `1.0` |
| `kafka-connect-source-connector` | `codex_with_k2_real_mcp` | `codex_without_k2` | `0.25` | `0.966667` |
| `kafka-connect-worker-config` | `codex_without_k2` | `codex_with_k2_real_mcp` | `0.166667` | `1.0` |
| `kafka-connect-worker-task` | `codex_without_k2` | `codex_with_k2_real_mcp` | `0.25` | `1.0` |
| `kafka-rest-connector-info` | `codex_with_k2_real_mcp` | `codex_without_k2` | `0.25` | `0.916667` |
| `kafka-rest-connector-state-info` | `codex_with_k2_real_mcp` | `codex_without_k2` | `0.25` | `0.916667` |

Agreement is computed after each judge's randomized A/B labels are mapped back to run names. The judges still see answer fingerprints such as citations and file paths, so this is a second-family robustness check rather than full human-blind validation.