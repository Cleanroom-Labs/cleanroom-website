"""
Sphinx documentation extractor for HTML files.
"""

from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import Config, config as default_config
from extractors.base import BaseExtractor, ContentSection


class SphinxExtractor(BaseExtractor):
    """Extract Sphinx documentation from HTML files."""

    # Files to skip (navigation, search, etc.)
    SKIP_FILES = {
        "search.html",
        "genindex.html",
        "permalink.html",
    }

    def __init__(self, config: Optional[Config] = None):
        super().__init__(config)

    def extract(self) -> list[ContentSection]:
        """Extract all Sphinx documentation in order."""
        sections = []

        if not self.config.paths.docs_dir.exists():
            if self.config.verbose:
                print(f"Docs directory not found: {self.config.paths.docs_dir}")
            return sections

        # Process in defined order
        for project in self.config.doc_order.projects:
            project_sections = self._extract_project(project)
            sections.extend(project_sections)

        return sections

    def _extract_project(self, project: str) -> list[ContentSection]:
        """Extract all pages for a project."""
        sections = []

        if project == "meta":
            # Meta docs are in the root docs/meta/ directory
            project_dir = self.config.paths.docs_dir / "meta"
        else:
            # Project-specific docs
            project_dir = self.config.paths.docs_dir / project

        if not project_dir.exists():
            if self.config.verbose:
                print(f"  Project directory not found: {project_dir}")
            return sections

        if self.config.verbose:
            print(f"  Processing project: {project}")

        # Get all HTML files in the project directory
        html_files = self._get_ordered_files(project_dir, project)

        for html_file in html_files:
            section = self._extract_page(html_file, project)
            if section:
                sections.append(section)

        return sections

    def _get_ordered_files(self, project_dir: Path, project: str) -> list[Path]:
        """Get HTML files in a logical order."""
        files = []

        # First, check for index.html
        index_file = project_dir / "index.html"
        if index_file.exists() and index_file.name not in self.SKIP_FILES:
            files.append(index_file)

        # Define subdirectory order for projects
        subdirs_order = ["readme", "requirements", "design", "use-cases", "testing", "api", "roadmap"]

        # Process subdirectories in order
        for subdir in subdirs_order:
            subdir_path = project_dir / subdir
            if subdir_path.exists() and subdir_path.is_dir():
                for html_file in sorted(subdir_path.glob("*.html")):
                    if html_file.name not in self.SKIP_FILES:
                        files.append(html_file)

        # Add remaining files in project_dir (not in subdirs)
        for html_file in sorted(project_dir.glob("*.html")):
            if html_file not in files and html_file.name not in self.SKIP_FILES:
                # Skip if it's just a redirect/index to subproject
                if html_file.name not in ["index.html"]:
                    files.append(html_file)

        # For meta directory, use explicit file list only (no fallback)
        if project == "meta":
            direct_files = [
                "principles.html",
                "meta-architecture.html",
                "release-roadmap.html",
                "specification-overview.html",
                "developer-guidelines.html",
                "scope-and-limitations.html",
                "competitive-landscape.html",
                "licensing.html",
                "rust-integration-guide.html",
                "sphinx-needs-guide.html",
            ]
            ordered_files = []
            for filename in direct_files:
                filepath = project_dir / filename
                if filepath.exists():
                    ordered_files.append(filepath)
            # No fallback - only include explicitly listed files
            files = ordered_files

        return files

    def _extract_page(self, html_file: Path, project: str) -> Optional[ContentSection]:
        """Extract content from a single HTML page."""
        try:
            with open(html_file, "r", encoding="utf-8") as f:
                html = f.read()
        except Exception as e:
            if self.config.verbose:
                print(f"    Error reading {html_file}: {e}")
            return None

        soup = BeautifulSoup(html, "html.parser")

        # Strip navigation elements
        soup = self.strip_elements(soup)

        # Extract main content
        content = self.extract_main_content(soup)
        if not content:
            if self.config.verbose:
                print(f"    No main content found in {html_file}")
            return None

        # Get title from first h1 or page title
        title = self._extract_title(soup, content)

        # Transform links and image paths
        content_soup = BeautifulSoup(str(content), "html.parser")
        content_soup = self.transform_links(content_soup, html_file)

        # Clean HTML to remove empty paragraphs and excessive whitespace
        cleaned_html = self.clean_html(str(content_soup))

        # Generate unique ID based on file path
        relative_path = html_file.relative_to(self.config.paths.docs_dir)
        section_id = str(relative_path).replace("/", "-").replace(".html", "")

        # Determine heading level based on structure
        level = 2 if project == "meta" else 2

        if self.config.verbose:
            print(f"    Extracted: {title}")

        return ContentSection(
            id=section_id,
            title=title,
            html_content=cleaned_html,
            level=level,
            source_path=html_file,
            anchor=section_id,
        )

    def _extract_title(self, soup: BeautifulSoup, content) -> str:
        """Extract page title from content or page metadata."""
        # Try to find h1 in content
        h1 = content.find("h1")
        if h1:
            # Get text without the headerlink anchor
            for headerlink in h1.find_all("a", class_="headerlink"):
                headerlink.decompose()
            return h1.get_text(strip=True)

        # Fall back to page title
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.get_text(strip=True)
            # Remove common suffixes
            for suffix in [" — Technical Documentation", " - Technical Documentation"]:
                if title.endswith(suffix):
                    title = title[:-len(suffix)]
            return title

        return "Untitled"
