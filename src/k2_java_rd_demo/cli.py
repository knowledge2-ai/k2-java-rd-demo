"""Command-line interface for the K2 Java R&D demo."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .agent_specs import build_agent_specs
from .assets import (
    build_documents_from_repo,
    generate_seed_guides,
    summarize_jsonl,
    write_jsonl,
)
from .chunking import chunking_catalog
from .customer_value import customer_value_scorecard, render_customer_value_report
from .docs_harvest import TavilyExtractOptions, build_docs_documents, discover_docs_urls
from .eval_cases import evaluation_case_dicts, evaluation_cases
from .evaluation import EvalCase, EvalRun, ExpectedArtifact, compare_runs
from .filters import DEMO_HYBRID, DEMO_RETURN, demo_filter_catalog
from .live_agents import validate_corpus_ids
from .live_agents import deploy_agents_and_feeds
from .live_client import create_knowledge2_client, live_client_config_from_env
from .live_k2 import (
    LiveK2Config,
    default_readiness_probes,
    load_jsonl_documents_by_role,
    orchestrate_live_k2,
)
from .live_eval import LiveEvalConfig, build_live_eval_search_requests, run_live_eval
from .mcp_contract import build_mcp_tool_contract
from .repo_checkout import build_checkout_plans, checkout_plans_to_dict
from .source_catalog import build_ingestion_manifest, docs_source_manifests


def _print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def cmd_show_config(_: argparse.Namespace) -> int:
    _print_json(
        {
            "hybrid": DEMO_HYBRID,
            "return": DEMO_RETURN,
            "filters": demo_filter_catalog(),
            "chunking": chunking_catalog(),
        }
    )
    return 0


def cmd_build_code_assets(args: argparse.Namespace) -> int:
    documents = build_documents_from_repo(
        args.repo_root,
        framework=args.framework,
        framework_version=args.version,
        repo=args.repo,
        repo_ref=args.repo_ref,
        max_files=args.max_files,
    )
    count = write_jsonl(documents, args.out)
    _print_json({"written": count, "out": str(args.out)})
    return 0


def cmd_discover_docs_urls(args: argparse.Namespace) -> int:
    results = []
    for source in docs_source_manifests(args.framework, include_kafka=args.include_kafka):
        urls = discover_docs_urls(source, max_pages=args.max_pages)
        results.append(
            {
                "framework": source.framework,
                "version": source.version,
                "corpus_name": source.corpus_name,
                "seed_urls": list(source.seed_urls),
                "url_count": len(urls),
                "urls": urls,
            }
        )
    _print_json({"sources": results})
    return 0


def cmd_build_docs_assets(args: argparse.Namespace) -> int:
    documents = []
    sources = docs_source_manifests(args.framework, include_kafka=args.include_kafka)
    counts_by_corpus: dict[str, int] = {}
    for source in sources:
        source_documents = build_docs_documents(
            source,
            max_pages=args.max_pages,
            extractor=args.extractor,
            tavily_options=TavilyExtractOptions(
                extract_depth=args.tavily_extract_depth,
                format=args.tavily_format,
                timeout=args.tavily_timeout,
                query=args.tavily_query,
                chunks_per_source=args.tavily_chunks_per_source,
                batch_size=args.tavily_batch_size,
            ),
            allow_empty=args.allow_empty,
        )
        documents.extend(source_documents)
        counts_by_corpus[source.corpus_name] = len(source_documents)
    count = write_jsonl(documents, args.out)
    _print_json(
        {
            "written": count,
            "out": str(args.out),
            "corpora": counts_by_corpus,
        }
    )
    return 0


def cmd_build_guides(args: argparse.Namespace) -> int:
    documents = generate_seed_guides(args.framework, args.version)
    count = write_jsonl(documents, args.out)
    _print_json({"written": count, "out": str(args.out)})
    return 0


def cmd_probe_jsonl(args: argparse.Namespace) -> int:
    summary = summarize_jsonl(args.input)
    _print_json(summary)
    return 0


def cmd_show_agent_specs(args: argparse.Namespace) -> int:
    _print_json(_build_agent_specs_from_args(args))
    return 0


def cmd_show_source_manifest(args: argparse.Namespace) -> int:
    manifest = build_ingestion_manifest(
        args.framework,
        include_kafka=args.include_kafka,
        project_name=args.project_name,
    )
    _print_json(manifest.to_dict())
    return 0


def cmd_show_eval_cases(args: argparse.Namespace) -> int:
    _print_json(evaluation_case_dicts(suite=args.suite, include_kafka=args.include_kafka))
    return 0


def cmd_show_mcp_contract(args: argparse.Namespace) -> int:
    _print_json(build_mcp_tool_contract(include_kafka=args.include_kafka))
    return 0


def cmd_plan_repo_checkout(args: argparse.Namespace) -> int:
    plans = build_checkout_plans(
        include_kafka=args.include_kafka,
        base_dir=args.base_dir,
        sparse=not args.full_clone,
    )
    _print_json(
        {
            "base_dir": str(args.base_dir),
            "sparse": not args.full_clone,
            "plans": checkout_plans_to_dict(plans),
        }
    )
    return 0


def cmd_validate_agent_specs(args: argparse.Namespace) -> int:
    specs = _build_agent_specs_from_args(args)
    validate_corpus_ids(specs)
    _print_json(
        {
            "valid": True,
            "agent_count": len(specs["agents"]),
            "feed_count": len(specs["feeds"]),
            "corpora": specs["corpora"],
        }
    )
    return 0


def cmd_show_readiness_probes(_: argparse.Namespace) -> int:
    _print_json([asdict(probe) for probe in default_readiness_probes()])
    return 0


def cmd_plan_live_run(args: argparse.Namespace) -> int:
    config = LiveK2Config(
        project_name=args.project_name,
        project_id=args.project_id,
        corpus_ids=_corpus_ids_from_args(args),
    )
    grouped = load_jsonl_documents_by_role(args.jsonl)
    _print_json(
        {
            "project_name": config.project_name,
            "project_id": config.project_id,
            "corpus_ids": dict(config.corpus_ids),
            "document_counts_by_role": {
                role: len(documents) for role, documents in sorted(grouped.items())
            },
            "readiness_probes": [asdict(probe) for probe in default_readiness_probes()],
            "next_live_function": "orchestrate_live_k2(client, jsonl_paths=..., config=...)",
        }
    )
    return 0


def cmd_run_live_k2(args: argparse.Namespace) -> int:
    _require_execute(args.execute, "run-live-k2")
    config = LiveK2Config.from_env(require_api_key=True)
    config = LiveK2Config(
        project_name=args.project_name or config.project_name,
        project_id=args.project_id or config.project_id,
        corpus_ids={**dict(config.corpus_ids), **_corpus_ids_from_args(args)},
        corpus_definitions=config.corpus_definitions,
        org_id=config.org_id,
        org_name=config.org_name,
        api_host=config.api_host,
    )
    client = create_knowledge2_client()
    result = orchestrate_live_k2(
        client,
        jsonl_paths=args.jsonl,
        config=config,
        create_missing=args.create_missing,
        run_sync=not args.skip_sync,
        run_probes=not args.skip_probes,
        auto_index=args.auto_index,
        idempotency_prefix=args.idempotency_prefix,
    )
    _print_json(
        {
            "client": live_client_config_from_env().to_dict(),
            "result": result.to_dict(),
        }
    )
    return 0


def cmd_deploy_live_agents(args: argparse.Namespace) -> int:
    _require_execute(args.execute, "deploy-live-agents")
    client = create_knowledge2_client()
    summary = deploy_agents_and_feeds(
        client,
        project_id=args.project_id,
        corpus_ids={
            "flink_docs": args.flink_docs_corpus_id,
            "flink_code": args.flink_code_corpus_id,
            "java_rd_guides": args.guides_corpus_id,
            **({"kafka_docs": args.kafka_docs_corpus_id} if args.kafka_docs_corpus_id else {}),
            **({"kafka_code": args.kafka_code_corpus_id} if args.kafka_code_corpus_id else {}),
        },
        activate=not args.skip_activate,
        run_feed_dry_run=args.run_feed_dry_run,
    )
    _print_json(
        {
            "client": live_client_config_from_env().to_dict(),
            "result": summary,
        }
    )
    return 0


def cmd_plan_live_eval(args: argparse.Namespace) -> int:
    config = _live_eval_config_from_args(args, execute=False)
    requests = build_live_eval_search_requests(config)
    _print_json(
        {
            "config": config.to_dict(),
            "request_count": len(requests),
            "requests": [request.to_dict() for request in requests],
            "next_live_function": "run_live_eval(client, config, baseline=...)",
        }
    )
    return 0


def cmd_run_live_eval(args: argparse.Namespace) -> int:
    _require_execute(args.execute, "run-live-eval")
    client = create_knowledge2_client()
    config = _live_eval_config_from_args(args, execute=True)
    scorecard = run_live_eval(client, config)
    _print_json(
        {
            "client": live_client_config_from_env().to_dict(),
            "scorecard": scorecard,
        }
    )
    return 0


def cmd_score_sample(_: argparse.Namespace) -> int:
    _print_json(_sample_scorecard())
    return 0


def cmd_score_demo_cases(args: argparse.Namespace) -> int:
    _print_json(_catalog_scorecard(suite=args.suite, include_kafka=args.include_kafka))
    return 0


def cmd_score_customer_value(args: argparse.Namespace) -> int:
    scorecard = customer_value_scorecard(include_kafka=args.include_kafka)
    if args.format == "markdown":
        print(render_customer_value_report(scorecard))
    else:
        _print_json(scorecard)
    return 0


def _corpus_ids_from_args(args: argparse.Namespace) -> dict[str, str]:
    return {
        key: value
        for key, value in {
            "docs": getattr(args, "docs_corpus_id", None),
            "code": getattr(args, "code_corpus_id", None),
            "guides": getattr(args, "guides_corpus_id", None),
        }.items()
        if value
    }


def _eval_corpus_ids_from_args(args: argparse.Namespace) -> dict[str, str]:
    return {
        key: value
        for key, value in {
            "docs": getattr(args, "docs_corpus_id", None),
            "code": getattr(args, "code_corpus_id", None),
            "guides": getattr(args, "guides_corpus_id", None),
            "flink_docs": getattr(args, "flink_docs_corpus_id", None),
            "flink_code": getattr(args, "flink_code_corpus_id", None),
            "kafka_docs": getattr(args, "kafka_docs_corpus_id", None),
            "kafka_code": getattr(args, "kafka_code_corpus_id", None),
        }.items()
        if value
    }


def _live_eval_config_from_args(args: argparse.Namespace, *, execute: bool) -> LiveEvalConfig:
    return LiveEvalConfig(
        project_id=args.project_id,
        corpus_ids=_eval_corpus_ids_from_args(args),
        include_kafka=args.include_kafka,
        top_k=args.top_k,
        execute=execute,
        include_guides=not args.skip_guides,
    )


def _build_agent_specs_from_args(args: argparse.Namespace) -> dict[str, Any]:
    corpus_ids = {
        key: value
        for key, value in {
            "flink_docs": args.flink_docs_corpus_id,
            "flink_code": args.flink_code_corpus_id,
            "java_rd_guides": args.guides_corpus_id,
            "kafka_docs": args.kafka_docs_corpus_id,
            "kafka_code": args.kafka_code_corpus_id,
        }.items()
        if value
    }
    return build_agent_specs(project_id=args.project_id, corpus_ids=corpus_ids)


def _require_execute(execute: bool, command: str) -> None:
    if not execute:
        raise RuntimeError(
            f"{command} would call the live K2 API. Re-run with --execute after "
            "verifying K2_API_KEY and corpus/project arguments."
        )


def _sample_scorecard() -> dict[str, Any]:
    doc_uri = "repo://apache/flink@release-2.2.0/docs/rest.md"
    code_uri = (
        "repo://apache/flink@release-2.2.0/"
        "flink-runtime/src/main/java/JobCheckpointHandler.java"
    )
    test_uri = (
        "repo://apache/flink@release-2.2.0/"
        "flink-runtime/src/test/java/JobCheckpointHandlerTest.java"
    )
    case = EvalCase(
        case_id="flink-rest-handler",
        title="Flink REST handler implementation",
        query="How should I add a Flink REST handler?",
        expected_artifacts=[
            ExpectedArtifact(
                key="rest handler source",
                source_uri=code_uri,
                source_kind="code",
                module="flink-runtime",
                api_surface="rest",
                class_name="JobCheckpointHandler",
            ),
            ExpectedArtifact(
                key="neighboring handler test",
                source_kind="test",
                module="flink-runtime",
                api_surface="rest",
                path_contains="JobCheckpointHandlerTest.java",
            ),
        ],
        expected_source_kinds=["docs", "code", "test"],
        required_modules=["flink-runtime"],
        required_api_surfaces=["rest"],
        must_mentions=["route registration", "AbstractRestHandler"],
        required_source_uris=[doc_uri],
        hallucination_markers=["MagicPlanner"],
    )
    docs_row = {
        "source_uri": doc_uri,
        "raw_text": "REST docs mention route registration and response body classes.",
        "metadata": {"source_kind": "docs", "module": "docs", "api_surface": "rest"},
    }
    code_row = {
        "source_uri": code_uri,
        "raw_text": "class JobCheckpointHandler extends AbstractRestHandler {}",
        "metadata": {
            "source_kind": "code",
            "module": "flink-runtime",
            "api_surface": "rest",
            "class_name": "JobCheckpointHandler",
        },
    }
    test_row = {
        "source_uri": test_uri,
        "raw_text": "JobCheckpointHandlerTest verifies handler wiring.",
        "metadata": {
            "source_kind": "test",
            "module": "flink-runtime",
            "api_surface": "rest",
            "path": "flink-runtime/src/test/java/JobCheckpointHandlerTest.java",
        },
    }
    return compare_runs(
        [case],
        [
            EvalRun(
                name="baseline",
                results_by_case={case.case_id: [docs_row]},
                answers_by_case={case.case_id: "Use the REST docs only: " + doc_uri},
            ),
            EvalRun(
                name="k2",
                results_by_case={case.case_id: [docs_row, code_row, test_row]},
                answers_by_case={
                    case.case_id: (
                        "Use route registration and AbstractRestHandler. Cite "
                        f"{doc_uri} and {code_uri}."
                    )
                },
            ),
        ],
    )


def _catalog_scorecard(*, suite: str = "demo", include_kafka: bool) -> dict[str, Any]:
    cases = evaluation_cases(suite=suite, include_kafka=include_kafka)
    baseline_rows = {
        case.case_id: _synthetic_rows_for_case(case, max_artifacts=1) for case in cases
    }
    k2_rows = {case.case_id: _synthetic_rows_for_case(case) for case in cases}
    k2_answers = {case.case_id: _synthetic_answer_for_case(case) for case in cases}
    return compare_runs(
        cases,
        [
            EvalRun(name="baseline", results_by_case=baseline_rows),
            EvalRun(name="k2", results_by_case=k2_rows, answers_by_case=k2_answers),
        ],
    )


def _synthetic_rows_for_case(
    case: EvalCase,
    *,
    max_artifacts: int | None = None,
) -> list[dict[str, Any]]:
    artifacts = list(case.expected_artifacts)
    if max_artifacts is not None:
        artifacts = artifacts[:max_artifacts]

    rows: list[dict[str, Any]] = []
    for artifact in artifacts:
        metadata = {
            "source_kind": artifact.source_kind,
            "module": artifact.module,
            "api_surface": artifact.api_surface,
            "path": artifact.path_contains
            or (artifact.source_uri or artifact.key).rsplit("/", maxsplit=1)[-1],
        }
        if artifact.class_name:
            metadata["class_name"] = artifact.class_name
        metadata.update(artifact.metadata_equals)

        rows.append(
            {
                "source_uri": artifact.source_uri,
                "raw_text": " ".join(
                    [
                        artifact.key,
                        *artifact.text_contains,
                        *case.must_mentions,
                        *(str(value) for value in artifact.metadata_equals.values()),
                    ]
                ),
                "metadata": metadata,
                "score": 1.0,
            }
        )
    return rows


def _synthetic_answer_for_case(case: EvalCase) -> str:
    citations = [
        artifact.source_uri for artifact in case.expected_artifacts if artifact.source_uri
    ]
    return " ".join([*case.must_mentions, *citations])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="k2-java-rd-demo")
    subparsers = parser.add_subparsers(dest="command", required=True)

    show_config = subparsers.add_parser("show-config", help="Print K2 filter/chunking recipes")
    show_config.set_defaults(func=cmd_show_config)

    build_code = subparsers.add_parser("build-code-assets", help="Build K2-ready JSONL from repo")
    build_code.add_argument("--repo-root", type=Path, required=True)
    build_code.add_argument("--framework", required=True, choices=["flink", "kafka"])
    build_code.add_argument("--version", required=True)
    build_code.add_argument("--repo", required=True)
    build_code.add_argument("--repo-ref", required=True)
    build_code.add_argument("--out", type=Path, required=True)
    build_code.add_argument("--max-files", type=int, default=None)
    build_code.set_defaults(func=cmd_build_code_assets)

    discover_docs = subparsers.add_parser(
        "discover-docs-urls",
        help="Discover docs page URLs from source catalog sitemaps or seed links",
    )
    discover_docs.add_argument("--framework", action="append")
    discover_docs.add_argument("--include-kafka", action="store_true")
    discover_docs.add_argument("--max-pages", type=int)
    discover_docs.set_defaults(func=cmd_discover_docs_urls)

    build_docs = subparsers.add_parser(
        "build-docs-assets",
        help="Harvest public docs pages into K2-ready JSONL",
    )
    build_docs.add_argument("--framework", action="append")
    build_docs.add_argument("--include-kafka", action="store_true")
    build_docs.add_argument("--max-pages", type=int)
    build_docs.add_argument(
        "--extractor",
        choices=["direct", "tavily"],
        default="direct",
        help="Docs content extraction backend. Tavily uses TAVILY_API_KEY.",
    )
    build_docs.add_argument(
        "--tavily-extract-depth",
        choices=["basic", "advanced"],
        default="basic",
    )
    build_docs.add_argument("--tavily-format", choices=["markdown", "text"], default="markdown")
    build_docs.add_argument("--tavily-timeout", type=float)
    build_docs.add_argument("--tavily-query")
    build_docs.add_argument("--tavily-chunks-per-source", type=int, default=3)
    build_docs.add_argument("--tavily-batch-size", type=int, default=20)
    build_docs.add_argument("--out", type=Path, required=True)
    build_docs.add_argument(
        "--allow-empty",
        action="store_true",
        help="Allow zero harvested documents instead of raising an error.",
    )
    build_docs.set_defaults(func=cmd_build_docs_assets)

    build_guides = subparsers.add_parser("build-guides", help="Build generated guide JSONL")
    build_guides.add_argument("--framework", required=True, choices=["flink", "kafka"])
    build_guides.add_argument("--version", required=True)
    build_guides.add_argument("--out", type=Path, required=True)
    build_guides.set_defaults(func=cmd_build_guides)

    probe = subparsers.add_parser("probe-jsonl", help="Validate and summarize generated JSONL")
    probe.add_argument("--input", type=Path, required=True)
    probe.set_defaults(func=cmd_probe_jsonl)

    agent_specs = subparsers.add_parser("show-agent-specs", help="Print dry-run Agent/Feed specs")
    agent_specs.add_argument("--project-id", default="<java-rd-demo-project-id>")
    agent_specs.add_argument("--flink-docs-corpus-id")
    agent_specs.add_argument("--flink-code-corpus-id")
    agent_specs.add_argument("--guides-corpus-id")
    agent_specs.add_argument("--kafka-docs-corpus-id")
    agent_specs.add_argument("--kafka-code-corpus-id")
    agent_specs.set_defaults(func=cmd_show_agent_specs)

    source_manifest = subparsers.add_parser(
        "show-source-manifest",
        help="Print deterministic OSS docs/code source manifest",
    )
    source_manifest.add_argument(
        "--framework",
        action="append",
        help="Framework to include. Repeat or pass comma-separated values.",
    )
    source_manifest.add_argument("--include-kafka", action="store_true")
    source_manifest.add_argument("--project-name", default="java-rd-demo")
    source_manifest.set_defaults(func=cmd_show_source_manifest)

    eval_cases = subparsers.add_parser(
        "show-eval-cases",
        help="Print customer-story eval case catalog",
    )
    eval_cases.add_argument("--include-kafka", action="store_true")
    eval_cases.add_argument("--suite", choices=["demo", "benchmark"], default="demo")
    eval_cases.set_defaults(func=cmd_show_eval_cases)

    mcp_contract = subparsers.add_parser(
        "show-mcp-contract",
        help="Print filter-aware MCP tool contract for Claude/Codex integrations",
    )
    mcp_contract.add_argument("--include-kafka", action="store_true")
    mcp_contract.set_defaults(func=cmd_show_mcp_contract)

    repo_checkout = subparsers.add_parser(
        "plan-repo-checkout",
        help="Print git commands for deterministic OSS source checkouts",
    )
    repo_checkout.add_argument("--include-kafka", action="store_true")
    repo_checkout.add_argument(
        "--base-dir",
        type=Path,
        default=Path("/tmp/k2-java-rd-demo-sources"),
    )
    repo_checkout.add_argument("--full-clone", action="store_true")
    repo_checkout.set_defaults(func=cmd_plan_repo_checkout)

    validate_specs = subparsers.add_parser(
        "validate-agent-specs",
        help="Validate Agent/Feed specs have concrete corpus IDs",
    )
    validate_specs.add_argument("--project-id", required=True)
    validate_specs.add_argument("--flink-docs-corpus-id", required=True)
    validate_specs.add_argument("--flink-code-corpus-id", required=True)
    validate_specs.add_argument("--guides-corpus-id", required=True)
    validate_specs.add_argument("--kafka-docs-corpus-id")
    validate_specs.add_argument("--kafka-code-corpus-id")
    validate_specs.set_defaults(func=cmd_validate_agent_specs)

    readiness = subparsers.add_parser(
        "show-readiness-probes",
        help="Print default K2 readiness probes",
    )
    readiness.set_defaults(func=cmd_show_readiness_probes)

    live_plan = subparsers.add_parser(
        "plan-live-run",
        help="Plan a live K2 orchestration run without calling K2",
    )
    live_plan.add_argument("--jsonl", type=Path, required=True, action="append")
    live_plan.add_argument("--project-name", default="java-rd-demo")
    live_plan.add_argument("--project-id")
    live_plan.add_argument("--docs-corpus-id")
    live_plan.add_argument("--code-corpus-id")
    live_plan.add_argument("--guides-corpus-id")
    live_plan.set_defaults(func=cmd_plan_live_run)

    live_run = subparsers.add_parser(
        "run-live-k2",
        help="Execute live K2 project/corpus upload, index sync, and readiness probes",
    )
    live_run.add_argument("--execute", action="store_true")
    live_run.add_argument("--jsonl", type=Path, required=True, action="append")
    live_run.add_argument("--project-name", default=None)
    live_run.add_argument("--project-id")
    live_run.add_argument("--docs-corpus-id")
    live_run.add_argument("--code-corpus-id")
    live_run.add_argument("--guides-corpus-id")
    live_run.add_argument("--create-missing", action="store_true",
        help="Create missing K2 projects and corpora instead of failing.")
    live_run.add_argument("--skip-sync", action="store_true")
    live_run.add_argument("--skip-probes", action="store_true")
    live_run.add_argument("--auto-index", action="store_true")
    live_run.add_argument("--idempotency-prefix")
    live_run.set_defaults(func=cmd_run_live_k2)

    live_agents = subparsers.add_parser(
        "deploy-live-agents",
        help="Execute live K2 Agent and Knowledge Feed creation",
    )
    live_agents.add_argument("--execute", action="store_true")
    live_agents.add_argument("--project-id", required=True)
    live_agents.add_argument("--flink-docs-corpus-id", required=True)
    live_agents.add_argument("--flink-code-corpus-id", required=True)
    live_agents.add_argument("--guides-corpus-id", required=True)
    live_agents.add_argument("--kafka-docs-corpus-id")
    live_agents.add_argument("--kafka-code-corpus-id")
    live_agents.add_argument("--skip-activate", action="store_true")
    live_agents.add_argument("--run-feed-dry-run", action="store_true")
    live_agents.set_defaults(func=cmd_deploy_live_agents)

    live_eval_plan = subparsers.add_parser(
        "plan-live-eval",
        help="Plan live K2 eval searches without calling K2",
    )
    _add_live_eval_args(live_eval_plan, require_project=True)
    live_eval_plan.set_defaults(func=cmd_plan_live_eval)

    live_eval_run = subparsers.add_parser(
        "run-live-eval",
        help="Execute live K2 retrieval eval searches and score the demo cases",
    )
    live_eval_run.add_argument("--execute", action="store_true")
    _add_live_eval_args(live_eval_run, require_project=True)
    live_eval_run.set_defaults(func=cmd_run_live_eval)

    score_sample = subparsers.add_parser(
        "score-sample",
        help="Run a synthetic baseline-vs-K2 scorecard",
    )
    score_sample.set_defaults(func=cmd_score_sample)

    score_demo_cases = subparsers.add_parser(
        "score-demo-cases",
        help="Score the reusable demo eval case catalog with synthetic rows",
    )
    score_demo_cases.add_argument("--include-kafka", action="store_true")
    score_demo_cases.add_argument("--suite", choices=["demo", "benchmark"], default="demo")
    score_demo_cases.set_defaults(func=cmd_score_demo_cases)

    score_customer_value = subparsers.add_parser(
        "score-customer-value",
        help="Score the Java-shop guardrail value story with synthetic rows",
    )
    score_customer_value.add_argument("--include-kafka", action="store_true")
    score_customer_value.add_argument("--format", choices=["json", "markdown"], default="json")
    score_customer_value.set_defaults(func=cmd_score_customer_value)

    return parser


def _add_live_eval_args(parser: argparse.ArgumentParser, *, require_project: bool) -> None:
    parser.add_argument("--project-id", required=require_project)
    parser.add_argument("--docs-corpus-id")
    parser.add_argument("--code-corpus-id")
    parser.add_argument("--guides-corpus-id")
    parser.add_argument("--flink-docs-corpus-id")
    parser.add_argument("--flink-code-corpus-id")
    parser.add_argument("--kafka-docs-corpus-id")
    parser.add_argument("--kafka-code-corpus-id")
    parser.add_argument("--include-kafka", action="store_true")
    parser.add_argument("--skip-guides", action="store_true")
    parser.add_argument("--top-k", type=int, default=12)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
