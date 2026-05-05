"""Patch-generation benchmark helpers for coding-agent feature tasks."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class VerificationCommand:
    """One command used to validate a generated patch."""

    name: str
    argv: Sequence[str]
    timeout_s: int = 900

    def __post_init__(self) -> None:
        object.__setattr__(self, "argv", tuple(str(part) for part in self.argv))
        if not self.argv:
            raise ValueError("verification command argv must not be empty")

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "argv": list(self.argv), "timeout_s": self.timeout_s}


@dataclass(frozen=True)
class PatchTask:
    """A feature-development task for comparing final code patches."""

    task_id: str
    title: str
    framework: str
    version: str
    repo: str
    repo_ref: str
    source_root_key: str
    prompt: str
    expected_paths: Sequence[str] = field(default_factory=tuple)
    allowed_path_prefixes: Sequence[str] = field(default_factory=tuple)
    success_criteria: Sequence[str] = field(default_factory=tuple)
    verification_commands: Sequence[VerificationCommand] = field(default_factory=tuple)
    k2_query: str = ""
    api_surface: str = ""
    task_class: str = "local_pattern"
    difficulty: str = "small"
    docs_paths: Sequence[str] = field(default_factory=tuple)
    docs_urls: Sequence[str] = field(default_factory=tuple)
    requires_docs: bool = False
    requires_guides: bool = False
    guide_paths: Sequence[str] = field(default_factory=tuple)
    guide_source_uris: Sequence[str] = field(default_factory=tuple)
    required_guardrails: Sequence[str] = field(default_factory=tuple)
    forbidden_patterns: Sequence[str] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        object.__setattr__(self, "expected_paths", _string_tuple(self.expected_paths))
        object.__setattr__(
            self, "allowed_path_prefixes", _string_tuple(self.allowed_path_prefixes)
        )
        object.__setattr__(self, "success_criteria", _string_tuple(self.success_criteria))
        object.__setattr__(self, "verification_commands", tuple(self.verification_commands))
        object.__setattr__(self, "docs_paths", _string_tuple(self.docs_paths))
        object.__setattr__(self, "docs_urls", _string_tuple(self.docs_urls))
        object.__setattr__(self, "guide_paths", _string_tuple(self.guide_paths))
        object.__setattr__(self, "guide_source_uris", _string_tuple(self.guide_source_uris))
        object.__setattr__(self, "required_guardrails", _string_tuple(self.required_guardrails))
        object.__setattr__(self, "forbidden_patterns", _string_tuple(self.forbidden_patterns))

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "framework": self.framework,
            "version": self.version,
            "repo": self.repo,
            "repo_ref": self.repo_ref,
            "source_root_key": self.source_root_key,
            "prompt": self.prompt,
            "expected_paths": list(self.expected_paths),
            "allowed_path_prefixes": list(self.allowed_path_prefixes),
            "success_criteria": list(self.success_criteria),
            "verification_commands": [
                command.to_dict() for command in self.verification_commands
            ],
            "k2_query": self.k2_query,
            "api_surface": self.api_surface,
            "task_class": self.task_class,
            "difficulty": self.difficulty,
            "docs_paths": list(self.docs_paths),
            "docs_urls": list(self.docs_urls),
            "requires_docs": self.requires_docs,
            "requires_guides": self.requires_guides,
            "guide_paths": list(self.guide_paths),
            "guide_source_uris": list(self.guide_source_uris),
            "required_guardrails": list(self.required_guardrails),
            "forbidden_patterns": list(self.forbidden_patterns),
        }


PATCH_ARM_NAMES = (
    "codex_repo_only",
    "codex_repo_plus_docs",
    "codex_repo_plus_guides_dump",
    "codex_with_k2_mcp",
    "codex_with_k2_mcp_no_guides",
    "codex_with_k2_mcp_filters_off",
)

CODEX_INFRA_FAILURE_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "codex_websocket_failure",
        (
            "failed to connect to websocket",
            "backend-api/codex/responses",
        ),
    ),
    (
        "codex_model_refresh_failure",
        (
            "failed to refresh available models",
            "backend-api/codex/models",
        ),
    ),
    (
        "codex_chatgpt_request_failure",
        (
            "http/request failed",
            "backend-api/wham/apps",
            "chatgpt.com/backend-api",
        ),
    ),
    (
        "codex_dns_failure",
        (
            "dns error",
            "name resolution",
            "temporary failure in name resolution",
            "nodename nor servname",
        ),
    ),
    (
        "codex_network_failure",
        (
            "network is unreachable",
            "connection reset",
            "connection refused",
            "tls handshake",
        ),
    ),
)


def patch_tasks(*, include_kafka: bool = True) -> tuple[PatchTask, ...]:
    """Return the built-in feature-task catalog.

    These tasks are intentionally small, source-local changes.  They are meant
    to compare generated patches, not to be a replacement for a full SWE-bench
    style benchmark.
    """

    tasks: list[PatchTask] = [
        PatchTask(
            task_id="flink-rest-job-vertex-watermarks-include-missing",
            title="Add optional missing-subtask reporting to Flink vertex watermark REST output",
            framework="flink",
            version="2.2.0",
            repo="apache/flink",
            repo_ref="release-2.2.0",
            source_root_key="flink",
            api_surface="rest",
            task_class="docs_code_test",
            difficulty="small",
            requires_docs=True,
            requires_guides=True,
            guide_paths=("guides/flink/confluence-rest-handler-guardrails.md",),
            guide_source_uris=(
                "generated://guides/flink/confluence-rest-handler-guardrails.md",
            ),
            required_guardrails=("CF-FLINK-REST-001",),
            forbidden_patterns=("Spring MVC", "JAX-RS", "servlet controller"),
            docs_paths=("flink-docs/content/docs/ops/rest_api.md", "flink-docs/content"),
            docs_urls=("https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/",),
            k2_query=(
                "Flink 2.2 JobVertexWatermarksHandler request parameters MetricCollectionResponseBody tests"
            ),
            prompt=(
                "Add a small backwards-compatible request option to the Flink 2.2 "
                "`JobVertexWatermarksHandler`. When an optional query parameter named "
                "`includeMissing` is true, include one `Metric` per subtask even if the "
                "current input watermark metric is absent, using the existing metric id and "
                "a null value. Preserve the default behavior when the query parameter is "
                "absent or false. Update the focused handler test coverage."
            ),
            expected_paths=(
                "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/"
                "metrics/JobVertexWatermarksHandler.java",
                "flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/"
                "metrics/JobVertexWatermarksHandlerTest.java",
            ),
            allowed_path_prefixes=(
                "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/"
                "metrics/",
                "flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/job/"
                "metrics/",
                "flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/"
                "metrics/",
            ),
            success_criteria=(
                "`includeMissing` is optional and defaults to current behavior.",
                "Missing watermark metrics are emitted only when explicitly requested.",
                "Focused handler tests cover default, partial, and include-missing behavior.",
            ),
            verification_commands=(
                VerificationCommand(
                    name="flink-runtime-rest-message-test",
                    argv=(
                        "./mvnw",
                        "-pl",
                        "flink-runtime",
                        "-DskipITs",
                        "-Dcheckstyle.skip",
                        "-Dspotless.check.skip=true",
                        "-Denforcer.skip=true",
                        "-DfailIfNoTests=false",
                        "-Dsurefire.module.config.jdk21=",
                        "-Dtest=JobVertexWatermarksHandlerTest",
                        "test",
                    ),
                    timeout_s=1800,
                ),
            ),
        ),
        PatchTask(
            task_id="flink-rest-cluster-overview-optional-cluster-id",
            title="Add optional cluster id metadata to Flink cluster overview REST output",
            framework="flink",
            version="2.2.0",
            repo="apache/flink",
            repo_ref="release-2.2.0",
            source_root_key="flink",
            api_surface="rest",
            task_class="version_sensitive_rest",
            difficulty="small",
            requires_docs=True,
            docs_paths=("flink-docs/content/docs/ops/rest_api.md", "flink-docs/content"),
            docs_urls=("https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/",),
            k2_query=(
                "Flink 2.2 ClusterOverviewWithVersion JSON fields legacy message test"
            ),
            prompt=(
                "Add an optional JSON field named `cluster-id` to the Flink 2.2 "
                "`ClusterOverviewWithVersion` REST response body. Existing constructors, "
                "existing JSON field names, equality, and hash-code behavior should remain "
                "compatible when the field is absent. Update the focused marshalling test."
            ),
            expected_paths=(
                "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/legacy/"
                "messages/ClusterOverviewWithVersion.java",
                "flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/legacy/"
                "messages/ClusterOverviewWithVersionTest.java",
            ),
            allowed_path_prefixes=(
                "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/legacy/"
                "messages/",
                "flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/legacy/"
                "messages/",
            ),
            success_criteria=(
                "Existing JSON fields and constructor call sites remain compatible.",
                "`cluster-id` is optional.",
                "Focused serialization coverage is added or updated.",
            ),
            verification_commands=(
                VerificationCommand(
                    name="flink-runtime-cluster-overview-test",
                    argv=(
                        "./mvnw",
                        "-pl",
                        "flink-runtime",
                        "-DskipITs",
                        "-Dcheckstyle.skip",
                        "-Dspotless.check.skip=true",
                        "-Denforcer.skip=true",
                        "-DfailIfNoTests=false",
                        "-Dsurefire.module.config.jdk21=",
                        "-Dtest=ClusterOverviewWithVersionTest",
                        "test",
                    ),
                    timeout_s=1800,
                ),
            ),
        ),
        PatchTask(
            task_id="flink-rest-dashboard-config-optional-deployment-mode",
            title="Add optional deployment mode metadata to Flink dashboard configuration",
            framework="flink",
            version="2.2.0",
            repo="apache/flink",
            repo_ref="release-2.2.0",
            source_root_key="flink",
            api_surface="rest",
            task_class="docs_code_test",
            difficulty="small",
            requires_docs=True,
            requires_guides=True,
            guide_paths=("guides/flink/confluence-rest-handler-guardrails.md",),
            guide_source_uris=(
                "generated://guides/flink/confluence-rest-handler-guardrails.md",
            ),
            required_guardrails=("CF-FLINK-REST-001",),
            forbidden_patterns=("Spring MVC", "JAX-RS", "servlet controller"),
            docs_paths=("flink-docs/content/docs/ops/rest_api.md", "flink-docs/content"),
            docs_urls=("https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/",),
            k2_query=(
                "Flink 2.2 DashboardConfiguration optional JSON field marshalling test"
            ),
            prompt=(
                "Add a backwards-compatible optional JSON field named `deployment-mode` "
                "to the Flink 2.2 `DashboardConfiguration` response body. Existing "
                "constructors and `DashboardConfiguration.from(...)` call sites should "
                "remain source-compatible and should omit the field when no deployment "
                "mode is supplied. Update focused marshalling coverage."
            ),
            expected_paths=(
                "flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/"
                "DashboardConfiguration.java",
                "flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/"
                "DashboardConfigurationTest.java",
            ),
            allowed_path_prefixes=(
                "flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/",
                "flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/",
            ),
            success_criteria=(
                "`deployment-mode` is optional and omitted when absent.",
                "Existing factory and constructor usage stays compatible.",
                "Serialization coverage verifies present and absent values.",
            ),
            verification_commands=(
                VerificationCommand(
                    name="flink-dashboard-configuration-test",
                    argv=(
                        "./mvnw",
                        "-pl",
                        "flink-runtime",
                        "-DskipITs",
                        "-Dcheckstyle.skip",
                        "-Dspotless.check.skip=true",
                        "-Denforcer.skip=true",
                        "-DfailIfNoTests=false",
                        "-Dsurefire.module.config.jdk21=",
                        "-Dtest=DashboardConfigurationTest",
                        "test",
                    ),
                    timeout_s=1800,
                ),
            ),
        ),
        PatchTask(
            task_id="flink-rest-job-status-optional-status-timestamp",
            title="Add optional status timestamp to Flink job status REST output",
            framework="flink",
            version="2.2.0",
            repo="apache/flink",
            repo_ref="release-2.2.0",
            source_root_key="flink",
            api_surface="rest",
            task_class="docs_code_test",
            difficulty="small",
            requires_docs=True,
            requires_guides=True,
            guide_paths=("guides/flink/confluence-rest-handler-guardrails.md",),
            guide_source_uris=(
                "generated://guides/flink/confluence-rest-handler-guardrails.md",
            ),
            required_guardrails=("CF-FLINK-REST-001",),
            forbidden_patterns=("Spring MVC", "JAX-RS", "servlet controller"),
            docs_paths=("flink-docs/content/docs/ops/rest_api.md", "flink-docs/content"),
            docs_urls=("https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/",),
            k2_query=(
                "Flink 2.2 JobStatusInfo JSON marshalling optional timestamp handler test"
            ),
            prompt=(
                "Add a backwards-compatible optional JSON field named `status-timestamp` "
                "to the Flink 2.2 `JobStatusInfo` response body. Preserve the existing "
                "`JobStatusInfo(JobStatus)` constructor and current `JobStatusHandler` "
                "behavior when the timestamp is absent. Add focused marshalling tests for "
                "the absent and present timestamp cases."
            ),
            expected_paths=(
                "flink-runtime/src/main/java/org/apache/flink/runtime/messages/"
                "webmonitor/JobStatusInfo.java",
                "flink-runtime/src/test/java/org/apache/flink/runtime/messages/"
                "webmonitor/JobStatusInfoTest.java",
            ),
            allowed_path_prefixes=(
                "flink-runtime/src/main/java/org/apache/flink/runtime/messages/webmonitor/",
                "flink-runtime/src/test/java/org/apache/flink/runtime/messages/webmonitor/",
                "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/",
                "flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/",
            ),
            success_criteria=(
                "`status-timestamp` is optional and omitted when absent.",
                "Existing handler behavior and constructor usage remain compatible.",
                "Focused tests cover JSON with and without the timestamp.",
            ),
            verification_commands=(
                VerificationCommand(
                    name="flink-job-status-info-test",
                    argv=(
                        "./mvnw",
                        "-pl",
                        "flink-runtime",
                        "-DskipITs",
                        "-Dcheckstyle.skip",
                        "-Dspotless.check.skip=true",
                        "-Denforcer.skip=true",
                        "-DfailIfNoTests=false",
                        "-Dsurefire.module.config.jdk21=",
                        "-Dtest=JobStatusInfoTest",
                        "test",
                    ),
                    timeout_s=1800,
                ),
            ),
        ),
        PatchTask(
            task_id="flink-rest-job-config-optional-scheduler-hint",
            title="Add optional scheduler hint metadata to Flink job config REST output",
            framework="flink",
            version="2.2.0",
            repo="apache/flink",
            repo_ref="release-2.2.0",
            source_root_key="flink",
            api_surface="rest",
            task_class="docs_code_test",
            difficulty="small",
            requires_docs=True,
            requires_guides=True,
            guide_paths=("guides/flink/confluence-rest-handler-guardrails.md",),
            guide_source_uris=(
                "generated://guides/flink/confluence-rest-handler-guardrails.md",
            ),
            required_guardrails=("CF-FLINK-REST-001",),
            forbidden_patterns=("Spring MVC", "JAX-RS", "servlet controller"),
            docs_paths=("flink-docs/content/docs/ops/rest_api.md", "flink-docs/content"),
            docs_urls=("https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/",),
            k2_query=(
                "Flink 2.2 JobConfigInfo custom serializer optional JSON field test"
            ),
            prompt=(
                "Add a backwards-compatible optional JSON field named `scheduler-hint` "
                "to the Flink 2.2 `JobConfigInfo` response body. Preserve the existing "
                "constructor and custom serializer/deserializer behavior when the field "
                "is absent. Add focused tests covering serialization and deserialization "
                "with and without the hint."
            ),
            expected_paths=(
                "flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/"
                "JobConfigInfo.java",
                "flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/"
                "JobConfigInfoTest.java",
            ),
            allowed_path_prefixes=(
                "flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/",
                "flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/",
            ),
            success_criteria=(
                "`scheduler-hint` is optional and omitted when absent.",
                "Custom serializer and deserializer remain backwards-compatible.",
                "Focused tests cover absent and present values.",
            ),
            verification_commands=(
                VerificationCommand(
                    name="flink-job-config-info-test",
                    argv=(
                        "./mvnw",
                        "-pl",
                        "flink-runtime",
                        "-DskipITs",
                        "-Dcheckstyle.skip",
                        "-Dspotless.check.skip=true",
                        "-Denforcer.skip=true",
                        "-DfailIfNoTests=false",
                        "-Dsurefire.module.config.jdk21=",
                        "-Dtest=JobConfigInfoTest",
                        "test",
                    ),
                    timeout_s=1800,
                ),
            ),
        ),
        PatchTask(
            task_id="flink-rest-job-details-optional-archived-flag",
            title="Add optional archived flag to Flink job details REST output",
            framework="flink",
            version="2.2.0",
            repo="apache/flink",
            repo_ref="release-2.2.0",
            source_root_key="flink",
            api_surface="rest",
            task_class="docs_code_test",
            difficulty="small",
            requires_docs=True,
            requires_guides=True,
            guide_paths=("guides/flink/confluence-rest-handler-guardrails.md",),
            guide_source_uris=(
                "generated://guides/flink/confluence-rest-handler-guardrails.md",
            ),
            required_guardrails=("CF-FLINK-REST-001",),
            forbidden_patterns=("Spring MVC", "JAX-RS", "servlet controller"),
            docs_paths=("flink-docs/content/docs/ops/rest_api.md", "flink-docs/content"),
            docs_urls=("https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/",),
            k2_query=(
                "Flink 2.2 JobDetailsInfo optional archived JSON field marshalling test"
            ),
            prompt=(
                "Add a backwards-compatible optional Boolean JSON field named `archived` "
                "to the Flink 2.2 `JobDetailsInfo` response body. Preserve the existing "
                "constructor and handler behavior when the flag is absent. Update focused "
                "marshalling coverage for absent, true, and false values."
            ),
            expected_paths=(
                "flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/job/"
                "JobDetailsInfo.java",
                "flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/job/"
                "JobDetailsInfoTest.java",
            ),
            allowed_path_prefixes=(
                "flink-runtime/src/main/java/org/apache/flink/runtime/rest/messages/job/",
                "flink-runtime/src/test/java/org/apache/flink/runtime/rest/messages/job/",
                "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/",
                "flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/",
            ),
            success_criteria=(
                "`archived` is optional and omitted when absent.",
                "Existing constructor and handler call sites remain compatible.",
                "Focused tests cover absent, true, and false values.",
            ),
            verification_commands=(
                VerificationCommand(
                    name="flink-job-details-info-test",
                    argv=(
                        "./mvnw",
                        "-pl",
                        "flink-runtime",
                        "-DskipITs",
                        "-Dcheckstyle.skip",
                        "-Dspotless.check.skip=true",
                        "-Denforcer.skip=true",
                        "-DfailIfNoTests=false",
                        "-Dsurefire.module.config.jdk21=",
                        "-Dtest=JobDetailsInfoTest",
                        "test",
                    ),
                    timeout_s=1800,
                ),
            ),
        ),
    ]
    if include_kafka:
        tasks.extend(
            [
                PatchTask(
                    task_id="kafka-connect-plugin-info-optional-location",
                    title="Add optional location metadata to Kafka Connect plugin info response",
                    framework="kafka",
                    version="4.2",
                    repo="apache/kafka",
                    repo_ref="4.2",
                    source_root_key="kafka",
                    api_surface="connect",
                    task_class="docs_code_test",
                    difficulty="small",
                    requires_docs=True,
                    requires_guides=True,
                    guide_paths=("guides/kafka/confluence-connect-rest-entity-guardrails.md",),
                    guide_source_uris=(
                        "generated://guides/kafka/confluence-connect-rest-entity-guardrails.md",
                    ),
                    required_guardrails=("CF-KAFKA-CONNECT-007",),
                    forbidden_patterns=("Spring Validator", "Bean Validation", "javax.validation"),
                    docs_paths=("docs", "connect/runtime/src/main/java"),
                    docs_urls=("https://kafka.apache.org/42/kafka-connect/connector-development-guide/",),
                    k2_query=(
                        "Kafka 4.2 Connect PluginInfo REST entity JSON serialization test"
                    ),
                    prompt=(
                        "Add a backwards-compatible optional JSON field named `location` to "
                        "the Kafka Connect `PluginInfo` REST entity. Existing construction "
                        "from `PluginDesc` should remain compatible and should omit the field "
                        "when no location is available. Add focused JSON serialization and "
                        "deserialization coverage in the existing entity test."
                    ),
                    expected_paths=(
                        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/PluginInfo.java",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/PluginInfoTest.java",
                    ),
                    allowed_path_prefixes=(
                        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/",
                    ),
                    success_criteria=(
                        "`location` is optional and omitted when null.",
                        "Existing PluginDesc construction remains source-compatible.",
                        "Unit tests cover location present and absent behavior.",
                    ),
                    verification_commands=(
                        VerificationCommand(
                            name="kafka-connect-plugin-info-test",
                            argv=(
                                "./gradlew",
                                ":connect:runtime:test",
                                "--tests",
                                "org.apache.kafka.connect.runtime.rest.entities.PluginInfoTest",
                            ),
                            timeout_s=1800,
                        ),
                    ),
                ),
                PatchTask(
                    task_id="kafka-connect-create-connector-request-validate-only",
                    title="Add optional validate-only flag to Kafka Connect create-connector request",
                    framework="kafka",
                    version="4.2",
                    repo="apache/kafka",
                    repo_ref="4.2",
                    source_root_key="kafka",
                    api_surface="connect",
                    task_class="version_sensitive_connect",
                    difficulty="small",
                    requires_docs=True,
                    docs_paths=("docs", "connect/runtime/src/main/java"),
                    docs_urls=("https://kafka.apache.org/42/kafka-connect/",),
                    k2_query=(
                        "Kafka 4.2 Connect CreateConnectorRequest initial_state JSON test"
                    ),
                    prompt=(
                        "Add a backwards-compatible optional Boolean field named "
                        "`validate_only` to the Kafka Connect `CreateConnectorRequest` REST "
                        "entity. Preserve the existing record construction pattern and "
                        "`initial_state` behavior. Add focused tests for absent, true, and "
                        "false values without changing connector creation semantics."
                    ),
                    expected_paths=(
                        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/CreateConnectorRequest.java",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/CreateConnectorRequestTest.java",
                    ),
                    allowed_path_prefixes=(
                        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/",
                    ),
                    success_criteria=(
                        "`validate_only` is optional and maps to JSON `validate_only`.",
                        "Existing initial_state behavior remains unchanged.",
                        "Focused tests cover absent, true, and false values.",
                    ),
                    verification_commands=(
                        VerificationCommand(
                            name="kafka-create-connector-request-test",
                            argv=(
                                "./gradlew",
                                ":connect:runtime:test",
                                "--tests",
                                "org.apache.kafka.connect.runtime.rest.entities."
                                "CreateConnectorRequestTest",
                            ),
                            timeout_s=1800,
                        ),
                    ),
                ),
                PatchTask(
                    task_id="kafka-connect-connector-info-optional-owner",
                    title="Add optional owner metadata to Kafka Connect connector info response",
                    framework="kafka",
                    version="4.2",
                    repo="apache/kafka",
                    repo_ref="4.2",
                    source_root_key="kafka",
                    api_surface="connect",
                    task_class="docs_code_test",
                    difficulty="small",
                    requires_docs=True,
                    requires_guides=True,
                    guide_paths=("guides/kafka/confluence-connect-rest-entity-guardrails.md",),
                    guide_source_uris=(
                        "generated://guides/kafka/confluence-connect-rest-entity-guardrails.md",
                    ),
                    required_guardrails=("CF-KAFKA-CONNECT-007",),
                    forbidden_patterns=("Spring Validator", "Bean Validation", "javax.validation"),
                    docs_paths=("docs", "connect/runtime/src/main/java"),
                    docs_urls=("https://kafka.apache.org/42/kafka-connect/",),
                    k2_query=(
                        "Kafka 4.2 Connect ConnectorInfo REST entity optional JSON field test"
                    ),
                    prompt=(
                        "Add a backwards-compatible optional JSON field named `owner` to "
                        "the Kafka Connect `ConnectorInfo` REST entity. Existing record "
                        "construction should remain source-compatible and should omit the "
                        "field when no owner is available. Add focused JSON serialization "
                        "and deserialization coverage."
                    ),
                    expected_paths=(
                        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/ConnectorInfo.java",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/ConnectorInfoTest.java",
                    ),
                    allowed_path_prefixes=(
                        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/",
                    ),
                    success_criteria=(
                        "`owner` is optional and omitted when null.",
                        "Existing ConnectorInfo construction remains source-compatible.",
                        "Unit tests cover owner present and absent behavior.",
                    ),
                    verification_commands=(
                        VerificationCommand(
                            name="kafka-connect-connector-info-test",
                            argv=(
                                "./gradlew",
                                ":connect:runtime:test",
                                "--tests",
                                "org.apache.kafka.connect.runtime.rest.entities."
                                "ConnectorInfoTest",
                            ),
                            timeout_s=1800,
                        ),
                    ),
                ),
                PatchTask(
                    task_id="kafka-connect-task-info-optional-generation",
                    title="Add optional generation metadata to Kafka Connect task info response",
                    framework="kafka",
                    version="4.2",
                    repo="apache/kafka",
                    repo_ref="4.2",
                    source_root_key="kafka",
                    api_surface="connect",
                    task_class="docs_code_test",
                    difficulty="small",
                    requires_docs=True,
                    requires_guides=True,
                    guide_paths=("guides/kafka/confluence-connect-rest-entity-guardrails.md",),
                    guide_source_uris=(
                        "generated://guides/kafka/confluence-connect-rest-entity-guardrails.md",
                    ),
                    required_guardrails=("CF-KAFKA-CONNECT-007",),
                    forbidden_patterns=("Spring Validator", "Bean Validation", "javax.validation"),
                    docs_paths=("docs", "connect/runtime/src/main/java"),
                    docs_urls=("https://kafka.apache.org/42/kafka-connect/",),
                    k2_query=(
                        "Kafka 4.2 Connect TaskInfo REST entity optional generation JSON test"
                    ),
                    prompt=(
                        "Add a backwards-compatible optional Integer JSON field named "
                        "`generation` to the Kafka Connect `TaskInfo` REST entity. Preserve "
                        "existing record construction when generation is absent and omit "
                        "the JSON field when null. Add focused serialization and "
                        "deserialization tests."
                    ),
                    expected_paths=(
                        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/TaskInfo.java",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/TaskInfoTest.java",
                    ),
                    allowed_path_prefixes=(
                        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/",
                    ),
                    success_criteria=(
                        "`generation` is optional and omitted when null.",
                        "Existing TaskInfo construction remains source-compatible.",
                        "Unit tests cover generation present and absent behavior.",
                    ),
                    verification_commands=(
                        VerificationCommand(
                            name="kafka-connect-task-info-test",
                            argv=(
                                "./gradlew",
                                ":connect:runtime:test",
                                "--tests",
                                "org.apache.kafka.connect.runtime.rest.entities.TaskInfoTest",
                            ),
                            timeout_s=1800,
                        ),
                    ),
                ),
                PatchTask(
                    task_id="kafka-connect-server-info-optional-worker-id",
                    title="Add optional worker id metadata to Kafka Connect server info response",
                    framework="kafka",
                    version="4.2",
                    repo="apache/kafka",
                    repo_ref="4.2",
                    source_root_key="kafka",
                    api_surface="connect",
                    task_class="docs_code_test",
                    difficulty="small",
                    requires_docs=True,
                    requires_guides=True,
                    guide_paths=("guides/kafka/confluence-connect-rest-entity-guardrails.md",),
                    guide_source_uris=(
                        "generated://guides/kafka/confluence-connect-rest-entity-guardrails.md",
                    ),
                    required_guardrails=("CF-KAFKA-CONNECT-007",),
                    forbidden_patterns=("Spring Validator", "Bean Validation", "javax.validation"),
                    docs_paths=("docs", "connect/runtime/src/main/java"),
                    docs_urls=("https://kafka.apache.org/42/kafka-connect/",),
                    k2_query=(
                        "Kafka 4.2 Connect ServerInfo REST entity optional worker_id JSON test"
                    ),
                    prompt=(
                        "Add a backwards-compatible optional JSON field named `worker_id` "
                        "to the Kafka Connect `ServerInfo` REST entity. Preserve the "
                        "existing public constructor that accepts only `kafkaClusterId`, "
                        "and omit `worker_id` when no worker id is supplied. Add focused "
                        "JSON serialization and deserialization tests."
                    ),
                    expected_paths=(
                        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/ServerInfo.java",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/ServerInfoTest.java",
                    ),
                    allowed_path_prefixes=(
                        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/",
                    ),
                    success_criteria=(
                        "`worker_id` is optional and omitted when null.",
                        "Existing ServerInfo construction remains source-compatible.",
                        "Unit tests cover worker id present and absent behavior.",
                    ),
                    verification_commands=(
                        VerificationCommand(
                            name="kafka-connect-server-info-test",
                            argv=(
                                "./gradlew",
                                ":connect:runtime:test",
                                "--tests",
                                "org.apache.kafka.connect.runtime.rest.entities.ServerInfoTest",
                            ),
                            timeout_s=1800,
                        ),
                    ),
                ),
                PatchTask(
                    task_id="kafka-connect-config-value-info-optional-source",
                    title="Add optional source metadata to Kafka Connect config value response",
                    framework="kafka",
                    version="4.2",
                    repo="apache/kafka",
                    repo_ref="4.2",
                    source_root_key="kafka",
                    api_surface="connect",
                    task_class="docs_code_test",
                    difficulty="small",
                    requires_docs=True,
                    requires_guides=True,
                    guide_paths=("guides/kafka/confluence-connect-rest-entity-guardrails.md",),
                    guide_source_uris=(
                        "generated://guides/kafka/confluence-connect-rest-entity-guardrails.md",
                    ),
                    required_guardrails=("CF-KAFKA-CONNECT-007",),
                    forbidden_patterns=("Spring Validator", "Bean Validation", "javax.validation"),
                    docs_paths=("docs", "connect/runtime/src/main/java"),
                    docs_urls=("https://kafka.apache.org/42/kafka-connect/",),
                    k2_query=(
                        "Kafka 4.2 Connect ConfigValueInfo optional source JSON test"
                    ),
                    prompt=(
                        "Add a backwards-compatible optional JSON field named `source` to "
                        "the Kafka Connect `ConfigValueInfo` REST entity. Existing record "
                        "construction should remain source-compatible and should omit "
                        "`source` when null. Add focused JSON serialization and "
                        "deserialization tests."
                    ),
                    expected_paths=(
                        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/ConfigValueInfo.java",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/ConfigValueInfoTest.java",
                    ),
                    allowed_path_prefixes=(
                        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/",
                        "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/"
                        "rest/entities/",
                    ),
                    success_criteria=(
                        "`source` is optional and omitted when null.",
                        "Existing ConfigValueInfo construction remains source-compatible.",
                        "Unit tests cover source present and absent behavior.",
                    ),
                    verification_commands=(
                        VerificationCommand(
                            name="kafka-connect-config-value-info-test",
                            argv=(
                                "./gradlew",
                                ":connect:runtime:test",
                                "--tests",
                                "org.apache.kafka.connect.runtime.rest.entities."
                                "ConfigValueInfoTest",
                            ),
                            timeout_s=1800,
                        ),
                    ),
                ),
            ]
        )
    return tuple(tasks)


def patch_generation_prompt(task: PatchTask, *, arm_name: str) -> str:
    """Build a controlled feature-development prompt for one benchmark arm."""

    if arm_name not in PATCH_ARM_NAMES:
        raise ValueError(f"unknown patch benchmark arm: {arm_name}")
    retrieval_clause = _retrieval_clause(task, arm_name)
    return (
        "You are running a controlled patch-generation benchmark for a Java R&D task.\n"
        f"{retrieval_clause}\n"
        "Web search and browser use are disabled. Keep the patch minimal and scoped. "
        "Run only focused tests that are relevant and affordable; if you cannot run a test, "
        "state exactly why.\n\n"
        f"Repository: {task.repo}@{task.repo_ref}\n"
        f"Framework/version: {task.framework} {task.version}\n"
        f"Task class: {task.task_class}\n"
        f"Task: {task.title}\n\n"
        f"Feature request:\n{task.prompt}\n\n"
        "Allowed edit neighborhoods:\n"
        f"{json.dumps(list(task.allowed_path_prefixes), indent=2)}\n\n"
        "Success criteria:\n"
        f"{json.dumps(list(task.success_criteria), indent=2)}\n\n"
        "Final response requirements:\n"
        "- Summarize the implemented code changes.\n"
        "- If guide evidence is available, include a Guide compliance line naming the "
        "applicable guide or guardrail and any forbidden patterns avoided.\n"
        "- List tests run and their result.\n"
        "- List any remaining uncertainty.\n"
        "- Do not include large code blocks; the benchmark records the git diff separately.\n"
    )


def _retrieval_clause(task: PatchTask, arm_name: str) -> str:
    docs_context = _docs_context(task)
    if arm_name == "codex_repo_only":
        return (
            "Do not use K2 or MCP tools. Use only local repository inspection such as `rg` "
            "and file reads. Do not use external web search."
        )
    if arm_name == "codex_repo_plus_docs":
        return (
            "Do not use K2 or MCP tools. Use local repository inspection plus the local "
            "documentation directories listed below. Web search remains disabled; URLs are "
            f"version-pinned identifiers, not fetch instructions.\n{docs_context}"
        )
    if arm_name == "codex_repo_plus_guides_dump":
        return (
            "Do not use K2 or MCP tools. Use local repository inspection plus the local "
            "Confluence-style guide dump and documentation directories listed below. This is "
            "the strongest vanilla-Codex baseline: the same guide content is available as "
            "local files, but there is no MCP steering or K2 metadata routing.\n"
            f"{docs_context}\n{_guide_dump_context(task)}"
        )
    if arm_name == "codex_with_k2_mcp_no_guides":
        return (
            "You must use available K2 MCP retrieval tools before editing, but guide retrieval "
            "is intentionally disabled for this ablation. Use version-specific docs, source, "
            f"and tests. Cite retrieved source URIs. Suggested query: {task.k2_query}."
        )
    if arm_name == "codex_with_k2_mcp_filters_off":
        return (
            "You must use available K2 MCP retrieval tools before editing. Metadata filters are "
            "intentionally disabled for this ablation, so verify returned source versions and "
            f"paths carefully. Cite retrieved source URIs. Suggested query: {task.k2_query}."
        )
    return (
        "You must use the available K2 MCP retrieval tool before editing. Make exactly one "
        "`k2_answer_with_sources` call. Use K2 to inspect version-specific docs, source, "
        "tests, and generated Confluence-style engineering guides before local exploration. "
        "Avoid broad local `rg`; read only the exact files you plan to edit or exact "
        "source/test paths returned by K2. "
        "If a guide result includes a guardrail ID, cite that exact ID in the final Guide "
        "compliance line, along with the retrieved guide source URI and forbidden patterns "
        "avoided. Cite retrieved source URIs in your final summary. Suggested retrieval query: "
        f"{task.k2_query}."
    )


def _docs_context(task: PatchTask) -> str:
    lines = ["Local/version-pinned documentation context:"]
    if task.docs_paths:
        lines.append(f"- Local docs/search roots: {json.dumps(list(task.docs_paths))}")
    if task.docs_urls:
        lines.append(f"- Version-pinned docs URLs: {json.dumps(list(task.docs_urls))}")
    if len(lines) == 1:
        lines.append("- No task-specific docs roots are declared; inspect repository docs if present.")
    return "\n".join(lines)


def _guide_dump_context(task: PatchTask) -> str:
    lines = ["Local Confluence-style guide dump context:"]
    if task.guide_paths:
        local_paths = [f".k2-demo-confluence-dump/{path}" for path in task.guide_paths]
        lines.append(f"- Local guide files: {json.dumps(local_paths)}")
        lines.append("- Inspect the applicable guide files before editing or citing guardrails.")
    if len(lines) == 1:
        lines.append("- No task-specific guide files are declared.")
    return "\n".join(lines)


def score_patch_run(
    task: PatchTask,
    *,
    diff_text: str,
    answer_text: str | None = None,
    verification_results: Sequence[Mapping[str, Any]] = (),
    duration_s: float | None = None,
    token_metrics: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Score one generated patch with deterministic, source-level metrics."""

    changed_files = extract_changed_files(diff_text)
    changed_set = set(changed_files)
    expected_set = set(task.expected_paths)
    expected_hits = sorted(changed_set & expected_set)
    expected_score = len(expected_hits) / len(expected_set) if expected_set else None
    scope_score = _scope_score(changed_files, task.allowed_path_prefixes)
    diff_score = 1.0 if diff_text.strip() else 0.0
    verification_score = _verification_score(verification_results)
    guide_guardrail_score = _guide_guardrail_score(
        task,
        answer_text=answer_text,
        diff_text=diff_text,
    )

    scored_values = [
        value
        for value in (
            expected_score,
            scope_score,
            diff_score,
            verification_score,
            guide_guardrail_score,
        )
        if value is not None
    ]
    combined_score = sum(scored_values) / len(scored_values) if scored_values else 0.0
    guide_guardrail_pass = guide_guardrail_score is None or guide_guardrail_score >= 1.0
    return {
        "task_id": task.task_id,
        "title": task.title,
        "framework": task.framework,
        "task_class": task.task_class,
        "difficulty": task.difficulty,
        "score": round(combined_score, 6),
        "passed": (
            combined_score >= 0.8
            and verification_score == 1.0
            and guide_guardrail_pass
        ),
        "duration_s": round(duration_s, 3) if duration_s is not None else None,
        "token_metrics": dict(token_metrics or {}),
        "changed_files": changed_files,
        "score_breakdown": {
            "expected_file_coverage": _round_optional(expected_score),
            "scope_score": _round_optional(scope_score),
            "diff_present": diff_score,
            "verification_score": _round_optional(verification_score),
            "guide_guardrail_score": _round_optional(guide_guardrail_score),
        },
        "expected_file_hits": expected_hits,
        "missing_expected_files": sorted(expected_set - changed_set),
        "out_of_scope_files": _out_of_scope_files(changed_files, task.allowed_path_prefixes),
        "failure_categories": classify_patch_failure(
            diff_text=diff_text,
            changed_files=changed_files,
            verification_results=verification_results,
            missing_expected_files=sorted(expected_set - changed_set),
            out_of_scope_files=_out_of_scope_files(changed_files, task.allowed_path_prefixes),
            guide_guardrail_score=guide_guardrail_score,
        ),
        "verification_results": [dict(result) for result in verification_results],
    }


def extract_changed_files(diff_text: str) -> list[str]:
    """Return repo-relative paths touched by a unified git diff."""

    changed: list[str] = []
    seen: set[str] = set()
    for line in diff_text.splitlines():
        if not line.startswith("diff --git "):
            continue
        parts = line.split()
        if len(parts) < 4:
            continue
        path = _strip_diff_prefix(parts[3])
        if path == "/dev/null":
            path = _strip_diff_prefix(parts[2])
        if path and path not in seen:
            seen.add(path)
            changed.append(path)
    return changed


def extract_codex_usage_metrics(events_text: str) -> dict[str, Any]:
    """Extract best-effort token and tool metrics from Codex JSON event output."""

    totals = {
        "input_tokens": 0,
        "output_tokens": 0,
        "cached_input_tokens": 0,
        "total_tokens": 0,
    }
    max_seen = dict(totals)
    event_count = 0
    tool_counts: dict[str, int] = {}
    mcp_tool_failures: dict[str, int] = {}
    for line in events_text.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        event_count += 1
        for usage in _walk_usage_dicts(event):
            for key in totals:
                value = _int_value(usage.get(key))
                if value is not None:
                    max_seen[key] = max(max_seen[key], value)
        tool_name = _tool_name_from_event(event)
        if tool_name:
            tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1
        failed_tool_name = _failed_mcp_tool_name_from_event(event)
        if failed_tool_name:
            mcp_tool_failures[failed_tool_name] = (
                mcp_tool_failures.get(failed_tool_name, 0) + 1
            )
    for key, value in max_seen.items():
        totals[key] = value
    if not totals["total_tokens"]:
        totals["total_tokens"] = totals["input_tokens"] + totals["output_tokens"]
    k2_tool_failure_count = sum(
        count for tool, count in mcp_tool_failures.items() if tool.startswith("k2_")
    )
    return {
        **totals,
        "event_count": event_count,
        "tool_counts": dict(sorted(tool_counts.items())),
        "mcp_tool_failures": dict(sorted(mcp_tool_failures.items())),
        "k2_tool_failure_count": k2_tool_failure_count,
    }


def validate_local_java_imports(
    task: PatchTask,
    worktree: Path,
    changed_files: Sequence[str],
) -> dict[str, Any]:
    """Check changed Java files for unresolved same-project imports.

    This is a lightweight compile-proxy for environments where Maven/Gradle are
    not installed.  It intentionally checks only imports from the benchmarked
    framework's own package namespace.
    """

    import_prefix = _framework_import_prefix(task.framework)
    if not import_prefix:
        return {
            "name": "local-java-import-resolution",
            "passed": True,
            "checked_imports": 0,
            "unresolved_imports": [],
        }
    source_roots = _java_source_roots(worktree)
    unresolved: list[dict[str, str]] = []
    checked = 0
    for relative_path in changed_files:
        if not relative_path.endswith(".java"):
            continue
        path = worktree / relative_path
        if not path.exists():
            continue
        for imported in _java_imports(path.read_text(encoding="utf-8", errors="replace")):
            if not _should_check_project_import(imported, import_prefix):
                continue
            checked += 1
            if not _import_resolves(imported, source_roots):
                unresolved.append({"file": relative_path, "import": imported})
    return {
        "name": "local-java-import-resolution",
        "passed": not unresolved,
        "checked_imports": checked,
        "unresolved_imports": unresolved,
    }


def classify_patch_failure(
    *,
    diff_text: str,
    changed_files: Sequence[str],
    verification_results: Sequence[Mapping[str, Any]],
    missing_expected_files: Sequence[str],
    out_of_scope_files: Sequence[str],
    guide_guardrail_score: float | None = None,
) -> list[str]:
    """Return stable failure buckets for post-run analysis."""

    categories: list[str] = []
    if not diff_text.strip():
        categories.append("no_patch")
    if missing_expected_files:
        categories.append("missed_expected_files")
    if out_of_scope_files:
        categories.append("out_of_scope_changes")
    if guide_guardrail_score is not None and guide_guardrail_score < 1.0:
        categories.append("guide_guardrail_failure")
    for result in verification_results:
        if result.get("passed"):
            continue
        name = str(result.get("name") or "")
        if name == "git-diff-check":
            categories.append("patch_format_failure")
        elif name == "local-java-import-resolution":
            categories.append("static_import_failure")
        elif name:
            categories.append("focused_test_failure")
    if changed_files and not categories and _verification_score(verification_results) != 1.0:
        categories.append("unclassified_verification_failure")
    return sorted(set(categories))


def _guide_guardrail_score(
    task: PatchTask,
    *,
    answer_text: str | None,
    diff_text: str,
) -> float | None:
    if not task.required_guardrails:
        return None
    if answer_text is None:
        return None
    haystack = _normalize_text(f"{answer_text}\n{diff_text}")
    required_hits = sum(
        1 for item in task.required_guardrails if _normalize_text(item) in haystack
    )
    required_score = required_hits / len(task.required_guardrails)
    guide_citations = (
        *task.guide_source_uris,
        *(f".k2-demo-confluence-dump/{path}" for path in task.guide_paths),
        *task.guide_paths,
    )
    citation_score = 1.0 if any(
        _normalize_text(citation) in haystack for citation in guide_citations
    ) else 0.0
    diff_haystack = _normalize_text(diff_text)
    forbidden_hits = [
        pattern
        for pattern in task.forbidden_patterns
        if _normalize_text(pattern) in diff_haystack
    ]
    forbidden_score = 0.0 if forbidden_hits else 1.0
    return (required_score * 0.6) + (citation_score * 0.2) + (forbidden_score * 0.2)


def summarize_patch_scorecard(runs: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Aggregate patch benchmark task scores by arm."""

    by_arm: dict[str, list[Mapping[str, Any]]] = {}
    for run in runs:
        arm = str(run.get("arm_name") or "")
        if arm:
            by_arm.setdefault(arm, []).append(run)
    summaries = []
    for arm_name, arm_runs in sorted(by_arm.items()):
        valid_arm_runs = [run for run in arm_runs if not is_infra_invalid_run(run)]
        scores = [float(run.get("score") or 0.0) for run in valid_arm_runs]
        durations = [
            float(run["duration_s"])
            for run in valid_arm_runs
            if isinstance(run.get("duration_s"), (int, float))
        ]
        total_tokens = [
            int((run.get("token_metrics") or {}).get("total_tokens") or 0)
            for run in valid_arm_runs
        ]
        guide_scores = [
            float((run.get("score_breakdown") or {}).get("guide_guardrail_score"))
            for run in valid_arm_runs
            if isinstance((run.get("score_breakdown") or {}).get("guide_guardrail_score"), (int, float))
        ]
        summaries.append(
            {
                "arm_name": arm_name,
                "task_count": len(arm_runs),
                "valid_task_count": len(valid_arm_runs),
                "infra_invalid_tasks": len(arm_runs) - len(valid_arm_runs),
                "passed_tasks": sum(1 for run in valid_arm_runs if run.get("passed")),
                "mean_score": _mean(scores),
                "mean_duration_s": _mean(durations),
                "mean_total_tokens": _mean(total_tokens),
                "mean_guide_guardrail_score": _mean(guide_scores),
            }
        )
    return {
        "arms": summaries,
        "by_task_class": _summaries_by_key(runs, "task_class"),
        "failure_categories": _failure_category_counts(runs),
        "signal": assess_feature_development_signal(runs),
    }


def assess_feature_development_signal(
    runs: Sequence[Mapping[str, Any]],
    *,
    baseline_arm: str = "codex_repo_plus_guides_dump",
    treatment_arm: str = "codex_with_k2_mcp",
    min_tasks_for_claim: int = 10,
) -> dict[str, Any]:
    """Apply the predeclared K2 feature-development decision rule."""

    infra_invalid_count = sum(1 for run in runs if is_infra_invalid_run(run))
    valid_runs = [run for run in runs if not is_infra_invalid_run(run)]
    baseline = [run for run in valid_runs if run.get("arm_name") == baseline_arm]
    treatment = [run for run in valid_runs if run.get("arm_name") == treatment_arm]
    paired_task_ids = sorted(
        {str(run.get("task_id")) for run in baseline}
        & {str(run.get("task_id")) for run in treatment}
    )
    baseline_pass_rate = _pass_rate(baseline)
    treatment_pass_rate = _pass_rate(treatment)
    pass_rate_delta = treatment_pass_rate - baseline_pass_rate
    baseline_duration = _mean(
        [float(run["duration_s"]) for run in baseline if isinstance(run.get("duration_s"), (int, float))]
    )
    treatment_duration = _mean(
        [
            float(run["duration_s"])
            for run in treatment
            if isinstance(run.get("duration_s"), (int, float))
        ]
    )
    duration_ratio = (
        round(treatment_duration / baseline_duration, 6) if baseline_duration else None
    )
    baseline_duration_per_accepted_patch = _duration_per_accepted_patch(baseline)
    treatment_duration_per_accepted_patch = _duration_per_accepted_patch(treatment)
    duration_per_accepted_patch_ratio = (
        round(
            treatment_duration_per_accepted_patch / baseline_duration_per_accepted_patch,
            6,
        )
        if baseline_duration_per_accepted_patch and treatment_duration_per_accepted_patch
        else None
    )
    baseline_tokens = _mean(
        [
            int((run.get("token_metrics") or {}).get("total_tokens") or 0)
            for run in baseline
            if int((run.get("token_metrics") or {}).get("total_tokens") or 0) > 0
        ]
    )
    treatment_tokens = _mean(
        [
            int((run.get("token_metrics") or {}).get("total_tokens") or 0)
            for run in treatment
            if int((run.get("token_metrics") or {}).get("total_tokens") or 0) > 0
        ]
    )
    token_ratio = round(treatment_tokens / baseline_tokens, 6) if baseline_tokens else None
    baseline_tokens_per_accepted_patch = _tokens_per_accepted_patch(baseline)
    treatment_tokens_per_accepted_patch = _tokens_per_accepted_patch(treatment)
    token_per_accepted_patch_ratio = (
        round(
            treatment_tokens_per_accepted_patch / baseline_tokens_per_accepted_patch,
            6,
        )
        if baseline_tokens_per_accepted_patch and treatment_tokens_per_accepted_patch
        else None
    )
    baseline_guide_score = _mean_optional(
        [
            float((run.get("score_breakdown") or {}).get("guide_guardrail_score"))
            for run in baseline
            if isinstance(
                (run.get("score_breakdown") or {}).get("guide_guardrail_score"),
                (int, float),
            )
        ]
    )
    treatment_guide_score = _mean_optional(
        [
            float((run.get("score_breakdown") or {}).get("guide_guardrail_score"))
            for run in treatment
            if isinstance(
                (run.get("score_breakdown") or {}).get("guide_guardrail_score"),
                (int, float),
            )
        ]
    )
    guide_guardrail_delta = (
        round(treatment_guide_score - baseline_guide_score, 6)
        if baseline_guide_score is not None and treatment_guide_score is not None
        else None
    )
    guide_guardrail_ok = (
        guide_guardrail_delta is None or guide_guardrail_delta >= 0
    )
    duration_ok = duration_ratio is None or duration_ratio <= 1.3
    duration_per_accepted_patch_ok = (
        duration_per_accepted_patch_ratio is None
        or duration_per_accepted_patch_ratio <= 0.9
    )
    token_savings_ok = token_ratio is not None and token_ratio <= 0.9
    token_per_accepted_patch_savings_ok = (
        token_per_accepted_patch_ratio is not None
        and token_per_accepted_patch_ratio <= 0.9
    )
    quality_ok = (
        pass_rate_delta >= 0.15
        and guide_guardrail_ok
    )
    usable_output_efficiency_ok = (
        duration_ok or duration_per_accepted_patch_ok
    ) and token_per_accepted_patch_savings_ok
    if len(paired_task_ids) < min_tasks_for_claim:
        verdict = "insufficient_sample"
    elif quality_ok and token_savings_ok and usable_output_efficiency_ok:
        verdict = "k2_wins"
    elif quality_ok and token_savings_ok:
        verdict = "k2_quality_token_win_with_latency_tradeoff"
    elif quality_ok:
        verdict = "k2_quality_win_without_token_savings"
    elif abs(pass_rate_delta) <= 0.05:
        verdict = "no_clear_k2_win"
    else:
        verdict = "mixed_or_task_dependent"
    return {
        "baseline_arm": baseline_arm,
        "treatment_arm": treatment_arm,
        "infra_invalid_count": infra_invalid_count,
        "paired_task_count": len(paired_task_ids),
        "min_tasks_for_claim": min_tasks_for_claim,
        "baseline_pass_rate": round(baseline_pass_rate, 6),
        "treatment_pass_rate": round(treatment_pass_rate, 6),
        "pass_rate_delta": round(pass_rate_delta, 6),
        "baseline_mean_duration_s": baseline_duration,
        "treatment_mean_duration_s": treatment_duration,
        "duration_ratio": duration_ratio,
        "baseline_duration_per_accepted_patch_s": baseline_duration_per_accepted_patch,
        "treatment_duration_per_accepted_patch_s": treatment_duration_per_accepted_patch,
        "duration_per_accepted_patch_ratio": duration_per_accepted_patch_ratio,
        "duration_per_accepted_patch_ok": duration_per_accepted_patch_ok,
        "baseline_mean_total_tokens": baseline_tokens,
        "treatment_mean_total_tokens": treatment_tokens,
        "token_ratio": token_ratio,
        "token_savings_ok": token_savings_ok,
        "baseline_tokens_per_accepted_patch": baseline_tokens_per_accepted_patch,
        "treatment_tokens_per_accepted_patch": treatment_tokens_per_accepted_patch,
        "token_per_accepted_patch_ratio": token_per_accepted_patch_ratio,
        "token_per_accepted_patch_savings_ok": token_per_accepted_patch_savings_ok,
        "usable_output_efficiency_ok": usable_output_efficiency_ok,
        "baseline_mean_guide_guardrail_score": baseline_guide_score,
        "treatment_mean_guide_guardrail_score": treatment_guide_score,
        "guide_guardrail_delta": guide_guardrail_delta,
        "guide_guardrail_ok": guide_guardrail_ok,
        "duration_ok": duration_ok,
        "verdict": verdict,
    }


def verify_patch_scorecard_evidence(
    payload: Mapping[str, Any],
    *,
    baseline_arm: str = "codex_repo_plus_guides_dump",
    treatment_arm: str = "codex_with_k2_mcp",
    min_tasks_for_claim: int = 10,
    require_k2_probe: bool = True,
    require_k2_tools: bool = True,
    require_focused_tests: bool = False,
) -> dict[str, Any]:
    """Audit whether a patch scorecard supports a public K2 customer claim."""

    runs = payload.get("runs")
    runs = runs if isinstance(runs, Sequence) and not isinstance(runs, (str, bytes)) else []
    run_rows = [run for run in runs if isinstance(run, Mapping)]
    signal = assess_feature_development_signal(
        run_rows,
        baseline_arm=baseline_arm,
        treatment_arm=treatment_arm,
        min_tasks_for_claim=min_tasks_for_claim,
    )
    issues: list[str] = []
    checks: dict[str, bool] = {}

    baseline_raw = _runs_by_task(run_rows, baseline_arm)
    treatment_raw = _runs_by_task(run_rows, treatment_arm)
    raw_paired_task_ids = sorted(set(baseline_raw) & set(treatment_raw))
    checks["no_infra_invalid_runs"] = True
    for task_id in raw_paired_task_ids:
        for arm_name, run in (
            (baseline_arm, baseline_raw[task_id]),
            (treatment_arm, treatment_raw[task_id]),
        ):
            if is_infra_invalid_run(run):
                checks["no_infra_invalid_runs"] = False
                reason = (
                    run.get("infra_failure_reason")
                    or classify_codex_infra_failure(str(run.get("error") or ""))
                    or "unknown"
                )
                issues.append(f"{task_id}: {arm_name} run is infrastructure-invalid ({reason})")

    valid_run_rows = [run for run in run_rows if not is_infra_invalid_run(run)]
    baseline = _runs_by_task(valid_run_rows, baseline_arm)
    treatment = _runs_by_task(valid_run_rows, treatment_arm)
    paired_task_ids = sorted(set(baseline) & set(treatment))
    checks["paired_sample_size"] = len(paired_task_ids) >= min_tasks_for_claim
    if not checks["paired_sample_size"]:
        issues.append(
            f"paired task count {len(paired_task_ids)} is below required {min_tasks_for_claim}"
        )

    k2_probe = _k2_probe_from_payload(payload)
    checks["k2_sdk_probe"] = (
        not require_k2_probe
        or (
            isinstance(k2_probe, Mapping)
            and (_int_value(k2_probe.get("result_count")) or 0) > 0
            and bool(k2_probe.get("first_source_uri"))
        )
    )
    if not checks["k2_sdk_probe"]:
        issues.append("missing successful live K2 SDK preflight probe")

    checks["k2_tool_calls"] = True
    checks["k2_tool_failures_absent"] = True
    checks["codex_usage_metrics"] = True
    checks["focused_tests"] = True
    task_specs = _task_specs_by_id(payload)
    for task_id in paired_task_ids:
        k2_run = treatment[task_id]
        token_metrics = k2_run.get("token_metrics") or {}
        if require_k2_tools and not _has_k2_tool_call(token_metrics):
            checks["k2_tool_calls"] = False
            issues.append(f"{task_id}: K2 treatment run has no recorded K2 MCP tool call")
        if (_int_value(token_metrics.get("k2_tool_failure_count")) or 0) > 0 or (
            "k2_mcp_tool_failure" in (k2_run.get("failure_categories") or [])
        ):
            checks["k2_tool_failures_absent"] = False
            issues.append(f"{task_id}: K2 treatment run recorded an MCP tool failure")
        if (_int_value(token_metrics.get("total_tokens")) or 0) <= 0:
            checks["codex_usage_metrics"] = False
            issues.append(f"{task_id}: K2 treatment run has no total token metric")
        if require_focused_tests and not _focused_tests_recorded(
            baseline[task_id],
            task_specs.get(task_id),
        ):
            checks["focused_tests"] = False
            issues.append(f"{task_id}: baseline run lacks focused task test evidence")
        if require_focused_tests and not _focused_tests_recorded(
            k2_run,
            task_specs.get(task_id),
        ):
            checks["focused_tests"] = False
            issues.append(f"{task_id}: K2 treatment run lacks focused task test evidence")

    checks["decision_rule"] = signal.get("verdict") == "k2_wins"
    if not checks["decision_rule"]:
        issues.append(f"decision rule verdict is {signal.get('verdict')!r}, not 'k2_wins'")

    claim_ready = all(checks.values())
    return {
        "claim_ready": claim_ready,
        "baseline_arm": baseline_arm,
        "treatment_arm": treatment_arm,
        "checks": checks,
        "issues": issues,
        "signal": signal,
    }


def render_patch_scorecard_audit(audit: Mapping[str, Any]) -> str:
    """Render a concise Markdown audit for patch scorecard claim readiness."""

    signal = audit.get("signal") or {}
    lines = [
        "# Patch Scorecard Evidence Audit",
        "",
        f"- Claim ready: `{str(bool(audit.get('claim_ready'))).lower()}`",
        f"- Verdict: `{signal.get('verdict')}`",
        f"- Paired tasks: `{signal.get('paired_task_count')}`",
        f"- Pass-rate delta: `{_format_float(signal.get('pass_rate_delta'))}`",
        f"- Duration ratio: `{_format_float(signal.get('duration_ratio'))}`",
        "- Duration per accepted patch ratio: "
        f"`{_format_float(signal.get('duration_per_accepted_patch_ratio'))}`",
        f"- Token ratio: `{_format_float(signal.get('token_ratio'))}`",
        "- Tokens per accepted patch ratio: "
        f"`{_format_float(signal.get('token_per_accepted_patch_ratio'))}`",
        f"- Guide score delta: `{_format_float(signal.get('guide_guardrail_delta'))}`",
        "",
        "## Checks",
        "",
    ]
    for name, passed in sorted((audit.get("checks") or {}).items()):
        lines.append(f"- `{name}`: `{str(bool(passed)).lower()}`")
    issues = list(audit.get("issues") or [])
    if issues:
        lines.extend(["", "## Blocking Issues", ""])
        lines.extend(f"- {issue}" for issue in issues)
    return "\n".join(lines)


def render_patch_report(payload: Mapping[str, Any]) -> str:
    """Render a compact Markdown report for a patch-generation benchmark run."""

    summary = payload.get("summary", {})
    lines = [
        "# Patch-Generation Benchmark",
        "",
        f"Generated: `{payload.get('generated_at')}`",
        "",
        "## Summary",
        "",
        "| Arm | Tasks | Valid | Infra invalid | Passed | Mean score | Mean duration s | Mean total tokens | Mean guide score |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for arm in summary.get("arms", []):
        lines.append(
            "| {arm} | `{tasks}` | `{valid}` | `{invalid}` | `{passed}` | `{score}` | `{duration}` | `{tokens}` | `{guide}` |".format(
                arm=arm.get("arm_name"),
                tasks=arm.get("task_count"),
                valid=arm.get("valid_task_count", arm.get("task_count")),
                invalid=arm.get("infra_invalid_tasks", 0),
                passed=arm.get("passed_tasks"),
                score=_format_float(arm.get("mean_score")),
                duration=_format_float(arm.get("mean_duration_s")),
                tokens=_format_float(arm.get("mean_total_tokens")),
                guide=_format_float(arm.get("mean_guide_guardrail_score")),
            )
        )
    signal = summary.get("signal") or {}
    if signal:
        lines.extend(
            [
                "",
                "## Decision Rule",
                "",
                f"- Verdict: `{signal.get('verdict')}`",
                f"- Paired tasks: `{signal.get('paired_task_count')}` "
                f"(claim threshold: `{signal.get('min_tasks_for_claim')}`)",
                f"- Pass-rate delta ({signal.get('treatment_arm')} minus "
                f"{signal.get('baseline_arm')}): `{_format_float(signal.get('pass_rate_delta'))}`",
                f"- Duration ratio: `{_format_float(signal.get('duration_ratio'))}`",
                "- Duration per accepted patch ratio: "
                f"`{_format_float(signal.get('duration_per_accepted_patch_ratio'))}`",
                f"- Token ratio: `{_format_float(signal.get('token_ratio'))}`",
                "- Tokens per accepted patch ratio: "
                f"`{_format_float(signal.get('token_per_accepted_patch_ratio'))}`",
                f"- Token-savings threshold met: `{str(bool(signal.get('token_savings_ok'))).lower()}`",
                "- Usable-output efficiency threshold met: "
                f"`{str(bool(signal.get('usable_output_efficiency_ok'))).lower()}`",
                f"- Guide score delta: `{_format_float(signal.get('guide_guardrail_delta'))}`",
                f"- Guide threshold met: `{str(bool(signal.get('guide_guardrail_ok'))).lower()}`",
                "",
            ]
        )
    if summary.get("by_task_class"):
        lines.extend(
            [
                "## Task-Class Split",
                "",
                "| Task class | Arm | Tasks | Passed | Pass rate | Mean score |",
                "| --- | --- | ---: | ---: | ---: | ---: |",
            ]
        )
        for row in summary.get("by_task_class", []):
            lines.append(
                "| {task_class} | {arm} | `{tasks}` | `{passed}` | `{rate}` | `{score}` |".format(
                    task_class=row.get("task_class"),
                    arm=row.get("arm_name"),
                    tasks=row.get("task_count"),
                    passed=row.get("passed_tasks"),
                    rate=_format_float(row.get("pass_rate")),
                    score=_format_float(row.get("mean_score")),
                )
            )
        lines.append("")
    if summary.get("failure_categories"):
        lines.extend(
            [
                "## Failure Categories",
                "",
                "| Arm | Category | Count |",
                "| --- | --- | ---: |",
            ]
        )
        for row in summary.get("failure_categories", []):
            lines.append(
                f"| {row.get('arm_name')} | {row.get('category')} | `{row.get('count')}` |"
            )
        lines.append("")
    lines.extend(["", "## Per-Task Results", ""])
    for run in payload.get("runs", []):
        lines.extend(
            [
                f"### {run.get('title')} (`{run.get('task_id')}`)",
                "",
                f"- Arm: `{run.get('arm_name')}`",
                f"- Run status: `{run.get('run_status') or 'completed'}`",
                (
                    "- Infra failure reason: "
                    f"`{run.get('infra_failure_reason') or classify_codex_infra_failure(str(run.get('error') or ''))}`"
                ),
                f"- Score: `{_format_float(run.get('score'))}`",
                f"- Passed: `{str(run.get('passed')).lower()}`",
                f"- Duration seconds: `{_format_float(run.get('duration_s'))}`",
                f"- Token metrics: `{json.dumps(run.get('token_metrics') or {}, sort_keys=True)}`",
                f"- Changed files: `{json.dumps(run.get('changed_files') or [])}`",
                f"- Score breakdown: `{json.dumps(run.get('score_breakdown') or {}, sort_keys=True)}`",
                f"- Failure categories: `{json.dumps(run.get('failure_categories') or [])}`",
                "",
            ]
        )
    lines.extend(
        [
            "## Interpretation Notes",
            "",
            "- This benchmark compares generated patches, wall-clock time, and token usage.",
            "- Use `codex_repo_plus_guides_dump` as the fair vanilla baseline for customer claims about local code plus Confluence dumps.",
            "- Deterministic patch scores are not a substitute for human code review.",
            "- Test results should be treated as first-order evidence when task-specific tests are run.",
        ]
    )
    return "\n".join(lines)


def _string_tuple(values: Sequence[str]) -> tuple[str, ...]:
    return tuple(str(value) for value in values if str(value))


def _strip_diff_prefix(path: str) -> str:
    for prefix in ("a/", "b/"):
        if path.startswith(prefix):
            return path[len(prefix) :]
    return path


def _scope_score(changed_files: Sequence[str], allowed_prefixes: Sequence[str]) -> float | None:
    if not changed_files:
        return 0.0
    if not allowed_prefixes:
        return None
    in_scope = [
        path for path in changed_files if any(path.startswith(prefix) for prefix in allowed_prefixes)
    ]
    return len(in_scope) / len(changed_files)


def _out_of_scope_files(
    changed_files: Sequence[str], allowed_prefixes: Sequence[str]
) -> list[str]:
    if not allowed_prefixes:
        return []
    return [
        path
        for path in changed_files
        if not any(path.startswith(prefix) for prefix in allowed_prefixes)
    ]


def _verification_score(results: Sequence[Mapping[str, Any]]) -> float | None:
    if not results:
        return None
    return sum(1 for result in results if result.get("passed")) / len(results)


def _framework_import_prefix(framework: str) -> str:
    if framework == "flink":
        return "org.apache.flink."
    if framework == "kafka":
        return "org.apache.kafka."
    return ""


def _should_check_project_import(imported: str, import_prefix: str) -> bool:
    if not imported.startswith(import_prefix) or imported.endswith(".*"):
        return False
    # Flink shaded packages are dependency relocation namespaces, not source
    # files in the checked-out modules.
    if imported.startswith("org.apache.flink.shaded."):
        return False
    return True


def _java_source_roots(worktree: Path) -> tuple[Path, ...]:
    roots = []
    for path in worktree.rglob("src"):
        for suffix in ("main/java", "test/java"):
            candidate = path / suffix
            if candidate.is_dir():
                roots.append(candidate)
    return tuple(roots)


def _java_imports(text: str) -> list[str]:
    imports = []
    for match in re.finditer(r"^\s*import\s+(?:static\s+)?([A-Za-z_][\w.]*|\S+\.\*)\s*;", text, re.M):
        imports.append(match.group(1))
    return imports


def _import_resolves(imported: str, source_roots: Sequence[Path]) -> bool:
    parts = imported.split(".")
    # Nested classes are imported as package.Outer.Inner, so progressively
    # strip suffixes until a top-level Java file is found.
    for end in range(len(parts), 1, -1):
        candidate = Path(*parts[:end]).with_suffix(".java")
        if any((root / candidate).exists() for root in source_roots):
            return True
    return False


def _round_optional(value: float | None) -> float | None:
    return round(value, 6) if value is not None else None


def _walk_usage_dicts(value: Any) -> list[Mapping[str, Any]]:
    found: list[Mapping[str, Any]] = []
    if isinstance(value, Mapping):
        keys = set(value)
        if keys & {"input_tokens", "output_tokens", "total_tokens", "cached_input_tokens"}:
            found.append(value)
        for nested in value.values():
            found.extend(_walk_usage_dicts(nested))
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        for nested in value:
            found.extend(_walk_usage_dicts(nested))
    return found


def _tool_name_from_event(event: Mapping[str, Any]) -> str:
    item = event.get("item")
    if isinstance(item, Mapping):
        for key in ("tool", "tool_name", "name"):
            value = item.get(key)
            if isinstance(value, str) and value:
                item_type = item.get("type")
                if item_type is None or "tool" in str(item_type):
                    return value
    for key in ("tool", "tool_name", "name"):
        value = event.get(key)
        if isinstance(value, str) and value and "tool" in str(event.get("type", "")):
            return value
    return ""


def _failed_mcp_tool_name_from_event(event: Mapping[str, Any]) -> str:
    item = event.get("item")
    if not isinstance(item, Mapping):
        return ""
    if item.get("type") != "mcp_tool_call":
        return ""
    tool_name = str(item.get("tool") or "")
    if not tool_name:
        return ""
    if item.get("status") == "failed" or item.get("error"):
        return tool_name
    result = item.get("result")
    if not isinstance(result, Mapping):
        return ""
    content = result.get("content")
    if not isinstance(content, Sequence) or isinstance(content, (str, bytes)):
        return ""
    for part in content:
        if not isinstance(part, Mapping):
            continue
        text = part.get("text")
        if isinstance(text, str) and "K2 MCP tool failed:" in text:
            return tool_name
    return ""


def _int_value(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str) and re.fullmatch(r"\d+", value):
        return int(value)
    return None


def _pass_rate(runs: Sequence[Mapping[str, Any]]) -> float:
    if not runs:
        return 0.0
    return sum(1 for run in runs if run.get("passed")) / len(runs)


def _duration_per_accepted_patch(runs: Sequence[Mapping[str, Any]]) -> float | None:
    passed = sum(1 for run in runs if run.get("passed"))
    if not passed:
        return None
    durations = [
        float(run["duration_s"])
        for run in runs
        if isinstance(run.get("duration_s"), (int, float))
    ]
    if not durations:
        return None
    return round(sum(durations) / passed, 6)


def _tokens_per_accepted_patch(runs: Sequence[Mapping[str, Any]]) -> float | None:
    passed = sum(1 for run in runs if run.get("passed"))
    if not passed:
        return None
    token_counts = [
        int((run.get("token_metrics") or {}).get("total_tokens") or 0)
        for run in runs
        if int((run.get("token_metrics") or {}).get("total_tokens") or 0) > 0
    ]
    if not token_counts:
        return None
    return round(sum(token_counts) / passed, 6)


def _summaries_by_key(
    runs: Sequence[Mapping[str, Any]],
    key: str,
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for run in runs:
        group_value = str(run.get(key) or "unknown")
        arm_name = str(run.get("arm_name") or "")
        if not arm_name:
            continue
        grouped.setdefault((group_value, arm_name), []).append(run)
    rows = []
    for (group_value, arm_name), group_runs in sorted(grouped.items()):
        valid_group_runs = [run for run in group_runs if not is_infra_invalid_run(run)]
        scores = [float(run.get("score") or 0.0) for run in valid_group_runs]
        rows.append(
            {
                key: group_value,
                "arm_name": arm_name,
                "task_count": len(group_runs),
                "valid_task_count": len(valid_group_runs),
                "infra_invalid_tasks": len(group_runs) - len(valid_group_runs),
                "passed_tasks": sum(1 for run in valid_group_runs if run.get("passed")),
                "pass_rate": round(_pass_rate(valid_group_runs), 6),
                "mean_score": _mean(scores),
            }
        )
    return rows


def classify_codex_infra_failure(error_text: str | None) -> str:
    """Return a stable infra-failure reason for Codex transport errors."""

    if not error_text:
        return ""
    normalized = _normalize_text(error_text)
    for reason, markers in CODEX_INFRA_FAILURE_PATTERNS:
        if any(marker in normalized for marker in markers):
            return reason
    return ""


def is_infra_invalid_run(run: Mapping[str, Any]) -> bool:
    """Whether a run should be excluded from claim-grade scoring."""

    if str(run.get("run_status") or "") == "infra_invalid":
        return True
    if classify_codex_infra_failure(str(run.get("error") or "")):
        return True
    categories = run.get("failure_categories") or []
    return any(str(category) == "codex_infra_failure" for category in categories)


def merge_patch_scorecard_payloads(
    payloads: Sequence[Mapping[str, Any]],
    *,
    prefer_later: bool = True,
) -> dict[str, Any]:
    """Merge scorecards, replacing earlier task/arm rows with retry rows."""

    if not payloads:
        raise ValueError("at least one scorecard payload is required")
    merged: dict[str, Any] = dict(payloads[0])
    task_rows: dict[str, Mapping[str, Any]] = {}
    run_rows: dict[tuple[str, str], Mapping[str, Any]] = {}
    for payload in payloads:
        for task in payload.get("tasks") or []:
            if isinstance(task, Mapping) and task.get("task_id"):
                task_rows[str(task["task_id"])] = task
        for run in payload.get("runs") or []:
            if not isinstance(run, Mapping):
                continue
            key = (str(run.get("task_id") or ""), str(run.get("arm_name") or ""))
            if not key[0] or not key[1]:
                continue
            existing = run_rows.get(key)
            if existing is None:
                run_rows[key] = run
                continue
            current_invalid = is_infra_invalid_run(existing)
            retry_invalid = is_infra_invalid_run(run)
            if (current_invalid and not retry_invalid) or (prefer_later and not retry_invalid):
                run_rows[key] = run
    runs = list(run_rows.values())
    merged["tasks"] = list(task_rows.values())
    merged["runs"] = runs
    merged["summary"] = summarize_patch_scorecard(runs)
    merged["preflight"] = _merged_preflight(payloads)
    merged["merged_from"] = [payload.get("run_id") for payload in payloads if payload.get("run_id")]
    return merged


def _merged_preflight(payloads: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    successful_k2_probe: dict[str, Any] | None = None
    for payload in payloads:
        preflight = payload.get("preflight")
        if not isinstance(preflight, Mapping):
            continue
        for key, value in preflight.items():
            if key != "k2_probe":
                merged[key] = value
        k2_probe = preflight.get("k2_probe")
        if isinstance(k2_probe, Mapping) and (_int_value(k2_probe.get("result_count")) or 0) > 0:
            successful_k2_probe = dict(k2_probe)
        elif "k2_probe" not in merged:
            merged["k2_probe"] = k2_probe
    if successful_k2_probe is not None:
        merged["k2_probe"] = successful_k2_probe
    return merged


def _failure_category_counts(runs: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    counts: dict[tuple[str, str], int] = {}
    for run in runs:
        arm_name = str(run.get("arm_name") or "")
        if not arm_name:
            continue
        categories = run.get("failure_categories") or []
        if is_infra_invalid_run(run):
            categories = sorted({*categories, "codex_infra_failure"})
        if not categories and not run.get("passed"):
            categories = ["unclassified_failure"]
        for category in categories:
            counts[(arm_name, str(category))] = counts.get((arm_name, str(category)), 0) + 1
    return [
        {"arm_name": arm_name, "category": category, "count": count}
        for (arm_name, category), count in sorted(counts.items())
    ]


def _mean(values: Sequence[float | int]) -> float:
    if not values:
        return 0.0
    return round(sum(float(value) for value in values) / len(values), 6)


def _mean_optional(values: Sequence[float | int]) -> float | None:
    if not values:
        return None
    return _mean(values)


def _runs_by_task(
    runs: Sequence[Mapping[str, Any]],
    arm_name: str,
) -> dict[str, Mapping[str, Any]]:
    return {
        str(run.get("task_id")): run
        for run in runs
        if run.get("arm_name") == arm_name and run.get("task_id")
    }


def _k2_probe_from_payload(payload: Mapping[str, Any]) -> Mapping[str, Any] | None:
    preflight = payload.get("preflight")
    if isinstance(preflight, Mapping) and isinstance(preflight.get("k2_probe"), Mapping):
        return preflight["k2_probe"]
    if isinstance(payload.get("k2_probe"), Mapping):
        return payload["k2_probe"]
    return None


def _task_specs_by_id(payload: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    tasks = payload.get("tasks") or []
    if not isinstance(tasks, Sequence) or isinstance(tasks, (str, bytes)):
        return {}
    return {
        str(task.get("task_id")): task
        for task in tasks
        if isinstance(task, Mapping) and task.get("task_id")
    }


def _has_k2_tool_call(token_metrics: Mapping[str, Any]) -> bool:
    tool_counts = token_metrics.get("tool_counts") or {}
    if not isinstance(tool_counts, Mapping):
        return False
    for tool_name, count in tool_counts.items():
        if str(tool_name).startswith("k2_") and (_int_value(count) or 0) > 0:
            return True
    return False


def _focused_tests_recorded(
    run: Mapping[str, Any],
    task_spec: Mapping[str, Any] | None,
) -> bool:
    if not task_spec:
        return False
    commands = task_spec.get("verification_commands") or []
    if not isinstance(commands, Sequence) or isinstance(commands, (str, bytes)):
        return False
    expected_commands = {
        str(command.get("name"))
        for command in commands
        if isinstance(command, Mapping) and command.get("name")
    }
    if not expected_commands:
        return True
    verification_results = run.get("verification_results") or []
    if not isinstance(verification_results, Sequence) or isinstance(
        verification_results,
        (str, bytes),
    ):
        return False
    recorded_commands = {
        str(result.get("name"))
        for result in verification_results
        if isinstance(result, Mapping) and result.get("name")
    }
    return bool(expected_commands & recorded_commands)


def _format_float(value: Any) -> str:
    if isinstance(value, (int, float)):
        return f"{float(value):.6f}".rstrip("0").rstrip(".")
    return ""


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.lower())


__all__ = [
    "PATCH_ARM_NAMES",
    "PatchTask",
    "VerificationCommand",
    "assess_feature_development_signal",
    "classify_codex_infra_failure",
    "classify_patch_failure",
    "extract_changed_files",
    "extract_codex_usage_metrics",
    "is_infra_invalid_run",
    "merge_patch_scorecard_payloads",
    "patch_generation_prompt",
    "patch_tasks",
    "render_patch_report",
    "render_patch_scorecard_audit",
    "score_patch_run",
    "summarize_patch_scorecard",
    "validate_local_java_imports",
    "verify_patch_scorecard_evidence",
]
