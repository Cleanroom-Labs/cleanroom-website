"""Tests for repo_tools.sync (minimal)."""

from pathlib import Path

from repo_tools.sync import DEFAULT_THEME_REPO, parse_gitmodules


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
