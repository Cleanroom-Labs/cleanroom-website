#!/usr/bin/env python3
"""
scripts/push-submodules.py
Pushes committed changes through nested submodules bottom-up using topological sort.

Usage:
    ./scripts/push-submodules.py           # Push all repos with unpushed commits
    ./scripts/push-submodules.py --dry-run # Preview what would be pushed
    ./scripts/push-submodules.py --force   # Skip validation (recovery scenarios)
"""

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from functools import cached_property
from graphlib import TopologicalSorter
from pathlib import Path
from typing import Optional


class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

    @classmethod
    def red(cls, text: str) -> str:
        return f"{cls.RED}{text}{cls.NC}"

    @classmethod
    def green(cls, text: str) -> str:
        return f"{cls.GREEN}{text}{cls.NC}"

    @classmethod
    def yellow(cls, text: str) -> str:
        return f"{cls.YELLOW}{text}{cls.NC}"

    @classmethod
    def blue(cls, text: str) -> str:
        return f"{cls.BLUE}{text}{cls.NC}"


class RepoStatus(Enum):
    """Validation status for a repository."""
    OK = "ok"
    PENDING = "pending"
    UP_TO_DATE = "up-to-date"
    UNCOMMITTED = "uncommitted"
    DETACHED = "detached"
    NO_REMOTE = "no-remote"


@dataclass
class RepoInfo:
    """Information about a git repository."""
    path: Path
    repo_root: Path

    # Populated during validation
    branch: Optional[str] = None
    ahead_count: Optional[str] = None
    status: RepoStatus = RepoStatus.OK
    error_message: Optional[str] = None
    parent: Optional['RepoInfo'] = field(default=None, repr=False)

    @cached_property
    def rel_path(self) -> str:
        """Get path relative to repo root, or friendly name for root."""
        if self.path == self.repo_root:
            return "(website root)"
        return str(self.path.relative_to(self.repo_root))

    @property
    def depth(self) -> int:
        """Get directory depth for sorting."""
        return len(self.path.parts)

    def git(self, *args: str, check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
        """Run a git command in this repository."""
        cmd = ["git", "-C", str(self.path)] + list(args)
        return subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            check=check,
        )

    def has_uncommitted_changes(self) -> bool:
        """Check if repo has uncommitted changes."""
        diff_result = self.git("diff", "--quiet", check=False)
        cached_result = self.git("diff", "--cached", "--quiet", check=False)
        return diff_result.returncode != 0 or cached_result.returncode != 0

    def get_branch(self) -> Optional[str]:
        """Get current branch name, or None if detached HEAD."""
        result = self.git("branch", "--show-current", check=False)
        branch = result.stdout.strip()
        return branch if branch else None

    def has_remote(self) -> bool:
        """Check if origin remote exists."""
        result = self.git("remote", "get-url", "origin", check=False)
        return result.returncode == 0

    def get_ahead_count(self, branch: str) -> str:
        """Get count of commits ahead of remote. Returns 'new-branch' if remote branch doesn't exist."""
        # Check if upstream is configured
        result = self.git("rev-parse", "--abbrev-ref", "@{upstream}", check=False)
        if result.returncode == 0:
            count_result = self.git("rev-list", "--count", "@{upstream}..HEAD", check=False)
            return count_result.stdout.strip() if count_result.returncode == 0 else "0"

        # No upstream - check if remote branch exists
        ls_result = self.git("ls-remote", "--heads", "origin", branch, check=False)
        if branch in ls_result.stdout:
            count_result = self.git("rev-list", "--count", f"origin/{branch}..HEAD", check=False)
            return count_result.stdout.strip() if count_result.returncode == 0 else "0"

        return "new-branch"

    def validate(self) -> bool:
        """Validate repository state. Returns True if valid for pushing."""
        # Check for uncommitted changes
        if self.has_uncommitted_changes():
            self.status = RepoStatus.UNCOMMITTED
            self.error_message = f"Has uncommitted changes. Run: cd {self.rel_path} && git status"
            return False

        # Check for detached HEAD
        self.branch = self.get_branch()
        if not self.branch:
            self.status = RepoStatus.DETACHED
            self.error_message = f"Detached HEAD state. Run: cd {self.rel_path} && git checkout <branch>"
            return False

        # Check for remote
        if not self.has_remote():
            self.status = RepoStatus.NO_REMOTE
            self.error_message = "No remote 'origin' configured"
            return False

        # Check commits ahead
        self.ahead_count = self.get_ahead_count(self.branch)

        if self.ahead_count == "0":
            self.status = RepoStatus.UP_TO_DATE
        else:
            self.status = RepoStatus.PENDING

        return True

    def push(self, dry_run: bool = False) -> bool:
        """Push repository to remote. Returns True on success."""
        # Branch must be set (validation ensures this)
        assert self.branch is not None, "Cannot push without a branch"

        if self.ahead_count == "new-branch":
            print(f"  {Colors.blue('Pushing')} {self.rel_path} {Colors.yellow(f'(new branch: {self.branch})')}")
        else:
            print(f"  {Colors.blue('Pushing')} {self.rel_path} {Colors.green(f'({self.ahead_count} commits on {self.branch})')}")

        if dry_run:
            return True

        # Try regular push first, then with -u if needed
        result = self.git("push", check=False, capture=False)
        if result.returncode != 0:
            result = self.git("push", "-u", "origin", self.branch, check=False, capture=False)

        return result.returncode == 0


def discover_repos(repo_root: Path) -> list[RepoInfo]:
    """Discover all git repositories (main repo + submodules, excluding cleanroom-theme)."""
    repos = [RepoInfo(path=repo_root, repo_root=repo_root)]

    # Find all submodule .git files
    for git_file in repo_root.rglob(".git"):
        # Skip node_modules
        if "node_modules" in git_file.parts:
            continue

        # Submodules have .git as a file, not directory
        if git_file.is_file():
            submodule_path = git_file.parent

            # Skip cleanroom-theme submodules - they're pinned via submodule pointers
            if submodule_path.name == "cleanroom-theme":
                continue

            repos.append(RepoInfo(path=submodule_path, repo_root=repo_root))

    return repos


def build_dependency_graph(repos: list[RepoInfo]) -> dict[Path, set[Path]]:
    """
    Build a dependency graph where children must be pushed before parents.
    Returns dict mapping repo path -> set of repo paths that must be pushed first.
    """
    paths = {repo.path for repo in repos}

    # Build graph: for each repo, find its parent (if any)
    graph: dict[Path, set[Path]] = {repo.path: set() for repo in repos}

    for repo in repos:
        # Walk up the directory tree to find parent repo
        for parent_path in repo.path.parents:
            if parent_path in paths:
                # Parent depends on child being pushed first
                graph[parent_path].add(repo.path)
                break

    return graph


def topological_sort_repos(repos: list[RepoInfo]) -> list[RepoInfo]:
    """Sort repositories so children come before parents (bottom-up)."""
    graph = build_dependency_graph(repos)

    # Create path -> repo lookup
    path_to_repo = {repo.path: repo for repo in repos}

    # TopologicalSorter gives us nodes in dependency order
    # We need children first, so the graph edges point parent -> child
    sorter = TopologicalSorter(graph)
    sorted_paths = list(sorter.static_order())

    return [path_to_repo[path] for path in sorted_paths]


def print_status_table(repos: list[RepoInfo]) -> None:
    """Print a formatted status table."""
    print(f"\n{Colors.blue('Repository Status:')}")
    print("  " + "─" * 70)
    print(f"  {'Repository':<45} {'Branch':<12} {'Ahead':<10} {'Status':<12}")
    print("  " + "─" * 70)

    for repo in repos:
        status_str = repo.status.value
        branch_str = repo.branch or "?"
        ahead_str = repo.ahead_count or "-"

        if repo.status == RepoStatus.PENDING:
            status_colored = Colors.yellow(status_str)
        elif repo.status == RepoStatus.UP_TO_DATE:
            status_colored = Colors.green(status_str)
        else:
            status_colored = Colors.red(status_str)

        print(f"  {repo.rel_path:<45} {branch_str:<12} {ahead_str:<10} {status_colored}")

    print("  " + "─" * 70)
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Push committed changes through nested submodules bottom-up.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Push all repos with unpushed commits
  %(prog)s --dry-run          # Preview what would be pushed
  %(prog)s --force            # Push even with validation warnings

The script validates that each repo:
  - Is on a branch (not detached HEAD)
  - Has no uncommitted changes
  - Has a pushable remote
  - Has commits ahead of remote
""",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be pushed without pushing",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip validation (for recovery scenarios)",
    )
    args = parser.parse_args()

    # Validate execution context
    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent

    if not (repo_root / "scripts" / "build-docs.mjs").exists():
        print(Colors.red("Error: Must run from cleanroom-website repository"))
        print(f"Current directory: {Path.cwd()}")
        return 1

    os.chdir(repo_root)

    # Discovery phase
    print(Colors.blue("Discovering repositories..."))
    print()

    repos = discover_repos(repo_root)
    print(f"Found {Colors.green(str(len(repos)))} repositories")
    print()

    # Validation phase
    print(Colors.blue("Validating repositories..."))
    print()

    validation_failed = False
    repos_to_push: list[RepoInfo] = []

    for repo in repos:
        if repo.validate():
            if repo.status == RepoStatus.PENDING:
                repos_to_push.append(repo)
        else:
            print(f"  {Colors.red('✗')} {repo.rel_path}")
            print(f"    {Colors.red(repo.error_message or 'Unknown error')}")
            validation_failed = True

    # Print status table
    print_status_table(repos)

    # Handle validation failures
    if validation_failed and not args.force:
        print(Colors.red("Validation failed. Fix the issues above or use --force to skip validation."))
        return 1

    if validation_failed and args.force:
        print(Colors.yellow("Warning: Proceeding despite validation failures (--force)"))
        print()

    # Check if anything to push
    if not repos_to_push:
        print(Colors.green("All repositories are up-to-date. Nothing to push."))
        return 0

    # Sort repos using topological sort (children before parents)
    sorted_repos = topological_sort_repos(repos_to_push)

    # Push phase
    print(Colors.blue(f"Pushing {len(sorted_repos)} repositories (bottom-up)..."))
    if args.dry_run:
        print(Colors.yellow("(dry-run mode - no actual pushes)"))
    print()

    push_failed = False
    pushed_count = 0

    for repo in sorted_repos:
        if repo.push(dry_run=args.dry_run):
            pushed_count += 1
        else:
            push_failed = True
            print(f"  {Colors.red('✗ Failed to push')} {repo.rel_path}")

    print()

    # Final summary
    if args.dry_run:
        print(f"{Colors.yellow('Dry run complete.')} Would push {pushed_count} repositories.")
        print()
        print(Colors.blue("To execute:"))
        print("  ./scripts/push-submodules.py")
    elif push_failed:
        print(Colors.red("Some pushes failed."))
        print()
        print(Colors.blue("Troubleshooting:"))
        print("  - Check remote connectivity: git remote -v")
        print("  - Check authentication: ssh -T git@github.com")
        print("  - Try pushing manually: cd <repo> && git push -v")
        return 1
    else:
        print(Colors.green(f"Successfully pushed {pushed_count} repositories."))
        print()
        print(Colors.blue("Next steps:"))
        print("  1. Verify: ./scripts/check-submodules.sh")
        print("  2. Check CI status on GitHub")

    return 0


if __name__ == "__main__":
    sys.exit(main())
