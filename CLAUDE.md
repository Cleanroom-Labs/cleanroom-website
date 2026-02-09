# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Reference

See [README.md](README.md) for complete documentation including build commands, repository structure, and submodule workflows.

**Build docs:** `node scripts/build-docs.mjs` (add `--version <ver>` to build a specific version)
**Build site only:** `npm run build:web`

**Check submodules:** `grove check`

**Sync common:** `grove sync`

**Check theme staleness:** `cd common && npm run check-staleness`

**Generate PDF:** `python -m scripts.generate-pdf` (add `--draft` for watermark)

## Key Concepts

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the submodule structure, design rationale, and submodule descriptions.

- **Doc versioning**: Docs are versioned monolithically — one tag on `technical-docs` versions all projects together. The `DOCS_VERSION` env var controls the version (defaults to `dev`).
- **Warnings policy**: Treat Sphinx warnings as failures, except intersphinx inventory fetch warnings which may appear when offline or before deployment
- **Submodule URLs**: Submodules point to GitHub (e.g., `git@github.com:Cleanroom-Labs/cleanroom-website-common.git`).
- **Next.js build mode**: Use webpack (`--webpack`) for `dev`/`build` to avoid Turbopack panics in restricted environments.
- **Runtime requirement**: Next.js 16 requires Node.js 20.9+.
- **CI Node version**: GitHub Actions reads the Node version from `.nvmrc`.

## Important Files

| File | Purpose |
|------|---------|
| `scripts/build-docs.mjs` | Main build orchestrator |
| `grove/` | Git submodule management CLI (`grove check/push/sync/visualize`) |
| `scripts/generate-pdf/` | PDF report generator for website content |
| `technical-docs/source/conf.py` | Master Sphinx configuration |
| `technical-docs/scripts/update-versions-json.sh` | Update versions.json manifest for multi-version docs |
| `common/theme_config.py` | Shared Sphinx config, version helpers, banner setup |
| `technical-docs/CLAUDE.md` | Guidance for working with Sphinx docs |

## Detailed Documentation

| Guide | When to Read |
|-------|--------------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Understanding design decisions |
| [docs/SUBMODULES_GUIDE.md](docs/SUBMODULES_GUIDE.md) | Troubleshooting submodule issues |
| [docs/CI_CD_GUIDE.md](docs/CI_CD_GUIDE.md) | CI/CD configuration |
| [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) | Production deployment steps |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common issues and solutions |
| [docs/STYLE_GUIDE.md](docs/STYLE_GUIDE.md) | Writing style and terminology conventions |
| [docs/VERSIONING_GUIDE.md](docs/VERSIONING_GUIDE.md) | Versioning, branching, and multi-version hosting |

## NPM Scripts

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start development server (webpack) |
| `npm run dev:clean` | Build docs then start dev server (webpack) |
| `npm run build` | Production build (webpack; builds docs first) |
| `npm run build:web` | Production build (webpack; skips docs) |
| `npm run build-docs` | Build Sphinx documentation only |
| `npm run lint` | Print lint setup guidance (linting not configured yet) |

If you need to run Next directly, prefer:

```bash
./node_modules/.bin/next dev --webpack
./node_modules/.bin/next build --webpack
```

See [README.md](README.md) for workflows and [docs/](docs/) for detailed guides.
