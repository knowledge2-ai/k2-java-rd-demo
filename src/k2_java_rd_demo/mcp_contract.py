"""MCP-style tool contract for the Java R&D demo.

The contract is deliberately offline and SDK-free. It gives an integration layer
the tool names, argument schemas, default K2 metadata filters, and presenter
guardrails needed to route Java R&D questions through K2-backed retrieval.
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from typing import Any, Mapping

from .filters import (
    DEMO_HYBRID,
    DEMO_RETURN,
    eq,
    flink_checkpoint_docs_or_guides_filter,
    flink_docs_filter,
    flink_rest_code_filter,
    flink_rest_tests_filter,
    in_,
    kafka_connect_filter,
    ne,
    structured_filter,
)

CONTRACT_VERSION = "java-rd-demo-mcp-v1"
FLINK_FRAMEWORK_VERSION = "2.2.0"
KAFKA_FRAMEWORK_VERSION = "4.2.0"
TOOL_NAMES = (
    "k2_search_guides",
    "k2_search_docs",
    "k2_search_code",
    "k2_search_tests",
    "k2_present_answer",
)


@dataclass(frozen=True, kw_only=True)
class McpToolSpec:
    name: str
    description: str
    input_schema: Mapping[str, Any]
    default_metadata_filter: Mapping[str, Any]
    default_hybrid_config: Mapping[str, Any]
    return_config: Mapping[str, Any]
    presenter_notes: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": _copy_jsonable(self.input_schema),
            "default_metadata_filter": _copy_jsonable(self.default_metadata_filter),
            "default_hybrid_config": _copy_jsonable(self.default_hybrid_config),
            "return_config": _copy_jsonable(self.return_config),
            "presenter_notes": list(self.presenter_notes),
        }


def k2_search_guides_spec(*, include_kafka: bool = False) -> McpToolSpec:
    return McpToolSpec(
        name="k2_search_guides",
        description=(
            "Search Java R&D guide pages before looking at raw docs or source. Use this to "
            "find implementation checklists, routing rules, and test-selection guidance."
        ),
        input_schema=_search_input_schema(
            query_description="Natural-language guide search, for example REST handler checklist.",
            include_kafka=include_kafka,
        ),
        default_metadata_filter=_with_optional_kafka(
            _flink_guides_filter(),
            _kafka_docs_or_guides_filter(),
            include_kafka=include_kafka,
        ),
        default_hybrid_config=_copy_jsonable(DEMO_HYBRID),
        return_config=_copy_jsonable(DEMO_RETURN),
        presenter_notes=(
            "Use guides first to recover project conventions before source edits are discussed.",
            "Default Flink filter targets 2.2.0 guide/docs material for REST and checkpointing.",
            *_kafka_presenter_notes(include_kafka),
        ),
    )


def k2_search_docs_spec(*, include_kafka: bool = False) -> McpToolSpec:
    return McpToolSpec(
        name="k2_search_docs",
        description=(
            "Search version-specific framework documentation and release guidance. Prefer this "
            "for public API behavior, compatibility notes, and upgrade-sensitive claims."
        ),
        input_schema=_search_input_schema(
            query_description="Documentation query, for example Flink 2.2 checkpoint storage.",
            include_kafka=include_kafka,
        ),
        default_metadata_filter=_with_optional_kafka(
            _flink_docs_rest_or_checkpoint_filter(),
            _kafka_docs_filter(),
            include_kafka=include_kafka,
        ),
        default_hybrid_config=_copy_jsonable(DEMO_HYBRID),
        return_config=_copy_jsonable(DEMO_RETURN),
        presenter_notes=(
            "Flink defaults are limited to framework=flink, framework_version=2.2.0, "
            "source_kind=docs, and api_surface in [rest, checkpointing].",
            "Cite docs for public behavior before deriving implementation details from code.",
            *_kafka_presenter_notes(include_kafka),
        ),
    )


def k2_search_code_spec(*, include_kafka: bool = False) -> McpToolSpec:
    return McpToolSpec(
        name="k2_search_code",
        description=(
            "Search production source for implementation patterns after guides and docs identify "
            "the expected API behavior."
        ),
        input_schema=_search_input_schema(
            query_description="Source query, for example REST handler route registration.",
            include_kafka=include_kafka,
        ),
        default_metadata_filter=_with_optional_kafka(
            _flink_code_rest_or_checkpoint_filter(),
            _kafka_code_filter(),
            include_kafka=include_kafka,
        ),
        default_hybrid_config=_copy_jsonable(DEMO_HYBRID),
        return_config=_copy_jsonable(DEMO_RETURN),
        presenter_notes=(
            "Flink code defaults cover flink-runtime production classes for REST and "
            "checkpointing and exclude stability=test_only.",
            "Return class names, file paths, and nearby abstractions rather than copying code.",
            *_kafka_presenter_notes(include_kafka),
        ),
    )


def k2_search_tests_spec(*, include_kafka: bool = False) -> McpToolSpec:
    return McpToolSpec(
        name="k2_search_tests",
        description=(
            "Search neighboring tests and regression patterns for the same framework, module, "
            "and API surface."
        ),
        input_schema=_search_input_schema(
            query_description="Test query, for example checkpoint coordinator regression tests.",
            include_kafka=include_kafka,
        ),
        default_metadata_filter=_with_optional_kafka(
            _flink_tests_rest_or_checkpoint_filter(),
            _kafka_tests_filter(),
            include_kafka=include_kafka,
        ),
        default_hybrid_config=_copy_jsonable(DEMO_HYBRID),
        return_config=_copy_jsonable(DEMO_RETURN),
        presenter_notes=(
            "Search tests before edits and keep production code separate from test-only helpers.",
            "Flink test defaults target flink-runtime tests for REST and checkpointing.",
            *_kafka_presenter_notes(include_kafka),
        ),
    )


def k2_present_answer_spec(*, include_kafka: bool = False) -> McpToolSpec:
    """Presenter-facing answer tool.

    This is intentionally separate from the server's ``k2_answer_with_sources``
    backend tool.  The contract version (``k2_present_answer``) enforces
    citations and an implementation plan — guardrails for prompt-engineering
    that the backend does not require.  The server's tool only needs a query
    string and performs its own multi-role retrieval internally.
    """
    return McpToolSpec(
        name="k2_present_answer",
        description=(
            "Produce an answer grounded in retrieved sources. For coding requests, the caller "
            "must provide citations and a plan before edits are proposed."
        ),
        input_schema=_answer_input_schema(include_kafka=include_kafka),
        default_metadata_filter=_with_optional_kafka(
            _flink_answer_filter(),
            kafka_connect_filter(KAFKA_FRAMEWORK_VERSION),
            include_kafka=include_kafka,
        ),
        default_hybrid_config=_copy_jsonable(DEMO_HYBRID),
        return_config=_copy_jsonable(DEMO_RETURN),
        presenter_notes=(
            "Do not edit code until the answer includes cited docs, source, and test evidence.",
            "For Flink 2.2, explain whether the claim comes from REST docs, checkpointing docs, "
            "runtime code, or tests.",
            "For edit-oriented answers, include a short implementation plan before patch details.",
            *_kafka_presenter_notes(include_kafka),
        ),
    )


def mcp_tool_specs(*, include_kafka: bool = False) -> tuple[McpToolSpec, ...]:
    return (
        k2_search_guides_spec(include_kafka=include_kafka),
        k2_search_docs_spec(include_kafka=include_kafka),
        k2_search_code_spec(include_kafka=include_kafka),
        k2_search_tests_spec(include_kafka=include_kafka),
        k2_present_answer_spec(include_kafka=include_kafka),
    )


def build_mcp_tool_contract(include_kafka: bool = False) -> dict[str, Any]:
    frameworks = {
        "flink": {
            "default_version": FLINK_FRAMEWORK_VERSION,
            "api_surfaces": ["rest", "checkpointing"],
            "filter_summary": (
                "Flink filters pin framework=flink and framework_version=2.2.0, then "
                "separate guides/docs, production code, and tests with source_kind plus "
                "api_surface in [rest, checkpointing]."
            ),
        }
    }
    if include_kafka:
        frameworks["kafka"] = {
            "default_version": KAFKA_FRAMEWORK_VERSION,
            "api_surfaces": ["connect"],
            "filter_summary": (
                "Kafka filters pin framework=kafka, framework_version=4.2.0, "
                "api_surface=connect, and source_kind in [docs, code, test]."
            ),
        }

    return {
        "contract_version": CONTRACT_VERSION,
        "style": "mcp_tool_contract",
        "frameworks": frameworks,
        "tools": [spec.to_dict() for spec in mcp_tool_specs(include_kafka=include_kafka)],
    }


def mcp_tool_contract_json(*, include_kafka: bool = False, indent: int | None = 2) -> str:
    return json.dumps(
        build_mcp_tool_contract(include_kafka=include_kafka),
        indent=indent,
        sort_keys=True,
    )


def _search_input_schema(*, query_description: str, include_kafka: bool) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["query"],
        "properties": {
            "query": {
                "type": "string",
                "minLength": 1,
                "description": query_description,
            },
            **_routing_properties(include_kafka),
            "top_k": {
                "type": "integer",
                "minimum": 1,
                "maximum": 50,
                "default": 12,
                "description": "Maximum K2 retrieval results to return.",
            },
            "metadata_filter": _metadata_filter_property(),
            "hybrid_config": _config_override_property("hybrid retrieval config"),
            "return_config": _config_override_property("return config"),
        },
    }


def _answer_input_schema(*, include_kafka: bool) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["question", "citations", "plan_before_edits"],
        "properties": {
            "question": {
                "type": "string",
                "minLength": 1,
                "description": "Question to answer from retrieved K2 sources.",
            },
            **_routing_properties(include_kafka),
            "citations": {
                "type": "array",
                "minItems": 1,
                "description": (
                    "Source evidence required before answering. Include at least one cited "
                    "source URI; coding answers should include docs, source, and tests."
                ),
                "items": {
                    "type": "object",
                    "additionalProperties": True,
                    "required": ["source_uri"],
                    "properties": {
                        "source_uri": {"type": "string", "minLength": 1},
                        "source_kind": {"type": "string"},
                        "summary": {"type": "string"},
                    },
                },
            },
            "plan_before_edits": {
                "type": "array",
                "minItems": 1,
                "description": (
                    "Implementation or verification plan that must be stated before code edits "
                    "for edit-oriented requests."
                ),
                "items": {"type": "string", "minLength": 1},
            },
            "metadata_filter": _metadata_filter_property(),
            "return_config": _config_override_property("return config"),
        },
    }


def _routing_properties(include_kafka: bool) -> dict[str, Any]:
    frameworks = ["flink", "kafka"] if include_kafka else ["flink"]
    framework_versions = [FLINK_FRAMEWORK_VERSION, KAFKA_FRAMEWORK_VERSION]
    api_surfaces = (
        ["rest", "checkpointing", "connect"] if include_kafka else ["rest", "checkpointing"]
    )
    version_description = "Flink defaults to 2.2.0."
    surface_description = "Flink surfaces are rest and checkpointing."
    if include_kafka:
        version_description += " Kafka Connect uses 4.2.0 when framework=kafka."
        surface_description += " Kafka 4.2 uses api_surface=connect."

    return {
        "framework": {
            "type": "string",
            "enum": frameworks,
            "default": "flink",
            "description": "Framework to search.",
        },
        "framework_version": {
            "type": "string",
            "enum": framework_versions if include_kafka else [FLINK_FRAMEWORK_VERSION],
            "default": FLINK_FRAMEWORK_VERSION,
            "description": version_description,
        },
        "api_surface": {
            "type": "string",
            "enum": api_surfaces,
            "default": "rest",
            "description": surface_description,
        },
    }


def _metadata_filter_property() -> dict[str, Any]:
    return {
        "type": "object",
        "description": (
            "Optional override for default_metadata_filter. Use the structured K2 filter shape "
            "{condition: 'and'|'or', filters: [...]} with leaf filters containing key/op/value."
        ),
    }


def _config_override_property(label: str) -> dict[str, Any]:
    return {
        "type": "object",
        "description": f"Optional override for the default {label}.",
    }


def _flink_guides_filter() -> dict[str, Any]:
    return flink_checkpoint_docs_or_guides_filter(FLINK_FRAMEWORK_VERSION)


def _flink_docs_rest_or_checkpoint_filter() -> dict[str, Any]:
    return structured_filter(
        [
            flink_docs_filter(FLINK_FRAMEWORK_VERSION),
            in_("api_surface", ["rest", "checkpointing"]),
        ]
    )


def _flink_code_rest_or_checkpoint_filter() -> dict[str, Any]:
    return _filter_union(
        flink_rest_code_filter(FLINK_FRAMEWORK_VERSION),
        structured_filter(
            [
                eq("framework", "flink"),
                eq("framework_version", FLINK_FRAMEWORK_VERSION),
                eq("source_kind", "code"),
                eq("module", "flink-runtime"),
                eq("api_surface", "checkpointing"),
                ne("stability", "test_only"),
            ]
        ),
    )


def _flink_tests_rest_or_checkpoint_filter() -> dict[str, Any]:
    return _filter_union(
        flink_rest_tests_filter(FLINK_FRAMEWORK_VERSION),
        structured_filter(
            [
                eq("framework", "flink"),
                eq("framework_version", FLINK_FRAMEWORK_VERSION),
                eq("source_kind", "test"),
                eq("module", "flink-runtime"),
                eq("api_surface", "checkpointing"),
            ]
        ),
    )


def _flink_answer_filter() -> dict[str, Any]:
    return _filter_union(
        _flink_guides_filter(),
        _flink_docs_rest_or_checkpoint_filter(),
        _flink_code_rest_or_checkpoint_filter(),
        _flink_tests_rest_or_checkpoint_filter(),
    )


def _kafka_docs_or_guides_filter() -> dict[str, Any]:
    return structured_filter(
        [
            kafka_connect_filter(KAFKA_FRAMEWORK_VERSION),
            in_("source_kind", ["docs", "guide"]),
        ]
    )


def _kafka_docs_filter() -> dict[str, Any]:
    return structured_filter(
        [
            kafka_connect_filter(KAFKA_FRAMEWORK_VERSION),
            eq("source_kind", "docs"),
        ]
    )


def _kafka_code_filter() -> dict[str, Any]:
    return structured_filter(
        [
            kafka_connect_filter(KAFKA_FRAMEWORK_VERSION),
            eq("source_kind", "code"),
        ]
    )


def _kafka_tests_filter() -> dict[str, Any]:
    return structured_filter(
        [
            kafka_connect_filter(KAFKA_FRAMEWORK_VERSION),
            eq("source_kind", "test"),
        ]
    )


def _with_optional_kafka(
    flink_filter: Mapping[str, Any],
    kafka_filter: Mapping[str, Any],
    *,
    include_kafka: bool,
) -> dict[str, Any]:
    if not include_kafka:
        return _copy_jsonable(flink_filter)
    return _filter_union(flink_filter, kafka_filter)


def _filter_union(*filters: Mapping[str, Any]) -> dict[str, Any]:
    selected = [_copy_jsonable(filter_spec) for filter_spec in filters]
    if len(selected) == 1:
        return selected[0]
    return structured_filter(selected, condition="or")


def _kafka_presenter_notes(include_kafka: bool) -> tuple[str, ...]:
    if not include_kafka:
        return ()
    return (
        "When framework=kafka, use framework_version=4.2.0 and api_surface=connect.",
        "Kafka Connect filters use source_kind in [docs, code, test] unless a tool narrows it.",
    )


def _copy_jsonable(value: Any) -> Any:
    return copy.deepcopy(value)


# ---------------------------------------------------------------------------
# Schema parity validation
# ---------------------------------------------------------------------------

# Search tools are expected to share these core properties between
# the offline contract and the live MCP server.  The answer tool is
# intentionally split: the contract defines a presenter-facing schema
# with required citations/plan, while the server exposes a simpler
# backend query interface.

SEARCH_TOOL_NAMES = frozenset({
    "k2_search_guides",
    "k2_search_docs",
    "k2_search_code",
    "k2_search_tests",
})


def validate_contract_server_parity(
    contract_tools: list[dict[str, Any]],
    server_tools: list[dict[str, Any]],
) -> list[str]:
    """Compare contract and server tool schemas, returning a list of issues.

    Only search tools (not the answer tool) are checked for property-level
    parity.  Returns an empty list when everything matches.
    """
    issues: list[str] = []

    contract_by_name = {tool["name"]: tool for tool in contract_tools}
    server_by_name = {tool["name"]: tool for tool in server_tools}

    # Every search tool in the server should appear in the contract
    for name in SEARCH_TOOL_NAMES:
        if name not in server_by_name:
            issues.append(f"search tool {name!r} missing from server")
        if name not in contract_by_name:
            issues.append(f"search tool {name!r} missing from contract")

    # For shared search tools, verify required fields are compatible
    for name in SEARCH_TOOL_NAMES & set(server_by_name) & set(contract_by_name):
        # Contract uses snake_case "input_schema"; MCP server uses camelCase "inputSchema"
        contract_schema = contract_by_name[name].get("input_schema", {})
        server_schema = server_by_name[name].get("inputSchema", {})

        server_required = set(server_schema.get("required", []))
        contract_required = set(contract_schema.get("required", []))
        if not server_required.issubset(contract_required):
            missing = server_required - contract_required
            issues.append(
                f"{name}: server requires {missing} not in contract required fields"
            )

        # Verify shared properties have compatible types
        server_props = server_schema.get("properties", {})
        contract_props = contract_schema.get("properties", {})
        for prop_name in set(server_props) & set(contract_props):
            server_type = server_props[prop_name].get("type")
            contract_type = contract_props[prop_name].get("type")
            if server_type and contract_type and server_type != contract_type:
                issues.append(
                    f"{name}.{prop_name}: type mismatch "
                    f"(server={server_type}, contract={contract_type})"
                )

    return issues


__all__ = [
    "CONTRACT_VERSION",
    "FLINK_FRAMEWORK_VERSION",
    "KAFKA_FRAMEWORK_VERSION",
    "McpToolSpec",
    "SEARCH_TOOL_NAMES",
    "TOOL_NAMES",
    "build_mcp_tool_contract",
    "k2_present_answer_spec",
    "k2_search_code_spec",
    "k2_search_docs_spec",
    "k2_search_guides_spec",
    "k2_search_tests_spec",
    "mcp_tool_contract_json",
    "mcp_tool_specs",
    "validate_contract_server_parity",
]
