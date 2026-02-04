"""Shared fixtures for PDF generation tests."""

import shutil
import sys
from pathlib import Path

import pytest

# Ensure the generate-pdf module is importable
MODULE_DIR = Path(__file__).resolve().parent.parent
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

from config import Config, Paths, Colors, Fonts, PageLayout, Selectors, DocOrder, ScreenshotConfig

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def pytest_configure(config):
    config.addinivalue_line("markers", "integration: requires real repo content (built docs)")


@pytest.fixture
def fixtures_dir():
    """Path to the test fixtures directory."""
    return FIXTURES_DIR


@pytest.fixture
def config(tmp_path):
    """Config with paths pointed at tmp_path for isolation."""
    cfg = object.__new__(Config)
    cfg.colors = Colors()
    cfg.fonts = Fonts()
    cfg.page_layout = PageLayout()
    cfg.selectors = Selectors()
    cfg.doc_order = DocOrder()
    cfg.screenshot = ScreenshotConfig()
    cfg.verbose = False
    cfg.repo_root = tmp_path
    cfg.paths = Paths()
    cfg.paths.docs_dir = tmp_path / "docs"
    cfg.paths.blog_dir = tmp_path / "blog"
    cfg.paths.output_dir = tmp_path / "output"
    cfg.paths.screenshots_dir = tmp_path / "output" / "screenshots"
    return cfg


@pytest.fixture
def real_config():
    """Real Config() that resolves against the actual repo."""
    return Config()


@pytest.fixture
def sphinx_html_file(tmp_path, fixtures_dir):
    """Copy sample Sphinx HTML to a tmp docs directory and return its path."""
    docs_dir = tmp_path / "docs" / "testproject"
    docs_dir.mkdir(parents=True)
    dest = docs_dir / "sample.html"
    shutil.copy(fixtures_dir / "sample-sphinx.html", dest)
    return dest


@pytest.fixture
def blog_dir_with_post(tmp_path, fixtures_dir):
    """Copy sample blog post to a tmp blog directory and return the directory."""
    blog_dir = tmp_path / "blog"
    blog_dir.mkdir(parents=True)
    shutil.copy(fixtures_dir / "sample-post.mdx", blog_dir / "2026-01-15-test-post.mdx")
    return blog_dir
