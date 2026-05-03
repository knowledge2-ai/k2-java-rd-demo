#!/usr/bin/env python3
"""Run live Codex without-K2 vs with-K2-context comparison for the demo."""

from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from k2_java_rd_demo._subprocess_env import safe_subprocess_env  # noqa: E402
from k2_java_rd_demo.k2_config import load_k2_config  # noqa: E402

from k2_java_rd_demo.codex_comparison import (  # noqa: E402
    CodexCliConfig,
    baseline_prompt,
    build_answer_scorecard,
    k2_context_prompt,
    run_codex_answer,
)
from k2_java_rd_demo.eval_cases import evaluation_cases  # noqa: E402
from k2_java_rd_demo.evaluation import EvalCase  # noqa: E402
from k2_java_rd_demo.filters import DEMO_RETURN  # noqa: E402
from k2_java_rd_demo.live_eval import (  # noqa: E402
    LiveEvalConfig,
    build_live_eval_search_requests,
    normalize_live_eval_rows,
)
from k2_java_rd_demo.question_stats import write_question_stats  # noqa: E402


# Loaded at import time — an intentional snapshot of the environment.
# Tests that need different values should patch the module-level constants.
_k2_config = load_k2_config()
PROJECT_ID = _k2_config.project_id
CORPUS_IDS = dict(_k2_config.corpus_ids)

DOCS_HYBRID = {
    "enabled": True,
    "fusion_mode": "rrf",
    "rrf_k": 61,
    "dense_weight": 0.9,
    "sparse_weight": 0.1,
    "metadata_sparse_weight": 0.0,
    "metadata_sparse_enabled": True,
}

CODE_HYBRID = {
    "enabled": True,
    "fusion_mode": "rrf",
    "rrf_k": 60,
    "dense_weight": 0.0,
    "sparse_weight": 0.8,
    "metadata_sparse_weight": 0.2,
    "metadata_sparse_enabled": True,
}


class KubectlInternalK2Client:
    """Small live client that executes retrieval inside the API pod."""

    def __init__(self, *, namespace: str = "k2-mvp", deployment: str = "deploy/k2-mvp-api-internal"):
        self.namespace = namespace
        self.deployment = deployment

    def search(self, corpus_id: str, query: str, **kwargs: Any) -> dict[str, Any]:
        payload = {
            "corpus_id": corpus_id,
            "query": query,
            "top_k": int(kwargs.get("top_k") or 10),
            "filters": kwargs.get("filters"),
            "hybrid": _select_hybrid(corpus_id, kwargs.get("filters")),
        }
        encoded = base64.b64encode(json.dumps(payload).encode()).decode()
        cmd = [
            "kubectl",
            "-n",
            self.namespace,
            "exec",
            "-i",
            self.deployment,
            "--",
            "env",
            f"PAYLOAD_B64={encoded}",
            "python",
            "-c",
            _POD_RETRIEVAL_SCRIPT,
        ]
        completed = subprocess.run(
            cmd,
            text=True,
            capture_output=True,
            check=True,
            timeout=120,
            env=safe_subprocess_env(),
        )
        return json.loads(completed.stdout)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    selected_cases = evaluation_cases(suite=args.suite, include_kafka=True)
    if args.case_id:
        wanted = set(args.case_id)
        selected_cases = tuple(case for case in selected_cases if case.case_id in wanted)
    if args.max_cases:
        selected_cases = selected_cases[: args.max_cases]
    if not selected_cases:
        raise SystemExit("no eval cases selected")

    if not args.execute:
        print(
            json.dumps(
                {
                    "mode": "dry-run",
                    "case_count": len(selected_cases),
                    "cases": [case.case_id for case in selected_cases],
                    "model": args.model,
                    "project_id": args.project_id,
                    "top_k": args.top_k,
                    "note": "pass --execute to run live Codex/kubectl comparison",
                },
                indent=2,
            )
        )
        return 0

    run_id = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    out_dir = args.out_dir / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    config = LiveEvalConfig(
        project_id=args.project_id,
        corpus_ids=CORPUS_IDS,
        include_kafka=True,
        top_k=args.top_k,
        execute=True,
        hybrid=DOCS_HYBRID,
        return_config=DEMO_RETURN,
    )
    client = KubectlInternalK2Client(namespace=args.namespace, deployment=args.deployment)
    rows_by_case = _collect_rows(client, config, selected_cases)

    codex_config = CodexCliConfig(model=args.model, timeout_s=args.codex_timeout_s)
    baseline_answers: dict[str, str] = {}
    k2_answers: dict[str, str] = {}
    prompts_dir = out_dir / "prompts"
    answers_dir = out_dir / "answers"

    for case in selected_cases:
        baseline_answers[case.case_id] = run_codex_answer(
            baseline_prompt(case),
            answers_dir / f"{case.case_id}.without-k2.md",
            codex_config,
        )
        k2_answers[case.case_id] = run_codex_answer(
            k2_context_prompt(case, rows_by_case.get(case.case_id, ())),
            answers_dir / f"{case.case_id}.with-k2.md",
            codex_config,
        )
        (prompts_dir / f"{case.case_id}.without-k2.txt").parent.mkdir(
            parents=True, exist_ok=True
        )
        (prompts_dir / f"{case.case_id}.without-k2.txt").write_text(
            baseline_prompt(case),
            encoding="utf-8",
        )
        (prompts_dir / f"{case.case_id}.with-k2.txt").write_text(
            k2_context_prompt(case, rows_by_case.get(case.case_id, ())),
            encoding="utf-8",
        )

    scorecard = build_answer_scorecard(
        selected_cases,
        baseline_answers=baseline_answers,
        k2_rows_by_case=rows_by_case,
        k2_answers=k2_answers,
    )
    payload = {
        "run_id": run_id,
        "generated_at": datetime.now(UTC).isoformat(),
        "method": "codex_exec_no_context_vs_codex_exec_with_k2_mcp_context_payload",
        "project_id": args.project_id,
        "corpus_ids": CORPUS_IDS,
        "retrieval_profiles": {"docs": DOCS_HYBRID, "code_tests_guides": CODE_HYBRID},
        "cases": [case.to_dict() for case in selected_cases],
        "rows_by_case": rows_by_case,
        "answers": {
            "codex_without_k2": baseline_answers,
            "codex_with_k2_mcp_context": k2_answers,
        },
        "scorecard": scorecard,
    }
    result_path = out_dir / "scorecard.json"
    result_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    report_path = out_dir / "report.md"
    report_path.write_text(_render_report(payload), encoding="utf-8")
    stats_paths = write_question_stats(payload, out_dir=out_dir)

    print(
        json.dumps(
            {
                "result_path": str(result_path),
                "report_path": str(report_path),
                "stats_paths": {name: str(path) for name, path in stats_paths.items()},
                "scorecard": scorecard,
            },
            indent=2,
        )
    )
    return 0


def _collect_rows(
    client: KubectlInternalK2Client,
    config: LiveEvalConfig,
    cases: tuple[EvalCase, ...],
) -> dict[str, list[dict[str, Any]]]:
    rows_by_case: dict[str, list[dict[str, Any]]] = {case.case_id: [] for case in cases}
    seen_by_case: dict[str, set[tuple[str, str]]] = {case.case_id: set() for case in cases}

    for request in build_live_eval_search_requests(config, cases):
        response = client.search(
            request.corpus_id,
            request.query,
            top_k=request.top_k,
            filters=dict(request.filters),
        )
        rows = normalize_live_eval_rows(
            response.get("results", []),
            inferred_metadata={
                "corpus_role": request.role,
                "source_kind": request.source_kind,
            },
        )
        for row in rows:
            key = (str(row.get("source_uri") or ""), str((row.get("metadata") or {}).get("path") or ""))
            if key in seen_by_case[request.case_id]:
                continue
            seen_by_case[request.case_id].add(key)
            rows_by_case[request.case_id].append(row)
    return rows_by_case


def _select_hybrid(corpus_id: str, filters: Mapping[str, Any] | None) -> dict[str, Any]:
    source_kind = _filter_value(filters, "source_kind")
    if corpus_id in {CORPUS_IDS["flink_docs"], CORPUS_IDS["kafka_docs"]} and source_kind == "docs":
        return dict(DOCS_HYBRID)
    return dict(CODE_HYBRID)


def _filter_value(filter_obj: Mapping[str, Any] | None, key: str) -> str | None:
    if not filter_obj:
        return None
    if filter_obj.get("key") == key:
        value = filter_obj.get("value")
        return str(value) if isinstance(value, str) else None
    for child in filter_obj.get("filters") or ():
        if isinstance(child, Mapping):
            value = _filter_value(child, key)
            if value:
                return value
    return None


def _render_report(payload: Mapping[str, Any]) -> str:
    scorecard = payload["scorecard"]
    runs = {run["run_name"]: run for run in scorecard["runs"]}
    baseline = runs["codex_without_k2"]
    k2 = runs["codex_with_k2_mcp_context"]
    comparison = scorecard["comparisons"][0]
    lines = [
        "# Codex With K2 vs Without K2 E2E Comparison",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        "## Summary",
        "",
        f"- Cases: `{scorecard['case_count']}`",
        f"- Codex without K2: {_score_component_summary(baseline)}; passed cases: `{baseline['passed_cases']}`",
        f"- Codex with K2 MCP context: {_score_component_summary(k2)}; passed cases: `{k2['passed_cases']}`",
        f"- Score delta: `{comparison['score_delta_vs_baseline']}`",
        f"- Retrieval score delta: `{_component_delta(comparison, 'retrieval_score')}`",
        f"- Answer score delta: `{_component_delta(comparison, 'answer_score')}`",
        "",
        "## Method",
        "",
        "- The baseline run used `codex exec` with no K2 evidence, no web search, no project files, and ignored user MCP config.",
        "- The K2 run used the same Codex path, but the prompt included live K2 retrieval results as an MCP-style tool-output payload.",
        "- Scoring uses the repo's demo rubric: expected artifacts, source-kind coverage, module hits, API-surface hits, required mentions, citations, and hallucination markers.",
        "- This validates answer quality impact from K2 context. It does not yet start a standalone stdio MCP server; the included K2 payload is the exact evidence that server would return.",
        "",
        "## Retrieval Profiles",
        "",
        "```json",
        json.dumps(payload["retrieval_profiles"], indent=2, sort_keys=True),
        "```",
        "",
        "## Per-Case Results",
        "",
    ]
    by_case = {
        run["run_name"]: {case["case_id"]: case for case in run["cases"]}
        for run in scorecard["runs"]
    }
    for case in payload["cases"]:
        case_id = case["case_id"]
        b = by_case["codex_without_k2"][case_id]
        k = by_case["codex_with_k2_mcp_context"][case_id]
        lines.extend(
            [
                f"### {case['title']}",
                "",
                f"- Case ID: `{case_id}`",
                f"- Without K2: {_case_component_summary(b)}, passed `{b['passed']}`, results `{b['result_count']}`",
                f"- With K2: {_case_component_summary(k)}, passed `{k['passed']}`, results `{k['result_count']}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Demo Interpretation",
            "",
            "K2 changes the agent behavior from generic framework advice to sourced, version-pinned engineering guidance. The strongest signal is not just higher score; it is that the K2-assisted answer can cite the exact docs, implementation classes, and neighboring tests used to plan a Java change.",
            "",
        ]
    )
    return "\n".join(lines)


def _score_component_summary(run: Mapping[str, Any]) -> str:
    components = _run_score_components(run)
    return (
        f"combined `{_format_score(components.get('combined_score'))}`, "
        f"retrieval `{_format_score(components.get('retrieval_score'))}`, "
        f"answer `{_format_score(components.get('answer_score'))}`, "
        f"safety `{_format_score(components.get('safety_score'))}`"
    )


def _case_component_summary(case: Mapping[str, Any]) -> str:
    breakdown = case.get("score_breakdown")
    if not isinstance(breakdown, Mapping):
        breakdown = {}
    return (
        f"combined `{_format_score(case.get('score'))}`, "
        f"retrieval `{_format_score(breakdown.get('retrieval_score'))}`, "
        f"answer `{_format_score(breakdown.get('answer_score'))}`, "
        f"safety `{_format_score(breakdown.get('safety_score'))}`"
    )


def _run_score_components(run: Mapping[str, Any]) -> Mapping[str, Any]:
    components = run.get("score_components")
    if isinstance(components, Mapping):
        return components
    metric_averages = run.get("metric_averages")
    if not isinstance(metric_averages, Mapping):
        metric_averages = {}
    return {
        "combined_score": run.get("score"),
        "retrieval_score": metric_averages.get("retrieval_score_avg"),
        "answer_score": metric_averages.get("answer_score_avg"),
        "safety_score": metric_averages.get("hallucination_markers"),
    }


def _component_delta(comparison: Mapping[str, Any], component_name: str) -> str:
    deltas = comparison.get("score_component_deltas_vs_baseline")
    if isinstance(deltas, Mapping):
        return _format_score(deltas.get(component_name))
    metric_deltas = comparison.get("metric_deltas_vs_baseline")
    if isinstance(metric_deltas, Mapping):
        fallback_name = {
            "retrieval_score": "retrieval_score_avg",
            "answer_score": "answer_score_avg",
            "safety_score": "hallucination_markers",
        }.get(component_name, component_name)
        return _format_score(metric_deltas.get(fallback_name))
    return ""


def _format_score(value: Any) -> str:
    if isinstance(value, (int, float)):
        return f"{float(value):.6f}".rstrip("0").rstrip(".")
    return ""


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--namespace", default="k2-mvp")
    parser.add_argument("--deployment", default="deploy/k2-mvp-api-internal")
    parser.add_argument("--project-id", default=PROJECT_ID)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--model")
    parser.add_argument("--codex-timeout-s", type=int, default=900)
    parser.add_argument("--max-cases", type=int)
    parser.add_argument("--case-id", action="append")
    parser.add_argument("--suite", choices=["demo", "benchmark"], default="demo")
    parser.add_argument("--out-dir", type=Path, default=ROOT / ".eval-runs")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Required to run live Codex/kubectl comparison. Without this flag the script prints "
        "the planned configuration and exits.",
    )
    return parser


_POD_RETRIEVAL_SCRIPT = r"""
import base64
import json
import os
import urllib.request

from k2_core.db.session import SessionLocal
from k2_core.db.models import Chunk, Corpus, Document, Project

payload = json.loads(base64.b64decode(os.environ["PAYLOAD_B64"]).decode())

with SessionLocal() as db:
    corpus = db.query(Corpus).filter(Corpus.id == payload["corpus_id"]).first()
    if corpus is None:
        raise RuntimeError("corpus not found")
    project = db.query(Project).filter(Project.id == corpus.project_id).first()
    if project is None:
        raise RuntimeError("project not found")
    org_id = project.org_id

request_payload = {
    "corpus_id": payload["corpus_id"],
    "queries": [payload["query"]],
    "top_k": payload["top_k"],
    "filters": payload.get("filters"),
    "hybrid": payload.get("hybrid"),
}
request = urllib.request.Request(
    os.environ.get("RETRIEVAL_SERVICE_URL", "http://k2-mvp-retriever:8003").rstrip()
    + "/internal/retrieval:batch",
    data=json.dumps(request_payload).encode(),
    headers={
        "Content-Type": "application/json",
        "X-Worker-Token": os.environ["INTERNAL_WORKER_TOKEN"],
        "X-Org-Id": org_id,
    },
    method="POST",
)
with urllib.request.urlopen(request, timeout=60) as response:
    body = json.loads(response.read().decode())

raw_results = body.get("results", [[]])[0]
chunk_ids = [chunk_id for chunk_id, _score in raw_results]
scores = {chunk_id: score for chunk_id, score in raw_results}
rows = []
with SessionLocal() as db:
    chunks = db.query(Chunk).filter(Chunk.id.in_(chunk_ids)).all() if chunk_ids else []
    by_chunk_id = {chunk.id: chunk for chunk in chunks}
    documents = (
        db.query(Document).filter(Document.id.in_({chunk.document_id for chunk in chunks})).all()
        if chunks
        else []
    )
    by_document_id = {document.id: document for document in documents}
    for chunk_id in chunk_ids:
        chunk = by_chunk_id.get(chunk_id)
        if chunk is None:
            continue
        document = by_document_id.get(chunk.document_id)
        if document is None:
            continue
        metadata = {
            **(document.custom_metadata or {}),
            **(chunk.custom_metadata or {}),
        }
        rows.append(
            {
                "chunk_id": chunk_id,
                "source_uri": document.source_uri,
                "raw_text": chunk.text,
                "metadata": metadata,
                "score": scores.get(chunk_id),
            }
        )

print(json.dumps({"results": rows, "retrieval_config": body.get("retrieval_config", {})}))
"""


if __name__ == "__main__":
    raise SystemExit(main())
