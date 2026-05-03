# K2 + Codex Java R&D Demo: Evaluation Methodology and Results

**Date:** 2026-05-01

**Headline run:** `docs/evaluations/runs/20260501T134908Z-real-mcp/`

**System under test:** the same Codex model in two configurations: baseline with no retrieval tools, and Codex connected to K2 through a local stdio MCP server.

**2026-05-02 extension:** added a retrieval-capable Codex + `rg`/filesystem
baseline over the same sparse Flink/Kafka checkouts, two judge-family runs for
both K2-vs-no-tool and K2-vs-`rg`, and a 20-case K2 no-skill / filters-off
ablation. A separate patch-generation benchmark now measures final code diff,
focused verification, wall-clock time, guide compliance, and Codex token/tool
metrics. The customer-relevant patch baseline is vanilla Codex with local repo
access plus a local Confluence-style guide dump; the first one-task smoke run
predated that stronger baseline and should be treated only as harness
validation.

## Executive Summary

This evaluation asks a narrow question:

> Does connecting the same Codex model to K2 through MCP improve its ability to answer version-pinned Apache Flink and Apache Kafka engineering questions with verifiable source evidence?

On the 100 class-anchored Flink/Kafka retrieval cases, the K2-backed MCP
configuration produced substantially stronger deterministic source grounding
than the no-tool baseline and the `rg`/filesystem baseline.

| Run | Answers | Combined | Retrieval | Answer | Safety | Evidence Passes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Codex without K2 | 100/100 | 0.189375 | 0.000000 | 0.378750 | 1.000000 | 0/100 |
| Codex + `rg`/filesystem | 100/100 | 0.754083 | 0.637333 | 0.870833 | 1.000000 | 2/100 |
| Codex with K2 MCP | 100/100 | 0.928875 | 0.954000 | 0.903750 | 1.000000 | 93/100 |

The deterministic scorecard measures evidence grounding, not compile-and-run
correctness. A "pass" means the answer cleared a strict threshold requiring
version-pinned docs, source files, test anchors, citations, and required topic
mentions.

The partially blinded OpenAI-family LLM-judge run preferred the K2-backed answer
in 71/100 cases, with no ties and mean confidence 0.8573. A second
Claude-family judge run preferred K2 in 74/100 cases, with no ties and mean
confidence 0.7424. Those judge results compare against the intentionally strict
no-tool baseline. Against the stronger `rg`/filesystem baseline, the same judge
families preferred `rg` answers: OpenAI-family 56/100 and Claude-family 99/100.
This report therefore supports a source-grounding claim, not a broad
human-preference or answer-quality claim.

## Architecture

The assisted configuration uses a local MCP server:

- Runner: `scripts/run_codex_k2_real_mcp_comparison.py`
- MCP server: `src/k2_java_rd_demo/k2_mcp_server.py`
- Backend: K2 SDK API
- Tool: `k2_answer_with_sources`
- Data: version-pinned Apache Flink 2.2 docs/source/tests, Apache Kafka 4.2 docs/source/tests, and generated Java R&D guide documents

The baseline and assisted runs use the same model and task prompt shape. Shell, browser, and web search are disabled in both runs. The assisted run may call only the K2 MCP tool and uses the K2 demo skill instructions that describe how to query K2.

## Retrieval Design

The benchmark intentionally uses both dense and sparse retrieval profiles:

- Documentation retrieval favors dense semantic matching for conceptual questions.
- Code and test retrieval favors sparse and metadata-sparse matching because Java class names, package names, method names, and file paths are exact-match-heavy.
- Metadata filters separate framework, version, source kind, module, API surface, class name, and path.

This mirrors the target enterprise use case: large Java systems where internal docs, source, tests, and engineering guides must be queried together without losing source provenance.

## Benchmark Corpus

The benchmark has 100 class-anchored retrieval cases:

- 50 Apache Flink questions, covering REST endpoint patterns and checkpointing/state internals.
- 50 Apache Kafka questions, covering Kafka Connect REST, connector runtime, configuration, data model, class loading, and client override policy areas.

Each case has expected evidence requirements such as:

- source kinds: docs, code, tests
- modules: `flink-runtime`, `connect`, `clients`, `docs`
- API surfaces: `rest`, `checkpointing`, `connect`
- source URI coverage for specific implementation files
- required answer mentions
- hallucination markers to penalize unrelated frameworks such as Spring MVC or Bean Validation

The case catalog is in `src/k2_java_rd_demo/benchmark_cases.py`. The cases intentionally emphasize class names, modules, API surfaces, source URIs, and version-pinned docs; they should not be described as a broad sample of all Java coding tasks.

## Scoring

Each answer receives:

```text
retrieval_score = average(
  artifact_matches,
  source_kind_coverage,
  module_hits,
  api_surface_hits,
  source_uri_coverage
)

answer_score = average(
  must_mention_coverage,
  citation_coverage
)

combined_score = average(retrieval_score, answer_score) * hallucination_safety_score
```

The baseline can still receive answer-quality credit for naming relevant concepts. However, because it has no retrieval rows and usually cannot cite exact version-pinned source URIs, it cannot clear the evidence-grounding pass threshold.

## LLM-Judge

The secondary judge uses blinded A/B labels with deterministic shuffling per case. It does not see which answer came from K2 until after scoring is mapped back.

K2 vs no-tool results:

- K2-backed answer preferred: 71
- Baseline answer preferred: 29
- Ties: 0
- Mean confidence: 0.8573

Second-family judge check:

- Claude-family K2-backed answer preferred: 74
- Claude-family baseline answer preferred: 26
- Cross-judge simple agreement: 0.770
- Cohen's kappa: 0.424

Dimension averages:

| Run | Correctness | Grounding | Specificity | Usefulness | Risk |
| --- | ---: | ---: | ---: | ---: | ---: |
| Codex with K2 MCP | 3.70 | 4.24 | 4.16 | 3.93 | 3.57 |
| Codex without K2 | 2.90 | 2.18 | 2.61 | 2.83 | 2.79 |

K2 vs `rg`/filesystem results:

| Judge | K2 Wins | `rg` Wins | Ties | Mean Confidence |
| --- | ---: | ---: | ---: | ---: |
| Codex CLI / OpenAI-family | 44 | 56 | 0 | 0.8001 |
| Claude Code / Anthropic-family | 1 | 99 | 0 | 0.8308 |

This is a negative result for an LLM-judge answer-preference claim over a fair
retrieval-capable baseline. It likely reflects a mismatch between the
deterministic source-grounding rubric and what the judges prefer in prose:
judges often rewarded concise, file-specific `rg` answers even when K2 had
broader cross-corpus evidence coverage. Human spot-checks and prompt changes
should precede any renewed answer-quality claim.

## Retrieval-Capable Baseline

The 2026-05-02 extension added a baseline where Codex had shell/file-read access
to deterministic sparse checkouts of Flink and Kafka, could use `rg`, and still
had no K2, browser, or web search access.

| Run | Combined | Retrieval | Answer | Safety | Evidence Passes |
| --- | ---: | ---: | ---: | ---: | ---: |
| Codex without K2 | 0.189375 | 0.000000 | 0.378750 | 1.000000 | 0/100 |
| Codex + `rg`/filesystem | 0.754083 | 0.637333 | 0.870833 | 1.000000 | 2/100 |
| Codex with K2 MCP | 0.928875 | 0.954000 | 0.903750 | 1.000000 | 93/100 |

The `rg` baseline materially improves answer quality and exact source grounding.
K2 still retrieves broader evidence across docs, source, tests, and generated
guides, which is why its retrieval score and evidence-pass count remain higher.
The LLM judges do not confirm that this broader evidence made the final answer
more preferable to a reader.

## Ablation Slice

A 20-case Flink REST slice compared the original K2 setup with two ablations.

| Run | Combined | Retrieval | Answer | Evidence Passes |
| --- | ---: | ---: | ---: | ---: |
| K2 MCP original | 0.891875 | 0.940000 | 0.843750 | 18/20 |
| K2 MCP without explicit skill choreography | 0.888333 | 0.901667 | 0.875000 | 18/20 |
| K2 MCP with metadata filters disabled | 0.898125 | 0.940000 | 0.856250 | 19/20 |

This small slice should be treated as an ablation check, not as proof that
filters are or are not decisive. It mainly shows that the K2 MCP tool itself
remains effective without the explicit skill prompt on these class-name-heavy
Flink REST questions.

## Failure Analysis

K2 failed the deterministic evidence threshold on 7/100 cases. The failures are
concentrated in exact source URI/citation misses for broad or ambiguous classes:
`flink-rest-savepoint-handlers`, `flink-rest-checkpoint-handlers`,
`kafka-connect-herder`, `kafka-connect-worker`, `kafka-connect-config-def`,
`kafka-connect-converter`, and `kafka-connect-schemas`.

The `rg` baseline scored higher than K2 on six cases, all from this failure set.
That is useful signal for improving K2 retrieval disambiguation, especially for
Kafka Connect API/runtime classes whose exact source paths span multiple modules.

## Artifacts

- Deterministic report: `docs/evaluations/runs/20260501T134908Z-real-mcp/report.md`
- Scorecard: `docs/evaluations/runs/20260501T134908Z-real-mcp/scorecard.json`
- Per-question stats: `docs/evaluations/runs/20260501T134908Z-real-mcp/per-question-stats.md`
- LLM-judge report: `docs/evaluations/runs/20260501T134908Z-real-mcp/llm-judge-runs/20260501T141610Z-llm-judge/judge-report.md`
- Claude-family judge report: `docs/evaluations/runs/20260501T134908Z-real-mcp/llm-judge-runs/20260501T231305Z-llm-judge/judge-report.md`
- Judge-family comparison: `docs/evaluations/runs/20260501T134908Z-real-mcp/llm-judge-runs/judge-family-comparison.md`
- Retrieval-capable baseline extension: `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260501T231541Z-extension-arms/extension-report.md`
- K2 vs `rg` Codex-family judge report: `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260501T231541Z-extension-arms/llm-judge-runs/20260502T213319Z-llm-judge/judge-report.md`
- K2 vs `rg` Claude-family judge report: `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260501T231541Z-extension-arms/llm-judge-runs/20260502T214046Z-llm-judge/judge-report.md`
- K2 vs `rg` judge-family comparison: `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260501T231541Z-extension-arms/llm-judge-runs/judge-family-comparison-k2-vs-rg.md`
- K2 ablation slice: `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260502T000108Z-extension-arms/extension-report.md`

## Limitations

- This is an evidence-grounding benchmark, not a patch-generation benchmark.
- It does not compile generated code or run Flink/Kafka test suites.
- The no-tool baseline is intentionally strict: no shell, no browser, no web search, no repo access. A separate `rg`/filesystem baseline now provides a retrieval-capable comparison, but it is still not a vanilla vector-store or Sourcegraph/Cursor comparison.
- The benchmark uses a curated class-anchored case set designed for this Java R&D demo.
- The evaluation now includes local grep/filesystem retrieval, but it still does not isolate K2 against a generic vector database, standalone BM25, Sourcegraph, Cursor, or another RAG system.
- The deterministic combined score is retrieval-shaped by design. Retrieval score, answer score, and combined score should be inspected separately before drawing conclusions.
- The fair-baseline LLM judges preferred `rg`/filesystem answers over K2
  answers. This should be treated as a product and prompt-quality finding, not
  as an ignorable disagreement.
- The secondary judge is only partially blinded because source-grounded answers have visible structural fingerprints such as citations and exact file paths.
- The original assisted run has K2-specific tool instructions. A 20-case no-skill ablation has been added, but a larger no-skill run and neutral baseline coaching would still be stronger.
- The baseline model may already know some Flink/Kafka concepts from pretraining, so the cleanest claim is about exact source grounding and citation quality.

## Defensible Claim

For this controlled 100-case run, connecting Codex to K2 through MCP materially
improved deterministic exact evidence grounding for version-pinned,
class-anchored Java R&D questions. The fair-baseline LLM judges did not prefer
K2 answers over `rg` answers, so the defensible claim is source-grounding and
cross-corpus evidence coverage, not general answer-quality or coding-agent
superiority.
