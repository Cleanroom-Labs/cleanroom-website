"""Tests for BaseExtractor HTML processing methods."""

from pathlib import Path

from bs4 import BeautifulSoup

from extractors.base import BaseExtractor, ContentSection
from config import Config


class ConcreteExtractor(BaseExtractor):
    """Concrete implementation for testing abstract base class."""
    def extract(self):
        return []


class TestStripElements:
    def test_removes_nav_elements(self, config):
        html = """
        <html><body>
          <nav>Nav content</nav>
          <footer>Footer</footer>
          <script>var x = 1;</script>
          <style>.foo {}</style>
          <div role="main"><p>Main content</p></div>
        </body></html>
        """
        soup = BeautifulSoup(html, "html.parser")
        ext = ConcreteExtractor(config)
        result = ext.strip_elements(soup)

        assert result.find("nav") is None
        assert result.find("footer") is None
        assert result.find("script") is None
        assert result.find("style") is None
        assert "Main content" in result.get_text()

    def test_preserves_content_when_no_nav(self, config):
        html = '<div role="main"><p>Content here</p></div>'
        soup = BeautifulSoup(html, "html.parser")
        ext = ConcreteExtractor(config)
        result = ext.strip_elements(soup)

        assert "Content here" in result.get_text()


class TestExtractMainContent:
    def test_primary_selector(self, config):
        html = '<div role="main"><p>Primary content</p></div>'
        soup = BeautifulSoup(html, "html.parser")
        ext = ConcreteExtractor(config)
        content = ext.extract_main_content(soup)

        assert content is not None
        assert "Primary content" in content.get_text()

    def test_fallback_selector(self, config):
        html = '<div class="rst-content"><p>Fallback content</p></div>'
        soup = BeautifulSoup(html, "html.parser")
        ext = ConcreteExtractor(config)
        content = ext.extract_main_content(soup)

        assert content is not None
        assert "Fallback content" in content.get_text()

    def test_returns_none_when_missing(self, config):
        html = "<div><p>No matching selector</p></div>"
        soup = BeautifulSoup(html, "html.parser")
        ext = ConcreteExtractor(config)
        content = ext.extract_main_content(soup)

        assert content is None


class TestTransformLinks:
    def test_external_link_gets_arrow(self, config, tmp_path):
        html = '<a href="https://example.com">Example</a>'
        soup = BeautifulSoup(html, "html.parser")
        ext = ConcreteExtractor(config)
        result = ext.transform_links(soup, tmp_path / "file.html")

        link = result.find("a")
        assert link["href"] == "https://example.com"
        assert "\u2197" in link.get_text()  # ↗

    def test_internal_link_becomes_anchor(self, config, tmp_path):
        html = '<a href="other-page.html">Link</a>'
        soup = BeautifulSoup(html, "html.parser")
        ext = ConcreteExtractor(config)
        result = ext.transform_links(soup, tmp_path / "file.html")

        link = result.find("a")
        assert link["href"] == "#other-page"

    def test_anchor_link_unchanged(self, config, tmp_path):
        html = '<a href="#section">Link</a>'
        soup = BeautifulSoup(html, "html.parser")
        ext = ConcreteExtractor(config)
        result = ext.transform_links(soup, tmp_path / "file.html")

        link = result.find("a")
        assert link["href"] == "#section"

    def test_mailto_unchanged(self, config, tmp_path):
        html = '<a href="mailto:test@example.com">Email</a>'
        soup = BeautifulSoup(html, "html.parser")
        ext = ConcreteExtractor(config)
        result = ext.transform_links(soup, tmp_path / "file.html")

        link = result.find("a")
        assert link["href"] == "mailto:test@example.com"


class TestCleanHtml:
    def test_removes_empty_paragraphs(self, config):
        html = "<p>Keep this</p><p></p><p>   </p><p>And this</p>"
        ext = ConcreteExtractor(config)
        result = ext.clean_html(html)

        soup = BeautifulSoup(result, "html.parser")
        paragraphs = soup.find_all("p")
        texts = [p.get_text(strip=True) for p in paragraphs]
        assert texts == ["Keep this", "And this"]

    def test_preserves_pre_code_whitespace(self, config):
        html = "<pre><code>  indented  code  </code></pre>"
        ext = ConcreteExtractor(config)
        result = ext.clean_html(html)

        assert "  indented  code  " in result

    def test_normalizes_text_whitespace(self, config):
        html = "<p>multiple   spaces   here</p>"
        ext = ConcreteExtractor(config)
        result = ext.clean_html(html)

        soup = BeautifulSoup(result, "html.parser")
        assert soup.find("p").get_text() == "multiple spaces here"
