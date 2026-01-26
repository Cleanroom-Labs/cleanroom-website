"""
Base extractor class with common functionality.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import Config, config as default_config


@dataclass
class ContentSection:
    """Represents a section of extracted content."""
    id: str
    title: str
    html_content: str
    level: int = 1  # Heading level (1 = h1, 2 = h2, etc.)
    source_path: Optional[Path] = None
    anchor: Optional[str] = None
    children: list["ContentSection"] = field(default_factory=list)

    @property
    def anchor_id(self) -> str:
        """Generate a valid HTML anchor ID."""
        if self.anchor:
            return self.anchor
        # Convert title to anchor-friendly format
        return self.id.replace("/", "-").replace(".", "-").lower()


class BaseExtractor(ABC):
    """Base class for content extractors."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or default_config

    @abstractmethod
    def extract(self) -> list[ContentSection]:
        """Extract content and return list of sections."""
        pass

    def strip_elements(self, soup: BeautifulSoup) -> BeautifulSoup:
        """Remove navigation and non-content elements from HTML."""
        for selector in self.config.selectors.strip:
            for element in soup.select(selector):
                element.decompose()
        return soup

    def extract_main_content(self, soup: BeautifulSoup) -> Optional[Tag]:
        """Extract main content area from HTML."""
        # Try primary content selector
        content = soup.select_one(self.config.selectors.content)
        if content:
            return content

        # Try fallback selector
        content = soup.select_one(self.config.selectors.fallback_content)
        if content:
            return content

        return None

    def transform_links(self, soup: BeautifulSoup, base_path: Path) -> BeautifulSoup:
        """Transform internal links to PDF anchors and fix image paths."""
        # Transform internal links to anchors
        for link in soup.find_all("a", href=True):
            href = link["href"]

            # Skip external links and anchors
            if href.startswith(("http://", "https://", "mailto:", "#")):
                # Mark external links with arrow
                if href.startswith(("http://", "https://")):
                    if not link.string or "↗" not in link.get_text():
                        link.append(" ↗")
                continue

            # Transform internal links to PDF anchors
            # Remove .html extension and convert path to anchor
            clean_href = href.replace(".html", "").replace("/", "-").replace("..", "")
            if clean_href.startswith("-"):
                clean_href = clean_href[1:]
            link["href"] = f"#{clean_href}"

        # Fix image paths to absolute file:// URLs
        for img in soup.find_all("img", src=True):
            src = img["src"]

            # Skip data URIs and absolute URLs
            if src.startswith(("data:", "http://", "https://")):
                continue

            # Resolve relative path
            if src.startswith("/"):
                # Absolute path from docs root
                abs_path = self.config.paths.docs_dir / src.lstrip("/")
            else:
                # Relative path from current file
                abs_path = (base_path.parent / src).resolve()

            # Convert to file:// URL
            if abs_path.exists():
                img["src"] = f"file://{abs_path}"
            elif self.config.verbose:
                print(f"  Warning: Image not found: {abs_path}")

        return soup

    def clean_html(self, html: str) -> str:
        """Clean and normalize HTML content."""
        soup = BeautifulSoup(html, "html.parser")

        # Remove empty paragraphs
        for p in soup.find_all("p"):
            if not p.get_text(strip=True):
                p.decompose()

        # Remove excessive whitespace in text nodes
        for text in soup.find_all(string=True):
            if text.parent.name not in ["pre", "code"]:
                cleaned = " ".join(text.split())
                if cleaned != text:
                    text.replace_with(cleaned)

        return str(soup)
