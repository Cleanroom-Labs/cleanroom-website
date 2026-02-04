"""Tests for SphinxExtractor."""

import shutil

from extractors.sphinx import SphinxExtractor


def test_extract_returns_empty_when_no_docs_dir(config):
    """Extract returns empty list when docs directory doesn't exist."""
    ext = SphinxExtractor(config)
    assert ext.extract() == []


def test_skip_files_excluded(config, tmp_path, fixtures_dir):
    """search.html, genindex.html, permalink.html are skipped."""
    project_dir = tmp_path / "docs" / "testproject"
    project_dir.mkdir(parents=True)

    # Copy a valid file
    shutil.copy(fixtures_dir / "sample-sphinx.html", project_dir / "valid.html")

    # Create skip files
    for skip_name in ["search.html", "genindex.html", "permalink.html"]:
        shutil.copy(fixtures_dir / "sample-sphinx.html", project_dir / skip_name)

    ext = SphinxExtractor(config)
    files = ext._get_ordered_files(project_dir, "testproject")

    filenames = [f.name for f in files]
    assert "valid.html" in filenames
    assert "search.html" not in filenames
    assert "genindex.html" not in filenames
    assert "permalink.html" not in filenames


def test_extract_page_parses_title_from_h1(config, sphinx_html_file):
    """Title is extracted from h1, stripping headerlink anchors."""
    config.paths.docs_dir = sphinx_html_file.parent.parent
    ext = SphinxExtractor(config)
    section = ext._extract_page(sphinx_html_file, "testproject")

    assert section is not None
    assert section.title == "Test Page Title"
    # Should not contain the headerlink paragraph symbol
    assert "\u00b6" not in section.title


def test_extract_page_falls_back_to_page_title(config, tmp_path):
    """When no h1 in content, title comes from <title> tag."""
    docs_dir = tmp_path / "docs" / "proj"
    docs_dir.mkdir(parents=True)
    html_file = docs_dir / "notitle.html"
    html_file.write_text(
        '<!DOCTYPE html><html><head>'
        '<title>Fallback Title &mdash; Technical Documentation</title>'
        '</head><body>'
        '<div role="main"><p>Content without h1</p></div>'
        '</body></html>'
    )

    config.paths.docs_dir = tmp_path / "docs"
    ext = SphinxExtractor(config)
    section = ext._extract_page(html_file, "proj")

    assert section is not None
    assert section.title == "Fallback Title"


def test_extract_page_returns_none_when_no_content(config, tmp_path, fixtures_dir):
    """Pages without main content return None."""
    docs_dir = tmp_path / "docs" / "proj"
    docs_dir.mkdir(parents=True)
    dest = docs_dir / "empty.html"
    shutil.copy(fixtures_dir / "sample-sphinx-no-content.html", dest)

    config.paths.docs_dir = tmp_path / "docs"
    ext = SphinxExtractor(config)
    section = ext._extract_page(dest, "proj")

    assert section is None


def test_get_ordered_files_index_first(config, tmp_path, fixtures_dir):
    """index.html comes first in the file list."""
    project_dir = tmp_path / "docs" / "proj"
    project_dir.mkdir(parents=True)

    for name in ["zebra.html", "index.html", "alpha.html"]:
        shutil.copy(fixtures_dir / "sample-sphinx.html", project_dir / name)

    ext = SphinxExtractor(config)
    files = ext._get_ordered_files(project_dir, "proj")

    assert files[0].name == "index.html"


def test_get_ordered_files_subdirs_in_order(config, tmp_path, fixtures_dir):
    """Subdirectories are processed in the defined order."""
    project_dir = tmp_path / "docs" / "proj"
    project_dir.mkdir(parents=True)

    # Create subdirs in reverse order
    for subdir in ["design", "requirements", "readme"]:
        subdir_path = project_dir / subdir
        subdir_path.mkdir()
        shutil.copy(fixtures_dir / "sample-sphinx.html", subdir_path / "index.html")

    ext = SphinxExtractor(config)
    files = ext._get_ordered_files(project_dir, "proj")

    # Extract subdirectory names from file paths
    subdirs = [f.parent.name for f in files if f.parent != project_dir]
    assert subdirs == ["readme", "requirements", "design"]


def test_meta_project_uses_explicit_file_list(config, tmp_path, fixtures_dir):
    """Meta project only returns files from the hardcoded list."""
    meta_dir = tmp_path / "docs" / "meta"
    meta_dir.mkdir(parents=True)

    # Create a file that IS in the list
    shutil.copy(fixtures_dir / "sample-sphinx.html", meta_dir / "principles.html")
    # Create a file that is NOT in the list
    shutil.copy(fixtures_dir / "sample-sphinx.html", meta_dir / "random-extra.html")

    config.paths.docs_dir = tmp_path / "docs"
    ext = SphinxExtractor(config)
    files = ext._get_ordered_files(meta_dir, "meta")

    filenames = [f.name for f in files]
    assert "principles.html" in filenames
    assert "random-extra.html" not in filenames


def test_section_id_generation(config, sphinx_html_file):
    """Section ID is generated from relative file path."""
    config.paths.docs_dir = sphinx_html_file.parent.parent
    ext = SphinxExtractor(config)
    section = ext._extract_page(sphinx_html_file, "testproject")

    assert section is not None
    assert section.id == "testproject-sample"
