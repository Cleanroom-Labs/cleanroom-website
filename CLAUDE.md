# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is the **cleanroom-website** repository - a documentation aggregation platform using nested git submodules to manage technical docs for the AirGap project suite (Whisper, Deploy, Transfer). The website builds and serves Sphinx-generated documentation.

## Build Commands

```bash
# Build all documentation (submodules → Sphinx → public/docs)
node scripts/build-docs.mjs

# Helper scripts
./scripts/check-submodules.sh       # Verify submodule health
./scripts/build-single-project.sh   # Build individual project docs
./scripts/update-project-docs.sh    # Update to specific version
./scripts/add-new-project.sh        # Add new project as submodule
./scripts/deploy-release.sh         # Deploy tagged releases
./scripts/test-ci-locally.sh        # Simulate CI locally
```

## Architecture

### Three-Level Nested Submodules

```
cleanroom-website/                    # Level 1 - This repo
└── cleanroom-technical-docs/         # Level 2 - Submodule (aggregator)
    ├── airgap-whisper-docs/          # Level 3 - Submodule
    ├── airgap-deploy-docs/           # Level 3 - Submodule
    ├── airgap-transfer-docs/         # Level 3 - Submodule
    ├── source/                       # Master Sphinx source
    │   ├── index.rst                 # Landing page
    │   └── conf.py                   # Sphinx config with intersphinx
    ├── shared/                       # Shared theme configuration
    └── requirements.txt              # Python Sphinx dependencies
```

### Key Concepts

- **Version coupling**: Git SHAs pin exact documentation versions to website releases
- **Three-commit propagation**: Changes in project docs require commits in: submodule → technical-docs → website
- **Detached HEAD is normal**: Submodules point to specific commits, not branches
- **Dual-homing**: Code repos also include their docs as submodules

### Build Process

1. Submodule verification
2. Python venv setup in `cleanroom-technical-docs/.venv`
3. Dependencies installed from `requirements.txt`
4. Individual project builds (enables intersphinx cross-refs)
5. Master build with cross-reference verification
6. Output copied to `public/docs/`
7. Build fails if any Sphinx warnings

## Working with Submodules

```bash
# Initial setup
git clone --recursive <repo-url>
# or
git submodule update --init --recursive

# Update all submodules
git pull --recurse-submodules

# Make changes in a project's docs
cd cleanroom-technical-docs/<project>-docs
git checkout main  # Switch from detached HEAD to branch
# make changes, commit, push
# then propagate: commit in technical-docs, then in website
```

## Documentation Technology

- **Format**: reStructuredText (.rst) with Sphinx
- **Extensions**: sphinx-needs (traceability), intersphinx (cross-project refs)
- **Directives**: `.. req::`, `.. test::`, `.. usecase::` for requirements traceability
- **System dependency**: Graphviz required for diagrams (`brew install graphviz`)

## Core Design Principles

From `cleanroom-technical-docs/source/meta/principles.rst`:

1. **Privacy Through Data Locality** - No network code in applications
2. **Minimal Dependencies** - Target ≤10 direct Rust dependencies
3. **Simple Architecture** - Write obvious code, avoid abstraction
4. **Air-Gap Ready** - Must work with zero internet access

## CI/CD

- **build-all-docs.yml**: Builds documentation, verifies structure, uploads artifacts
- **verify-submodules.yml**: Weekly health checks, update detection
- **Deployment**: Tag-based (v* for production, v*-rc.* for preview)

## Key Files

- `docs/ARCHITECTURE.md` - Design decisions and alternatives considered
- `docs/SUBMODULES_GUIDE.md` - Daily operations and troubleshooting
- `docs/CI_CD_GUIDE.md` - Workflow setup and environment variables
- `cleanroom-technical-docs/CLAUDE.md` - Guidance for the Sphinx docs submodule
