from __future__ import annotations

import json
import unittest

from tests import _paths  # noqa: F401

from k2_java_rd_demo.metadata import DEMO_DATASET_ID
from k2_java_rd_demo.source_catalog import (
    FLINK_DOCS_ENTRYPOINT,
    KAFKA_CONNECT_GUIDE,
    KAFKA_DOCS_ENTRYPOINT,
    build_ingestion_manifest,
    manifest_to_json,
    normalize_frameworks,
)


class SourceCatalogTests(unittest.TestCase):
    def test_default_manifest_contains_flink_docs_and_code_only(self) -> None:
        manifest = build_ingestion_manifest()

        self.assertEqual(manifest.dataset_id, DEMO_DATASET_ID)
        self.assertEqual(manifest.frameworks, ("flink",))
        self.assertFalse(manifest.include_kafka)
        self.assertEqual([source.framework for source in manifest.docs_sources], ["flink"])
        self.assertEqual([source.framework for source in manifest.code_sources], ["flink"])

        flink_docs = manifest.docs_sources[0]
        self.assertEqual(flink_docs.corpus_name, "flink-docs-2.2")
        self.assertEqual(flink_docs.corpus_role, "docs")
        self.assertEqual(flink_docs.source_kind, "docs")
        self.assertEqual(flink_docs.doc_type, "release_docs")
        self.assertEqual(flink_docs.seed_urls, (FLINK_DOCS_ENTRYPOINT,))

        flink_code = manifest.code_sources[0]
        self.assertEqual(flink_code.corpus_name, "flink-code-2.2")
        self.assertEqual(flink_code.repo, "apache/flink")
        self.assertEqual(flink_code.repo_ref, "release-2.2.0")
        self.assertIn("https://github.com/apache/flink.git", flink_code.clone_urls)
        self.assertIn("flink-runtime/src/main/java/", flink_code.include_paths)
        self.assertIn("target/", flink_code.exclude_paths)
        self.assertIn("test", flink_code.source_kinds)

    def test_optional_kafka_sources_are_added_deterministically(self) -> None:
        manifest = build_ingestion_manifest(include_kafka=True)

        self.assertEqual(manifest.frameworks, ("flink", "kafka"))
        self.assertTrue(manifest.include_kafka)
        self.assertEqual(
            [source.corpus_name for source in manifest.docs_sources],
            ["flink-docs-2.2", "kafka-docs-4.2"],
        )
        self.assertEqual(
            [source.corpus_name for source in manifest.code_sources],
            ["flink-code-2.2", "kafka-code-4.2"],
        )

        kafka_docs = manifest.docs_sources[1]
        self.assertEqual(kafka_docs.framework, "kafka")
        self.assertEqual(kafka_docs.version, "4.2.0")
        self.assertIn(KAFKA_DOCS_ENTRYPOINT, kafka_docs.seed_urls)
        self.assertIn(KAFKA_CONNECT_GUIDE, kafka_docs.seed_urls)
        self.assertIn("42/kafka-connect/connector-development-guide/", kafka_docs.include_paths)

        kafka_code = manifest.code_sources[1]
        self.assertEqual(kafka_code.repo, "apache/kafka")
        self.assertIn("https://github.com/apache/kafka.git", kafka_code.clone_urls)
        self.assertIn("connect/runtime/src/main/java/", kafka_code.include_paths)

    def test_selected_frameworks_accept_comma_separated_cli_shape(self) -> None:
        self.assertEqual(normalize_frameworks("flink"), ("flink",))
        self.assertEqual(normalize_frameworks("flink,kafka"), ("flink", "kafka"))
        self.assertEqual(normalize_frameworks(["kafka"]), ("flink", "kafka"))

        with self.assertRaises(ValueError):
            normalize_frameworks("spark")

    def test_manifest_shape_is_json_serializable(self) -> None:
        manifest = build_ingestion_manifest(["flink"], include_kafka=True)
        payload = manifest.to_dict()

        self.assertEqual(payload["frameworks"], ["flink", "kafka"])
        self.assertEqual(payload["docs_sources"][0]["seed_urls"], [FLINK_DOCS_ENTRYPOINT])
        self.assertEqual(
            payload["code_sources"][0]["clone_urls"],
            ["https://github.com/apache/flink.git"],
        )

        encoded = manifest_to_json(manifest, indent=None)
        decoded = json.loads(encoded)
        self.assertEqual(decoded, payload)


if __name__ == "__main__":
    unittest.main()
