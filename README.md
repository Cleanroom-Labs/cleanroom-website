# Cleanroom Website

Documentation aggregation platform using nested git submodules to manage technical documentation for multiple projects with version-coupled releases.

## Prerequisites

- Python 3.9+
- Node.js 20.9+ (required by Next.js 16)
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
| `./scripts/check-submodules.py` | Verify submodule health |
| `./scripts/build-single-project.sh <project>` | Build single project docs |
| `./scripts/update-project-docs.sh <project> <version>` | Update project to version |
| `./scripts/add-new-project.sh <project> <repo-url>` | Add new project |
| `./scripts/deploy-release.sh <project> <version>` | Deploy tagged release |
| `./scripts/test-ci-locally.sh` | Simulate CI locally |
| `python -m scripts.generate-pdf` | Generate comprehensive PDF from website |

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

# Generate PDF
python -m scripts.generate-pdf

# Options
python -m scripts.generate-pdf --output custom-output.pdf
python -m scripts.generate-pdf --skip-screenshots  # Use cached screenshots
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
- [Submodules Guide](docs/SUBMODULES_GUIDE.md) - Daily operations
- [CI/CD Guide](docs/CI_CD_GUIDE.md) - Workflow configuration
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Production deployment steps
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions
