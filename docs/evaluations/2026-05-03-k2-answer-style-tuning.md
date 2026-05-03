# K2 Answer-Style Tuning Follow-up

This follow-up tests a narrow product hypothesis from the 100-case fair-baseline
run: LLM judges often preferred local `rg` answers because they were concise,
file-first, and line-specific, even when K2 retrieved broader cross-corpus
evidence.

## Change

The K2 MCP answer tool now returns an explicit answer-style contract and a small
`preferred_sources` budget. The prompt asks Codex to:

- answer like a strong local `rg`/file-read result;
- start with concrete code or test anchors, not a documentation overview;
- prefer implementation and neighboring test sources for implementation
  questions;
- cite only used sources;
- keep missing evidence in an `Uncertainties` section;
- avoid mentioning K2, MCP, retrieval internals, scores, filters, or tool calls.

## Answer-Only Judge Remediation

The next prompt revision targets the failure mode where a judge sees only the
final answer and cannot inspect hidden retrieval evidence. The answer contract
now asks the model to:

- make each important claim self-verifying from the final text;
- prefer clickable `web_line_url` / `web_source_url` citations over internal
  `repo://` identifiers;
- state helper indirection and the helper's concrete return expression together
  when both are visible in line snippets;
- use 2-4 implementation bullets and 1-3 direct neighboring test bullets;
- omit broader related docs/classes/tests unless they directly prove the answer.

This does not make answer-only judging equivalent to evidence-aware judging, but
it reduces the chance that a true source-backed claim is penalized because the
supporting snippet is invisible.

The extension runner has a new `codex_with_k2_mcp_tuned` arm so this behavior can
be tested separately from earlier K2 runs.

## Two-Case Smoke Result

The smoke run reran two known difficult cases against `codex_grep_filesystem`
and `codex_with_k2_mcp_tuned`:

| Arm | Combined | Retrieval | Answer | Evidence Passes |
| --- | ---: | ---: | ---: | ---: |
| Codex + `rg`/filesystem | 0.712500 | 0.633333 | 0.791667 | 0/2 |
| Codex + K2 MCP tuned | 0.893750 | 0.933333 | 0.854167 | 2/2 |

The deterministic score improved for tuned K2 on both cases. This is not yet a
100-case result.

## Judge Result

The two judge families disagreed completely on the same two cases:

| Judge | `rg` Wins | Tuned K2 Wins | Ties |
| --- | ---: | ---: | ---: |
| Codex-family judge | 0 | 2 | 0 |
| Claude-family judge | 2 | 0 | 0 |

This should be treated as an unresolved product signal, not a publishable win.
The tuned K2 answers became more compact and code-first, but Claude still
preferred the `rg` answers' line-level specificity.

## Current Diagnosis

The remaining gap is not only prompt style. In the Flink `JobPlanHandler` case,
K2 retrieved the correct source URI but the returned excerpt did not include the
exact method body that local `rg` found with line anchors. The K2 answer
therefore had to say the exact body-building logic was not visible.

The next tuning step should improve retrieval payloads for Java source:

- return method-level snippets around matched classes and symbols;
- include stable line spans when the source URI is a repository file;
- prioritize neighboring tests with matching class names before broad docs;
- preserve K2's docs/code/test coverage while exposing the same concrete anchor
  quality developers expect from local file reads.

## Rerun After Answer-Only Remediation

Rerun:
`docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/answer-only-fix-rerun/20260503T071004Z-extension-arms/extension-report.md`

Deterministic scorecard:

| Run | Combined | Retrieval | Answer | Passed |
| --- | ---: | ---: | ---: | ---: |
| `codex_without_k2` | `0.260416` | `0` | `0.520833` | `0/2` |
| `codex_grep_filesystem` | `0.7125` | `0.633333` | `0.791667` | `0/2` |
| `codex_with_k2_mcp_tuned` | `0.910417` | `0.966666` | `0.854167` | `2/2` |
| `codex_with_k2_real_mcp` | `0.775` | `0.8` | `0.75` | `1/2` |

Per-case tuned K2 scores:

| Case | Score | Passed |
| --- | ---: | ---: |
| `kafka-connect-converter` | `0.916667` | yes |
| `flink-rest-job-plan-handler` | `0.904167` | yes |

Claude-family answer-only judge:

- Winner counts: `codex_grep_filesystem: 2`
- Mean confidence: `0.735`
- Interpretation: answer-only judging still rewards plausible, file-local `rg`
  answers even when some claims are not externally verified in the judge prompt.

Claude-family evidence-aware judge:

- Winner counts: `codex_with_k2_mcp_tuned: 2`
- Mean confidence: `0.785`
- Interpretation: when the judge sees retrieved evidence snippets, it prefers
  K2 on both regression cases and penalizes unsupported `rg` claims.

Conclusion: the answer-style remediation improved the deterministic K2 answer
score from `0.791667` to `0.854167` on this two-case slice and preserved a
`2/2` evidence pass rate. It did not make answer-only LLM judging reliable by
itself. Public reporting should keep deterministic scoring primary, use
evidence-aware judging for qualitative preference, and disclose answer-only
judge disagreement as a limitation.

## Artifacts

- Smoke run:
  `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260501T231541Z-extension-arms/extension-runs/20260502T234443Z-extension-arms/extension-report.md`
- Codex-family judge:
  `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260501T231541Z-extension-arms/extension-runs/20260502T234443Z-extension-arms/llm-judge-runs/20260502T235110Z-llm-judge/judge-report.md`
- Claude-family judge:
  `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260501T231541Z-extension-arms/extension-runs/20260502T234443Z-extension-arms/llm-judge-runs/claude-family/20260502T235228Z-llm-judge/judge-report.md`
- Judge-family comparison:
  `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260501T231541Z-extension-arms/extension-runs/20260502T234443Z-extension-arms/llm-judge-runs/judge-family-comparison-k2-tuned-vs-rg.md`
- Answer-only remediation rerun:
  `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/answer-only-fix-rerun/20260503T071004Z-extension-arms/extension-report.md`
- Claude-family answer-only rerun:
  `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/answer-only-fix-rerun/20260503T071004Z-extension-arms/llm-judge-runs/claude-family/20260503T071701Z-llm-judge/judge-report.md`
- Claude-family evidence-aware rerun:
  `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/answer-only-fix-rerun/20260503T071004Z-extension-arms/llm-judge-runs/claude-family-evidence-aware/20260503T071822Z-llm-judge/judge-report.md`
