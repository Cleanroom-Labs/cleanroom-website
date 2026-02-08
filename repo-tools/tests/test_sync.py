"""Tests for repo_tools.sync."""

import pytest
from pathlib import Path

from repo_tools.repo_utils import DEFAULT_THEME_REPO
from repo_tools.sync import parse_gitmodules, resolve_target_commit


class TestDefaultThemeRepoPath:
    def test_is_path_object(self):
        assert isinstance(DEFAULT_THEME_REPO, Path)

    def test_points_to_expected_location(self):
        expected = Path.home() / "Projects" / "cleanroom-website-common"
        assert DEFAULT_THEME_REPO == expected


class TestParseGitmodules:
    def test_extracts_common_submodule(self, tmp_path: Path):
        """parse_gitmodules should return entries whose URL contains
        'cleanroom-website-common'."""
        gitmodules = tmp_path / ".gitmodules"
        gitmodules.write_text(
            '[submodule "common"]\n'
            "    path = common\n"
            "    url = git@github.com:Cleanroom-Labs/cleanroom-website-common.git\n"
        )
        results = parse_gitmodules(gitmodules)
        assert len(results) == 1
        path, url = results[0]
        assert path == "common"
        assert "cleanroom-website-common" in url

    def test_ignores_non_common_submodule(self, tmp_path: Path):
        """Submodules whose URL does not contain 'cleanroom-website-common'
        should be excluded."""
        gitmodules = tmp_path / ".gitmodules"
        gitmodules.write_text(
            '[submodule "other"]\n'
            "    path = other\n"
            "    url = git@github.com:Cleanroom-Labs/other-repo.git\n"
        )
        results = parse_gitmodules(gitmodules)
        assert len(results) == 0

    def test_multiple_submodules_mixed(self, tmp_path: Path):
        """Only submodules matching cleanroom-website-common should appear."""
        gitmodules = tmp_path / ".gitmodules"
        gitmodules.write_text(
            '[submodule "common"]\n'
            "    path = source/common\n"
            "    url = git@github.com:Cleanroom-Labs/cleanroom-website-common.git\n"
            '[submodule "other"]\n'
            "    path = other\n"
            "    url = git@github.com:Cleanroom-Labs/other-repo.git\n"
            '[submodule "theme2"]\n'
            "    path = theme2\n"
            "    url = https://github.com/Cleanroom-Labs/cleanroom-website-common.git\n"
        )
        results = parse_gitmodules(gitmodules)
        assert len(results) == 2
        paths = [r[0] for r in results]
        assert "source/common" in paths
        assert "theme2" in paths

    def test_missing_file(self, tmp_path: Path):
        """A nonexistent .gitmodules file should return an empty list."""
        gitmodules = tmp_path / ".gitmodules"
        results = parse_gitmodules(gitmodules)
        assert results == []

    def test_empty_file(self, tmp_path: Path):
        """An empty .gitmodules file should return an empty list."""
        gitmodules = tmp_path / ".gitmodules"
        gitmodules.write_text("")
        results = parse_gitmodules(gitmodules)
        assert results == []


# ---------------------------------------------------------------------------
# resolve_target_commit
# ---------------------------------------------------------------------------

class TestResolveTargetCommit:
    def test_explicit_sha_returned_as_is(self):
        """An explicit commit SHA should be returned without modification."""
        sha = "abc1234"
        result_sha, source = resolve_target_commit(sha, Path("/nonexistent"))
        assert result_sha == sha
        assert source == "CLI argument"

    def test_full_sha_returned(self):
        """A full 40-char SHA should be accepted."""
        sha = "a" * 40
        result_sha, _ = resolve_target_commit(sha, Path("/nonexistent"))
        assert result_sha == sha

    def test_invalid_sha_raises(self):
        """A non-hex string should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid commit SHA"):
            resolve_target_commit("not-a-sha!", Path("/nonexistent"))

    def test_too_short_sha_raises(self):
        """A SHA shorter than 7 chars should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid commit SHA"):
            resolve_target_commit("abc12", Path("/nonexistent"))

    def test_missing_theme_repo_raises(self, tmp_path: Path):
        """When no commit is given and theme repo doesn't exist, should raise."""
        with pytest.raises(ValueError, match="not found"):
            resolve_target_commit(None, tmp_path / "nonexistent")
