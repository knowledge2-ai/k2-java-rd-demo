# Patch-Generation Benchmark Plan

This benchmark layer measures whether K2 helps a coding agent produce better
code, not just better grounded answers.

It complements the 100-question retrieval benchmark:

- Retrieval benchmark: source grounding, answer quality, and evidence coverage.
- Patch benchmark: final code diff, focused verification, wall-clock time, and
  Codex token/tool metrics.

## Arms

| Arm | Repository access | K2 MCP | Web/browser |
| --- | --- | --- | --- |
| `codex_repo_only` | writable local checkout, shell/file tools | no | disabled |
| `codex_repo_plus_docs` | writable local checkout, shell/file tools, declared local docs paths and version-pinned docs URLs | no | disabled |
| `codex_repo_plus_guides_dump` | writable local checkout, shell/file tools, declared docs, local Confluence-style guide dump | no | disabled |
| `codex_with_k2_mcp` | writable local checkout, shell/file tools | yes | disabled |
| `codex_with_k2_mcp_no_guides` | writable local checkout, shell/file tools | yes, guide tool disabled | disabled |
| `codex_with_k2_mcp_filters_off` | writable local checkout, shell/file tools | yes, metadata filters disabled | disabled |

The no-tool baseline is intentionally omitted. It is useful for Q&A, but it is
not a fair feature-development baseline because an agent must inspect and edit
files.

## Built-In Tasks

The initial task set is deliberately small and source-local:

| Task | Framework | Goal |
| --- | --- | --- |
| `flink-rest-job-vertex-watermarks-include-missing` | Flink 2.2 | Add optional missing-subtask reporting to `JobVertexWatermarksHandler` and focused handler coverage |
| `flink-rest-cluster-overview-optional-cluster-id` | Flink 2.2 | Add optional `cluster-id` to `ClusterOverviewWithVersion` and marshalling coverage |
| `kafka-connect-plugin-info-optional-location` | Kafka 4.2 | Add optional `location` to `PluginInfo` and focused JSON coverage |
| `kafka-connect-create-connector-request-validate-only` | Kafka 4.2 | Add optional `validate_only` to `CreateConnectorRequest` and entity coverage |

These are not intended to be secretly merged upstream. They are controlled
feature requests that force the agent to find existing Java patterns, keep
compatibility, edit a small code surface, and update tests.

## Metrics

Each task-arm run records:

- Final `git diff --binary` patch, including newly created untracked files.
- Changed files.
- Expected-file coverage.
- Out-of-scope file changes.
- `git diff --check` result.
- Lightweight same-project Java import-resolution check.
- Guide guardrail score when a task declares Confluence-style guardrails.
- Forbidden-pattern safety score from the applicable guide.
- Optional task-specific test command result when `--run-tests` is set.
- Local verifier command resolution, for example `./mvnw` to `mvn` when a
  wrapperless OSS checkout is tested with a local Maven install.
- Task class, failure categories, and the predeclared signal-assessment verdict.
- Wall-clock duration in seconds.
- Best-effort Codex token metrics from JSON events.
- Tool counts inferred from Codex JSON events.
- MCP tool failure counts inferred from Codex JSON events.

The scoring expected paths are stored in the task metadata and report, but the
agent prompt only receives the feature request, success criteria, and allowed
edit neighborhoods. This avoids turning the patch benchmark into a pure
golden-file lookup task.

For the `codex_repo_plus_guides_dump` arm, the prompt may list the local
`.k2-demo-confluence-dump/...` guide file path, but it must not expose the
required guardrail ID or generated guide source URI. The final answer has to
surface the guardrail by reading the local guide dump. The K2 arm has to surface
the same guardrail through MCP retrieval.

The deterministic score is the mean of available source-level checks:

```text
score = mean(
  expected_file_coverage,
  scope_score,
  diff_present,
  guide_guardrail_score when answer text and guide expectations are present,
  verification_score when verification was run
)
```

The guide guardrail score requires:

- all required guardrail IDs in the final answer or patch evidence;
- at least one guide citation, either the K2 source URI or local guide-dump
  path;
- no forbidden implementation markers from the applicable guide.

The task pass condition requires a score of at least `0.8`, guide guardrail
score of `1.0` when applicable, and all verification checks to pass. This score
is intentionally simple. It is useful for dashboards and spotting obvious
failures, but it is not a substitute for human code review or a blinded LLM
judge over final patches.

For K2 arms, any failed K2 MCP tool call is also a run failure. This prevents a
K2-labeled run from silently falling back to local repository search and being
mistaken for a successful K2-assisted result.

The runner also performs live preflight checks before launching Codex. SDK runs
require `K2_API_KEY` after loading `--env-file`; kubectl runs require permission
to read the configured deployment in the target namespace. Add
`--probe-k2-sdk` to require one live SDK retrieval against the Flink REST corpus
before any benchmark result can be treated as K2-backed.

## Decision Rule

The benchmark applies a conservative signal rule to the customer-relevant
paired `codex_repo_plus_guides_dump` and `codex_with_k2_mcp` runs:

```text
K2 wins only if:
  paired_task_count >= 10
  and K2 pass_rate >= guide_dump_baseline pass_rate + 15 percentage points
  and K2 mean guide guardrail score is at least the guide_dump_baseline score
  and K2 median/mean duration is not more than 30% slower
  and K2 token_ratio <= 0.90 for token-savings claims
```

If fewer than 10 paired tasks are present, the report verdict is
`insufficient_sample`. If the pass-rate delta is within +/-5 points, the verdict
is `no_clear_k2_win`. Anything in between is reported as
`mixed_or_task_dependent` and should be split by task class. If K2 improves
quality but does not reduce tokens, publish that as a quality result only.

The built-in catalog currently contains 12 small Java feature tasks across
Flink REST response/message classes and Kafka Connect REST entities. Ten of the
12 require generated Confluence-style guardrails, which makes the benchmark
large enough for the decision rule while preserving customer-relevant guide
compliance pressure.

## Running

Dry-run the task catalog:

```bash
python scripts/run_patch_generation_benchmark.py --max-tasks 2
```

Check live K2 readiness without launching Codex:

```bash
python scripts/run_patch_generation_benchmark.py \
  --preflight-only \
  --probe-k2-sdk \
  --arm codex_repo_plus_guides_dump \
  --arm codex_with_k2_mcp \
  --mcp-backend sdk \
  --env-file .env
```

Run the full claim-grade sequence:

```bash
python scripts/run_claim_grade_patch_benchmark.py \
  --env-file .env
```

This wrapper performs the preflight probe, runs both benchmark arms with focused
tests, writes `patch-scorecard.json`, writes `patch-scorecard-audit.json` and
`patch-scorecard-audit.md`, and exits non-zero unless the audit is claim-ready.

Run both arms without expensive framework tests:

```bash
python scripts/run_patch_generation_benchmark.py \
  --execute \
  --probe-k2-sdk \
  --arm codex_repo_plus_guides_dump \
  --arm codex_with_k2_mcp \
  --mcp-backend sdk \
  --retrieval-profile java_exact \
  --env-file .env
```

Run focused task tests as well:

```bash
python scripts/run_patch_generation_benchmark.py \
  --execute \
  --probe-k2-sdk \
  --arm codex_repo_plus_guides_dump \
  --arm codex_with_k2_mcp \
  --mcp-backend sdk \
  --retrieval-profile java_exact \
  --env-file .env \
  --run-tests
```

For Flink tasks, the focused Maven command includes environment compatibility
flags such as `-Denforcer.skip=true` and `-Dsurefire.module.config.jdk21=` so a
wrapperless local checkout can still execute the target unit test on newer local
toolchains. These flags avoid demo-machine Maven/JDK gates; they do not skip the
focused unit test itself.

Outputs are written under `docs/evaluations/patch-runs/<run-id>/`:

- `patch-scorecard.json`
- `patch-report.md`
- `artifacts/<task>/<arm>/prompt.txt`
- `artifacts/<task>/<arm>/answer.md`
- `artifacts/<task>/<arm>/patch.diff`
- `artifacts/<task>/<arm>/codex-events.jsonl`
- `artifacts/<task>/<arm>/verification.json`

Audit the scorecard before publishing a K2 customer-value claim:

```bash
python scripts/verify_patch_generation_scorecard.py \
  docs/evaluations/patch-runs/<run-id>/patch-scorecard.json \
  --require-focused-tests
```

The audit recomputes the decision rule and rejects the claim if the run is
under-sampled, lacks a live K2 SDK probe, lacks recorded K2 MCP tool calls,
contains K2 tool failures, lacks token metrics, lacks focused test evidence, or
does not satisfy the documented quality, guide-score, duration, and token
thresholds.

## Publication Guidance

Use this benchmark for a narrower and stronger claim:

> On controlled Java feature-development tasks, K2-assisted Codex can be
> compared against vanilla Codex with the same local repository and
> Confluence-style guide dump by final patch quality, focused tests,
> guide compliance, time-to-patch, and token usage.

Do not report a product claim until at least 10 paired tasks have completed
with focused verification and either human review or a blinded patch judge.
