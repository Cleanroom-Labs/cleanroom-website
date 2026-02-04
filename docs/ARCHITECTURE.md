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
├── technical-docs/                   # Submodule (aggregates projects)
│   ├── <project>/                    # Submodules (project docs)
│   ├── common/                       # Submodule (shared theme & build tools)
│   └── source/                       # Master documentation
└── scripts/                          # Helper scripts
```

For operational details, see [technical-docs/README.md](../technical-docs/README.md).

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

Projects import shared configuration from `common/theme_config.py` (at each repo's root level), allowing:
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
├── technical-docs/                                   # Level 1 submodule
│   ├── whisper/                                      # Level 2 submodule
│   │   └── common/                                   # Level 3 submodule
│   ├── deploy/                                       # Level 2 submodule
│   │   └── common/                                   # Level 3 submodule
│   ├── transfer/                                     # Level 2 submodule
│   │   └── common/                                   # Level 3 submodule
│   └── common/                                       # Level 2 submodule
└── common/                                           # Level 1 submodule
```

| Submodule | Purpose |
|-----------|---------|
| `technical-docs` | Aggregates all project documentation into a single Sphinx build. |
| `common` | Shared theme, styling, and build tools used by all documentation projects. |
| `whisper` | Documentation for Cleanroom Whisper, an offline audio transcription application. |
| `deploy` | Documentation for AirGap Deploy, a tool for preparing software deployments for air-gapped systems. |
| `transfer` | Documentation for AirGap Transfer, a tool for transferring files to air-gapped systems. |

The `common` submodule appears at each repo's root level so that each project can build its documentation independently with consistent styling.

## References

- [Submodules Guide](./SUBMODULES_GUIDE.md) - Daily operations
- [Git Submodules Documentation](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
