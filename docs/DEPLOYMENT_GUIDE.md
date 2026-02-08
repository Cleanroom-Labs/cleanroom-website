# Production Deployment Guide

This guide covers deploying the documentation to GitHub Pages.

## Prerequisites

- All builds passing locally (`./scripts/test-ci-locally.sh`)
- Submodules in healthy state (`repo-tools check`)
- All changes committed and pushed

## Deployment Overview

Documentation is deployed to GitHub Pages via the `gh-pages` branch in the `technical-docs` repository. Two workflows handle deployment:

- **`sphinx-docs.yml`** — Builds on every push to main; deploys dev docs to `gh-pages/dev/`
- **`deploy-tagged.yml`** — Builds versioned docs from tags; deploys to `gh-pages/<version>/`

Versions accumulate on the `gh-pages` branch — each deployment adds a new directory without removing existing versions.

```
GitHub Organization
├── cleanroom-website           # Parent repository
├── technical-docs              # Documentation aggregator
└── <project>                   # Individual project docs (multiple)
```

## Step 1: Create GitHub Repositories

Create repositories for each component. Do not initialize them (we're pushing existing code).

## Step 2: Push Repositories

### Push project documentation repositories first

```bash
cd <project>
git remote add origin git@github.com:<org>/<project>.git
git push -u origin main
git push --tags
```

### Update and push technical-docs

```bash
cd technical-docs

# Update .gitmodules to use GitHub URLs
# [submodule "<project>"]
#     path = <project>
#     url = git@github.com:<org>/<project>.git

git submodule sync --recursive
git add .gitmodules
git commit -m "Update submodule URLs to GitHub"
git remote add origin git@github.com:<org>/technical-docs.git
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

1. Navigate to `technical-docs` repository settings
2. Go to **Settings → Pages**
3. Set **Source** to "GitHub Actions"
4. Under **Settings → Actions → General**, set workflow permissions to "Read and write"

## Step 4: Trigger First Deployment

```bash
cd technical-docs
git commit --allow-empty -m "Trigger initial deployment"
git push
```

Monitor the build in the Actions tab. Documentation will be available at:
```
https://<org>.github.io/technical-docs/
```

## Deploying Updates

### Content updates

```bash
# Make changes in project docs
cd technical-docs/<project>
git checkout main
# ... edit files ...
git add . && git commit -m "Update" && git push

# Update parent references
cd .. && git add <project> && git commit -m "Update docs" && git push
```

### Tagged releases

```bash
cd technical-docs

# Release candidate
git tag v1.0.0-rc.1
git push origin v1.0.0-rc.1
# → Deploys to gh-pages/1.0.0-rc.1/ with RC banner

# Stable release
git tag v1.0.0
git push origin v1.0.0
# → Deploys to gh-pages/1.0.0/, updates latest symlink
```

After tagging, the `deploy-tagged.yml` workflow:
1. Builds docs with `DOCS_VERSION` set from the tag
2. Adds the version to `gh-pages/<version>/`
3. Updates `versions.json` manifest
4. Updates `latest` symlink (stable releases only)
5. Deploys via GitHub Pages

### Version management

The `gh-pages` branch accumulates all versions:

```
gh-pages/
├── dev/              → Rebuilt on every push to main
├── 1.0.0/            → Stable release
├── 1.0.0-rc.1/       → Release candidate
├── latest -> 1.0.0   → Symlink to newest stable
└── versions.json     → Version manifest
```

To manually update `versions.json`:
```bash
./scripts/update-versions-json.sh \
  --version "1.0.0" \
  --url "/docs/1.0.0/" \
  --stable \
  --file gh-pages/versions.json
```

## Rollback

```bash
# Preferred: revert the last deployment commit
cd technical-docs
git revert HEAD
git push

# Last resort: reset + force-push (coordinate first; rewrites history)
# git reset --hard <commit-sha>
# git push --force-with-lease origin main
```

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for deployment troubleshooting.

## Custom Domain (Optional)

1. Add CNAME record: `docs.example.com → <org>.github.io`
2. In repository Settings → Pages, set custom domain
3. Enable "Enforce HTTPS"
