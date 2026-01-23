# Nested Submodule Architecture

## Problem Statement

Cleanroom Labs maintains 3+ AirGap projects with:
- Independent development timelines
- Documentation versioned with code
- Centralized documentation website
- Shared branding and styling
- Waterfall workflow (docs-first)

## Solution: Nested Submodules

### Structure

```
cleanroom-website/                    # Next.js website
├── cleanroom-technical-docs/         # Submodule (aggregates projects)
│   ├── shared/                       # Shared theme configuration
│   │   ├── theme-config.py          # Common Sphinx settings
│   │   └── extensions.txt           # Shared dependencies
│   ├── source/
│   │   ├── index.rst                # Master landing page
│   │   ├── conf.py                  # Master config
│   │   └── _static/
│   │       └── custom.css           # Shared styling
│   ├── project-1-docs/              # Submodule
│   ├── project-2-docs/              # Submodule  
│   └── project-3-docs/              # Submodule
└── scripts/                          # Helper scripts
```

Each code repository also includes its docs as a submodule:

```
airgap-project-1/                     # Code repository
├── docs/ → airgap-project-1-docs/    # Same repo as in technical-docs
├── src/
└── tests/
```

## Key Design Decisions

### 1. Three-Level Nesting

**Levels:**
1. Website → Technical Docs (single submodule)
2. Technical Docs → Project Docs (multiple submodules)
3. Code Repo → Project Docs (dual-homing)

**Benefits:**
- Explicit version coupling (git SHAs)
- Separate review workflows
- Independent ownership
- Centralized aggregation
- Semantic versioning support

**Trade-offs:**
- 3 commits to propagate changes
- Requires submodule knowledge
- More complex than monorepo

### 2. Shared Theme via Inheritance

Projects import shared configuration:

```python
# project-1-docs/source/conf.py
import sys, os
sys.path.insert(0, os.path.abspath('../../shared'))
from theme_config import *  # Import shared settings

# Project-specific overrides
project = 'AirGap Project 1'
version = '1.0.0'
```

**Location:** `cleanroom-technical-docs/shared/theme-config.py`

### 3. Tag-Based Deployment

**Release Process:**
1. Tag docs: `git tag v1.0.0 && git push origin v1.0.0`
2. Tag code: `git tag v1.0.0 && git push origin v1.0.0`
3. Update website: `./scripts/deploy-release.sh project-1 v1.0.0`

### 4. Cross-Project References

Using Sphinx intersphinx:

```python
intersphinx_mapping = {
    'project2': ('https://cleanroomlabs.dev/docs/project-2/', None),
}
```

```rst
See :doc:`project2:installation` for details.
```

## Alternatives Considered

### Monorepo
❌ No version coupling between docs and code
❌ Less clear ownership
❌ Can't tag docs independently

### Separate Repos (No Submodules)
❌ No centralized aggregation
❌ Hard to ensure consistent theme
❌ No dual-homing

### Sparse Checkout
❌ Complex configuration
❌ Doesn't solve version coupling

## Implementation Status

### Completed
- ✅ Infrastructure setup
- ✅ Shared theme configuration
- ✅ Helper scripts
- ✅ Documentation

### Remaining
- Migration of 3 projects
- CI/CD configuration
- Team training
- Production deployment

## Multi-Version Support (Future)

```
public/docs/
├── project-1/
│   ├── latest/     → symlink to 2.0.0/
│   ├── 2.0.0/
│   ├── 1.1.0/
│   └── 1.0.0/
```

Implementation phases:
1. MVP: Single version per project (current)
2. Add version switcher dropdown
3. Build multiple versions in parallel
4. Add RC preview URLs

Tool: `sphinx-multiversion` extension

## Maintenance

### Adding New Project
1. Create docs repository
2. Set up conf.py with shared theme import
3. Run `./scripts/add-new-project.sh <project> <repo-url>`
4. Update master index.rst
5. Configure intersphinx

### Updating Shared Theme
1. Edit `cleanroom-technical-docs/shared/theme-config.py`
2. Test with one project
3. Roll out to others
4. Verify builds

## References

- [Submodules Guide](./SUBMODULES_GUIDE.md)
- [Migration Plan](../migration-plan.md)
- [Git Submodules Docs](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
