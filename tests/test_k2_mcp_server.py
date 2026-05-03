from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tests import _paths  # noqa: F401

from k2_java_rd_demo.k2_mcp_server import (
    K2McpConfig,
    K2McpServer,
    _answer_queries,
    _enrich_rows_with_local_sources,
    _hybrid_for_source_kind,
    _is_retriable_sdk_error,
    _normalize_target_rows,
    _preferred_anchor_terms,
    tool_specs,
)
from k2_java_rd_demo.source_links import repo_web_url


class K2McpServerTests(unittest.TestCase):
    def test_repo_uri_maps_to_clickable_github_url(self) -> None:
        self.assertEqual(
            repo_web_url("repo://apache/flink@release-2.2.0/Foo.java#L10-L20"),
            (
                "https://github.com/apache/flink/blob/"
                "5a336892424a9458653ead89610bf60d771ab8d7/Foo.java#L10-L20"
            ),
        )
        self.assertEqual(
            repo_web_url("repo://apache/kafka@4.2/connect/runtime/Foo.java"),
            (
                "https://github.com/apache/kafka/blob/"
                "ba74c3a289456f7346f2bece2cf76fcae55be9a4/connect/runtime/Foo.java"
            ),
        )

    def test_answer_queries_do_not_inject_oracle_class_names(self) -> None:
        query = "How do I add a Flink REST handler?"
        generated = _answer_queries(framework="flink", api_surface="rest", query=query)
        text = json.dumps(generated)

        self.assertIn(query, text)
        for leaked_name in (
            "DispatcherRestEndpoint",
            "JobDetailsHandler",
            "CheckpointCoordinator",
            "ConnectorPluginsResource",
            "AbstractHerder",
            "ConfigDef",
        ):
            self.assertNotIn(leaked_name, text)

    def test_initialize_and_tool_list(self) -> None:
        server = K2McpServer(K2McpConfig())

        init = server.handle(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {"protocolVersion": "2025-06-18"},
            }
        )
        listed = server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        resources = server.handle({"jsonrpc": "2.0", "id": 4, "method": "resources/list"})

        self.assertEqual(init["result"]["serverInfo"]["name"], "k2-java-rd-demo")
        self.assertEqual(resources["result"]["resources"], [])
        tool_names = [tool["name"] for tool in listed["result"]["tools"]]
        self.assertIn("k2_answer_with_sources", tool_names)
        json.dumps(tool_specs())

    def test_disable_guides_removes_guide_tool_and_answer_search(self) -> None:
        server = K2McpServer(K2McpConfig(disable_guides=True))
        calls = []

        def fake_search(**kwargs):  # type: ignore[no-untyped-def]
            calls.append(kwargs)
            return {"results": []}

        server._retrieval_search = fake_search  # type: ignore[method-assign]
        listed = server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        tool_names = [tool["name"] for tool in listed["result"]["tools"]]

        self.assertNotIn("k2_search_guides", tool_names)
        self.assertNotIn("k2_search_guides", server.tools)

        response = server.handle(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "k2_answer_with_sources",
                    "arguments": {
                        "query": "rest handler",
                        "framework": "flink",
                        "api_surface": "rest",
                    },
                },
            }
        )

        self.assertFalse(response["result"]["isError"])
        self.assertTrue(calls)
        payload = json.loads(response["result"]["content"][0]["text"])
        self.assertNotIn("guides", {search["name"] for search in payload["searches"]})
        self.assertNotIn("guide", {search["source_kind"] for search in payload["searches"]})

    def test_tool_call_returns_mcp_content_and_logs(self) -> None:
        server = K2McpServer(K2McpConfig(case_id="case-1"))
        server._retrieval_search = lambda **_kwargs: {  # type: ignore[method-assign]
            "results": [
                {
                    "source_uri": "repo://apache/flink@release-2.2.0/Foo.java",
                    "raw_text": "class Foo extends AbstractRestHandler",
                    "metadata": {
                        "framework": "flink",
                        "framework_version": "2.2.0",
                        "source_kind": "code",
                        "module": "flink-runtime",
                        "api_surface": "rest",
                        "class_name": "Foo",
                    },
                    "score": 0.9,
                }
            ]
        }

        response = server.handle(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "k2_search_code",
                    "arguments": {
                        "query": "rest handler",
                        "framework": "flink",
                        "api_surface": "rest",
                    },
                },
            }
        )

        self.assertFalse(response["result"]["isError"])
        text = response["result"]["content"][0]["text"]
        payload = json.loads(text)
        self.assertEqual(payload["source_kind"], "code")
        self.assertEqual(payload["results"][0]["class_name"], "Foo")
        self.assertEqual(payload["results"][0]["metadata"]["source_kind"], "code")

    def test_sdk_backend_calls_public_search_api(self) -> None:
        server = K2McpServer(K2McpConfig(api_key="test-key"))
        fake = FakeSdkClient()
        server._sdk_client = fake

        response = server._retrieval_search(
            corpus_id="corpus-1",
            query="rest handler",
            top_k=3,
            filters={"condition": "and", "filters": []},
            hybrid={"enabled": True},
        )

        self.assertEqual(response["backend"], "sdk")
        self.assertEqual(response["results"][0]["text"], "SDK text")
        self.assertEqual(fake.calls[0]["corpus_id"], "corpus-1")
        self.assertEqual(fake.calls[0]["return_config"]["include_provenance"], True)

    def test_missing_api_key_rejected_for_sdk_backend(self) -> None:
        server = K2McpServer(K2McpConfig())

        with self.assertRaisesRegex(RuntimeError, "K2_API_KEY"):
            server._retrieval_search(
                corpus_id="corpus-1",
                query="rest handler",
                top_k=3,
                filters={},
                hybrid={},
            )

    def test_config_parses_metadata_filter_disable_flag(self) -> None:
        config = K2McpConfig.from_env(
            {
                "K2_MCP_DISABLE_METADATA_FILTERS": "true",
                "K2_MCP_RETRIEVAL_PROFILE": "metadata_exact",
                "K2_MCP_SOURCE_BASE": "/tmp/sources",
            }
        )

        self.assertTrue(config.disable_metadata_filters)
        self.assertEqual(config.retrieval_profile, "metadata_exact")
        self.assertEqual(config.source_base, "/tmp/sources")

    def test_hybrid_profiles_tune_code_weights(self) -> None:
        exact = _hybrid_for_source_kind("code", "java_exact")
        metadata_exact = _hybrid_for_source_kind("code", "metadata_exact")
        docs = _hybrid_for_source_kind("docs", "java_exact")

        self.assertEqual(exact["dense_weight"], 0.0)
        self.assertGreater(exact["sparse_weight"], metadata_exact["sparse_weight"])
        self.assertGreater(metadata_exact["metadata_sparse_weight"], exact["metadata_sparse_weight"])
        self.assertGreater(docs["dense_weight"], docs["sparse_weight"])

    def test_converter_preferred_terms_avoid_broad_side_tests(self) -> None:
        terms = _preferred_anchor_terms("Kafka Connect Converter key value split", ("Converter",))

        self.assertIn("PluginsTest", terms)
        self.assertIn("WorkerConfigTest", terms)
        self.assertNotIn("MultiVersionTest", terms)
        self.assertNotIn("AbstractWorkerSourceTaskTest", terms)

    def test_search_role_can_disable_metadata_filters_for_ablation(self) -> None:
        server = K2McpServer(K2McpConfig(disable_metadata_filters=True))
        calls = []

        def fake_retrieval(**kwargs):
            calls.append(kwargs)
            return {"results": []}

        server._retrieval_search = fake_retrieval  # type: ignore[method-assign]

        payload = server._search_role(
            {
                "query": "rest handler",
                "framework": "flink",
                "api_surface": "rest",
                "class_name": "Foo",
            },
            role="code",
            source_kind="code",
        )

        self.assertEqual(payload["metadata_filter_mode"], "disabled")
        self.assertEqual(payload["filters"], {})
        self.assertTrue(calls)
        self.assertTrue(all(call["filters"] == {} for call in calls))

    def test_search_role_keeps_metadata_filters_enabled_by_default(self) -> None:
        server = K2McpServer(K2McpConfig())
        calls = []

        def fake_retrieval(**kwargs):
            calls.append(kwargs)
            return {"results": []}

        server._retrieval_search = fake_retrieval  # type: ignore[method-assign]

        payload = server._search_role(
            {"query": "rest handler", "framework": "flink", "api_surface": "rest"},
            role="code",
            source_kind="code",
        )

        self.assertEqual(payload["metadata_filter_mode"], "enabled")
        self.assertIn("filters", payload["filters"])
        self.assertTrue(calls)
        self.assertTrue(all(call["filters"] for call in calls))

    def test_answer_tool_runs_dynamic_target_class_lookups(self) -> None:
        server = K2McpServer(K2McpConfig(case_id="case-1"))
        calls = []

        def fake_retrieval(**kwargs):
            calls.append(kwargs)
            filters = json.dumps(kwargs["filters"])
            source_kind = "test" if "FooTest" in filters else "code"
            class_name = "FooTest" if source_kind == "test" else "Foo"
            suffix = "FooTest.java" if source_kind == "test" else "Foo.java"
            return {
                "results": [
                    {
                        "source_uri": f"repo://apache/flink@release-2.2.0/{suffix}",
                        "raw_text": f"class {class_name}",
                        "metadata": {
                            "framework": "flink",
                            "framework_version": "2.2.0",
                            "source_kind": source_kind,
                            "module": "flink-runtime",
                            "api_surface": "rest",
                            "class_name": class_name,
                            "path": suffix,
                        },
                        "score": 1.0,
                    }
                ]
            }

        server._retrieval_search = fake_retrieval  # type: ignore[method-assign]

        payload = server._answer_with_sources(
            {
                "query": "For Flink 2.2.0, inspect Foo.",
                "framework": "flink",
                "api_surface": "rest",
                "target_class_names": ["Foo"],
                "top_k": 2,
            }
        )

        filter_text = "\n".join(json.dumps(call["filters"]) for call in calls)
        self.assertIn('"key": "class_name"', filter_text)
        self.assertIn('"value": "Foo"', filter_text)
        self.assertIn('"value": "FooTest"', filter_text)
        self.assertIn('"op": "text_match"', filter_text)
        self.assertIn('"value": "Foo.java"', filter_text)
        self.assertIn('"value": "FooTest.java"', filter_text)
        self.assertEqual(payload["target_class_names"], ("Foo",))
        self.assertEqual(
            payload["answer_style"]["section_contract"]["Recommendation"].split()[0],
            "Exactly",
        )
        self.assertIn("self-verifying", payload["tool_guidance"])
        self.assertIn("omit broader related evidence", payload["tool_guidance"])
        self.assertIn("local rg/file-read", payload["tool_guidance"])
        preferred_uris = {source["source_uri"] for source in payload["preferred_sources"]}
        self.assertIn("repo://apache/flink@release-2.2.0/Foo.java", preferred_uris)
        self.assertIn("repo://apache/flink@release-2.2.0/FooTest.java", preferred_uris)
        preferred_urls = {source["web_source_url"] for source in payload["preferred_sources"]}
        self.assertIn(
            "https://github.com/apache/flink/blob/"
            "5a336892424a9458653ead89610bf60d771ab8d7/Foo.java",
            preferred_urls,
        )
        target_uris = {target["source_uri"] for target in payload["citation_targets"]}
        self.assertIn("repo://apache/flink@release-2.2.0/Foo.java", target_uris)
        self.assertIn("repo://apache/flink@release-2.2.0/FooTest.java", target_uris)
        target_urls = {target["web_source_url"] for target in payload["citation_targets"]}
        self.assertIn(
            "https://github.com/apache/flink/blob/"
            "5a336892424a9458653ead89610bf60d771ab8d7/Foo.java",
            target_urls,
        )

    def test_local_source_enrichment_adds_line_snippets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            source_base = Path(tmp)
            source_file = (
                source_base
                / "apache-flink-release-2.2.0"
                / "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/FooHandler.java"
            )
            source_file.parent.mkdir(parents=True)
            source_file.write_text(
                "\n".join(
                    [
                        "package org.apache.flink.runtime.rest.handler.job;",
                        "public class FooHandler {",
                        "    protected JobPlanInfo handleRequest(HandlerRequest request, AccessExecutionGraph graph) {",
                        "        return new JobPlanInfo(graph.getPlan());",
                        "    }",
                        "}",
                    ]
                ),
                encoding="utf-8",
            )
            rows = [
                {
                    "source_uri": (
                        "repo://apache/flink@release-2.2.0/"
                        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/FooHandler.java"
                    ),
                    "raw_text": "public class FooHandler",
                    "metadata": {
                        "framework": "flink",
                        "source_kind": "code",
                        "class_name": "FooHandler",
                        "path": "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/FooHandler.java",
                    },
                }
            ]

            enriched = _enrich_rows_with_local_sources(
                rows,
                query="For Flink REST API 2.2.0, inspect FooHandler.",
                target_class_names=("FooHandler",),
                source_base=str(source_base),
            )

        self.assertIn("#L", enriched[0]["line_source_uri"])
        self.assertIn("#L", enriched[0]["web_line_url"])
        self.assertIn("github.com/apache/flink/blob/", enriched[0]["web_line_url"])
        self.assertIn("handleRequest", enriched[0]["line_snippet"])
        self.assertIn("getPlan", enriched[0]["line_snippet"])

    def test_normalize_target_rows_corrects_class_name_from_path(self) -> None:
        rows = [
            {
                "source_uri": "repo://apache/kafka@4.2/connect/runtime/StandaloneHerder.java",
                "metadata": {
                    "source_kind": "code",
                    "class_name": "incorrect",
                    "path": "connect/runtime/src/main/java/StandaloneHerder.java",
                },
            },
            {
                "source_uri": "repo://apache/kafka@4.2/connect/runtime/Other.java",
                "metadata": {"source_kind": "code", "class_name": "Other", "path": "Other.java"},
            },
            {
                "source_uri": "repo://apache/kafka@4.2/connect/runtime/LongConverter.java",
                "metadata": {
                    "source_kind": "code",
                    "class_name": "LongConverter",
                    "path": "connect/runtime/src/main/java/LongConverter.java",
                },
            },
        ]

        normalized = _normalize_target_rows(
            rows,
            ("StandaloneHerder", "Converter"),
            api_surface="connect",
        )

        self.assertEqual(normalized[0]["metadata"]["class_name"], "StandaloneHerder")
        self.assertEqual(normalized[0]["metadata"]["api_surface"], "connect")
        self.assertEqual(normalized[0]["class_name"], "StandaloneHerder")
        self.assertEqual(normalized[1]["metadata"]["class_name"], "Other")
        self.assertEqual(normalized[2]["metadata"]["class_name"], "LongConverter")


    def test_is_retriable_for_direct_import_error(self) -> None:
        self.assertTrue(_is_retriable_sdk_error(ImportError("no sdk")))

    def test_is_retriable_for_wrapped_import_error(self) -> None:
        """_get_sdk_client() wraps ImportError as RuntimeError(...) from exc."""
        cause = ModuleNotFoundError("No module named 'sdk'")
        wrapped = RuntimeError("SDK not installed")
        wrapped.__cause__ = cause
        self.assertTrue(_is_retriable_sdk_error(wrapped))

    def test_is_retriable_for_connection_error(self) -> None:
        self.assertTrue(_is_retriable_sdk_error(ConnectionError("refused")))

    def test_is_retriable_for_timeout(self) -> None:
        self.assertTrue(_is_retriable_sdk_error(TimeoutError("timed out")))

    def test_is_not_retriable_for_value_error(self) -> None:
        self.assertFalse(_is_retriable_sdk_error(ValueError("bad input")))

    def test_is_not_retriable_for_auth_status(self) -> None:
        exc = RuntimeError("forbidden")
        exc.status_code = 403  # type: ignore[attr-defined]
        self.assertFalse(_is_retriable_sdk_error(exc))

    def test_is_retriable_for_server_error_status(self) -> None:
        exc = RuntimeError("internal")
        exc.status_code = 502  # type: ignore[attr-defined]
        self.assertTrue(_is_retriable_sdk_error(exc))

    def test_is_retriable_for_rate_limit_status(self) -> None:
        exc = RuntimeError("rate limited")
        exc.status_code = 429  # type: ignore[attr-defined]
        self.assertTrue(_is_retriable_sdk_error(exc))

    def test_auto_backend_falls_back_when_sdk_missing(self) -> None:
        """backend=auto with SDK not installed should fall back to kubectl."""
        server = K2McpServer(K2McpConfig(
            backend="auto", api_key="test-key", deployment="test-deploy",
        ))

        # Simulate _get_sdk_client raising the same way it does when SDK is missing
        def fake_get_sdk_client():
            try:
                raise ModuleNotFoundError("No module named 'sdk'")
            except ModuleNotFoundError as exc:
                raise RuntimeError("SDK not installed") from exc

        server._get_sdk_client = fake_get_sdk_client  # type: ignore[method-assign]

        kubectl_called = []
        def fake_kubectl(payload):
            kubectl_called.append(payload)
            return {"backend": "kubectl", "results": []}

        server._retrieval_search_kubectl = fake_kubectl  # type: ignore[method-assign]

        result = server._retrieval_search(
            corpus_id="c", query="test", top_k=3, filters={}, hybrid={},
        )

        self.assertEqual(result["backend"], "kubectl")
        self.assertEqual(len(kubectl_called), 1)
        self.assertIn("sdk_error", result)


class FakeSdkClient:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def search(self, corpus_id: str, query: str, **kwargs):
        self.calls.append({"corpus_id": corpus_id, "query": query, **kwargs})
        return {
            "results": [
                {
                    "chunk_id": "chunk-1",
                    "score": 0.7,
                    "text": "SDK text",
                    "custom_metadata": {"source_kind": "docs"},
                    "system_metadata": {"source_uri": "sdk://source"},
                }
            ],
            "meta": {"cold_start": {"likely": False}},
        }


if __name__ == "__main__":
    unittest.main()
