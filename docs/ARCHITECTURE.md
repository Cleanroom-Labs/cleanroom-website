# Nested Submodule Architecture

## Problem Statement

This project maintains multiple documentation sets with:
- Independent development timelines
- Documentation versioned with code
- Centralized documentation website
- Shared branding and styling

## Solution: Nested Submodules

A three-level nested submodule architecture:

1. **Website → Technical Docs** (single submodule)
2. **Technical Docs → Project Docs** (multiple submodules)
3. **Code Repo → Project Docs** (dual-homing, optional)

```
cleanroom-website/                    # Parent repository
├── cleanroom-technical-docs/         # Submodule (aggregates projects)
│   ├── <project>-docs/               # Submodules (project docs)
│   ├── shared/                       # Shared theme configuration
│   └── source/                       # Master documentation
└── scripts/                          # Helper scripts
```

For operational details, see [cleanroom-technical-docs/README.md](../cleanroom-technical-docs/README.md).

## Design Decisions

### Three-Level Nesting

**Benefits:**
- Explicit version coupling via git SHAs
- Separate review workflows
- Independent ownership per project
- Centralized aggregation
- Semantic versioning support

**Trade-offs:**
- 3 commits to propagate changes
- Requires submodule knowledge
- More complex than monorepo

### Shared Theme via Inheritance

Projects import shared configuration from `shared/theme_config.py`, allowing:
- Single source of truth for styling
- Easy global updates
- Project-specific overrides when needed

### Tag-Based Deployment

Releases use git tags:
- `v*` tags (e.g., `v1.0.0`) → Production deployment
- `v*-rc.*` tags (e.g., `v1.0.0-rc.1`) → Preview deployment

## Alternatives Considered

### Monorepo
- ❌ No version coupling between docs and code
- ❌ Less clear ownership
- ❌ Can't tag docs independently

### Separate Repos (No Submodules)
- ❌ No centralized aggregation
- ❌ Hard to ensure consistent theme
- ❌ No dual-homing capability

### Sparse Checkout
- ❌ Complex configuration
- ❌ Doesn't solve version coupling

## Future: Multi-Version Support

Planned structure for versioned documentation:

```
public/docs/
├── <project>/
│   ├── latest/     → symlink to current version
│   ├── 2.0.0/
│   └── 1.0.0/
```

Tool: `sphinx-multiversion` extension

## Submodules

The full nesting structure:

```
cleanroom-website/                                    # This repo
├── cleanroom-technical-docs/                         # Level 1 submodule
│   ├── cleanroom-whisper-docs/                       # Level 2 submodule
│   │   └── source/cleanroom-theme/                   # Level 3 submodule
│   ├── airgap-deploy-docs/                           # Level 2 submodule
│   │   └── source/cleanroom-theme/                   # Level 3 submodule
│   ├── airgap-transfer-docs/                         # Level 2 submodule
│   │   └── source/cleanroom-theme/                   # Level 3 submodule
│   └── source/cleanroom-theme/                       # Level 2 submodule
└── cleanroom-theme/                                  # Level 1 submodule
```

| Submodule | Purpose |
|-----------|---------|
| `cleanroom-technical-docs` | Aggregates all project documentation into a single Sphinx build. |
| `cleanroom-theme` | Shared theme and styling used by all documentation projects. |
| `cleanroom-whisper-docs` | Documentation for Cleanroom Whisper, an offline audio transcription application. |
| `airgap-deploy-docs` | Documentation for AirGap Deploy, a tool for preparing software deployments for air-gapped systems. |
| `airgap-transfer-docs` | Documentation for AirGap Transfer, a tool for transferring files to air-gapped systems. |

The `cleanroom-theme` submodule appears at multiple levels so that each project can build its documentation independently with consistent styling.

## References

- [Submodules Guide](./SUBMODULES_GUIDE.md) - Daily operations
- [Git Submodules Documentation](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
