# K2 Java R&D Customer Demo Runbook

Use this runbook to present K2 as the context layer for Claude Code, Codex, or a
similar coding agent working in a large legacy Java R&D codebase. The demo uses
Apache Flink and optional Apache Kafka assets as safe public stand-ins for a
customer repository and Confluence-style engineering guides.

## Security Notes

- Do not paste, commit, or screen-share K2 keys.
- K2 credentials must come from environment variables such as `K2_API_KEY` and
  `K2_API_HOST`; scripts and markdown should never contain a literal key.
- Rotate any credential that may have appeared in chat, logs, terminals, or
  other non-secret storage before using it for a customer-facing demo.
- Use public OSS data or sanitized customer data only.

## Demo Story

Run the same engineering task three ways:

| Mode | Agent context | Customer-visible result |
| --- | --- | --- |
| Baseline Claude/Codex without K2 | Task prompt only | The agent makes generic Java or Flink guesses and usually has weak citations. |
| Repo-only Claude/Codex | Local repository tools such as grep, file reads, and tests | The agent can eventually find files, but it may miss versioned docs, Confluence-style conventions, and neighboring tests unless it searches perfectly. |
| K2-assisted Claude/Codex | Local repo plus K2 metadata filters, K2 Agents, and Knowledge Feeds over docs, code, tests, and guides | The agent retrieves conventions first, then implementation patterns and tests, with citations tied to docs URLs, modules, classes, and paths. |

The customer point is not that Claude or Codex cannot search a repository. The
point is that K2 gives the agent a version-aware knowledge layer that already
understands docs, modules, tests, APIs, guide pages, and exact identifiers.

## Presenter Setup

Export credentials outside the repo:

```bash
export K2_API_KEY="..."
export K2_API_HOST="https://api.knowledge2.ai"
```

Build guide assets:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli build-guides \
  --framework flink \
  --version 2.2.0 \
  --out /tmp/java-rd-guides.jsonl
```

Plan source checkouts and docs harvesting:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli plan-repo-checkout --include-kafka \
  --base-dir /tmp/k2-java-rd-demo-sources

PYTHONPATH=src python -m k2_java_rd_demo.cli discover-docs-urls \
  --framework flink \
  --max-pages 25
```

Build docs assets after confirming the URL set:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli build-docs-assets \
  --framework flink \
  --max-pages 25 \
  --out /tmp/flink-docs.jsonl
```

Inspect the demo configuration and sample scorecard:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli show-config
PYTHONPATH=src python -m k2_java_rd_demo.cli show-agent-specs
PYTHONPATH=src python -m k2_java_rd_demo.cli show-readiness-probes
PYTHONPATH=src python -m k2_java_rd_demo.cli show-mcp-contract --include-kafka
PYTHONPATH=src python -m k2_java_rd_demo.cli score-sample
PYTHONPATH=src python -m k2_java_rd_demo.cli score-demo-cases --include-kafka
PYTHONPATH=src python -m k2_java_rd_demo.cli score-customer-value \
  --include-kafka \
  --format markdown
PYTHONPATH=src python -m unittest discover -s tests/e2e
```

Run the customer-relevant feature-development benchmark once the K2 MCP backend
and local source checkouts are ready. The default catalog contains 12 paired
Flink/Kafka tasks, so it can satisfy the 10-task publication threshold when run
without `--max-tasks` or `--task-id`:

```bash
python scripts/run_claim_grade_patch_benchmark.py \
  --env-file .env
```

The claim-grade runner performs the SDK preflight probe, executes both arms
with focused tests, writes the patch scorecard, and writes the evidence audit.
It exits non-zero if the audit is not claim-ready. The equivalent manual steps
are:

```bash
python scripts/run_patch_generation_benchmark.py \
  --preflight-only \
  --probe-k2-sdk \
  --arm codex_repo_plus_guides_dump \
  --arm codex_with_k2_mcp \
  --retrieval-profile java_exact \
  --mcp-backend sdk \
  --env-file .env
```

```bash
python scripts/run_patch_generation_benchmark.py \
  --execute \
  --probe-k2-sdk \
  --arm codex_repo_plus_guides_dump \
  --arm codex_with_k2_mcp \
  --retrieval-profile java_exact \
  --mcp-backend sdk \
  --env-file .env \
  --out-dir docs/evaluations/patch-runs/customer-guardrail
```

Audit the generated scorecard before using it in a customer narrative:

```bash
python scripts/verify_patch_generation_scorecard.py \
  docs/evaluations/patch-runs/<run-id>/patch-scorecard.json \
  --require-focused-tests
```

Validate Agent and Knowledge Feed specs after concrete corpus IDs exist:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli validate-agent-specs \
  --project-id "<project-id>" \
  --flink-docs-corpus-id "<docs-corpus-id>" \
  --flink-code-corpus-id "<code-corpus-id>" \
  --guides-corpus-id "<guides-corpus-id>"
```

Plan a live K2 run without calling the K2 API:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli plan-live-run \
  --jsonl /tmp/java-rd-guides.jsonl \
  --project-id "<project-id>" \
  --guides-corpus-id "<guides-corpus-id>"
```

Execute the upload, index sync, and readiness probes only after the plan is
validated:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli run-live-k2 \
  --execute \
  --jsonl /tmp/java-rd-guides.jsonl \
  --project-id "<project-id>" \
  --guides-corpus-id "<guides-corpus-id>" \
  --idempotency-prefix java-rd-demo
```

Deploy K2 Agents and the Knowledge Feed after docs, code, and guide corpora are
ready:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli deploy-live-agents \
  --execute \
  --project-id "<project-id>" \
  --flink-docs-corpus-id "<docs-corpus-id>" \
  --flink-code-corpus-id "<code-corpus-id>" \
  --guides-corpus-id "<guides-corpus-id>" \
  --run-feed-dry-run
```

Plan the live retrieval scorecard before calling K2:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli plan-live-eval \
  --project-id "<project-id>" \
  --flink-docs-corpus-id "<docs-corpus-id>" \
  --flink-code-corpus-id "<code-corpus-id>" \
  --guides-corpus-id "<guides-corpus-id>"
```

Run the live scorecard after readiness probes pass:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli run-live-eval \
  --execute \
  --project-id "<project-id>" \
  --flink-docs-corpus-id "<docs-corpus-id>" \
  --flink-code-corpus-id "<code-corpus-id>" \
  --guides-corpus-id "<guides-corpus-id>"
```

## Live Demo Flow

1. Show the customer task:

```text
You are adding a new REST endpoint to Apache Flink that exposes a checkpoint
summary for a running job. Identify the right module, handler pattern, route
registration pattern, request/response message classes, and test locations.
Produce an implementation plan with source citations before editing code.
```

2. Run baseline Claude/Codex without K2. Ask for the plan and call out missing
   citations, stale guesses, wrong module assumptions, or missing test paths.
3. Run repo-only Claude/Codex. Allow local search and file reads, but do not
   provide K2 context. Show that success depends on the agent guessing the right
   terms and manually stitching together docs, source, and tests.
4. Run the strongest vanilla baseline, `codex_repo_plus_guides_dump`, with the
   same local repository and local Confluence-style guide dump. This is the fair
   customer comparison for "Codex with a folder of code and Confluence exports."
5. Enable the K2 skill and MCP tools. Require the agent to retrieve with
   metadata filters before planning or editing.
6. Use K2 Agents in this order: `java_rd_guides_agent` for conventions,
   `flink_docs_agent` for release-specific docs, and `flink_code_agent` for
   source and test patterns.
7. Show Knowledge Feeds as the durable loop: repeated findings from docs, code,
   and tests are materialized into reusable guide documents instead of staying
   trapped in one chat transcript.
8. Compare the outputs with `score-sample`, `score-customer-value`, the patch
   benchmark, and a human scorecard:
   artifact recall, time to correct plan, citation coverage, exact identifier
   accuracy, test plan quality, and hallucination count.
9. Use `score-customer-value --include-kafka --format markdown` to show the
   enterprise-specific value claim: repo-only search can find code and tests,
   while K2 is evaluated on whether the agent also found and applied the
   Confluence-style guide guardrails.

## Required K2 Retrieval Filters

For the Flink REST endpoint task, use metadata filters before broad search:

- Docs and guide conventions: `framework=flink`,
  `framework_version=2.2.0`, `source_kind in [docs, guide]`,
  `api_surface in [checkpointing, rest]`.
- Production code patterns: `framework=flink`, `framework_version=2.2.0`,
  `source_kind=code`, `module=flink-runtime`, `api_surface=rest`,
  `stability!=test_only`.
- Test patterns: `framework=flink`, `framework_version=2.2.0`,
  `source_kind=test`, `module=flink-runtime`, `api_surface=rest`.
- Exact class lookup: `framework=flink`, `language=java`,
  `class_name text_match RestHandler` or the class fragment under discussion.

For Kafka Connect tasks, filter to `framework=kafka`,
`framework_version=4.2.0`, `api_surface=connect`, and
`source_kind in [docs, code, test]`.

## Presenter Talking Points

- Metadata filters turn a large Java estate into routable context. The agent can
  ask for the current release, the right module, production code only, tests
  only, or engineering guides without dragging stale or unrelated pages into the
  answer.
- Knowledge Feeds matter for Confluence-style teams because hard-won patterns
  become durable guide pages. The next agent run starts from the current
  convention instead of rediscovering it from scattered docs, source files, and
  old tickets.
- Legacy Java R&D has many exact identifiers: class names, config keys, REST
  routes, exception names, Maven modules, and package names. K2 hybrid retrieval
  combines semantic, lexical, and metadata-sparse signals so these identifiers
  stay visible.
- K2 Agents encode the retrieval workflow. Guides explain conventions, docs
  anchor release-specific behavior, code shows implementation patterns, and
  tests reveal validation style.
- The demo is credible because Flink and Kafka have the same shape as customer
  platforms: large Java repositories, version-specific documentation, module
  boundaries, and many tests.
- The customer-specific win condition is guardrail compliance, not just answer
  style. A repo-only answer can be concise and still be wrong for the company if
  it ignores the internal controller, compatibility, audit, or testing rules
  that live outside the repository.

## Close

End by showing the K2-assisted plan with citations beside the baseline output.
The customer should see fewer guesses, better file and test recall, and a clear
path from Confluence-style guides to implementation-ready agent context.
