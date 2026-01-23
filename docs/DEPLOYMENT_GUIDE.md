# Production Deployment Guide

This guide covers deploying the documentation to GitHub Pages.

## Prerequisites

- All builds passing locally (`./scripts/test-ci-locally.sh`)
- Submodules in healthy state (`./scripts/check-submodules.sh`)
- All changes committed and pushed

## Deployment Overview

```
GitHub Organization
├── cleanroom-website           # Parent repository
├── cleanroom-technical-docs    # Documentation aggregator
└── <project>-docs              # Individual project docs (multiple)
```

## Step 1: Create GitHub Repositories

Create repositories for each component. Do not initialize them (we're pushing existing code).

## Step 2: Push Repositories

### Push project documentation repositories first

```bash
cd <project>-docs
git remote add origin git@github.com:<org>/<project>-docs.git
git push -u origin main
git push --tags
```

### Update and push cleanroom-technical-docs

```bash
cd cleanroom-technical-docs

# Update .gitmodules to use GitHub URLs
# [submodule "<project>-docs"]
#     path = <project>-docs
#     url = git@github.com:<org>/<project>-docs.git

git submodule sync --recursive
git add .gitmodules
git commit -m "Update submodule URLs to GitHub"
git remote add origin git@github.com:<org>/cleanroom-technical-docs.git
git push -u origin main
```

### Update and push cleanroom-website

```bash
cd cleanroom-website

# Update .gitmodules for technical-docs
git submodule sync --recursive
git add .gitmodules
git commit -m "Update technical-docs submodule URL"
git remote add origin git@github.com:<org>/cleanroom-website.git
git push -u origin main
```

## Step 3: Configure GitHub Pages

1. Navigate to `cleanroom-technical-docs` repository settings
2. Go to **Settings → Pages**
3. Set **Source** to "GitHub Actions"
4. Under **Settings → Actions → General**, set workflow permissions to "Read and write"

## Step 4: Trigger First Deployment

```bash
cd cleanroom-technical-docs
git commit --allow-empty -m "Trigger initial deployment"
git push
```

Monitor the build in the Actions tab. Documentation will be available at:
```
https://<org>.github.io/cleanroom-technical-docs/
```

## Deploying Updates

### Content updates

```bash
# Make changes in project docs
cd cleanroom-technical-docs/<project>-docs
git checkout main
# ... edit files ...
git add . && git commit -m "Update" && git push

# Update parent references
cd .. && git add <project>-docs && git commit -m "Update docs" && git push
```

### Tagged releases

```bash
# Tag project docs
cd cleanroom-technical-docs/<project>-docs
git tag v1.0.0 && git push origin v1.0.0

# Tag technical-docs
cd ..
git add <project>-docs
git commit -m "Release v1.0.0"
git tag v1.0.0 && git push origin main && git push origin v1.0.0
```

## Rollback

```bash
# Revert last deployment
cd cleanroom-technical-docs
git revert HEAD
git push

# Or rollback to specific version
git reset --hard <commit-sha>
git push --force origin main
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Submodule not initialized" | Add `submodules: recursive` to checkout action |
| "Resource not accessible" | Enable workflow write permissions in settings |
| Old content showing | Hard refresh browser, wait for CDN cache |
| Cross-references broken | Verify intersphinx uses relative paths |

## Custom Domain (Optional)

1. Add CNAME record: `docs.example.com → <org>.github.io`
2. In repository Settings → Pages, set custom domain
3. Enable "Enforce HTTPS"
