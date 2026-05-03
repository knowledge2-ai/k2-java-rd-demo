# Blinded LLM-as-Judge Comparison

Generated: `2026-05-03T01:24:06.027965+00:00`

## Method

- The judge saw answer labels `A` and `B`; labels were deterministically randomized per case.
- The judge did not see which answer came from K2 or the baseline until results were mapped back.
- Explicit system identity tokens in answer text were normalized before judging.
- The deterministic evidence-grounding scorecard remains the primary benchmark metric; this is a secondary qualitative preference check.
- The reference checklist came from the published benchmark case metadata, not from either answer.

## Aggregate Judge Results

- Cases judged: `2`
- Winner counts: `{"codex_grep_filesystem": 2}`
- Win rates excluding ties: `{"codex_grep_filesystem": 1.0, "codex_with_k2_mcp_tuned": 0.0}`
- Tie rate: `0.0`
- Mean confidence: `0.685`

## Deterministic Scorecard Context

- `codex_without_k2`: combined `0.135416`, retrieval `0`, answer `0.270833`, safety `1`, passed `0/2`
- `codex_grep_filesystem`: combined `0.7125`, retrieval `0.633333`, answer `0.791667`, safety `1`, passed `0/2`
- `codex_with_k2_mcp_tuned`: combined `0.879167`, retrieval `0.966666`, answer `0.791667`, safety `1`, passed `2/2`
- `codex_with_k2_real_mcp`: combined `0.375`, retrieval `0`, answer `0.75`, safety `1`, passed `0/2`

## Dimension Averages

| Run | Correctness | Grounding | Specificity | Usefulness | Risk |
| --- | ---: | ---: | ---: | ---: | ---: |
| codex_grep_filesystem | `4.0` | `4.5` | `4.5` | `4.5` | `4.0` |
| codex_with_k2_mcp_tuned | `3.0` | `4.0` | `4.0` | `4.0` | `3.0` |

## Per-Question Judge Decisions

### 1. Kafka Connect pattern for Converter (`kafka-connect-converter`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_with_k2_mcp_tuned", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_with_k2_mcp_tuned": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}}`
- Rationale: B correctly identifies that the key/value split is config-time (in configure()), not conversion-time — the fromConnectData/toConnectData logic is symmetric. It grounds on a concrete implementation (StringConverter), correctly notes no StringConverterTest exists, and adds integration tests. A's claim about KEY_CONVERTER_VERSION_CONFIG and VALUE_CONVERTER_VERSION_CONFIG in ConnectorConfig, plus the MultiVersionTest framing around converter loading, carries elevated hallucination risk even if versioned plugins are real in 4.x.

### 2. Flink REST pattern for JobPlanHandler (`flink-rest-job-plan-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_with_k2_mcp_tuned", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_mcp_tuned": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}}`
- Rationale: A introduces a `createJobPlanInfo(executionGraph)` helper method and `getTargetRestEndpointURL()` call that are likely fabricated; Flink handlers at this level typically call `new JobPlanInfo(executionGraph.getPlan())` directly. B's claim matches that simpler pattern and adds concrete `JobPlanInfo.Plan` field names (`jid`, `name`, `type`, `nodes`, `parallelism`, `operator_strategy`, etc.) plus the `RuntimeMessageHeaders` V1 versioning anchor, making it immediately actionable for an engineer modifying the handler or its DTO.
