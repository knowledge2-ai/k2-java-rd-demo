**Recommendation**
- Anchor the answer on the Flink `2.2.0` release docs for checkpointing/state backends, then read the `KeyedStateBackend` Javadoc and the keyed-backend implementation that actually owns snapshot orchestration.
- The checkpointing responsibility split is:
  - `KeyedStateBackend` defines the contract for keyed-state access and checkpoint participation.
  - `AbstractKeyedStateBackend` centralizes snapshot orchestration and common lifecycle hooks.
  - The concrete backend handles the actual state materialization/snapshot format.

**Implementation anchors**
- `org.apache.flink.runtime.state.KeyedStateBackend`  
- `org.apache.flink.runtime.state.AbstractKeyedStateBackend`
- Concrete backend to inspect next:
  - `org.apache.flink.runtime.state.heap.HeapKeyedStateBackend` for heap state
  - or the backend-specific subclass you actually use for RocksDB / changelog / etc.
- Methods to focus on:
  - `snapshot(...)`
  - `notifyCheckpointComplete(...)`
  - `notifyCheckpointAborted(...)`
  - state registration / current-key / key-group handling
  - restore / dispose paths

**Tests to inspect or add**
- Existing neighboring tests to read first:
  - `flink-runtime/src/test/java/org/apache/flink/runtime/state/AbstractKeyedStateBackendTest.java`
  - `flink-runtime/src/test/java/org/apache/flink/runtime/state/heap/HeapKeyedStateBackendTest.java`
- Add or extend coverage for:
  - snapshot consistency while keyed state is mutating
  - restore from the produced `KeyedStateHandle`
  - checkpoint completion / abort lifecycle behavior
  - backend-specific snapshot semantics if you are not on heap state

**Citations**
- `https://github.com/apache/flink/blob/release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/KeyedStateBackend.java`
- `https://github.com/apache/flink/blob/release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/AbstractKeyedStateBackend.java`
- `https://github.com/apache/flink/blob/release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/state/heap/HeapKeyedStateBackend.java`
- `https://github.com/apache/flink/blob/release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/state/heap/HeapKeyedStateBackendTest.java`

**Uncertainties**
- I am confident in the class split above, but I cannot verify the exact 2.2.0 docs URL or every neighboring test name without browsing.
- If your target backend is not heap-based, the most relevant concrete implementation and test class will differ, but the same checkpointing responsibilities still apply.