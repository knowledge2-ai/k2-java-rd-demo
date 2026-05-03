---
name: k2-java-rd-demo
description: Use K2 context for the Java R&D demo when Claude, Codex, or another coding agent must plan legacy Java changes with metadata-filtered docs, code, tests, guides, K2 Agents, Knowledge Feeds, and source citations before edits.
---

# K2 Java R&D Demo

Use this skill for Apache Flink or Kafka demo tasks that compare baseline
Claude/Codex against K2-assisted coding-agent behavior.

## Rules

1. Do not edit code until the plan cites retrieved docs, code, and tests.
2. When the benchmark arm permits K2, start with the narrowest docs/code/tests
   filters that match the framework, version, source kind, module, and API
   surface. Broaden only when filtered retrieval misses required evidence.
3. Search guides first for conventions, docs second for release behavior,
   code third for implementation patterns, and tests fourth for validation
   patterns.
4. For customer-value tasks, name the retrieved Confluence-style guardrail ID
   before proposing code changes, for example `CF-FLINK-REST-001` or
   `CF-KAFKA-CONNECT-007`.
5. If K2 results conflict with the local checkout, trust local files for exact
   contents and use K2 as navigation context.
6. Never request or store K2 keys in files. K2 credentials must come from
   environment variables such as `K2_API_KEY` and `K2_API_HOST`.
7. Do not claim metadata filters caused a win unless a filters-off ablation on
   the same task slice supports that claim.

## Filters

Use these metadata filters for Flink 2.2 REST and checkpointing work:

- Guides/docs: `framework=flink`, `framework_version=2.2.0`,
  `source_kind in [docs, guide]`, `api_surface in [checkpointing, rest]`.
- Production code: `framework=flink`, `framework_version=2.2.0`,
  `source_kind=code`, `module=flink-runtime`, `api_surface=rest`,
  `stability!=test_only`.
- Tests: `framework=flink`, `framework_version=2.2.0`, `source_kind=test`,
  `module=flink-runtime`, `api_surface=rest`.
- Class lookup: `framework=flink`, `language=java`,
  `class_name text_match <ClassFragment>`.

Use this filter for Kafka Connect work: `framework=kafka`,
`framework_version=4.2.0`, `api_surface=connect`, and
`source_kind in [docs, code, test]`.

## Agent Route

- Ask `java_rd_guides_agent` for conventions and Confluence-style guidance.
- Ask `flink_docs_agent` for version-specific Flink docs and source URLs.
- Ask `flink_code_agent` for source paths, class names, and neighboring tests.
- Use Knowledge Feeds when a recurring cross-corpus finding should become a
  reusable guide artifact.

## Required Output Before Edits

Before changing code, produce a short plan that includes:

- cited docs URLs or guide paths for the convention,
- cited production source paths/classes for the implementation pattern,
- cited test paths/helpers for validation,
- exact metadata filters used,
- open uncertainties that require local file inspection.
