from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from tests import _paths  # noqa: F401

from k2_java_rd_demo._subprocess_env import safe_subprocess_env


class SubprocessEnvTests(unittest.TestCase):
    @patch.dict(os.environ, {"K2_API_KEY": "secret", "PATH": "/usr/bin", "HOME": "/home/user"})
    def test_strips_k2_api_key(self) -> None:
        env = safe_subprocess_env()
        self.assertNotIn("K2_API_KEY", env)

    @patch.dict(os.environ, {"TAVILY_API_KEY": "secret", "PATH": "/usr/bin"})
    def test_strips_tavily_api_key(self) -> None:
        env = safe_subprocess_env()
        self.assertNotIn("TAVILY_API_KEY", env)

    @patch.dict(os.environ, {"K2_API_KEY": "secret", "PATH": "/usr/bin", "HOME": "/home"})
    def test_keeps_path_and_home(self) -> None:
        env = safe_subprocess_env()
        self.assertEqual(env["PATH"], "/usr/bin")
        self.assertEqual(env["HOME"], "/home")

    @patch.dict(os.environ, {"K2_API_KEY": "secret", "OPENAI_API_KEY": "oai"})
    def test_openai_key_stripped_by_default(self) -> None:
        env = safe_subprocess_env()
        self.assertNotIn("OPENAI_API_KEY", env)

    @patch.dict(os.environ, {"K2_API_KEY": "secret", "OPENAI_API_KEY": "oai"})
    def test_allow_re_includes_openai_key(self) -> None:
        env = safe_subprocess_env(allow={"OPENAI_API_KEY"})
        self.assertIn("OPENAI_API_KEY", env)

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "anthropic", "PATH": "/usr/bin"})
    def test_anthropic_key_stripped_by_default(self) -> None:
        env = safe_subprocess_env()
        self.assertNotIn("ANTHROPIC_API_KEY", env)

    @patch.dict(os.environ, {"ANTHROPIC_API_KEY": "anthropic", "PATH": "/usr/bin"})
    def test_allow_re_includes_anthropic_key(self) -> None:
        env = safe_subprocess_env(allow={"ANTHROPIC_API_KEY"})
        self.assertIn("ANTHROPIC_API_KEY", env)

    @patch.dict(os.environ, {"K2_API_KEY": "secret", "OPENAI_API_KEY": "oai"})
    def test_extra_redact_strips_additional_keys(self) -> None:
        env = safe_subprocess_env(extra_redact={"OPENAI_API_KEY"})
        self.assertNotIn("OPENAI_API_KEY", env)
        self.assertNotIn("K2_API_KEY", env)

    @patch.dict(os.environ, {"K2_API_KEY": "secret", "PATH": "/usr/bin"})
    def test_allow_re_includes_redacted_key(self) -> None:
        env = safe_subprocess_env(allow={"K2_API_KEY"})
        self.assertIn("K2_API_KEY", env)

    @patch.dict(os.environ, {"K2_API_KEY": "k2", "TAVILY_API_KEY": "tav", "OPENAI_API_KEY": "oai", "PATH": "/usr/bin"})
    def test_allow_and_extra_redact_together(self) -> None:
        env = safe_subprocess_env(allow={"TAVILY_API_KEY"}, extra_redact={"OPENAI_API_KEY"})
        self.assertIn("TAVILY_API_KEY", env)
        self.assertNotIn("K2_API_KEY", env)
        self.assertNotIn("OPENAI_API_KEY", env)


if __name__ == "__main__":
    unittest.main()
