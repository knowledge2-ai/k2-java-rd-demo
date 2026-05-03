# Extended Benchmark Arms

Generated: `2026-05-02T23:50:49.512339+00:00`

## Summary

- Cases: `2`
- Source roots: `{"flink": "/tmp/k2-java-rd-demo-sources/apache-flink-release-2.2.0", "kafka": "/tmp/k2-java-rd-demo-sources/apache-kafka-4.2"}`

| Run | Combined | Retrieval | Answer | Safety | Passes |
| --- | ---: | ---: | ---: | ---: | ---: |
| codex_without_k2 | `0.135416` | `0` | `0.270833` | `1` | `0/2` |
| codex_grep_filesystem | `0.7125` | `0.633333` | `0.791667` | `1` | `0/2` |
| codex_with_k2_mcp_tuned | `0.89375` | `0.933333` | `0.854167` | `1` | `2/2` |
| codex_with_k2_real_mcp | `0.375` | `0` | `0.75` | `1` | `0/2` |

## Pairwise Deltas vs No-Tool Baseline

| Run | Combined Delta | Retrieval Delta | Answer Delta |
| --- | ---: | ---: | ---: |
| codex_grep_filesystem | `0.577084` | `0.633333` | `0.520834` |
| codex_with_k2_mcp_tuned | `0.758334` | `0.933333` | `0.583334` |
| codex_with_k2_real_mcp | `0.239584` | `0` | `0.479167` |

## Per-Case Results

### Kafka Connect pattern for Converter (`kafka-connect-converter`)

- `codex_without_k2`: combined `0.083333`, retrieval `0`, answer `0.166666`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_mcp_tuned`: combined `0.883333`, retrieval `0.933333`, answer `0.833333`, passed `true`, results `24`
- `codex_with_k2_real_mcp`: combined `0.25`, retrieval `0`, answer `0.5`, passed `false`, results `0`

### Flink REST pattern for JobPlanHandler (`flink-rest-job-plan-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.691667`, retrieval `0.633333`, answer `0.75`, passed `false`, results `1`
- `codex_with_k2_mcp_tuned`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `23`
- `codex_with_k2_real_mcp`: combined `0.5`, retrieval `0`, answer `1`, passed `false`, results `0`
