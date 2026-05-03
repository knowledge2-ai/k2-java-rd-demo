# Blinded LLM-as-Judge Comparison

Generated: `2026-05-03T07:19:47.609859+00:00`

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
- Mean confidence: `0.785`

## Deterministic Scorecard Context

- `codex_without_k2`: combined `0.260416`, retrieval `0`, answer `0.520833`, safety `1`, passed `0/2`
- `codex_grep_filesystem`: combined `0.7125`, retrieval `0.633333`, answer `0.791667`, safety `1`, passed `0/2`
- `codex_with_k2_mcp_tuned`: combined `0.910417`, retrieval `0.966666`, answer `0.854167`, safety `1`, passed `2/2`
- `codex_with_k2_real_mcp`: combined `0.775`, retrieval `0.8`, answer `0.75`, safety `1`, passed `1/2`

## Dimension Averages

| Run | Correctness | Grounding | Specificity | Usefulness | Risk |
| --- | ---: | ---: | ---: | ---: | ---: |
| codex_grep_filesystem | `3.5` | `2.5` | `4.0` | `4.0` | `3.0` |
| codex_with_k2_mcp_tuned | `5.0` | `4.5` | `4.5` | `4.5` | `4.5` |

## Per-Question Judge Decisions

### 1. Kafka Connect pattern for Converter (`kafka-connect-converter`)

- Winner: `codex_with_k2_mcp_tuned`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_with_k2_mcp_tuned", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 2, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_with_k2_mcp_tuned": {"correctness": 5, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: A's core claims are directly confirmed by evidence snippets: Plugins.java L463 showing isKeyConverter derivation, BooleanConverter showing ConverterType.KEY/VALUE usage, ConnectorConfig and Plugins snippets. B cites MultiVersionTest.testVersionedConverter, PluginRecommenderTest.testConverterVersionRecommenders, and WorkerTest versioned methods — plausible but unverified by its single thin evidence entry. B's grounding is severely weakened by having only one evidence snippet with no code content.

### 2. Flink REST pattern for JobPlanHandler (`flink-rest-job-plan-handler`)

- Winner: `codex_with_k2_mcp_tuned`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_with_k2_mcp_tuned", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 3, "grounding": 3, "risk": 3, "specificity": 4, "usefulness": 4}, "codex_with_k2_mcp_tuned": {"correctness": 5, "grounding": 5, "risk": 5, "specificity": 5, "usefulness": 5}}`
- Rationale: A correctly identifies `handleRequest` delegates to `createJobPlanInfo(executionGraph)` (confirmed by evidence L60-63). B fabricates `new JobPlanInfo(executionGraph.getPlan())` — no such direct call exists in evidence. A cites the live Flink 2.2 REST docs page with the actual `/jobs/:jobid/plan` contract. B substitutes doc-generator classes as the docs anchor, which is less actionable. A's claims are all supported by provided evidence snippets; B's evidence is a single class-name stub.
