# Blinded LLM-as-Judge Comparison

Generated: `2026-05-03T01:27:07.367127+00:00`

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
- Mean confidence: `0.685`

## Deterministic Scorecard Context

- `codex_without_k2`: combined `0.135416`, retrieval `0`, answer `0.270833`, safety `1`, passed `0/2`
- `codex_grep_filesystem`: combined `0.7125`, retrieval `0.633333`, answer `0.791667`, safety `1`, passed `0/2`
- `codex_with_k2_mcp_tuned`: combined `0.879167`, retrieval `0.966666`, answer `0.791667`, safety `1`, passed `2/2`
- `codex_with_k2_real_mcp`: combined `0.375`, retrieval `0`, answer `0.75`, safety `1`, passed `0/2`

## Dimension Averages

| Run | Correctness | Grounding | Specificity | Usefulness | Risk |
| --- | ---: | ---: | ---: | ---: | ---: |
| codex_grep_filesystem | `4.0` | `3.0` | `4.5` | `4.0` | `4.0` |
| codex_with_k2_mcp_tuned | `5.0` | `5.0` | `5.0` | `5.0` | `4.5` |

## Per-Question Judge Decisions

### 1. Kafka Connect pattern for Converter (`kafka-connect-converter`)

- Winner: `codex_with_k2_mcp_tuned`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_with_k2_mcp_tuned", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 4, "usefulness": 4}, "codex_with_k2_mcp_tuned": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}}`
- Rationale: A is better grounded: its Plugins.newConverter citation is confirmed by the evidence snippet showing isKeyConverter detection and classPropertyName prefix logic. A also surfaces ConnectorConfig validators, ConverterType enum, MultiVersionTest, and WorkerConfig config keys—all precise, version-pinned anchors. B is technically sound but its evidence is nearly empty (only a stub Converter.java entry), and its StringConverter focus narrows scope unnecessarily. B's claim about no StringConverterTest existing is unverifiable and adds marginal value.

### 2. Flink REST pattern for JobPlanHandler (`flink-rest-job-plan-handler`)

- Winner: `codex_with_k2_mcp_tuned`
- Confidence: `0.65`
- Blinded label mapping: `{"A": "codex_with_k2_mcp_tuned", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 3, "risk": 4, "specificity": 5, "usefulness": 4}, "codex_with_k2_mcp_tuned": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}}`
- Rationale: Evidence confirms A's two-step flow: `handleRequest()` → `createJobPlanInfo(executionGraph)` → `new JobPlanInfo(...)`. B collapses this by stating `handleRequest()` directly returns `new JobPlanInfo(executionGraph.getPlan())`, skipping the helper and slightly misrepresenting the indirection. A's evidence base is materially stronger: multiple confirmed code snippets vs. B's stub-only evidence. B adds useful versioning detail via `RuntimeMessageHeaders` but its grounding is unconfirmed.
