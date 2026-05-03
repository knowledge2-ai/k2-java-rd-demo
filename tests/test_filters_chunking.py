from __future__ import annotations

import unittest

from tests import _paths  # noqa: F401

from k2_java_rd_demo.chunking import chunking_for_source_kind
from k2_java_rd_demo.filters import DEMO_HYBRID, demo_filter_catalog, flink_rest_code_filter


class FilterChunkingTests(unittest.TestCase):
    def test_hybrid_includes_metadata_sparse(self) -> None:
        self.assertTrue(DEMO_HYBRID["metadata_sparse_enabled"])
        self.assertGreater(DEMO_HYBRID["metadata_sparse_weight"], 0)

    def test_filter_shape(self) -> None:
        filters = flink_rest_code_filter()
        self.assertEqual(filters["condition"], "and")
        self.assertTrue(all("key" in item and "op" in item for item in filters["filters"]))

    def test_filter_catalog_has_demo_recipes(self) -> None:
        catalog = demo_filter_catalog()
        self.assertIn("flink_rest_code", catalog)
        self.assertIn("kafka_connect", catalog)
        kafka_api_surface_filter = next(
            item for item in catalog["kafka_connect"]["filters"] if item["key"] == "api_surface"
        )
        self.assertEqual(kafka_api_surface_filter["op"], "in")
        self.assertEqual(kafka_api_surface_filter["value"], ["connect", "rest"])

    def test_chunking_profiles_are_separate(self) -> None:
        self.assertEqual(chunking_for_source_kind("code")["chunk_size"], 1200)
        self.assertEqual(chunking_for_source_kind("test")["chunk_size"], 1400)
        self.assertEqual(chunking_for_source_kind("docs")["chunk_size"], 220)


if __name__ == "__main__":
    unittest.main()
