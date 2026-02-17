[![Netlify Status](https://api.netlify.com/api/v1/badges/cfbc479f-26a0-4031-aa6c-f4d80183e7c2/deploy-status)](https://app.netlify.com/projects/cleanroomlabswebsite/deploys)

# Cleanroom Website

Documentation aggregation platform using nested git submodules to manage technical documentation for multiple projects with version-coupled releases.

## Prerequisites

- Python 3.14+
- Node.js 20.9+ (required by Next.js 16; see `.nvmrc`)
- Graphviz (`brew install graphviz` on macOS)

## Getting Started

```bash
# Clone with all submodules
git clone --recursive <repo-url>
cd cleanroom-website

# Or initialize submodules after cloning
git submodule update --init --recursive

# Install grove (submodule management CLI)
pip install -r requirements.txt
# Or for active grove development: pip install -e ~/Projects/cleanroom-labs/grove

# Build documentation
node scripts/build-docs.mjs
```

Output is generated to `public/docs/index.html`.

## Build Commands

### npm Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server (webpack; uses existing built docs) |
| `npm run dev:clean` | Rebuild docs, then start dev server (webpack) |
| `npm run build` | Build docs + production site build (webpack) |
| `npm run build:web` | Build the Next.js site only (webpack; skips docs) |
| `npm run build-docs` | Build Sphinx documentation only |
| `npm run start` | Start production server |
| `npm run lint` | Print lint setup guidance (linting not configured yet) |

### Shell Scripts

| Command | Description |
|---------|-------------|
| `./scripts/build-single-project.sh <project>` | Build single project docs |
| `./scripts/update-project-docs.sh <project> <version>` | Update project to version |
| `./scripts/add-new-project.sh <project> <repo-url>` | Add new project |
| `./scripts/deploy-release.sh <project> <version>` | Deploy tagged release |
| `./scripts/test-ci-locally.sh` | Simulate CI locally |
| `python -m scripts.generate-pdf` | Generate comprehensive PDF from website |

## Grove (Submodule Management)

Grove is a CLI for managing the nested git submodule hierarchy in this repository. It handles verification, synchronization, pushing, visualization, and worktree management across all submodules.

### Installation

```bash
pip install -r requirements.txt
```

For active grove development, use an editable install from the [grove repository](https://github.com/Cleanroom-Labs/grove):

```bash
pip install -e ~/Projects/cleanroom-labs/grove
```

Requires Python 3.11+. All commands can be run from any subdirectory.

### Commands

| Command | Description |
|---------|-------------|
| `grove init` | Generate a template `.grove.toml` with all options documented |
| `grove check` | Verify submodule health and sync group consistency |
| `grove check -v` | Verbose check with commit SHAs and remotes |
| `grove push` | Push changes bottom-up through nested submodules |
| `grove push --dry-run` | Preview what would be pushed |
| `grove sync` | Sync all submodule sync groups to latest |
| `grove sync common` | Sync a specific group |
| `grove visualize` | Open interactive submodule visualizer GUI |
| `grove worktree add <branch> <path>` | Create worktree with submodule init |
| `grove worktree remove <path>` | Remove a worktree |
| `grove worktree merge <branch>` | Merge feature branch across all submodules bottom-up |
| `grove worktree merge --continue` | Resume after resolving conflicts |
| `grove worktree merge --abort` | Abort and restore pre-merge state |
| `grove claude install` | Install Claude Code skills for grove workflows |

### Configuration

Grove reads `.grove.toml` in the repository root for sync group definitions and worktree merge test commands. Configuration is optional — commands gracefully handle repos without it.

See the [grove repository](https://github.com/Cleanroom-Labs/grove) for full documentation including flags, exit codes, and configuration format.

### Claude Code Skills

Grove ships Claude Code skills for common workflows. Install them with:

```bash
grove claude install          # Project scope (.claude/skills/)
grove claude install --user   # User scope (~/.claude/skills/)
grove claude install --check  # Check if skills are up to date
```

Installed skills:

| Skill | Description |
|-------|-------------|
| `/grove-ship` | Health check all submodules, then push if clean |
| `/grove-feature <branch> [path]` | Create a feature branch worktree with submodule init |
| `/grove-sync [group] [commit]` | Sync submodule groups with dry-run preview |
| `/grove-merge <branch>` | Merge feature branch bottom-up with conflict handling |

## Mobile Testing with ngrok

To test the site from a mobile device or share a preview URL:

```bash
# Install ngrok
brew install ngrok

# Start dev server and tunnel
npm run dev
ngrok http 3000  # In another terminal
```

Access the generated URL (e.g., `https://abc123.ngrok.io`) from any device. Press `Ctrl+C` to stop the tunnel.

## PDF Generation

Generate a comprehensive PDF report from the website content:

```bash
# Prerequisites: build docs and start dev server
npm run build-docs
npm run dev  # In a separate terminal

# macOS: install system dependencies and set library path
brew install pango glib
export DYLD_LIBRARY_PATH=/opt/homebrew/lib

# Generate PDF
python -m scripts.generate-pdf

# Options
python -m scripts.generate-pdf --output custom-output.pdf
python -m scripts.generate-pdf --skip-screenshots  # Use cached screenshots
python -m scripts.generate-pdf --draft              # Add DRAFT watermark
```

The PDF includes:
- Cover page with hero section screenshot
- Table of contents with clickable navigation
- All blog posts (sorted by date)
- Complete technical documentation

See [scripts/generate-pdf/README.md](scripts/generate-pdf/README.md) for details.

See [docs/SUBMODULES_GUIDE.md](docs/SUBMODULES_GUIDE.md) for submodule operations and release workflows.

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the submodule structure, design rationale, and alternatives considered.

## Documentation Technology

- **Sphinx** with reStructuredText (.rst)
- **sphinx-needs** for requirements traceability (`:req:`, `:test:`, `:usecase:` directives)
- **intersphinx** for cross-project references
- **Graphviz** for diagram generation

## CI/CD

| Workflow | Location | Purpose |
|----------|----------|---------|
| `build-all-docs.yml` | `cleanroom-website` | Build and verify all documentation |
| `verify-submodules.yml` | `cleanroom-website` | Weekly submodule health checks |
| `sphinx-docs.yml` | `technical-docs` | Build, check warnings, and verify docs |

See [docs/CI_CD_GUIDE.md](docs/CI_CD_GUIDE.md) for details.

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - Design decisions and rationale
- [Submodules Guide](docs/SUBMODULES_GUIDE.md) - Daily operations
- [CI/CD Guide](docs/CI_CD_GUIDE.md) - Workflow configuration
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Production deployment steps
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [Style Guide](docs/STYLE_GUIDE.md) - Writing conventions and terminology
