# Patch-Generation E2E Smoke Run

This run executed one controlled Flink 2.2 feature-development task through two
Codex arms:

- `codex_repo_only`
- `codex_with_k2_mcp`

Both arms generated a patch, passed `git diff --check`, passed the focused
`JobVertexWatermarksHandlerTest` Maven invocation, and passed the lightweight
same-project Java import-resolution check.

| Arm | Passed | Score | Duration | Total tokens | K2 tool calls |
| --- | ---: | ---: | ---: | ---: | --- |
| `codex_repo_only` | `1/1` | `1.000` | `201.849s` | `2,624,225` | none |
| `codex_with_k2_mcp` | `1/1` | `1.000` | `201.090s` | `3,393,421` | `k2_search_code`, `k2_search_docs`, `k2_search_guides`, `k2_search_tests` |

Interpret this as an E2E harness validation, not as an engineering-productivity
claim. A publishable productivity claim needs at least 5-10 verified tasks and
human review or a blinded patch judge over the final patches.

The raw Codex JSON event streams were intentionally not committed. The retained
artifacts are the report, scorecard, prompts, final answers, diffs, and
verification results.
