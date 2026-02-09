"""
repo_tools.cli
Main CLI entry point: repo-tools {check,push,sync,visualize}
"""

import argparse
import os
import sys

from repo_tools.repo_utils import Colors


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="repo-tools",
        description="Git submodule management tools.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  repo-tools check              Check submodule health and sync groups
  repo-tools check -v           Verbose check with commit SHAs
  repo-tools push --dry-run     Preview what would be pushed
  repo-tools sync               Sync all groups to latest
  repo-tools sync common        Sync just "common" group
  repo-tools sync common abc123 Sync "common" to specific commit
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
        help="Verify submodules are on branches and sync groups are consistent",
        description="Verify all submodules are correctly configured: on a branch "
        "(not detached HEAD) and all sync-group submodules at the same commit.",
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
        help="Synchronize submodule sync groups across all locations",
        description="Synchronize submodule sync groups across all "
        "locations with validation and push support.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  repo-tools sync                       Sync all groups to latest
  repo-tools sync common                Sync just "common" group
  repo-tools sync common abc1234        Sync "common" to specific commit
  repo-tools sync --dry-run             Preview what would happen
  repo-tools sync --no-push             Commit only, skip pushing
  repo-tools sync --force               Skip remote sync validation
""",
    )
    sync_parser.add_argument(
        "group",
        nargs="?",
        help="Sync group name (syncs all groups if omitted)",
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
  repo-tools worktree add my-feature ../my-project-wt1
  repo-tools worktree add --checkout existing-branch ../wt2
  repo-tools worktree remove ../my-project-wt1
  repo-tools worktree remove --force ../my-project-wt1
  repo-tools worktree merge my-feature
  repo-tools worktree merge --continue
  repo-tools worktree merge --abort
  repo-tools worktree merge --status
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
    worktree_add_parser.add_argument(
        "--no-copy-config",
        action="store_true",
        help="Skip copying local git config from the main worktree",
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

    worktree_merge_parser = worktree_subparsers.add_parser(
        "merge",
        help="Merge a branch across all submodules bottom-up",
        description="Merge a feature branch into the current branch across all "
        "repos in the submodule tree, processing leaves first.",
    )
    worktree_merge_parser.add_argument(
        "branch",
        nargs="?",
        help="Branch to merge into the current branch",
    )
    worktree_merge_parser.add_argument(
        "--continue",
        action="store_true",
        dest="continue_merge",
        help="Resume after resolving a conflict or test failure",
    )
    worktree_merge_parser.add_argument(
        "--abort",
        action="store_true",
        help="Undo all merges and restore pre-merge state",
    )
    worktree_merge_parser.add_argument(
        "--status",
        action="store_true",
        help="Show current merge progress",
    )
    worktree_merge_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without merging",
    )
    worktree_merge_parser.add_argument(
        "--no-recurse",
        action="store_true",
        help="Only operate on the root repo",
    )
    worktree_merge_parser.add_argument(
        "--no-ff",
        action="store_true",
        help="Always create a merge commit (even for fast-forwards)",
    )
    worktree_merge_parser.add_argument(
        "--no-test",
        action="store_true",
        help="Skip running test commands",
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
        if args.worktree_command == "merge":
            from repo_tools.worktree_merge import run
            return run(args)
        from repo_tools.worktree import run
        return run(args)

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
