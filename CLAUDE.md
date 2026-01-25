# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Reference

See [README.md](README.md) for complete documentation including build commands, repository structure, and submodule workflows.

**Build docs:** `node scripts/build-docs.mjs`

**Check submodules:** `./scripts/check-submodules.sh`

**Sync theme:** `./scripts/sync-theme.sh`

## Key Concepts

- **Three-level nested submodules**: website → technical-docs → project-docs
- **Three-commit propagation**: Changes in project docs require commits in: submodule → technical-docs → website
- **Detached HEAD is normal**: Submodules point to specific commits, not branches. Use `git checkout main` to make changes.
- **Build fails on warnings**: Sphinx warnings indicate broken references and must be fixed

## Important Files

| File | Purpose |
|------|---------|
| `scripts/build-docs.mjs` | Main build orchestrator |
| `scripts/sync-theme.sh` | Propagate theme changes to all submodules |
| `cleanroom-technical-docs/source/conf.py` | Master Sphinx configuration |
| `cleanroom-technical-docs/CLAUDE.md` | Guidance for working with Sphinx docs |

## Detailed Documentation

| Guide | When to Read |
|-------|--------------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Understanding design decisions |
| [docs/SUBMODULES_GUIDE.md](docs/SUBMODULES_GUIDE.md) | Troubleshooting submodule issues |
| [docs/CI_CD_GUIDE.md](docs/CI_CD_GUIDE.md) | CI/CD configuration |

## Working in This Repo

When modifying documentation:
1. Run `./scripts/check-submodules.sh` to verify health
2. Make changes in the appropriate submodule (checkout a branch first)
3. Build with `node scripts/build-docs.mjs` to verify no warnings
4. Propagate commits through all three levels

When modifying build scripts:
1. Test locally with `./scripts/test-ci-locally.sh`
2. Check that `public/docs/` is generated correctly

When updating the theme:
1. Make changes in `/Users/andfranklin/Projects/cleanroom-theme`
2. Run `npm run build` to regenerate outputs
3. Commit and push changes in the standalone repo
4. Run `./scripts/sync-theme.sh` to propagate to all 5 submodule locations
5. Build with `node scripts/build-docs.mjs` to verify
6. Push changes in website (and any modified project repos)
