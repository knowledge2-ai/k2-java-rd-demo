# K2 Java R&D Demo Architecture

Date: 2026-04-25

## Executive Summary

This demo should show a practical R&D workflow, not a generic chatbot. The
customer has a large legacy Java application plus Confluence guides describing
controllers, modules, conventions, tests, and release practices. Since we do
not have their code or Confluence data, use Apache Flink as the primary stand-in
and Apache Kafka as the optional second corpus:

- Flink is a large Java codebase with release-specific documentation, REST API
  surfaces, runtime modules, tests, configuration, and connector docs.
- Kafka adds a second Java platform with Kafka Connect and Streams docs, useful
  for demonstrating multi-corpus routing and exact identifier lookup.
- The K2-assisted agent gets structured retrieval over docs, source, tests, and
  generated "Confluence-like" guides. The baseline agent gets the same task
  prompt without K2 retrieval context.

The key message is:

> K2 turns scattered engineering knowledge into a filterable, version-aware,
> source-cited context layer for coding agents. The agent stops guessing where
> conventions live and starts grounding each change plan in the right docs,
> modules, classes, and tests.

## Source Baseline

Public source material verified for this design:

- Apache Flink v2.2.0 documentation: `https://nightlies.apache.org/flink/flink-docs-release-2.2/`
  - The page identifies the docs version as `v2.2.0`.
  - It includes Java/R&D-relevant sections such as DataStream API, Table API,
    REST API, connectors, deployment, operations, and Flink development.
  - Page shows documentation built on 2026-04-24.
- Apache Kafka 4.2 docs: `https://kafka.apache.org/42/`
  - The page is the Apache Kafka 4.2.x documentation entrypoint.
  - It includes API, configuration, design, implementation, operations,
    Kafka Connect, and Kafka Streams sections.
  - Page shows last modified on 2026-02-16.
- Kafka Connector Development Guide:
  `https://kafka.apache.org/42/kafka-connect/connector-development-guide/`

Local K2 assets to reuse:

- `/Users/antonmishel/k2/devops/k2-sdk-validation/examples/website_expert.py`
  - Use as the starting point for URL discovery, URL ingestion, indexing, and
    `search_generate` demo answers.
- `/Users/antonmishel/k2/devops/k2-sdk-validation/examples/eval_website_expert.py`
  - Use as the starting point for a scorecard harness.
- `/Users/antonmishel/k2/devops/mcp-server-k2`
  - Existing Claude Code MCP server with `k2_search`, indexing, corpus status,
    corpus creation, and index build tools.
- `/Users/antonmishel/k2/devops/k2_mvp/examples/04_multi_corpus_agent`
  - Existing multi-corpus routing example.
- `/Users/antonmishel/k2/devops/k2_mvp/examples/08_retrieval_benchmark`
  - Existing retrieval benchmark pattern for apples-to-apples evaluation.

## Demo Goals

1. Show that K2 improves agent code navigation for a large Java platform.
2. Show docs + code + tests + conventions retrieved together with citations.
3. Show metadata filters scoping retrieval by framework, version, module,
   source kind, language, API surface, and test status.
4. Show exact technical identifiers found through hybrid sparse and
   metadata-sparse retrieval, not only semantic embeddings.
5. Show an eval harness that measures retrieval success, not only a polished
   one-off answer.
6. Leave a customer-facing path from OSS demo to their real Confluence +
   monorepo ingestion.

## Non-Goals

- Do not claim Flink/Kafka are identical to the customer's system. They are
  stand-ins for large Java R&D knowledge.
- Do not ingest or expose private customer data in this demo.
- Do not hard-code production K2 credentials into scripts, docs, MCP config, or
  shell history. Use environment variables only.
- Do not benchmark against external LLM providers with proprietary customer
  material. Public OSS data is safe for this demo.

## Demo Storyline

Run the same engineering task three ways:

| Mode | Agent Context | Expected Behavior |
| --- | --- | --- |
| A. No K2 | Task prompt only | Generic Java/Flink guesses, weak or no citations. |
| B. Repo only | Local OSS repo and grep tools | Can eventually find files, but misses docs/test conventions unless it searches well. |
| C. K2-assisted | Local repo plus K2 MCP/skill retrieval over docs, code, tests, and guides | Finds the right docs, modules, implementation classes, tests, and version-specific constraints quickly, with citations. |

The most convincing demo is Mode B vs Mode C because it mirrors Claude Code or
Codex in a real legacy repo. The value is not "the model cannot grep"; it is
"the model can ask a knowledge layer that already understands docs, code,
tests, versions, modules, and conventions."

## Recommended Demo Tasks

### Task 1: Flink REST Handler / Controller Analogue

Prompt:

```text
You are adding a new REST endpoint to Apache Flink that exposes a checkpoint
summary for a running job. Identify the right module, handler pattern, route
registration pattern, request/response message classes, and test locations.
Produce an implementation plan with source citations before editing code.
```

Why it maps to the customer:

- "Add a controller" is a common enterprise Java workflow.
- Flink REST handlers provide a controller-like analogue without needing
  Spring.
- The correct answer requires docs, runtime code, message classes, routing, and
  tests.

Expected K2-assisted behavior:

- Search Flink docs filtered to `topic=rest-api` and `topic=checkpointing`.
- Search Flink source filtered to `module=flink-runtime`, `source_kind=code`,
  `api_surface=rest`.
- Search tests filtered to `source_kind=test`, `module=flink-runtime`,
  `api_surface=rest`.
- Return a plan citing the docs URL, handler classes, message classes, and test
  paths.

### Task 2: Kafka Connect Validation Rule

Prompt:

```text
Add a validation rule to a Kafka Connect connector-style configuration. Find the
docs that explain connector development, the code patterns for ConfigDef-based
validation, and the tests that should be copied. Produce the plan with citations.
```

Why it works:

- It demonstrates exact identifier lookup, especially `ConfigDef`, connector
  terms, and config keys.
- It shows K2 routing between Kafka docs, Kafka code, and tests.

### Task 3: Version-Specific Upgrade Guidance

Prompt:

```text
We need to upgrade a streaming application from the previous release to the
current Flink 2.2 docs. Find the version-specific upgrade notes and the code or
tests most likely affected by DataStream state/checkpointing changes.
```

Why it works:

- Version filters matter.
- K2 can keep release-specific corpora separate and prevent stale docs from
  contaminating the answer.

## Target Architecture

```text
                 Public OSS sources
        +--------------------------------+
        | Flink docs 2.2 / Kafka docs 4.2|
        | Flink code / Kafka code        |
        | Curated Confluence-like guides |
        +---------------+----------------+
                        |
                        v
              Demo ingestion pipeline
        +--------------------------------+
        | website_expert URL discovery   |
        | code parser / metadata enricher|
        | deterministic manifest builder |
        +---------------+----------------+
                        |
                        v
                    K2 project
        +--------------------------------+
        | Corpus: flink-docs-2.2         |
        | Corpus: flink-code-2.2         |
        | Corpus: kafka-docs-4.2         |
        | Corpus: kafka-code-4.2         |
        | Optional: java-rd-guides       |
        +---------------+----------------+
                        |
                        v
         Dense + text BM25 + metadata BM25
        +--------------------------------+
        | K2 search / search_generate    |
        | metadata filters               |
        | provenance + scores            |
        +---------------+----------------+
                        |
                        v
        Claude Code / Codex via MCP + skill
        +--------------------------------+
        | k2_search_docs                 |
        | k2_search_code                 |
        | k2_search_tests                |
        | k2_answer_with_sources         |
        +--------------------------------+
```

## Corpus Strategy

Use separate corpora during the demo rather than one large mixed corpus. This
makes routing visible and gives the presenter clean examples of scoped search.

| Corpus | Contents | Purpose |
| --- | --- | --- |
| `flink-docs-2.2` | Flink 2.2 docs pages and selected Javadocs | Release-specific documentation and how-to guidance. |
| `flink-code-2.2` | Java/Scala source, tests, build files, examples | Implementation patterns and test conventions. |
| `kafka-docs-4.2` | Kafka 4.2 docs and Kafka Connect guide | Optional second platform; demonstrates corpus routing. |
| `kafka-code-4.2` | Kafka source, tests, examples | Optional code pattern corpus. |
| `java-rd-guides` | Generated guides derived from docs/code, written like Confluence pages | Mirrors customer Confluence: "how to add a controller", "module map", "test checklist". |

For the first customer-facing demo, use Flink docs + Flink code + generated
guides as the core. Add Kafka only if there is time to show multi-corpus routing.

## Ingestion Plan

### Phase 1: Fast Prototype

Use the SDK directly:

1. Create a project: `java-rd-demo`.
2. Create the corpora listed above.
3. Use `ingest_urls(..., auto_index=False)` for public docs.
4. Clone the OSS repositories locally at pinned refs.
5. Run a code/document metadata enrichment script.
6. Upload code/guides with `upload_documents_batch_and_wait(..., auto_index=False)`.
7. Run `sync_indexes(corpus_id, wait=True)` once per corpus.
8. Run metadata readiness probes before showing the demo.

### Phase 2: Deterministic Demo Asset

For a repeatable launch demo, materialize all fetched docs and code documents
into a manifest backed by object storage. This matches the local K2 demo
metadata contract style: required metadata keys plus probe filters. URL ingestion
is useful for rapid iteration, but deterministic manifests make demos repeatable
and avoid live website drift.

## Metadata Design

K2 custom metadata has practical limits: keep the schema compact, normalized,
and filterable. Current platform validation allows up to 50 custom metadata keys,
10 KB total serialized metadata, and 1 KB per value. Sparse metadata indexing
also has server-side caps, so do not put giant symbol lists or full imports into
metadata.

Do not duplicate reserved/system fields such as `source_uri`, `document_id`,
`chunk_index`, `page_start`, or `page_end` in custom metadata. Set `source_uri`
as the document source field and let K2 system metadata carry it.

### Required Custom Metadata Keys

Every ingested document should include these keys:

| Key | Type | Examples | Purpose |
| --- | --- | --- | --- |
| `demo_dataset_id` | string | `java-rd-oss-2026-04` | Demo readiness and cleanup. |
| `corpus_role` | string | `docs`, `code`, `guides` | Coarse routing and probe checks. |
| `framework` | string | `flink`, `kafka` | Product/platform filter. |
| `framework_version` | string | `2.2.0`, `4.2.0` | Version isolation. |
| `source_kind` | string | `docs`, `code`, `test`, `build`, `config`, `guide` | Main retrieval scope. |
| `artifact_type` | string | `how_to`, `reference`, `source`, `unit_test`, `integration_test`, `build_config` | More precise artifact filter. |
| `language` | string | `java`, `scala`, `markdown`, `html`, `xml`, `properties` | Language/tooling filter. |
| `license` | string | `apache-2.0` | Compliance signal for OSS demo data. |
| `repo` | string | `apache/flink`, `apache/kafka`, `none` | Code provenance. |
| `repo_ref` | string | `release-2.2.0`, `4.2`, `docs-2.2` | Reproducibility. |
| `path` | string | `flink-runtime/src/.../Foo.java` | Code/document path display and filtering. |
| `module` | string | `flink-runtime`, `connect`, `streams`, `docs` | Main Java module filter. |
| `api_surface` | string | `rest`, `checkpointing`, `datastream`, `connect`, `streams`, `configuration` | Task-level routing. |
| `topic` | string | `rest-api`, `state`, `connector-development`, `testing` | Human-readable topic. |
| `audience` | string | `framework_contributor`, `application_developer`, `connector_author`, `platform_operator` | Customer-style guide targeting. |
| `stability` | string | `public_api`, `internal`, `test_only`, `experimental` | Avoid using test/internal examples accidentally. |
| `tags` | array[string] | `["controller-analog", "rest", "checkpointing"]` | Metadata sparse ranking and broad grouping. |

### Optional Code Metadata

Use these only for code/test documents. Keep values short.

| Key | Type | Examples | Notes |
| --- | --- | --- | --- |
| `java_package` | string | `org.apache.flink.runtime.rest.handler.job` | Better than putting package only in text. |
| `class_name` | string | `JobVertexDetailsHandler` | High-value exact lookup. |
| `symbol_kind` | string | `class`, `interface`, `enum`, `method_group` | Useful when splitting large files. |
| `symbols` | array[string] | `["handleRequest", "createMessageParameters"]` | Cap at 20 symbols or 1 KB. |
| `extends` | string | `AbstractRestHandler` | Helps find pattern inheritance. |
| `implements` | array[string] | `["SourceTask"]` | Cap aggressively. |
| `test_target` | string | `JobVertexDetailsHandler` | For test documents only. |
| `is_test` | boolean | `true`, `false` | Hard filter for tests. |

### Optional Documentation Metadata

Use these for docs/guides:

| Key | Type | Examples | Notes |
| --- | --- | --- | --- |
| `doc_section` | string | `Application Development`, `Kafka Connect` | Top-level docs navigation. |
| `nav_path` | string | `Application Development > DataStream API > Testing` | Keep under 1 KB. |
| `heading_path` | string | `REST API > Jobs > Checkpoints` | Good for `text_match`. |
| `guide_type` | string | `how_to`, `architecture`, `coding_standard`, `test_checklist`, `runbook` | Mirrors Confluence. |
| `doc_url_depth` | number | `3` | Optional quality/debugging signal. |

## Metadata Sparse Retrieval Strategy

Use metadata sparse retrieval as a ranking signal, not as a replacement for hard
filters. The strongest pattern is:

1. Apply hard filters for non-negotiable scope: framework, version, source kind,
   module, and test/code/docs split.
2. Let metadata sparse boost exact identifiers and structured hints:
   `class_name`, `api_surface`, `topic`, `tags`, `java_package`, and
   `heading_path`.
3. Use hybrid dense + text sparse for the actual content.

Recommended default search config for demo tools:

```python
DEMO_HYBRID = {
    "enabled": True,
    "fusion_mode": "rrf",
    "rrf_k": 60,
    "dense_weight": 0.60,
    "sparse_weight": 0.30,
    "metadata_sparse_weight": 0.10,
    "metadata_sparse_enabled": True,
}

DEMO_RETURN = {
    "include_text": True,
    "include_scores": True,
    "include_provenance": True,
}
```

Rationale:

- Dense retrieval handles conceptual prompts like "controller analogue" or
  "checkpoint summary".
- Text BM25 handles exact strings like class names, config keys, method names,
  and REST route fragments.
- Metadata BM25 boosts structured fields such as `module=flink-runtime`,
  `api_surface=rest`, or `class_name=...`.
- K2 normalizes enabled retrieval weights. For exact-identifier tasks, test a
  slightly higher `metadata_sparse_weight` such as `0.15`.
- RRF is a safer default for mixed corpora because it blends rank positions
  rather than relying on score comparability.

If the retriever emits metadata sparse diagnostics, show those in the demo log
to make the K2 capability visible.

## Filter Design

Prefer structured filters for anything customer-facing. Flat filters are fine
for quick scripts, but structured filters demonstrate K2's operator support and
map cleanly to UI/filter-builder concepts.

For restrictive filters, keep the corpus scoped and retrieve a slightly larger
candidate set. In the demo tools, use `top_k=12` to `20`, and if rerank is
enabled use `rerank.top_k=50`. This avoids a brittle demo where the query text is
too broad and the filter removes most of the initial candidates.

Supported operator patterns to demonstrate:

- Equality: `==`
- Negation: `!=`
- Lists: `in`, `not_in`
- Numeric/date comparisons when available: `>`, `>=`, `<`, `<=`
- Array/string containment: `contains`
- Text-ish metadata matching: `text_match`
- Boolean grouping: `condition: and` or `condition: or`

### Filter: Flink Docs Only

```python
FILTER_FLINK_DOCS_22 = {
    "condition": "and",
    "filters": [
        {"key": "demo_dataset_id", "op": "==", "value": "java-rd-oss-2026-04"},
        {"key": "framework", "op": "==", "value": "flink"},
        {"key": "framework_version", "op": "==", "value": "2.2.0"},
        {"key": "source_kind", "op": "==", "value": "docs"},
    ],
}
```

### Filter: Flink REST Controller Analogue

```python
FILTER_FLINK_REST_CODE = {
    "condition": "and",
    "filters": [
        {"key": "framework", "op": "==", "value": "flink"},
        {"key": "framework_version", "op": "==", "value": "2.2.0"},
        {"key": "source_kind", "op": "==", "value": "code"},
        {"key": "module", "op": "==", "value": "flink-runtime"},
        {"key": "api_surface", "op": "==", "value": "rest"},
        {"key": "stability", "op": "!=", "value": "test_only"},
    ],
}
```

### Filter: Flink REST Tests

```python
FILTER_FLINK_REST_TESTS = {
    "condition": "and",
    "filters": [
        {"key": "framework", "op": "==", "value": "flink"},
        {"key": "framework_version", "op": "==", "value": "2.2.0"},
        {"key": "source_kind", "op": "==", "value": "test"},
        {"key": "module", "op": "==", "value": "flink-runtime"},
        {"key": "api_surface", "op": "==", "value": "rest"},
    ],
}
```

### Filter: Topic Search Across Docs And Guides

```python
FILTER_FLINK_CHECKPOINT_DOCS_OR_GUIDES = {
    "condition": "and",
    "filters": [
        {"key": "framework", "op": "==", "value": "flink"},
        {"key": "framework_version", "op": "==", "value": "2.2.0"},
        {"key": "source_kind", "op": "in", "value": ["docs", "guide"]},
        {"key": "api_surface", "op": "in", "value": ["checkpointing", "rest"]},
    ],
}
```

### Filter: Kafka Connect Development

```python
FILTER_KAFKA_CONNECT = {
    "condition": "and",
    "filters": [
        {"key": "framework", "op": "==", "value": "kafka"},
        {"key": "framework_version", "op": "==", "value": "4.2.0"},
        {"key": "api_surface", "op": "==", "value": "connect"},
        {"key": "source_kind", "op": "in", "value": ["docs", "code", "test"]},
    ],
}
```

### Filter: Exact Class Lookup

```python
FILTER_CLASS_LOOKUP = {
    "condition": "and",
    "filters": [
        {"key": "framework", "op": "==", "value": "flink"},
        {"key": "language", "op": "==", "value": "java"},
        {"key": "class_name", "op": "text_match", "value": "RestHandler"},
    ],
}
```

### Probe Filters For Demo Readiness

Before the demo, run fixed probe queries. The goal is not just "search returns
something"; the goal is "filters return source-specific evidence."

```yaml
datasets:
  - dataset_id: java_rd_flink_docs_22
    required_metadata_keys:
      - demo_dataset_id
      - corpus_role
      - framework
      - framework_version
      - source_kind
      - artifact_type
      - module
      - api_surface
      - topic
      - tags
    probe_filter_query: "how do I add a REST API endpoint for checkpoint information"
    probe_filters:
      condition: and
      filters:
        - key: framework
          op: "=="
          value: flink
        - key: framework_version
          op: "=="
          value: "2.2.0"
        - key: source_kind
          op: "in"
          value: ["docs", "guide"]
        - key: api_surface
          op: "in"
          value: ["rest", "checkpointing"]
    probe_min_results: 3

  - dataset_id: java_rd_flink_code_22
    required_metadata_keys:
      - demo_dataset_id
      - framework
      - framework_version
      - source_kind
      - language
      - repo
      - repo_ref
      - path
      - module
      - java_package
      - class_name
      - api_surface
    probe_filter_query: "REST handler implementation pattern for job checkpoint endpoint"
    probe_filters:
      condition: and
      filters:
        - key: framework
          op: "=="
          value: flink
        - key: source_kind
          op: "=="
          value: code
        - key: module
          op: "=="
          value: flink-runtime
        - key: api_surface
          op: "=="
          value: rest
    probe_min_results: 5
```

## Chunking Strategy

Chunking should differ by artifact type. A single default chunker across docs,
source, and tests will dilute the demo.

### Docs HTML Pages

Preferred:

```python
DOCS_CHUNKING = {
    "strategy": "docling",
    "docling_chunker_type": "hybrid",
    "docling_max_tokens": 420,
    "docling_merge_peers": True,
    "docling_merge_list_items": True,
    "docling_processing_mode": "batch",
    "dedup_mode": "minhash",
}
```

Fallback if Docling is unavailable for HTML in the target environment:

```python
DOCS_CHUNKING_FALLBACK = {
    "strategy": "unstructured",
    "chunking_strategy": "by_title",
    "chunk_size": 1800,
    "overlap": 150,
    "combine_text_under_n_chars": 500,
    "multipage_sections": True,
    "dedup_mode": "minhash",
}
```

Rationale:

- Documentation pages have headings, lists, and tables. Heading-aware chunking
  preserves the structure that developers search for.
- Around 420 tokens keeps chunks under the current embedding safety window while
  retaining enough surrounding context for code agents.
- Dedup is acceptable for docs because repeated nav/footer text should not
  dominate search.
- Do not set `dedup_partition_keys` unless the importer explicitly places those
  partition values into chunk system metadata. The normal demo metadata fields
  are custom metadata, and they are better used for search filters and metadata
  sparse ranking.

### Confluence-Like Guides

For generated markdown guides:

```python
GUIDE_CHUNKING = {
    "strategy": "semantic",
    "chunk_size": 1200,
    "overlap": 120,
    "dedup_mode": "minhash",
}
```

Rationale:

- Guides are naturally heading-oriented.
- Semantic/paragraph splitting preserves "How to add X" steps better than fixed
  token windows.
- These guides intentionally mimic customer Confluence pages and should retrieve
  before raw source when the task asks "how do we do this here?"

### Java/Scala Source Code

Do not rely on generic document chunking as the main code parser. Preprocess
source files into logical documents first, then let K2 apply only light chunking.

Preprocessor output:

- One document for each normal-sized class/test class.
- For very large files, one document per class plus method-group documents.
- Each raw text document starts with a compact metadata header:

```text
Repository: apache/flink
Ref: release-2.2.0
Path: flink-runtime/src/main/java/...
Module: flink-runtime
Package: org.apache.flink.runtime...
Class: ...
Extends: ...
Implements: ...

<source excerpt>
```

Recommended K2 chunking:

```python
CODE_CHUNKING = {
    "strategy": "fixed",
    "chunk_size": 350,
    "overlap": 60,
    "dedup_mode": "off",
}
```

Rationale:

- Code needs symbol-aware preprocessing because Java classes, imports,
  annotations, and tests carry meaning that generic prose chunkers do not know.
- Keep code chunks smaller than prose chunks so embeddings see complete methods
  or compact method groups.
- Do not deduplicate code. Repeated Java boilerplate is often the pattern the
  agent needs to copy.

### Tests

Tests should be separate from production code through `source_kind=test` and
`is_test=true`.

```python
TEST_CHUNKING = {
    "strategy": "fixed",
    "chunk_size": 450,
    "overlap": 80,
    "dedup_mode": "off",
}
```

Rationale:

- Tests need enough room for setup, action, assertions, and helper methods.
- Test retrieval should be explicit. Agents should not copy test-only patterns
  into production code unless the query asks for tests.

### Build And Configuration Files

```python
CONFIG_CHUNKING = {
    "strategy": "fixed",
    "chunk_size": 250,
    "overlap": 40,
    "dedup_mode": "off",
}
```

Rationale:

- Build/config files are exact identifier-heavy.
- BM25 and metadata sparse will carry much of the search quality.

## MCP And Skill Design

The existing `mcp-server-k2` is a good starting point. For this demo, extend it
with task-specific wrappers so the model does not have to hand-build filters on
every call.

Recommended MCP tools:

| Tool | Inputs | Behavior |
| --- | --- | --- |
| `k2_search_docs` | `query`, `framework`, `version`, `api_surface`, `top_k` | Applies docs/guides filters and returns cited docs. |
| `k2_search_code` | `query`, `framework`, `version`, `module`, `api_surface`, `top_k` | Applies code filters and returns source snippets. |
| `k2_search_tests` | `query`, `framework`, `version`, `module`, `api_surface`, `top_k` | Applies test filters. |
| `k2_search_all` | `query`, `framework`, `version`, optional `filters` | General fallback with explicit filters. |
| `k2_answer_with_sources` | `query`, `framework`, `version`, `filters` | Calls `search_generate` and returns answer + source list. |
| `k2_demo_probe` | `dataset_id` | Runs the fixed metadata readiness probe. |

Tool defaults:

- `top_k=12` for docs/code/test search.
- `top_k=20` for broad `search_all`.
- `rerank.enabled=true` with `rerank.top_k=50` if reranker is enabled in the
  environment.
- Always include text, scores, and provenance.
- Always show metadata fields in compact form: framework, version, source kind,
  module, path, class name, topic, and source URI.

Recommended Codex/Claude skill behavior:

1. Search guides/docs first for conventions.
2. Search code for implementation patterns.
3. Search tests for validation patterns.
4. Cite sources in every plan.
5. If K2 results conflict with local repo state, trust local repo for exact file
   contents and use K2 as navigation context.
6. Never make an implementation claim from an unfiltered broad search when a
   docs/code/tests filter is available.

## Baseline Vs K2 Evaluation

Use a small rubric that engineering stakeholders understand.

| Metric | Measurement |
| --- | --- |
| Required artifact recall | Did the answer identify the expected docs, modules, source classes, and tests? |
| Time to correct plan | Number of tool calls or minutes before a plausible plan. |
| Citation coverage | Percentage of major claims with source URI/path. |
| Exact identifier accuracy | Correct class names, config keys, method names, modules. |
| Test plan quality | Does it identify real neighboring tests and test helpers? |
| Hallucination count | Non-existent files, wrong framework conventions, stale version claims. |

Evaluation harness:

1. Define 10-15 task cases in YAML.
2. For each task, list expected source patterns:
   - required docs URLs or docs topics,
   - required modules,
   - required class/package patterns,
   - required test path patterns.
3. Run K2 retrieval with fixed filters and record Recall@10 / MRR@10 / NDCG@10.
4. Run baseline prompts and score the final answer against the same artifact
   checklist.
5. Save a side-by-side markdown or notebook report.

Suggested eval case shape:

```yaml
- id: flink_rest_checkpoint_endpoint
  prompt: >
    Add a REST endpoint that exposes a checkpoint summary for a running Flink job.
    Identify implementation and test patterns before editing.
  framework: flink
  version: "2.2.0"
  expected:
    modules:
      - flink-runtime
    api_surfaces:
      - rest
      - checkpointing
    source_kind_hits:
      docs: 2
      code: 3
      test: 2
    must_mention:
      - REST handler
      - message parameters
      - response body
      - handler test
```

## Demo Runbook

1. Export credentials outside scripts:

```bash
export K2_API_KEY="..."
export K2_API_HOST="https://api.knowledge2.ai"
```

2. Create corpora:

```text
java-rd-demo / flink-docs-2.2
java-rd-demo / flink-code-2.2
java-rd-demo / java-rd-guides
optional: java-rd-demo / kafka-docs-4.2
optional: java-rd-demo / kafka-code-4.2
```

3. Ingest docs:

```python
client.ingest_urls(
    corpus_id=flink_docs_corpus,
    urls=flink_url_items,
    chunking=DOCS_CHUNKING,
    auto_index=False,
    wait=True,
)
```

4. Ingest code:

```python
client.upload_documents_batch_and_wait(
    corpus_id=flink_code_corpus,
    docs=code_documents,
    chunking=CODE_CHUNKING,
    auto_index=False,
)
```

5. Build indexes:

```python
client.sync_indexes(flink_docs_corpus, wait=True)
client.sync_indexes(flink_code_corpus, wait=True)
client.sync_indexes(guides_corpus, wait=True)
```

6. Run readiness probes:

```python
client.search(
    corpus_id=flink_docs_corpus,
    query="how do I add a REST API endpoint for checkpoint information",
    filters=FILTER_FLINK_CHECKPOINT_DOCS_OR_GUIDES,
    hybrid=DEMO_HYBRID,
    top_k=12,
    return_config=DEMO_RETURN,
)
```

7. Configure MCP:

```text
K2_API_KEY from env
K2_PROJECT_ID for java-rd-demo
K2_CORPUS_ID default to flink-docs-2.2 or a router config file
K2_API_HOST=https://api.knowledge2.ai
```

8. Run the baseline task without K2 tools.
9. Run the same task with K2 MCP tools and the skill instructions.
10. Show scorecard and retrieved sources side by side.

## Customer-Facing Talk Track

Use this framing:

- "Your Confluence is not just text; it is a routing layer. K2 metadata lets the
  agent ask for only the current version, only the right module, only tests, or
  only coding standards."
- "Legacy Java has many exact identifiers. Dense embeddings alone are weak on
  config keys, class names, REST routes, and exception names. K2 hybrid search
  combines semantic, lexical, and metadata signals."
- "Agents are more reliable when they retrieve the convention first, the code
  pattern second, and the tests third."
- "The demo uses Flink/Kafka because they have the same shape as your problem:
  large Java codebases, release-specific docs, module conventions, and tests."

## Risks And Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Public docs drift before demo | Demo answers change | Pin versions and materialize deterministic manifests. |
| Too much corpus noise | Agent retrieves broad docs instead of implementation examples | Use separate corpora, hard filters, and topic/module metadata. |
| Metadata values exceed limits | Ingestion errors or sparse metadata truncation | Keep metadata short; cap `symbols` and `nav_path`. |
| Code chunking loses method context | Weak implementation retrieval | Preprocess by Java class/method group before K2 ingest. |
| Baseline is too weak | Demo feels unfair | Include Mode B with local repo grep to make comparison credible. |
| MCP tool is too generic | Agent underuses metadata | Add docs/code/test wrapper tools with built-in filters. |
| Credential leakage | Security incident | Never store keys in files; rotate any credential that appears in logs, terminals, or other non-secret storage. |

## Implementation Work Items

1. Build `scripts/build_java_rd_demo_assets.py`.
   - URL discovery from Flink/Kafka docs.
   - Repo clone/ref validation.
   - Code file allowlist and metadata extraction.
   - Generated Confluence-like guide creation.
   - Manifest output for deterministic reruns.
2. Extend `mcp-server-k2`.
   - Add filter-aware search inputs.
   - Add docs/code/tests wrapper tools.
   - Add compact provenance output.
3. Add a Codex/Claude skill.
   - Search order: guides/docs, then code, then tests.
   - Require citations before implementation.
   - Provide filter recipes for Flink and Kafka tasks.
4. Add `eval_java_rd_demo.py`.
   - Load YAML eval cases.
   - Run K2 retrieval and optional `search_generate`.
   - Run no-K2 baseline prompt outputs.
   - Produce markdown scorecard.
5. Rehearse the three demo tasks.
   - Keep one "wow" path short enough for live presentation.
   - Keep a pre-recorded fallback output for network/API issues.

## Open Decisions

- Whether to implement code parsing with a lightweight regex/parser first or use
  tree-sitter Java for more reliable class/method extraction.
- Whether Kafka is included in the first live customer demo or kept as a backup
  multi-corpus story.
- Whether to use `search_generate` live or have the agent retrieve sources and
  generate the implementation plan itself. For coding-agent demos, the second is
  usually more credible because it shows the agent's tool use.
- Whether to promote the demo asset as a shared K2 template corpus after the
  customer demo. If yes, use deterministic manifests and readiness probes from
  the start.
