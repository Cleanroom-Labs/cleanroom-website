# Git Submodules Guide

## Overview

This repository uses a three-level nested submodule architecture for documentation management.

## Architecture

```
cleanroom-website/                # Level 1
└── cleanroom-technical-docs/     # Level 2 (submodule)
    ├── project-1-docs/           # Level 3 (submodule)
    ├── project-2-docs/           # Level 3 (submodule)
    └── project-3-docs/           # Level 3 (submodule)
```

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
   cd cleanroom-technical-docs/<project>-docs
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
   git add <project>-docs
   git commit -m "Update reference"
   git push
   
   cd ..
   git add cleanroom-technical-docs
   git commit -m "Update reference"
   git push
   ```

### Release Workflow

1. Tag documentation:
   ```bash
   cd cleanroom-technical-docs/<project>-docs
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. Update website to use the release:
   ```bash
   cd /path/to/cleanroom-website
   ./scripts/deploy-release.sh <project> v1.0.0
   ```

## Troubleshooting

### Detached HEAD State

This is normal for submodules pointing to specific commits. To work on docs:

```bash
cd cleanroom-technical-docs/<project>-docs
git checkout main
```

### Changes Not Showing

Update submodules:
```bash
git submodule update --recursive --remote
```

### Can't Push Changes

Make sure you're on a branch:
```bash
git checkout main
```

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

