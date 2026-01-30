# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Reference

See [README.md](README.md) for complete documentation including build commands, repository structure, and submodule workflows.

**Build docs:** `node scripts/build-docs.mjs`
**Build site only:** `npm run build:web`

**Check submodules:** `./scripts/check-submodules.py`

**Sync theme:** `./scripts/sync-theme.py`

**Check theme staleness:** `cd cleanroom-theme && npm run check-staleness`

**Generate PDF:** `python -m scripts.generate-pdf`

## Key Concepts

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the submodule structure, design rationale, and submodule descriptions.

- **Warnings policy**: Treat Sphinx warnings as failures, except intersphinx inventory fetch warnings which may appear when offline or before deployment
- **Local submodules**: All submodules point to local directories (e.g., `~/Projects/cleanroom-theme`), not GitHub. The main website repo has no remote.
- **Next.js build mode**: Use webpack (`--webpack`) for `dev`/`build` to avoid Turbopack panics in restricted environments.
- **Runtime requirement**: Next.js 16 requires Node.js 20.9+.
- **CI Node version**: GitHub Actions reads the Node version from `.nvmrc`.

## Important Files

| File | Purpose |
|------|---------|
| `scripts/build-docs.mjs` | Main build orchestrator |
| `scripts/sync-theme.py` | Propagate theme changes to all submodules |
| `scripts/push-submodules.py` | Propagate commits through nested submodules |
| `scripts/generate-pdf/` | PDF report generator for website content |
| `scripts/submodule_visualizer/` | Interactive visualization of submodule relationships |
| `cleanroom-technical-docs/source/conf.py` | Master Sphinx configuration |
| `cleanroom-technical-docs/CLAUDE.md` | Guidance for working with Sphinx docs |

## Detailed Documentation

| Guide | When to Read |
|-------|--------------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Understanding design decisions |
| [docs/SUBMODULES_GUIDE.md](docs/SUBMODULES_GUIDE.md) | Troubleshooting submodule issues |
| [docs/CI_CD_GUIDE.md](docs/CI_CD_GUIDE.md) | CI/CD configuration |
| [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) | Production deployment steps |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common issues and solutions |

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
