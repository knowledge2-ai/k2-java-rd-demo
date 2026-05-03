# Per-Question Benchmark Statistics

## Aggregate Summary

- Cases: `100`
- Baseline `codex_without_k2`: combined=0.189375, retrieval=0, answer=0.37875, safety=1, answered `100/100`, passed `0/100`
- K2-assisted `codex_with_k2_real_mcp`: combined=0.928875, retrieval=0.954, answer=0.90375, safety=1, answered `100/100`, passed `93/100`
- `passed` means the answer cleared the deterministic evidence-grounding threshold; it is not an answer-count metric.
- Per-question score movement: improved `100`, unchanged `0`, regressed `0`

## Summary Table

| # | Case ID | Question | Baseline C/R/A | K2 C/R/A | Delta C/R/A | Baseline pass | K2 pass | MCP calls | K2 evidence gaps |
|---:|---|---|---:|---:|---:|---|---|---:|---|
| 1 | `flink-rest-dispatcher-rest-endpoint` | For Flink REST API 2.2.0, inspect `DispatcherRestEndpoint`: identify where dispatcher REST handlers are registered. Which version-pinned docs, impl... | `0.125/0/0.25` | `0.841667/0.933333/0.75` | `0.716667/0.933333/0.5` | `false` | `true` | `1` | artifacts: 1; must-mentions: 2 |
| 2 | `flink-rest-web-monitor-endpoint` | For Flink REST API 2.2.0, inspect `WebMonitorEndpoint`: explain how the web monitor endpoint wires REST handlers. Which version-pinned docs, implem... | `0.1875/0/0.375` | `0.875/1/0.75` | `0.6875/1/0.375` | `false` | `true` | `1` | must-mentions: 2 |
| 3 | `flink-rest-rest-server-endpoint` | For Flink REST API 2.2.0, inspect `RestServerEndpoint`: trace the abstract REST endpoint lifecycle. Which version-pinned docs, implementation class... | `0.125/0/0.25` | `0.875/1/0.75` | `0.75/1/0.5` | `false` | `true` | `1` | must-mentions: 2 |
| 4 | `flink-rest-abstract-rest-handler` | For Flink REST API 2.2.0, inspect `AbstractRestHandler`: implement a request handler with the correct response-body contract. Which version-pinned... | `0.1875/0/0.375` | `0.904167/0.933333/0.875` | `0.716667/0.933333/0.5` | `false` | `true` | `1` | artifacts: 1; must-mentions: 1 |
| 5 | `flink-rest-job-details-handler` | For Flink REST API 2.2.0, inspect `JobDetailsHandler`: use a neighboring job REST handler as an implementation analogue. Which version-pinned docs,... | `0.1875/0/0.375` | `0.9375/1/0.875` | `0.75/1/0.5` | `false` | `true` | `1` | must-mentions: 1 |
| 6 | `flink-rest-job-config-handler` | For Flink REST API 2.2.0, inspect `JobConfigHandler`: inspect how job configuration is exposed through REST. Which version-pinned docs, implementat... | `0.1875/0/0.375` | `0.9375/1/0.875` | `0.75/1/0.5` | `false` | `true` | `1` | must-mentions: 1 |
| 7 | `flink-rest-job-exceptions-handler` | For Flink REST API 2.2.0, inspect `JobExceptionsHandler`: inspect exception response handling for a job endpoint. Which version-pinned docs, implem... | `0.1875/0/0.375` | `0.9375/1/0.875` | `0.75/1/0.5` | `false` | `true` | `1` | must-mentions: 1 |
| 8 | `flink-rest-job-accumulators-handler` | For Flink REST API 2.2.0, inspect `JobAccumulatorsHandler`: inspect accumulator response construction for a job endpoint. Which version-pinned docs... | `0.1875/0/0.375` | `0.904167/0.933333/0.875` | `0.716667/0.933333/0.5` | `false` | `true` | `1` | artifacts: 1; must-mentions: 1 |
| 9 | `flink-rest-job-plan-handler` | For Flink REST API 2.2.0, inspect `JobPlanHandler`: explain how plan metadata is returned through a REST handler. Which version-pinned docs, implem... | `0.1875/0/0.375` | `0.966667/0.933333/1` | `0.779167/0.933333/0.625` | `false` | `true` | `1` | artifacts: 1 |
| 10 | `flink-rest-job-vertex-details-handler` | For Flink REST API 2.2.0, inspect `JobVertexDetailsHandler`: inspect a vertex-scoped REST endpoint implementation. Which version-pinned docs, imple... | `0.1875/0/0.375` | `0.904167/0.933333/0.875` | `0.716667/0.933333/0.5` | `false` | `true` | `1` | artifacts: 1; must-mentions: 1 |
| 11 | `flink-rest-job-vertex-taskmanagers-handler` | For Flink REST API 2.2.0, inspect `JobVertexTaskManagersHandler`: inspect task-manager detail routing for a job vertex. Which version-pinned docs,... | `0.25/0/0.5` | `0.966667/0.933333/1` | `0.716667/0.933333/0.5` | `false` | `true` | `1` | artifacts: 1 |
| 12 | `flink-rest-job-cancellation-handler` | For Flink REST API 2.2.0, inspect `JobCancellationHandler`: trace cancellation request handling and response behavior. Which version-pinned docs, i... | `0.1875/0/0.375` | `1/1/1` | `0.8125/1/0.625` | `false` | `true` | `1` | none |
| 13 | `flink-rest-savepoint-handlers` | For Flink REST API 2.2.0, inspect `SavepointHandlers`: trace savepoint trigger and polling REST behavior. Which version-pinned docs, implementation... | `0.125/0/0.25` | `0.808333/0.866667/0.75` | `0.683333/0.866667/0.5` | `false` | `false` | `1` | artifacts: 2; must-mentions: 2 |
| 14 | `flink-rest-checkpoint-handlers` | For Flink REST API 2.2.0, inspect `CheckpointHandlers`: trace checkpoint trigger and status REST behavior. Which version-pinned docs, implementatio... | `0.1875/0/0.375` | `0.6125/0.6/0.625` | `0.425/0.6/0.25` | `false` | `false` | `1` | artifacts: 3; API surfaces: 1; must-mentions: 3 |
| 15 | `flink-rest-job-resource-requirements-update-handler` | For Flink REST API 2.2.0, inspect `JobResourceRequirementsUpdateHandler`: inspect request-body validation for job resource requirement updates. Whi... | `0.125/0/0.25` | `0.841667/0.933333/0.75` | `0.716667/0.933333/0.5` | `false` | `true` | `1` | artifacts: 1; must-mentions: 2 |
| 16 | `flink-rest-job-submit-handler` | For Flink REST API 2.2.0, inspect `JobSubmitHandler`: inspect job submission request handling. Which version-pinned docs, implementation class, and... | `0.125/0/0.25` | `0.875/1/0.75` | `0.75/1/0.5` | `false` | `true` | `1` | must-mentions: 2 |
| 17 | `flink-rest-file-uploads` | For Flink REST API 2.2.0, inspect `FileUploads`: inspect uploaded-file tracking for REST requests. Which version-pinned docs, implementation class,... | `0.125/0/0.25` | `0.9375/1/0.875` | `0.8125/1/0.625` | `false` | `true` | `1` | must-mentions: 1 |
| 18 | `flink-rest-dashboard-config-handler` | For Flink REST API 2.2.0, inspect `DashboardConfigHandler`: inspect cluster dashboard configuration responses. Which version-pinned docs, implement... | `0.1875/0/0.375` | `0.904167/0.933333/0.875` | `0.716667/0.933333/0.5` | `false` | `true` | `1` | artifacts: 1; must-mentions: 1 |
| 19 | `flink-rest-cluster-overview-handler` | For Flink REST API 2.2.0, inspect `ClusterOverviewHandler`: inspect cluster overview response construction. Which version-pinned docs, implementati... | `0.1875/0/0.375` | `0.904167/0.933333/0.875` | `0.716667/0.933333/0.5` | `false` | `true` | `1` | artifacts: 1; must-mentions: 1 |
| 20 | `flink-rest-taskmanagers-handler` | For Flink REST API 2.2.0, inspect `TaskManagersHandler`: inspect task-manager collection response handling. Which version-pinned docs, implementati... | `0.25/0/0.5` | `0.904167/0.933333/0.875` | `0.654167/0.933333/0.375` | `false` | `true` | `1` | artifacts: 1; must-mentions: 1 |
| 21 | `flink-rest-taskmanager-details-handler` | For Flink REST API 2.2.0, inspect `TaskManagerDetailsHandler`: inspect task-manager detail lookup behavior. Which version-pinned docs, implementati... | `0.1875/0/0.375` | `0.9375/1/0.875` | `0.75/1/0.5` | `false` | `true` | `1` | must-mentions: 1 |
| 22 | `flink-rest-job-vertex-back-pressure-handler` | For Flink REST API 2.2.0, inspect `JobVertexBackPressureHandler`: inspect back-pressure endpoint behavior for job vertices. Which version-pinned do... | `0.1875/0/0.375` | `1/1/1` | `0.8125/1/0.625` | `false` | `true` | `1` | none |
| 23 | `flink-rest-job-vertex-watermarks-handler` | For Flink REST API 2.2.0, inspect `JobVertexWatermarksHandler`: inspect watermark reporting through REST. Which version-pinned docs, implementation... | `0.1875/0/0.375` | `1/1/1` | `0.8125/1/0.625` | `false` | `true` | `1` | none |
| 24 | `flink-rest-subtask-current-attempt-details-handler` | For Flink REST API 2.2.0, inspect `SubtaskCurrentAttemptDetailsHandler`: inspect subtask-attempt details routing. Which version-pinned docs, implem... | `0.25/0/0.5` | `1/1/1` | `0.75/1/0.5` | `false` | `true` | `1` | none |
| 25 | `flink-rest-job-vertex-flame-graph-handler` | For Flink REST API 2.2.0, inspect `JobVertexFlameGraphHandler`: inspect flame-graph endpoint behavior for job vertices. Which version-pinned docs,... | `0.1875/0/0.375` | `1/1/1` | `0.8125/1/0.625` | `false` | `true` | `1` | none |
| 26 | `flink-checkpointing-checkpoint-coordinator` | For Flink checkpointing 2.2.0, inspect `CheckpointCoordinator`: trace checkpoint triggering and coordinator responsibilities. Which version-pinned... | `0.125/0/0.25` | `0.9375/1/0.875` | `0.8125/1/0.625` | `false` | `true` | `1` | must-mentions: 1 |
| 27 | `flink-checkpointing-pending-checkpoint` | For Flink checkpointing 2.2.0, inspect `PendingCheckpoint`: explain pending checkpoint state transitions. Which version-pinned docs, implementation... | `0.1875/0/0.375` | `0.9375/1/0.875` | `0.75/1/0.5` | `false` | `true` | `1` | must-mentions: 1 |
| 28 | `flink-checkpointing-completed-checkpoint` | For Flink checkpointing 2.2.0, inspect `CompletedCheckpoint`: explain completed checkpoint metadata and lifecycle. Which version-pinned docs, imple... | `0.25/0/0.5` | `0.9375/1/0.875` | `0.6875/1/0.375` | `false` | `true` | `1` | must-mentions: 1 |
| 29 | `flink-checkpointing-completed-checkpoint-store` | For Flink checkpointing 2.2.0, inspect `CompletedCheckpointStore`: inspect how completed checkpoints are retained. Which version-pinned docs, imple... | `0.125/0/0.25` | `0.9375/1/0.875` | `0.8125/1/0.625` | `false` | `true` | `1` | must-mentions: 1 |
| 30 | `flink-checkpointing-default-completed-checkpoint-store` | For Flink checkpointing 2.2.0, inspect `DefaultCompletedCheckpointStore`: inspect default completed checkpoint retention behavior. Which version-pi... | `0.125/0/0.25` | `0.9375/1/0.875` | `0.8125/1/0.625` | `false` | `true` | `11` | must-mentions: 1 |
| 31 | `flink-checkpointing-checkpoint-stats-tracker` | For Flink checkpointing 2.2.0, inspect `CheckpointStatsTracker`: explain checkpoint statistics tracking. Which version-pinned docs, implementation... | `0.1875/0/0.375` | `0.9375/1/0.875` | `0.75/1/0.5` | `false` | `true` | `1` | must-mentions: 1 |
| 32 | `flink-checkpointing-checkpoint-stats-snapshot` | For Flink checkpointing 2.2.0, inspect `CheckpointStatsSnapshot`: inspect checkpoint statistics snapshot behavior. Which version-pinned docs, imple... | `0.1875/0/0.375` | `0.9375/1/0.875` | `0.75/1/0.5` | `false` | `true` | `1` | must-mentions: 1 |
| 33 | `flink-checkpointing-checkpoint-metrics` | For Flink checkpointing 2.2.0, inspect `CheckpointMetrics`: identify checkpoint metric fields used by reporting code. Which version-pinned docs, im... | `0.125/0/0.25` | `0.9375/1/0.875` | `0.8125/1/0.625` | `false` | `true` | `1` | must-mentions: 1 |
| 34 | `flink-checkpointing-checkpoint-properties` | For Flink checkpointing 2.2.0, inspect `CheckpointProperties`: explain checkpoint property flags and savepoint behavior. Which version-pinned docs,... | `0.25/0/0.5` | `1/1/1` | `0.75/1/0.5` | `false` | `true` | `1` | none |
| 35 | `flink-checkpointing-checkpoint-retention-policy` | For Flink checkpointing 2.2.0, inspect `CheckpointRetentionPolicy`: explain checkpoint retention policy choices. Which version-pinned docs, impleme... | `0.25/0/0.5` | `0.904167/0.933333/0.875` | `0.654167/0.933333/0.375` | `false` | `true` | `1` | artifacts: 1; must-mentions: 1 |
| 36 | `flink-checkpointing-checkpoint-id-counter` | For Flink checkpointing 2.2.0, inspect `CheckpointIDCounter`: inspect checkpoint id allocation behavior. Which version-pinned docs, implementation... | `0.1875/0/0.375` | `0.904167/0.933333/0.875` | `0.716667/0.933333/0.5` | `false` | `true` | `1` | artifacts: 1; must-mentions: 1 |
| 37 | `flink-checkpointing-standalone-checkpoint-id-counter` | For Flink checkpointing 2.2.0, inspect `StandaloneCheckpointIDCounter`: inspect standalone checkpoint id allocation. Which version-pinned docs, imp... | `0.125/0/0.25` | `0.9375/1/0.875` | `0.8125/1/0.625` | `false` | `true` | `1` | must-mentions: 1 |
| 38 | `flink-checkpointing-checkpoint-failure-manager` | For Flink checkpointing 2.2.0, inspect `CheckpointFailureManager`: explain tolerated checkpoint failure handling. Which version-pinned docs, implem... | `0.125/0/0.25` | `0.875/1/0.75` | `0.75/1/0.5` | `false` | `true` | `5` | must-mentions: 2 |
| 39 | `flink-checkpointing-checkpoint-plan-calculator` | For Flink checkpointing 2.2.0, inspect `CheckpointPlanCalculator`: trace checkpoint plan calculation responsibilities. Which version-pinned docs, i... | `0.125/0/0.25` | `0.9375/1/0.875` | `0.8125/1/0.625` | `false` | `true` | `1` | must-mentions: 1 |
| 40 | `flink-checkpointing-default-checkpoint-plan-calculator` | For Flink checkpointing 2.2.0, inspect `DefaultCheckpointPlanCalculator`: inspect the default checkpoint plan calculation implementation. Which ver... | `0.125/0/0.25` | `0.9375/1/0.875` | `0.8125/1/0.625` | `false` | `true` | `1` | must-mentions: 1 |
| 41 | `flink-checkpointing-checkpoint-request-decider` | For Flink checkpointing 2.2.0, inspect `CheckpointRequestDecider`: explain checkpoint request scheduling decisions. Which version-pinned docs, impl... | `0.1875/0/0.375` | `0.9375/1/0.875` | `0.75/1/0.5` | `false` | `true` | `1` | must-mentions: 1 |
| 42 | `flink-checkpointing-checkpoint-resources-cleanup-runner` | For Flink checkpointing 2.2.0, inspect `CheckpointResourcesCleanupRunner`: inspect checkpoint resource cleanup behavior. Which version-pinned docs,... | `0.1875/0/0.375` | `0.9375/1/0.875` | `0.75/1/0.5` | `false` | `true` | `1` | must-mentions: 1 |
| 43 | `flink-checkpointing-checkpoint-storage-loader` | For Flink checkpointing 2.2.0, inspect `CheckpointStorageLoader`: explain checkpoint storage loading during configuration. Which version-pinned doc... | `0.25/0/0.5` | `0.9375/1/0.875` | `0.6875/1/0.375` | `false` | `true` | `1` | must-mentions: 1 |
| 44 | `flink-checkpointing-checkpoint-storage-coordinator-view` | For Flink checkpointing 2.2.0, inspect `CheckpointStorageCoordinatorView`: explain the coordinator-facing checkpoint storage contract. Which versio... | `0.125/0/0.25` | `0.904167/0.933333/0.875` | `0.779167/0.933333/0.625` | `false` | `true` | `1` | artifacts: 1; must-mentions: 1 |
| 45 | `flink-checkpointing-state-backend` | For Flink checkpointing 2.2.0, inspect `StateBackend`: explain state backend responsibilities during checkpointing. Which version-pinned docs, impl... | `0.1875/0/0.375` | `0.904167/0.933333/0.875` | `0.716667/0.933333/0.5` | `false` | `true` | `1` | artifacts: 1; must-mentions: 1 |
| 46 | `flink-checkpointing-operator-state-backend` | For Flink checkpointing 2.2.0, inspect `OperatorStateBackend`: inspect operator-state checkpointing responsibilities. Which version-pinned docs, im... | `0.1875/0/0.375` | `0.9375/1/0.875` | `0.75/1/0.5` | `false` | `true` | `1` | must-mentions: 1 |
| 47 | `flink-checkpointing-keyed-state-backend` | For Flink checkpointing 2.2.0, inspect `KeyedStateBackend`: inspect keyed-state checkpointing responsibilities. Which version-pinned docs, implemen... | `0.1875/0/0.375` | `0.966667/0.933333/1` | `0.779167/0.933333/0.625` | `false` | `true` | `1` | artifacts: 1 |
| 48 | `flink-checkpointing-savepoint-restore-settings` | For Flink checkpointing 2.2.0, inspect `SavepointRestoreSettings`: explain savepoint restore settings during upgrades. Which version-pinned docs, i... | `0.25/0/0.5` | `1/1/1` | `0.75/1/0.5` | `false` | `true` | `1` | none |
| 49 | `flink-checkpointing-savepoint-format-type` | For Flink checkpointing 2.2.0, inspect `SavepointFormatType`: explain savepoint format choices. Which version-pinned docs, implementation class, an... | `0.25/0/0.5` | `0.904167/0.933333/0.875` | `0.654167/0.933333/0.375` | `false` | `true` | `8` | artifacts: 1; must-mentions: 1 |
| 50 | `flink-checkpointing-checkpoint-coordinator-configuration` | For Flink checkpointing 2.2.0, inspect `CheckpointCoordinatorConfiguration`: inspect checkpoint coordinator configuration options. Which version-pi... | `0.125/0/0.25` | `0.904167/0.933333/0.875` | `0.779167/0.933333/0.625` | `false` | `true` | `1` | artifacts: 1; must-mentions: 1 |
| 51 | `kafka-rest-connector-plugins-resource` | For Kafka Connect REST 4.2.0, inspect `ConnectorPluginsResource`: trace connector plugin validation through the REST resource. Which version-pinned... | `0.25/0/0.5` | `1/1/1` | `0.75/1/0.5` | `false` | `true` | `1` | none |
| 52 | `kafka-connect-abstract-herder` | For Kafka Connect 4.2.0, inspect `AbstractHerder`: trace connector configuration validation in the herder layer. Which version-pinned docs, impleme... | `0.166667/0/0.333334` | `1/1/1` | `0.833333/1/0.666666` | `false` | `true` | `1` | none |
| 53 | `kafka-connect-distributed-herder` | For Kafka Connect 4.2.0, inspect `DistributedHerder`: inspect distributed connector config update behavior. Which version-pinned docs, implementati... | `0.25/0/0.5` | `1/1/1` | `0.75/1/0.5` | `false` | `true` | `1` | none |
| 54 | `kafka-connect-standalone-herder` | For Kafka Connect 4.2.0, inspect `StandaloneHerder`: inspect standalone connector config update behavior. Which version-pinned docs, implementation... | `0.166667/0/0.333334` | `1/1/1` | `0.833333/1/0.666666` | `false` | `true` | `1` | none |
| 55 | `kafka-connect-herder` | For Kafka Connect 4.2.0, inspect `Herder`: identify the connector management interface. Which version-pinned docs, implementation class, and neighb... | `0.25/0/0.5` | `0.583333/0.666667/0.5` | `0.333333/0.666667/0` | `false` | `false` | `21` | artifacts: 2; source URIs: 1; citations: 1 |
| 56 | `kafka-connect-worker` | For Kafka Connect 4.2.0, inspect `Worker`: trace connector and task lifecycle responsibilities. Which version-pinned docs, implementation class, an... | `0.25/0/0.5` | `0.583333/0.666667/0.5` | `0.333333/0.666667/0` | `false` | `false` | `1` | artifacts: 2; source URIs: 1; citations: 1 |
| 57 | `kafka-connect-worker-connector` | For Kafka Connect 4.2.0, inspect `WorkerConnector`: inspect connector startup and failure handling. Which version-pinned docs, implementation class... | `0.166667/0/0.333334` | `1/1/1` | `0.833333/1/0.666666` | `false` | `true` | `1` | none |
| 58 | `kafka-connect-worker-task` | For Kafka Connect 4.2.0, inspect `WorkerTask`: inspect common task lifecycle behavior. Which version-pinned docs, implementation class, and neighbo... | `0.25/0/0.5` | `1/1/1` | `0.75/1/0.5` | `false` | `true` | `1` | none |
| 59 | `kafka-connect-worker-sink-task` | For Kafka Connect 4.2.0, inspect `WorkerSinkTask`: inspect sink task delivery and commit behavior. Which version-pinned docs, implementation class,... | `0.166667/0/0.333334` | `1/1/1` | `0.833333/1/0.666666` | `false` | `true` | `1` | none |
| 60 | `kafka-connect-worker-source-task` | For Kafka Connect 4.2.0, inspect `WorkerSourceTask`: inspect source task polling and commit behavior. Which version-pinned docs, implementation cla... | `0.166667/0/0.333334` | `1/1/1` | `0.833333/1/0.666666` | `false` | `true` | `3` | none |
| 61 | `kafka-connect-connector-config` | For Kafka Connect 4.2.0, inspect `ConnectorConfig`: explain shared connector configuration validation. Which version-pinned docs, implementation cl... | `0.25/0/0.5` | `1/1/1` | `0.75/1/0.5` | `false` | `true` | `1` | none |
| 62 | `kafka-connect-sink-connector-config` | For Kafka Connect 4.2.0, inspect `SinkConnectorConfig`: inspect sink connector-specific config validation. Which version-pinned docs, implementatio... | `0.25/0/0.5` | `0.966667/0.933333/1` | `0.716667/0.933333/0.5` | `false` | `true` | `1` | artifacts: 1 |
| 63 | `kafka-connect-source-connector-config` | For Kafka Connect 4.2.0, inspect `SourceConnectorConfig`: inspect source connector-specific config validation. Which version-pinned docs, implement... | `0.166667/0/0.333334` | `1/1/1` | `0.833333/1/0.666666` | `false` | `true` | `1` | none |
| 64 | `kafka-connect-worker-config` | For Kafka Connect 4.2.0, inspect `WorkerConfig`: inspect worker-level configuration parsing. Which version-pinned docs, implementation class, and n... | `0.166667/0/0.333334` | `1/1/1` | `0.833333/1/0.666666` | `false` | `true` | `1` | none |
| 65 | `kafka-connect-distributed-config` | For Kafka Connect 4.2.0, inspect `DistributedConfig`: inspect distributed worker configuration behavior. Which version-pinned docs, implementation... | `0.166667/0/0.333334` | `1/1/1` | `0.833333/1/0.666666` | `false` | `true` | `1` | none |
| 66 | `kafka-connect-standalone-config` | For Kafka Connect 4.2.0, inspect `StandaloneConfig`: inspect standalone worker configuration behavior. Which version-pinned docs, implementation cl... | `0.083333/0/0.166666` | `1/1/1` | `0.916667/1/0.833334` | `false` | `true` | `1` | none |
| 67 | `kafka-connect-config-def` | For Kafka Connect 4.2.0, inspect `ConfigDef`: explain Kafka configuration definition and validation semantics. Which version-pinned docs and implem... | `0.25/0/0.5` | `0.55/0.6/0.5` | `0.3/0.6/0` | `false` | `false` | `1` | artifacts: 1; modules: 1; source URIs: 1; citations: 1 |
| 68 | `kafka-connect-config-value` | For Kafka Connect 4.2.0, inspect `ConfigValue`: explain validation result representation. Which version-pinned docs and implementation class should... | `0.25/0/0.5` | `1/1/1` | `0.75/1/0.5` | `false` | `true` | `1` | none |
| 69 | `kafka-connect-config-transformer` | For Kafka Connect 4.2.0, inspect `ConfigTransformer`: inspect externalized configuration transformation behavior. Which version-pinned docs and imp... | `0.25/0/0.5` | `1/1/1` | `0.75/1/0.5` | `false` | `true` | `1` | none |
| 70 | `kafka-connect-config-provider` | For Kafka Connect 4.2.0, inspect `ConfigProvider`: inspect the config provider contract used for externalized secrets. Which version-pinned docs an... | `0.166667/0/0.333334` | `1/1/1` | `0.833333/1/0.666666` | `false` | `true` | `1` | none |
| 71 | `kafka-connect-plugins` | For Kafka Connect 4.2.0, inspect `Plugins`: trace plugin discovery and connector class loading. Which version-pinned docs, implementation class, an... | `0.25/0/0.5` | `0.966667/0.933333/1` | `0.716667/0.933333/0.5` | `false` | `true` | `1` | artifacts: 1 |
| 72 | `kafka-connect-plugin-desc` | For Kafka Connect 4.2.0, inspect `PluginDesc`: inspect plugin descriptor metadata. Which version-pinned docs, implementation class, and neighboring... | `0.166667/0/0.333334` | `1/1/1` | `0.833333/1/0.666666` | `false` | `true` | `1` | none |
| 73 | `kafka-connect-plugin-type` | For Kafka Connect 4.2.0, inspect `PluginType`: inspect plugin type classification. Which version-pinned docs, implementation class, and neighboring... | `0.25/0/0.5` | `0.966667/0.933333/1` | `0.716667/0.933333/0.5` | `false` | `true` | `1` | artifacts: 1 |
| 74 | `kafka-connect-delegating-class-loader` | For Kafka Connect 4.2.0, inspect `DelegatingClassLoader`: inspect plugin classloader delegation behavior. Which version-pinned docs, implementation... | `0.25/0/0.5` | `1/1/1` | `0.75/1/0.5` | `false` | `true` | `1` | none |
| 75 | `kafka-connect-plugin-class-loader` | For Kafka Connect 4.2.0, inspect `PluginClassLoader`: inspect isolated plugin class loading. Which version-pinned docs, implementation class, and n... | `0.25/0/0.5` | `0.883333/0.933333/0.833333` | `0.633333/0.933333/0.333333` | `false` | `true` | `1` | artifacts: 1; must-mentions: 1 |
| 76 | `kafka-connect-plugin-scan-result` | For Kafka Connect 4.2.0, inspect `PluginScanResult`: inspect plugin scanning results. Which version-pinned docs, implementation class, and neighbor... | `0.25/0/0.5` | `0.966667/0.933333/1` | `0.716667/0.933333/0.5` | `false` | `true` | `1` | artifacts: 1 |
| 77 | `kafka-connect-plugin-utils` | For Kafka Connect 4.2.0, inspect `PluginUtils`: inspect plugin path and alias helper behavior. Which version-pinned docs, implementation class, and... | `0.166667/0/0.333334` | `1/1/1` | `0.833333/1/0.666666` | `false` | `true` | `1` | none |
| 78 | `kafka-rest-connect-rest-server` | For Kafka Connect REST 4.2.0, inspect `ConnectRestServer`: trace Connect REST server wiring. Which version-pinned docs, implementation class, and n... | `0.166667/0/0.333334` | `1/1/1` | `0.833333/1/0.666666` | `false` | `true` | `1` | none |
| 79 | `kafka-rest-rest-server-config` | For Kafka Connect REST 4.2.0, inspect `RestServerConfig`: inspect Connect REST server configuration. Which version-pinned docs, implementation clas... | `0.166667/0/0.333334` | `1/1/1` | `0.833333/1/0.666666` | `false` | `true` | `1` | none |
| 80 | `kafka-rest-connectors-resource` | For Kafka Connect REST 4.2.0, inspect `ConnectorsResource`: trace connector CRUD REST behavior. Which version-pinned docs, implementation class, an... | `0.166667/0/0.333334` | `1/1/1` | `0.833333/1/0.666666` | `false` | `true` | `1` | none |
| 81 | `kafka-rest-connector-state-info` | For Kafka Connect REST 4.2.0, inspect `ConnectorStateInfo`: inspect connector state response representation. Which version-pinned docs and implemen... | `0.25/0/0.5` | `0.916667/1/0.833333` | `0.666667/1/0.333333` | `false` | `true` | `1` | must-mentions: 1 |
| 82 | `kafka-rest-connector-info` | For Kafka Connect REST 4.2.0, inspect `ConnectorInfo`: inspect connector info response representation. Which version-pinned docs and implementation... | `0.25/0/0.5` | `0.916667/1/0.833333` | `0.666667/1/0.333333` | `false` | `true` | `1` | must-mentions: 1 |
| 83 | `kafka-rest-create-connector-request` | For Kafka Connect REST 4.2.0, inspect `CreateConnectorRequest`: inspect connector creation request validation. Which version-pinned docs, implement... | `0.166667/0/0.333334` | `0.916667/1/0.833333` | `0.75/1/0.499999` | `false` | `true` | `1` | must-mentions: 1 |
| 84 | `kafka-rest-connector-type` | For Kafka Connect REST 4.2.0, inspect `ConnectorType`: inspect connector type classification. Which version-pinned docs, implementation class, and... | `0.166667/0/0.333334` | `1/1/1` | `0.833333/1/0.666666` | `false` | `true` | `1` | none |
| 85 | `kafka-connect-connector` | For Kafka Connect 4.2.0, inspect `Connector`: inspect the base connector contract. Which version-pinned docs, implementation class, and neighboring... | `0.25/0/0.5` | `0.933333/0.866667/1` | `0.683333/0.866667/0.5` | `false` | `true` | `1` | artifacts: 2 |
| 86 | `kafka-connect-source-connector` | For Kafka Connect 4.2.0, inspect `SourceConnector`: inspect source connector implementation responsibilities. Which version-pinned docs, implementa... | `0.25/0/0.5` | `0.966667/0.933333/1` | `0.716667/0.933333/0.5` | `false` | `true` | `1` | artifacts: 1 |
| 87 | `kafka-connect-sink-connector` | For Kafka Connect 4.2.0, inspect `SinkConnector`: inspect sink connector implementation responsibilities. Which version-pinned docs, implementation... | `0.25/0/0.5` | `0.966667/0.933333/1` | `0.716667/0.933333/0.5` | `false` | `true` | `1` | artifacts: 1 |
| 88 | `kafka-connect-transformation` | For Kafka Connect 4.2.0, inspect `Transformation`: inspect single-message transform behavior. Which version-pinned docs, implementation class, and... | `0.083333/0/0.166666` | `0.933333/0.866667/1` | `0.85/0.866667/0.833334` | `false` | `true` | `1` | artifacts: 2 |
| 89 | `kafka-connect-header-converter` | For Kafka Connect 4.2.0, inspect `HeaderConverter`: inspect header conversion behavior. Which version-pinned docs, implementation class, and neighb... | `0.166667/0/0.333334` | `0.966667/0.933333/1` | `0.8/0.933333/0.666666` | `false` | `true` | `1` | artifacts: 1 |
| 90 | `kafka-connect-converter` | For Kafka Connect 4.2.0, inspect `Converter`: inspect value/key conversion behavior. Which version-pinned docs, implementation class, and neighbori... | `0.083333/0/0.166666` | `0.583333/0.666667/0.5` | `0.5/0.666667/0.333334` | `false` | `false` | `1` | artifacts: 2; source URIs: 1; citations: 1 |
| 91 | `kafka-connect-schemas` | For Kafka Connect 4.2.0, inspect `Schema`: inspect Connect schema representation. Which version-pinned docs, implementation class, and neighboring... | `0.25/0/0.5` | `0.583333/0.666667/0.5` | `0.333333/0.666667/0` | `false` | `false` | `9` | artifacts: 2; source URIs: 1; citations: 1 |
| 92 | `kafka-connect-schema-builder` | For Kafka Connect 4.2.0, inspect `SchemaBuilder`: inspect Connect schema construction behavior. Which version-pinned docs, implementation class, an... | `0.166667/0/0.333334` | `0.966667/0.933333/1` | `0.8/0.933333/0.666666` | `false` | `true` | `1` | artifacts: 1 |
| 93 | `kafka-connect-struct` | For Kafka Connect 4.2.0, inspect `Struct`: inspect structured Connect data validation. Which version-pinned docs, implementation class, and neighbo... | `0.25/0/0.5` | `0.933333/0.866667/1` | `0.683333/0.866667/0.5` | `false` | `true` | `2` | artifacts: 2 |
| 94 | `kafka-connect-sink-record` | For Kafka Connect 4.2.0, inspect `SinkRecord`: inspect sink record metadata available to connectors. Which version-pinned docs, implementation clas... | `0.25/0/0.5` | `1/1/1` | `0.75/1/0.5` | `false` | `true` | `1` | none |
| 95 | `kafka-connect-source-record` | For Kafka Connect 4.2.0, inspect `SourceRecord`: inspect source record construction and partition metadata. Which version-pinned docs, implementati... | `0.166667/0/0.333334` | `0.966667/0.933333/1` | `0.8/0.933333/0.666666` | `false` | `true` | `1` | artifacts: 1 |
| 96 | `kafka-connect-connector-client-config-request` | For Kafka Connect 4.2.0, inspect `ConnectorClientConfigRequest`: inspect connector client override policy inputs. Which version-pinned docs, implem... | `0.166667/0/0.333334` | `0.966667/0.933333/1` | `0.8/0.933333/0.666666` | `false` | `true` | `2` | artifacts: 1 |
| 97 | `kafka-connect-connector-client-config-override-policy` | For Kafka Connect 4.2.0, inspect `ConnectorClientConfigOverridePolicy`: inspect connector client override validation behavior. Which version-pinned... | `0.166667/0/0.333334` | `0.916667/1/0.833333` | `0.75/1/0.499999` | `false` | `true` | `1` | must-mentions: 1 |
| 98 | `kafka-connect-abstract-connector-client-config-override-policy` | For Kafka Connect 4.2.0, inspect `AbstractConnectorClientConfigOverridePolicy`: inspect shared connector client override policy behavior. Which ver... | `0.083333/0/0.166666` | `0.883333/0.933333/0.833333` | `0.8/0.933333/0.666667` | `false` | `true` | `1` | artifacts: 1; must-mentions: 1 |
| 99 | `kafka-connect-none-connector-client-config-override-policy` | For Kafka Connect 4.2.0, inspect `NoneConnectorClientConfigOverridePolicy`: inspect policy behavior when overrides are not allowed. Which version-p... | `0.166667/0/0.333334` | `1/1/1` | `0.833333/1/0.666666` | `false` | `true` | `1` | none |
| 100 | `kafka-connect-principal-connector-client-config-override-policy` | For Kafka Connect 4.2.0, inspect `PrincipalConnectorClientConfigOverridePolicy`: inspect principal-only client override validation behavior. Which... | `0.25/0/0.5` | `1/1/1` | `0.75/1/0.5` | `false` | `true` | `1` | none |

## Per-Question Details

### 1. Flink REST pattern for DispatcherRestEndpoint (`flink-rest-dispatcher-rest-endpoint`)

Question: For Flink REST API 2.2.0, inspect `DispatcherRestEndpoint`: identify where dispatcher REST handlers are registered. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.125, retrieval=0, answer=0.25, safety=1`, K2 `combined=0.841667, retrieval=0.933333, answer=0.75, safety=1`, delta `combined=0.716667, retrieval=0.933333, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.5, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.5, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1; must-mentions: 2
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 2. Flink REST pattern for WebMonitorEndpoint (`flink-rest-web-monitor-endpoint`)

Question: For Flink REST API 2.2.0, inspect `WebMonitorEndpoint`: explain how the web monitor endpoint wires REST handlers. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.875, retrieval=1, answer=0.75, safety=1`, delta `combined=0.6875, retrieval=1, answer=0.375, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.5, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 2
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 3. Flink REST pattern for RestServerEndpoint (`flink-rest-rest-server-endpoint`)

Question: For Flink REST API 2.2.0, inspect `RestServerEndpoint`: trace the abstract REST endpoint lifecycle. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.125, retrieval=0, answer=0.25, safety=1`, K2 `combined=0.875, retrieval=1, answer=0.75, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.5, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.5, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 2
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 4. Flink REST pattern for AbstractRestHandler (`flink-rest-abstract-rest-handler`)

Question: For Flink REST API 2.2.0, inspect `AbstractRestHandler`: implement a request handler with the correct response-body contract. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.904167, retrieval=0.933333, answer=0.875, safety=1`, delta `combined=0.716667, retrieval=0.933333, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1; must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 5. Flink REST pattern for JobDetailsHandler (`flink-rest-job-details-handler`)

Question: For Flink REST API 2.2.0, inspect `JobDetailsHandler`: use a neighboring job REST handler as an implementation analogue. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 6. Flink REST pattern for JobConfigHandler (`flink-rest-job-config-handler`)

Question: For Flink REST API 2.2.0, inspect `JobConfigHandler`: inspect how job configuration is exposed through REST. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 7. Flink REST pattern for JobExceptionsHandler (`flink-rest-job-exceptions-handler`)

Question: For Flink REST API 2.2.0, inspect `JobExceptionsHandler`: inspect exception response handling for a job endpoint. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 8. Flink REST pattern for JobAccumulatorsHandler (`flink-rest-job-accumulators-handler`)

Question: For Flink REST API 2.2.0, inspect `JobAccumulatorsHandler`: inspect accumulator response construction for a job endpoint. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.904167, retrieval=0.933333, answer=0.875, safety=1`, delta `combined=0.716667, retrieval=0.933333, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1; must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 9. Flink REST pattern for JobPlanHandler (`flink-rest-job-plan-handler`)

Question: For Flink REST API 2.2.0, inspect `JobPlanHandler`: explain how plan metadata is returned through a REST handler. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.966667, retrieval=0.933333, answer=1, safety=1`, delta `combined=0.779167, retrieval=0.933333, answer=0.625, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 10. Flink REST pattern for JobVertexDetailsHandler (`flink-rest-job-vertex-details-handler`)

Question: For Flink REST API 2.2.0, inspect `JobVertexDetailsHandler`: inspect a vertex-scoped REST endpoint implementation. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.904167, retrieval=0.933333, answer=0.875, safety=1`, delta `combined=0.716667, retrieval=0.933333, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1; must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 11. Flink REST pattern for JobVertexTaskManagersHandler (`flink-rest-job-vertex-taskmanagers-handler`)

Question: For Flink REST API 2.2.0, inspect `JobVertexTaskManagersHandler`: inspect task-manager detail routing for a job vertex. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.966667, retrieval=0.933333, answer=1, safety=1`, delta `combined=0.716667, retrieval=0.933333, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 12. Flink REST pattern for JobCancellationHandler (`flink-rest-job-cancellation-handler`)

Question: For Flink REST API 2.2.0, inspect `JobCancellationHandler`: trace cancellation request handling and response behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.8125, retrieval=1, answer=0.625, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 13. Flink REST pattern for SavepointHandlers (`flink-rest-savepoint-handlers`)

Question: For Flink REST API 2.2.0, inspect `SavepointHandlers`: trace savepoint trigger and polling REST behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.125, retrieval=0, answer=0.25, safety=1`, K2 `combined=0.808333, retrieval=0.866667, answer=0.75, safety=1`, delta `combined=0.683333, retrieval=0.866667, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `false`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.333333, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.5, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.5, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 2; must-mentions: 2
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 14. Flink REST pattern for CheckpointHandlers (`flink-rest-checkpoint-handlers`)

Question: For Flink REST API 2.2.0, inspect `CheckpointHandlers`: trace checkpoint trigger and status REST behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.6125, retrieval=0.6, answer=0.625, safety=1`, delta `combined=0.425, retrieval=0.6, answer=0.25, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `false`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0, source_kind_coverage=1, module_hits=1, api_surface_hits=0, must_mention_coverage=0.25, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 3; API surfaces: 1; must-mentions: 3
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 15. Flink REST pattern for JobResourceRequirementsUpdateHandler (`flink-rest-job-resource-requirements-update-handler`)

Question: For Flink REST API 2.2.0, inspect `JobResourceRequirementsUpdateHandler`: inspect request-body validation for job resource requirement updates. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.125, retrieval=0, answer=0.25, safety=1`, K2 `combined=0.841667, retrieval=0.933333, answer=0.75, safety=1`, delta `combined=0.716667, retrieval=0.933333, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.5, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.5, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1; must-mentions: 2
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 16. Flink REST pattern for JobSubmitHandler (`flink-rest-job-submit-handler`)

Question: For Flink REST API 2.2.0, inspect `JobSubmitHandler`: inspect job submission request handling. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.125, retrieval=0, answer=0.25, safety=1`, K2 `combined=0.875, retrieval=1, answer=0.75, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.5, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.5, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 2
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 17. Flink REST pattern for FileUploads (`flink-rest-file-uploads`)

Question: For Flink REST API 2.2.0, inspect `FileUploads`: inspect uploaded-file tracking for REST requests. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.125, retrieval=0, answer=0.25, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.8125, retrieval=1, answer=0.625, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.5, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 18. Flink REST pattern for DashboardConfigHandler (`flink-rest-dashboard-config-handler`)

Question: For Flink REST API 2.2.0, inspect `DashboardConfigHandler`: inspect cluster dashboard configuration responses. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.904167, retrieval=0.933333, answer=0.875, safety=1`, delta `combined=0.716667, retrieval=0.933333, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1; must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 19. Flink REST pattern for ClusterOverviewHandler (`flink-rest-cluster-overview-handler`)

Question: For Flink REST API 2.2.0, inspect `ClusterOverviewHandler`: inspect cluster overview response construction. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.904167, retrieval=0.933333, answer=0.875, safety=1`, delta `combined=0.716667, retrieval=0.933333, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1; must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 20. Flink REST pattern for TaskManagersHandler (`flink-rest-taskmanagers-handler`)

Question: For Flink REST API 2.2.0, inspect `TaskManagersHandler`: inspect task-manager collection response handling. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.904167, retrieval=0.933333, answer=0.875, safety=1`, delta `combined=0.654167, retrieval=0.933333, answer=0.375, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1; must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 21. Flink REST pattern for TaskManagerDetailsHandler (`flink-rest-taskmanager-details-handler`)

Question: For Flink REST API 2.2.0, inspect `TaskManagerDetailsHandler`: inspect task-manager detail lookup behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 22. Flink REST pattern for JobVertexBackPressureHandler (`flink-rest-job-vertex-back-pressure-handler`)

Question: For Flink REST API 2.2.0, inspect `JobVertexBackPressureHandler`: inspect back-pressure endpoint behavior for job vertices. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.8125, retrieval=1, answer=0.625, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 23. Flink REST pattern for JobVertexWatermarksHandler (`flink-rest-job-vertex-watermarks-handler`)

Question: For Flink REST API 2.2.0, inspect `JobVertexWatermarksHandler`: inspect watermark reporting through REST. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.8125, retrieval=1, answer=0.625, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 24. Flink REST pattern for SubtaskCurrentAttemptDetailsHandler (`flink-rest-subtask-current-attempt-details-handler`)

Question: For Flink REST API 2.2.0, inspect `SubtaskCurrentAttemptDetailsHandler`: inspect subtask-attempt details routing. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 25. Flink REST pattern for JobVertexFlameGraphHandler (`flink-rest-job-vertex-flame-graph-handler`)

Question: For Flink REST API 2.2.0, inspect `JobVertexFlameGraphHandler`: inspect flame-graph endpoint behavior for job vertices. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.8125, retrieval=1, answer=0.625, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 26. Flink checkpointing pattern for CheckpointCoordinator (`flink-checkpointing-checkpoint-coordinator`)

Question: For Flink checkpointing 2.2.0, inspect `CheckpointCoordinator`: trace checkpoint triggering and coordinator responsibilities. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.125, retrieval=0, answer=0.25, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.8125, retrieval=1, answer=0.625, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.5, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 27. Flink checkpointing pattern for PendingCheckpoint (`flink-checkpointing-pending-checkpoint`)

Question: For Flink checkpointing 2.2.0, inspect `PendingCheckpoint`: explain pending checkpoint state transitions. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 28. Flink checkpointing pattern for CompletedCheckpoint (`flink-checkpointing-completed-checkpoint`)

Question: For Flink checkpointing 2.2.0, inspect `CompletedCheckpoint`: explain completed checkpoint metadata and lifecycle. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.6875, retrieval=1, answer=0.375, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 29. Flink checkpointing pattern for CompletedCheckpointStore (`flink-checkpointing-completed-checkpoint-store`)

Question: For Flink checkpointing 2.2.0, inspect `CompletedCheckpointStore`: inspect how completed checkpoints are retained. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.125, retrieval=0, answer=0.25, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.8125, retrieval=1, answer=0.625, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.5, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 30. Flink checkpointing pattern for DefaultCompletedCheckpointStore (`flink-checkpointing-default-completed-checkpoint-store`)

Question: For Flink checkpointing 2.2.0, inspect `DefaultCompletedCheckpointStore`: inspect default completed checkpoint retention behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.125, retrieval=0, answer=0.25, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.8125, retrieval=1, answer=0.625, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1, "k2_search_code": 5, "k2_search_docs": 1, "k2_search_tests": 4}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.5, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 31. Flink checkpointing pattern for CheckpointStatsTracker (`flink-checkpointing-checkpoint-stats-tracker`)

Question: For Flink checkpointing 2.2.0, inspect `CheckpointStatsTracker`: explain checkpoint statistics tracking. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 32. Flink checkpointing pattern for CheckpointStatsSnapshot (`flink-checkpointing-checkpoint-stats-snapshot`)

Question: For Flink checkpointing 2.2.0, inspect `CheckpointStatsSnapshot`: inspect checkpoint statistics snapshot behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 33. Flink checkpointing pattern for CheckpointMetrics (`flink-checkpointing-checkpoint-metrics`)

Question: For Flink checkpointing 2.2.0, inspect `CheckpointMetrics`: identify checkpoint metric fields used by reporting code. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.125, retrieval=0, answer=0.25, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.8125, retrieval=1, answer=0.625, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.5, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 34. Flink checkpointing pattern for CheckpointProperties (`flink-checkpointing-checkpoint-properties`)

Question: For Flink checkpointing 2.2.0, inspect `CheckpointProperties`: explain checkpoint property flags and savepoint behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 35. Flink checkpointing pattern for CheckpointRetentionPolicy (`flink-checkpointing-checkpoint-retention-policy`)

Question: For Flink checkpointing 2.2.0, inspect `CheckpointRetentionPolicy`: explain checkpoint retention policy choices. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.904167, retrieval=0.933333, answer=0.875, safety=1`, delta `combined=0.654167, retrieval=0.933333, answer=0.375, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1; must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 36. Flink checkpointing pattern for CheckpointIDCounter (`flink-checkpointing-checkpoint-id-counter`)

Question: For Flink checkpointing 2.2.0, inspect `CheckpointIDCounter`: inspect checkpoint id allocation behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.904167, retrieval=0.933333, answer=0.875, safety=1`, delta `combined=0.716667, retrieval=0.933333, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1; must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 37. Flink checkpointing pattern for StandaloneCheckpointIDCounter (`flink-checkpointing-standalone-checkpoint-id-counter`)

Question: For Flink checkpointing 2.2.0, inspect `StandaloneCheckpointIDCounter`: inspect standalone checkpoint id allocation. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.125, retrieval=0, answer=0.25, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.8125, retrieval=1, answer=0.625, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.5, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 38. Flink checkpointing pattern for CheckpointFailureManager (`flink-checkpointing-checkpoint-failure-manager`)

Question: For Flink checkpointing 2.2.0, inspect `CheckpointFailureManager`: explain tolerated checkpoint failure handling. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.125, retrieval=0, answer=0.25, safety=1`, K2 `combined=0.875, retrieval=1, answer=0.75, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1, "k2_search_code": 1, "k2_search_docs": 1, "k2_search_tests": 2}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.5, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.5, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 2
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 39. Flink checkpointing pattern for CheckpointPlanCalculator (`flink-checkpointing-checkpoint-plan-calculator`)

Question: For Flink checkpointing 2.2.0, inspect `CheckpointPlanCalculator`: trace checkpoint plan calculation responsibilities. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.125, retrieval=0, answer=0.25, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.8125, retrieval=1, answer=0.625, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.5, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 40. Flink checkpointing pattern for DefaultCheckpointPlanCalculator (`flink-checkpointing-default-checkpoint-plan-calculator`)

Question: For Flink checkpointing 2.2.0, inspect `DefaultCheckpointPlanCalculator`: inspect the default checkpoint plan calculation implementation. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.125, retrieval=0, answer=0.25, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.8125, retrieval=1, answer=0.625, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.5, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 41. Flink checkpointing pattern for CheckpointRequestDecider (`flink-checkpointing-checkpoint-request-decider`)

Question: For Flink checkpointing 2.2.0, inspect `CheckpointRequestDecider`: explain checkpoint request scheduling decisions. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 42. Flink checkpointing pattern for CheckpointResourcesCleanupRunner (`flink-checkpointing-checkpoint-resources-cleanup-runner`)

Question: For Flink checkpointing 2.2.0, inspect `CheckpointResourcesCleanupRunner`: inspect checkpoint resource cleanup behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 43. Flink checkpointing pattern for CheckpointStorageLoader (`flink-checkpointing-checkpoint-storage-loader`)

Question: For Flink checkpointing 2.2.0, inspect `CheckpointStorageLoader`: explain checkpoint storage loading during configuration. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.6875, retrieval=1, answer=0.375, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 44. Flink checkpointing pattern for CheckpointStorageCoordinatorView (`flink-checkpointing-checkpoint-storage-coordinator-view`)

Question: For Flink checkpointing 2.2.0, inspect `CheckpointStorageCoordinatorView`: explain the coordinator-facing checkpoint storage contract. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.125, retrieval=0, answer=0.25, safety=1`, K2 `combined=0.904167, retrieval=0.933333, answer=0.875, safety=1`, delta `combined=0.779167, retrieval=0.933333, answer=0.625, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.5, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1; must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 45. Flink checkpointing pattern for StateBackend (`flink-checkpointing-state-backend`)

Question: For Flink checkpointing 2.2.0, inspect `StateBackend`: explain state backend responsibilities during checkpointing. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.904167, retrieval=0.933333, answer=0.875, safety=1`, delta `combined=0.716667, retrieval=0.933333, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1; must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 46. Flink checkpointing pattern for OperatorStateBackend (`flink-checkpointing-operator-state-backend`)

Question: For Flink checkpointing 2.2.0, inspect `OperatorStateBackend`: inspect operator-state checkpointing responsibilities. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.9375, retrieval=1, answer=0.875, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 47. Flink checkpointing pattern for KeyedStateBackend (`flink-checkpointing-keyed-state-backend`)

Question: For Flink checkpointing 2.2.0, inspect `KeyedStateBackend`: inspect keyed-state checkpointing responsibilities. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.1875, retrieval=0, answer=0.375, safety=1`, K2 `combined=0.966667, retrieval=0.933333, answer=1, safety=1`, delta `combined=0.779167, retrieval=0.933333, answer=0.625, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.75, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 48. Flink checkpointing pattern for SavepointRestoreSettings (`flink-checkpointing-savepoint-restore-settings`)

Question: For Flink checkpointing 2.2.0, inspect `SavepointRestoreSettings`: explain savepoint restore settings during upgrades. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 49. Flink checkpointing pattern for SavepointFormatType (`flink-checkpointing-savepoint-format-type`)

Question: For Flink checkpointing 2.2.0, inspect `SavepointFormatType`: explain savepoint format choices. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.904167, retrieval=0.933333, answer=0.875, safety=1`, delta `combined=0.654167, retrieval=0.933333, answer=0.375, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1, "k2_search_code": 4, "k2_search_docs": 1, "k2_search_tests": 2}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1; must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 50. Flink checkpointing pattern for CheckpointCoordinatorConfiguration (`flink-checkpointing-checkpoint-coordinator-configuration`)

Question: For Flink checkpointing 2.2.0, inspect `CheckpointCoordinatorConfiguration`: inspect checkpoint coordinator configuration options. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.125, retrieval=0, answer=0.25, safety=1`, K2 `combined=0.904167, retrieval=0.933333, answer=0.875, safety=1`, delta `combined=0.779167, retrieval=0.933333, answer=0.625, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.75, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.5, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1; must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 51. Kafka Connect pattern for ConnectorPluginsResource (`kafka-rest-connector-plugins-resource`)

Question: For Kafka Connect REST 4.2.0, inspect `ConnectorPluginsResource`: trace connector plugin validation through the REST resource. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 52. Kafka Connect pattern for AbstractHerder (`kafka-connect-abstract-herder`)

Question: For Kafka Connect 4.2.0, inspect `AbstractHerder`: trace connector configuration validation in the herder layer. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.833333, retrieval=1, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 53. Kafka Connect pattern for DistributedHerder (`kafka-connect-distributed-herder`)

Question: For Kafka Connect 4.2.0, inspect `DistributedHerder`: inspect distributed connector config update behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 54. Kafka Connect pattern for StandaloneHerder (`kafka-connect-standalone-herder`)

Question: For Kafka Connect 4.2.0, inspect `StandaloneHerder`: inspect standalone connector config update behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.833333, retrieval=1, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 55. Kafka Connect pattern for Herder (`kafka-connect-herder`)

Question: For Kafka Connect 4.2.0, inspect `Herder`: identify the connector management interface. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.583333, retrieval=0.666667, answer=0.5, safety=1`, delta `combined=0.333333, retrieval=0.666667, answer=0, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `false`
- MCP calls: `{"k2_answer_with_sources": 1, "k2_search_code": 9, "k2_search_docs": 2, "k2_search_tests": 9}`
- K2 metric scores: `artifact_matches=0.333333, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 2; source URIs: 1; citations: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 56. Kafka Connect pattern for Worker (`kafka-connect-worker`)

Question: For Kafka Connect 4.2.0, inspect `Worker`: trace connector and task lifecycle responsibilities. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.583333, retrieval=0.666667, answer=0.5, safety=1`, delta `combined=0.333333, retrieval=0.666667, answer=0, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `false`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.333333, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 2; source URIs: 1; citations: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 57. Kafka Connect pattern for WorkerConnector (`kafka-connect-worker-connector`)

Question: For Kafka Connect 4.2.0, inspect `WorkerConnector`: inspect connector startup and failure handling. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.833333, retrieval=1, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 58. Kafka Connect pattern for WorkerTask (`kafka-connect-worker-task`)

Question: For Kafka Connect 4.2.0, inspect `WorkerTask`: inspect common task lifecycle behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 59. Kafka Connect pattern for WorkerSinkTask (`kafka-connect-worker-sink-task`)

Question: For Kafka Connect 4.2.0, inspect `WorkerSinkTask`: inspect sink task delivery and commit behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.833333, retrieval=1, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 60. Kafka Connect pattern for WorkerSourceTask (`kafka-connect-worker-source-task`)

Question: For Kafka Connect 4.2.0, inspect `WorkerSourceTask`: inspect source task polling and commit behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.833333, retrieval=1, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1, "k2_search_code": 1, "k2_search_tests": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 61. Kafka Connect pattern for ConnectorConfig (`kafka-connect-connector-config`)

Question: For Kafka Connect 4.2.0, inspect `ConnectorConfig`: explain shared connector configuration validation. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 62. Kafka Connect pattern for SinkConnectorConfig (`kafka-connect-sink-connector-config`)

Question: For Kafka Connect 4.2.0, inspect `SinkConnectorConfig`: inspect sink connector-specific config validation. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.966667, retrieval=0.933333, answer=1, safety=1`, delta `combined=0.716667, retrieval=0.933333, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 63. Kafka Connect pattern for SourceConnectorConfig (`kafka-connect-source-connector-config`)

Question: For Kafka Connect 4.2.0, inspect `SourceConnectorConfig`: inspect source connector-specific config validation. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.833333, retrieval=1, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 64. Kafka Connect pattern for WorkerConfig (`kafka-connect-worker-config`)

Question: For Kafka Connect 4.2.0, inspect `WorkerConfig`: inspect worker-level configuration parsing. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.833333, retrieval=1, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 65. Kafka Connect pattern for DistributedConfig (`kafka-connect-distributed-config`)

Question: For Kafka Connect 4.2.0, inspect `DistributedConfig`: inspect distributed worker configuration behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.833333, retrieval=1, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 66. Kafka Connect pattern for StandaloneConfig (`kafka-connect-standalone-config`)

Question: For Kafka Connect 4.2.0, inspect `StandaloneConfig`: inspect standalone worker configuration behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.083333, retrieval=0, answer=0.166666, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.916667, retrieval=1, answer=0.833334, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.333333, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 67. Kafka Connect pattern for ConfigDef (`kafka-connect-config-def`)

Question: For Kafka Connect 4.2.0, inspect `ConfigDef`: explain Kafka configuration definition and validation semantics. Which version-pinned docs and implementation class should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.55, retrieval=0.6, answer=0.5, safety=1`, delta `combined=0.3, retrieval=0.6, answer=0, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `false`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.5, source_kind_coverage=1, module_hits=0.5, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1; modules: 1; source URIs: 1; citations: 1
- Baseline evidence gaps: artifacts: 2; source kinds: 2; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 68. Kafka Connect pattern for ConfigValue (`kafka-connect-config-value`)

Question: For Kafka Connect 4.2.0, inspect `ConfigValue`: explain validation result representation. Which version-pinned docs and implementation class should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 2; source kinds: 2; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 69. Kafka Connect pattern for ConfigTransformer (`kafka-connect-config-transformer`)

Question: For Kafka Connect 4.2.0, inspect `ConfigTransformer`: inspect externalized configuration transformation behavior. Which version-pinned docs and implementation class should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 2; source kinds: 2; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 70. Kafka Connect pattern for ConfigProvider (`kafka-connect-config-provider`)

Question: For Kafka Connect 4.2.0, inspect `ConfigProvider`: inspect the config provider contract used for externalized secrets. Which version-pinned docs and implementation class should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.833333, retrieval=1, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 2; source kinds: 2; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 71. Kafka Connect pattern for Plugins (`kafka-connect-plugins`)

Question: For Kafka Connect 4.2.0, inspect `Plugins`: trace plugin discovery and connector class loading. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.966667, retrieval=0.933333, answer=1, safety=1`, delta `combined=0.716667, retrieval=0.933333, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 72. Kafka Connect pattern for PluginDesc (`kafka-connect-plugin-desc`)

Question: For Kafka Connect 4.2.0, inspect `PluginDesc`: inspect plugin descriptor metadata. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.833333, retrieval=1, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 73. Kafka Connect pattern for PluginType (`kafka-connect-plugin-type`)

Question: For Kafka Connect 4.2.0, inspect `PluginType`: inspect plugin type classification. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.966667, retrieval=0.933333, answer=1, safety=1`, delta `combined=0.716667, retrieval=0.933333, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 74. Kafka Connect pattern for DelegatingClassLoader (`kafka-connect-delegating-class-loader`)

Question: For Kafka Connect 4.2.0, inspect `DelegatingClassLoader`: inspect plugin classloader delegation behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 75. Kafka Connect pattern for PluginClassLoader (`kafka-connect-plugin-class-loader`)

Question: For Kafka Connect 4.2.0, inspect `PluginClassLoader`: inspect isolated plugin class loading. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.883333, retrieval=0.933333, answer=0.833333, safety=1`, delta `combined=0.633333, retrieval=0.933333, answer=0.333333, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.666667, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1; must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 76. Kafka Connect pattern for PluginScanResult (`kafka-connect-plugin-scan-result`)

Question: For Kafka Connect 4.2.0, inspect `PluginScanResult`: inspect plugin scanning results. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.966667, retrieval=0.933333, answer=1, safety=1`, delta `combined=0.716667, retrieval=0.933333, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 77. Kafka Connect pattern for PluginUtils (`kafka-connect-plugin-utils`)

Question: For Kafka Connect 4.2.0, inspect `PluginUtils`: inspect plugin path and alias helper behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.833333, retrieval=1, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 78. Kafka Connect pattern for ConnectRestServer (`kafka-rest-connect-rest-server`)

Question: For Kafka Connect REST 4.2.0, inspect `ConnectRestServer`: trace Connect REST server wiring. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.833333, retrieval=1, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 79. Kafka Connect pattern for RestServerConfig (`kafka-rest-rest-server-config`)

Question: For Kafka Connect REST 4.2.0, inspect `RestServerConfig`: inspect Connect REST server configuration. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.833333, retrieval=1, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 80. Kafka Connect pattern for ConnectorsResource (`kafka-rest-connectors-resource`)

Question: For Kafka Connect REST 4.2.0, inspect `ConnectorsResource`: trace connector CRUD REST behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.833333, retrieval=1, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 81. Kafka Connect pattern for ConnectorStateInfo (`kafka-rest-connector-state-info`)

Question: For Kafka Connect REST 4.2.0, inspect `ConnectorStateInfo`: inspect connector state response representation. Which version-pinned docs and implementation class should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.916667, retrieval=1, answer=0.833333, safety=1`, delta `combined=0.666667, retrieval=1, answer=0.333333, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.666667, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 2; source kinds: 2; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 82. Kafka Connect pattern for ConnectorInfo (`kafka-rest-connector-info`)

Question: For Kafka Connect REST 4.2.0, inspect `ConnectorInfo`: inspect connector info response representation. Which version-pinned docs and implementation class should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.916667, retrieval=1, answer=0.833333, safety=1`, delta `combined=0.666667, retrieval=1, answer=0.333333, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.666667, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 2; source kinds: 2; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 83. Kafka Connect pattern for CreateConnectorRequest (`kafka-rest-create-connector-request`)

Question: For Kafka Connect REST 4.2.0, inspect `CreateConnectorRequest`: inspect connector creation request validation. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=0.916667, retrieval=1, answer=0.833333, safety=1`, delta `combined=0.75, retrieval=1, answer=0.499999, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.666667, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 84. Kafka Connect pattern for ConnectorType (`kafka-rest-connector-type`)

Question: For Kafka Connect REST 4.2.0, inspect `ConnectorType`: inspect connector type classification. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.833333, retrieval=1, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 85. Kafka Connect pattern for Connector (`kafka-connect-connector`)

Question: For Kafka Connect 4.2.0, inspect `Connector`: inspect the base connector contract. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.933333, retrieval=0.866667, answer=1, safety=1`, delta `combined=0.683333, retrieval=0.866667, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.333333, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 2
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 86. Kafka Connect pattern for SourceConnector (`kafka-connect-source-connector`)

Question: For Kafka Connect 4.2.0, inspect `SourceConnector`: inspect source connector implementation responsibilities. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.966667, retrieval=0.933333, answer=1, safety=1`, delta `combined=0.716667, retrieval=0.933333, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 87. Kafka Connect pattern for SinkConnector (`kafka-connect-sink-connector`)

Question: For Kafka Connect 4.2.0, inspect `SinkConnector`: inspect sink connector implementation responsibilities. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.966667, retrieval=0.933333, answer=1, safety=1`, delta `combined=0.716667, retrieval=0.933333, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 88. Kafka Connect pattern for Transformation (`kafka-connect-transformation`)

Question: For Kafka Connect 4.2.0, inspect `Transformation`: inspect single-message transform behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.083333, retrieval=0, answer=0.166666, safety=1`, K2 `combined=0.933333, retrieval=0.866667, answer=1, safety=1`, delta `combined=0.85, retrieval=0.866667, answer=0.833334, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.333333, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.333333, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 2
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 89. Kafka Connect pattern for HeaderConverter (`kafka-connect-header-converter`)

Question: For Kafka Connect 4.2.0, inspect `HeaderConverter`: inspect header conversion behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=0.966667, retrieval=0.933333, answer=1, safety=1`, delta `combined=0.8, retrieval=0.933333, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 90. Kafka Connect pattern for Converter (`kafka-connect-converter`)

Question: For Kafka Connect 4.2.0, inspect `Converter`: inspect value/key conversion behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.083333, retrieval=0, answer=0.166666, safety=1`, K2 `combined=0.583333, retrieval=0.666667, answer=0.5, safety=1`, delta `combined=0.5, retrieval=0.666667, answer=0.333334, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `false`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.333333, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.333333, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 2; source URIs: 1; citations: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 91. Kafka Connect pattern for Schema (`kafka-connect-schemas`)

Question: For Kafka Connect 4.2.0, inspect `Schema`: inspect Connect schema representation. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.583333, retrieval=0.666667, answer=0.5, safety=1`, delta `combined=0.333333, retrieval=0.666667, answer=0, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `false`
- MCP calls: `{"k2_answer_with_sources": 1, "k2_search_code": 1, "k2_search_tests": 7}`
- K2 metric scores: `artifact_matches=0.333333, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 2; source URIs: 1; citations: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 92. Kafka Connect pattern for SchemaBuilder (`kafka-connect-schema-builder`)

Question: For Kafka Connect 4.2.0, inspect `SchemaBuilder`: inspect Connect schema construction behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=0.966667, retrieval=0.933333, answer=1, safety=1`, delta `combined=0.8, retrieval=0.933333, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 93. Kafka Connect pattern for Struct (`kafka-connect-struct`)

Question: For Kafka Connect 4.2.0, inspect `Struct`: inspect structured Connect data validation. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=0.933333, retrieval=0.866667, answer=1, safety=1`, delta `combined=0.683333, retrieval=0.866667, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1, "k2_search_tests": 1}`
- K2 metric scores: `artifact_matches=0.333333, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 2
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 94. Kafka Connect pattern for SinkRecord (`kafka-connect-sink-record`)

Question: For Kafka Connect 4.2.0, inspect `SinkRecord`: inspect sink record metadata available to connectors. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1

### 95. Kafka Connect pattern for SourceRecord (`kafka-connect-source-record`)

Question: For Kafka Connect 4.2.0, inspect `SourceRecord`: inspect source record construction and partition metadata. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=0.966667, retrieval=0.933333, answer=1, safety=1`, delta `combined=0.8, retrieval=0.933333, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 96. Kafka Connect pattern for ConnectorClientConfigRequest (`kafka-connect-connector-client-config-request`)

Question: For Kafka Connect 4.2.0, inspect `ConnectorClientConfigRequest`: inspect connector client override policy inputs. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=0.966667, retrieval=0.933333, answer=1, safety=1`, delta `combined=0.8, retrieval=0.933333, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1, "k2_search_tests": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 97. Kafka Connect pattern for ConnectorClientConfigOverridePolicy (`kafka-connect-connector-client-config-override-policy`)

Question: For Kafka Connect 4.2.0, inspect `ConnectorClientConfigOverridePolicy`: inspect connector client override validation behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=0.916667, retrieval=1, answer=0.833333, safety=1`, delta `combined=0.75, retrieval=1, answer=0.499999, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.666667, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 98. Kafka Connect pattern for AbstractConnectorClientConfigOverridePolicy (`kafka-connect-abstract-connector-client-config-override-policy`)

Question: For Kafka Connect 4.2.0, inspect `AbstractConnectorClientConfigOverridePolicy`: inspect shared connector client override policy behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.083333, retrieval=0, answer=0.166666, safety=1`, K2 `combined=0.883333, retrieval=0.933333, answer=0.833333, safety=1`, delta `combined=0.8, retrieval=0.933333, answer=0.666667, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=0.666667, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=0.666667, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.333333, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: artifacts: 1; must-mentions: 1
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 2; source URIs: 1; citations: 1

### 99. Kafka Connect pattern for NoneConnectorClientConfigOverridePolicy (`kafka-connect-none-connector-client-config-override-policy`)

Question: For Kafka Connect 4.2.0, inspect `NoneConnectorClientConfigOverridePolicy`: inspect policy behavior when overrides are not allowed. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.166667, retrieval=0, answer=0.333334, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.833333, retrieval=1, answer=0.666666, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=0.666667, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; must-mentions: 1; source URIs: 1; citations: 1

### 100. Kafka Connect pattern for PrincipalConnectorClientConfigOverridePolicy (`kafka-connect-principal-connector-client-config-override-policy`)

Question: For Kafka Connect 4.2.0, inspect `PrincipalConnectorClientConfigOverridePolicy`: inspect principal-only client override validation behavior. Which version-pinned docs, implementation class, and neighboring tests should anchor the answer?

- Score components: baseline `combined=0.25, retrieval=0, answer=0.5, safety=1`, K2 `combined=1, retrieval=1, answer=1, safety=1`, delta `combined=0.75, retrieval=1, answer=0.5, safety=0`
- Answer generated: baseline `true`, K2 `true`
- Pass: baseline `false`, K2 `true`
- MCP calls: `{"k2_answer_with_sources": 1}`
- K2 metric scores: `artifact_matches=1, source_kind_coverage=1, module_hits=1, api_surface_hits=1, must_mention_coverage=1, source_uri_coverage=1, citation_coverage=1, hallucination_markers=1`
- Baseline metric scores: `artifact_matches=0, source_kind_coverage=0, module_hits=0, api_surface_hits=0, must_mention_coverage=1, source_uri_coverage=0, citation_coverage=0, hallucination_markers=1`
- K2 evidence gaps: none
- Baseline evidence gaps: artifacts: 3; source kinds: 3; modules: 2; API surfaces: 1; source URIs: 1; citations: 1
