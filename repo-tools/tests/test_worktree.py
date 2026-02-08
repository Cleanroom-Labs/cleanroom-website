"""Tests for repo_tools.worktree."""

import argparse
import subprocess
from pathlib import Path
from unittest.mock import patch

from repo_tools.repo_utils import parse_gitmodules
from repo_tools.worktree import (
    _init_submodules,
    add_worktree,
    remove_worktree,
)


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(cwd)] + list(args),
        capture_output=True, text=True, check=True,
    )


# ---------------------------------------------------------------------------
# parse_gitmodules (shared from repo_utils, used by worktree)
# ---------------------------------------------------------------------------

class TestParseGitmodulesAll:
    def test_missing_file(self, tmp_path: Path):
        """Nonexistent .gitmodules should return empty list."""
        result = parse_gitmodules(tmp_path / ".gitmodules")
        assert result == []

    def test_empty_file(self, tmp_path: Path):
        """Empty .gitmodules should return empty list."""
        (tmp_path / ".gitmodules").write_text("")
        result = parse_gitmodules(tmp_path / ".gitmodules")
        assert result == []

    def test_single_submodule(self, tmp_path: Path):
        (tmp_path / ".gitmodules").write_text(
            '[submodule "technical-docs"]\n'
            "    path = technical-docs\n"
            "    url = /path/to/technical-docs\n"
        )
        result = parse_gitmodules(tmp_path / ".gitmodules")
        assert len(result) == 1
        name, path, url = result[0]
        assert name == "technical-docs"
        assert path == "technical-docs"
        assert url == "/path/to/technical-docs"

    def test_multiple_submodules(self, tmp_path: Path):
        """Should return ALL submodules when no url_match is given."""
        (tmp_path / ".gitmodules").write_text(
            '[submodule "technical-docs"]\n'
            "    path = technical-docs\n"
            "    url = /path/to/technical-docs\n"
            '[submodule "common"]\n'
            "    path = source/common\n"
            "    url = /path/to/common\n"
        )
        result = parse_gitmodules(tmp_path / ".gitmodules")
        assert len(result) == 2
        names = [r[0] for r in result]
        assert "technical-docs" in names
        assert "common" in names


# ---------------------------------------------------------------------------
# _init_submodules
# ---------------------------------------------------------------------------

class TestInitSubmodules:
    def test_no_gitmodules_returns_true(self, tmp_path: Path):
        """Directory without .gitmodules should succeed immediately."""
        worktree = tmp_path / "wt"
        worktree.mkdir()
        assert _init_submodules(worktree, tmp_path) is True


# ---------------------------------------------------------------------------
# add_worktree (integration)
# ---------------------------------------------------------------------------

class TestAddWorktree:
    def test_creates_worktree_directory(self, tmp_submodule_tree: Path):
        """Worktree directory should exist after add."""
        wt_path = tmp_submodule_tree.parent / "test-wt"
        args = argparse.Namespace(branch="test-branch", path=str(wt_path), checkout=False)

        with patch("repo_tools.worktree.find_repo_root", return_value=tmp_submodule_tree):
            result = add_worktree(args)

        assert result == 0
        assert wt_path.exists()
        assert (wt_path / ".git").exists()

    def test_initializes_nested_submodules(self, tmp_submodule_tree: Path):
        """Nested submodules should be checked out in the new worktree."""
        wt_path = tmp_submodule_tree.parent / "test-wt"
        args = argparse.Namespace(branch="test-branch", path=str(wt_path), checkout=False)

        with patch("repo_tools.worktree.find_repo_root", return_value=tmp_submodule_tree):
            result = add_worktree(args)

        assert result == 0
        # Level 2: technical-docs submodule
        assert (wt_path / "technical-docs" / ".git").exists()
        # Level 3: common submodule inside technical-docs
        assert (wt_path / "technical-docs" / "common" / ".git").exists()
        # Verify actual content from the grandchild repo
        assert (wt_path / "technical-docs" / "common" / "theme.txt").exists()

    def test_checkout_existing_branch(self, tmp_submodule_tree: Path):
        """--checkout should use an existing branch without creating a new one."""
        _git(tmp_submodule_tree, "branch", "existing-branch")

        wt_path = tmp_submodule_tree.parent / "test-wt"
        args = argparse.Namespace(branch="existing-branch", path=str(wt_path), checkout=True)

        with patch("repo_tools.worktree.find_repo_root", return_value=tmp_submodule_tree):
            result = add_worktree(args)

        assert result == 0
        assert wt_path.exists()

    def test_path_already_exists_returns_1(self, tmp_submodule_tree: Path):
        """Should fail if the target path already exists."""
        wt_path = tmp_submodule_tree.parent / "test-wt"
        wt_path.mkdir()  # pre-create

        args = argparse.Namespace(branch="test-branch", path=str(wt_path), checkout=False)

        with patch("repo_tools.worktree.find_repo_root", return_value=tmp_submodule_tree):
            result = add_worktree(args)

        assert result == 1


# ---------------------------------------------------------------------------
# remove_worktree (integration)
# ---------------------------------------------------------------------------

class TestRemoveWorktree:
    def test_removes_worktree(self, tmp_submodule_tree: Path):
        """Worktree directory should be gone after remove."""
        wt_path = tmp_submodule_tree.parent / "test-wt"
        _git(tmp_submodule_tree, "worktree", "add", "-b", "rm-branch", str(wt_path))
        assert wt_path.exists()

        args = argparse.Namespace(path=str(wt_path), force=False)

        with patch("repo_tools.worktree.find_repo_root", return_value=tmp_submodule_tree):
            result = remove_worktree(args)

        assert result == 0
        assert not wt_path.exists()

    def test_force_removes_dirty_worktree(self, tmp_submodule_tree: Path):
        """--force should remove a worktree with uncommitted changes."""
        wt_path = tmp_submodule_tree.parent / "test-wt"
        _git(tmp_submodule_tree, "worktree", "add", "-b", "dirty-branch", str(wt_path))
        (wt_path / "dirty.txt").write_text("uncommitted\n")

        args = argparse.Namespace(path=str(wt_path), force=True)

        with patch("repo_tools.worktree.find_repo_root", return_value=tmp_submodule_tree):
            result = remove_worktree(args)

        assert result == 0
        assert not wt_path.exists()
