from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from tests import _paths  # noqa: F401

from k2_java_rd_demo.k2_config import K2ConfigError, K2ProjectConfig, load_k2_config


class K2ConfigTests(unittest.TestCase):
    def test_defaults_load_without_env_vars(self) -> None:
        config = load_k2_config(environ={})

        self.assertEqual(config.project_id, "8fb08a32-24e9-431f-8250-5a0a619b7232")
        self.assertIn("flink_docs", config.corpus_ids)
        self.assertIn("flink_code", config.corpus_ids)
        self.assertIn("guides", config.corpus_ids)

    def test_env_vars_override_defaults(self) -> None:
        config = load_k2_config(environ={
            "K2_PROJECT_ID": "custom-project-id",
            "K2_FLINK_DOCS_CORPUS_ID": "custom-docs-id",
        })

        self.assertEqual(config.project_id, "custom-project-id")
        self.assertEqual(config.corpus_ids["flink_docs"], "custom-docs-id")
        # Non-overridden roles keep defaults
        self.assertIn("flink_code", config.corpus_ids)

    def test_require_corpus_raises_on_missing(self) -> None:
        config = K2ProjectConfig(project_id="test", corpus_ids={})
        with self.assertRaises(K2ConfigError):
            config.require_corpus("flink_docs")

    def test_require_corpus_returns_id(self) -> None:
        config = K2ProjectConfig(
            project_id="test", corpus_ids={"flink_docs": "abc-123"},
        )
        self.assertEqual(config.require_corpus("flink_docs"), "abc-123")

    def test_blank_env_vars_fall_back_to_defaults(self) -> None:
        config = load_k2_config(environ={"K2_PROJECT_ID": "  ", "K2_FLINK_DOCS_CORPUS_ID": ""})

        self.assertEqual(config.project_id, "8fb08a32-24e9-431f-8250-5a0a619b7232")
        self.assertEqual(config.corpus_ids["flink_docs"], "e87160e6-c5e8-4bee-81eb-7f7d7b8cd331")

    @patch.dict(os.environ, {"K2_PROJECT_ID": "env-project-id"}, clear=False)
    def test_default_environ_reads_os_environ(self) -> None:
        config = load_k2_config()
        self.assertEqual(config.project_id, "env-project-id")

    def test_corpus_ids_are_immutable(self) -> None:
        config = load_k2_config(environ={})
        with self.assertRaises(TypeError):
            config.corpus_ids["new_key"] = "value"


if __name__ == "__main__":
    unittest.main()
