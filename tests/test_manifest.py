from __future__ import annotations

import unittest

from tests import _paths  # noqa: F401

from k2_java_rd_demo._manifest import build_reproducibility_manifest


class ManifestTests(unittest.TestCase):
    def test_manifest_includes_required_fields(self) -> None:
        manifest = build_reproducibility_manifest()

        self.assertIn("git_sha", manifest)
        self.assertIn("git_dirty", manifest)
        self.assertIn("python_version", manifest)
        self.assertIn("platform", manifest)
        self.assertIn("timestamp", manifest)
        self.assertIn("env_flags", manifest)
        self.assertIsInstance(manifest["env_flags"], dict)
        self.assertIn("K2_API_KEY", manifest["env_flags"])

    def test_git_sha_is_string_or_none(self) -> None:
        manifest = build_reproducibility_manifest()

        sha = manifest["git_sha"]
        self.assertTrue(sha is None or (isinstance(sha, str) and len(sha) == 40))

    def test_env_flags_are_booleans(self) -> None:
        manifest = build_reproducibility_manifest()

        for key, value in manifest["env_flags"].items():
            self.assertIsInstance(value, bool, f"{key} should be a bool")


if __name__ == "__main__":
    unittest.main()
