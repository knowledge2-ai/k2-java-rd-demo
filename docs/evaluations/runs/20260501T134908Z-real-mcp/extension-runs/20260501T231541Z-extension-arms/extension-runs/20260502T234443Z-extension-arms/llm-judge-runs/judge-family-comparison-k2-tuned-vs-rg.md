# LLM Judge Family Comparison

Generated: `2026-05-02T23:55:40.572284+00:00`

## Summary

- Shared cases: `2`
- Left judge: `codex-cli:gpt-5.4-mini`
- Right judge: `claude-cli:sonnet`
- Simple agreement: `0.000`
- Cohen's kappa: `0.000`

| Winner | Left count | Right count |
| --- | ---: | ---: |
| `codex_grep_filesystem` | `0` | `2` |
| `codex_with_k2_mcp_tuned` | `2` | `0` |

## Disagreements

- Disagreement count: `2`

| Case | Left winner | Right winner | Deterministic `codex_grep_filesystem` | Deterministic `codex_with_k2_mcp_tuned` |
| --- | --- | --- | ---: | ---: |
| `flink-rest-job-plan-handler` | `codex_with_k2_mcp_tuned` | `codex_grep_filesystem` | `0.691667` | `0.904167` |
| `kafka-connect-converter` | `codex_with_k2_mcp_tuned` | `codex_grep_filesystem` | `0.733333` | `0.883333` |

Agreement is computed after each judge's randomized A/B labels are mapped back to run names. The judges still see answer fingerprints such as citations and file paths, so this is a second-family robustness check rather than full human-blind validation.