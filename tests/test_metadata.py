from __future__ import annotations

import json
import unittest

from tests import _paths  # noqa: F401

from k2_java_rd_demo.metadata import (
    MetadataValidationError,
    build_code_metadata,
    infer_api_surface,
    infer_module,
    infer_source_kind,
    validate_metadata,
)


JAVA_TEXT = """
package org.apache.flink.runtime.rest.handler.job;

public class JobCheckpointHandler extends AbstractRestHandler implements Runnable {
    public String handleRequest(String request) {
        return request;
    }

    private void helper() {
    }
}
"""


class MetadataTests(unittest.TestCase):
    def test_infer_source_kind(self) -> None:
        self.assertEqual(infer_source_kind("flink-runtime/src/main/java/Foo.java"), "code")
        self.assertEqual(infer_source_kind("flink-runtime/src/test/java/FooTest.java"), "test")
        self.assertEqual(infer_source_kind("pom.xml"), "build")
        self.assertEqual(infer_source_kind("conf/flink.yaml"), "config")

    def test_infer_module(self) -> None:
        self.assertEqual(infer_module("flink-runtime/src/main/java/Foo.java"), "flink-runtime")

    def test_infer_api_surface_prefers_kafka_connect_domain_over_rest_path(self) -> None:
        self.assertEqual(
            infer_api_surface("connect/runtime/src/main/java/rest/ConnectorPluginsResource.java"),
            "connect",
        )
        self.assertEqual(
            infer_api_surface(
                "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/"
                "CheckpointCoordinator.java",
                "REST endpoint text should not override checkpointing path.",
            ),
            "checkpointing",
        )

    def test_build_code_metadata_extracts_java_symbols(self) -> None:
        metadata = build_code_metadata(
            path="flink-runtime/src/main/java/Foo.java",
            text=JAVA_TEXT,
            framework="flink",
            framework_version="2.2.0",
            repo="apache/flink",
            repo_ref="release-2.2.0",
        )
        self.assertEqual(metadata["java_package"], "org.apache.flink.runtime.rest.handler.job")
        self.assertEqual(metadata["class_name"], "JobCheckpointHandler")
        self.assertEqual(metadata["extends"], "AbstractRestHandler")
        self.assertIn("Runnable", metadata["implements"])
        self.assertIn("handleRequest", metadata["symbols"])
        self.assertEqual(metadata["api_surface"], "rest")

    def test_build_code_metadata_compacts_large_symbol_lists(self) -> None:
        long_methods = "\n".join(
            f"public void methodWithAVeryLongGeneratedName{i:02d}"
            f"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ() {{}}"
            for i in range(40)
        )
        metadata = build_code_metadata(
            path="connect/runtime/src/test/java/GeneratedTest.java",
            text=f"public class GeneratedTest {{\n{long_methods}\n}}",
            framework="kafka",
            framework_version="4.2.0",
            repo="apache/kafka",
            repo_ref="4.2",
        )

        self.assertLessEqual(len(json.dumps(metadata["symbols"]).encode("utf-8")), 1024)
        self.assertLessEqual(len(metadata["symbols"]), 20)

    def test_reserved_key_rejected(self) -> None:
        metadata = build_code_metadata(
            path="flink-runtime/src/main/java/Foo.java",
            text=JAVA_TEXT,
            framework="flink",
            framework_version="2.2.0",
            repo="apache/flink",
            repo_ref="release-2.2.0",
        )
        metadata["source_uri"] = "repo://bad"
        with self.assertRaises(MetadataValidationError):
            validate_metadata(metadata)


if __name__ == "__main__":
    unittest.main()
