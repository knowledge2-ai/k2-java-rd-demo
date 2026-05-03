from __future__ import annotations

import unittest
from email.message import Message
from unittest.mock import patch

from tests import _paths  # noqa: F401

from k2_java_rd_demo.docs_harvest import (
    DocsHarvestError,
    HarvestStats,
    MAX_FETCH_BYTES,
    TavilyExtractOptions,
    build_docs_documents,
    discover_docs_urls,
    extract_docs_pages_with_tavily,
    fetch_url_text,
    html_to_text,
)
from k2_java_rd_demo.source_catalog import DocsSourceManifest


def manifest(
    *,
    seed_urls: tuple[str, ...] = ("https://docs.example/current/",),
    include_paths: tuple[str, ...] = ("current/",),
    exclude_paths: tuple[str, ...] = (),
) -> DocsSourceManifest:
    return DocsSourceManifest(
        framework="flink",
        version="2.2.0",
        repo="apache/flink",
        repo_ref="release-2.2.0",
        corpus_name="flink-docs-2.2",
        seed_urls=seed_urls,
        include_paths=include_paths,
        exclude_paths=exclude_paths,
    )


def fake_fetcher(pages: dict[str, str]):
    def fetch(url: str) -> str:
        return pages[url]

    return fetch


class FakeTavilyClient:
    def __init__(self, raw_content_by_url: dict[str, str]) -> None:
        self.raw_content_by_url = raw_content_by_url
        self.calls = []

    def extract(self, **kwargs):
        self.calls.append(kwargs)
        return {
            "results": [
                {"url": url, "raw_content": self.raw_content_by_url[url]}
                for url in kwargs["urls"]
                if url in self.raw_content_by_url
            ],
            "failed_results": [],
        }


class DocsHarvestTests(unittest.TestCase):
    def test_discovers_sitemap_index_and_flat_urlsets_deterministically(self) -> None:
        pages = {
            "https://docs.example/current/sitemap.xml": """
                <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                  <sitemap><loc>https://docs.example/current/part-b.xml</loc></sitemap>
                  <sitemap><loc>https://docs.example/current/part-a.xml</loc></sitemap>
                </sitemapindex>
            """,
            "https://docs.example/current/part-a.xml": """
                <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                  <url><loc>https://docs.example/current/z.html</loc></url>
                  <url><loc>https://other.example/current/a.html</loc></url>
                  <url><loc>https://docs.example/current/private/hidden.html</loc></url>
                </urlset>
            """,
            "https://docs.example/current/part-b.xml": """
                <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                  <url><loc>https://docs.example/current/b.html#section</loc></url>
                  <url><loc>https://docs.example/current/a.html</loc></url>
                  <url><loc>https://docs.example/current/site.css</loc></url>
                </urlset>
            """,
        }

        urls = discover_docs_urls(
            manifest(exclude_paths=("current/private/",)),
            max_pages=2,
            fetch_text=fake_fetcher(pages),
        )

        self.assertEqual(
            urls,
            [
                "https://docs.example/current/a.html",
                "https://docs.example/current/b.html",
            ],
        )

    def test_direct_flat_sitemap_seed_is_supported(self) -> None:
        pages = {
            "https://docs.example/sitemap.xml": """
                <urlset>
                  <url><loc>https://docs.example/current/rest.html</loc></url>
                  <url><loc>https://docs.example/old/rest.html</loc></url>
                </urlset>
            """,
        }

        urls = discover_docs_urls(
            manifest(seed_urls=("https://docs.example/sitemap.xml",)),
            fetch_text=fake_fetcher(pages),
        )

        self.assertEqual(urls, ["https://docs.example/current/rest.html"])

    def test_falls_back_to_same_site_seed_links_when_sitemap_is_missing(self) -> None:
        pages = {
            "https://docs.example/docs/index.html": """
                <html><body>
                  <a href="guide.html#top">Guide</a>
                  <a href="/docs/api.html">API</a>
                  <a href="/private/hidden.html">Hidden</a>
                  <a href="https://other.example/docs/external.html">External</a>
                  <a href="/docs/image.png">Image</a>
                </body></html>
            """,
        }

        urls = discover_docs_urls(
            manifest(
                seed_urls=("https://docs.example/docs/index.html",),
                include_paths=("docs/",),
                exclude_paths=("private/",),
            ),
            fetch_text=fake_fetcher(pages),
        )

        self.assertEqual(
            urls,
            [
                "https://docs.example/docs/api.html",
                "https://docs.example/docs/guide.html",
                "https://docs.example/docs/index.html",
            ],
        )

    def test_html_to_text_strips_navigation_scripts_and_styles(self) -> None:
        text = html_to_text(
            """
            <html>
              <head><title>REST Docs</title><style>.hidden { display: none; }</style></head>
              <body>
                <nav>Previous Next Search</nav>
                <main>
                  <h1>REST Endpoint</h1>
                  <p>Route registration &amp; response body classes.</p>
                  <ul><li>Validate parameters</li><li>Return errors</li></ul>
                </main>
                <script>window.noise = true;</script>
              </body>
            </html>
            """
        )

        self.assertIn("REST Endpoint", text)
        self.assertIn("Route registration & response body classes.", text)
        self.assertIn("- Validate parameters", text)
        self.assertNotIn("Previous Next Search", text)
        self.assertNotIn("window.noise", text)
        self.assertNotIn("display: none", text)

    def test_build_docs_documents_returns_valid_demo_documents(self) -> None:
        pages = {
            "https://docs.example/current/sitemap.xml": """
                <urlset>
                  <url><loc>https://docs.example/current/rest-api.html</loc></url>
                  <url><loc>https://docs.example/current/checkpointing.html</loc></url>
                </urlset>
            """,
            "https://docs.example/current/rest-api.html": """
                <html>
                  <head><title>REST API</title></head>
                  <body><main><h1>REST API</h1><p>Handlers register endpoint routes.</p></main></body>
                </html>
            """,
            "https://docs.example/current/checkpointing.html": """
                <html>
                  <head><title>Checkpointing</title></head>
                  <body><main><h1>Checkpointing</h1><p>Savepoint and checkpoint docs.</p></main></body>
                </html>
            """,
        }

        documents = build_docs_documents(manifest(), fetch_text=fake_fetcher(pages))

        self.assertEqual(len(documents), 2)
        first = documents[0]
        item = first.to_k2_item()
        self.assertEqual(item["source_uri"], "https://docs.example/current/checkpointing.html")
        self.assertIn("URL: https://docs.example/current/checkpointing.html", first.raw_text)

        metadata = first.metadata
        self.assertEqual(metadata["corpus_role"], "docs")
        self.assertEqual(metadata["source_kind"], "docs")
        self.assertEqual(metadata["repo"], "apache/flink")
        self.assertEqual(metadata["repo_ref"], "release-2.2.0")
        self.assertEqual(metadata["framework"], "flink")
        self.assertEqual(metadata["framework_version"], "2.2.0")
        self.assertEqual(metadata["language"], "html")
        self.assertEqual(metadata["module"], "docs")
        self.assertEqual(metadata["api_surface"], "checkpointing")
        self.assertEqual(metadata["path"], "current/checkpointing.html")
        self.assertEqual(metadata["title"], "Checkpointing")
        self.assertIn("docs", metadata["tags"])
        self.assertIn("checkpointing", metadata["tags"])

    def test_tavily_extract_backend_preserves_url_order_and_options(self) -> None:
        client = FakeTavilyClient(
            {
                "https://docs.example/current/a.html": "# REST API\n\nRoute registration.",
                "https://docs.example/current/b.html": "# Checkpointing\n\nState backend notes.",
            }
        )

        pages = extract_docs_pages_with_tavily(
            [
                "https://docs.example/current/a.html",
                "https://docs.example/current/b.html",
            ],
            options=TavilyExtractOptions(
                extract_depth="advanced",
                format="markdown",
                timeout=12.0,
                query="Flink controller-like endpoint docs",
                chunks_per_source=2,
                batch_size=1,
            ),
            tavily_client=client,
        )

        self.assertEqual([page.url for page in pages], [
            "https://docs.example/current/a.html",
            "https://docs.example/current/b.html",
        ])
        self.assertEqual(pages[0].title, "REST API")
        self.assertEqual(pages[0].extraction_provider, "tavily")
        self.assertEqual(len(client.calls), 2)
        self.assertEqual(client.calls[0]["extract_depth"], "advanced")
        self.assertEqual(client.calls[0]["format"], "markdown")
        self.assertEqual(client.calls[0]["query"], "Flink controller-like endpoint docs")
        self.assertEqual(client.calls[0]["chunks_per_source"], 2)

    def test_build_docs_documents_can_use_tavily_extracted_markdown(self) -> None:
        pages = {
            "https://docs.example/current/sitemap.xml": """
                <urlset>
                  <url><loc>https://docs.example/current/rest-api.html</loc></url>
                </urlset>
            """,
        }
        client = FakeTavilyClient(
            {
                "https://docs.example/current/rest-api.html": (
                    "# REST API\n\nHandlers register endpoint routes."
                ),
            }
        )

        documents = build_docs_documents(
            manifest(),
            fetch_text=fake_fetcher(pages),
            extractor="tavily",
            tavily_client=client,
        )

        self.assertEqual(len(documents), 1)
        metadata = documents[0].metadata
        self.assertEqual(metadata["language"], "markdown")
        self.assertEqual(metadata["extraction_provider"], "tavily")
        self.assertEqual(metadata["extraction_format"], "markdown")
        self.assertEqual(metadata["title"], "REST API")
        self.assertIn("Handlers register endpoint routes.", documents[0].raw_text)


    def test_zero_docs_raises_by_default(self) -> None:
        pages = {
            "https://docs.example/current/sitemap.xml": """
                <urlset>
                  <url><loc>https://docs.example/current/empty.html</loc></url>
                </urlset>
            """,
            "https://docs.example/current/empty.html": "<html><body></body></html>",
        }

        with self.assertRaises(DocsHarvestError) as ctx:
            build_docs_documents(manifest(), fetch_text=fake_fetcher(pages))
        self.assertIn("zero documents", str(ctx.exception))

    def test_allow_empty_suppresses_error(self) -> None:
        pages = {
            "https://docs.example/current/sitemap.xml": """
                <urlset>
                  <url><loc>https://docs.example/current/empty.html</loc></url>
                </urlset>
            """,
            "https://docs.example/current/empty.html": "<html><body></body></html>",
        }

        documents = build_docs_documents(
            manifest(), fetch_text=fake_fetcher(pages), allow_empty=True,
        )
        self.assertEqual(documents, [])

    def test_fetch_failure_tracked_in_stats(self) -> None:
        stats = HarvestStats()

        def failing_fetch(url: str) -> str:
            if "bad" in url:
                raise ConnectionError("simulated failure")
            return "<html><body>content</body></html>"

        from k2_java_rd_demo.docs_harvest import _fetch_optional

        result_ok = _fetch_optional(failing_fetch, "https://example.com/good", stats)
        result_bad = _fetch_optional(failing_fetch, "https://example.com/bad", stats)

        self.assertIsNotNone(result_ok)
        self.assertIsNone(result_bad)
        self.assertEqual(stats.urls_attempted, 2)
        self.assertEqual(stats.urls_succeeded, 1)
        self.assertEqual(stats.urls_failed, 1)
        self.assertEqual(stats.failures[0]["url"], "https://example.com/bad")
        self.assertEqual(stats.failures[0]["type"], "ConnectionError")

    @patch("k2_java_rd_demo.docs_harvest.urlopen")
    def test_non_text_content_type_rejected(self, mock_urlopen) -> None:
        headers = Message()
        headers["Content-Type"] = "application/octet-stream"
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.headers = headers

        with self.assertRaises(ValueError) as ctx:
            fetch_url_text("https://example.com/binary.bin")
        self.assertIn("rejected content-type", str(ctx.exception))
        self.assertIn("application/octet-stream", str(ctx.exception))

    @patch("k2_java_rd_demo.docs_harvest.urlopen")
    def test_oversized_response_rejected(self, mock_urlopen) -> None:
        headers = Message()
        headers["Content-Type"] = "text/html; charset=utf-8"
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.headers = headers
        mock_response.read.return_value = b"x" * (MAX_FETCH_BYTES + 1)

        with self.assertRaises(ValueError) as ctx:
            fetch_url_text("https://example.com/huge.html")
        self.assertIn(f"exceeds {MAX_FETCH_BYTES} bytes", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
