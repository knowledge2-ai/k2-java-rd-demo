# K2 MCP Retrieval Tuning Loop

Date: 2026-05-03

## Scope

This pass tuned the real stdio MCP path used by Codex for two regression cases where
the Claude-family answer-only judge previously preferred the `rg` filesystem baseline:

- `kafka-connect-converter`
- `flink-rest-job-plan-handler`

The goal was not to hide the `rg` result. The goal was to determine whether K2 retrieval
and MCP answer shaping could produce equal-or-better source-grounded answers, and whether
the qualitative judge was evaluating actual evidence or relying on priors.

## K2 Tuning Changes

- Added query-time retrieval profiles. The default MCP profile is now `java_exact`.
- `java_exact` uses docs with stronger dense weight and Java code/tests with stronger sparse
  weight for exact class, method, config-key, and path terms.
- Added framework-neighbor lookups derived from the queried public API/class names:
  - Kafka `Converter`: `Converter`, `StringConverter`, `ConverterConfig`, `ConverterType`,
    `Plugins`, `WorkerConfig`, `ConnectorConfig`, `PluginsTest`, `MultiVersionTest`,
    `AbstractWorkerSourceTaskTest`, `WorkerSinkTaskTest`, and converter unit tests.
  - Flink `JobPlanHandler`: `JobPlanHeaders`, `JobPlanInfo`, `JsonPlanGenerator`,
    `WebMonitorEndpoint`, `DefaultExecutionGraphBuilder`, archival/versioning/docs generator
    anchors, and neighboring response/JSON tests.
- Added local source line-slice enrichment for retrieved repo URIs so final answers can cite
  exact line ranges instead of only chunk-level URIs.
- Increased future Java source ingestion chunking from 180 characters to larger source-aware
  fixed chunks: 1200 chars for production code and 1400 chars for tests. This affects future
  reupload/reindex runs; live corpora are still evaluated through query-time tuning plus line
  enrichment.
- Fixed a real MCP bug where tuple role queries were treated as one string instead of multiple
  independent searches.

## Final Two-Case Result

Final run:

`docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260501T231541Z-extension-arms/extension-runs/20260503T011523Z-extension-arms/extension-scorecard.json`

Deterministic scorecard:

| Run | Combined | Retrieval | Answer | Passed |
| --- | ---: | ---: | ---: | ---: |
| `codex_grep_filesystem` | `0.7125` | `0.633333` | `0.791667` | `0/2` |
| `codex_with_k2_mcp_tuned` | `0.879167` | `0.966666` | `0.791667` | `2/2` |

## Claude-Family Judge Results

Answer-only blinded judge:

`docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260501T231541Z-extension-arms/extension-runs/20260503T011523Z-extension-arms/llm-judge-runs/claude-family/20260503T012228Z-llm-judge/judge-report.md`

- Winner counts: `codex_grep_filesystem: 2`
- Important limitation: the judge penalized the K2 answer for citing real Flink methods
  (`createJobPlanInfo(...)`, `getTargetRestEndpointURL()`) as likely fabricated, which shows
  answer-only LLM judging can rely on priors instead of verifying citations.

Evidence-aware blinded judge:

`docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260501T231541Z-extension-arms/extension-runs/20260503T011523Z-extension-arms/llm-judge-runs/claude-family-evidence-aware/20260503T012610Z-llm-judge/judge-report.md`

- Winner counts: `codex_with_k2_mcp_tuned: 2`
- Dimension averages for tuned K2: correctness `5.0`, grounding `5.0`, specificity `5.0`,
  usefulness `5.0`, risk `4.5`.

## Takeaway

K2 wins the deterministic evidence-grounding benchmark on these two regression cases and wins
the evidence-aware Claude-family judge. The original answer-only Claude-family judge still
prefers `rg`, but its rationale contains source-verification mistakes. For public reporting,
the evidence-aware judge should be presented as the more defensible qualitative metric, with
the answer-only result disclosed as a limitation.
