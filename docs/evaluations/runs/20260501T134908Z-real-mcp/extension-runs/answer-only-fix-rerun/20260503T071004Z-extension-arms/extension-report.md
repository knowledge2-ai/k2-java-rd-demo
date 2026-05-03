# Extended Benchmark Arms

Generated: `2026-05-03T07:16:20.093284+00:00`

## Summary

- Cases: `2`
- Source roots: `{"flink": "/tmp/k2-java-rd-demo-sources/apache-flink-release-2.2.0", "kafka": "/tmp/k2-java-rd-demo-sources/apache-kafka-4.2"}`

| Run | Combined | Retrieval | Answer | Safety | Passes |
| --- | ---: | ---: | ---: | ---: | ---: |
| codex_without_k2 | `0.260416` | `0` | `0.520833` | `1` | `0/2` |
| codex_grep_filesystem | `0.7125` | `0.633333` | `0.791667` | `1` | `0/2` |
| codex_with_k2_mcp_tuned | `0.910417` | `0.966666` | `0.854167` | `1` | `2/2` |
| codex_with_k2_real_mcp | `0.775` | `0.8` | `0.75` | `1` | `1/2` |

## Pairwise Deltas vs No-Tool Baseline

| Run | Combined Delta | Retrieval Delta | Answer Delta |
| --- | ---: | ---: | ---: |
| codex_grep_filesystem | `0.452084` | `0.633333` | `0.270834` |
| codex_with_k2_mcp_tuned | `0.650001` | `0.966666` | `0.333334` |
| codex_with_k2_real_mcp | `0.514584` | `0.8` | `0.229167` |

## Per-Case Results

### Kafka Connect pattern for Converter (`kafka-connect-converter`)

- `codex_without_k2`: combined `0.333333`, retrieval `0`, answer `0.666667`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.733333`, retrieval `0.633333`, answer `0.833333`, passed `false`, results `1`
- `codex_with_k2_mcp_tuned`: combined `0.916667`, retrieval `1`, answer `0.833333`, passed `true`, results `37`
- `codex_with_k2_real_mcp`: combined `0.583333`, retrieval `0.666667`, answer `0.5`, passed `false`, results `13`

### Flink REST pattern for JobPlanHandler (`flink-rest-job-plan-handler`)

- `codex_without_k2`: combined `0.1875`, retrieval `0`, answer `0.375`, passed `false`, results `0`
- `codex_grep_filesystem`: combined `0.691667`, retrieval `0.633333`, answer `0.75`, passed `false`, results `1`
- `codex_with_k2_mcp_tuned`: combined `0.904167`, retrieval `0.933333`, answer `0.875`, passed `true`, results `40`
- `codex_with_k2_real_mcp`: combined `0.966667`, retrieval `0.933333`, answer `1`, passed `true`, results `23`
