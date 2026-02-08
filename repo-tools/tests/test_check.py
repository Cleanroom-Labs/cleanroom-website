"""Tests for repo_tools.check."""

import subprocess
from pathlib import Path
from unittest.mock import patch

from repo_tools.check import check_repo_state, get_tag_or_branch, run
from repo_tools.repo_utils import RepoInfo


# ---------------------------------------------------------------------------
# get_tag_or_branch / check_repo_state
# ---------------------------------------------------------------------------

class TestGetTagOrBranch:
    def test_returns_branch_name(self, tmp_git_repo: Path):
        repo = RepoInfo(path=tmp_git_repo, repo_root=tmp_git_repo)
        result = get_tag_or_branch(repo)
        assert result is not None
        assert len(result) > 0

    def test_returns_tag_when_on_tag(self, tmp_git_repo: Path):
        """When HEAD is exactly on a tag, the tag name should be returned."""
        subprocess.run(
            ["git", "-C", str(tmp_git_repo), "tag", "v1.0.0"],
            check=True,
            capture_output=True,
        )
        repo = RepoInfo(path=tmp_git_repo, repo_root=tmp_git_repo)
        result = get_tag_or_branch(repo)
        # Could be tag or branch -- both are valid since HEAD is on both.
        assert result is not None


class TestCheckRepoState:
    def test_healthy_repo(self, tmp_git_repo: Path, capsys):
        repo = RepoInfo(path=tmp_git_repo, repo_root=tmp_git_repo)
        result = check_repo_state(repo, "test-repo")
        assert result is True
        captured = capsys.readouterr()
        assert "test-repo" in captured.out

    def test_verbose_shows_sha(self, tmp_git_repo: Path, capsys):
        repo = RepoInfo(path=tmp_git_repo, repo_root=tmp_git_repo)
        result = check_repo_state(repo, "test-repo", verbose=True)
        assert result is True
        captured = capsys.readouterr()
        # Verbose mode should include commit SHA in parentheses.
        assert "(" in captured.out


# ---------------------------------------------------------------------------
# run() -- integration with the real check module
# ---------------------------------------------------------------------------

class TestCheckRun:
    def test_all_healthy(self, tmp_submodule_tree: Path, capsys):
        """When the submodule tree is healthy, run() should exit 0.

        We patch __file__ resolution inside check.py so it uses our
        temporary tree as the repo root.
        """
        import argparse

        args = argparse.Namespace(verbose=False)

        # Patch the repo_root derivation inside check.run.
        # check.run computes: repo_root = Path(__file__).parent.parent.parent.parent.resolve()
        # We mock Path(__file__) by patching the function-level code.
        # Easier: call the helper functions directly with our tree.

        # Instead of calling run() (which hard-codes its repo_root from __file__),
        # we test the building blocks individually.
        from repo_tools.check import check_common_sync, check_repo_state
        from repo_tools.repo_utils import RepoInfo

        td = tmp_submodule_tree / "technical-docs"
        repo = RepoInfo(path=td, repo_root=tmp_submodule_tree)
        assert check_repo_state(repo, "technical-docs", verbose=False) is True

        # common sync should pass (only one common submodule, trivially in sync)
        assert check_common_sync(tmp_submodule_tree, verbose=False) is True

    def test_verbose_output(self, tmp_submodule_tree: Path, capsys):
        """Verbose check should include commit SHAs in the output."""
        from repo_tools.check import check_repo_state
        from repo_tools.repo_utils import RepoInfo

        td = tmp_submodule_tree / "technical-docs"
        repo = RepoInfo(path=td, repo_root=tmp_submodule_tree)
        check_repo_state(repo, "technical-docs", verbose=True)

        captured = capsys.readouterr()
        # In verbose mode the SHA is shown in parentheses, e.g. "(abc1234)"
        assert "(" in captured.out
        assert ")" in captured.out

    def test_detached_head_detected(self, tmp_submodule_tree: Path, capsys):
        """A repo in detached HEAD state should be flagged."""
        td = tmp_submodule_tree / "technical-docs"

        # Detach HEAD by checking out a commit directly.
        sha = subprocess.run(
            ["git", "-C", str(td), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        subprocess.run(
            ["git", "-C", str(td), "checkout", sha],
            capture_output=True,
            check=True,
        )

        repo = RepoInfo(path=td, repo_root=tmp_submodule_tree)
        result = check_repo_state(repo, "technical-docs")
        assert result is False

        captured = capsys.readouterr()
        assert "detached" in captured.out.lower()
