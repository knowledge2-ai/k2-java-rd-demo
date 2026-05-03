# K2 Java R&D Demo

This is a Python evaluation harness measuring K2's effect on coding agents
working over Java codebases. It does not contain a Java SDK or Java application.

The repository builds a customer demo for K2 as a context platform for coding
agents working in large legacy Java codebases.

The demo starts with public OSS stand-ins:

- Apache Flink docs and source code as the primary legacy-Java analogue.
- Apache Kafka docs and source code as an optional second platform.
- Generated Confluence-like guide documents derived from docs/code patterns.

The final customer demo should include K2 Search, K2 Agents, Knowledge Feeds,
and MCP-served retrieval over docs, source, tests, and generated guides.
Metadata filters and metadata-sparse retrieval are part of the system design,
but the current public evidence should be framed around the measured recall
and source-grounding delta against local `rg`/filesystem search.

## Repository Layout

```text
docs/designs/      Architecture/design docs
src/               Demo package
tests/             Offline unit tests
```

## Local Setup

This package uses only the Python standard library for the offline dry-run path.

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli --help
PYTHONPATH=src python -m unittest discover -s tests
PYTHONPATH=src python -m unittest discover -s tests/e2e
```

## Dry-Run Code Asset Build

Plan deterministic sparse checkouts for Flink and optional Kafka:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli plan-repo-checkout --include-kafka \
  --base-dir /tmp/k2-java-rd-demo-sources
```

After running the printed `git` commands, point the builder at a local checkout
of Flink or Kafka:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli build-code-assets \
  --repo-root /path/to/flink \
  --framework flink \
  --version 2.2.0 \
  --repo apache/flink \
  --repo-ref release-2.2.0 \
  --out /tmp/flink-code.jsonl \
  --max-files 200
```

Validate the generated asset:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli probe-jsonl \
  --input /tmp/flink-code.jsonl
```

## Dry-Run Docs Asset Build

Preview docs URLs discovered from sitemaps or seed pages:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli discover-docs-urls \
  --framework flink \
  --max-pages 25
```

Harvest public docs pages into K2-ready JSONL:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli build-docs-assets \
  --framework flink \
  --max-pages 25 \
  --out /tmp/flink-docs.jsonl
```

## Dry-Run Guide Asset Build

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli build-guides \
  --framework flink \
  --version 2.2.0 \
  --out /tmp/java-rd-guides.jsonl
```

## Inspect K2 Recipes

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli show-config
PYTHONPATH=src python -m k2_java_rd_demo.cli show-source-manifest --include-kafka
PYTHONPATH=src python -m k2_java_rd_demo.cli plan-repo-checkout --include-kafka
PYTHONPATH=src python -m k2_java_rd_demo.cli show-agent-specs
PYTHONPATH=src python -m k2_java_rd_demo.cli show-readiness-probes
PYTHONPATH=src python -m k2_java_rd_demo.cli show-eval-cases --include-kafka
PYTHONPATH=src python -m k2_java_rd_demo.cli show-mcp-contract --include-kafka
PYTHONPATH=src python -m k2_java_rd_demo.cli score-sample
PYTHONPATH=src python -m k2_java_rd_demo.cli score-demo-cases --include-kafka
PYTHONPATH=src python -m k2_java_rd_demo.cli score-customer-value \
  --include-kafka \
  --format markdown
```

Run the customer-relevant feature-development benchmark after K2 credentials and
source checkouts are available. The default catalog contains 12 paired
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

Audit a generated scorecard before making any public K2 claim:

```bash
python scripts/verify_patch_generation_scorecard.py \
  docs/evaluations/patch-runs/<run-id>/patch-scorecard.json \
  --require-focused-tests
```

Validate Agent and Knowledge Feed specs after you have concrete corpus IDs:

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

Execute the live K2 upload/index/probe flow only after validating the plan:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli run-live-k2 \
  --execute \
  --jsonl /tmp/java-rd-guides.jsonl \
  --project-id "<project-id>" \
  --guides-corpus-id "<guides-corpus-id>" \
  --idempotency-prefix java-rd-demo
```

Create K2 Agents and the Knowledge Feed after the docs/code/guides corpora are
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

The live commands refuse to call K2 unless `--execute` is present.

Plan live scorecard searches without calling K2:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli plan-live-eval \
  --project-id "<project-id>" \
  --flink-docs-corpus-id "<flink-docs-corpus-id>" \
  --flink-code-corpus-id "<flink-code-corpus-id>" \
  --guides-corpus-id "<guides-corpus-id>"
```

Execute the live retrieval scorecard after corpora are indexed:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli run-live-eval \
  --execute \
  --project-id "<project-id>" \
  --flink-docs-corpus-id "<flink-docs-corpus-id>" \
  --flink-code-corpus-id "<flink-code-corpus-id>" \
  --guides-corpus-id "<guides-corpus-id>"
```

## Customer Demo Packaging

- Demo runbook: `docs/runbooks/customer-demo-runbook.md`
- Public evaluation methodology and results: `docs/evaluations/2026-05-01-public-methodology-report.md`
- Concise blog basis with fair-baseline, second-judge, and ablation results:
  `docs/evaluations/2026-05-02-blog-basis.md`
- Full 100-case question catalog:
  `docs/evaluations/2026-05-02-question-catalog.md`
- Patch-generation benchmark plan:
  `docs/evaluations/2026-05-02-patch-generation-benchmark.md`
- Feature-development validation strategy:
  `docs/evaluations/2026-05-02-feature-development-validation-strategy.md`
- Customer-value guardrail demo:
  `docs/evaluations/2026-05-03-customer-value-guardrail-demo.md`
- Corrected 100-case real MCP run: `docs/evaluations/runs/20260501T134908Z-real-mcp/report.md`
- Retrieval-capable baseline extension:
  `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260501T231541Z-extension-arms/extension-report.md`
- K2 vs `rg` judge-family comparison:
  `docs/evaluations/runs/20260501T134908Z-real-mcp/extension-runs/20260501T231541Z-extension-arms/llm-judge-runs/judge-family-comparison-k2-vs-rg.md`
- K2 answer-style tuning follow-up:
  `docs/evaluations/2026-05-03-k2-answer-style-tuning.md`
- Claude/Codex skill package: `skills/k2-java-rd-demo/SKILL.md`
- Deterministic source manifest: `show-source-manifest`
- Reusable evaluation catalog: `show-eval-cases`
- MCP tool contract: `show-mcp-contract`
- Live retrieval scorecard: `plan-live-eval` and `run-live-eval --execute`

The runbook presents the customer-facing story across baseline Claude/Codex,
repo-only Claude/Codex, and K2-assisted Claude/Codex with K2 Agents,
Knowledge Feeds, and source-grounded MCP retrieval.

## Credential Handling

Do not commit K2 keys or customer data. Live K2 execution reads credentials only
from environment variables, for example:

```bash
export K2_API_KEY="..."
export K2_API_HOST="https://api.knowledge2.ai"
```

Rotate any credential that may have appeared in chat, logs, terminals, or other
non-secret storage before using it for a customer-facing demo.

## Evaluation Status

The included 2026-05-01/2026-05-02 artifacts are controlled
evidence-grounding comparisons across three relevant arms: Codex with no
retrieval tools, Codex with local `rg`/filesystem access to the same sparse
Flink/Kafka source checkouts, and Codex connected to K2 through MCP. They are
useful for demonstrating source grounding, metadata, MCP traces, and the gap
between repository-only search and K2's cross-corpus retrieval.
The fair-baseline LLM judges prefer the `rg`/filesystem answers over K2 answers,
so public copy should not claim human-preferred answer quality from the
retrieval benchmark without further prompt work and human review.
The answer-style tuning follow-up improves deterministic evidence on a two-case
smoke run, but the Codex-family and Claude-family judges still disagree, so the
next retrieval product step is method-level snippets and line-span evidence.

These retrieval artifacts should still not be presented as a general coding
benchmark: the cases are class-anchored and the metadata-filter ablation is only
a 20-case slice.

The patch-generation benchmark adds a separate measurement layer for
feature-development tasks. The first smoke run
(`docs/evaluations/patch-runs/20260502T085752Z-patch-generation/`) completed one
Flink task with focused Maven verification for both repo-only Codex and
K2-assisted Codex. Both arms passed. It should still be run on at least 10
paired, verified tasks using the stronger `codex_repo_plus_guides_dump`
baseline before making a public engineering-productivity claim.
The predeclared decision rule and falsification plan are captured in
`docs/evaluations/2026-05-02-feature-development-validation-strategy.md`.

The customer-value guardrail scorecard adds the missing enterprise framing:
baseline and repo-only agents can produce plausible Java plans, but they do not
see Confluence-style internal rules. The `score-customer-value` command models
this explicitly across baseline, repo-only, and K2-assisted arms. Treat it as a
demo design and scoring harness; live customer proof still requires running the
same tasks through the real MCP/K2 path with retrieved guide, docs, code, and
test evidence.

## Planned Live K2 Flow

1. Build or load deterministic JSONL assets.
2. Create project and corpora.
3. Upload docs/code/guides with K2 SDK.
4. Build dense, sparse, and metadata-sparse indexes.
5. Create K2 Agents for docs, code, tests, and guides.
6. Create Knowledge Feeds that materialize cross-corpus guide artifacts.
7. Expose source-grounded MCP tools to Claude Code or Codex.
8. Run the baseline vs K2-assisted coding-agent scorecard.
9. Run the patch-generation benchmark for final code output, time, and tokens.

The live orchestration modules are duck-typed and offline-tested. They do not
import the K2 SDK directly; later live scripts can pass a real `Knowledge2`
client while tests keep using fake clients.
