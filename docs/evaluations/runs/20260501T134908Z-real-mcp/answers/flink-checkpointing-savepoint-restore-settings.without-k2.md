**Recommendation**
- For Flink 2.2.0 upgrades, treat `SavepointRestoreSettings` as the job-submission contract for restoring an upgraded job from a savepoint, not as checkpointing state itself.
- Use a savepoint path plus `allowNonRestoredState=false` when you want the upgrade to fail on any missing state mapping.
- Use `allowNonRestoredState=true` only when you intentionally drop operators or state during the upgrade.
- In practice, the answer should distinguish “restart from savepoint” from “normal checkpoint recovery.”

**Implementation anchors**
- Version-pinned docs: the Flink 2.2 savepoints docs under the release-2.2 docs tree.
- Implementation class: `org.apache.flink.runtime.jobgraph.SavepointRestoreSettings`.
- Behavior to call out: factory methods for “no savepoint restore” vs “restore from path,” with the non-restored-state flag controlling strictness during restore.

**Tests to inspect or add**
- `flink-runtime/src/test/java/org/apache/flink/runtime/jobgraph/SavepointRestoreSettingsTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/jobgraph/JobGraphTest.java`
- If upgrade semantics are not already covered, add a round-trip test that submits a `JobGraph` with savepoint settings and asserts strict restore fails when mappings are missing, while the non-strict path succeeds.

**Citations**
- `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/savepoints/`
- `flink-runtime/src/main/java/org/apache/flink/runtime/jobgraph/SavepointRestoreSettings.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/jobgraph/SavepointRestoreSettingsTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/jobgraph/JobGraphTest.java`

**Uncertainties**
- I’m confident about the runtime class/package and the upgrade semantics, but I’m not fully certain whether Flink 2.2.0’s `SavepointRestoreSettings` also carries a restore-mode enum in addition to path and `allowNonRestoredState`.
- I’m also not fully certain whether the docs URL is exactly the `flink-docs-release-2.2` path or a nearby 2.2.0 variant.