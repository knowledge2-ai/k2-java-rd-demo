**Recommendation**
- Anchor the answer on the 2.2.0 REST API docs for multipart upload behavior, then tie it to the `FileUploads` helper that owns request-scoped temp-file tracking and cleanup.
- Treat the key behavior as: uploaded files are registered while the REST request is being parsed, then unregistered/deleted on normal completion and on failure paths.

**Implementation anchors**
- Version-pinned docs: the Flink 2.2.0 REST API docs page covering file uploads / multipart requests.
- Implementation class: `FileUploads` in the REST handler stack.
- Lifecycle path: the REST request parsing and handler-completion code that adds uploads to the request-scoped tracker and disposes them afterward.

**Tests to inspect or add**
- The unit test for `FileUploads` itself.
- Nearby REST handler tests that cover:
  - successful request completion
  - parse/validation failure after upload creation
  - handler exception after upload parsing
- Add or extend a regression test that proves uploaded files are deregistered and cleaned up even when the request fails after parsing.

**Citations**
- None confirmed from memory with enough certainty to cite precisely.

**Uncertainties**
- I am not certain of the exact 2.2.0 package path for `FileUploads` (`rest.handler` vs `rest.handler.util`).
- I am also not certain of the exact version-pinned docs URL/path for the multipart upload section, so verify those against the 2.2.0 release tag before using them as hard references.