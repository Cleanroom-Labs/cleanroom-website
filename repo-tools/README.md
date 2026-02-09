# repo-tools

Git submodule management tools for the Cleanroom Labs website repository.

## Overview

`repo-tools` provides a unified CLI for managing the complex git submodule hierarchy in the Cleanroom Labs website. The package includes subcommands for verifying, synchronizing, pushing, visualizing, and managing worktrees of nested submodules.

All subcommands can be run from any subdirectory within the repository. Configuration (`.repo-tools.toml`) is optional — commands gracefully handle repos without it.

## Installation

Install in development mode from the `repo-tools/` directory:

```bash
cd repo-tools
pip install -e .
```

For development with testing dependencies:

```bash
pip install -e ".[dev]"
```

**Requirements:** Python 3.11+

## Usage

### `repo-tools check`

Verify that all submodules are on branches (not detached HEAD) and that all sync-group submodules are at the same commit. When no sync groups are configured (no `.repo-tools.toml`), the sync-group check is skipped with a warning.

```bash
# Basic check
repo-tools check

# Verbose output with commit SHAs and remotes
repo-tools check -v
repo-tools check --verbose
```

**Exit codes:**
- `0` — All checks passed
- `1` — One or more issues found

### `repo-tools push`

Push committed changes through nested submodules in bottom-up order using topological sort. This ensures child submodules are pushed before their parents.

```bash
# Push all submodules
repo-tools push

# Dry run: preview what would be pushed
repo-tools push --dry-run

# Force push (skip validation, for recovery scenarios)
repo-tools push --force
```

**Exit codes:**
- `0` — Push successful
- `1` — Push failed or validation error

### `repo-tools sync`

Synchronize submodule sync groups (defined in `.repo-tools.toml`) across all locations in the repository tree. By default, syncs to the latest commit on `main` from the standalone repo or remote URL.

```bash
# Sync all groups to latest
repo-tools sync

# Sync just the "common" group
repo-tools sync common

# Sync "common" to a specific commit
repo-tools sync common abc1234

# Preview changes without making them
repo-tools sync --dry-run

# Commit changes but skip pushing
repo-tools sync --no-push

# Skip remote sync validation
repo-tools sync --force
```

**Flags:**
- `group` (positional) — Sync group name (syncs all groups if omitted)
- `commit` (positional) — Target commit SHA (optional)
- `--dry-run` — Preview changes without making them
- `--no-push` — Commit only, skip pushing to remotes
- `--force` — Skip remote sync validation

**Exit codes:**
- `0` — Sync successful (or no sync groups configured)
- `1` — Sync failed or validation error

### `repo-tools visualize`

Open an interactive tkinter GUI showing the git repository hierarchy and submodule relationships. Can be run from any subdirectory within a repository. Nodes are color-coded by status:

- **Green** — Clean working directory
- **Yellow** — Uncommitted changes
- **Red** — Error or detached HEAD

Sync-group submodules are outlined with a distinct border color per group.

```bash
# Visualize current repository (auto-detects repo root)
repo-tools visualize

# Visualize specific repository
repo-tools visualize /path/to/repo
```

The GUI supports:
- Zooming (mouse wheel)
- Panning (click and drag)
- Node selection (click node for details)
- Interactive submodule operations

### `repo-tools worktree`

Create and remove git worktrees with automatic recursive submodule initialization. Local git config (e.g. `user.name`, `user.email`, signing settings) is copied from the main worktree and its submodules to the new worktree by default. Structural keys (`core.*`, `remote.*`, `submodule.*`, `extensions.*`, `gc.*`) are excluded.

```bash
# Create a new worktree with a new branch
repo-tools worktree add feature-x ../feature-x-wt

# Create a worktree using an existing branch
repo-tools worktree add --checkout existing-branch ../wt-path

# Skip copying local git config
repo-tools worktree add --no-copy-config feature-x ../feature-x-wt

# Remove a worktree
repo-tools worktree remove ../feature-x-wt

# Force-remove a worktree with uncommitted changes
repo-tools worktree remove --force ../feature-x-wt
```

## Development

### Running Tests

```bash
cd repo-tools
pytest
```

### Project Structure

```
repo-tools/
├── pyproject.toml              # Package configuration
├── README.md                   # This file
├── docs/
│   └── submodule-workflow.md   # Detailed workflow documentation
├── src/
│   └── repo_tools/
│       ├── __init__.py
│       ├── cli.py              # Main CLI entry point
│       ├── config.py           # .repo-tools.toml loader
│       ├── repo_utils.py       # Shared git utilities
│       ├── check.py            # check subcommand
│       ├── push.py             # push subcommand
│       ├── sync.py             # sync subcommand
│       ├── worktree.py         # worktree subcommand
│       └── visualizer/         # visualize subcommand
│           ├── __init__.py
│           ├── __main__.py
│           ├── actions.py
│           ├── app.py
│           ├── graph_canvas.py
│           ├── layout.py
│           └── repo_node.py
└── tests/                      # Test suite
```

## Documentation

For detailed workflow guidance, see:
- [docs/submodule-workflow.md](docs/submodule-workflow.md) — Common workflows and troubleshooting
- [../docs/SUBMODULES_GUIDE.md](../docs/SUBMODULES_GUIDE.md) — Repository-wide submodule documentation
- [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) — Submodule design rationale

## License

Part of the Cleanroom Labs website repository.
