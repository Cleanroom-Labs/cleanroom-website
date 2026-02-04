"""Tests for PDF generation configuration."""

import pytest
from config import Config


# --- Unit tests (no filesystem dependency) ---

def test_output_path_construction():
    cfg = Config()
    assert cfg.paths.output_path == cfg.paths.output_dir / cfg.paths.output_filename


def test_selectors_strip_is_nonempty():
    cfg = Config()
    assert len(cfg.selectors.strip) > 0


def test_doc_order_contains_expected_projects():
    cfg = Config()
    assert "meta" in cfg.doc_order.projects
    assert "transfer" in cfg.doc_order.projects
    assert "deploy" in cfg.doc_order.projects
    assert "whisper" in cfg.doc_order.projects


def test_default_output_filename():
    cfg = Config()
    assert cfg.paths.output_filename == "cleanroom-labs.pdf"


def test_default_page_layout():
    cfg = Config()
    assert cfg.page_layout.size == "A4"
    assert cfg.page_layout.margin_top == "20mm"


# --- Integration tests (require real repo content) ---

@pytest.mark.integration
def test_docs_dir_exists(real_config):
    assert real_config.paths.docs_dir.exists(), (
        f"docs_dir does not exist: {real_config.paths.docs_dir}"
    )


@pytest.mark.integration
def test_blog_dir_exists(real_config):
    assert real_config.paths.blog_dir.exists(), (
        f"blog_dir does not exist: {real_config.paths.blog_dir}"
    )


@pytest.mark.integration
def test_doc_order_projects_match_filesystem(real_config):
    """Every project in doc_order should have a directory under docs_dir."""
    for project in real_config.doc_order.projects:
        project_dir = real_config.paths.docs_dir / project
        assert project_dir.exists(), (
            f"Project '{project}' in doc_order but directory not found: {project_dir}"
        )


@pytest.mark.integration
def test_meta_direct_files_all_exist(real_config):
    """Every file in SphinxExtractor's hardcoded meta list should exist."""
    from extractors.sphinx import SphinxExtractor

    extractor = SphinxExtractor(real_config)
    meta_dir = real_config.paths.docs_dir / "meta"

    # Get the hardcoded file list by calling _get_ordered_files with project="meta"
    files = extractor._get_ordered_files(meta_dir, "meta")
    assert len(files) > 0, "No meta files returned by _get_ordered_files"

    for f in files:
        assert f.exists(), f"Meta file listed but not found: {f}"
