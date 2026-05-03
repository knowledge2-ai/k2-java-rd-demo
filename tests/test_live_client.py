from __future__ import annotations

import unittest

from tests import _paths  # noqa: F401

from k2_java_rd_demo.live_client import create_knowledge2_client, live_client_config_from_env
from k2_java_rd_demo.live_k2 import LiveK2ConfigError


class FakeKnowledge2:
    def __init__(self, **kwargs: str) -> None:
        self.kwargs = kwargs


class LiveClientTests(unittest.TestCase):
    def test_config_from_env_redacts_api_key(self) -> None:
        config = live_client_config_from_env(
            {"K2_API_KEY": "secret-value", "K2_API_HOST": "https://api.example"}
        )

        self.assertTrue(config.api_key_present)
        self.assertEqual(config.api_host, "https://api.example")
        self.assertNotIn("secret-value", str(config.to_dict()))

    def test_create_client_uses_env_without_exposing_secret(self) -> None:
        client = create_knowledge2_client(
            {"K2_API_KEY": "secret-value", "K2_API_HOST": "https://api.example"},
            knowledge2_cls=FakeKnowledge2,
        )

        self.assertEqual(
            client.kwargs,
            {"api_key": "secret-value", "api_host": "https://api.example"},
        )

    def test_create_client_requires_api_key(self) -> None:
        with self.assertRaisesRegex(LiveK2ConfigError, "K2_API_KEY"):
            create_knowledge2_client({}, knowledge2_cls=FakeKnowledge2)


if __name__ == "__main__":
    unittest.main()
