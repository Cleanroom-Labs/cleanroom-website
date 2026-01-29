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
import sys
from pathlib import Path

from lib.repo_utils import (
    Colors,
    RepoStatus,
    discover_repos,
    print_status_table,
    topological_sort_repos,
)


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
  - Has no uncommitted changes
  - Has a pushable remote (if it needs pushing)
  - Is on a branch (for repos that will be pushed)
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
    repos_to_push: list = []

    for repo in repos:
        if repo.validate(allow_detached=True, allow_no_remote=True):
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
        print("  1. Verify: ./scripts/check-submodules.py")
        print("  2. Check CI status on GitHub")

    return 0


if __name__ == "__main__":
    sys.exit(main())
