**Recommendation**
- Explain `CheckpointProperties` as the runtime carrier for checkpoint lifecycle policy, not as storage format metadata.
- For Flink 2.2.0, the key distinction is:
  - regular checkpoints derive `discard*` behavior from the configured retention policy;
  - savepoints are retained snapshots and should not be auto-discarded by subsumption, cancellation, failure, suspension, or normal completion.
- If you mention savepoint variants, keep the wording conservative: the exact branch for forced or unclaimed savepoints should be verified against the factory methods in the 2.2.0 code.

**Implementation anchors**
- Version-pinned docs: Flink 2.2 checkpointing docs and savepoints docs.
- Implementation class: `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointProperties.java`
- Neighboring model classes to read with it: `CheckpointRetentionPolicy`, `CheckpointType`, and any savepoint-type factory in the same package.
- Flag-level summary to anchor the prose:
  - `discardSubsumed`
  - `discardFinished`
  - `discardCancelled`
  - `discardFailed`
  - `discardSuspended`
  - savepoint indicator / forced-savepoint handling
- The practical rule to state: savepoints override the normal cleanup lifecycle; checkpoints follow the retention policy.

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointPropertiesTest.java`
- Adjacent tests in `org.apache.flink.runtime.checkpoint` that exercise checkpoint/savepoint factories.
- Add or verify coverage for:
  - default checkpoint retention mapping
  - externalized checkpoint cleanup behavior
  - savepoint retention behavior
  - forced savepoint behavior
  - unclaimed savepoint behavior if that path exists in 2.2.0

**Citations**
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointProperties.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointPropertiesTest.java`

**Uncertainties**
- I am not fully certain whether 2.2.0 exposes an explicit unclaimed-savepoint branch directly in `CheckpointProperties` or via adjacent savepoint classes, so verify the factory methods before writing exact docs text.
- I am not giving a hard docs URL because the version-pinned public path can vary by Flink docs site generation; use the 2.2 checkpointing and savepoints pages when you anchor the narrative.