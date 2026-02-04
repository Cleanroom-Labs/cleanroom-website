# Git Submodules Guide

## Overview

This repository uses a three-level nested submodule architecture for documentation management.

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full submodule nesting
structure and design rationale.

In short: `cleanroom-website` → `technical-docs` → project submodules
(`whisper`, `deploy`, `transfer`), each with their own `common` submodule.

## Quick Reference

### Initial Setup
```bash
# Clone with all submodules
git clone --recursive <repo-url>

# Or initialize after cloning
git submodule update --init --recursive
```

### Update All Submodules
```bash
git pull --recurse-submodules
# or
git submodule update --recursive --remote
```

### Check Status
```bash
./scripts/check-submodules.py
```

### Update a Project
```bash
./scripts/update-project-docs.sh <project> <version>
```

### Add New Project
```bash
./scripts/add-new-project.sh <project> <repo-url>
```

## Working with Submodules

### Making Changes

1. Navigate to submodule:
   ```bash
   cd technical-docs/<project>
   ```

2. Checkout a branch (not detached HEAD):
   ```bash
   git checkout main
   ```

3. Make changes and commit:
   ```bash
   git add .
   git commit -m "Update docs"
   git push
   ```

4. Update parent repositories (requires 3 commits):
   ```bash
   cd ..
   git add <project>
   git commit -m "Update reference"
   git push
   
   cd ..
   git add technical-docs
   git commit -m "Update reference"
   git push
   ```

### Release Workflow

1. Tag documentation:
   ```bash
   cd technical-docs/<project>
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. Update website to use the release:
   ```bash
   cd /path/to/cleanroom-website
   ./scripts/deploy-release.sh <project> v1.0.0
   ```

For troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md#submodule-issues).

## Best Practices

1. Use helper scripts for multi-level updates
2. Run `./scripts/check-submodules.py` before committing
3. Use semantic versioning for documentation releases
4. Keep docs and code versions synchronized
5. Test builds locally before pushing

## Helper Scripts

| Script | Purpose |
|--------|---------|
| `check-submodules.py` | Verify submodule health |
| `update-project-docs.sh` | Update project to specific version |
| `add-new-project.sh` | Add new project documentation |
| `build-single-project.sh` | Build project docs locally |
| `deploy-release.sh` | Deploy documentation release |

