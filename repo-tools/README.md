# repo-tools

Git submodule management tools for the Cleanroom Labs website repository.

## Overview

`repo-tools` provides a unified CLI for managing the complex git submodule hierarchy in the Cleanroom Labs website. The package includes four subcommands for verifying, synchronizing, pushing, and visualizing nested submodules.

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

Verify that all submodules are on branches (not detached HEAD) and that all instances of the common submodule (`cleanroom-website-common`) are at the same commit.

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

Synchronize the common submodule (`cleanroom-website-common`) across all locations in the repository tree. By default, syncs to the latest commit on `main` from the standalone theme repository.

```bash
# Sync to latest main, commit, and push
repo-tools sync

# Sync to specific commit
repo-tools sync abc1234

# Preview changes without making them
repo-tools sync --dry-run

# Commit changes but skip pushing
repo-tools sync --no-push

# Skip remote sync validation
repo-tools sync --force

# Specify custom theme repository path
repo-tools sync --theme-repo ~/custom/path/cleanroom-website-common

# Verify generated files are up-to-date after sync
repo-tools sync --verify

# Auto-regenerate stale generated files (implies --verify)
repo-tools sync --rebuild
```

**Flags:**
- `commit` (positional) — Target commit SHA (optional)
- `--dry-run` — Preview changes without making them
- `--no-push` — Commit only, skip pushing to remotes
- `--force` — Skip remote sync validation
- `--theme-repo PATH` — Path to standalone theme repository (default: `~/Projects/cleanroom-website-common`)
- `--verify` — Check for stale generated files after sync
- `--rebuild` — Auto-regenerate stale files after sync

**Exit codes:**
- `0` — Sync successful
- `1` — Sync failed or validation error

### `repo-tools visualize`

Open an interactive tkinter GUI showing the git repository hierarchy and submodule relationships. Nodes are color-coded by status:

- **Green** — Clean working directory
- **Yellow** — Uncommitted changes
- **Red** — Error or detached HEAD

```bash
# Visualize current repository
repo-tools visualize

# Visualize specific repository
repo-tools visualize /path/to/repo
```

The GUI supports:
- Zooming (mouse wheel)
- Panning (click and drag)
- Node selection (click node for details)
- Interactive submodule operations

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
│       ├── repo_utils.py       # Shared git utilities
│       ├── check.py            # check subcommand
│       ├── push.py             # push subcommand
│       ├── sync.py             # sync subcommand
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
