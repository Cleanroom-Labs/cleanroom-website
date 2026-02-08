"""
repo_tools/worktree.py
Create and remove git worktrees with automatic submodule initialization.

Ports the zsh add-worktree/init_submodules_from_worktree helper (documented in
docs/submodule-workflow.md) to Python so it works from any shell.
"""
from __future__ import annotations

import re
from pathlib import Path

from repo_tools.repo_utils import Colors, find_repo_root, run_git


def _parse_gitmodules_all(gitmodules_path: Path) -> list[tuple[str, str]]:
    """Parse a .gitmodules file and return (name, path) for ALL submodules.

    Returns an empty list when the file is missing or empty.
    """
    if not gitmodules_path.exists():
        return []

    content = gitmodules_path.read_text()
    results: list[tuple[str, str]] = []

    current_name: str | None = None
    current_path: str | None = None

    for line in content.split("\n"):
        line = line.strip()

        if line.startswith("[submodule"):
            # Save previous section
            if current_name and current_path:
                results.append((current_name, current_path))
            current_name = None
            current_path = None
            # Extract name from [submodule "name"]
            m = re.search(r'"(.+)"', line)
            if m:
                current_name = m.group(1)
        elif line.startswith("path = "):
            current_path = line[7:].strip()

    # Don't forget the last section
    if current_name and current_path:
        results.append((current_name, current_path))

    return results


def _init_submodules(worktree_path: Path, ref_worktree: Path) -> bool:
    """Recursively initialize submodules using the main worktree as reference.

    When the main worktree already has a submodule checked out, temporarily
    overrides the URL to point at that copy (avoiding redundant network
    fetches and resolving local filesystem URLs). Original URLs are restored
    via ``git submodule sync --recursive``.
    """
    gitmodules = worktree_path / ".gitmodules"
    if not gitmodules.exists():
        return True

    # git submodule init
    result = run_git(worktree_path, "submodule", "init", check=False)
    if result.returncode != 0:
        print(f"  {Colors.red('git submodule init failed')} in {worktree_path}")
        return False

    entries = _parse_gitmodules_all(gitmodules)

    # Override each submodule URL to point to the main worktree's copy
    # (only when the reference path exists; otherwise let git use the
    # original URL from .gitmodules, which works for remote URLs)
    for name, subpath in entries:
        ref_path = ref_worktree / subpath
        if ref_path.exists():
            run_git(
                worktree_path,
                "config", f"submodule.{name}.url", str(ref_path),
                check=False,
            )

    # git submodule update
    result = run_git(worktree_path, "submodule", "update", check=False)
    if result.returncode != 0:
        print(f"  {Colors.red('git submodule update failed')} in {worktree_path}")
        return False

    # Recurse into each submodule
    for _name, subpath in entries:
        sub_worktree = worktree_path / subpath
        sub_ref = ref_worktree / subpath
        if not _init_submodules(sub_worktree, sub_ref):
            return False

    # Restore original remote URLs at all levels
    run_git(worktree_path, "submodule", "sync", "--recursive", check=False)

    return True


def add_worktree(args) -> int:
    """Create a git worktree and recursively initialize submodules."""
    try:
        repo_root = find_repo_root()
    except FileNotFoundError as e:
        print(Colors.red(str(e)))
        return 1

    worktree_path = Path(args.path).resolve()

    if worktree_path.exists():
        print(f"{Colors.red('Error')}: path already exists: {worktree_path}")
        return 1

    branch = args.branch

    # Build git worktree add command
    git_args = ["worktree", "add"]
    if not args.checkout:
        git_args.extend(["-b", branch, str(worktree_path)])
    else:
        git_args.extend([str(worktree_path), branch])

    print(f"{Colors.blue('Creating worktree')} at {worktree_path} on branch {Colors.green(branch)}...")

    result = run_git(repo_root, *git_args, check=False, capture=False)
    if result.returncode != 0:
        print(f"{Colors.red('Failed to create worktree')}")
        return 1

    print(f"{Colors.blue('Initializing submodules')} (using main worktree as reference)...")

    if not _init_submodules(worktree_path, repo_root):
        print(f"\n{Colors.yellow('Warning')}: worktree created but submodule initialization failed.")
        print(f"  Path:   {worktree_path}")
        print(f"  Branch: {branch}")
        print("  You may need to initialize submodules manually.")
        return 1

    print(f"\n{Colors.green('Worktree created successfully')}")
    print(f"  Path:   {worktree_path}")
    print(f"  Branch: {branch}")
    return 0


def remove_worktree(args) -> int:
    """Remove a git worktree and prune stale entries."""
    try:
        repo_root = find_repo_root()
    except FileNotFoundError as e:
        print(Colors.red(str(e)))
        return 1

    worktree_path = Path(args.path).resolve()

    git_args = ["worktree", "remove"]
    if args.force:
        git_args.append("--force")
    git_args.append(str(worktree_path))

    print(f"{Colors.blue('Removing worktree')} at {worktree_path}...")

    result = run_git(repo_root, *git_args, check=False, capture=False)
    if result.returncode != 0:
        print(f"{Colors.red('Failed to remove worktree')}")
        return 1

    # Prune stale worktree entries
    run_git(repo_root, "worktree", "prune", check=False)

    print(f"{Colors.green('Worktree removed successfully')}")
    return 0


def run(args) -> int:
    """Entry point for the worktree subcommand."""
    if args.worktree_command == "add":
        return add_worktree(args)
    if args.worktree_command == "remove":
        return remove_worktree(args)
    # Should not be reached (argparse handles unknown subcommands)
    return 2
