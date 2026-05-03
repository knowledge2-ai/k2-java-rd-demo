# Customer-Value Guardrail Demo

Date: 2026-05-03

## Purpose

This demo answers the customer question directly: K2 is useful for a legacy Java
shop when the coding agent must follow organization-specific guide pages, not
only search local Java files.

The demo should not claim that K2 beats `rg` for exact file lookup. The stronger
and more defensible claim is that K2 gives the agent governed cross-corpus
context: Confluence-style guardrails, version-pinned docs, production code, and
neighboring tests.

## What Was Built

- Generated guide assets now include Confluence-style guardrail pages:
  - `CF-FLINK-REST-001` for Flink REST handler/controller-like changes.
  - `CF-FLINK-CKPT-004` for Flink checkpointing upgrade compatibility.
  - `CF-KAFKA-CONNECT-007` for Kafka Connect REST entity compatibility.
- A new CLI scorecard models three customer-facing arms:
  - `baseline_no_retrieval`
  - `repo_only`
  - `k2_guides_docs_code_tests`
- The scorecard separates code lookup from enterprise guardrail compliance.

Command:

```bash
PYTHONPATH=src python -m k2_java_rd_demo.cli score-customer-value \
  --include-kafka \
  --format markdown
```

## Dry-Run Result

| Arm | Scenarios | Passed | Mean score |
| --- | ---: | ---: | ---: |
| `baseline_no_retrieval` | `3` | `0` | `0` |
| `repo_only` | `3` | `0` | `0.4625` |
| `k2_guides_docs_code_tests` | `3` | `3` | `1` |

## Why This Matters

Repo-only search can find implementation classes and tests. That is useful, but
it still misses the customer-specific policy layer when the policy lives in
Confluence rather than source code.

The K2-assisted arm is scored on whether the agent found and applied:

- the governing guide/guardrail ID;
- production implementation anchors;
- neighboring test anchors;
- required implementation terms;
- absence of forbidden patterns such as Spring MVC, JAX-RS, servlet controllers,
  deprecated checkpoint backends, Bean Validation, or `javax.validation`.

## Demo Framing

Use this as the customer story:

> The value of K2 is not replacing IntelliJ or `rg`. The value is making an AI
> coding agent organization-aware and auditable before it edits code.

The live demo should show the same task three ways:

1. Baseline agent produces a plausible generic Java plan.
2. Repo-only agent finds useful files and tests but has no way to know the
   Confluence guardrails.
3. K2-assisted agent retrieves the internal guide first, then docs/code/tests,
   and produces a plan with cited guardrail compliance.

## Limitation

This scorecard is a deterministic dry-run model. It is useful for demo design
and for preventing the public story from drifting back to "K2 beats grep." It is
not a measured live Codex/Claude benchmark until the same scenarios are run
through the real K2 MCP path with captured traces, generated code, time, tokens,
tests, and LLM-as-judge review.
