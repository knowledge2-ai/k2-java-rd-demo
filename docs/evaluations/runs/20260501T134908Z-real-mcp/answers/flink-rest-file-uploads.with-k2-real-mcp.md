**Recommendation**
Anchor the answer on the Flink 2.2.0 REST API docs, the `FileUploads` implementation in `flink-runtime`, and the dedicated `FileUploadsTest`. The strongest doc anchor is the core REST API page plus its “Developing” section, which points implementation work to `flink-runtime` and the REST handler model [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001) [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002).

**Implementation anchors**
- Version-pinned docs: `flink/flink-docs-release-2.2/docs/ops/rest_api/index.html` for the REST API overview and development guidance [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001).
- Implementation class: `flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/FileUploads.java`, `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/FileUploads.java`.
- Behavior anchor from the implementation snippet: `FileUploads` is a container for uploaded files, supports directory cleanup on `close()`, and has an `EMPTY` singleton.
- If you need the broader REST backend context, the docs explicitly say the REST backend lives in `flink-runtime` and is routed through `WebMonitorEndpoint` [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002).

**Tests to inspect or add**
- Existing direct test anchor: `flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/FileUploadsTest.java`, `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/FileUploadsTest.java`.
- This test already covers the key tracking behavior surfaced by K2: relative-path rejection and directory scanning/collection.
- If you add coverage, keep it adjacent to `FileUploadsTest` and focus on uploaded-file tracking edge cases: nested directory traversal, duplicate file handling if applicable, and cleanup on `close()`.

**Citations**
- Docs: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0001)
- Docs developing section: [https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002](https://nightlies.apache.org/flink/flink-docs-release-2.2/docs/ops/rest_api/#part-0002)
- Implementation: `repo://apache/flink@release-2.2.0/flink-runtime/src/main/java/org/apache/flink/runtime/rest/handler/FileUploads.java`
- Test: `repo://apache/flink@release-2.2.0/flink-runtime/src/test/java/org/apache/flink/runtime/rest/handler/FileUploadsTest.java`

**Uncertainties**
- K2 surfaced a strong direct test anchor only for `FileUploadsTest`; it did not return a richer set of neighboring REST-handler tests specifically around `FileUploads`.
- The doc evidence is version-pinned and relevant to REST handler architecture, but it does not name `FileUploads` explicitly; the direct `FileUploads` contract comes from the implementation and test sources.
