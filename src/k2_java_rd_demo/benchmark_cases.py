"""100-case benchmark catalog for the Java R&D demo.

The original demo cases are intentionally small and story-like. This module
defines a broader candidate suite so public-facing evaluation is not based on
three hand-picked questions.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .evaluation import EvalCase, ExpectedArtifact

FLINK_REPO = "apache/flink"
FLINK_REF = "release-2.2.0"
KAFKA_REPO = "apache/kafka"
KAFKA_REF = "4.2"


@dataclass(frozen=True)
class TopicSpec:
    slug: str
    title: str
    framework: str
    api_surface: str
    module: str
    class_name: str
    path: str
    task: str
    doc_path_contains: str
    doc_text_contains: tuple[str, ...]
    must_mentions: tuple[str, ...]
    hallucination_markers: tuple[str, ...]
    include_test: bool = True


def benchmark_eval_cases() -> list[EvalCase]:
    """Return the 100-case public benchmark candidate catalog."""

    return [_case_from_topic(topic) for topic in _TOPICS]


def benchmark_eval_case_dicts() -> list[dict[str, Any]]:
    """Return the benchmark eval catalog in a JSON-serializable shape."""

    return [case.to_dict() for case in benchmark_eval_cases()]


def _case_from_topic(topic: TopicSpec) -> EvalCase:
    anchors = (
        "version-pinned docs, implementation class, and neighboring tests"
        if topic.include_test
        else "version-pinned docs and implementation class"
    )
    source_uri = _source_uri(topic)
    expected_artifacts: list[ExpectedArtifact] = [
        ExpectedArtifact(
            key=f"{topic.framework} docs for {topic.title}",
            source_kind="docs",
            module="docs",
            api_surface=topic.api_surface,
            path_contains=topic.doc_path_contains,
            text_contains=topic.doc_text_contains,
            metadata_equals={"framework_version": _version(topic.framework)},
        ),
        ExpectedArtifact(
            key=f"{topic.class_name} source",
            source_uri=source_uri,
            source_kind="code",
            module=topic.module,
            api_surface=topic.api_surface,
            class_name=topic.class_name,
            path_contains=topic.path.rsplit("/", maxsplit=1)[-1],
            text_contains=(topic.class_name,),
        ),
    ]
    if topic.include_test:
        expected_artifacts.append(
            ExpectedArtifact(
                key=f"{topic.class_name} neighboring test",
                source_kind="test",
                module=topic.module,
                api_surface=topic.api_surface,
                path_contains=f"{topic.class_name}Test",
            )
        )

    return EvalCase(
        case_id=f"{topic.framework}-{topic.api_surface}-{topic.slug}",
        title=topic.title,
        query=(
            f"For {_question_scope(topic)} {_version(topic.framework)}, inspect "
            f"`{topic.class_name}`: {topic.task}. "
            f"Which {anchors} should anchor the answer?"
        ),
        expected_artifacts=tuple(expected_artifacts),
        expected_source_kinds=("docs", "code", "test") if topic.include_test else ("docs", "code"),
        required_modules=("docs", topic.module),
        required_api_surfaces=(topic.api_surface,),
        must_mentions=topic.must_mentions,
        hallucination_markers=topic.hallucination_markers,
        pass_threshold=0.82,
    )


def _source_uri(topic: TopicSpec) -> str:
    repo = FLINK_REPO if topic.framework == "flink" else KAFKA_REPO
    ref = FLINK_REF if topic.framework == "flink" else KAFKA_REF
    return f"repo://{repo}@{ref}/{topic.path}"


def _version(framework: str) -> str:
    return "2.2.0" if framework == "flink" else "4.2.0"


def _question_scope(topic: TopicSpec) -> str:
    if topic.framework == "kafka":
        return "Kafka Connect REST" if topic.api_surface == "rest" else "Kafka Connect"
    if topic.api_surface == "rest":
        return "Flink REST API"
    if topic.api_surface == "checkpointing":
        return "Flink checkpointing"
    return topic.framework.title()


def _flink_rest(
    slug: str,
    class_name: str,
    path: str,
    task: str,
    *,
    include_test: bool = True,
) -> TopicSpec:
    return TopicSpec(
        slug=slug,
        title=f"Flink REST pattern for {class_name}",
        framework="flink",
        api_surface="rest",
        module="flink-runtime",
        class_name=class_name,
        path=path,
        task=task,
        doc_path_contains="rest_api",
        doc_text_contains=("REST API",),
        must_mentions=("REST API", class_name, "route", "response"),
        hallucination_markers=("@RestController", "Spring MVC", "JAX-RS", "servlet"),
        include_test=include_test,
    )


def _flink_checkpoint(
    slug: str,
    class_name: str,
    path: str,
    task: str,
    *,
    module: str = "flink-runtime",
    include_test: bool = True,
) -> TopicSpec:
    return TopicSpec(
        slug=slug,
        title=f"Flink checkpointing pattern for {class_name}",
        framework="flink",
        api_surface="checkpointing",
        module=module,
        class_name=class_name,
        path=path,
        task=task,
        doc_path_contains="checkpoint",
        doc_text_contains=("checkpoint",),
        must_mentions=("checkpointing", class_name, "state", "savepoint"),
        hallucination_markers=(
            "FsStateBackend",
            "MemoryStateBackend",
            "disable checkpointing during upgrade",
        ),
        include_test=include_test,
    )


def _kafka_connect(
    slug: str,
    class_name: str,
    path: str,
    task: str,
    *,
    module: str = "connect",
    api_surface: str = "connect",
    include_test: bool = True,
) -> TopicSpec:
    return TopicSpec(
        slug=slug,
        title=f"Kafka Connect pattern for {class_name}",
        framework="kafka",
        api_surface=api_surface,
        module=module,
        class_name=class_name,
        path=path,
        task=task,
        doc_path_contains="connect",
        doc_text_contains=("connect",),
        must_mentions=_kafka_must_mentions(
            class_name=class_name,
            task=task,
            api_surface=api_surface,
        ),
        hallucination_markers=("Spring Validator", "Bean Validation", "javax.validation"),
        include_test=include_test,
    )


def _kafka_must_mentions(*, class_name: str, task: str, api_surface: str) -> tuple[str, ...]:
    topic_text = f"{class_name} {task}".lower()
    task_text = task.lower()
    mentions = ["Kafka Connect", class_name]
    if api_surface == "rest":
        mentions.append("REST")
    elif "plugin" in topic_text:
        mentions.append("plugin")
    elif "valid" in task_text:
        mentions.append("validation")
    elif "config" in topic_text:
        mentions.append("configuration")
    elif "schema" in topic_text:
        mentions.append("schema")
    elif "record" in topic_text:
        mentions.append("record")
    else:
        mentions.append("connector")
    return tuple(mentions)


_FLINK_REST_TOPICS = (
    _flink_rest(
        "dispatcher-rest-endpoint",
        "DispatcherRestEndpoint",
        "flink-runtime/src/main/java/org/apache/flink/runtime/dispatcher/DispatcherRestEndpoint.java",
        "identify where dispatcher REST handlers are registered",
    ),
    _flink_rest(
        "web-monitor-endpoint",
        "WebMonitorEndpoint",
        "flink-runtime/src/main/java/org/apache/flink/runtime/webmonitor/WebMonitorEndpoint.java",
        "explain how the web monitor endpoint wires REST handlers",
    ),
    _flink_rest(
        "rest-server-endpoint",
        "RestServerEndpoint",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/RestServerEndpoint.java",
        "trace the abstract REST endpoint lifecycle",
    ),
    _flink_rest(
        "abstract-rest-handler",
        "AbstractRestHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/AbstractRestHandler.java",
        "implement a request handler with the correct response-body contract",
    ),
    _flink_rest(
        "job-details-handler",
        "JobDetailsHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobDetailsHandler.java",
        "use a neighboring job REST handler as an implementation analogue",
    ),
    _flink_rest(
        "job-config-handler",
        "JobConfigHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobConfigHandler.java",
        "inspect how job configuration is exposed through REST",
    ),
    _flink_rest(
        "job-exceptions-handler",
        "JobExceptionsHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobExceptionsHandler.java",
        "inspect exception response handling for a job endpoint",
    ),
    _flink_rest(
        "job-accumulators-handler",
        "JobAccumulatorsHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobAccumulatorsHandler.java",
        "inspect accumulator response construction for a job endpoint",
    ),
    _flink_rest(
        "job-plan-handler",
        "JobPlanHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobPlanHandler.java",
        "explain how plan metadata is returned through a REST handler",
    ),
    _flink_rest(
        "job-vertex-details-handler",
        "JobVertexDetailsHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobVertexDetailsHandler.java",
        "inspect a vertex-scoped REST endpoint implementation",
    ),
    _flink_rest(
        "job-vertex-taskmanagers-handler",
        "JobVertexTaskManagersHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobVertexTaskManagersHandler.java",
        "inspect task-manager detail routing for a job vertex",
    ),
    _flink_rest(
        "job-cancellation-handler",
        "JobCancellationHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobCancellationHandler.java",
        "trace cancellation request handling and response behavior",
    ),
    _flink_rest(
        "savepoint-handlers",
        "SavepointHandlers",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/savepoints/SavepointHandlers.java",
        "trace savepoint trigger and polling REST behavior",
    ),
    _flink_rest(
        "checkpoint-handlers",
        "CheckpointHandlers",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/checkpoints/CheckpointHandlers.java",
        "trace checkpoint trigger and status REST behavior",
    ),
    _flink_rest(
        "job-resource-requirements-update-handler",
        "JobResourceRequirementsUpdateHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobResourceRequirementsUpdateHandler.java",
        "inspect request-body validation for job resource requirement updates",
    ),
    _flink_rest(
        "job-submit-handler",
        "JobSubmitHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobSubmitHandler.java",
        "inspect job submission request handling",
    ),
    _flink_rest(
        "file-uploads",
        "FileUploads",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/FileUploads.java",
        "inspect uploaded-file tracking for REST requests",
    ),
    _flink_rest(
        "dashboard-config-handler",
        "DashboardConfigHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/cluster/DashboardConfigHandler.java",
        "inspect cluster dashboard configuration responses",
    ),
    _flink_rest(
        "cluster-overview-handler",
        "ClusterOverviewHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/cluster/ClusterOverviewHandler.java",
        "inspect cluster overview response construction",
    ),
    _flink_rest(
        "taskmanagers-handler",
        "TaskManagersHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagersHandler.java",
        "inspect task-manager collection response handling",
    ),
    _flink_rest(
        "taskmanager-details-handler",
        "TaskManagerDetailsHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/taskmanager/TaskManagerDetailsHandler.java",
        "inspect task-manager detail lookup behavior",
    ),
    _flink_rest(
        "job-vertex-back-pressure-handler",
        "JobVertexBackPressureHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobVertexBackPressureHandler.java",
        "inspect back-pressure endpoint behavior for job vertices",
    ),
    _flink_rest(
        "job-vertex-watermarks-handler",
        "JobVertexWatermarksHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/metrics/JobVertexWatermarksHandler.java",
        "inspect watermark reporting through REST",
    ),
    _flink_rest(
        "subtask-current-attempt-details-handler",
        "SubtaskCurrentAttemptDetailsHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/SubtaskCurrentAttemptDetailsHandler.java",
        "inspect subtask-attempt details routing",
    ),
    _flink_rest(
        "job-vertex-flame-graph-handler",
        "JobVertexFlameGraphHandler",
        "flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/job/JobVertexFlameGraphHandler.java",
        "inspect flame-graph endpoint behavior for job vertices",
    ),
)

_FLINK_CHECKPOINT_TOPICS = (
    _flink_checkpoint(
        "checkpoint-coordinator",
        "CheckpointCoordinator",
        "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinator.java",
        "trace checkpoint triggering and coordinator responsibilities",
    ),
    _flink_checkpoint(
        "pending-checkpoint",
        "PendingCheckpoint",
        "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/PendingCheckpoint.java",
        "explain pending checkpoint state transitions",
    ),
    _flink_checkpoint(
        "completed-checkpoint",
        "CompletedCheckpoint",
        "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CompletedCheckpoint.java",
        "explain completed checkpoint metadata and lifecycle",
    ),
    _flink_checkpoint(
        "completed-checkpoint-store",
        "CompletedCheckpointStore",
        "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CompletedCheckpointStore.java",
        "inspect how completed checkpoints are retained",
    ),
    _flink_checkpoint(
        "default-completed-checkpoint-store",
        "DefaultCompletedCheckpointStore",
        "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCompletedCheckpointStore.java",
        "inspect default completed checkpoint retention behavior",
    ),
    _flink_checkpoint(
        "checkpoint-stats-tracker",
        "CheckpointStatsTracker",
        "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointStatsTracker.java",
        "explain checkpoint statistics tracking",
    ),
    _flink_checkpoint(
        "checkpoint-stats-snapshot",
        "CheckpointStatsSnapshot",
        "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointStatsSnapshot.java",
        "inspect checkpoint statistics snapshot behavior",
    ),
    _flink_checkpoint(
        "checkpoint-metrics",
        "CheckpointMetrics",
        "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointMetrics.java",
        "identify checkpoint metric fields used by reporting code",
    ),
    _flink_checkpoint(
        "checkpoint-properties",
        "CheckpointProperties",
        "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointProperties.java",
        "explain checkpoint property flags and savepoint behavior",
    ),
    _flink_checkpoint(
        "checkpoint-retention-policy",
        "CheckpointRetentionPolicy",
        "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointRetentionPolicy.java",
        "explain checkpoint retention policy choices",
    ),
    _flink_checkpoint(
        "checkpoint-id-counter",
        "CheckpointIDCounter",
        "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointIDCounter.java",
        "inspect checkpoint id allocation behavior",
    ),
    _flink_checkpoint(
        "standalone-checkpoint-id-counter",
        "StandaloneCheckpointIDCounter",
        "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/StandaloneCheckpointIDCounter.java",
        "inspect standalone checkpoint id allocation",
    ),
    _flink_checkpoint(
        "checkpoint-failure-manager",
        "CheckpointFailureManager",
        "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointFailureManager.java",
        "explain tolerated checkpoint failure handling",
    ),
    _flink_checkpoint(
        "checkpoint-plan-calculator",
        "CheckpointPlanCalculator",
        "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointPlanCalculator.java",
        "trace checkpoint plan calculation responsibilities",
    ),
    _flink_checkpoint(
        "default-checkpoint-plan-calculator",
        "DefaultCheckpointPlanCalculator",
        "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/DefaultCheckpointPlanCalculator.java",
        "inspect the default checkpoint plan calculation implementation",
    ),
    _flink_checkpoint(
        "checkpoint-request-decider",
        "CheckpointRequestDecider",
        "flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointRequestDecider.java",
        "explain checkpoint request scheduling decisions",
    ),
    _flink_checkpoint(
        "checkpoint-resources-cleanup-runner",
        "CheckpointResourcesCleanupRunner",
        "flink-runtime/src/main/java/org/apache/flink/runtime/dispatcher/cleanup/CheckpointResourcesCleanupRunner.java",
        "inspect checkpoint resource cleanup behavior",
    ),
    _flink_checkpoint(
        "checkpoint-storage-loader",
        "CheckpointStorageLoader",
        "flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageLoader.java",
        "explain checkpoint storage loading during configuration",
    ),
    _flink_checkpoint(
        "checkpoint-storage-coordinator-view",
        "CheckpointStorageCoordinatorView",
        "flink-runtime/src/main/java/org/apache/flink/runtime/state/CheckpointStorageCoordinatorView.java",
        "explain the coordinator-facing checkpoint storage contract",
    ),
    _flink_checkpoint(
        "state-backend",
        "StateBackend",
        "flink-runtime/src/main/java/org/apache/flink/runtime/state/StateBackend.java",
        "explain state backend responsibilities during checkpointing",
    ),
    _flink_checkpoint(
        "operator-state-backend",
        "OperatorStateBackend",
        "flink-runtime/src/main/java/org/apache/flink/runtime/state/OperatorStateBackend.java",
        "inspect operator-state checkpointing responsibilities",
    ),
    _flink_checkpoint(
        "keyed-state-backend",
        "KeyedStateBackend",
        "flink-runtime/src/main/java/org/apache/flink/runtime/state/KeyedStateBackend.java",
        "inspect keyed-state checkpointing responsibilities",
    ),
    _flink_checkpoint(
        "savepoint-restore-settings",
        "SavepointRestoreSettings",
        "flink-runtime/src/main/java/org/apache/flink/runtime/jobgraph/SavepointRestoreSettings.java",
        "explain savepoint restore settings during upgrades",
    ),
    _flink_checkpoint(
        "savepoint-format-type",
        "SavepointFormatType",
        "flink-core/src/main/java/org/apache/flink/core/execution/SavepointFormatType.java",
        "explain savepoint format choices",
        module="flink-core",
    ),
    _flink_checkpoint(
        "checkpoint-coordinator-configuration",
        "CheckpointCoordinatorConfiguration",
        "flink-runtime/src/main/java/org/apache/flink/runtime/jobgraph/tasks/CheckpointCoordinatorConfiguration.java",
        "inspect checkpoint coordinator configuration options",
    ),
)

_KAFKA_CONNECT_TOPICS = (
    _kafka_connect(
        "connector-plugins-resource",
        "ConnectorPluginsResource",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/resources/ConnectorPluginsResource.java",
        "trace connector plugin validation through the REST resource",
        api_surface="rest",
    ),
    _kafka_connect(
        "abstract-herder",
        "AbstractHerder",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/AbstractHerder.java",
        "trace connector configuration validation in the herder layer",
    ),
    _kafka_connect(
        "distributed-herder",
        "DistributedHerder",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/distributed/DistributedHerder.java",
        "inspect distributed connector config update behavior",
    ),
    _kafka_connect(
        "standalone-herder",
        "StandaloneHerder",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/standalone/StandaloneHerder.java",
        "inspect standalone connector config update behavior",
    ),
    _kafka_connect(
        "herder",
        "Herder",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/Herder.java",
        "identify the connector management interface",
    ),
    _kafka_connect(
        "worker",
        "Worker",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/Worker.java",
        "trace connector and task lifecycle responsibilities",
    ),
    _kafka_connect(
        "worker-connector",
        "WorkerConnector",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConnector.java",
        "inspect connector startup and failure handling",
    ),
    _kafka_connect(
        "worker-task",
        "WorkerTask",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerTask.java",
        "inspect common task lifecycle behavior",
    ),
    _kafka_connect(
        "worker-sink-task",
        "WorkerSinkTask",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSinkTask.java",
        "inspect sink task delivery and commit behavior",
    ),
    _kafka_connect(
        "worker-source-task",
        "WorkerSourceTask",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerSourceTask.java",
        "inspect source task polling and commit behavior",
    ),
    _kafka_connect(
        "connector-config",
        "ConnectorConfig",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/ConnectorConfig.java",
        "explain shared connector configuration validation",
    ),
    _kafka_connect(
        "sink-connector-config",
        "SinkConnectorConfig",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/SinkConnectorConfig.java",
        "inspect sink connector-specific config validation",
    ),
    _kafka_connect(
        "source-connector-config",
        "SourceConnectorConfig",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/SourceConnectorConfig.java",
        "inspect source connector-specific config validation",
    ),
    _kafka_connect(
        "worker-config",
        "WorkerConfig",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/WorkerConfig.java",
        "inspect worker-level configuration parsing",
    ),
    _kafka_connect(
        "distributed-config",
        "DistributedConfig",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/distributed/DistributedConfig.java",
        "inspect distributed worker configuration behavior",
    ),
    _kafka_connect(
        "standalone-config",
        "StandaloneConfig",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/standalone/StandaloneConfig.java",
        "inspect standalone worker configuration behavior",
    ),
    _kafka_connect(
        "config-def",
        "ConfigDef",
        "clients/src/main/java/org/apache/kafka/common/config/ConfigDef.java",
        "explain Kafka configuration definition and validation semantics",
        module="clients",
        include_test=False,
    ),
    _kafka_connect(
        "config-value",
        "ConfigValue",
        "clients/src/main/java/org/apache/kafka/common/config/ConfigValue.java",
        "explain validation result representation",
        module="clients",
        include_test=False,
    ),
    _kafka_connect(
        "config-transformer",
        "ConfigTransformer",
        "clients/src/main/java/org/apache/kafka/common/config/ConfigTransformer.java",
        "inspect externalized configuration transformation behavior",
        module="clients",
        include_test=False,
    ),
    _kafka_connect(
        "config-provider",
        "ConfigProvider",
        "clients/src/main/java/org/apache/kafka/common/config/provider/ConfigProvider.java",
        "inspect the config provider contract used for externalized secrets",
        module="clients",
        include_test=False,
    ),
    _kafka_connect(
        "plugins",
        "Plugins",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/Plugins.java",
        "trace plugin discovery and connector class loading",
    ),
    _kafka_connect(
        "plugin-desc",
        "PluginDesc",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/PluginDesc.java",
        "inspect plugin descriptor metadata",
    ),
    _kafka_connect(
        "plugin-type",
        "PluginType",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/PluginType.java",
        "inspect plugin type classification",
    ),
    _kafka_connect(
        "delegating-class-loader",
        "DelegatingClassLoader",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/DelegatingClassLoader.java",
        "inspect plugin classloader delegation behavior",
    ),
    _kafka_connect(
        "plugin-class-loader",
        "PluginClassLoader",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/PluginClassLoader.java",
        "inspect isolated plugin class loading",
    ),
    _kafka_connect(
        "plugin-scan-result",
        "PluginScanResult",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/PluginScanResult.java",
        "inspect plugin scanning results",
    ),
    _kafka_connect(
        "plugin-utils",
        "PluginUtils",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/isolation/PluginUtils.java",
        "inspect plugin path and alias helper behavior",
    ),
    _kafka_connect(
        "connect-rest-server",
        "ConnectRestServer",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/ConnectRestServer.java",
        "trace Connect REST server wiring",
        api_surface="rest",
    ),
    _kafka_connect(
        "rest-server-config",
        "RestServerConfig",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/RestServerConfig.java",
        "inspect Connect REST server configuration",
        api_surface="rest",
    ),
    _kafka_connect(
        "connectors-resource",
        "ConnectorsResource",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/resources/ConnectorsResource.java",
        "trace connector CRUD REST behavior",
        api_surface="rest",
    ),
    _kafka_connect(
        "connector-state-info",
        "ConnectorStateInfo",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/entities/ConnectorStateInfo.java",
        "inspect connector state response representation",
        api_surface="rest",
        include_test=False,
    ),
    _kafka_connect(
        "connector-info",
        "ConnectorInfo",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/entities/ConnectorInfo.java",
        "inspect connector info response representation",
        api_surface="rest",
        include_test=False,
    ),
    _kafka_connect(
        "create-connector-request",
        "CreateConnectorRequest",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/entities/CreateConnectorRequest.java",
        "inspect connector creation request validation",
        api_surface="rest",
    ),
    _kafka_connect(
        "connector-type",
        "ConnectorType",
        "connect/runtime/src/main/java/org/apache/kafka/connect/runtime/rest/entities/ConnectorType.java",
        "inspect connector type classification",
        api_surface="rest",
    ),
    _kafka_connect(
        "connector",
        "Connector",
        "connect/api/src/main/java/org/apache/kafka/connect/connector/Connector.java",
        "inspect the base connector contract",
    ),
    _kafka_connect(
        "source-connector",
        "SourceConnector",
        "connect/api/src/main/java/org/apache/kafka/connect/source/SourceConnector.java",
        "inspect source connector implementation responsibilities",
    ),
    _kafka_connect(
        "sink-connector",
        "SinkConnector",
        "connect/api/src/main/java/org/apache/kafka/connect/sink/SinkConnector.java",
        "inspect sink connector implementation responsibilities",
    ),
    _kafka_connect(
        "transformation",
        "Transformation",
        "connect/api/src/main/java/org/apache/kafka/connect/transforms/Transformation.java",
        "inspect single-message transform behavior",
    ),
    _kafka_connect(
        "header-converter",
        "HeaderConverter",
        "connect/api/src/main/java/org/apache/kafka/connect/storage/HeaderConverter.java",
        "inspect header conversion behavior",
    ),
    _kafka_connect(
        "converter",
        "Converter",
        "connect/api/src/main/java/org/apache/kafka/connect/storage/Converter.java",
        "inspect value/key conversion behavior",
    ),
    _kafka_connect(
        "schemas",
        "Schema",
        "connect/api/src/main/java/org/apache/kafka/connect/data/Schema.java",
        "inspect Connect schema representation",
    ),
    _kafka_connect(
        "schema-builder",
        "SchemaBuilder",
        "connect/api/src/main/java/org/apache/kafka/connect/data/SchemaBuilder.java",
        "inspect Connect schema construction behavior",
    ),
    _kafka_connect(
        "struct",
        "Struct",
        "connect/api/src/main/java/org/apache/kafka/connect/data/Struct.java",
        "inspect structured Connect data validation",
    ),
    _kafka_connect(
        "sink-record",
        "SinkRecord",
        "connect/api/src/main/java/org/apache/kafka/connect/sink/SinkRecord.java",
        "inspect sink record metadata available to connectors",
    ),
    _kafka_connect(
        "source-record",
        "SourceRecord",
        "connect/api/src/main/java/org/apache/kafka/connect/source/SourceRecord.java",
        "inspect source record construction and partition metadata",
    ),
    _kafka_connect(
        "connector-client-config-request",
        "ConnectorClientConfigRequest",
        "connect/api/src/main/java/org/apache/kafka/connect/connector/policy/ConnectorClientConfigRequest.java",
        "inspect connector client override policy inputs",
    ),
    _kafka_connect(
        "connector-client-config-override-policy",
        "ConnectorClientConfigOverridePolicy",
        "connect/api/src/main/java/org/apache/kafka/connect/connector/policy/ConnectorClientConfigOverridePolicy.java",
        "inspect connector client override validation behavior",
    ),
    _kafka_connect(
        "abstract-connector-client-config-override-policy",
        "AbstractConnectorClientConfigOverridePolicy",
        "connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/AbstractConnectorClientConfigOverridePolicy.java",
        "inspect shared connector client override policy behavior",
    ),
    _kafka_connect(
        "none-connector-client-config-override-policy",
        "NoneConnectorClientConfigOverridePolicy",
        "connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/NoneConnectorClientConfigOverridePolicy.java",
        "inspect policy behavior when overrides are not allowed",
    ),
    _kafka_connect(
        "principal-connector-client-config-override-policy",
        "PrincipalConnectorClientConfigOverridePolicy",
        "connect/runtime/src/main/java/org/apache/kafka/connect/connector/policy/PrincipalConnectorClientConfigOverridePolicy.java",
        "inspect principal-only client override validation behavior",
    ),
)

_TOPICS = (*_FLINK_REST_TOPICS, *_FLINK_CHECKPOINT_TOPICS, *_KAFKA_CONNECT_TOPICS)

if len(_TOPICS) != 100:  # pragma: no cover - import-time guard for future edits.
    raise RuntimeError(f"benchmark catalog must contain 100 cases, found {len(_TOPICS)}")


__all__ = ["benchmark_eval_case_dicts", "benchmark_eval_cases"]
