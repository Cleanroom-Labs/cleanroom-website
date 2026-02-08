"""Shared fixtures for repo-tools tests."""

import subprocess
import sys
from pathlib import Path

import pytest

# Make the src/ directory importable without installing the package.
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    """Run a git command inside *cwd* and return the CompletedProcess."""
    return subprocess.run(
        ["git", "-C", str(cwd)] + list(args),
        capture_output=True,
        text=True,
        check=True,
    )


@pytest.fixture()
def tmp_git_repo(tmp_path: Path) -> Path:
    """Create a bare-bones temporary git repository with one initial commit.

    Returns the repository root path.
    """
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test User")

    # Create an initial commit so HEAD exists.
    readme = repo / "README.md"
    readme.write_text("# test repo\n")
    _git(repo, "add", "README.md")
    _git(repo, "commit", "-m", "Initial commit")

    return repo


@pytest.fixture()
def tmp_submodule_tree(tmp_path: Path) -> Path:
    """Create a parent repo with nested submodules.

    Layout::

        parent/                     (main repo -- project root)
        +-- technical-docs/         (submodule pointing at child repo)
        |   +-- common/             (submodule pointing at grandchild repo)
        +-- .repo-tools.toml        (optional config)

    Returns the *parent* repository path.
    """
    # ---- grandchild repo (stands in for a shared submodule) ----
    grandchild = tmp_path / "grandchild_origin"
    grandchild.mkdir()
    _git(grandchild, "init")
    _git(grandchild, "config", "user.email", "test@example.com")
    _git(grandchild, "config", "user.name", "Test User")
    (grandchild / "theme.txt").write_text("theme content\n")
    _git(grandchild, "add", "theme.txt")
    _git(grandchild, "commit", "-m", "Initial grandchild commit")

    # ---- child repo (stands in for technical-docs) ----
    child = tmp_path / "child_origin"
    child.mkdir()
    _git(child, "init")
    _git(child, "config", "user.email", "test@example.com")
    _git(child, "config", "user.name", "Test User")
    (child / "index.rst").write_text("index\n")
    _git(child, "add", "index.rst")
    _git(child, "commit", "-m", "Initial child commit")

    # Add grandchild as a submodule named "common" inside child.
    _git(child, "submodule", "add", str(grandchild), "common")
    _git(child, "commit", "-m", "Add common submodule")

    # ---- parent repo (stands in for the project root) ----
    parent = tmp_path / "parent"
    parent.mkdir()
    _git(parent, "init")
    _git(parent, "config", "user.email", "test@example.com")
    _git(parent, "config", "user.name", "Test User")

    # Create .repo-tools.toml with a sync group for testing.
    # The grandchild repo URL will be a local path; url-match uses a
    # substring that appears in that path.
    (parent / ".repo-tools.toml").write_text(
        '[sync-groups.common]\n'
        f'url-match = "grandchild_origin"\n'
        f'standalone-repo = "{grandchild}"\n'
    )

    _git(parent, "add", ".repo-tools.toml")
    _git(parent, "commit", "-m", "Initial parent commit")

    # Add child as a submodule named "technical-docs" inside parent.
    _git(parent, "submodule", "add", str(child), "technical-docs")
    _git(parent, "commit", "-m", "Add technical-docs submodule")

    # Recursively initialise so the nested grandchild submodule is available.
    _git(parent, "submodule", "update", "--init", "--recursive")

    # Configure git user inside the submodule worktrees (needed for commits
    # that tests may make inside these directories).
    for sub in [parent / "technical-docs", parent / "technical-docs" / "common"]:
        if (sub / ".git").exists():
            _git(sub, "config", "user.email", "test@example.com")
            _git(sub, "config", "user.name", "Test User")

    return parent
