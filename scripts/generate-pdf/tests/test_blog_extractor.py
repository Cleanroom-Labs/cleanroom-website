"""Tests for BlogExtractor."""

import shutil

from extractors.blog import BlogExtractor


def test_extract_returns_empty_when_no_blog_dir(config):
    """Extract returns empty list when blog directory doesn't exist."""
    ext = BlogExtractor(config)
    assert ext.extract() == []


def test_extract_single_post(config, blog_dir_with_post):
    """Extract a single post from fixtures."""
    config.paths.blog_dir = blog_dir_with_post
    ext = BlogExtractor(config)
    sections = ext.extract()

    assert len(sections) == 1
    assert sections[0].title == "Test Post Title"
    assert sections[0].id == "blog-test-post"
    assert sections[0].anchor == "blog-test-post"


def test_extract_post_converts_markdown(config, blog_dir_with_post):
    """Markdown content is converted to HTML."""
    config.paths.blog_dir = blog_dir_with_post
    ext = BlogExtractor(config)
    sections = ext.extract()

    html = sections[0].html_content
    assert "<strong>" in html or "<b>" in html  # **bold**
    assert "<code>" in html  # `code`


def test_extract_post_html_has_metadata(config, blog_dir_with_post):
    """Extracted HTML includes metadata classes."""
    config.paths.blog_dir = blog_dir_with_post
    ext = BlogExtractor(config)
    sections = ext.extract()

    html = sections[0].html_content
    assert 'class="blog-title"' in html
    assert 'class="blog-date"' in html
    assert 'class="blog-author"' in html
    assert 'class="blog-tag"' in html


def test_extract_sorts_by_date_newest_first(config, tmp_path, fixtures_dir):
    """Multiple posts are sorted newest first."""
    blog_dir = tmp_path / "blog"
    blog_dir.mkdir()

    # Create two posts with different dates
    shutil.copy(fixtures_dir / "sample-post.mdx", blog_dir / "post1.mdx")

    # Write a second post with an older date
    (blog_dir / "post2.mdx").write_text(
        '---\ntitle: "Older Post"\ndate: "2025-06-01"\nslug: "older"\n---\nOld content.\n'
    )

    config.paths.blog_dir = blog_dir
    ext = BlogExtractor(config)
    sections = ext.extract()

    assert len(sections) == 2
    assert sections[0].title == "Test Post Title"  # 2026-01-15 (newer)
    assert sections[1].title == "Older Post"  # 2025-06-01 (older)


def test_build_metadata_html_formats_date(config):
    """Date string is formatted to human-readable form."""
    ext = BlogExtractor(config)
    html = ext._build_metadata_html("Title", "2026-01-15", "", [], "")
    assert "January 15, 2026" in html


def test_build_metadata_html_with_tags(config):
    """Tags are rendered as blog-tag spans."""
    ext = BlogExtractor(config)
    html = ext._build_metadata_html("Title", "", "", ["testing", "ci"], "")
    assert '<span class="blog-tag">testing</span>' in html
    assert '<span class="blog-tag">ci</span>' in html
