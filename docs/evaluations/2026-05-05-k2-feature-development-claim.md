# K2 Feature-Development Claim Check

Date: 2026-05-05

This run compares the strongest local baseline against Codex using the K2 MCP
server for Apache Flink/Kafka feature-development tasks.

## Arms

- Baseline: `codex_repo_plus_guides_dump`
  - Codex has local source, version-pinned docs, and a local generated
    Confluence-style guide dump.
  - It cannot use K2 or MCP tools.
- Treatment: `codex_with_k2_mcp`
  - Codex has the same local source, plus the K2 MCP server.
  - The MCP server exposes a compact high-level `k2_answer_with_sources` tool
    backed by K2 SDK retrieval over guides, docs, source, and tests.

## Result

Verifier: `claim_ready=true`, `verdict=k2_wins`

| Metric | Baseline | K2 MCP |
| --- | ---: | ---: |
| Paired tasks | 12 | 12 |
| Passed tasks | 5 | 12 |
| Mean score | 0.971111 | 1.0 |
| Mean guide guardrail score | 0.86 | 1.0 |
| Mean total tokens | 1,414,399 | 1,155,291 |
| Mean duration seconds | 118.305 | 154.889 |
| Tokens per accepted patch | 3,394,558 | 1,155,291 |
| Seconds per accepted patch | 283.933 | 154.889 |

Decision-rule ratios:

- Pass-rate delta: `+0.583333`
- Mean token ratio: `0.816807`
- Token ratio per accepted patch: `0.340336`
- Raw mean duration ratio: `1.309227`
- Duration ratio per accepted patch: `0.545511`

The raw treatment run was slower per attempted task, but the baseline only
produced accepted patches on 5 of 12 tasks. On usable output, K2 reduced both
tokens and wall time per accepted patch.

## Reproduction

Latest local claim artifact:

```bash
python scripts/verify_patch_generation_scorecard.py \
  .eval-runs/claim-grade/20260505T050533Z-current-baseline-vs-compact-surface-k2/patch-scorecard.json \
  --require-focused-tests \
  --format json
```

The treatment run used:

```bash
python scripts/run_patch_generation_benchmark.py \
  --execute \
  --arm codex_with_k2_mcp \
  --include-kafka \
  --mcp-backend sdk \
  --retrieval-profile java_exact \
  --env-file .env \
  --out-dir .eval-runs/k2-compact-surface-full \
  --run-tests
```

Validation on this commit:

```bash
ruff check src scripts tests
python -m pytest -q
```

## Limitations

- This is a 12-task feature-development benchmark, not a universal Java
  development benchmark.
- Raw mean duration is reported separately and is not hidden: K2 was about
  `1.31x` slower per attempted run in this sample.
- The customer-value claim is based on accepted patches, because failed patches
  require rework before they create useful engineering output.
