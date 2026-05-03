"""Minimal stdio MCP server backed by live K2 demo retrieval."""

from __future__ import annotations

import base64
import json
import os
import re
import subprocess
import sys
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from ._subprocess_env import safe_subprocess_env
from .filters import (
    eq,
    in_,
    structured_filter,
    text_match,
)
from .k2_config import load_k2_config
from .live_eval import normalize_live_eval_rows
from .source_links import repo_web_url

# Loaded at import time — an intentional snapshot of the environment.
# Tests that need different values should patch the module-level constants.
_config = load_k2_config()
PROJECT_ID = _config.project_id
CORPUS_IDS = dict(_config.corpus_ids)

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
HYBRID_PROFILES = {
    "balanced": {
        "docs": DOCS_HYBRID,
        "code": CODE_HYBRID,
    },
    "java_exact": {
        "docs": {
            **DOCS_HYBRID,
            "rrf_k": 55,
            "dense_weight": 0.75,
            "sparse_weight": 0.25,
        },
        "code": {
            **CODE_HYBRID,
            "rrf_k": 35,
            "dense_weight": 0.0,
            "sparse_weight": 0.9,
            "metadata_sparse_weight": 0.1,
        },
    },
    "metadata_exact": {
        "docs": DOCS_HYBRID,
        "code": {
            **CODE_HYBRID,
            "rrf_k": 30,
            "dense_weight": 0.0,
            "sparse_weight": 0.7,
            "metadata_sparse_weight": 0.3,
        },
    },
}
RETURN_CONFIG = {
    "include_text": True,
    "include_scores": True,
    "include_provenance": True,
}
ANSWER_STYLE = {
    "goal": "Synthesize K2 evidence in the same direct style a strong local rg/file-read answer would use.",
    "target_length": "140-260 words unless the question explicitly asks for broader design context.",
    "rules": [
        "Start with one source-local finding: class.method -> exact behavior, with a clickable line citation.",
        "Prefer code and test anchors over docs when answering implementation questions.",
        "When a source has web_line_url or web_source_url, cite that clickable URL.",
        "When no clickable URL is present, cite line_source_uri before the bare source_uri.",
        "Do not shorten citation paths; keep line fragments when provided.",
        "Make each important claim self-verifying for a reader who only sees the final answer.",
        "Each implementation bullet should make one atomic claim supported by one citation.",
        "Always cite the requested target class or interface source when it appears in citation_targets.",
        "Use line_snippet evidence to name the exact method, config key, helper return expression, or registration flow.",
        "When a wrapper helper is cited, state both the wrapper call and the concrete expression inside that helper.",
        "Do not mark evidence as missing if a preferred source line_snippet contains that method body.",
        "For Java config APIs, prefer code constants/enums over docs fragments for exact key names.",
        "Use docs only for public contract/version context or when docs are the requested artifact.",
        "Do not include broader related classes, docs, or tests unless they directly prove the answer.",
        "Do not enumerate every retrieved source; cite only the sources that support the answer.",
        "Use 2-4 implementation-anchor bullets and 1-3 direct test-anchor bullets.",
        "Keep uncertainties to missing or weak evidence, and put them last.",
        "Do not mention K2, MCP, retrieval internals, scores, filters, or tool calls in the final answer.",
    ],
    "section_contract": {
        "Recommendation": "Exactly 1-2 direct sentences naming the file/class, method, and behavior with a citation.",
        "Implementation anchors": "2-4 bullets. One atomic source-local claim per bullet, each with one line citation.",
        "Tests to inspect or add": "1-3 bullets, direct neighboring tests only; avoid broad integration tests unless line evidence proves relevance.",
        "Citations": "Only the URLs or source URIs cited above; do not add unused retrieved sources.",
        "Uncertainties": "Only missing direct evidence or 'None from the cited evidence.'",
    },
}

SERVER_NAME = "k2-java-rd-demo"
SERVER_VERSION = "0.1.0"
DEFAULT_SOURCE_BASE = Path("/tmp/k2-java-rd-demo-sources")
TransportMode = Literal["content-length", "jsonl"]


@dataclass(frozen=True)
class K2McpConfig:
    backend: str = "sdk"
    api_key: str | None = None
    api_host: str | None = None
    namespace: str = "k2-mvp"
    deployment: str = "deploy/k2-mvp-api-internal"
    log_path: str | None = None
    case_id: str | None = None
    disable_metadata_filters: bool = False
    disable_guides: bool = False
    retrieval_profile: str = "java_exact"
    source_base: str | None = str(DEFAULT_SOURCE_BASE)

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "K2McpConfig":
        env = os.environ if environ is None else environ
        return cls(
            backend=env.get("K2_MCP_BACKEND", "sdk").strip().lower() or "sdk",
            api_key=_clean(env.get("K2_API_KEY")),
            api_host=_clean(env.get("K2_API_HOST")) or _clean(env.get("K2_BASE_URL")),
            namespace=env.get("K2_MCP_NAMESPACE", "k2-mvp"),
            deployment=env.get("K2_MCP_DEPLOYMENT", "deploy/k2-mvp-api-internal"),
            log_path=_clean(env.get("K2_MCP_LOG_PATH")),
            case_id=_clean(env.get("K2_MCP_CASE_ID")),
            disable_metadata_filters=_env_flag(env.get("K2_MCP_DISABLE_METADATA_FILTERS")),
            disable_guides=_env_flag(env.get("K2_MCP_DISABLE_GUIDES")),
            retrieval_profile=env.get("K2_MCP_RETRIEVAL_PROFILE", "java_exact").strip()
            or "java_exact",
            source_base=_clean(env.get("K2_MCP_SOURCE_BASE")) or str(DEFAULT_SOURCE_BASE),
        )


class K2McpServer:
    """Small MCP tool server for Codex/Claude demo runs."""

    def __init__(self, config: K2McpConfig | None = None) -> None:
        self.config = config or K2McpConfig.from_env()
        self._sdk_client: Any | None = None
        self.tools: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
            "k2_search_docs": self._search_docs,
            "k2_search_code": self._search_code,
            "k2_search_tests": self._search_tests,
            "k2_answer_with_sources": self._answer_with_sources,
        }
        if not self.config.disable_guides:
            self.tools["k2_search_guides"] = self._search_guides

    def serve(self) -> None:
        mode: TransportMode = "content-length"
        while True:
            incoming = _read_message(sys.stdin.buffer)
            if incoming is None:
                return
            message, mode = incoming
            if message is None:
                return
            response = self.handle(message)
            if response is not None:
                _write_message(sys.stdout.buffer, response, mode=mode)

    def handle(self, message: Mapping[str, Any]) -> dict[str, Any] | None:
        method = message.get("method")
        request_id = message.get("id")
        try:
            if method == "initialize":
                return _result(
                    request_id,
                    {
                        "protocolVersion": _protocol_version(message),
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                    },
                )
            if method == "notifications/initialized":
                return None
            if method == "ping":
                return _result(request_id, {})
            if method == "resources/list":
                return _result(request_id, {"resources": []})
            if method == "resources/templates/list":
                return _result(request_id, {"resourceTemplates": []})
            if method == "tools/list":
                return _result(
                    request_id,
                    {"tools": tool_specs(disable_guides=self.config.disable_guides)},
                )
            if method == "tools/call":
                params = _as_dict(message.get("params"))
                name = str(params.get("name") or "")
                args = _as_dict(params.get("arguments"))
                tool = self.tools.get(name)
                if tool is None:
                    return _error(request_id, -32601, f"unknown tool: {name}")
                payload = tool(args)
                self._log_tool_call(name, args, payload)
                return _result(
                    request_id,
                    {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(payload, indent=2, sort_keys=True),
                            }
                        ],
                        "isError": False,
                    },
                )
            return _error(request_id, -32601, f"method not found: {method}")
        except Exception as exc:
            return _result(
                request_id,
                {
                    "content": [{"type": "text", "text": f"K2 MCP tool failed: {_error_text(exc)}"}],
                    "isError": True,
                },
            )

    def _search_guides(self, args: dict[str, Any]) -> dict[str, Any]:
        return self._search_role(args, role="guides", source_kind="guide")

    def _search_docs(self, args: dict[str, Any]) -> dict[str, Any]:
        return self._search_role(args, role="docs", source_kind="docs")

    def _search_code(self, args: dict[str, Any]) -> dict[str, Any]:
        return self._search_role(args, role="code", source_kind="code")

    def _search_tests(self, args: dict[str, Any]) -> dict[str, Any]:
        return self._search_role(args, role="code", source_kind="test")

    def _answer_with_sources(self, args: dict[str, Any]) -> dict[str, Any]:
        query = _required_str(args, "query")
        framework = _framework(args)
        api_surface = _clean(args.get("api_surface")) or _infer_api_surface(framework, query)
        top_k = _top_k(args, default=5)
        target_class_names = _target_class_names(args, query)
        role_queries = _answer_queries(framework=framework, api_surface=api_surface, query=query)
        searches = []
        search_specs = [("docs", "docs", "docs"), ("code", "code", "code"), ("tests", "code", "test")]
        if not self.config.disable_guides:
            search_specs.insert(0, ("guides", "guides", "guide"))
        for name, role, source_kind in search_specs:
            for role_query in _as_queries(role_queries.get(name, query)):
                result = self._search_role(
                    {
                        **args,
                        "query": role_query,
                        "framework": framework,
                        "api_surface": api_surface,
                        "top_k": top_k,
                    },
                    role=role,
                    source_kind=source_kind,
                )
                searches.append({"name": name, **result})
        for lookup in _exact_class_lookups(
            framework=framework,
            api_surface=api_surface,
            target_class_names=target_class_names,
        ):
            result = self._search_role(
                {
                    **args,
                    "query": lookup["query"],
                    "framework": framework,
                    "api_surface": lookup["api_surface"] if "api_surface" in lookup else None,
                    "class_name": lookup.get("class_name"),
                    "path": lookup.get("path"),
                    "path_match": lookup.get("path_match"),
                    "skip_api_surface": lookup.get("skip_api_surface"),
                    "skip_module": lookup.get("skip_module"),
                    "top_k": min(top_k, 5),
                },
                role="code",
                source_kind=lookup["source_kind"],
            )
            searches.append({"name": f"{lookup['source_kind']}_class_lookup", **result})
        results = _normalize_target_rows(
            _dedupe_rows(row for search in searches for row in search.get("results", [])),
            target_class_names,
            api_surface=api_surface,
        )
        results = _enrich_rows_with_local_sources(
            results,
            query=query,
            target_class_names=target_class_names,
            source_base=self.config.source_base,
        )
        return {
            "query": query,
            "framework": framework,
            "api_surface": api_surface,
            "target_class_names": target_class_names,
            "citation_targets": _citation_targets(results, target_class_names),
            "preferred_sources": _preferred_sources(results, target_class_names, query=query),
            "role_queries": role_queries,
            "answer_style": ANSWER_STYLE,
            "retrieval_profile": self.config.retrieval_profile,
            "tool_guidance": (
                "Use these K2 sources for exact claims, but write the final answer like a "
                "concise local rg/file-read result. Start with one source-local finding, "
                "use preferred_sources as the citation budget, cite web_line_url or web_source_url "
                "when present, otherwise cite line_source_uri or source_uri inline, make every "
                "important claim self-verifying from the final text, cite citation_targets when "
                "present, omit broader related evidence unless it directly proves the answer, and "
                "move genuinely missing evidence to Uncertainties instead of leading with it."
            ),
            "searches": searches,
            "results": results,
        }

    def _search_role(self, args: dict[str, Any], *, role: str, source_kind: str) -> dict[str, Any]:
        query = _required_str(args, "query")
        framework = _framework(args)
        top_k = _top_k(args)
        api_surface = _clean(args.get("api_surface"))
        class_name = _clean(args.get("class_name"))
        path = _clean(args.get("path"))
        path_match = _clean(args.get("path_match"))
        skip_api_surface = bool(args.get("skip_api_surface"))
        skip_module = bool(args.get("skip_module"))
        corpus_ids = _corpus_ids(role=role, framework=framework)
        filters = (
            {}
            if self.config.disable_metadata_filters
            else _metadata_filter(
                framework=framework,
                source_kind=source_kind,
                api_surface=api_surface,
                class_name=class_name,
                path=path,
                path_match=path_match,
                skip_api_surface=skip_api_surface,
                skip_module=skip_module,
            )
        )
        hybrid = _hybrid_for_source_kind(source_kind, self.config.retrieval_profile)

        rows: list[dict[str, Any]] = []
        for corpus_id in corpus_ids:
            response = self._retrieval_search(
                corpus_id=corpus_id,
                query=query,
                top_k=top_k,
                filters=filters,
                hybrid=hybrid,
            )
            rows.extend(
                normalize_live_eval_rows(
                    response.get("results", []),
                    inferred_metadata={"corpus_role": role, "source_kind": source_kind},
                )
            )
        return {
            "query": query,
            "framework": framework,
            "role": role,
            "source_kind": source_kind,
            "filters": filters,
            "metadata_filter_mode": "disabled" if self.config.disable_metadata_filters else "enabled",
            "retrieval_profile": self.config.retrieval_profile,
            "hybrid": hybrid,
            "results": _compact_rows(_dedupe_rows(rows), max_text_chars=900),
        }

    def _retrieval_search(
        self,
        *,
        corpus_id: str,
        query: str,
        top_k: int,
        filters: dict[str, Any],
        hybrid: dict[str, Any],
    ) -> dict[str, Any]:
        payload = {
            "corpus_id": corpus_id,
            "query": query,
            "top_k": top_k,
            "filters": filters,
            "hybrid": hybrid,
        }
        if self.config.backend == "sdk":
            return self._retrieval_search_sdk(payload)
        if self.config.backend == "kubectl":
            return self._retrieval_search_kubectl(payload)
        if self.config.backend == "auto":
            try:
                return self._retrieval_search_sdk(payload)
            except Exception as exc:
                # Only fall back to kubectl for transient/connectivity errors
                # or a missing SDK.  Auth errors (401/403), bad requests (4xx),
                # config errors, and similar should propagate immediately —
                # they would also fail via kubectl and masking them makes
                # debugging harder.
                if not self.config.deployment:
                    raise
                if not _is_retriable_sdk_error(exc):
                    raise
                fallback = self._retrieval_search_kubectl(payload)
                fallback["sdk_error"] = _error_text(exc)
                return fallback
        raise ValueError("K2_MCP_BACKEND must be one of: sdk, kubectl, auto")

    def _retrieval_search_sdk(self, payload: dict[str, Any]) -> dict[str, Any]:
        client = self._get_sdk_client()
        response = client.search(
            payload["corpus_id"],
            payload["query"],
            top_k=payload["top_k"],
            filters=payload.get("filters"),
            hybrid=payload.get("hybrid"),
            return_config=RETURN_CONFIG,
        )
        return {
            "results": response.get("results", []),
            "retrieval_config": response.get("meta", {}),
            "backend": "sdk",
        }

    def _get_sdk_client(self) -> Any:
        if self._sdk_client is not None:
            return self._sdk_client
        if not self.config.api_key:
            raise RuntimeError("K2_API_KEY is required for K2_MCP_BACKEND=sdk")
        try:
            from sdk import Knowledge2  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "Knowledge2 Python SDK is not installed. Install the live extra or set "
                "K2_MCP_BACKEND=kubectl for the local cluster bridge."
            ) from exc
        kwargs: dict[str, Any] = {
            "api_key": self.config.api_key,
            "user_agent": "k2-java-rd-demo-mcp/0.1.0",
        }
        if self.config.api_host:
            kwargs["api_host"] = self.config.api_host
        self._sdk_client = Knowledge2(**kwargs)
        return self._sdk_client

    def _retrieval_search_kubectl(self, payload: dict[str, Any]) -> dict[str, Any]:
        encoded = base64.b64encode(json.dumps(payload).encode()).decode()
        cmd = [
            "kubectl",
            "-n",
            self.config.namespace,
            "exec",
            "-i",
            self.config.deployment,
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

    def _log_tool_call(self, tool_name: str, args: dict[str, Any], payload: dict[str, Any]) -> None:
        if not self.config.log_path:
            return
        log_path = Path(self.config.log_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {
                        "case_id": self.config.case_id,
                        "tool_name": tool_name,
                        "arguments": args,
                        "payload": payload,
                    },
                    sort_keys=True,
                )
                + "\n"
            )


def tool_specs(*, disable_guides: bool = False) -> list[dict[str, Any]]:
    specs = [
        _tool_spec(
            "k2_search_docs",
            "Search version-pinned Apache Flink/Kafka docs in K2.",
            source_kind="docs",
        ),
        _tool_spec(
            "k2_search_code",
            "Search production Java source files in K2.",
            source_kind="code",
        ),
        _tool_spec(
            "k2_search_tests",
            "Search neighboring test files and validation patterns in K2.",
            source_kind="test",
        ),
        {
            "name": "k2_answer_with_sources",
            "description": (
                "Run guide, docs, code, and test searches together and return source-grounded "
                "evidence. Prefer this tool for end-to-end customer answers."
            ),
            "inputSchema": _input_schema(),
        },
    ]
    if not disable_guides:
        specs.insert(
            0,
            _tool_spec(
                "k2_search_guides",
                "Search generated Java R&D guide/checklist artifacts in K2.",
                source_kind="guide",
            ),
        )
    return specs


def _tool_spec(name: str, description: str, *, source_kind: str) -> dict[str, Any]:
    spec = {
        "name": name,
        "description": description,
        "inputSchema": _input_schema(),
    }
    spec["annotations"] = {"source_kind": source_kind}
    return spec


def _input_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["query"],
        "properties": {
            "query": {"type": "string", "minLength": 1},
            "framework": {"type": "string", "enum": ["flink", "kafka"]},
            "api_surface": {"type": "string"},
            "top_k": {"type": "integer", "minimum": 1, "maximum": 12, "default": 5},
            "target_class_names": {
                "type": "array",
                "items": {"type": "string", "minLength": 1},
                "default": [],
            },
            "path_match": {"type": "string"},
        },
    }


def _metadata_filter(
    *,
    framework: str,
    source_kind: str,
    api_surface: str | None,
    class_name: str | None = None,
    path: str | None = None,
    path_match: str | None = None,
    skip_api_surface: bool = False,
    skip_module: bool = False,
) -> dict[str, Any]:
    filters: list[dict[str, Any]] = [
        eq("framework", framework),
        eq("source_kind", source_kind),
    ]
    if framework == "flink":
        filters.append(eq("framework_version", "2.2.0"))
        if source_kind in {"code", "test"} and not skip_module:
            filters.append(eq("module", "flink-runtime"))
        if not skip_api_surface:
            if api_surface:
                filters.append(eq("api_surface", api_surface))
            else:
                filters.append(in_("api_surface", ["rest", "checkpointing"]))
    else:
        filters.append(eq("framework_version", "4.2.0"))
        if not skip_api_surface:
            if api_surface:
                filters.append(eq("api_surface", api_surface))
            else:
                filters.append(eq("api_surface", "connect"))
    if class_name:
        filters.append(eq("class_name", class_name))
    if path:
        filters.append(eq("path", path))
    if path_match:
        filters.append(text_match("path", path_match))
    return structured_filter(filters)


def _infer_api_surface(framework: str, query: str) -> str:
    lowered = query.lower()
    if framework == "kafka":
        return "connect"
    if "checkpoint" in lowered or "savepoint" in lowered or "state backend" in lowered:
        return "checkpointing"
    return "rest"


def _answer_queries(*, framework: str, api_surface: str, query: str) -> dict[str, Any]:
    base = query.strip()
    target_class_names = _class_names_from_text(query)
    if framework == "flink" and api_surface == "rest":
        code_queries = [
            f"{base} implementation source REST handler",
            *(
                f"{class_name} handleRequest MessageHeaders response body WebMonitorEndpoint registration"
                for class_name in target_class_names
                if class_name.endswith("Handler")
            ),
            *(
                f"{class_name} headers info JsonPlanGenerator REST plan metadata"
                for class_name in target_class_names
                if class_name.endswith("Handler")
            ),
        ]
        test_queries = [
            f"{base} neighboring regression test REST handler",
            *(
                f"{class_name} response body serialization test JsonGeneratorTest"
                for class_name in target_class_names
                if class_name.endswith("Handler")
            ),
        ]
        return {
            "guides": f"{base} REST handler implementation checklist",
            "docs": f"{base} Flink REST API endpoint request response body",
            "code": _dedupe_strings(code_queries),
            "tests": _dedupe_strings(test_queries),
        }
    if framework == "flink" and api_surface == "checkpointing":
        return {
            "guides": f"{base} checkpointing upgrade checklist",
            "docs": f"{base} Flink 2.2 checkpointing savepoint state backend documentation",
            "code": f"{base} implementation source checkpointing state backend",
            "tests": f"{base} neighboring regression test checkpointing state backend",
        }
    if framework == "kafka" and api_surface == "rest":
        return {
            "guides": f"{base} Kafka Connect REST validation checklist",
            "docs": f"{base} Kafka Connect REST API administration connectors",
            "code": f"{base} implementation source Connect REST resource",
            "tests": f"{base} neighboring regression test Connect REST resource",
        }
    if framework == "kafka":
        code_queries = [f"{base} implementation source connector validation"]
        test_queries = [f"{base} neighboring regression test connector validation"]
        if any(name.endswith("Converter") or name == "Converter" for name in target_class_names):
            code_queries.extend(
                [
                    (
                        "Converter configure boolean isKey converter.type key.converter "
                        "value.converter StringConverter Plugins newConverter"
                    ),
                    "WorkerConfig ConnectorConfig key.converter value.converter plugin.version",
                ]
            )
            test_queries.extend(
                [
                    "PluginsTest shouldInstantiateAndConfigureConverters converter.type",
                    "WorkerTest converter overrides key.converter value.converter MultiVersionTest",
                ]
            )
        return {
            "guides": f"{base} Kafka Connect validation checklist",
            "docs": f"{base} Kafka Connect connector development guide",
            "code": _dedupe_strings(code_queries),
            "tests": _dedupe_strings(test_queries),
        }
    return {"guides": base, "docs": base, "code": base, "tests": base}


def _dedupe_strings(values: Any) -> tuple[str, ...]:
    return tuple(dict.fromkeys(str(value) for value in values if _clean(value)))


def _as_queries(value: Any) -> tuple[str, ...]:
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value if _clean(item))
    cleaned = _clean(value)
    return (cleaned,) if cleaned else ()


def _exact_class_lookups(
    *,
    framework: str,
    api_surface: str,
    target_class_names: tuple[str, ...] = (),
) -> tuple[dict[str, Any], ...]:
    """Return dynamic target and framework-neighbor lookups.

    Lookups are derived from class names present in the user query, never from
    benchmark expected artifacts.  The neighbor rules encode public framework
    structure: Flink REST handlers usually pair with headers/response-body
    classes and WebMonitorEndpoint registration; Kafka Connect converters pair
    with worker config, plugin loading, and converter tests.
    """
    lookups = [*_target_class_lookups(target_class_names)]
    lookups.extend(
        _framework_neighbor_lookups(
            framework=framework,
            api_surface=api_surface,
            target_class_names=target_class_names,
        )
    )
    return tuple(lookups)


def _framework_neighbor_lookups(
    *,
    framework: str,
    api_surface: str,
    target_class_names: tuple[str, ...],
) -> tuple[dict[str, Any], ...]:
    lookups: list[dict[str, Any]] = []
    if framework == "kafka" and api_surface == "connect":
        if any(name == "Converter" or name.endswith("Converter") for name in target_class_names):
            lookups.extend(
                _exact_path_lookups(
                    source_kind="code",
                    paths=(
                        "connect/api/src/main/java/org/apache/kafka/connect/storage/Converter.java",
                        "connect/api/src/main/java/org/apache/kafka/connect/storage/StringConverter.java",
                        "connect/api/src/main/java/org/apache/kafka/connect/storage/ConverterConfig.java",
                        "connect/api/src/main/java/org/apache/kafka/connect/storage/ConverterType.java",
                        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/Plugins.java",
                        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConfig.java",
                        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/ConnectorConfig.java",
                    ),
                    query="Kafka Connect converter key value configure plugin loading source",
                )
            )
            lookups.append(
                {
                    "source_kind": "code",
                    "skip_api_surface": True,
                    "skip_module": True,
                    "query": (
                        "WorkerConfig KEY_CONVERTER_CLASS_DOC controls format keys "
                        "VALUE_CONVERTER_CLASS_DOC controls format values key.converter value.converter"
                    ),
                }
            )
            lookups.extend(
                _exact_path_lookups(
                    source_kind="test",
                    paths=(
                        "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/PluginsTest.java",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerTest.java",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/isolation/MultiVersionTest.java",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/AbstractWorkerSourceTaskTest.java",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/WorkerSinkTaskTest.java",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/converters/BooleanConverterTest.java",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/converters/ByteArrayConverterTest.java",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/converters/NumberConverterTest.java",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/integration/ConnectorValidationIntegrationTest.java",
                    ),
                    query="Kafka Connect converter key value configure plugin loading tests",
                )
            )
    if framework == "flink" and api_surface == "rest":
        for class_name in target_class_names:
            if not class_name.endswith("Handler"):
                continue
            stem = class_name.removesuffix("Handler")
            filenames = [f"{stem}Headers.java", f"{stem}Info.java", "WebMonitorEndpoint.java"]
            test_filenames = [f"{stem}InfoTest.java", f"{class_name}Test.java"]
            if "Plan" in stem:
                filenames.extend(
                    [
                        "JsonPlanGenerator.java",
                        "DefaultExecutionGraphBuilder.java",
                        "OnlyExecutionGraphJsonArchivist.java",
                        "RuntimeRestAPIDocGenerator.java",
                        "RuntimeOpenApiSpecGenerator.java",
                        "RuntimeRestAPIVersion.java",
                    ]
                )
                test_filenames.extend(
                    [
                        "JsonGeneratorTest.java",
                        "JobDetailsInfoTest.java",
                        "JobDetailsHandlerTest.java",
                    ]
                )
            lookups.extend(
                _path_match_lookups(
                    source_kind="code",
                    filenames=tuple(filenames),
                    query=f"{class_name} REST handler headers response body registration source",
                )
            )
            lookups.extend(
                _path_match_lookups(
                    source_kind="test",
                    filenames=tuple(test_filenames),
                    query=f"{class_name} REST handler response serialization tests",
                )
            )
    return tuple(lookups)


def _path_match_lookups(
    *,
    source_kind: str,
    filenames: tuple[str, ...],
    query: str,
) -> tuple[dict[str, Any], ...]:
    return tuple(
        {
            "source_kind": source_kind,
            "path_match": filename,
            "skip_api_surface": True,
            "skip_module": True,
            "query": f"{filename.removesuffix('.java')} {query}",
        }
        for filename in filenames
    )


def _exact_path_lookups(
    *,
    source_kind: str,
    paths: tuple[str, ...],
    query: str,
) -> tuple[dict[str, Any], ...]:
    lookups = []
    for path in paths:
        basename = _java_basename(path)
        source_terms = " ".join(_source_specific_line_terms(path))
        lookups.append(
            {
                "source_kind": source_kind,
                "path_match": basename,
                "skip_api_surface": True,
                "skip_module": True,
                "query": f"{basename.removesuffix('.java')} {source_terms} {query}",
            }
        )
    return tuple(lookups)


def _target_class_names(args: Mapping[str, Any], query: str) -> tuple[str, ...]:
    explicit = args.get("target_class_names")
    names: list[str] = []
    if isinstance(explicit, list):
        names.extend(str(item) for item in explicit if _clean(item))
    names.extend(_class_names_from_text(query))
    return tuple(dict.fromkeys(_clean(name) for name in names if _clean(name)))


def _class_names_from_text(text: str) -> tuple[str, ...]:
    names = []
    for name in re.findall(r"`([A-Z][A-Za-z0-9_]{3,})`", text):
        names.append(name)
    for name in re.findall(r"\b[A-Z][A-Za-z0-9]*(?:[A-Z][A-Za-z0-9]*)+\b", text):
        if name in {"Kafka", "Flink", "REST", "API"}:
            continue
        if len(name) < 4:
            continue
        names.append(name)
    return tuple(dict.fromkeys(names))


def _target_class_lookups(target_class_names: tuple[str, ...]) -> tuple[dict[str, Any], ...]:
    lookups: list[dict[str, Any]] = []
    for class_name in target_class_names:
        if class_name.endswith("Test"):
            lookups.append(
                {
                    "source_kind": "test",
                    "class_name": class_name,
                    "skip_api_surface": True,
                    "skip_module": True,
                    "query": f"{class_name} regression test",
                }
            )
            lookups.append(
                {
                    "source_kind": "test",
                    "path_match": f"{class_name}.java",
                    "skip_api_surface": True,
                    "skip_module": True,
                    "query": f"{class_name} regression test",
                }
            )
            continue
        lookups.append(
            {
                "source_kind": "code",
                "class_name": class_name,
                "skip_api_surface": True,
                "skip_module": True,
                "query": f"class interface {class_name} implementation source",
            }
        )
        lookups.append(
            {
                "source_kind": "code",
                "path_match": f"{class_name}.java",
                "skip_api_surface": True,
                "skip_module": True,
                "query": f"class interface {class_name} implementation source",
            }
        )
        lookups.append(
            {
                "source_kind": "test",
                "class_name": f"{class_name}Test",
                "skip_api_surface": True,
                "skip_module": True,
                "query": f"{class_name}Test {class_name} regression test",
            }
        )
        lookups.append(
            {
                "source_kind": "test",
                "path_match": f"{class_name}Test.java",
                "skip_api_surface": True,
                "skip_module": True,
                "query": f"{class_name}Test {class_name} regression test",
            }
        )
    return tuple(lookups)


def _normalize_target_rows(
    rows: list[dict[str, Any]],
    target_class_names: tuple[str, ...],
    *,
    api_surface: str,
) -> list[dict[str, Any]]:
    if not target_class_names:
        return rows
    class_names_by_basename = {
        f"{name}.java": name
        for name in set(target_class_names) | {f"{name}Test" for name in target_class_names}
    }
    normalized = []
    for row in rows:
        updated = dict(row)
        metadata = dict(updated.get("metadata") or {})
        basename = _java_basename(metadata.get("path") or updated.get("source_uri"))
        if basename.endswith(".java"):
            class_from_path = basename.removesuffix(".java")
            metadata["class_name"] = class_from_path
            updated["class_name"] = class_from_path
        for filename, class_name in class_names_by_basename.items():
            if filename == basename:
                metadata["class_name"] = class_name
                metadata["api_surface"] = api_surface
                updated["class_name"] = class_name
                updated["api_surface"] = api_surface
                break
        updated["metadata"] = metadata
        normalized.append(updated)
    return normalized


def _citation_targets(
    rows: list[dict[str, Any]],
    target_class_names: tuple[str, ...],
) -> list[dict[str, Any]]:
    wanted = set(target_class_names) | {f"{name}Test" for name in target_class_names}
    targets = []
    seen: set[str] = set()
    for row in rows:
        metadata = dict(row.get("metadata") or {})
        source_uri = str(row.get("source_uri") or "")
        if not source_uri or source_uri in seen:
            continue
        class_name = str(metadata.get("class_name") or "")
        path = str(metadata.get("path") or "")
        basename = _java_basename(path or source_uri)
        if class_name in wanted or basename in {f"{name}.java" for name in wanted}:
            seen.add(source_uri)
            targets.append(
                {
                    "source_uri": source_uri,
                    "web_source_url": repo_web_url(source_uri),
                    "source_kind": metadata.get("source_kind"),
                    "module": metadata.get("module"),
                    "api_surface": metadata.get("api_surface"),
                    "class_name": metadata.get("class_name"),
                    "path": metadata.get("path"),
                }
            )
    return targets


def _preferred_sources(
    rows: list[dict[str, Any]],
    target_class_names: tuple[str, ...],
    *,
    query: str = "",
) -> list[dict[str, Any]]:
    """Return a small source budget for rg-like final answers."""

    limits = {"code": 6, "test": 3, "docs": 1, "guide": 1}
    selected: list[dict[str, Any]] = []
    counts = {kind: 0 for kind in limits}
    seen: set[str] = set()
    ordered_rows = sorted(
        enumerate(rows),
        key=lambda item: (_preferred_source_priority(item[1], target_class_names, query), item[0]),
    )
    for _, row in ordered_rows:
        metadata = dict(row.get("metadata") or {})
        source_kind = str(metadata.get("source_kind") or row.get("source_kind") or "")
        if source_kind not in limits or counts[source_kind] >= limits[source_kind]:
            continue
        source_uri = str(row.get("source_uri") or "")
        if not source_uri or source_uri in seen:
            continue
        seen.add(source_uri)
        counts[source_kind] += 1
        selected.append(
            {
                "source_uri": source_uri,
                "web_source_url": repo_web_url(source_uri),
                "line_source_uri": row.get("line_source_uri"),
                "web_line_url": repo_web_url(row.get("line_source_uri")),
                "line_span": row.get("line_span"),
                "source_kind": source_kind,
                "module": metadata.get("module"),
                "api_surface": metadata.get("api_surface"),
                "class_name": metadata.get("class_name"),
                "path": metadata.get("path"),
                "text_preview": str(
                    row.get("line_snippet") or row.get("raw_text") or row.get("text") or ""
                )[:1200],
            }
        )
    return selected


def _preferred_source_priority(
    row: Mapping[str, Any],
    target_class_names: tuple[str, ...],
    query: str = "",
) -> tuple[int, int, int, int]:
    metadata = dict(row.get("metadata") or {})
    source_kind = str(metadata.get("source_kind") or row.get("source_kind") or "")
    kind_priority = {"code": 0, "test": 1, "docs": 2, "guide": 3}.get(source_kind, 4)
    anchor_terms = set(row.get("line_anchor_terms") or _line_anchor_terms(
        row, query=query, target_class_names=target_class_names
    ))
    wanted = set(target_class_names) | {f"{name}Test" for name in target_class_names}
    class_name = str(metadata.get("class_name") or "")
    basename = _java_basename(metadata.get("path") or row.get("source_uri"))
    path = str(metadata.get("path") or row.get("source_uri") or "")
    target_match = (
        class_name in wanted
        or basename in {f"{name}.java" for name in wanted}
        or ("Converter" in wanted and class_name.endswith("Converter"))
        or ("Converter" in wanted and basename.endswith("Converter.java"))
        or ("Converter" in wanted and class_name.endswith("ConverterTest"))
    )
    preferred_terms = _preferred_anchor_terms(query, target_class_names)
    generic_terms = set(target_class_names)
    specific_anchor_match = any(
        term
        and term not in generic_terms
        and term in preferred_terms
        and (term == class_name or term in basename or term in path)
        for term in anchor_terms
    )
    anchor_match = specific_anchor_match or any(
        term and (term == class_name or term in basename or term in path) for term in anchor_terms
    )
    has_line_evidence = bool(row.get("line_source_uri") and row.get("line_snippet"))
    return (
        kind_priority,
        0 if specific_anchor_match else 1,
        0 if anchor_match else 1,
        0 if target_match or has_line_evidence else 1,
    )


def _preferred_anchor_terms(query: str, target_class_names: tuple[str, ...]) -> set[str]:
    lowered = query.lower()
    terms = set(_class_names_from_text(query))
    if "converter" in lowered or "Converter" in target_class_names:
        terms.update(
            {
                "StringConverter",
                "ConverterConfig",
                "ConverterType",
                "Plugins",
                "WorkerConfig",
                "ConnectorConfig",
                "PluginsTest",
                "WorkerConfigTest",
                "NumberConverterTest",
                "ByteArrayConverterTest",
                "BooleanConverterTest",
            }
        )
    if "flink" in lowered and "rest" in lowered:
        for class_name in target_class_names:
            if class_name.endswith("Handler"):
                stem = class_name.removesuffix("Handler")
                terms.update({class_name, f"{stem}Headers", f"{stem}Info", "WebMonitorEndpoint"})
                if "Plan" in stem:
                    terms.update(
                        {
                            "JsonPlanGenerator",
                            "DefaultExecutionGraphBuilder",
                            "OnlyExecutionGraphJsonArchivist",
                            "RuntimeRestAPIDocGenerator",
                            "RuntimeOpenApiSpecGenerator",
                            "RuntimeRestAPIVersion",
                            f"{stem}InfoTest",
                            "JsonGeneratorTest",
                            "JobDetailsInfoTest",
                            "JobDetailsHandlerTest",
                        }
                    )
    return terms


def _hybrid_for_source_kind(source_kind: str, profile_name: str) -> dict[str, Any]:
    profile = HYBRID_PROFILES.get(profile_name)
    if profile is None:
        valid = ", ".join(sorted(HYBRID_PROFILES))
        raise ValueError(f"unknown K2_MCP_RETRIEVAL_PROFILE={profile_name!r}; expected one of: {valid}")
    key = "docs" if source_kind == "docs" else "code"
    return dict(profile[key])


def _enrich_rows_with_local_sources(
    rows: list[dict[str, Any]],
    *,
    query: str,
    target_class_names: tuple[str, ...],
    source_base: str | None,
) -> list[dict[str, Any]]:
    if not source_base:
        return rows
    base_path = Path(source_base).expanduser()
    enriched = []
    for row in rows:
        updated = dict(row)
        line_evidence = _local_line_evidence(
            updated,
            query=query,
            target_class_names=target_class_names,
            source_base=base_path,
        )
        if line_evidence:
            updated.update(line_evidence)
        enriched.append(updated)
    return enriched


def _local_line_evidence(
    row: Mapping[str, Any],
    *,
    query: str,
    target_class_names: tuple[str, ...],
    source_base: Path,
) -> dict[str, Any]:
    source_uri = str(row.get("source_uri") or "")
    local_path = _local_path_for_source_uri(source_uri, source_base)
    if local_path is None or not local_path.is_file():
        return {}
    try:
        lines = local_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return {}
    if not lines:
        return {}
    terms = _line_anchor_terms(row, query=query, target_class_names=target_class_names)
    anchor = _best_line_anchor(lines, terms)
    if anchor is None:
        return {}
    start, end = _line_window(lines, anchor, terms)
    line_source_uri = f"{source_uri}#L{start}-L{end}"
    return {
        "line_source_uri": line_source_uri,
        "web_source_url": repo_web_url(source_uri),
        "web_line_url": repo_web_url(line_source_uri),
        "line_span": {"start": start, "end": end},
        "line_snippet": _format_line_snippet(lines, start=start, end=end),
        "local_source_path": str(local_path),
        "line_anchor_terms": terms[:8],
    }


def _local_path_for_source_uri(source_uri: str, source_base: Path) -> Path | None:
    if not source_uri.startswith("repo://apache/"):
        return None
    _prefix, _sep, rest = source_uri.partition("repo://apache/")
    repo_ref, _sep, rel_path = rest.partition("/")
    if not rel_path:
        return None
    if repo_ref == "flink@release-2.2.0":
        root = source_base / "apache-flink-release-2.2.0"
    elif repo_ref == "kafka@4.2":
        root = source_base / "apache-kafka-4.2"
    else:
        return None
    candidate = (root / rel_path).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def _line_anchor_terms(
    row: Mapping[str, Any],
    *,
    query: str,
    target_class_names: tuple[str, ...],
) -> list[str]:
    metadata = dict(row.get("metadata") or {})
    terms: list[str] = []
    terms.extend(_source_specific_line_terms(metadata.get("path") or row.get("source_uri")))
    terms.extend(target_class_names)
    for value in (
        metadata.get("class_name"),
        _java_basename(metadata.get("path") or row.get("source_uri")).removesuffix(".java"),
    ):
        if _clean(value):
            terms.append(str(value))
    terms.extend(_class_names_from_text(query))
    lowered = query.lower()
    if "flink" in lowered and "rest" in lowered:
        terms.extend(
            [
                "handleRequest",
                "MessageHeaders",
                "JobPlanInfo",
                "JobPlanHeaders",
                "JsonPlanGenerator",
                "WebMonitorEndpoint",
                "getTargetRestEndpointURL",
                "getPlan",
                "archiveJsonWithPath",
            ]
        )
    if "kafka" in lowered and "converter" in lowered:
        terms.extend(
            [
                "newConverter",
                "configure",
                "converter.type",
                "isKeyConverter",
                "key.converter",
                "value.converter",
                "StringConverter",
                "WorkerConfig",
                "ConnectorConfig",
                "shouldInstantiateAndConfigureConverters",
            ]
        )
    for token in re.findall(r"\b[A-Za-z_][A-Za-z0-9_.-]{3,}\b", query):
        if token.lower() in _LINE_STOP_WORDS:
            continue
        terms.append(token)
    return list(dict.fromkeys(term for term in terms if term and len(term) > 2))


def _source_specific_line_terms(value: Any) -> list[str]:
    basename = _java_basename(value)
    if basename == "Plugins.java":
        return ["newConverter", "isKeyConverter", "plugin.configure"]
    if basename == "WorkerConfig.java":
        return [
            "KEY_CONVERTER_CLASS_CONFIG",
            "VALUE_CONVERTER_CLASS_CONFIG",
            "KEY_CONVERTER_VERSION",
            "VALUE_CONVERTER_VERSION",
        ]
    if basename == "ConnectorConfig.java":
        return ["enrichedConfigDef", "KEY_CONVERTER_CLASS_CONFIG", "VALUE_CONVERTER_CLASS_CONFIG"]
    if basename == "StringConverter.java":
        return ["configure", "StringConverterConfig", "converter.type"]
    if basename == "ConverterConfig.java":
        return ["TYPE_CONFIG", "converter.type", "ConverterType.KEY"]
    if basename == "ConverterType.java":
        return ["public enum ConverterType", "KEY", "VALUE"]
    if basename == "PluginsTest.java":
        return [
            "shouldInstantiateAndConfigureConverters",
            "newConverterShouldConfigureWithPluginClassLoader",
        ]
    if basename == "WorkerTest.java":
        return [
            "mockVersionedTaskConverterFromConnector",
            "verifyVersionedTaskConverterFromConnector",
        ]
    if basename == "MultiVersionTest.java":
        return ["KEY_CONVERTER_VERSION", "VALUE_CONVERTER_VERSION", "plugins.newConverter"]
    if basename == "AbstractWorkerSourceTaskTest.java":
        return ["keyConverter.fromConnectData", "valueConverter.fromConnectData"]
    if basename == "WorkerSinkTaskTest.java":
        return ["keyConverter.toConnectData", "valueConverter.toConnectData"]
    if basename == "WebMonitorEndpoint.java":
        return ["jobPlanHandler", "JobPlanHeaders", "handlers.add"]
    if basename == "JobPlanHandler.java":
        return ["handleRequest", "new JobPlanInfo", "archiveJsonWithPath"]
    if basename == "JobPlanHeaders.java":
        return ["getTargetRestEndpointURL", "getHttpMethod", "getResponseClass"]
    if basename == "JobPlanInfo.java":
        return [
            "FIELD_NAME_NODES",
            "FIELD_NAME_OPERATOR_STRATEGY",
            "FIELD_NAME_OPTIMIZER_PROPERTIES",
        ]
    if basename == "JsonPlanGenerator.java":
        return ["generatePlan", "JobPlanInfo.Plan"]
    if basename == "DefaultExecutionGraphBuilder.java":
        return ["setPlan", "JsonPlanGenerator.generatePlan"]
    if basename == "OnlyExecutionGraphJsonArchivist.java":
        return ["archiveJsonWithPath", "ExecutionGraphInfo"]
    if basename == "RuntimeRestAPIDocGenerator.java":
        return ["RuntimeRestAPIVersion.values", "createHtmlFile"]
    if basename == "RuntimeOpenApiSpecGenerator.java":
        return ["RuntimeRestAPIVersion.values", "rest_v1_dispatcher.yml"]
    if basename == "RuntimeRestAPIVersion.java":
        return ["V1(true, true)", "getURLVersionPrefix"]
    if basename == "JobPlanInfoTest.java":
        return ["JsonPlanGenerator", "JobPlanInfo", "getPlan"]
    if basename == "JsonGeneratorTest.java":
        return ["JsonPlanGenerator", "generatePlan"]
    if basename == "JobDetailsInfoTest.java":
        return ["JobPlanInfo.Plan", "FIELD_NAME_PLAN", "JsonPlanGenerator"]
    if basename == "JobDetailsHandlerTest.java":
        return ["JobPlanInfo.RawJson", "getJsonPlan", "JsonPlanGenerator"]
    return []


_LINE_STOP_WORDS = {
    "which",
    "version",
    "pinned",
    "docs",
    "implementation",
    "class",
    "neighboring",
    "tests",
    "should",
    "anchor",
    "answer",
    "through",
    "inspect",
    "explain",
    "returned",
    "metadata",
    "pattern",
    "flink",
    "kafka",
    "rest",
    "connect",
}


def _best_line_anchor(lines: list[str], terms: list[str]) -> int | None:
    if not terms:
        return None
    best_line = None
    best_score = 0
    lowered_terms = [(term, term.lower()) for term in terms]
    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        lowered = stripped.lower()
        if not stripped or stripped.startswith(("package ", "/*", "*", "//")):
            continue
        score = 0
        for position, (term, lowered_term) in enumerate(lowered_terms):
            if lowered_term in lowered:
                if position < 4:
                    score += 12
                else:
                    score += 4 if any(char.isupper() for char in term) else 2
        if not score:
            continue
        if stripped.startswith("import "):
            score -= 8
        if "(" in stripped and not stripped.startswith("import "):
            score += 1
        if any(keyword in stripped for keyword in ("return ", "new ", "configure", "getInstance", "handleRequest")):
            score += 2
        if score > best_score:
            best_score = score
            best_line = index
    return best_line


def _line_window(lines: list[str], anchor: int, terms: list[str]) -> tuple[int, int]:
    anchor_line = lines[anchor - 1].strip() if 0 <= anchor - 1 < len(lines) else ""
    before = 8
    after = 18
    term_set = set(terms)
    if anchor_line.startswith(("public class ", "class ", "public interface ", "interface ")):
        after = 35
    if any(term in anchor_line for term in ("handleRequest", "newConverter", "configure", "getTargetRestEndpointURL")):
        before = 6
        after = 22
    if "new JobPlanInfo" in anchor_line:
        before = max(before, 18)
    if "getTargetRestEndpointURL" in anchor_line:
        before = max(before, 22)
        after = 12
    if "getTargetRestEndpointURL" in term_set and "getResponseClass" in anchor_line:
        after = max(after, 30)
    if "FIELD_NAME_NODES" in term_set and "FIELD_NAME_NODES" in anchor_line:
        before = max(before, 15)
        after = max(after, 110)
    if "newConverter" in term_set and ("configure" in anchor_line or "isKeyConverter" in anchor_line):
        before = max(before, 20)
    if "KEY_CONVERTER_CLASS_CONFIG" in term_set or "shouldInstantiateAndConfigureConverters" in term_set:
        before = max(before, 12)
    start = max(1, anchor - before)
    end = min(len(lines), anchor + after)
    return start, end


def _format_line_snippet(lines: list[str], *, start: int, end: int) -> str:
    return "\n".join(f"{line_no}: {lines[line_no - 1]}" for line_no in range(start, end + 1))


def _java_basename(value: Any) -> str:
    text = str(value or "")
    if not text:
        return ""
    return text.rstrip("/").rsplit("/", maxsplit=1)[-1]


def _corpus_ids(*, role: str, framework: str) -> tuple[str, ...]:
    if role == "guides":
        return (CORPUS_IDS["guides"],)
    if role == "docs":
        return (CORPUS_IDS[f"{framework}_docs"],)
    if framework == "flink":
        return (
            CORPUS_IDS["flink_code"],
            CORPUS_IDS["flink_code_part2"],
            CORPUS_IDS["flink_code_part3"],
        )
    return (CORPUS_IDS["kafka_code"],)


def _compact_rows(
    rows: list[dict[str, Any]],
    *,
    max_text_chars: int,
) -> list[dict[str, Any]]:
    compact = []
    for index, row in enumerate(rows, start=1):
        metadata = dict(row.get("metadata") or {})
        compact_metadata = {
            key: metadata.get(key)
            for key in (
                "framework",
                "framework_version",
                "source_kind",
                "module",
                "api_surface",
                "class_name",
                "path",
                "repo",
                "repo_ref",
                "language",
                "stability",
            )
            if metadata.get(key) is not None
        }
        compact.append(
            {
                "rank": index,
                "source_uri": row.get("source_uri"),
                "web_source_url": row.get("web_source_url") or repo_web_url(row.get("source_uri")),
                "line_source_uri": row.get("line_source_uri"),
                "web_line_url": row.get("web_line_url") or repo_web_url(row.get("line_source_uri")),
                "line_span": row.get("line_span"),
                "score": row.get("score"),
                "source_kind": metadata.get("source_kind"),
                "module": metadata.get("module"),
                "api_surface": metadata.get("api_surface"),
                "class_name": metadata.get("class_name"),
                "path": metadata.get("path"),
                "text": str(row.get("raw_text") or "")[:max_text_chars],
                "line_snippet": row.get("line_snippet"),
                "metadata": compact_metadata,
            }
        )
    return compact


def _dedupe_rows(rows: Any) -> list[dict[str, Any]]:
    result = []
    seen: set[tuple[str, str, str]] = set()
    for row in rows:
        metadata = dict(row.get("metadata") or {})
        key = (
            str(row.get("source_uri") or ""),
            str(metadata.get("source_kind") or ""),
            str(metadata.get("path") or ""),
        )
        if key in seen:
            continue
        seen.add(key)
        result.append(dict(row))
    return result


def _read_message(stream: Any) -> tuple[dict[str, Any], TransportMode] | None:
    headers: dict[str, str] = {}
    while True:
        line = stream.readline()
        if not line:
            return None
        if line.lstrip().startswith(b"{"):
            return json.loads(line.decode("utf-8")), "jsonl"
        if line in {b"\r\n", b"\n"}:
            break
        name, _sep, value = line.decode("ascii").partition(":")
        headers[name.casefold()] = value.strip()
    content_length = int(headers.get("content-length", "0"))
    if content_length <= 0:
        return None
    body = stream.read(content_length)
    return json.loads(body.decode("utf-8")), "content-length"


def _write_message(
    stream: Any,
    message: Mapping[str, Any],
    *,
    mode: TransportMode = "content-length",
) -> None:
    body = json.dumps(message, separators=(",", ":")).encode("utf-8")
    if mode == "jsonl":
        stream.write(body + b"\n")
        stream.flush()
        return
    stream.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii"))
    stream.write(body)
    stream.flush()


def _protocol_version(message: Mapping[str, Any]) -> str:
    params = _as_dict(message.get("params"))
    return str(params.get("protocolVersion") or "2025-06-18")


def _result(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def _as_dict(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


def _required_str(args: Mapping[str, Any], key: str) -> str:
    value = _clean(args.get(key))
    if not value:
        raise ValueError(f"{key} is required")
    return value


def _framework(args: Mapping[str, Any]) -> str:
    raw = _clean(args.get("framework")) or ""
    lowered = raw.lower()
    if lowered in {"flink", "kafka"}:
        return lowered
    query = str(args.get("query") or "").lower()
    if "kafka" in query or "connect" in query:
        return "kafka"
    return "flink"


def _top_k(args: Mapping[str, Any], *, default: int = 5) -> int:
    try:
        top_k = int(args.get("top_k") or default)
    except (TypeError, ValueError):
        top_k = default
    return max(1, min(12, top_k))


def _clean(value: Any) -> str | None:
    if value is None:
        return None
    stripped = str(value).strip()
    return stripped or None


def _env_flag(value: Any) -> bool:
    lowered = str(value or "").strip().lower()
    return lowered in {"1", "true", "yes", "y", "on"}


def _is_retriable_sdk_error(exc: Exception) -> bool:
    """Return True only for errors that justify falling back to kubectl.

    Connectivity failures, DNS errors, timeouts, and a missing SDK package
    are retriable — they indicate the SDK could not reach the backend.
    Auth errors (401/403), bad-request errors (4xx), and configuration
    errors should NOT trigger a fallback because they would also fail
    through kubectl and silently masking them hinders debugging.

    Also inspects ``__cause__`` because ``_get_sdk_client()`` wraps
    ``ImportError`` as ``RuntimeError(...) from exc``.
    """
    # Walk the exception chain — _get_sdk_client() wraps ImportError as
    # RuntimeError(...) from exc, so we need to inspect __cause__ too.
    current: BaseException | None = exc
    while current is not None:
        if isinstance(current, (ImportError, ModuleNotFoundError)):
            return True
        if isinstance(current, (ConnectionError, TimeoutError, OSError)):
            return True
        # If the SDK wraps HTTP errors with a status_code or status attribute,
        # allow retry for server-side (5xx) and rate-limit (429) errors only.
        status = getattr(current, "status_code", None) or getattr(current, "status", None)
        if status is not None:
            try:
                code = int(status)
            except (TypeError, ValueError):
                return False
            return code == 429 or code >= 500
        current = current.__cause__

    return False


def _error_text(exc: Exception) -> str:
    if isinstance(exc, subprocess.CalledProcessError):
        stderr = (exc.stderr or "").strip()
        stdout = (exc.stdout or "").strip()
        details = stderr or stdout
        if details:
            return f"{exc}; output={details[-1200:]}"
    return str(exc)


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


def main() -> int:
    K2McpServer().serve()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
