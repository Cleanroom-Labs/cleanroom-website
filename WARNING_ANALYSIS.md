# Build Warning Analysis

## Summary

Total Warnings: 44  
Categories: 3 main types  
Root Cause: Path references to content that moved to submodules

## Warning Categories

### Category 1: Toctree Submodule References (3 warnings)

**Location:** `source/index.rst:18`

**Warnings:**
```
WARNING: toctree contains reference to nonexisting document 'airgap-whisper-docs/source/index'
WARNING: toctree contains reference to nonexisting document 'airgap-deploy-docs/source/index'
WARNING: toctree contains reference to nonexisting document 'airgap-transfer-docs/source/index'
```

**Root Cause:**  
Sphinx toctree cannot directly include documents from Git submodules. The paths `airgap-whisper-docs/source/index` don't exist in the main Sphinx build's source tree.

**Impact:** Medium - Main table of contents doesn't link to project docs

**Suggested Fix:**
Remove submodule references from main toctree. Instead:

**Option A:** Use external links
```rst
.. toctree::
   :maxdepth: 2
   :caption: Projects

   AirGap Whisper <https://cleanroomlabs.dev/docs/airgap-whisper/>
   AirGap Deploy <https://cleanroomlabs.dev/docs/airgap-deploy/>
   AirGap Transfer <https://cleanroomlabs.dev/docs/airgap-transfer/>
```

**Option B:** Create stub pages
```rst
.. toctree::
   :maxdepth: 2
   :caption: Projects

   projects/whisper
   projects/deploy
   projects/transfer
```

Then create `source/projects/whisper.rst`:
```rst
AirGap Whisper
==============

View the full documentation at: https://cleanroomlabs.dev/docs/airgap-whisper/

Or browse locally at: `/airgap-whisper/index.html`
```

### Category 2: Cross-References to Moved Content (38 warnings)

**Pattern:** References to `/airgap-whisper/`, `/airgap-deploy/`, `/airgap-transfer/` paths

**Affected Files:**
- `source/index.rst` (3 warnings)
- `source/meta/release-roadmap.rst` (6 warnings)
- `source/meta/requirements-overview.rst` (3 warnings)
- `source/meta/meta-architecture.rst` (6 warnings)
- `source/meta/rust-integration-guide.rst` (3 warnings)
- `source/blog/*.rst` (17 warnings)

**Example Warnings:**
```
source/index.rst:42: WARNING: unknown document: '../airgap-whisper-docs/source/requirements/srs'
source/meta/release-roadmap.rst:28: WARNING: unknown document: '/airgap-whisper/roadmap'
source/blog/introducing-airgap-suite.rst:63: WARNING: unknown document: '/airgap-whisper/readme'
```

**Root Cause:**  
Content moved from `source/airgap-whisper/` to `airgap-whisper-docs/source/`. References using old paths no longer resolve.

**Impact:** High - Broken internal documentation links

**Suggested Fixes:**

**Option 1: Update to submodule paths** (if building with submodules in source tree)
```rst
# Before:
:doc:`/airgap-whisper/readme`

# After:
:doc:`/airgap-whisper-docs/source/readme`
```

**Option 2: Use external links** (recommended for separate builds)
```rst
# Before:
:doc:`/airgap-whisper/readme`

# After:
`AirGap Whisper README <https://cleanroomlabs.dev/docs/airgap-whisper/readme.html>`_
```

**Option 3: Configure intersphinx** (best for cross-project references)
```python
# In source/conf.py
intersphinx_mapping = {
    'airgap-whisper': ('https://cleanroomlabs.dev/docs/airgap-whisper/', None),
    'airgap-deploy': ('https://cleanroomlabs.dev/docs/airgap-deploy/', None),
    'airgap-transfer': ('https://cleanroomlabs.dev/docs/airgap-transfer/', None),
}
```

Then use:
```rst
:doc:`airgap-whisper:readme`
:doc:`airgap-deploy:requirements/srs`
```

### Category 3: Undefined Labels (6 warnings)

**Pattern:** Labels that existed in old project docs

**Example:**
```
source/meta/meta-architecture.rst:557: WARNING: undefined label: 'airgap-whisper-readme-competition'
```

**Root Cause:**  
Labels like `airgap-whisper-readme-competition` were defined in the old `source/airgap-whisper/readme.rst`, which is now in a submodule.

**Impact:** Medium - Reference links don't work

**Suggested Fix:**

Either remove the label references or recreate them in meta docs:
```rst
# Before (broken):
:ref:`airgap-whisper-readme-competition`

# After (external link):
`AirGap Whisper Competition <https://cleanroomlabs.dev/docs/airgap-whisper/readme.html#competition>`_
```

## Detailed Fix Recommendations

### Quick Win: Update source/index.rst

```rst
# Change toctree from:
.. toctree::
   :maxdepth: 2
   :caption: Projects

   ../airgap-whisper-docs/source/index
   ../airgap-deploy-docs/source/index
   ../airgap-transfer-docs/source/index

# To:
.. toctree::
   :maxdepth: 2
   :caption: Projects

   projects/whisper
   projects/deploy
   projects/transfer
```

Create stub files in `source/projects/`:
- `whisper.rst` - Links to whisper docs
- `deploy.rst` - Links to deploy docs
- `transfer.rst` - Links to transfer docs

### Medium Effort: Configure Intersphinx

Add to `source/conf.py`:
```python
intersphinx_mapping = {
    'airgap-whisper': ('../airgap-whisper-docs/build/html/', None),
    'airgap-deploy': ('../airgap-deploy-docs/build/html/', None),
    'airgap-transfer': ('../airgap-transfer-docs/build/html/', None),
}
```

Then update meta docs to use intersphinx:
```python
# Script to update references
sed -i 's/:doc:`\/airgap-whisper\/\(.*\)`/:doc:`airgap-whisper:\1`/g' source/meta/*.rst
sed -i 's/:doc:`\/airgap-deploy\/\(.*\)`/:doc:`airgap-deploy:\1`/g' source/meta/*.rst
sed -i 's/:doc:`\/airgap-transfer\/\(.*\)`/:doc:`airgap-transfer:\1`/g' source/meta/*.rst
```

### High Effort: Restructure Documentation

**Option A: Keep meta docs, use external links**
- Update all meta docs and blog posts to use external links
- Simple, works immediately
- Breaks if URLs change

**Option B: Move meta docs to each project**
- Duplicate principles.rst in each project
- Each project is self-contained
- Harder to maintain consistency

**Option C: Build projects first, then reference**
- Build all project docs first
- Use intersphinx with local paths
- Requires coordinated build order
- Best for production

## Recommended Approach

### Phase 1: Immediate (Eliminate all warnings)

1. **Update source/index.rst** - Use stub pages instead of submodule refs
2. **Configure intersphinx** - Set up cross-project references  
3. **Update meta docs** - Change :doc: to intersphinx format
4. **Remove broken label refs** - Replace with external links

### Phase 2: Long-term (Architecture decision)

Decide on documentation architecture:

**Option A: Centralized meta (current)**
- Keep meta docs in cleanroom-technical-docs
- Projects reference meta via intersphinx
- Good for: Consistent principles across projects

**Option B: Distributed meta**
- Duplicate meta docs in each project
- Each project is standalone
- Good for: Independent project development

**Option C: Hybrid**
- High-level meta stays centralized
- Project-specific details in projects
- Good for: Balance of both approaches

## Impact Assessment

| Fix | Warnings Resolved | Effort | Risk |
|-----|------------------|--------|------|
| Update index.rst toctree | 3 | Low | Low |
| Configure intersphinx | 38 | Medium | Low |
| Remove label refs | 6 | Low | Low |
| **Total** | **47** | **Medium** | **Low** |

## Files Requiring Updates

### High Priority
- `source/index.rst` - Update toctree (3 warnings)
- `source/conf.py` - Add intersphinx config

### Medium Priority
- `source/meta/release-roadmap.rst` (6 warnings)
- `source/meta/meta-architecture.rst` (6 warnings)
- `source/meta/requirements-overview.rst` (3 warnings)
- `source/meta/rust-integration-guide.rst` (3 warnings)

### Low Priority (Blog posts)
- `source/blog/introducing-airgap-suite.rst` (9 warnings)
- `source/blog/demo-whisper-quick-capture.rst` (3 warnings)
- `source/blog/demo-transfer-ollama.rst` (4 warnings)
- `source/blog/demo-deploy-rust-app.rst` (3 warnings)

## Next Steps

1. Review and approve fix approach
2. Implement intersphinx configuration
3. Update index.rst
4. Update meta docs with find/replace
5. Test build - verify 0 warnings
6. Update project docs if needed
7. Document the new reference patterns

