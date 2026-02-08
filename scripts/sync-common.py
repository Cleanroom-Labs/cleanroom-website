#!/usr/bin/env python3
"""
scripts/sync-common.py
Synchronizes cleanroom-website-common submodule across all locations with validation and push support.

Usage:
    ./scripts/sync-common.py                  # Sync to latest main, commit, and push
    ./scripts/sync-common.py abc1234          # Sync to specific commit
    ./scripts/sync-common.py --dry-run        # Preview changes
    ./scripts/sync-common.py --no-push        # Commit only, skip pushing
    ./scripts/sync-common.py --force          # Skip remote sync validation
    ./scripts/sync-common.py --verify         # Check for stale generated files after sync
    ./scripts/sync-common.py --rebuild        # Auto-regenerate stale files after sync

This script:
1. Resolves the target common submodule commit (from CLI or standalone repo)
2. Discovers all cleanroom-website-common submodule locations
3. Validates parent repos are in sync with remotes (prevents divergence)
4. Updates common submodules to target commit
5. Commits changes bottom-up through the hierarchy
6. Pushes all changes (unless --no-push)
"""

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from lib.repo_utils import (
    Colors,
    RepoInfo,
    RepoStatus,
    print_status_table,
    topological_sort_repos,
)


# Default standalone theme repo path
DEFAULT_THEME_REPO = Path.home() / "Projects" / "cleanroom-website-common"


@dataclass
class ThemeSubmodule:
    """Information about a theme submodule location."""
    path: Path
    parent_repo: Path
    submodule_rel_path: str  # Path relative to parent repo (e.g., "source/theme")
    current_commit: Optional[str] = None

    def git(self, *args: str, check: bool = True, capture: bool = True) -> subprocess.CompletedProcess:
        """Run a git command in this submodule."""
        cmd = ["git", "-C", str(self.path)] + list(args)
        return subprocess.run(cmd, capture_output=capture, text=True, check=check)

    def get_current_commit(self) -> Optional[str]:
        """Get current HEAD commit."""
        result = self.git("rev-parse", "HEAD", check=False)
        return result.stdout.strip() if result.returncode == 0 else None

    def update_to_commit(self, commit: str, dry_run: bool = False) -> bool:
        """Update submodule to target commit."""
        if dry_run:
            return True

        # Fetch all remotes to ensure we have the commit
        self.git("fetch", "--all", "--quiet", check=False)

        # Checkout the target commit (puts it in detached HEAD, which is correct for submodules)
        result = self.git("checkout", commit, "--quiet", check=False)
        return result.returncode == 0


def parse_gitmodules(gitmodules_path: Path) -> list[tuple[str, str]]:
    """
    Parse a .gitmodules file and return list of (path, url) for theme submodules.
    """
    if not gitmodules_path.exists():
        return []

    content = gitmodules_path.read_text()
    results = []

    # Parse submodule sections
    # Format:
    # [submodule "name"]
    #     path = some/path
    #     url = git@github.com:org/repo.git
    current_path = None
    current_url = None

    for line in content.split("\n"):
        line = line.strip()

        # New section
        if line.startswith("[submodule"):
            # Save previous section if it was a theme
            if current_path and current_url and "cleanroom-website-common" in current_url:
                results.append((current_path, current_url))
            current_path = None
            current_url = None
        elif line.startswith("path = "):
            current_path = line[7:].strip()
        elif line.startswith("url = "):
            current_url = line[6:].strip()

    # Don't forget last section
    if current_path and current_url and "cleanroom-website-common" in current_url:
        results.append((current_path, current_url))

    return results


def discover_theme_submodules(repo_root: Path) -> list[ThemeSubmodule]:
    """Discover all cleanroom-website-common submodule locations by parsing .gitmodules files."""
    submodules = []

    # Find all .gitmodules files
    for gitmodules_path in repo_root.rglob(".gitmodules"):
        # Skip node_modules
        if "node_modules" in gitmodules_path.parts:
            continue

        parent_repo = gitmodules_path.parent
        theme_entries = parse_gitmodules(gitmodules_path)

        for submodule_path, _ in theme_entries:
            full_path = parent_repo / submodule_path

            # Verify the submodule exists (has .git file or directory)
            if not (full_path / ".git").exists():
                continue

            submodule = ThemeSubmodule(
                path=full_path,
                parent_repo=parent_repo,
                submodule_rel_path=submodule_path,
            )
            submodule.current_commit = submodule.get_current_commit()
            submodules.append(submodule)

    return submodules


def get_parent_repos_for_submodules(
    theme_submodules: list[ThemeSubmodule],
    repo_root: Path
) -> list[RepoInfo]:
    """
    Get the parent repos that will need commits after updating theme submodules.
    Returns repos sorted by depth (deepest first for bottom-up commits).
    """
    parent_paths = set()

    for submodule in theme_submodules:
        # Add the immediate parent repo
        parent_paths.add(submodule.parent_repo)

        # Walk up to find all ancestor repos that contain submodules
        current = submodule.parent_repo
        while current != repo_root and current != current.parent:
            # Check if this directory is a submodule (has .git file, not directory)
            git_file = current / ".git"
            if git_file.is_file():
                # Find the actual git repo containing this submodule
                for parent in current.parents:
                    if (parent / ".git").is_dir() or (parent / ".git").is_file():
                        parent_paths.add(parent)
                        break
            current = current.parent

    # Always include repo_root
    parent_paths.add(repo_root)

    # Create RepoInfo objects
    repos = [RepoInfo(path=p, repo_root=repo_root) for p in parent_paths]

    # Sort by depth (deepest first)
    repos.sort(key=lambda r: -r.depth)

    return repos


def resolve_target_commit(
    commit_arg: Optional[str],
    theme_repo_path: Path
) -> tuple[str, str]:
    """
    Resolve the target commit SHA.

    Returns:
        Tuple of (full_sha, source_description)
    """
    if commit_arg:
        # Validate it looks like a commit
        if not re.match(r"^[a-f0-9]{7,40}$", commit_arg):
            raise ValueError(f"Invalid commit SHA: {commit_arg}")
        return (commit_arg, "CLI argument")

    # Get latest from standalone repo
    if not theme_repo_path.exists():
        raise ValueError(
            f"Standalone theme repo not found at {theme_repo_path}\n"
            "Please specify a commit SHA explicitly or use --theme-repo PATH"
        )

    # Fetch and get origin/main
    result = subprocess.run(
        ["git", "-C", str(theme_repo_path), "remote", "get-url", "origin"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        # Has origin, fetch and use origin/main
        subprocess.run(
            ["git", "-C", str(theme_repo_path), "fetch", "origin", "main", "--quiet"],
            capture_output=True,
        )
        result = subprocess.run(
            ["git", "-C", str(theme_repo_path), "rev-parse", "origin/main"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return (result.stdout.strip(), f"origin/main from {theme_repo_path}")

    # Fallback to local main
    result = subprocess.run(
        ["git", "-C", str(theme_repo_path), "rev-parse", "main"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return (result.stdout.strip(), f"main from {theme_repo_path}")

    raise ValueError(f"Could not resolve commit from {theme_repo_path}")


def commit_submodule_changes(
    parent_repo: RepoInfo,
    submodule_paths: list[str],
    message: str,
    dry_run: bool = False
) -> bool:
    """
    Commit submodule changes in a parent repo.
    Returns True if a commit was made.
    """
    # Check if there are changes to the specified submodule paths
    has_changes = False
    for subpath in submodule_paths:
        result = parent_repo.git("diff", "--quiet", subpath, check=False)
        if result.returncode != 0:
            has_changes = True
            break

    if not has_changes:
        return False

    if dry_run:
        print(f"  {Colors.yellow('Would commit')} in {parent_repo.rel_path}: {message}")
        return True

    # Stage the submodule paths
    for subpath in submodule_paths:
        parent_repo.git("add", subpath, check=False)

    # Check if anything was staged
    result = parent_repo.git("diff", "--cached", "--quiet", check=False)
    if result.returncode == 0:
        return False

    # Commit
    parent_repo.git("commit", "-m", message, check=False)
    print(f"  {Colors.green('Committed')} in {parent_repo.rel_path}: {message}")
    return True


def push_ahead_theme_submodules(
    theme_submodules: list[ThemeSubmodule],
    dry_run: bool = False
) -> bool:
    """
    Push any theme submodules that are ahead of their remotes.

    This handles the local submodule workflow where changes are made in
    cleanroom-website/common and need to be pushed to the local
    remote (~/Projects/cleanroom-website-common) before syncing to other locations.

    Returns True if any were pushed.
    """
    pushed_any = False

    for submodule in theme_submodules:
        # Check if on a branch (not detached HEAD)
        branch_result = submodule.git("branch", "--show-current", check=False)
        branch = branch_result.stdout.strip()
        if not branch:
            continue  # Skip detached HEAD submodules

        # Fetch from origin to get accurate ahead/behind counts
        submodule.git("fetch", "origin", "--quiet", check=False)

        # Check if ahead of remote
        ahead_result = submodule.git(
            "rev-list", "--count", f"origin/{branch}..HEAD", check=False
        )
        if ahead_result.returncode != 0:
            continue

        ahead_count = ahead_result.stdout.strip()
        if ahead_count and ahead_count != "0":
            rel_path = str(submodule.path.name)
            if dry_run:
                print(f"  {Colors.yellow('Would push')} {rel_path} ({ahead_count} commits ahead)")
            else:
                result = submodule.git("push", "origin", branch, check=False, capture=False)
                if result.returncode == 0:
                    print(f"  {Colors.green('Pushed')} {rel_path} ({ahead_count} commits)")
                    pushed_any = True
                else:
                    print(f"  {Colors.red('Failed to push')} {rel_path}")

    return pushed_any


def check_theme_staleness(theme_path: Path, rebuild: bool = False) -> tuple[bool, str]:
    """
    Check if generated files in a common submodule location are stale.

    Args:
        theme_path: Path to the cleanroom-website-common submodule
        rebuild: If True, regenerate stale files

    Returns:
        Tuple of (is_stale, message)
    """
    staleness_script = theme_path / "scripts" / "check-staleness.js"

    if not staleness_script.exists():
        return (False, "staleness check not available")

    try:
        args = ["node", str(staleness_script)]
        if rebuild:
            args.append("--fix")

        result = subprocess.run(
            args,
            cwd=str(theme_path),
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            if rebuild and "regenerated" in result.stdout.lower():
                return (False, "regenerated")
            return (False, "up-to-date")
        else:
            return (True, "stale")
    except Exception as e:
        return (False, f"error: {e}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Synchronize cleanroom-website-common submodule across all locations.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Sync to latest main, commit, and push
  %(prog)s abc1234                  # Sync to specific commit
  %(prog)s --dry-run                # Preview what would happen
  %(prog)s --no-push                # Commit only, skip pushing
  %(prog)s --force                  # Skip remote sync validation

The script validates parent repos are in sync with remotes before making
changes, to prevent repository divergence. Use --force to skip this check.
""",
    )
    parser.add_argument(
        "commit",
        nargs="?",
        help="Target commit SHA (defaults to latest main from standalone repo)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without making them",
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="Commit only, skip pushing (push is default)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Skip remote sync validation",
    )
    parser.add_argument(
        "--theme-repo",
        type=Path,
        default=DEFAULT_THEME_REPO,
        help=f"Path to standalone theme repo (default: {DEFAULT_THEME_REPO})",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Check for stale generated files in each theme location after sync",
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Auto-regenerate stale generated files after sync (implies --verify)",
    )
    args = parser.parse_args()

    # --rebuild implies --verify
    if args.rebuild:
        args.verify = True

    # Validate execution context
    script_dir = Path(__file__).parent.resolve()
    repo_root = script_dir.parent

    if not (repo_root / "scripts" / "build-docs.mjs").exists():
        print(Colors.red("Error: Must run from cleanroom-website repository"))
        print(f"Current directory: {Path.cwd()}")
        return 1

    os.chdir(repo_root)

    # Phase 0: Push ahead theme submodules (before resolving target commit)
    # This handles the local submodule workflow where cleanroom-website/theme
    # may have commits that need to be pushed to the local remote first.
    print(Colors.blue("Checking for ahead theme submodules..."))
    theme_submodules_early = discover_theme_submodules(repo_root)
    if push_ahead_theme_submodules(theme_submodules_early, args.dry_run):
        print()

    # Phase 1: Resolve target commit
    print(Colors.blue("Resolving target commit..."))
    try:
        target_commit, commit_source = resolve_target_commit(args.commit, args.theme_repo)
    except ValueError as e:
        print(Colors.red(f"Error: {e}"))
        return 1

    print(f"Target: {Colors.green(target_commit[:7])} ({commit_source})")
    print()

    # Phase 2: Discover theme submodules
    print(Colors.blue("Discovering theme submodule locations..."))
    theme_submodules = discover_theme_submodules(repo_root)

    if not theme_submodules:
        print(Colors.red("Error: No theme submodules found"))
        return 1

    print(f"Found {Colors.green(str(len(theme_submodules)))} theme submodule locations:")
    for submodule in theme_submodules:
        rel_path = str(submodule.path.relative_to(repo_root))
        current = submodule.current_commit[:7] if submodule.current_commit else "unknown"
        target_short = target_commit[:7]

        if current == target_short:
            print(f"  {Colors.green('✓')} {rel_path} (already at {current})")
        else:
            print(f"  {Colors.yellow('→')} {rel_path} ({current} → {target_short})")
    print()

    # Check if any updates needed
    submodules_to_update = [
        s for s in theme_submodules
        if not s.current_commit or not s.current_commit.startswith(target_commit[:7])
    ]

    if not submodules_to_update:
        print(Colors.green("All theme submodules already at target commit. Nothing to do."))
        return 0

    # Phase 3: Validate parent repos
    print(Colors.blue("Validating parent repositories..."))

    # Get all parent repos (excluding theme submodules themselves)
    parent_repos = get_parent_repos_for_submodules(theme_submodules, repo_root)

    # Fetch all remotes first
    print("  Fetching from remotes...")
    for repo in parent_repos:
        repo.git("fetch", "--quiet", check=False)

    validation_failed = False
    for repo in parent_repos:
        # Validate with sync check (check if behind remote)
        if repo.validate(check_sync=True):
            pass  # OK
        else:
            print(f"  {Colors.red('✗')} {repo.rel_path}")
            print(f"    {Colors.red(repo.error_message or 'Unknown error')}")
            validation_failed = True

    print_status_table(parent_repos, show_behind=True)

    if validation_failed and not args.force:
        print(Colors.red("Validation failed. Fix the issues above or use --force to skip."))
        print()
        print(Colors.blue("Common fixes:"))
        print("  - Pull latest: cd <repo> && git pull")
        print("  - Checkout branch: cd <repo> && git checkout main")
        return 1

    if validation_failed and args.force:
        print(Colors.yellow("Warning: Proceeding despite validation failures (--force)"))
        print()

    if args.dry_run:
        print(Colors.yellow("Dry run mode - previewing changes:"))
        print()

    # Phase 4: Update theme submodules
    print(Colors.blue("Updating theme submodules..."))
    updated_submodules = []

    for submodule in submodules_to_update:
        rel_path = str(submodule.path.relative_to(repo_root))

        if args.dry_run:
            print(f"  {Colors.yellow('Would update')} {rel_path}")
            updated_submodules.append(submodule)
        else:
            if submodule.update_to_commit(target_commit):
                print(f"  {Colors.green('Updated')} {rel_path}")
                updated_submodules.append(submodule)
            else:
                print(f"  {Colors.red('Failed to update')} {rel_path}")
    print()

    if not updated_submodules:
        print(Colors.yellow("No submodules were updated."))
        return 0

    # Phase 5: Commit bottom-up
    print(Colors.blue("Committing changes bottom-up..."))

    # Build a map of parent repo -> submodule paths that changed
    parent_to_subpaths: dict[Path, list[str]] = {}
    for submodule in updated_submodules:
        parent = submodule.parent_repo
        if parent not in parent_to_subpaths:
            parent_to_subpaths[parent] = []
        parent_to_subpaths[parent].append(submodule.submodule_rel_path)

    # Commit in each parent repo (already sorted by depth, deepest first)
    committed_repos = []
    for repo in parent_repos:
        subpaths = parent_to_subpaths.get(repo.path, [])

        # For intermediate repos (like technical-docs), we need to check for
        # child submodule changes, not theme changes directly
        if not subpaths:
            # Check for any submodule changes
            result = repo.git("diff", "--name-only", check=False)
            if result.returncode == 0 and result.stdout.strip():
                # Stage all submodule changes
                changed_files = result.stdout.strip().split("\n")
                subpaths = [f for f in changed_files if f and ("/" not in f or f.endswith("-docs"))]

        if subpaths:
            if commit_submodule_changes(
                repo,
                subpaths,
                "chore: update common submodule",
                dry_run=args.dry_run,
            ):
                committed_repos.append(repo)
    print()

    # Phase 6: Push (unless --no-push)
    if args.no_push:
        print(Colors.yellow("Skipping push (--no-push specified)"))
        print()
        print(Colors.blue("Next steps:"))
        print("  1. Verify: ./scripts/check-submodules.py")
        print("  2. Build:  node scripts/build-docs.mjs")
        print("  3. Push:   ./scripts/push-submodules.py")
        return 0


    if not committed_repos and not args.dry_run:
        print(Colors.green("No commits made - nothing to push."))
        return 0

    # Re-validate repos to get accurate ahead counts
    repos_to_push = []
    for repo in parent_repos:
        repo.ahead_count = None  # Reset
        repo.behind_count = None
        repo.status = RepoStatus.OK
        if repo.validate():
            if repo.status == RepoStatus.PENDING:
                repos_to_push.append(repo)

    if not repos_to_push and not args.dry_run:
        print(Colors.green("All repositories up-to-date. Nothing to push."))
        return 0

    print(Colors.blue(f"Pushing {len(repos_to_push)} repositories..."))
    if args.dry_run:
        print(Colors.yellow("(dry-run mode - no actual pushes)"))
    print()

    # Sort repos for pushing (children before parents)
    sorted_repos = topological_sort_repos(repos_to_push)

    push_failed = False
    pushed_count = 0

    for repo in sorted_repos:
        if repo.push(dry_run=args.dry_run):
            pushed_count += 1
        else:
            push_failed = True
            print(f"  {Colors.red('✗ Failed to push')} {repo.rel_path}")

    print()

    # Phase 7: Verify staleness (optional)
    staleness_warning = False
    if args.verify and not args.dry_run:
        print(Colors.blue("Verifying generated files..."))

        for submodule in theme_submodules:
            rel_path = str(submodule.path.relative_to(repo_root))
            is_stale, status = check_theme_staleness(submodule.path, rebuild=args.rebuild)

            if is_stale:
                staleness_warning = True
                print(f"  {Colors.yellow('⚠')} {rel_path}: {status}")
            else:
                status_color = Colors.green if status == "up-to-date" else Colors.yellow
                print(f"  {status_color('✓')} {rel_path}: {status}")

        print()

        if staleness_warning:
            print(Colors.yellow("Warning: Some theme locations have stale generated files."))
            print()
            print(Colors.blue("To fix:"))
            print("  1. cd to each theme location")
            print("  2. Run: npm run build")
            print("  3. Commit and push the regenerated files")
            print()
            print("Or run: ./scripts/sync-common.py --rebuild")
            print()

    # Final summary
    if args.dry_run:
        print(f"{Colors.yellow('Dry run complete.')}")
        print()
        print(Colors.blue("Summary:"))
        print(f"  Target commit: {target_commit[:7]}")
        print(f"  Submodules to update: {len(updated_submodules)}")
        print(f"  Commits to make: {len(committed_repos)}")
        print(f"  Repos to push: {len(repos_to_push)}")
        print()
        print(Colors.blue("To execute:"))
        print("  ./scripts/sync-common.py")
    elif push_failed:
        print(Colors.red("Some pushes failed."))
        print()
        print(Colors.blue("Troubleshooting:"))
        print("  - Check remote connectivity: git remote -v")
        print("  - Try pushing manually: ./scripts/push-submodules.py")
        return 1
    else:
        print(Colors.green("Theme sync complete!"))
        print()
        print(Colors.blue("Summary:"))
        print(f"  Target commit: {target_commit[:7]}")
        print(f"  Submodules updated: {len(updated_submodules)}")
        print(f"  Repos pushed: {pushed_count}")
        print()
        print(Colors.blue("Next steps:"))
        print("  1. Verify: ./scripts/check-submodules.py")
        print("  2. Build:  node scripts/build-docs.mjs")

    return 0


if __name__ == "__main__":
    sys.exit(main())
