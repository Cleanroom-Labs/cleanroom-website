"""Tests for repo_tools.repo_utils."""

from pathlib import Path

from repo_tools.repo_utils import (
    Colors,
    RepoInfo,
    RepoStatus,
    discover_repos,
    topological_sort_repos,
)


# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------

class TestColors:
    def test_red_formatting(self):
        result = Colors.red("hello")
        assert result == "\033[0;31mhello\033[0m"

    def test_green_formatting(self):
        result = Colors.green("world")
        assert result == "\033[0;32mworld\033[0m"

    def test_yellow_formatting(self):
        result = Colors.yellow("warn")
        assert result == "\033[1;33mwarn\033[0m"

    def test_blue_formatting(self):
        result = Colors.blue("info")
        assert result == "\033[0;34minfo\033[0m"

    def test_empty_string(self):
        result = Colors.red("")
        assert result == "\033[0;31m\033[0m"


# ---------------------------------------------------------------------------
# RepoStatus
# ---------------------------------------------------------------------------

class TestRepoStatus:
    def test_expected_members(self):
        expected = {
            "OK",
            "PENDING",
            "UP_TO_DATE",
            "UNCOMMITTED",
            "DETACHED",
            "NO_REMOTE",
            "BEHIND",
            "DIVERGED",
        }
        actual = {member.name for member in RepoStatus}
        assert actual == expected

    def test_values(self):
        assert RepoStatus.OK.value == "ok"
        assert RepoStatus.PENDING.value == "pending"
        assert RepoStatus.UP_TO_DATE.value == "up-to-date"
        assert RepoStatus.UNCOMMITTED.value == "uncommitted"
        assert RepoStatus.DETACHED.value == "detached"
        assert RepoStatus.NO_REMOTE.value == "no-remote"
        assert RepoStatus.BEHIND.value == "behind"
        assert RepoStatus.DIVERGED.value == "diverged"


# ---------------------------------------------------------------------------
# RepoInfo.rel_path
# ---------------------------------------------------------------------------

class TestRepoInfoRelPath:
    def test_non_root_repo(self, tmp_git_repo: Path):
        """A submodule path should be expressed relative to repo_root."""
        repo_root = tmp_git_repo.parent
        info = RepoInfo(path=tmp_git_repo, repo_root=repo_root)
        assert info.rel_path == tmp_git_repo.name

    def test_root_repo(self, tmp_git_repo: Path):
        """When path == repo_root the friendly name should be returned."""
        info = RepoInfo(path=tmp_git_repo, repo_root=tmp_git_repo)
        assert info.rel_path == "(website root)"

    def test_nested_path(self, tmp_submodule_tree: Path):
        """A deeply nested submodule should show the full relative path."""
        nested = tmp_submodule_tree / "technical-docs" / "common"
        info = RepoInfo(path=nested, repo_root=tmp_submodule_tree)
        assert info.rel_path == "technical-docs/common"


# ---------------------------------------------------------------------------
# discover_repos
# ---------------------------------------------------------------------------

class TestDiscoverRepos:
    def test_finds_repos(self, tmp_submodule_tree: Path):
        """discover_repos should find the parent and child (excluding common)."""
        repos = discover_repos(tmp_submodule_tree, exclude_theme=True)
        paths = {r.path for r in repos}

        # Must include the root and the technical-docs submodule.
        assert tmp_submodule_tree in paths
        assert tmp_submodule_tree / "technical-docs" in paths

        # "common" should be excluded by default.
        common_paths = {p for p in paths if p.name == "common"}
        assert len(common_paths) == 0

    def test_exclude_theme_false(self, tmp_submodule_tree: Path):
        """With exclude_theme=False, common submodules should be included."""
        repos = discover_repos(tmp_submodule_tree, exclude_theme=False)
        paths = {r.path for r in repos}

        common_paths = {p for p in paths if p.name == "common"}
        assert len(common_paths) >= 1

    def test_root_always_included(self, tmp_submodule_tree: Path):
        repos = discover_repos(tmp_submodule_tree)
        root_repos = [r for r in repos if r.path == tmp_submodule_tree]
        assert len(root_repos) == 1


# ---------------------------------------------------------------------------
# topological_sort_repos
# ---------------------------------------------------------------------------

class TestTopologicalSort:
    def test_children_before_parents(self, tmp_submodule_tree: Path):
        """After topological sort, children must appear before their parents."""
        repos = discover_repos(tmp_submodule_tree, exclude_theme=False)
        sorted_repos = topological_sort_repos(repos)

        # Build an index mapping path -> position
        index = {r.path: i for i, r in enumerate(sorted_repos)}

        # technical-docs should come before parent
        td_path = tmp_submodule_tree / "technical-docs"
        if td_path in index and tmp_submodule_tree in index:
            assert index[td_path] < index[tmp_submodule_tree]

        # common should come before technical-docs
        common_path = tmp_submodule_tree / "technical-docs" / "common"
        if common_path in index and td_path in index:
            assert index[common_path] < index[td_path]


# ---------------------------------------------------------------------------
# RepoInfo.validate
# ---------------------------------------------------------------------------

class TestValidate:
    def test_clean_repo(self, tmp_git_repo: Path):
        """A freshly initialised repo with no remote should validate when
        allow_no_remote is True."""
        info = RepoInfo(path=tmp_git_repo, repo_root=tmp_git_repo)
        result = info.validate(allow_no_remote=True)
        assert result is True

    def test_uncommitted_changes_detected(self, tmp_git_repo: Path):
        """Modifying a tracked file should cause validation to fail with
        UNCOMMITTED status."""
        # Modify a tracked file (git diff --quiet only sees changes to tracked files).
        readme = tmp_git_repo / "README.md"
        readme.write_text("modified content\n")

        info = RepoInfo(path=tmp_git_repo, repo_root=tmp_git_repo)
        result = info.validate()
        assert result is False
        assert info.status == RepoStatus.UNCOMMITTED

    def test_no_remote_detected(self, tmp_git_repo: Path):
        """A repo without an origin remote should fail validation when
        allow_no_remote is False (default)."""
        info = RepoInfo(path=tmp_git_repo, repo_root=tmp_git_repo)
        result = info.validate(allow_no_remote=False)
        assert result is False
        assert info.status == RepoStatus.NO_REMOTE


# ---------------------------------------------------------------------------
# RepoInfo helper methods
# ---------------------------------------------------------------------------

class TestRepoInfoHelpers:
    def test_get_branch(self, tmp_git_repo: Path):
        info = RepoInfo(path=tmp_git_repo, repo_root=tmp_git_repo)
        branch = info.get_branch()
        # Default branch is usually "main" or "master".
        assert branch is not None
        assert len(branch) > 0

    def test_has_uncommitted_changes_clean(self, tmp_git_repo: Path):
        info = RepoInfo(path=tmp_git_repo, repo_root=tmp_git_repo)
        assert info.has_uncommitted_changes() is False

    def test_has_uncommitted_changes_dirty(self, tmp_git_repo: Path):
        (tmp_git_repo / "new.txt").write_text("new\n")
        info = RepoInfo(path=tmp_git_repo, repo_root=tmp_git_repo)
        # Untracked files don't show up in git diff, but staged or modified tracked files do.
        # Let's modify a tracked file instead.
        (tmp_git_repo / "README.md").write_text("modified\n")
        assert info.has_uncommitted_changes() is True

    def test_get_commit_sha(self, tmp_git_repo: Path):
        info = RepoInfo(path=tmp_git_repo, repo_root=tmp_git_repo)
        sha = info.get_commit_sha(short=True)
        assert sha != "unknown"
        assert len(sha) >= 7

    def test_get_commit_sha_full(self, tmp_git_repo: Path):
        info = RepoInfo(path=tmp_git_repo, repo_root=tmp_git_repo)
        sha = info.get_commit_sha(short=False)
        assert len(sha) == 40

    def test_name_property(self, tmp_git_repo: Path):
        info = RepoInfo(path=tmp_git_repo, repo_root=tmp_git_repo)
        assert info.name == tmp_git_repo.name

    def test_depth_property(self, tmp_submodule_tree: Path):
        root = RepoInfo(path=tmp_submodule_tree, repo_root=tmp_submodule_tree)
        child = RepoInfo(
            path=tmp_submodule_tree / "technical-docs",
            repo_root=tmp_submodule_tree,
        )
        assert child.depth > root.depth

    def test_has_remote_false(self, tmp_git_repo: Path):
        info = RepoInfo(path=tmp_git_repo, repo_root=tmp_git_repo)
        assert info.has_remote() is False
