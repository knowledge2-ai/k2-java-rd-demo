**Recommendation**
Use `CANONICAL` as the default recommendation for savepoints. It is the portable, forward-compatible choice and is the right answer for most checkpointing/savepoint guidance.

Use `NATIVE` only when you explicitly want backend-specific savepoints and accept the tradeoff that restores are less portable and more tightly coupled to the state backend.

**Implementation anchors**
- `flink-core/src/main/java/org/apache/flink/core/execution/SavepointFormatType.java`
- `flink-core/src/main/java/org/apache/flink/configuration/CheckpointingOptions.java` if you want the config surface that exposes the enum
- Version-pinned docs for Flink `2.2.x`: the savepoints page under the release-2.2 docs tree, typically `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/savepoints/`

**Tests to inspect or add**
- `flink-core/src/test/java/org/apache/flink/core/execution/SavepointFormatTypeTest.java` if present
- A neighboring enum/config test in the same package, typically around `CheckpointingOptions` or `CheckpointFormatType`
- Add or extend a focused test that asserts:
  - the allowed enum values
  - the default is `CANONICAL` if that is what 2.2.0 exposes
  - the config option round-trips the selected format

**Citations**
- Apache Flink 2.2 release docs: `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/state/savepoints/`
- Source: `flink-core/src/main/java/org/apache/flink/core/execution/SavepointFormatType.java`
- Nearby test anchor: `flink-core/src/test/java/org/apache/flink/core/execution/SavepointFormatTypeTest.java`

**Uncertainties**
- I’m not fully certain the public docs URL is rendered with that exact trailing path versus a nearby variant in the 2.2.0 site, but it should be under the `flink-docs-release-2.2` tree.
- I’m not fully certain whether the repo has a dedicated `SavepointFormatTypeTest` in 2.2.0 or only adjacent config tests; the correct package to inspect is still `org.apache.flink.core.execution`.
- If you need line-precise behavior for 2.2.0, verify against the `release-2.2` tag because minor-version defaults and config wiring can drift.