#!/usr/bin/env python3
"""
scripts/check-submodules.py
Verifies all submodules are correctly configured and not in detached HEAD.

Usage:
    ./scripts/check-submodules.py           # Basic check
    ./scripts/check-submodules.py --verbose # Show additional details
"""

import argparse
import sys
from pathlib import Path

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent))
from lib.repo_utils import Colors, RepoInfo


def get_tag_or_branch(repo: RepoInfo) -> str | None:
    """
    Get current tag or branch name.
    Returns tag if on an exact tag, otherwise branch name, or None if detached.
    """
    # Try to get exact tag first
    result = repo.git("describe", "--exact-match", "--tags", check=False)
    if result.returncode == 0:
        return result.stdout.strip()

    # Fall back to branch name
    return repo.get_branch()


def get_short_commit(repo: RepoInfo) -> str:
    """Get short commit hash for current HEAD."""
    result = repo.git("rev-parse", "--short", "HEAD", check=False)
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def check_repo_state(repo: RepoInfo, name: str, verbose: bool = False) -> bool:
    """
    Check if a repo is on a branch or tag.
    Returns True if healthy (on branch/tag), False if detached HEAD.
    """
    current = get_tag_or_branch(repo)

    if current:
        print(f"✓ {name} is on: {current}")
        if verbose:
            commit = get_short_commit(repo)
            print(f"    Commit: {commit}")
        return True
    else:
        print(f"⚠️  {name} is in detached HEAD state")
        print(f"    Current commit: {get_short_commit(repo)}")
        return False


def get_submodule_status(repo: RepoInfo) -> str:
    """Get git submodule status output."""
    result = repo.git("submodule", "status", check=False)
    return result.stdout if result.returncode == 0 else ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify all submodules are correctly configured and not in detached HEAD."
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show additional details (commits, remotes)"
    )
    args = parser.parse_args()

    # Determine repo root
    repo_root = Path(__file__).parent.parent.resolve()
    technical_docs = repo_root / "cleanroom-technical-docs"

    if not technical_docs.exists():
        print(f"{Colors.red('Error')}: cleanroom-technical-docs not found")
        return 1

    print("Checking submodule health...")
    print("")

    all_healthy = True

    # Check technical-docs submodule
    tech_docs_repo = RepoInfo(path=technical_docs, repo_root=repo_root)
    if not check_repo_state(tech_docs_repo, "technical-docs", args.verbose):
        all_healthy = False

    # Check each project submodule within technical-docs
    for project_dir in sorted(technical_docs.iterdir()):
        if not project_dir.is_dir():
            continue

        # Check if it's a git submodule (has .git file or directory)
        git_indicator = project_dir / ".git"
        if git_indicator.exists():
            project_name = project_dir.name
            project_repo = RepoInfo(path=project_dir, repo_root=repo_root)

            if not check_repo_state(project_repo, project_name, args.verbose):
                all_healthy = False

    print("")
    print("Submodule status:")
    submodule_status = get_submodule_status(tech_docs_repo)
    if submodule_status:
        print(submodule_status, end="")

    print("")
    print("To fix detached HEAD state:")
    print("  cd cleanroom-technical-docs/<project>-docs")
    print("  git checkout <branch-or-tag>")
    print("  cd ../..")
    print("  git add cleanroom-technical-docs")
    print('  git commit -m "Update submodule reference"')

    return 0 if all_healthy else 1


if __name__ == "__main__":
    sys.exit(main())
