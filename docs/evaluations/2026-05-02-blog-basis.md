# Blog Basis: K2 for Java R&D Coding Agents

This is a concise, publication-oriented summary of the current evidence. It is
written to support a technical blog post, not to claim a general benchmark win.

## Defensible Claim

On 100 class-anchored Apache Flink 2.2 and Apache Kafka 4.2 Java R&D questions,
Codex connected to K2 through a stdio MCP server produced more complete
version-pinned source grounding than both a no-tool Codex baseline and a
retrieval-capable Codex baseline using local `rg`/filesystem access to the same
source checkouts.

The narrow claim is deterministic source grounding. The fair-baseline LLM judges
did not prefer K2 answers over `rg` answers, and the patch-generation smoke run
does not prove a productivity win.

## Systems Compared

| Arm | Retrieval Access | Shell/Web | Cases |
| --- | --- | --- | ---: |
| No-tool Codex | None | disabled | 100 |
| Codex + `rg`/filesystem | Local sparse Flink/Kafka checkouts | shell/file reads only; web disabled | 100 |
| Codex + K2 MCP | K2 docs/code/tests/guides through stdio MCP | shell/web disabled | 100 |

The `rg` baseline is the fairer comparison to publish. It answers the obvious
developer critique: "couldn't I just let the agent grep the repository?"

## Deterministic Scorecard

| Arm | Combined | Retrieval | Answer | Safety | Evidence Passes |
| --- | ---: | ---: | ---: | ---: | ---: |
| No-tool Codex | 0.189375 | 0.000000 | 0.378750 | 1.000000 | 0/100 |
| Codex + `rg`/filesystem | 0.754083 | 0.637333 | 0.870833 | 1.000000 | 2/100 |
| Codex + K2 MCP | 0.928875 | 0.954000 | 0.903750 | 1.000000 | 93/100 |

Interpretation:

- `rg` materially improves over no-tool Codex, especially answer quality.
- K2 improves most on retrieval coverage: docs, code, tests, modules, API
  surfaces, and exact source URIs are retrieved together rather than discovered
  one file at a time.
- `Evidence Passes` is a strict source-grounding threshold, not an answer-count
  metric. All arms produced answers.

Full per-question data, including each question text, is in
`docs/evaluations/runs/20260501T134908Z-real-mcp/per-question-stats.md`.
The untruncated 100-case question list is in
`docs/evaluations/2026-05-02-question-catalog.md`.

## LLM-as-Judge Robustness

Two judge families scored randomized A/B answer pairs. The result depends
heavily on which baseline is used.

K2 vs no-tool baseline:

| Judge | K2 Wins | No-tool Wins | Ties | Mean Confidence |
| --- | ---: | ---: | ---: | ---: |
| Codex CLI / OpenAI-family | 71 | 29 | 0 | 0.8573 |
| Claude Code / Anthropic-family | 74 | 26 | 0 | 0.7424 |

K2 vs `rg`/filesystem baseline:

| Judge | K2 Wins | `rg` Wins | Ties | Mean Confidence |
| --- | ---: | ---: | ---: | ---: |
| Codex CLI / OpenAI-family | 44 | 56 | 0 | 0.8001 |
| Claude Code / Anthropic-family | 1 | 99 | 0 | 0.8308 |

The fair-baseline judge result is a negative finding for any public answer
quality claim. It suggests the deterministic source-grounding score and
LLM-judge preference measure different things: K2 retrieved broader cross-corpus
evidence, while judges often preferred the `rg` answers' concise file-specific
shape. Treat this as a prompt/product finding, not as something to smooth over.

## K2 Failure Analysis

K2 failed the deterministic evidence threshold on 7/100 cases:

| Case | K2 Combined | Main Gap |
| --- | ---: | --- |
| `flink-rest-savepoint-handlers` | 0.808333 | missed exact docs/source/test mix |
| `flink-rest-checkpoint-handlers` | 0.612500 | weak REST-source/test anchoring |
| `kafka-connect-herder` | 0.583333 | missed required `Herder` URI/citation |
| `kafka-connect-worker` | 0.583333 | missed required `Worker` URI/citation |
| `kafka-connect-config-def` | 0.550000 | missed `clients` module/source URI |
| `kafka-connect-converter` | 0.583333 | missed required `Converter` URI/citation |
| `kafka-connect-schemas` | 0.583333 | missed required schema URI/citation |

The `rg` baseline scored higher than K2 on 6 cases, all from this failure set:
`flink-rest-checkpoint-handlers`, `kafka-connect-herder`,
`kafka-connect-worker`, `kafka-connect-config-def`,
`kafka-connect-converter`, and `kafka-connect-schemas`.

This is a useful product signal: exact class/interface names in broad Kafka
Connect API packages need better disambiguation and stronger source URI
recall. K2 should not be presented as perfect.

## Ablations

A 20-case Flink REST slice compared the original K2 setup with two ablations:

| Arm | Combined | Retrieval | Answer | Evidence Passes |
| --- | ---: | ---: | ---: | ---: |
| K2 MCP original | 0.891875 | 0.940000 | 0.843750 | 18/20 |
| K2 MCP without explicit skill choreography | 0.888333 | 0.901667 | 0.875000 | 18/20 |
| K2 MCP with metadata filters disabled | 0.898125 | 0.940000 | 0.856250 | 19/20 |

Do not overclaim this ablation. On this small, class-name-heavy Flink REST slice,
the original profile, no-skill prompt, and filters-off run are close. The right
follow-up is a larger ablation with Kafka Connect and held-out natural-language
questions, not a claim that filters are always decisive.

## Retrieval Design

K2 used separate profiles by source type:

| Source Kind | Dense | Sparse | Metadata Sparse | Reason |
| --- | ---: | ---: | ---: | --- |
| Docs | 0.9 | 0.1 | 0.0 | semantic matching for conceptual text |
| Code/tests/guides | 0.0 | 0.8 | 0.2 | exact Java class, method, package, and path matching |

The measured K2 advantage in this run is broader recall and source coverage
across indexed corpora than local `rg` produced against the same sparse
checkouts. Metadata-aware retrieval is part of the product design, but the
20-case ablation below is not enough to claim that filters are the measured
differentiator.

## Answer-Style Tuning Follow-up

After the `rg` baseline beat K2 in fair-baseline LLM-judge preference, the MCP
answer tool was tuned to return an explicit `rg`-like answer contract and a
small `preferred_sources` budget. A two-case smoke run on previously weak
Kafka/Flink questions improved tuned K2's deterministic score over `rg`
(`0.893750` vs `0.712500`) and passed both strict evidence checks.

The judge result remains unresolved: a Codex-family judge preferred tuned K2 on
both cases, while a Claude-family judge preferred `rg` on both cases. The
practical diagnosis is that K2 retrieves broader evidence, but it still needs
better method-level snippets and line spans to match the concrete file-read
specificity of local `rg`.

The follow-up artifact is documented in
`docs/evaluations/2026-05-03-k2-answer-style-tuning.md`.

## Patch-Generation Extension

A separate patch-generation benchmark now compares final code diffs, focused
verification, wall-clock time, guide compliance, and best-effort Codex
token/tool metrics. The customer-relevant baseline is
`codex_repo_plus_guides_dump`: vanilla Codex with the same local repository and
a local Confluence-style guide export, but without K2 MCP routing, K2 Agents,
metadata filters, or Knowledge Feeds.

One earlier smoke run completed a Flink feature task with focused Maven
verification before the guide-dump baseline was added:

| Arm | Passed | Score | Duration | Total tokens |
| --- | ---: | ---: | ---: | ---: |
| Repo-only Codex | 1/1 | 1.000 | 201.849s | 2,624,225 |
| Codex + K2 MCP | 1/1 | 1.000 | 201.090s | 3,393,421 |

This confirms the E2E patch harness works and captures real compile/test
signals, but it is not yet a product claim: both arms passed one task, and the
run did not include the stronger guide-dump baseline. Report a
feature-development claim only after at least 10 paired
`codex_repo_plus_guides_dump` versus `codex_with_k2_mcp` tasks complete with
focused tests and either human review or a blinded patch judge.

The token result should be disclosed. On this one smoke task, K2 used about 30%
more Codex tokens for the same pass/fail outcome. That is expected to be a bad
trade on tasks where local search is already enough; the pilot should test
whether K2 earns the extra context cost on `docs_code_test` and
`version_sensitive_*` tasks.

The benchmark plan and first smoke artifact are documented in
`docs/evaluations/2026-05-02-patch-generation-benchmark.md` and
`docs/evaluations/patch-runs/20260502T085752Z-patch-generation/`.
The falsifiable decision rule and pilot plan are documented in
`docs/evaluations/2026-05-02-feature-development-validation-strategy.md`.

## Hallucination Markers

The marker lists are negative controls for obvious framework confusions such as
Spring MVC, JAX-RS, Bean Validation, and obsolete Flink state backend advice. In
the current 100-case run, no hallucination marker fired in either no-tool or K2
answers, so the safety multiplier did not drive the headline result.

## Artifacts

- Main 100-case K2 vs no-tool run:
  `docs/evaluations/runs/20260501T134908Z-real-mcp/report.md`
- 100-case no-tool vs `rg` vs K2 extension:
  `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260501T231541Z-extension-arms/extension-report.md`
- 20-case K2 no-skill / filters-off ablation:
  `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260502T000108Z-extension-arms/extension-report.md`
- Patch-generation benchmark plan:
  `docs/evaluations/2026-05-02-patch-generation-benchmark.md`
- Feature-development validation strategy:
  `docs/evaluations/2026-05-02-feature-development-validation-strategy.md`
- Patch-generation E2E smoke run:
  `docs/evaluations/patch-runs/20260502T085752Z-patch-generation/patch-report.md`
- Claude-family judge run:
  `docs/evaluations/runs/20260501T134908Z-real-mcp/llm-judge-runs/20260501T231305Z-llm-judge/judge-report.md`
- Judge-family comparison:
  `docs/evaluations/runs/20260501T134908Z-real-mcp/llm-judge-runs/judge-family-comparison.md`
- K2 vs `rg` Codex-family judge run:
  `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260501T231541Z-extension-arms/llm-judge-runs/20260502T213319Z-llm-judge/judge-report.md`
- K2 vs `rg` Claude-family judge run:
  `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260501T231541Z-extension-arms/llm-judge-runs/20260502T214046Z-llm-judge/judge-report.md`
- K2 vs `rg` judge-family comparison:
  `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260501T231541Z-extension-arms/llm-judge-runs/judge-family-comparison-k2-vs-rg.md`
- K2 answer-style tuning follow-up:
  `docs/evaluations/2026-05-03-k2-answer-style-tuning.md`

## Remaining Limits

- The 100 cases are class-anchored and template-shaped; this should be disclosed.
- Only one generated patch task has been compiled/tested; it is harness
  validation, not a productivity result.
- The `rg` baseline has shell access to sparse checkouts, not the full upstream
  repos.
- The 20-case ablation is not enough to prove the metadata-filter contribution.
- The one-task patch smoke validates the harness, not a feature-development win.
- LLM judges are only partially blinded because citations and file paths are
  visible answer features.
- The fair-baseline LLM judges prefer `rg` answers over K2 answers; do not claim
  human-perceived answer quality superiority without human review or prompt
  changes followed by reruns.
- A publishable product story still needs customer outcome, pricing motion, and
  competitive framing against Sourcegraph/Cursor/Claude Skills.
