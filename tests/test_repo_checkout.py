from __future__ import annotations

import json
import subprocess
import unittest
from unittest.mock import patch

from tests import _paths  # noqa: F401

from k2_java_rd_demo.repo_checkout import (
    DEFAULT_CHECKOUT_BASE_DIR,
    build_checkout_plan,
    build_checkout_plans,
    checkout_plans_to_json,
)
from k2_java_rd_demo.source_catalog import FLINK_CODE_SOURCE


class RepoCheckoutTests(unittest.TestCase):
    def test_default_plan_is_sparse_flink_checkout(self) -> None:
        plans = build_checkout_plans(base_dir="/tmp/demo-sources")

        self.assertEqual(len(plans), 1)
        plan = plans[0]
        self.assertEqual(plan.repo, "apache/flink")
        self.assertEqual(plan.repo_ref, "release-2.2.0")
        self.assertEqual(plan.clone_url, "https://github.com/apache/flink.git")
        self.assertEqual(plan.target_name, "apache-flink-release-2.2.0")
        self.assertEqual(plan.target_dir, "/tmp/demo-sources/apache-flink-release-2.2.0")
        self.assertTrue(plan.sparse)
        self.assertEqual(plan.include_paths, FLINK_CODE_SOURCE.include_paths)
        self.assertEqual(plan.exclude_paths, FLINK_CODE_SOURCE.exclude_paths)

        self.assertEqual(
            plan.commands[0],
            [
                "git",
                "clone",
                "--filter=blob:none",
                "--no-checkout",
                "--branch",
                "release-2.2.0",
                "https://github.com/apache/flink.git",
                "/tmp/demo-sources/apache-flink-release-2.2.0",
            ],
        )
        self.assertEqual(
            plan.commands[-1],
            ["git", "-C", plan.target_dir, "checkout", plan.repo_ref],
        )
        self.assertTrue(all(isinstance(command, list) for command in plan.commands))

    def test_optional_kafka_plan_is_added_deterministically(self) -> None:
        plans = build_checkout_plans(include_kafka=True, base_dir="/cache/sources")

        self.assertEqual([plan.repo for plan in plans], ["apache/flink", "apache/kafka"])
        self.assertEqual(
            [plan.target_name for plan in plans],
            [
                "apache-flink-release-2.2.0",
                "apache-kafka-4.2",
            ],
        )
        self.assertEqual(
            [plan.target_dir for plan in plans],
            [
                "/cache/sources/apache-flink-release-2.2.0",
                "/cache/sources/apache-kafka-4.2",
            ],
        )
        self.assertEqual(plans[1].repo_ref, "4.2")
        self.assertEqual(plans[1].clone_url, "https://github.com/apache/kafka.git")
        self.assertIn("connect/runtime/src/main/java/", plans[1].include_paths)

    def test_sparse_commands_include_sparse_checkout_paths(self) -> None:
        plan = build_checkout_plan(FLINK_CODE_SOURCE, base_dir=DEFAULT_CHECKOUT_BASE_DIR)

        sparse_set = plan.commands[2]
        self.assertEqual(
            sparse_set[:8],
            [
                "git",
                "-C",
                plan.target_dir,
                "sparse-checkout",
                "set",
                "--no-cone",
                "--",
                "flink-runtime/src/main/java/",
            ],
        )
        for include_path in FLINK_CODE_SOURCE.include_paths:
            self.assertIn(include_path, sparse_set)
        self.assertNotIn("target/", sparse_set)

    def test_full_clone_plan_omits_sparse_checkout_commands(self) -> None:
        plan = build_checkout_plan(FLINK_CODE_SOURCE, base_dir="/tmp/demo-sources", sparse=False)

        self.assertFalse(plan.sparse)
        self.assertEqual(
            plan.commands,
            (
                [
                    "git",
                    "clone",
                    "--branch",
                    "release-2.2.0",
                    "--single-branch",
                    "https://github.com/apache/flink.git",
                    "/tmp/demo-sources/apache-flink-release-2.2.0",
                ],
            ),
        )
        self.assertFalse(any("sparse-checkout" in command for command in plan.commands))

    def test_building_plans_does_not_execute_git(self) -> None:
        with patch.object(subprocess, "run") as run:
            plan = build_checkout_plan(FLINK_CODE_SOURCE, base_dir="/tmp/demo-sources")

        run.assert_not_called()
        self.assertEqual(plan.commands[0][0], "git")

    def test_plan_shape_is_json_serializable(self) -> None:
        plans = build_checkout_plans(include_kafka=True, base_dir="/tmp/demo-sources")

        payload = [plan.to_dict() for plan in plans]
        encoded = checkout_plans_to_json(plans, indent=None)
        decoded = json.loads(encoded)

        self.assertEqual(decoded, payload)
        self.assertEqual(decoded[0]["commands"][0][0], "git")
        self.assertEqual(decoded[0]["target_name"], "apache-flink-release-2.2.0")
        self.assertEqual(decoded[0]["include_paths"], list(FLINK_CODE_SOURCE.include_paths))
        self.assertIsInstance(decoded[0]["commands"], list)
        self.assertIsInstance(decoded[0]["commands"][0], list)


if __name__ == "__main__":
    unittest.main()
