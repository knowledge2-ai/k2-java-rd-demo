"""Standard-library docs website harvesting for the Java R&D demo."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from collections.abc import Callable, Iterable
from html.parser import HTMLParser
from typing import Any, Literal
from urllib.parse import unquote, urldefrag, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen
from xml.etree import ElementTree

from .assets import DemoDocument
from .metadata import (
    DEMO_DATASET_ID,
    compact_tags,
    infer_api_surface,
    infer_audience,
    infer_topic,
    validate_metadata,
)
from .source_catalog import DocsSourceManifest

FetchText = Callable[[str], str]
DocsExtractor = Literal["direct", "tavily"]

DEFAULT_TIMEOUT_SECONDS = 20
MAX_FETCH_BYTES = 5 * 1024 * 1024  # 5 MB
_ACCEPTED_CONTENT_TYPES = ("text/", "application/xml", "application/xhtml")
MAX_SITEMAPS = 100
TAVILY_MAX_URLS_PER_EXTRACT = 20


class DocsHarvestError(RuntimeError):
    """Raised when docs harvesting cannot complete with the requested backend."""


@dataclass
class HarvestStats:
    """Tracks fetch outcomes during docs harvesting."""

    urls_attempted: int = 0
    urls_succeeded: int = 0
    urls_failed: int = 0
    failures: list[dict[str, str]] = field(default_factory=list)

    def record_failure(self, url: str, error: Exception) -> None:
        self.urls_attempted += 1
        self.urls_failed += 1
        self.failures.append({
            "url": url,
            "error": str(error),
            "type": type(error).__name__,
        })

    def record_success(self) -> None:
        self.urls_attempted += 1
        self.urls_succeeded += 1


@dataclass(frozen=True)
class TavilyExtractOptions:
    api_key: str | None = None
    extract_depth: Literal["basic", "advanced"] = "basic"
    format: Literal["markdown", "text"] = "markdown"
    timeout: float | None = None
    query: str | None = None
    chunks_per_source: int = 3
    batch_size: int = TAVILY_MAX_URLS_PER_EXTRACT


@dataclass(frozen=True)
class ExtractedDocsPage:
    url: str
    text: str
    title: str | None = None
    extraction_provider: str = "direct"
    extraction_format: str = "html"

NOISE_TAGS = {
    "aside",
    "footer",
    "form",
    "header",
    "nav",
    "noscript",
    "script",
    "style",
    "svg",
}

BLOCK_TAGS = {
    "article",
    "blockquote",
    "body",
    "dd",
    "div",
    "dl",
    "dt",
    "figcaption",
    "figure",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "main",
    "ol",
    "p",
    "pre",
    "section",
    "table",
    "td",
    "th",
    "tr",
    "ul",
}

STATIC_SUFFIXES = {
    ".7z",
    ".avif",
    ".bmp",
    ".bz2",
    ".css",
    ".csv",
    ".gif",
    ".gz",
    ".ico",
    ".jar",
    ".jpeg",
    ".jpg",
    ".js",
    ".json",
    ".map",
    ".mp3",
    ".mp4",
    ".pdf",
    ".png",
    ".svg",
    ".tar",
    ".tgz",
    ".txt",
    ".wasm",
    ".webm",
    ".webp",
    ".xml",
    ".zip",
}


def fetch_url_text(url: str) -> str:
    """Fetch text over HTTP using only the standard library."""

    request = Request(
        url,
        headers={"User-Agent": "k2-java-rd-demo-docs-harvest/0.1"},
    )
    with urlopen(request, timeout=DEFAULT_TIMEOUT_SECONDS) as response:
        content_type = response.headers.get("Content-Type", "")
        if not any(content_type.startswith(ct) for ct in _ACCEPTED_CONTENT_TYPES):
            raise ValueError(f"rejected content-type {content_type!r} for {url}")
        data = response.read(MAX_FETCH_BYTES + 1)
        if len(data) > MAX_FETCH_BYTES:
            raise ValueError(f"response exceeds {MAX_FETCH_BYTES} bytes for {url}")
        charset = response.headers.get_content_charset() or "utf-8"
        return data.decode(charset, errors="replace")


def discover_docs_urls(
    source: DocsSourceManifest,
    max_pages: int | None = None,
    fetch_text: FetchText | None = None,
    stats: HarvestStats | None = None,
) -> list[str]:
    """Discover same-host docs URLs from sitemaps, falling back to seed-page links."""

    fetch = fetch_text or fetch_url_text
    allowed_hosts = _allowed_hosts(source.seed_urls)
    sitemap_urls = _discover_urls_from_sitemaps(source, fetch, allowed_hosts, stats=stats)
    candidate_urls = sitemap_urls or _discover_urls_from_seed_html(source, fetch, stats=stats)
    return _filter_urls(candidate_urls, source, allowed_hosts, max_pages=max_pages)


def build_docs_documents(
    source: DocsSourceManifest,
    max_pages: int | None = None,
    fetch_text: FetchText | None = None,
    extractor: DocsExtractor = "direct",
    tavily_options: TavilyExtractOptions | None = None,
    tavily_client: Any | None = None,
    allow_empty: bool = False,
) -> list[DemoDocument]:
    """Build K2-ready demo documents from a docs website manifest.

    Raises ``DocsHarvestError`` when zero documents are produced unless
    *allow_empty* is ``True``.
    """

    stats = HarvestStats()
    fetch = fetch_text or fetch_url_text
    urls = discover_docs_urls(source, max_pages=max_pages, fetch_text=fetch, stats=stats)
    pages = extract_docs_pages(
        urls,
        fetch_text=fetch,
        extractor=extractor,
        tavily_options=tavily_options,
        tavily_client=tavily_client,
    )

    documents: list[DemoDocument] = []
    for page in pages:
        if not page.text:
            continue
        metadata = _build_docs_metadata(
            source,
            page.url,
            text=page.text,
            title=page.title,
            extraction_provider=page.extraction_provider,
            extraction_format=page.extraction_format,
        )
        documents.append(
            DemoDocument(
                source_uri=page.url,
                raw_text=_build_raw_text(
                    page.url,
                    text=page.text,
                    metadata=metadata,
                    title=page.title,
                ),
                metadata=metadata,
            )
        )

    if not documents and not allow_empty:
        raise DocsHarvestError(
            f"zero documents harvested from {source.framework} {source.version} docs "
            f"({len(urls)} URLs discovered, {len(pages)} pages extracted, "
            f"{stats.urls_failed} fetch failures); "
            f"pass allow_empty=True to suppress this error"
        )

    return documents


def extract_docs_pages(
    urls: Iterable[str],
    *,
    fetch_text: FetchText | None = None,
    extractor: DocsExtractor = "direct",
    tavily_options: TavilyExtractOptions | None = None,
    tavily_client: Any | None = None,
) -> list[ExtractedDocsPage]:
    normalized_urls = [url for url in (_normalize_url(url) for url in urls) if url]
    if extractor == "direct":
        fetch = fetch_text or fetch_url_text
        return [_extract_page_direct(url, fetch) for url in normalized_urls]
    if extractor == "tavily":
        return extract_docs_pages_with_tavily(
            normalized_urls,
            options=tavily_options,
            tavily_client=tavily_client,
        )
    raise DocsHarvestError(f"unsupported docs extractor: {extractor}")


def extract_docs_pages_with_tavily(
    urls: Iterable[str],
    *,
    options: TavilyExtractOptions | None = None,
    tavily_client: Any | None = None,
) -> list[ExtractedDocsPage]:
    selected_options = options or TavilyExtractOptions()
    batch_size = max(1, min(selected_options.batch_size, TAVILY_MAX_URLS_PER_EXTRACT))
    client = tavily_client or _build_tavily_client(selected_options.api_key)

    pages: list[ExtractedDocsPage] = []
    for batch in _batched(list(urls), batch_size):
        kwargs: dict[str, Any] = {
            "urls": batch,
            "include_images": False,
            "extract_depth": selected_options.extract_depth,
            "format": selected_options.format,
        }
        if selected_options.timeout is not None:
            kwargs["timeout"] = selected_options.timeout
        if selected_options.query:
            kwargs["query"] = selected_options.query
            kwargs["chunks_per_source"] = selected_options.chunks_per_source

        response = client.extract(**kwargs)
        for result in _response_list(response, "results"):
            url = _normalize_url(str(result.get("url") or ""))
            raw_content = str(result.get("raw_content") or "").strip()
            if url is None or not raw_content:
                continue
            text = _normalize_text(raw_content)
            if not text:
                continue
            pages.append(
                ExtractedDocsPage(
                    url=url,
                    text=text,
                    title=_title_from_extracted_text(text),
                    extraction_provider="tavily",
                    extraction_format=selected_options.format,
                )
            )
    return pages


def html_to_text(html: str) -> str:
    """Convert HTML into readable text while stripping common navigation noise."""

    text, _title = _html_to_text_and_title(html)
    return text


def _discover_urls_from_sitemaps(
    source: DocsSourceManifest,
    fetch: FetchText,
    allowed_hosts: set[str],
    *,
    stats: HarvestStats | None = None,
) -> list[str]:
    urls: list[str] = []
    visited_sitemaps: set[str] = set()
    for sitemap_url in _sitemap_candidates(source.seed_urls):
        urls.extend(_read_sitemap_tree(
            sitemap_url, fetch, allowed_hosts, visited_sitemaps, stats=stats,
        ))
        if len(visited_sitemaps) >= MAX_SITEMAPS:
            break
    return urls


def _read_sitemap_tree(
    sitemap_url: str,
    fetch: FetchText,
    allowed_hosts: set[str],
    visited_sitemaps: set[str],
    *,
    stats: HarvestStats | None = None,
) -> list[str]:
    normalized_url = _normalize_url(sitemap_url)
    if (
        normalized_url is None
        or normalized_url in visited_sitemaps
        or not _same_allowed_host(normalized_url, allowed_hosts)
        or len(visited_sitemaps) >= MAX_SITEMAPS
    ):
        return []

    visited_sitemaps.add(normalized_url)
    sitemap_text = _fetch_optional(fetch, normalized_url, stats=stats)
    if not sitemap_text:
        return []

    parsed = _parse_sitemap_xml(sitemap_text)
    if parsed is None:
        return []

    kind, locations = parsed
    if kind == "urlset":
        return locations

    urls: list[str] = []
    for child_sitemap_url in locations:
        urls.extend(_read_sitemap_tree(
            child_sitemap_url, fetch, allowed_hosts, visited_sitemaps, stats=stats,
        ))
        if len(visited_sitemaps) >= MAX_SITEMAPS:
            break
    return urls


def _discover_urls_from_seed_html(
    source: DocsSourceManifest,
    fetch: FetchText,
    *,
    stats: HarvestStats | None = None,
) -> list[str]:
    urls: list[str] = []
    for seed_url in source.seed_urls:
        normalized_seed = _normalize_url(seed_url)
        if normalized_seed is not None:
            urls.append(normalized_seed)

        html = _fetch_optional(fetch, seed_url, stats=stats)
        if not html:
            continue
        for href in _extract_links(html):
            urls.append(urljoin(seed_url, href))
    return urls


def _sitemap_candidates(seed_urls: Iterable[str]) -> list[str]:
    candidates: list[str] = []
    for seed_url in seed_urls:
        normalized_seed = _normalize_url(seed_url)
        if normalized_seed is None:
            continue
        parsed = urlsplit(normalized_seed)
        lower_path = parsed.path.lower()
        if lower_path.endswith(".xml"):
            candidates.append(normalized_seed)

        if parsed.path.endswith("/"):
            candidates.append(urljoin(normalized_seed, "sitemap.xml"))
        else:
            directory_url = urljoin(normalized_seed, "./")
            candidates.append(urljoin(directory_url, "sitemap.xml"))
            last_segment = parsed.path.rsplit("/", 1)[-1]
            if "." not in last_segment:
                candidates.append(f"{normalized_seed.rstrip('/')}/sitemap.xml")

        candidates.append(urlunsplit((parsed.scheme, parsed.netloc, "/sitemap.xml", "", "")))
    return _unique_preserving_order(candidates)


def _parse_sitemap_xml(xml_text: str) -> tuple[str, list[str]] | None:
    try:
        root = ElementTree.fromstring(xml_text.lstrip())
    except ElementTree.ParseError:
        return None

    root_name = _local_name(root.tag)
    if root_name not in {"sitemapindex", "urlset"}:
        return None

    item_name = "sitemap" if root_name == "sitemapindex" else "url"
    locations: list[str] = []
    for item in root:
        if _local_name(item.tag) != item_name:
            continue
        loc = _first_child_text(item, "loc")
        if loc:
            locations.append(loc)
    return root_name, locations


def _first_child_text(element: ElementTree.Element, child_name: str) -> str | None:
    for child in element:
        if _local_name(child.tag) == child_name and child.text:
            return child.text.strip()
    return None


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def _filter_urls(
    candidate_urls: Iterable[str],
    source: DocsSourceManifest,
    allowed_hosts: set[str],
    *,
    max_pages: int | None,
) -> list[str]:
    if max_pages is not None and max_pages <= 0:
        return []

    urls: list[str] = []
    seen: set[str] = set()
    for candidate_url in candidate_urls:
        normalized_url = _normalize_url(candidate_url)
        if (
            normalized_url is None
            or normalized_url in seen
            or not _same_allowed_host(normalized_url, allowed_hosts)
            or not _allowed_by_manifest_paths(normalized_url, source)
            or not _looks_like_html_page(normalized_url)
        ):
            continue
        seen.add(normalized_url)
        urls.append(normalized_url)

    urls.sort(key=_url_sort_key)
    if max_pages is not None:
        return urls[:max_pages]
    return urls


def _normalize_url(url: str) -> str | None:
    stripped_url = str(url).strip()
    if not stripped_url:
        return None
    without_fragment, _fragment = urldefrag(stripped_url)
    parsed = urlsplit(without_fragment)
    scheme = parsed.scheme.lower()
    if scheme not in {"http", "https"} or not parsed.netloc:
        return None
    path = parsed.path or "/"
    return urlunsplit((scheme, parsed.netloc.lower(), path, parsed.query, ""))


def _allowed_hosts(seed_urls: Iterable[str]) -> set[str]:
    hosts: set[str] = set()
    for seed_url in seed_urls:
        normalized_url = _normalize_url(seed_url)
        if normalized_url is None:
            continue
        hosts.add(urlsplit(normalized_url).netloc.lower())
    return hosts


def _same_allowed_host(url: str, allowed_hosts: set[str]) -> bool:
    if not allowed_hosts:
        return True
    return urlsplit(url).netloc.lower() in allowed_hosts


def _allowed_by_manifest_paths(url: str, source: DocsSourceManifest) -> bool:
    path = _path_for_filtering(url)
    includes = tuple(_normalize_manifest_path(path) for path in source.include_paths)
    excludes = tuple(_normalize_manifest_path(path) for path in source.exclude_paths)

    if includes and not any(_path_matches(path, include_path) for include_path in includes):
        return False
    return not any(_path_matches(path, exclude_path) for exclude_path in excludes)


def _normalize_manifest_path(path: str) -> str:
    return unquote(str(path).strip().lstrip("/"))


def _path_for_filtering(url: str) -> str:
    return unquote(urlsplit(url).path.lstrip("/"))


def _path_matches(path: str, manifest_path: str) -> bool:
    if not manifest_path:
        return True
    if path == manifest_path.rstrip("/"):
        return True
    if path.startswith(manifest_path):
        return True

    haystack = f"/{path}"
    needle = f"/{manifest_path}"
    if manifest_path.endswith("/"):
        return needle in haystack
    return f"{needle}/" in f"{haystack}/"


def _looks_like_html_page(url: str) -> bool:
    path = urlsplit(url).path.lower()
    suffix = ""
    last_segment = path.rsplit("/", 1)[-1]
    if "." in last_segment:
        suffix = "." + last_segment.rsplit(".", 1)[-1]
    return suffix not in STATIC_SUFFIXES


def _url_sort_key(url: str) -> tuple[str, str, str, str]:
    parsed = urlsplit(url)
    return (parsed.scheme, parsed.netloc, parsed.path, parsed.query)


def _fetch_optional(
    fetch: FetchText, url: str, stats: HarvestStats | None = None,
) -> str | None:
    try:
        result = fetch(url)
        if stats is not None:
            stats.record_success()
        return result
    except Exception as exc:
        if stats is not None:
            stats.record_failure(url, exc)
        return None


def _unique_preserving_order(values: Iterable[str]) -> list[str]:
    unique: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        unique.append(value)
    return unique


def _html_to_text_and_title(html: str) -> tuple[str, str | None]:
    parser = _ReadableHTMLParser()
    parser.feed(html)
    parser.close()
    return parser.text(), parser.title()


def _extract_page_direct(url: str, fetch: FetchText) -> ExtractedDocsPage:
    html = fetch(url)
    text, title = _html_to_text_and_title(html)
    return ExtractedDocsPage(url=url, text=text, title=title)


def _build_tavily_client(api_key: str | None) -> Any:
    selected_api_key = api_key or os.environ.get("TAVILY_API_KEY")
    if not selected_api_key:
        raise DocsHarvestError("TAVILY_API_KEY is required when using the Tavily extractor")
    try:
        from tavily import TavilyClient
    except ImportError as exc:
        raise DocsHarvestError(
            "tavily-python is required when using the Tavily extractor; "
            "install the tavily optional dependency"
        ) from exc
    return TavilyClient(api_key=selected_api_key)


def _response_list(response: Any, key: str) -> list[dict[str, Any]]:
    if isinstance(response, dict):
        value = response.get(key)
    else:
        value = getattr(response, key, None)
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, dict)]


def _batched(values: list[str], batch_size: int) -> Iterable[list[str]]:
    for index in range(0, len(values), batch_size):
        yield values[index : index + batch_size]


def _title_from_extracted_text(text: str) -> str | None:
    for line in text.splitlines()[:20]:
        stripped = line.strip()
        if not stripped:
            continue
        markdown_title = stripped.lstrip("#").strip()
        markdown_title = re.sub(r"\s+\[#\]\([^)]*\)\s*$", "", markdown_title).strip()
        if stripped.startswith("#") and markdown_title:
            return markdown_title[:200]
    return None


class _LinkHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "a":
            return
        for name, value in attrs:
            if name.lower() == "href" and value:
                self.links.append(value.strip())
                return


def _extract_links(html: str) -> list[str]:
    parser = _LinkHTMLParser()
    parser.feed(html)
    parser.close()
    return parser.links


class _ReadableHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._parts: list[str] = []
        self._title_parts: list[str] = []
        self._skip_depth = 0
        self._title_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag_name = tag.lower()
        if self._skip_depth:
            if tag_name in NOISE_TAGS:
                self._skip_depth += 1
            return
        if tag_name in NOISE_TAGS:
            self._skip_depth = 1
            return
        if tag_name == "title":
            self._title_depth += 1
            return
        if tag_name == "br":
            self._append_break()
            return
        if tag_name == "li":
            self._append_break()
            self._parts.append("- ")
            return
        if tag_name in BLOCK_TAGS:
            self._append_break()

    def handle_endtag(self, tag: str) -> None:
        tag_name = tag.lower()
        if self._skip_depth:
            if tag_name in NOISE_TAGS:
                self._skip_depth -= 1
            return
        if tag_name == "title":
            self._title_depth = max(0, self._title_depth - 1)
            return
        if tag_name in BLOCK_TAGS or tag_name == "li":
            self._append_break()

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        if self._title_depth:
            self._title_parts.append(data)
            return
        if data.strip():
            self._parts.append(data)

    def text(self) -> str:
        return _normalize_text("".join(self._parts))

    def title(self) -> str | None:
        title = _normalize_text("".join(self._title_parts))
        return title or None

    def _append_break(self) -> None:
        if not self._parts or self._parts[-1].endswith("\n"):
            return
        self._parts.append("\n")


def _normalize_text(text: str) -> str:
    collapsed = re.sub(r"[ \t\r\f\v]+", " ", text)
    collapsed = re.sub(r" *\n *", "\n", collapsed)
    collapsed = re.sub(r"\n{3,}", "\n\n", collapsed)

    lines: list[str] = []
    for raw_line in collapsed.splitlines():
        line = raw_line.strip()
        if line:
            lines.append(line)
        elif lines and lines[-1]:
            lines.append("")
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def _build_docs_metadata(
    source: DocsSourceManifest,
    url: str,
    *,
    text: str,
    title: str | None,
    extraction_provider: str = "direct",
    extraction_format: str = "html",
) -> dict[str, Any]:
    path = _metadata_path(url)
    api_surface = infer_api_surface(path, text)
    topic = infer_topic(api_surface, "docs")
    metadata: dict[str, Any] = {
        "demo_dataset_id": DEMO_DATASET_ID,
        "corpus_role": "docs",
        "framework": source.framework,
        "framework_version": source.version,
        "source_kind": "docs",
        "artifact_type": "reference",
        "language": extraction_format if extraction_format in {"html", "markdown"} else "text",
        "license": "apache-2.0",
        "repo": source.repo,
        "repo_ref": source.repo_ref,
        "path": path,
        "module": "docs",
        "api_surface": api_surface,
        "topic": topic,
        "audience": infer_audience("docs", api_surface),
        "stability": "public_api",
        "tags": compact_tags(source.framework, source.version, "docs", api_surface, topic),
        "corpus_name": source.corpus_name,
        "doc_type": source.doc_type,
        "extraction_provider": extraction_provider,
        "extraction_format": extraction_format,
    }
    if title:
        metadata["title"] = title[:200]

    validate_metadata(metadata)
    return metadata


def _metadata_path(url: str) -> str:
    parsed = urlsplit(url)
    path = unquote(parsed.path.lstrip("/"))
    if not path:
        return "index.html"
    if path.endswith("/"):
        return f"{path}index.html"
    return path


def _build_raw_text(
    url: str,
    *,
    text: str,
    metadata: dict[str, Any],
    title: str | None,
) -> str:
    lines = [
        f"URL: {url}",
        f"Repository: {metadata['repo']}",
        f"Ref: {metadata['repo_ref']}",
        f"Path: {metadata['path']}",
        f"Framework: {metadata['framework']} {metadata['framework_version']}",
        f"Source kind: {metadata['source_kind']}",
        f"API surface: {metadata['api_surface']}",
    ]
    if title:
        lines.insert(0, f"Title: {title}")
    return "\n".join(lines) + "\n\n" + text


__all__ = [
    "DocsHarvestError",
    "ExtractedDocsPage",
    "FetchText",
    "HarvestStats",
    "MAX_FETCH_BYTES",
    "TavilyExtractOptions",
    "build_docs_documents",
    "discover_docs_urls",
    "extract_docs_pages",
    "extract_docs_pages_with_tavily",
    "fetch_url_text",
    "html_to_text",
]
