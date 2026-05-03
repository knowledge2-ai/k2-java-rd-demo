"""Reusable offline evaluation cases for the Java R&D demo."""

from __future__ import annotations

from typing import Any

from .evaluation import EvalCase, ExpectedArtifact

FLINK_REPO = "apache/flink"
FLINK_REF = "release-2.2.0"
KAFKA_CODE_REPO = "apache/kafka"
KAFKA_DOCS_REPO = "apache/kafka-site"
KAFKA_REF = "4.2"


def _repo_uri(repo: str, repo_ref: str, path: str) -> str:
    return f"repo://{repo}@{repo_ref}/{path}"


FLINK_REST_DOC_URI = _repo_uri(FLINK_REPO, FLINK_REF, "docs/content/docs/ops/rest_api.md")
FLINK_DISPATCHER_ENDPOINT_URI = _repo_uri(
    FLINK_REPO,
    FLINK_REF,
    "flink-runtime/src/main/java/org/apache/flink/runtime/dispatcher/DispatcherRestEndpoint.java",
)
FLINK_JOB_DETAILS_HANDLER_URI = _repo_uri(
    FLINK_REPO,
    FLINK_REF,
    "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandler.java",
)
FLINK_JOB_DETAILS_HANDLER_TEST_URI = _repo_uri(
    FLINK_REPO,
    FLINK_REF,
    "flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/job/"
    "JobDetailsHandlerTest.java",
)

FLINK_UPGRADE_DOC_URI = _repo_uri(
    FLINK_REPO, FLINK_REF, "docs/content/release-notes/flink-2.2.md"
)
FLINK_CHECKPOINTING_DOC_URI = _repo_uri(
    FLINK_REPO,
    FLINK_REF,
    "docs/content/docs/dev/datastream/fault-tolerance/checkpointing.md",
)
FLINK_CHECKPOINT_COORDINATOR_URI = _repo_uri(
    FLINK_REPO,
    FLINK_REF,
    "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinator.java",
)
FLINK_CHECKPOINT_COORDINATOR_TEST_URI = _repo_uri(
    FLINK_REPO,
    FLINK_REF,
    "flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java",
)

KAFKA_CONNECT_DOC_URI = _repo_uri(
    KAFKA_DOCS_REPO,
    KAFKA_REF,
    "42/kafka-connect/connector-development-guide/index.html",
)
KAFKA_CONNECTOR_PLUGINS_RESOURCE_URI = _repo_uri(
    KAFKA_CODE_REPO,
    KAFKA_REF,
    "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/resources/"
    "ConnectorPluginsResource.java",
)
KAFKA_ABSTRACT_HERDER_URI = _repo_uri(
    KAFKA_CODE_REPO,
    KAFKA_REF,
    "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/AbstractHerder.java",
)
KAFKA_CONFIG_DEF_URI = _repo_uri(
    KAFKA_CODE_REPO,
    KAFKA_REF,
    "clients/src/main/java/org/apache/kafka/common/config/ConfigDef.java",
)
KAFKA_CONNECTOR_PLUGINS_RESOURCE_TEST_URI = _repo_uri(
    KAFKA_CODE_REPO,
    KAFKA_REF,
    "connect/runtime/src/test/java/org/apache/kafka/connect/runtime/rest/resources/"
    "ConnectorPluginsResourceTest.java",
)


_FLINK_CASES = (
    EvalCase(
        case_id="flink-rest-handler-controller-analogue",
        title="Flink REST handler controller analogue",
        query=(
            "A customer wants to add a controller-like REST endpoint to Flink. "
            "Which docs, handler classes, route registration code, and tests should guide the change?"
        ),
        expected_artifacts=(
            ExpectedArtifact(
                key="flink REST API docs",
                source_uri=None,
                source_kind="docs",
                module="docs",
                api_surface="rest",
                path_contains="rest_api",
                text_contains=("REST API",),
            ),
            ExpectedArtifact(
                key="dispatcher route registration",
                source_uri=FLINK_DISPATCHER_ENDPOINT_URI,
                source_kind="code",
                module="flink-runtime",
                api_surface="rest",
                class_name="DispatcherRestEndpoint",
                text_contains=("initializeHandlers", "route"),
            ),
            ExpectedArtifact(
                key="neighboring REST handler",
                source_uri=FLINK_JOB_DETAILS_HANDLER_URI,
                source_kind="code",
                module="flink-runtime",
                api_surface="rest",
                class_name="JobDetailsHandler",
                text_contains=("AbstractRestHandler", "handleRequest"),
            ),
            ExpectedArtifact(
                key="neighboring REST handler test",
                source_uri=FLINK_JOB_DETAILS_HANDLER_TEST_URI,
                source_kind="test",
                module="flink-runtime",
                api_surface="rest",
                path_contains="JobDetailsHandlerTest.java",
            ),
        ),
        expected_source_kinds=("docs", "code", "test"),
        required_modules=("docs", "flink-runtime"),
        required_api_surfaces=("rest",),
        must_mentions=(
            "AbstractRestHandler",
            "DispatcherRestEndpoint",
            "route registration",
            "response body",
        ),
        hallucination_markers=(
            "@RestController",
            "Spring MVC",
            "JAX-RS resource",
            "MagicPlanner",
        ),
        pass_threshold=0.82,
    ),
    EvalCase(
        case_id="flink-2-2-upgrade-checkpointing-guidance",
        title="Flink 2.2 upgrade and checkpointing guidance",
        query=(
            "A customer is upgrading to Flink 2.2 and asks for version-specific checkpointing "
            "guidance. What release notes, checkpoint docs, runtime code, and tests should be cited?"
        ),
        expected_artifacts=(
            ExpectedArtifact(
                key="Flink 2.2 release notes",
                source_uri=None,
                source_kind="docs",
                module="docs",
                api_surface="checkpointing",
                path_contains="flink-2.2",
                text_contains=("Flink 2.2",),
                metadata_equals={"framework_version": "2.2.0"},
            ),
            ExpectedArtifact(
                key="checkpointing operations docs",
                source_uri=None,
                source_kind="docs",
                module="docs",
                api_surface="checkpointing",
                path_contains="checkpointing",
                text_contains=("checkpointing", "checkpoint storage"),
            ),
            ExpectedArtifact(
                key="checkpoint coordinator runtime code",
                source_uri=FLINK_CHECKPOINT_COORDINATOR_URI,
                source_kind="code",
                module="flink-runtime",
                api_surface="checkpointing",
                class_name="CheckpointCoordinator",
                text_contains=("triggerCheckpoint",),
            ),
            ExpectedArtifact(
                key="checkpoint coordinator regression tests",
                source_uri=FLINK_CHECKPOINT_COORDINATOR_TEST_URI,
                source_kind="test",
                module="flink-runtime",
                api_surface="checkpointing",
                path_contains="CheckpointCoordinatorTest.java",
            ),
        ),
        expected_source_kinds=("docs", "code", "test"),
        required_modules=("docs", "flink-runtime"),
        required_api_surfaces=("checkpointing",),
        must_mentions=(
            "Flink 2.2",
            "checkpointing",
            "checkpoint storage",
            "state backend",
            "savepoint compatibility",
        ),
        hallucination_markers=(
            "Flink 1.12",
            "FsStateBackend",
            "MemoryStateBackend",
            "disable checkpointing during upgrade",
        ),
        pass_threshold=0.82,
    ),
)

_KAFKA_CASES = (
    EvalCase(
        case_id="kafka-connect-validation-rule",
        title="Kafka Connect validation rule",
        query=(
            "A customer is adding a Kafka Connect connector validation rule. Which Connect REST "
            "docs, validation code paths, ConfigDef behavior, and tests should anchor the answer?"
        ),
        expected_artifacts=(
            ExpectedArtifact(
                key="Kafka Connect REST docs",
                source_uri=None,
                source_kind="docs",
                module="docs",
                api_surface="connect",
                path_contains="connector-development-guide",
                text_contains=("connector-plugins", "validate"),
            ),
            ExpectedArtifact(
                key="connector plugins validation resource",
                source_uri=KAFKA_CONNECTOR_PLUGINS_RESOURCE_URI,
                source_kind="code",
                module="connect",
                api_surface="rest",
                class_name="ConnectorPluginsResource",
                text_contains=("validateConfigs",),
            ),
            ExpectedArtifact(
                key="herder validation implementation",
                source_uri=KAFKA_ABSTRACT_HERDER_URI,
                source_kind="code",
                module="connect",
                api_surface="connect",
                path_contains="AbstractHerder.java",
                text_contains=("validateConnectorConfig",),
            ),
            ExpectedArtifact(
                key="ConfigDef validation semantics",
                source_uri=KAFKA_CONFIG_DEF_URI,
                source_kind="code",
                module="clients",
                api_surface="connect",
                path_contains="ConfigDef.java",
                text_contains=("ConfigValue",),
            ),
            ExpectedArtifact(
                key="connector plugins resource tests",
                source_uri=KAFKA_CONNECTOR_PLUGINS_RESOURCE_TEST_URI,
                source_kind="test",
                module="connect",
                api_surface="rest",
                path_contains="ConnectorPluginsResourceTest.java",
            ),
        ),
        expected_source_kinds=("docs", "code", "test"),
        required_modules=("docs", "connect", "clients"),
        required_api_surfaces=("connect",),
        must_mentions=(
            "connector-plugins",
            "validateConnectorConfig",
            "ConfigDef",
            "ConfigValue",
        ),
        hallucination_markers=(
            "Spring Validator",
            "Bean Validation",
            "javax.validation",
            "Schema Registry compatibility",
        ),
        pass_threshold=0.82,
    ),
)


def demo_eval_cases(*, include_kafka: bool = False) -> list[EvalCase]:
    """Return customer-story eval cases for the Java R&D demo."""

    cases = list(_FLINK_CASES)
    if include_kafka:
        cases.extend(_KAFKA_CASES)
    return cases


def demo_eval_case_dicts(*, include_kafka: bool = False) -> list[dict[str, Any]]:
    """Return the demo eval catalog in a JSON-serializable shape."""

    return [case.to_dict() for case in demo_eval_cases(include_kafka=include_kafka)]


def evaluation_cases(
    *,
    suite: str = "demo",
    include_kafka: bool = False,
) -> list[EvalCase]:
    """Return an evaluation case suite by name."""

    normalized = suite.strip().lower()
    if normalized == "demo":
        return demo_eval_cases(include_kafka=include_kafka)
    if normalized == "benchmark":
        from .benchmark_cases import benchmark_eval_cases

        return benchmark_eval_cases()
    raise ValueError("suite must be one of: demo, benchmark")


def evaluation_case_dicts(
    *,
    suite: str = "demo",
    include_kafka: bool = False,
) -> list[dict[str, Any]]:
    """Return an evaluation case suite in a JSON-serializable shape."""

    return [case.to_dict() for case in evaluation_cases(suite=suite, include_kafka=include_kafka)]


__all__ = [
    "demo_eval_case_dicts",
    "demo_eval_cases",
    "evaluation_case_dicts",
    "evaluation_cases",
]
