# Blinded LLM-as-Judge Comparison

Generated: `2026-05-03T07:18:13.186882+00:00`

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
- Mean confidence: `0.735`

## Deterministic Scorecard Context

- `codex_without_k2`: combined `0.260416`, retrieval `0`, answer `0.520833`, safety `1`, passed `0/2`
- `codex_grep_filesystem`: combined `0.7125`, retrieval `0.633333`, answer `0.791667`, safety `1`, passed `0/2`
- `codex_with_k2_mcp_tuned`: combined `0.910417`, retrieval `0.966666`, answer `0.854167`, safety `1`, passed `2/2`
- `codex_with_k2_real_mcp`: combined `0.775`, retrieval `0.8`, answer `0.75`, safety `1`, passed `1/2`

## Dimension Averages

| Run | Correctness | Grounding | Specificity | Usefulness | Risk |
| --- | ---: | ---: | ---: | ---: | ---: |
| codex_grep_filesystem | `5.0` | `5.0` | `5.0` | `5.0` | `4.0` |
| codex_with_k2_mcp_tuned | `3.5` | `4.0` | `4.0` | `4.0` | `3.5` |

## Per-Question Judge Decisions

### 1. Kafka Connect pattern for Converter (`kafka-connect-converter`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.72`
- Blinded label mapping: `{"A": "codex_with_k2_mcp_tuned", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_mcp_tuned": {"correctness": 4, "grounding": 4, "risk": 4, "specificity": 4, "usefulness": 4}}`
- Rationale: B is meaningfully better for Kafka Connect 4.2.0 specifically because it anchors on versioned converter infrastructure: MultiVersionTest.testVersionedConverter, PluginRecommenderTest.testConverterVersionRecommenders, and WorkerTest versioned selection paths are directly load-bearing for the version-pinned scope of the question. A omits these entirely. Both correctly identify Plugins.newConverter, WorkerConfig, ConnectorConfig, ConverterType, and the isKey path, but B's test surface is more complete and action-oriented for 4.2.0.

### 2. Flink REST pattern for JobPlanHandler (`flink-rest-job-plan-handler`)

- Winner: `codex_grep_filesystem`
- Confidence: `0.75`
- Blinded label mapping: `{"A": "codex_with_k2_mcp_tuned", "B": "codex_grep_filesystem"}`
- Scores by run: `{"codex_grep_filesystem": {"correctness": 5, "grounding": 5, "risk": 4, "specificity": 5, "usefulness": 5}, "codex_with_k2_mcp_tuned": {"correctness": 3, "grounding": 4, "risk": 3, "specificity": 4, "usefulness": 4}}`
- Rationale: B provides the actual handleRequest() body (new JobPlanInfo(executionGraph.getPlan())), correctly names AccessExecutionGraph.getPlan(), identifies archiveJsonWithPath() for job history, and correctly uses 'jid' as the JSON field name. A incorrectly says 'jobId'. B also surfaces RuntimeRestAPIDocGenerator/RuntimeOpenApiSpecGenerator as the version-pinned docs anchor, adds JobDetailsInfoTest and ArchivedExecutionGraphTest as neighboring tests, and covers the archiving path A omits entirely.
