**Recommendation**
- Anchor the explanation on the Flink 2.2.0 checkpointing docs for user-facing semantics, then use `CheckpointRequestDecider` as the implementation source of truth for when a request is triggered immediately versus deferred.
- The decision point is effectively: trigger now, delay until eligibility, or suppress because checkpointing state makes a new request invalid or redundant.

**Implementation anchors**
- `CheckpointRequestDecider` in the runtime checkpoint package is the class to inspect first.
- The key scheduling inputs to look for are:
  - whether a checkpoint is already pending or running
  - minimum pause / interval constraints between checkpoints
  - scheduler enabled/disabled state
  - whether a request should be coalesced into an existing scheduled trigger
- Read it together with the coordinator path that consumes its decision, since the decider schedules; the coordinator actually performs the trigger.

**Tests to inspect or add**
- `CheckpointRequestDeciderTest` for unit coverage of the branch table:
  - immediate trigger
  - delayed trigger
  - suppressed request while another checkpoint is active
  - boundary cases around timing
- `CheckpointCoordinatorTest` for integration behavior:
  - completion and rescheduling
  - cancellation / failure transitions
  - repeated requests while a checkpoint is in flight
- Add or extend tests for exact boundary timestamps and duplicate request coalescing.

**Citations**
- `https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/dev/datastream/fault-tolerance/checkpointing/`
- `flink-runtime/src/main/java/org/apache/flink/runtime/checkpoint/CheckpointRequestDecider.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointRequestDeciderTest.java`
- `flink-runtime/src/test/java/org/apache/flink/runtime/checkpoint/CheckpointCoordinatorTest.java`

**Uncertainties**
- I am not certain of the exact method names or returned decision type without inspecting the 2.2.0 source.
- If the branch/tag layout moved late in the release cycle, the exact docs URL or test file set may differ slightly, but the runtime checkpoint package and `CheckpointRequestDecider` are still the right anchors.