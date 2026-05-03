# Blinded LLM-as-Judge Comparison

Generated: `2026-05-02T23:53:20.169748+00:00`

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
- Mean confidence: `0.785`

## Deterministic Scorecard Context

- `codex_without_k2`: combined `0.135416`, retrieval `0`, answer `0.270833`, safety `1`, passed `0/2`
- `codex_grep_filesystem`: combined `0.7125`, retrieval `0.633333`, answer `0.791667`, safety `1`, passed `0/2`
- `codex_with_k2_mcp_tuned`: combined `0.89375`, retrieval `0.933333`, answer `0.854167`, safety `1`, passed `2/2`
- `codex_with_k2_real_mcp`: combined `0.375`, retrieval `0`, answer `0.75`, safety `1`, passed `0/2`

## Dimension Averages

| Run | Correctness | Grounding | Specificity | Usefulness | Risk |
| --- | ---: | ---: | ---: | ---: | ---: |
| codex_grep_filesystem | `4.5` | `5.0` | `5.0` | `5.0` | `3.5` |
| codex_with_k2_mcp_tuned | `3.5` | `3.5` | `3.0` | `3.5` | `4.0` |

## Per-Question Judge Decisions

### 1. Kafka Connect pattern for Converter (`kafka-connect-converter`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_with_k2_mcp_tuned", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 4, "grounding": 5, "risk": 3, "specificity": 5, "usefulness": 5}, "codex_with_k2_mcp_tuned": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 3, "usefulness": 4}}`
- Rationale: B is more complete: it adds StringConverter (the canonical key/value-branching example in connect/api), correctly names Plugins.newConverter vs A's newInternalConverter, and anchors config docs in WorkerConfig/ConnectorConfig source rather than external URLs. B's PluginsTest method names and ErrorHandlingTaskTest/MultiVersionTest citations give engineers precise jump points. Line-number specificity raises hallucination risk for B, but the class-level reasoning is sounder.

### 2. Flink REST pattern for JobPlanHandler (`flink-rest-job-plan-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.85`
- Blinded label mapping: `{"A": "codex_with_k2_mcp_tuned", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_mcp_tuned": {"correctness": 3, "grounding": 3, "risk": 4, "specificity": 3, "usefulness": 3}}`
- Rationale: B names the complete class chain (JobPlanHandler → JobPlanHeaders → JobPlanInfo → JsonPlanGenerator → WebMonitorEndpoint registration) with line-anchored source refs, explains the actual handleRequest flow (executionGraph.getPlan() → JobPlanInfo), pins tests to direct serialization coverage (JobPlanInfoTest, JsonGeneratorTest), and correctly surfaces the flink-docs doc-generator path. A omits JobPlanHeaders, JsonPlanGenerator, and WebMonitorEndpoint entirely, and its suggested tests are less directly related. Specific line numbers in B carry some hallucination risk but class names and flow are consistent with Flink 2.x architecture.
