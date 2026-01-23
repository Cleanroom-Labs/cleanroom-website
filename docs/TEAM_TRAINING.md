# Team Training: Nested Submodule Architecture

**Training Duration:** 30-45 minutes
**Prerequisites:** Git basics, command line familiarity
**Goal:** Team can confidently work with nested submodules

## Training Overview

This guide walks through the most common workflows you'll use when working with the nested submodule documentation architecture.

## Architecture Quick Reference

```
cleanroom-labs/                          # Parent repository
├── cleanroom-technical-docs/            # Level 1 submodule (aggregator)
│   ├── airgap-whisper-docs/             # Level 2 submodule (project)
│   ├── airgap-deploy-docs/              # Level 2 submodule (project)
│   └── airgap-transfer-docs/            # Level 2 submodule (project)
└── scripts/                             # Helper scripts
```

**Key concept:** Each submodule is an independent git repository with its own commits, branches, and tags.

## Part 1: Initial Setup (5 minutes)

### Clone the Repository

```bash
# Clone with all submodules
git clone --recurse-submodules git@github.com:cleanroom-labs/cleanroom-labs.git
cd cleanroom-labs

# Or if you already cloned without submodules:
git submodule update --init --recursive
```

### Verify Setup

```bash
# Check submodule health
./scripts/check-submodules.sh
```

**Expected output:**
```
Checking submodule health...

✓ technical-docs is on: main
✓ airgap-whisper-docs is on: main
✓ airgap-deploy-docs is on: main
✓ airgap-transfer-docs is on: main
```

**If you see "DETACHED HEAD":** Don't panic. This means the submodule is at a specific commit instead of a branch. This is normal for version pinning.

## Part 2: Common Workflows (20 minutes)

### Workflow 1: Updating Content in a Project (Most Common)

**Scenario:** You need to fix a typo in the AirGap Whisper documentation.

**Steps:**

```bash
# 1. Navigate to the project docs
cd cleanroom-technical-docs/airgap-whisper-docs

# 2. Make sure you're on main branch (not detached)
git checkout main
git pull origin main

# 3. Create a feature branch (optional but recommended)
git checkout -b fix/typo-in-readme

# 4. Make your changes
# ... edit source/readme.rst ...

# 5. Test the build
sphinx-build -M html source build
# Or use the helper script from the parent:
# cd ../..
# ./scripts/build-single-project.sh whisper

# 6. Commit your changes
git add source/readme.rst
git commit -m "Fix typo in whisper README"

# 7. Push to the project repository
git push origin fix/typo-in-readme
# Create PR on GitHub for the project repo

# 8. After PR is merged, update the parent repos
cd ..  # Back to cleanroom-technical-docs
git add airgap-whisper-docs
git commit -m "Update whisper docs: fix typo"
git push

cd ..  # Back to cleanroom-labs
git add cleanroom-technical-docs
git commit -m "Update technical docs (whisper typo fix)"
git push
```

**Key points:**
- Changes happen in the submodule
- Parent repos only track which commit of the submodule to use
- Must commit in **three places**: project → technical-docs → parent

### Workflow 2: Building Documentation Locally

**Scenario:** You want to preview documentation before pushing.

**Option A: Build all documentation**

```bash
# From cleanroom-labs root
./scripts/test-ci-locally.sh
```

This script:
- Verifies prerequisites
- Checks submodule health
- Builds all project docs
- Builds master docs
- Reports warnings

**Option B: Build single project**

```bash
#From cleanroom-labs root
./scripts/build-single-project.sh whisper

# Or manually:
cd cleanroom-technical-docs/airgap-whisper-docs
sphinx-build -M html source build
open build/html/index.html  # macOS
# xdg-open build/html/index.html  # Linux
```

**Option C: Build master docs only**

```bash
cd cleanroom-technical-docs
make html
open build/html/index.html
```

### Workflow 3: Checking Submodule Health

**Scenario:** CI is failing and you're not sure why.

```bash
# Check all submodules
./scripts/check-submodules.sh
```

**Common issues detected:**
- **Detached HEAD:** Submodule at specific commit, not branch
- **Uncommitted changes:** You have local edits not committed
- **Not initialized:** Submodule directory exists but empty

**Fix detached HEAD:**
```bash
cd cleanroom-technical-docs/airgap-whisper-docs
git checkout main
cd ../..
git add cleanroom-technical-docs
git commit -m "Update whisper docs submodule to main"
```

### Workflow 4: Updating a Project to a Specific Version

**Scenario:** You want to pin whisper docs to v1.0.0 release.

**Using helper script (recommended):**

```bash
./scripts/update-project-docs.sh whisper v1.0.0
git push
```

**Manual approach:**

```bash
cd cleanroom-technical-docs/airgap-whisper-docs
git fetch --tags
git checkout v1.0.0
cd ..
git add airgap-whisper-docs
git commit -m "Pin whisper docs to v1.0.0"
cd ..
git add cleanroom-technical-docs
git commit -m "Update technical docs (whisper v1.0.0)"
git push
```

### Workflow 5: Adding a New Project

**Scenario:** You're adding "AirGap Monitor" as a new project.

```bash
# 1. Create the project docs repository (on GitHub or locally)
cd ~/Projects
mkdir airgap-monitor-docs
cd airgap-monitor-docs
git init
# ... create Sphinx structure (copy from whisper-docs as template) ...
git add .
git commit -m "Initial commit"
git push origin main

# 2. Add as submodule
cd ~/Projects/cleanroom-labs
./scripts/add-new-project.sh monitor git@github.com:cleanroom-labs/airgap-monitor-docs.git

# 3. Update master docs to reference new project
cd cleanroom-technical-docs/source
# ... edit index.rst to add monitor ...
git add index.rst
git commit -m "Add monitor project to master docs"
git push

# 4. Configure intersphinx
cd ..
# ... edit source/conf.py to add monitor to intersphinx_mapping ...
git add source/conf.py
git commit -m "Add monitor to intersphinx"
git push

# 5. Update parent
cd ..
git add cleanroom-technical-docs
git commit -m "Add monitor project"
git push
```

### Workflow 6: Creating a Release

**Scenario:** You're ready to release whisper docs v1.0.0.

```bash
# 1. Tag the project docs
cd cleanroom-technical-docs/airgap-whisper-docs
git tag v1.0.0
git push origin v1.0.0

# 2. Update technical-docs to use tagged version
cd ..
git add airgap-whisper-docs
git commit -m "Release whisper docs v1.0.0"
git push

# 3. Tag technical-docs (optional)
git tag v1.0.0
git push origin v1.0.0

# This triggers deploy-tagged.yml workflow → GitHub Pages deployment
```

**For release candidates:**
```bash
# Same process, but use -rc suffix
git tag v1.0.0-rc.1
git push origin v1.0.0-rc.1
# This deploys to preview environment instead of production
```

## Part 3: Understanding Submodule States (10 minutes)

### What is Detached HEAD?

When you see "detached HEAD", it means the submodule is pointing to a specific commit rather than a branch.

**This is NORMAL when:**
- Pinning to a release version (e.g., v1.0.0)
- Parent repo references a specific commit for stability

**This is PROBLEMATIC when:**
- You're actively developing and need to push changes
- CI expects you to be on a branch

**Fix it:**
```bash
cd <submodule-directory>
git checkout main  # Or whatever branch you want
cd ..
git add <submodule-directory>
git commit -m "Update submodule to main branch"
```

### Submodule Updates

**When you `git pull` in the parent repo:**
- Parent repo updates
- Submodule references update
- **But submodule contents don't auto-update!**

**To update submodules after pull:**
```bash
git pull
git submodule update --recursive
```

**Or in one command:**
```bash
git pull --recurse-submodules
```

### Making Changes in Submodules

**Rule:** Always commit changes in the submodule FIRST, then update parent.

**Wrong order:**
```bash
# DON'T DO THIS
cd cleanroom-technical-docs
git add airgap-whisper-docs  # Trying to add uncommitted changes
git commit  # This will fail or create inconsistent state
```

**Correct order:**
```bash
# DO THIS
cd cleanroom-technical-docs/airgap-whisper-docs
git add .
git commit -m "Changes"
git push
cd ..
git add airgap-whisper-docs  # Now update parent reference
git commit -m "Update whisper docs"
git push
```

## Part 4: CI/CD Integration (5 minutes)

### How CI Works

**When you push to cleanroom-technical-docs main:**
1. `sphinx-docs.yml` workflow triggers
2. Checks out repo with recursive submodules
3. Builds each project individually
4. Builds master docs with intersphinx
5. Verifies cross-references
6. Deploys to GitHub Pages

**When you push a git tag (v*, v*-rc.*):**
1. `deploy-tagged.yml` workflow triggers
2. Determines environment (production vs preview)
3. Builds all documentation
4. Adds version badge
5. Deploys to appropriate environment

**When you push to cleanroom-labs main:**
1. `verify-submodules.yml` checks submodule health
2. `build-all-docs.yml` builds everything (if submodules changed)
3. Does NOT deploy (only technical-docs repo deploys)

### Testing CI Locally

**Before pushing, always test:**
```bash
./scripts/test-ci-locally.sh
```

**If this fails, CI will fail.**

**Common CI failures:**
- Build warnings (master must have 0 warnings)
- Submodule not initialized
- Broken cross-references

## Part 5: Quick Reference (5 minutes)

### Daily Commands

```bash
# Start your day
cd cleanroom-labs
git pull --recurse-submodules
./scripts/check-submodules.sh

# Make changes (in appropriate submodule)
cd cleanroom-technical-docs/airgap-whisper-docs
git checkout main
# ... edit files ...
git add .
git commit -m "Description"
git push

# Update parents
cd ..
git add airgap-whisper-docs
git commit -m "Update whisper docs"
git push

cd ..
git add cleanroom-technical-docs
git commit -m "Update technical docs"
git push

# Test before push
./scripts/test-ci-locally.sh
```

### When Things Go Wrong

**"Submodule not initialized":**
```bash
git submodule update --init --recursive
```

**"Detached HEAD" (and you want to be on main):**
```bash
cd <submodule>
git checkout main
cd ..
git add <submodule>
git commit -m "Update submodule to main"
```

**"Build failing with warnings":**
```bash
./scripts/test-ci-locally.sh  # See warnings locally
cd cleanroom-technical-docs
make html 2>&1 | grep -i warning  # Find specific warnings
```

**"Uncommitted changes in submodule":**
```bash
cd <submodule>
git status  # See what changed
git add <files>
git commit -m "Description"
git push
cd ..
git add <submodule>
git commit -m "Update submodule"
```

**"CI failing but local works":**
```bash
# Check for case-sensitive filename issues (macOS vs Linux)
# Check that requirements.txt is complete
# Check that Graphviz is installed in CI (it is in our workflows)
```

## Part 6: Practice Exercise (Optional, 10 minutes)

**Exercise:** Make a change to whisper docs and get it deployed.

1. Clone the repository (if you haven't)
2. Navigate to `cleanroom-technical-docs/airgap-whisper-docs`
3. Checkout main branch
4. Edit `source/readme.rst` (add your name to acknowledgements)
5. Build locally to verify: `sphinx-build -M html source build`
6. Commit and push to whisper-docs
7. Update technical-docs submodule reference
8. Update parent repository reference
9. Run `./scripts/test-ci-locally.sh` to verify
10. Push all changes

**Success criteria:** All three repositories updated, build passes with 0 warnings.

## Resources

- **Submodule operations:** `docs/SUBMODULES_GUIDE.md`
- **Architecture decisions:** `docs/ARCHITECTURE.md`
- **CI/CD workflows:** `docs/CI_CD_GUIDE.md`
- **Implementation status:** `docs/IMPLEMENTATION_COMPLETE.md`
- **Deployment guide:** `docs/DEPLOYMENT_GUIDE.md`

## Getting Help

**Before asking for help:**
1. Run `./scripts/check-submodules.sh` - often shows the problem
2. Run `./scripts/test-ci-locally.sh` - reproduces CI failures
3. Check workflow logs in GitHub Actions tab
4. Search this document for error message

**Common questions answered:**
- **"Why three commits?"** - Each repo is independent; must update each
- **"Why detached HEAD?"** - For version pinning stability
- **"Can I work directly in technical-docs/source?"** - Yes! That's the master docs, not a submodule
- **"Do I need to know Python/Sphinx?"** - No, helper scripts handle builds
- **"What if I break something?"** - Git makes it hard to lose data; just ask for help

## Conclusion

**Key takeaways:**
1. Submodules are independent git repositories
2. Always commit in submodule first, then update parent
3. Use helper scripts to simplify common tasks
4. Test locally with `./scripts/test-ci-locally.sh` before pushing
5. `./scripts/check-submodules.sh` is your friend

**You're ready when:**
- ✅ You can make a change and update all three levels
- ✅ You can build documentation locally
- ✅ You understand when detached HEAD is normal
- ✅ You know how to run the verification scripts

**Practice makes perfect.** Don't worry about making mistakes—git makes it easy to recover.

---

**Training complete! Questions? Review the resources above or ask the team.**
