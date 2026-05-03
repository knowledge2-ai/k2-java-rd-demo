# Feature-Development Validation Strategy

This document defines the falsifiable strategy for proving, or disproving, that
K2 improves Java feature development.

## Hypothesis

K2 improves feature-development outcomes when the task requires cross-corpus
context: version-pinned docs, source, neighboring tests, and generated
engineering guides. For customer-facing claims, the baseline must also receive
a local Confluence-style guide dump so K2 is compared against a strong vanilla
Codex setup, not against an artificially starved agent.

The null hypothesis is that K2 does not materially improve patch correctness,
review acceptability, time, or token efficiency over a fair retrieval-capable
baseline using the same model and local repository access.

## Arms

The patch benchmark supports these arms:

| Arm | Purpose |
| --- | --- |
| `codex_repo_only` | Fair baseline with local source, shell, `rg`, and file reads. |
| `codex_repo_plus_docs` | Strong baseline with local source plus declared local docs paths and version-pinned docs URLs. |
| `codex_repo_plus_guides_dump` | Strongest vanilla-Codex baseline with local source plus a local Confluence-style guide dump. No K2/MCP routing, Agents, metadata filters, or Knowledge Feeds. |
| `codex_with_k2_mcp` | Treatment arm using K2 MCP retrieval across docs, guides, code, and tests. |
| `codex_with_k2_mcp_no_guides` | K2 ablation with generated-guide retrieval disabled. |
| `codex_with_k2_mcp_filters_off` | K2 ablation with metadata filters disabled. |

The no-tool Codex arm is intentionally excluded from feature-development claims.
It remains useful for Q&A but is not a fair coding-agent baseline.

## Task Design

Each task must define:

- natural-language feature request
- repository and version
- task class
- allowed edit neighborhoods
- expected files for deterministic coverage scoring
- success criteria
- focused verification command
- local/version-pinned docs pointers for the strong baseline
- local Confluence-style guide files for the strongest vanilla baseline
- required guardrail IDs that must appear in the final answer evidence
- forbidden implementation patterns from the applicable guide

The prompt may list local guide file paths, but it must not leak the required
guardrail IDs or generated guide source URIs. The agent has to inspect either
the local guide dump or K2 retrieval output to surface those identifiers.

Task classes:

| Class | Intended signal |
| --- | --- |
| `local_pattern` | Whether local `rg` is already enough. |
| `docs_code_test` | Whether combining docs, source, and tests helps. |
| `version_sensitive_rest` | Whether version-pinned context prevents stale API choices. |
| `version_sensitive_connect` | Same for Kafka Connect-specific APIs. |

## Primary Metrics

The headline productivity claim should use only verified patch outcomes:

- focused test pass rate
- compile/test reachability
- deterministic scope/coverage score
- blinded patch-judge preference
- guide guardrail score
- forbidden-pattern safety score
- wall-clock duration
- token usage

The deterministic scorecard is a triage tool. Human review or a blinded patch
judge is still required before making a public claim about patch quality.

## Decision Rule

For customer-facing claims, compare K2 against
`codex_repo_plus_guides_dump`. Keep two separate verdicts:

- quality verdict: whether K2 improves correctness, guardrail compliance, and
  review acceptability;
- cost verdict: whether K2 also reduces total Codex tokens.

K2 earns the full customer-value claim only if:

```text
paired_task_count >= 10
and K2 pass_rate >= guide_dump_baseline pass_rate + 15 percentage points
and K2 mean_guide_guardrail_score >= guide_dump_baseline mean_guide_guardrail_score
and K2 duration_ratio <= 1.30
and K2 token_ratio <= 0.90
```

If the pass-rate delta is within +/-5 points, report `no_clear_k2_win`. If the
result depends on task class, report it as mixed rather than forcing a single
claim. If K2 improves quality but `token_ratio > 0.90`, report a quality win
without making a token-savings claim.

## Pilot Plan

1. Run the built-in 12-task pilot with `codex_repo_only`, `codex_repo_plus_docs`,
   `codex_repo_plus_guides_dump`, and `codex_with_k2_mcp`.
2. If K2 does not show signal, inspect K2 losses before scaling:
   - bad or stale retrieval
   - missing guide/source/test corpus coverage
   - overbroad context
   - agent ignored retrieved evidence
   - baseline found enough context with local search
3. Add ablations only after the main two-arm comparison is stable:
   - `codex_with_k2_mcp_no_guides`
   - `codex_with_k2_mcp_filters_off`
4. Scale to at least 30 tasks before external publication.
5. Add two-family blinded patch judging and human spot-checks for the final
   public report.

## Current Evidence

The first E2E smoke run proves the harness can execute real feature-development
tasks and focused Maven verification. It does not prove K2 wins:

| Run | Result |
| --- | --- |
| `docs/evaluations/patch-runs/20260502T085752Z-patch-generation/` | Both repo-only Codex and K2-assisted Codex passed one Flink task. |

This should be described as harness validation only.

The next required run is the customer-relevant pair:
`codex_repo_plus_guides_dump` versus `codex_with_k2_mcp`, with answer text,
patches, focused verification, guide guardrail scores, duration, and Codex token
metrics captured per task.
