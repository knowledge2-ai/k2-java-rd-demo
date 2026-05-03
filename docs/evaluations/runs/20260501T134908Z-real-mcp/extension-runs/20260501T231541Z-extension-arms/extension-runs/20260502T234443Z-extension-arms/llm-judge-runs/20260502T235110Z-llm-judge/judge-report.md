# Blinded LLM-as-Judge Comparison

Generated: `2026-05-02T23:52:13.925600+00:00`

## Method

- The judge saw answer labels `A` and `B`; labels were deterministically randomized per case.
- The judge did not see which answer came from K2 or the baseline until results were mapped back.
- Explicit system identity tokens in answer text were normalized before judging.
- The deterministic evidence-grounding scorecard remains the primary benchmark metric; this is a secondary qualitative preference check.
- The reference checklist came from the published benchmark case metadata, not from either answer.

## Aggregate Judge Results

- Cases judged: `2`
- Winner counts: `{"codex_with_k2_mcp_tuned": 2}`
- Win rates excluding ties: `{"codex_grep_filesystem": 0.0, "codex_with_k2_mcp_tuned": 1.0}`
- Tie rate: `0.0`
- Mean confidence: `0.745`

## Deterministic Scorecard Context

- `codex_without_k2`: combined `0.135416`, retrieval `0`, answer `0.270833`, safety `1`, passed `0/2`
- `codex_grep_filesystem`: combined `0.7125`, retrieval `0.633333`, answer `0.791667`, safety `1`, passed `0/2`
- `codex_with_k2_mcp_tuned`: combined `0.89375`, retrieval `0.933333`, answer `0.854167`, safety `1`, passed `2/2`
- `codex_with_k2_real_mcp`: combined `0.375`, retrieval `0`, answer `0.75`, safety `1`, passed `0/2`

## Dimension Averages

| Run | Correctness | Grounding | Specificity | Usefulness | Risk |
| --- | ---: | ---: | ---: | ---: | ---: |
| codex_grep_filesystem | `2.5` | `4.0` | `4.5` | `4.0` | `2.5` |
| codex_with_k2_mcp_tuned | `4.0` | `4.0` | `3.5` | `4.0` | `4.0` |

## Per-Question Judge Decisions

### 1. Kafka Connect pattern for Converter (`kafka-connect-converter`)

- Winner: `codex_with_k2_mcp_tuned`
- Confidence: `0.83`
- Blinded label mapping: `{"A": "codex_with_k2_mcp_tuned", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 2, "grounding": 3, "risk": 2, "specificity": 4, "usefulness": 3}, "codex_with_k2_mcp_tuned": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A is better anchored to Kafka 4.2 versioned docs and the actual Connect runtime/converter split, with a plausible test set and explicit uncertainty. B is more verbose but has a likely wrong source path for StringConverter, relies on source comments instead of version-pinned docs, and mixes in broader tests that are not clearly neighboring to Converter behavior.

### 2. Flink REST pattern for JobPlanHandler (`flink-rest-job-plan-handler`)

- Winner: `codex_with_k2_mcp_tuned`
- Confidence: `0.66`
- Blinded label mapping: `{"A": "codex_with_k2_mcp_tuned", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 5, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_mcp_tuned": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: A is safer and more directly aligned to the question: it anchors the exact `JobPlanHandler`, the versioned REST docs page, and nearby handler tests without overcommitting to an internal call path. B is more detailed, but it likely overstates the implementation flow and leans on broader generator/README anchors instead of the closest REST-handler evidence.
