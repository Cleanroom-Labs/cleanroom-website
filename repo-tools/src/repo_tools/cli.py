"""
repo_tools.cli
Main CLI entry point: repo-tools {check,push,sync,visualize}
"""

import argparse
import os
import sys
from pathlib import Path

from repo_tools.repo_utils import Colors, DEFAULT_THEME_REPO


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="repo-tools",
        description="Git submodule management tools for Cleanroom Labs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  repo-tools check              Check submodule health and common sync
  repo-tools check -v           Verbose check with commit SHAs
  repo-tools push --dry-run     Preview what would be pushed
  repo-tools sync               Sync common submodule to latest
  repo-tools sync abc1234       Sync to specific commit
  repo-tools visualize          Open interactive submodule visualizer
  repo-tools worktree add my-feature ../website-wt1
  repo-tools worktree remove ../website-wt1
""",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )
    subparsers = parser.add_subparsers(dest="command")

    # --- repo-tools check ---
    check_parser = subparsers.add_parser(
        "check",
        help="Verify submodules are on branches and common submodules are in sync",
        description="Verify all submodules are correctly configured: on a branch "
        "(not detached HEAD) and all common submodules at the same commit.",
    )
    check_parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show additional details (commits, remotes)",
    )

    # --- repo-tools push ---
    push_parser = subparsers.add_parser(
        "push",
        help="Push committed changes through nested submodules bottom-up",
        description="Push committed changes through nested submodules using "
        "topological sort to ensure children are pushed before parents.",
    )
    push_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be pushed without pushing",
    )
    push_parser.add_argument(
        "--force",
        action="store_true",
        help="Skip validation (for recovery scenarios)",
    )

    # --- repo-tools sync ---
    sync_parser = subparsers.add_parser(
        "sync",
        help="Synchronize common submodule across all locations",
        description="Synchronize cleanroom-website-common submodule across all "
        "locations with validation and push support.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  repo-tools sync                       Sync to latest main, commit, and push
  repo-tools sync abc1234               Sync to specific commit
  repo-tools sync --dry-run             Preview what would happen
  repo-tools sync --no-push             Commit only, skip pushing
  repo-tools sync --force               Skip remote sync validation
""",
    )
    sync_parser.add_argument(
        "commit",
        nargs="?",
        help="Target commit SHA (defaults to latest main from standalone repo)",
    )
    sync_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without making them",
    )
    sync_parser.add_argument(
        "--no-push",
        action="store_true",
        help="Commit only, skip pushing (push is default)",
    )
    sync_parser.add_argument(
        "--force",
        action="store_true",
        help="Skip remote sync validation",
    )
    sync_parser.add_argument(
        "--theme-repo",
        type=Path,
        default=DEFAULT_THEME_REPO,
        help="Path to standalone theme repo",
    )
    sync_parser.add_argument(
        "--verify",
        action="store_true",
        help="Check for stale generated files after sync",
    )
    sync_parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Auto-regenerate stale generated files after sync (implies --verify)",
    )

    # --- repo-tools visualize ---
    viz_parser = subparsers.add_parser(
        "visualize",
        help="Open interactive submodule visualizer GUI",
        description="Launch a tkinter GUI that visualizes the git repository "
        "hierarchy and submodule relationships.",
    )
    viz_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to git repository (default: current directory)",
    )

    # --- repo-tools worktree ---
    worktree_parser = subparsers.add_parser(
        "worktree",
        help="Manage git worktrees with automatic submodule initialization",
        description="Create and remove git worktrees with recursive submodule "
        "initialization using the main worktree as a reference.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  repo-tools worktree add my-feature ../cleanroom-website-wt1
  repo-tools worktree add --checkout existing-branch ../wt2
  repo-tools worktree remove ../cleanroom-website-wt1
  repo-tools worktree remove --force ../cleanroom-website-wt1
""",
    )
    worktree_subparsers = worktree_parser.add_subparsers(dest="worktree_command")

    worktree_add_parser = worktree_subparsers.add_parser(
        "add",
        help="Create a new worktree with submodules initialized",
        description="Create a git worktree on a new or existing branch, then "
        "recursively initialize all submodules with URLs pointing to the main "
        "worktree's copies.",
    )
    worktree_add_parser.add_argument(
        "branch",
        help="Branch name to create (or checkout with --checkout)",
    )
    worktree_add_parser.add_argument(
        "path",
        help="Path where the worktree should be created",
    )
    worktree_add_parser.add_argument(
        "--checkout",
        action="store_true",
        help="Checkout an existing branch instead of creating a new one",
    )

    worktree_remove_parser = worktree_subparsers.add_parser(
        "remove",
        help="Remove a worktree and prune stale entries",
        description="Remove a git worktree and run git worktree prune.",
    )
    worktree_remove_parser.add_argument(
        "path",
        help="Path to the worktree to remove",
    )
    worktree_remove_parser.add_argument(
        "--force",
        action="store_true",
        help="Force removal even if the worktree has uncommitted changes",
    )

    args = parser.parse_args(argv)

    # Handle --no-color and NO_COLOR env var
    if args.no_color or os.environ.get("NO_COLOR") is not None:
        Colors.disable()

    if not args.command:
        parser.print_help()
        return 2

    if args.command == "check":
        from repo_tools.check import run
        return run(args)

    if args.command == "push":
        from repo_tools.push import run
        return run(args)

    if args.command == "sync":
        from repo_tools.sync import run
        return run(args)

    if args.command == "visualize":
        from repo_tools.visualizer.__main__ import run
        return run(args)

    if args.command == "worktree":
        if not args.worktree_command:
            worktree_parser.print_help()
            return 2
        from repo_tools.worktree import run
        return run(args)

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
