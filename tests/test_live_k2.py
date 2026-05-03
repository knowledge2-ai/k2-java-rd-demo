from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any

from tests import _paths  # noqa: F401

from k2_java_rd_demo.assets import generate_seed_guides, write_jsonl
from k2_java_rd_demo.filters import DEMO_HYBRID, DEMO_RETURN, flink_rest_code_filter
from k2_java_rd_demo.live_k2 import (
    CorpusDefinition,
    LiveK2Config,
    LiveK2ConfigError,
    ReadinessProbe,
    ensure_live_project_and_corpora,
    load_jsonl_documents_by_role,
    orchestrate_live_k2,
    run_readiness_probes,
    sync_corpus_indexes,
    upload_documents_by_role,
)


class FakeK2Client:
    def __init__(self, *, search_results: dict[str, list[dict[str, Any]]] | None = None) -> None:
        self.calls: list[tuple[str, tuple[Any, ...], dict[str, Any]]] = []
        self.search_results = search_results or {}

    def create_project(self, name: str, **kwargs: Any) -> dict[str, Any]:
        self.calls.append(("create_project", (name,), kwargs))
        return {"id": "project-1", "name": name}

    def create_corpus(
        self,
        project_id: str,
        name: str,
        *,
        description: str | None = None,
    ) -> dict[str, Any]:
        self.calls.append(
            ("create_corpus", (project_id, name), {"description": description})
        )
        return {"id": f"corpus-{name}", "name": name}

    def upload_documents_batch_and_wait(
        self,
        corpus_id: str,
        documents: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        self.calls.append(("upload_documents_batch_and_wait", (corpus_id, documents), kwargs))
        return {"batch_id": f"batch-{corpus_id}", "doc_ids": ["doc-1"] * len(documents)}

    def sync_indexes(self, corpus_id: str, **kwargs: Any) -> dict[str, Any]:
        self.calls.append(("sync_indexes", (corpus_id,), kwargs))
        return {"job_id": f"job-{corpus_id}"}

    def search(self, corpus_id: str, query: str, **kwargs: Any) -> dict[str, Any]:
        self.calls.append(("search", (corpus_id, query), kwargs))
        return {"results": self.search_results.get(corpus_id, [])}


class FailingSearchClient(FakeK2Client):
    def search(self, corpus_id: str, query: str, **kwargs: Any) -> dict[str, Any]:
        self.calls.append(("search", (corpus_id, query), kwargs))
        raise RuntimeError("request failed api_key=abc123 token=def456")


class WaitFlagUploadClient(FakeK2Client):
    upload_documents_batch_and_wait = None

    def upload_documents_batch(
        self,
        corpus_id: str,
        documents: list[dict[str, Any]],
        **kwargs: Any,
    ) -> dict[str, Any]:
        self.calls.append(("upload_documents_batch", (corpus_id, documents), kwargs))
        return {"batch_id": f"batch-{corpus_id}", "doc_ids": ["doc-1"] * len(documents)}


class LiveK2Tests(unittest.TestCase):
    def test_create_project_and_corpora_when_ids_are_missing(self) -> None:
        client = FakeK2Client()
        definitions = {
            "code": CorpusDefinition(
                role="code",
                name="flink-code-2.2",
                description="code corpus",
                chunking_source_kind="code",
            ),
            "guides": CorpusDefinition(
                role="guides",
                name="java-rd-guides",
                description="guides corpus",
                chunking_source_kind="guide",
            ),
        }
        config = LiveK2Config(project_name="java-rd-demo", corpus_definitions=definitions)

        result = ensure_live_project_and_corpora(
            client, config, roles=["code", "guides"], create_missing=True,
        )

        self.assertTrue(result.project.created)
        self.assertEqual(result.project_id, "project-1")
        self.assertEqual(result.corpus_ids["code"], "corpus-flink-code-2.2")
        self.assertEqual(result.corpus_ids["guides"], "corpus-java-rd-guides")
        self.assertEqual(
            [call[0] for call in client.calls],
            ["create_project", "create_corpus", "create_corpus"],
        )

    def test_accept_existing_project_and_corpus_ids(self) -> None:
        client = FakeK2Client()
        config = LiveK2Config(
            project_id="project-existing",
            corpus_ids={"code": "corpus-existing"},
        )

        result = ensure_live_project_and_corpora(
            client,
            config,
            roles=["code"],
            create_missing=False,
        )

        self.assertFalse(result.project.created)
        self.assertFalse(result.corpora["code"].created)
        self.assertEqual(result.corpus_ids["code"], "corpus-existing")
        self.assertEqual(client.calls, [])

    def test_load_and_upload_jsonl_documents_grouped_by_role(self) -> None:
        client = FakeK2Client()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "guides.jsonl"
            write_jsonl(generate_seed_guides("flink", "2.2.0"), path)

            grouped = load_jsonl_documents_by_role([path])
            uploads = upload_documents_by_role(
                client,
                grouped,
                {"guides": "corpus-guides"},
                idempotency_prefix="demo",
            )

        self.assertEqual(set(grouped), {"guides"})
        self.assertEqual(uploads["guides"].document_count, 4)
        self.assertEqual(uploads["guides"].chunking["strategy"], "semantic")
        call_name, args, kwargs = client.calls[-1]
        self.assertEqual(call_name, "upload_documents_batch_and_wait")
        self.assertEqual(args[0], "corpus-guides")
        self.assertEqual(len(args[1]), 4)
        self.assertFalse(kwargs["auto_index"])
        self.assertEqual(kwargs["idempotency_key"], "demo-guides-upload")

    def test_upload_jsonl_documents_supports_wait_flag_sdk_shape(self) -> None:
        client = WaitFlagUploadClient()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "guides.jsonl"
            write_jsonl(generate_seed_guides("flink", "2.2.0"), path)

            uploads = upload_documents_by_role(
                client,
                load_jsonl_documents_by_role([path]),
                {"guides": "corpus-guides"},
            )

        self.assertEqual(
            uploads["guides"].response,
            {"batch_id": "batch-corpus-guides", "doc_ids": ["doc-1"] * 4},
        )
        call_name, args, kwargs = client.calls[-1]
        self.assertEqual(call_name, "upload_documents_batch")
        self.assertEqual(args[0], "corpus-guides")
        self.assertTrue(kwargs["wait"])

    def test_orchestrate_returns_structured_dataclass_dict(self) -> None:
        client = FakeK2Client()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "guides.jsonl"
            write_jsonl(generate_seed_guides("flink", "2.2.0"), path)

            result = orchestrate_live_k2(
                client,
                jsonl_paths=[path],
                config=LiveK2Config(
                    project_id="project-1",
                    corpus_ids={"guides": "corpus-guides"},
                ),
                roles=["guides"],
                create_missing=False,
                run_probes=False,
                idempotency_prefix="demo",
            )

        result_dict = result.to_dict()
        self.assertEqual(result.project_id, "project-1")
        self.assertEqual(result_dict["uploads"]["guides"]["document_count"], 4)
        self.assertEqual(result_dict["syncs"]["guides"]["corpus_id"], "corpus-guides")
        self.assertEqual(
            [call[0] for call in client.calls],
            ["upload_documents_batch_and_wait", "sync_indexes"],
        )

    def test_sync_indexes_for_selected_roles(self) -> None:
        client = FakeK2Client()

        syncs = sync_corpus_indexes(
            client,
            {"code": "corpus-code", "guides": "corpus-guides"},
            roles=["guides", "code"],
            idempotency_prefix="demo",
        )

        self.assertEqual(list(syncs), ["guides", "code"])
        self.assertEqual(syncs["guides"].response, {"job_id": "job-corpus-guides"})
        self.assertEqual(client.calls[0][0], "sync_indexes")
        self.assertEqual(client.calls[0][1], ("corpus-guides",))
        self.assertEqual(client.calls[0][2]["idempotency_key"], "demo-guides-sync")
        self.assertTrue(client.calls[0][2]["wait"])

    def test_readiness_probe_uses_existing_filters_and_hybrid_config(self) -> None:
        client = FakeK2Client(search_results={"corpus-code": [{}, {}, {}]})
        probe = ReadinessProbe(
            name="code-ready",
            role="code",
            query="REST handler implementation pattern",
            filters=flink_rest_code_filter(),
            min_results=2,
            top_k=7,
        )

        results = run_readiness_probes(client, {"code": "corpus-code"}, [probe])

        self.assertTrue(results[0].passed)
        self.assertEqual(results[0].result_count, 3)
        call_name, args, kwargs = client.calls[-1]
        self.assertEqual(call_name, "search")
        self.assertEqual(args, ("corpus-code", "REST handler implementation pattern"))
        self.assertEqual(kwargs["filters"], flink_rest_code_filter())
        self.assertEqual(kwargs["hybrid"], DEMO_HYBRID)
        self.assertEqual(kwargs["return_config"], DEMO_RETURN)
        self.assertEqual(kwargs["top_k"], 7)

    def test_validation_and_probe_failures_are_safe(self) -> None:
        with self.assertRaisesRegex(LiveK2ConfigError, "K2_API_KEY"):
            LiveK2Config.from_env({}, require_api_key=True)

        with self.assertRaisesRegex(LiveK2ConfigError, "corpus id"):
            ensure_live_project_and_corpora(
                FakeK2Client(),
                LiveK2Config(project_id="project-1", corpus_ids={}),
                roles=["code"],
                create_missing=False,
            )

        probe = ReadinessProbe(
            name="code-ready",
            role="code",
            query="REST handler implementation pattern",
            filters=flink_rest_code_filter(),
            min_results=1,
        )
        results = run_readiness_probes(
            FailingSearchClient(),
            {"code": "corpus-code"},
            [probe],
        )

        self.assertFalse(results[0].passed)
        self.assertIn("<redacted>", results[0].error or "")
        self.assertNotIn("abc123", results[0].error or "")
        self.assertNotIn("def456", results[0].error or "")


    def test_create_missing_false_raises_without_corpus_id(self) -> None:
        """Default create_missing=False rejects missing corpus IDs."""
        client = FakeK2Client()
        definitions = {
            "code": CorpusDefinition(
                role="code",
                name="flink-code-2.2",
                description="code corpus",
                chunking_source_kind="code",
            ),
        }
        config = LiveK2Config(
            project_id="project-1",
            corpus_definitions=definitions,
        )

        with self.assertRaisesRegex(LiveK2ConfigError, "corpus id"):
            ensure_live_project_and_corpora(client, config, roles=["code"])

        self.assertEqual(client.calls, [])

    def test_create_missing_true_creates_corpus(self) -> None:
        client = FakeK2Client()
        definitions = {
            "code": CorpusDefinition(
                role="code",
                name="flink-code-2.2",
                description="code corpus",
                chunking_source_kind="code",
            ),
        }
        config = LiveK2Config(
            project_id="project-1",
            corpus_definitions=definitions,
        )

        result = ensure_live_project_and_corpora(
            client, config, roles=["code"], create_missing=True,
        )

        self.assertTrue(result.corpora["code"].created)
        self.assertEqual(result.corpus_ids["code"], "corpus-flink-code-2.2")


if __name__ == "__main__":
    unittest.main()
