from __future__ import annotations

import json
import unittest
from typing import Any

from tests import _paths  # noqa: F401

from k2_java_rd_demo.filters import DEMO_HYBRID, DEMO_RETURN
from k2_java_rd_demo.k2_mcp_server import tool_specs as server_tool_specs
from k2_java_rd_demo.mcp_contract import (
    FLINK_FRAMEWORK_VERSION,
    KAFKA_FRAMEWORK_VERSION,
    SEARCH_TOOL_NAMES,
    TOOL_NAMES,
    build_mcp_tool_contract,
    mcp_tool_contract_json,
    validate_contract_server_parity,
)


class McpContractTests(unittest.TestCase):
    def test_default_contract_is_flink_only(self) -> None:
        contract = build_mcp_tool_contract()

        self.assertEqual(set(contract["frameworks"]), {"flink"})
        self.assertEqual(
            contract["frameworks"]["flink"]["default_version"],
            FLINK_FRAMEWORK_VERSION,
        )
        self.assertEqual([tool["name"] for tool in contract["tools"]], list(TOOL_NAMES))
        for tool in contract["tools"]:
            schema = tool["input_schema"]
            self.assertEqual(schema["properties"]["framework"]["enum"], ["flink"])
            self.assertEqual(schema["properties"]["framework_version"]["enum"], ["2.2.0"])
            self.assertNotIn("kafka", json.dumps(tool).lower())

    def test_kafka_can_be_included_in_schema_and_filters(self) -> None:
        contract = build_mcp_tool_contract(include_kafka=True)

        self.assertEqual(
            contract["frameworks"]["kafka"]["default_version"],
            KAFKA_FRAMEWORK_VERSION,
        )
        self.assertEqual(set(contract["frameworks"]["kafka"]["api_surfaces"]), {"connect"})
        for tool in contract["tools"]:
            schema = tool["input_schema"]
            self.assertEqual(schema["properties"]["framework"]["enum"], ["flink", "kafka"])
            self.assertIn("connect", schema["properties"]["api_surface"]["enum"])
            self.assertIn("kafka", json.dumps(tool["default_metadata_filter"]))
            self.assertIn("4.2.0", json.dumps(tool["default_metadata_filter"]))

    def test_filter_shapes_use_condition_and_filters(self) -> None:
        contract = build_mcp_tool_contract(include_kafka=True)

        for tool in contract["tools"]:
            with self.subTest(tool=tool["name"]):
                self.assert_filter_group(tool["default_metadata_filter"])
                self.assertTrue(
                    self.find_leaf(tool["default_metadata_filter"], "framework", "flink")
                )

    def test_specs_are_json_serializable(self) -> None:
        contract = build_mcp_tool_contract(include_kafka=True)

        encoded = json.dumps(contract, sort_keys=True)
        self.assertEqual(json.loads(encoded), contract)
        self.assertEqual(json.loads(mcp_tool_contract_json(include_kafka=True)), contract)

        for tool in contract["tools"]:
            self.assertEqual(tool["default_hybrid_config"], DEMO_HYBRID)
            self.assertEqual(tool["return_config"], DEMO_RETURN)

    def test_answer_tool_requires_citations_and_plan_before_edits(self) -> None:
        contract = build_mcp_tool_contract()
        answer_tool = next(
            tool for tool in contract["tools"] if tool["name"] == "k2_present_answer"
        )
        schema = answer_tool["input_schema"]

        self.assertIn("citations", schema["required"])
        self.assertIn("plan_before_edits", schema["required"])
        self.assertGreaterEqual(schema["properties"]["citations"]["minItems"], 1)
        self.assertGreaterEqual(schema["properties"]["plan_before_edits"]["minItems"], 1)
        self.assertIn("source_uri", schema["properties"]["citations"]["items"]["required"])
        self.assertIn("Do not edit code", "\n".join(answer_tool["presenter_notes"]))

    def assert_filter_group(self, filter_spec: dict[str, Any]) -> None:
        self.assertIn(filter_spec["condition"], {"and", "or"})
        self.assertIsInstance(filter_spec["filters"], list)
        self.assertTrue(filter_spec["filters"])
        for child in filter_spec["filters"]:
            if "condition" in child:
                self.assert_filter_group(child)
            else:
                self.assertIn("key", child)
                self.assertIn("op", child)
                self.assertIn("value", child)

    def find_leaf(self, filter_spec: dict[str, Any], key: str, value: Any) -> bool:
        for child in filter_spec["filters"]:
            if "condition" in child and self.find_leaf(child, key, value):
                return True
            if child.get("key") == key and child.get("value") == value:
                return True
        return False


    def test_search_tool_schema_parity_with_server(self) -> None:
        contract = build_mcp_tool_contract(include_kafka=True)
        contract_tools = contract["tools"]
        server_tools = server_tool_specs()

        issues = validate_contract_server_parity(contract_tools, server_tools)
        self.assertEqual(issues, [], f"parity issues found: {issues}")

    def test_all_search_tools_present_in_both(self) -> None:
        contract = build_mcp_tool_contract(include_kafka=True)
        contract_names = {tool["name"] for tool in contract["tools"]}
        server_names = {tool["name"] for tool in server_tool_specs()}

        for name in SEARCH_TOOL_NAMES:
            self.assertIn(name, contract_names, f"search tool {name} missing from contract")
            self.assertIn(name, server_names, f"search tool {name} missing from server")

    def test_parity_detects_type_mismatch(self) -> None:
        contract_tools = [
            {
                "name": "k2_search_docs",
                "input_schema": {
                    "required": ["query"],
                    "properties": {"query": {"type": "integer"}},
                },
            },
        ]
        server_tools = [
            {
                "name": "k2_search_docs",
                "inputSchema": {
                    "required": ["query"],
                    "properties": {"query": {"type": "string"}},
                },
            },
        ]
        issues = validate_contract_server_parity(contract_tools, server_tools)
        self.assertTrue(any("type mismatch" in issue for issue in issues))

    def test_parity_detects_missing_search_tool(self) -> None:
        contract_tools = [
            {"name": "k2_search_docs", "input_schema": {"required": ["query"], "properties": {}}},
        ]
        server_tools: list[dict[str, Any]] = []
        issues = validate_contract_server_parity(contract_tools, server_tools)
        self.assertTrue(any("missing from server" in issue for issue in issues))

    def test_answer_tool_intentional_schema_split(self) -> None:
        """The contract and server intentionally define separate answer tools.

        The contract exposes ``k2_present_answer`` — a presenter-facing tool
        that enforces citations and an implementation plan.  The server exposes
        ``k2_answer_with_sources`` — a backend tool that only requires a query
        and performs its own multi-role retrieval internally.  They are distinct
        tools with different names and different schemas by design.
        """
        contract = build_mcp_tool_contract()
        contract_names = {tool["name"] for tool in contract["tools"]}
        server_names = {tool["name"] for tool in server_tool_specs()}

        # Contract has the presenter tool, not the server's backend tool
        self.assertIn("k2_present_answer", contract_names)
        self.assertNotIn("k2_answer_with_sources", contract_names)

        # Server has the backend tool, not the contract's presenter tool
        self.assertIn("k2_answer_with_sources", server_names)
        self.assertNotIn("k2_present_answer", server_names)

        # Verify their schemas are intentionally different
        contract_answer = next(
            tool for tool in contract["tools"] if tool["name"] == "k2_present_answer"
        )
        server_answer = next(
            tool for tool in server_tool_specs() if tool["name"] == "k2_answer_with_sources"
        )

        contract_required = set(contract_answer["input_schema"]["required"])
        server_required = set(server_answer["inputSchema"]["required"])
        self.assertIn("citations", contract_required)
        self.assertIn("plan_before_edits", contract_required)
        self.assertEqual(server_required, {"query"})


if __name__ == "__main__":
    unittest.main()
