# Cleanroom Website

Documentation aggregation platform using nested git submodules to manage technical documentation for multiple projects with version-coupled releases.

## Prerequisites

- Python 3.9+
- Node.js (for build scripts)
- Graphviz (`brew install graphviz` on macOS)

## Getting Started

```bash
# Clone with all submodules
git clone --recursive <repo-url>
cd cleanroom-website

# Or initialize submodules after cloning
git submodule update --init --recursive

# Build documentation
node scripts/build-docs.mjs
```

Output is generated to `public/docs/index.html`.

## Repository Structure

```
cleanroom-website/                    # This repo
├── cleanroom-technical-docs/         # Submodule - documentation aggregator
│   ├── <project>-docs/               # Submodules - individual project docs
│   ├── source/                       # Master Sphinx source
│   ├── shared/                       # Shared theme configuration
│   └── requirements.txt              # Python dependencies
├── scripts/                          # Build and deployment automation
├── docs/                             # Developer documentation
└── public/docs/                      # Generated output (gitignored)
```

## Build Commands

| Command | Description |
|---------|-------------|
| `node scripts/build-docs.mjs` | Build all documentation |
| `./scripts/check-submodules.sh` | Verify submodule health |
| `./scripts/build-single-project.sh <project>` | Build single project docs |
| `./scripts/update-project-docs.sh <project> <version>` | Update project to version |
| `./scripts/add-new-project.sh <project> <repo-url>` | Add new project |
| `./scripts/deploy-release.sh <project> <version>` | Deploy tagged release |
| `./scripts/test-ci-locally.sh` | Simulate CI locally |

## Working with Submodules

### Update All Submodules

```bash
git pull --recurse-submodules
```

### Make Changes to Project Documentation

```bash
cd cleanroom-technical-docs/<project>-docs
git checkout main                    # Switch from detached HEAD
# make changes
git add . && git commit -m "Update"
git push

# Propagate to parent repos (3 commits total)
cd ..
git add <project>-docs && git commit -m "Update reference" && git push

cd ..
git add cleanroom-technical-docs && git commit -m "Update reference" && git push
```

### Release Workflow

```bash
# Tag the docs
cd cleanroom-technical-docs/<project>-docs
git tag v1.0.0 && git push origin v1.0.0

# Deploy to website
cd /path/to/cleanroom-website
./scripts/deploy-release.sh <project> v1.0.0
```

## Architecture

This repository uses a **three-level nested submodule architecture**:

1. **Website → Technical Docs**: Single submodule coupling website to docs aggregator
2. **Technical Docs → Project Docs**: Multiple submodules for each project
3. **Code Repos → Project Docs**: Dual-homing allows code repos to include their docs

Key characteristics:
- **Version coupling** via git SHAs ensures docs match website releases
- **Detached HEAD is normal** - submodules point to specific commits
- **Changes require 3 commits** to propagate from project docs to website

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for design rationale and alternatives considered.

## Documentation Technology

- **Sphinx** with reStructuredText (.rst)
- **sphinx-needs** for requirements traceability (`:req:`, `:test:`, `:usecase:` directives)
- **intersphinx** for cross-project references
- **Graphviz** for diagram generation

## CI/CD

| Workflow | Purpose |
|----------|---------|
| `build-all-docs.yml` | Build and verify documentation |
| `verify-submodules.yml` | Weekly submodule health checks |

Deployment uses tag-based releases:
- `v*` tags trigger production deployment
- `v*-rc.*` tags trigger preview deployment

See [docs/CI_CD_GUIDE.md](docs/CI_CD_GUIDE.md) for details.

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - Design decisions and rationale
- [Submodules Guide](docs/SUBMODULES_GUIDE.md) - Daily operations and troubleshooting
- [CI/CD Guide](docs/CI_CD_GUIDE.md) - Workflow configuration
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Production deployment steps
- [Migration Plan](migration-plan.md) - Original migration documentation
