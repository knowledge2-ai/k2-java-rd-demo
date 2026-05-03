**Recommendation**
`StateBackend` is the checkpointing policy boundary: it determines how task state is materialized into checkpointable artifacts, what restore metadata is emitted, and how backend-specific storage/snapshot handles are created. It does not own checkpoint triggering, barrier alignment, or completion orchestration; those live in the checkpointing runtime. For Flink 2.2.0, treat method-level behavior as version-sensitive and verify against source before relying on exact seams with `CheckpointStorage`.

**Implementation anchors**
- Version-pinned docs: Flink 2.2 state backends documentation page.
- Core source: `flink-runtime/src/main/java/org/apache/flink/runtime/state/StateBackend.java`
- Concrete backends to trace the checkpoint flow through:
  - `HashMapStateBackend`
  - `EmbeddedRocksDBStateBackend`
- Follow the call path from backend selection into keyed/operator state snapshot creation and restore handle generation.

**Tests to inspect or add**
- Neighboring tests in `flink-runtime/src/test/java/org/apache/flink/runtime/state/` that cover backend loading/configuration and checkpoint storage selection.
- Backend-specific snapshot/restore tests for `HashMapStateBackend` and `EmbeddedRocksDBStateBackend`.
- Add a regression test that asserts the backend emits checkpointable state handles/metadata and can restore from them.

**Citations**
- Flink 2.2 state backends docs: `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/state_backends/`
- `StateBackend.java`: `flink-runtime/src/main/java/org/apache/flink/runtime/state/StateBackend.java`

**Uncertainties**
- I’m not fully certain whether Flink 2.2.0 treats `StateBackend` as the primary checkpointing seam or as a thinner compatibility layer over `CheckpointStorage` plus concrete keyed/operator backends.
- I would verify the exact concrete backend class paths and the most relevant neighboring test names in the 2.2.0 branch before turning this into a code-level citation set.