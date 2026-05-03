from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests import _paths  # noqa: F401

from k2_java_rd_demo.assets import (
    build_documents_from_repo,
    generate_seed_guides,
    read_jsonl,
    write_jsonl,
)


class AssetTests(unittest.TestCase):
    def test_build_documents_from_repo_and_jsonl_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "flink-runtime" / "src" / "main" / "java" / "DemoHandler.java"
            source.parent.mkdir(parents=True)
            source.write_text(
                "package org.apache.flink.runtime.rest;\n"
                "public class DemoHandler { public String handleRequest() { return \"ok\"; } }\n",
                encoding="utf-8",
            )
            excluded = root / "flink-runtime" / "target" / "Generated.java"
            excluded.parent.mkdir(parents=True)
            excluded.write_text("public class Generated {}", encoding="utf-8")

            docs = build_documents_from_repo(
                root,
                framework="flink",
                framework_version="2.2.0",
                repo="apache/flink",
                repo_ref="release-2.2.0",
            )
            self.assertEqual(len(docs), 1)
            self.assertEqual(docs[0].metadata["module"], "flink-runtime")
            self.assertEqual(docs[0].metadata["api_surface"], "rest")

            out = root / "out.jsonl"
            self.assertEqual(write_jsonl(docs, out), 1)
            loaded = read_jsonl(out)
            self.assertEqual(loaded[0]["metadata"]["class_name"], "DemoHandler")

    def test_generate_seed_guides(self) -> None:
        guides = generate_seed_guides("flink", "2.2.0")
        self.assertGreaterEqual(len(guides), 2)
        self.assertEqual(guides[0].metadata["source_kind"], "guide")
        self.assertEqual(guides[0].metadata["corpus_role"], "guides")


if __name__ == "__main__":
    unittest.main()
