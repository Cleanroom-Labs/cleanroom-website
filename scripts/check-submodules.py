#!/usr/bin/env python3
"""
scripts/check-submodules.py
Verifies all submodules are correctly configured: on a branch (not detached HEAD)
and all common (cleanroom-website-common) submodules at the same commit.

Usage:
    ./scripts/check-submodules.py           # Basic check
    ./scripts/check-submodules.py --verbose # Show additional details
"""

import argparse
import sys
from pathlib import Path

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent))
from lib.repo_utils import Colors, RepoInfo, discover_repos


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


def check_repo_state(repo: RepoInfo, name: str, verbose: bool = False) -> bool:
    """
    Check if a repo is on a branch or tag.
    Returns True if healthy (on branch/tag), False if detached HEAD.
    """
    current = get_tag_or_branch(repo)

    if current:
        commit_info = ""
        if verbose:
            commit_info = f" ({repo.get_commit_sha(short=True)})"
        print(f"  {Colors.green('✓')} {name} is on: {current}{commit_info}")
        return True
    else:
        print(f"  {Colors.red('✗')} {name} is in detached HEAD state")
        print(f"      Current commit: {repo.get_commit_sha(short=True)}")
        return False


def check_common_sync(repo_root: Path, verbose: bool = False) -> bool:
    """
    Verify all common (cleanroom-website-common) submodules are at the same commit.
    Returns True if all in sync, False if any differ.
    """
    # Discover all repos including common submodules
    all_repos = discover_repos(repo_root, exclude_theme=False)

    # Filter to common submodules only
    common_repos = [r for r in all_repos if r.name == "common"]

    if not common_repos:
        print(f"  {Colors.yellow('⚠')} No common submodules found")
        return True

    # Get commit for each
    commits: dict[str, str] = {}
    for repo in common_repos:
        sha = repo.get_commit_sha(short=True)
        commits[repo.rel_path] = sha

    unique_commits = set(commits.values())

    if len(unique_commits) == 1:
        commit = next(iter(unique_commits))
        print(f"  {Colors.green('✓')} All {len(common_repos)} common submodules at {commit}")
        if verbose:
            for rel_path in sorted(commits):
                print(f"      {rel_path:<40} {commits[rel_path]}")
        return True

    # Out of sync — find the most common commit (majority)
    from collections import Counter
    commit_counts = Counter(commits.values())
    majority_commit = commit_counts.most_common(1)[0][0]

    print(f"  {Colors.red('✗')} Common submodules are NOT in sync "
          f"({len(unique_commits)} unique commits across {len(common_repos)} locations)")

    for rel_path in sorted(commits):
        sha = commits[rel_path]
        if sha != majority_commit:
            print(f"      {rel_path:<40} {sha}  {Colors.red('← differs')}")
        else:
            print(f"      {rel_path:<40} {sha}")

    return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify all submodules are correctly configured and in sync."
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show additional details (commits, remotes)"
    )
    args = parser.parse_args()

    # Determine repo root
    repo_root = Path(__file__).parent.parent.resolve()
    technical_docs = repo_root / "technical-docs"

    if not technical_docs.exists():
        print(f"{Colors.red('Error')}: technical-docs not found")
        return 1

    all_healthy = True
    issues: list[str] = []

    # Section 1: Check project submodules are on branches
    print(Colors.blue("Checking submodule branches..."))

    # Check technical-docs submodule
    tech_docs_repo = RepoInfo(path=technical_docs, repo_root=repo_root)
    if not check_repo_state(tech_docs_repo, "technical-docs", args.verbose):
        all_healthy = False
        issues.append("detached-head")

    # Check each project submodule within technical-docs
    for project_dir in sorted(technical_docs.iterdir()):
        if not project_dir.is_dir():
            continue

        # Check if it's a git submodule (has .git file) — skip common submodules
        git_indicator = project_dir / ".git"
        if git_indicator.exists() and project_dir.name != "common":
            project_repo = RepoInfo(path=project_dir, repo_root=repo_root)

            if not check_repo_state(project_repo, project_dir.name, args.verbose):
                all_healthy = False
                issues.append("detached-head")

    print()

    # Section 2: Check common submodule sync
    print(Colors.blue("Checking common submodule sync..."))

    if not check_common_sync(repo_root, args.verbose):
        all_healthy = False
        issues.append("common-out-of-sync")

    print()

    # Section 3: Summary and remediation
    if all_healthy:
        print(Colors.green("All checks passed."))
    else:
        print(Colors.red("Issues found:"))

        if "detached-head" in issues:
            print()
            print(f"  {Colors.yellow('Detached HEAD fix:')}")
            print("    cd technical-docs/<project>")
            print("    git checkout <branch-or-tag>")
            print("    cd ../..")
            print("    git add technical-docs")
            print('    git commit -m "Update submodule reference"')

        if "common-out-of-sync" in issues:
            print()
            print(f"  {Colors.yellow('Common submodule sync fix:')}")
            print("    ./scripts/sync-common.py")

    return 0 if all_healthy else 1


if __name__ == "__main__":
    sys.exit(main())
