"""
Blog post extractor for MDX files.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional

import frontmatter
import markdown

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import Config, config as default_config
from extractors.base import BaseExtractor, ContentSection


class BlogExtractor(BaseExtractor):
    """Extract blog posts from MDX files."""

    def __init__(self, config: Optional[Config] = None):
        super().__init__(config)
        self.md = markdown.Markdown(
            extensions=[
                "fenced_code",
                "tables",
                "toc",
                "codehilite",
                "nl2br",
            ],
            extension_configs={
                "codehilite": {
                    "css_class": "highlight",
                    "guess_lang": False,
                }
            },
        )

    def extract(self) -> list[ContentSection]:
        """Extract all blog posts, sorted by date (newest first)."""
        posts = []

        if not self.config.paths.blog_dir.exists():
            if self.config.verbose:
                print(f"Blog directory not found: {self.config.paths.blog_dir}")
            return posts

        for mdx_file in sorted(self.config.paths.blog_dir.glob("*.mdx")):
            section = self._extract_post(mdx_file)
            if section:
                posts.append(section)

        # Sort by date (newest first) - date is stored in metadata
        posts.sort(key=lambda p: p.source_path.stem if p.source_path else "", reverse=True)

        # Re-sort by actual date from frontmatter
        posts_with_dates = []
        for post in posts:
            date_str = self._get_post_date(post)
            posts_with_dates.append((date_str, post))

        posts_with_dates.sort(key=lambda x: x[0], reverse=True)
        return [post for _, post in posts_with_dates]

    def _get_post_date(self, post: ContentSection) -> str:
        """Extract date from post for sorting."""
        # Parse the original file to get date
        if post.source_path and post.source_path.exists():
            try:
                with open(post.source_path, "r", encoding="utf-8") as f:
                    fm = frontmatter.load(f)
                    return fm.get("date", "1970-01-01")
            except Exception:
                pass
        return "1970-01-01"

    def _extract_post(self, mdx_file: Path) -> Optional[ContentSection]:
        """Extract a single blog post from an MDX file."""
        try:
            with open(mdx_file, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)
        except Exception as e:
            if self.config.verbose:
                print(f"Error parsing {mdx_file}: {e}")
            return None

        title = post.get("title", mdx_file.stem)
        date = post.get("date", "")
        author = post.get("author", "")
        tags = post.get("tags", [])
        slug = post.get("slug", mdx_file.stem)
        excerpt = post.get("excerpt", "")

        # Reset markdown instance for clean conversion
        self.md.reset()

        # Convert markdown content to HTML
        html_content = self.md.convert(post.content)

        # Build the full HTML with metadata header
        metadata_html = self._build_metadata_html(title, date, author, tags, excerpt)
        full_html = f"{metadata_html}\n{html_content}"

        if self.config.verbose:
            print(f"  Extracted blog post: {title}")

        return ContentSection(
            id=f"blog-{slug}",
            title=title,
            html_content=full_html,
            level=1,
            source_path=mdx_file,
            anchor=f"blog-{slug}",
        )

    def _build_metadata_html(
        self,
        title: str,
        date: str,
        author: str,
        tags: list[str],
        excerpt: str,
    ) -> str:
        """Build HTML for post metadata header with compact spacing."""
        parts = [f'<h1 class="blog-title">{title}</h1>']

        # Consolidated meta line: date, author, and tags together
        meta_parts = []
        if date:
            # Format date nicely
            try:
                dt = datetime.strptime(date, "%Y-%m-%d")
                formatted_date = dt.strftime("%B %d, %Y")
            except ValueError:
                formatted_date = date
            meta_parts.append(f'<span class="blog-date">{formatted_date}</span>')

        if author:
            meta_parts.append(f'<span class="blog-author">by {author}</span>')

        # Add tags inline with date/author
        if tags:
            tag_html = " ".join(f'<span class="blog-tag">{tag}</span>' for tag in tags)
            meta_parts.append(f'<span class="blog-tags">{tag_html}</span>')

        if meta_parts:
            parts.append(f'<p class="blog-meta">{" · ".join(meta_parts)}</p>')

        # Excerpt/summary (if present)
        if excerpt:
            parts.append(f'<p class="blog-excerpt">{excerpt}</p>')

        return "\n".join(parts)
