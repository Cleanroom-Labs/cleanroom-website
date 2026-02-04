# CI/CD Guide for AirGap Documentation

This guide explains the CI/CD infrastructure for building and deploying the nested submodule documentation architecture.

## Overview

The CI/CD system consists of **three workflows** that handle different aspects of the build and deployment process:

### 1. Build, Verify, and Deploy Dev (Main Branch)
**File:** `technical-docs/.github/workflows/sphinx-docs.yml`

**Triggers:**
- Push to `main` branch (when docs or submodules change)
- Pull requests to `main`
- Manual workflow dispatch

**What it does:**
1. Checks out repository with all nested submodules
2. Verifies submodule initialization
3. Builds documentation with `DOCS_VERSION=dev` via `make html`
4. Checks for warnings via `make html-check`
5. Verifies project docs are present in build output
6. Verifies cross-references are working
7. Uploads build artifact
8. **On push to main only:** Deploys to `gh-pages` branch under `dev/` directory

**Key features:**
- Full submodule support with `submodules: recursive`
- Individual project builds before master build (enables intersphinx)
- Centralized warning detection via `make html-check` (matches local build behavior)
- Cross-reference verification
- Python 3.14, Graphviz for diagram generation
- Automatic dev deployment on every push to main (not PRs)

### 2. Deploy Tagged Release (Versioned)
**File:** `technical-docs/.github/workflows/deploy-tagged.yml`

**Triggers:**
- Git tags matching `v*` (e.g., `v1.0.0`, `v1.0.0-rc.1`, `v1.0.0-beta.1`)

**What it does:**
1. Extracts version and stage (stable/rc/beta) from tag name
2. Builds all documentation with `DOCS_VERSION` set from the tag
3. Checks out the `gh-pages` branch (creates it if needed)
4. Copies build output to a versioned directory (`gh-pages/<version>/`)
5. Updates `latest` symlink for stable releases
6. Updates `versions.json` manifest via `scripts/update-versions-json.sh`
7. Commits to `gh-pages` branch and deploys via GitHub Pages

**Version stages:**
- **Stable** (e.g., `v1.0.0`): Updates `latest` symlink, marked as stable in `versions.json`
- **Release candidate** (e.g., `v1.0.0-rc.1`): Deployed alongside other versions, RC banner shown
- **Beta** (e.g., `v1.0.0-beta.1`): Deployed alongside other versions, beta banner shown

**Key features:**
- Build-and-archive: each tagged version is built once and stored permanently
- Concurrency group (`pages-deploy`) prevents parallel deploys from corrupting `gh-pages`
- Versions accumulate on `gh-pages` branch — old versions are never removed

### 3. Verify Submodule Health
**File:** `cleanroom-website/.github/workflows/verify-submodules.yml`

**Triggers:**
- Push to `main` branch
- Pull requests
- Manual workflow dispatch
- Weekly schedule (Mondays at 9am UTC)

**What it does:**
1. Checks submodule status (detached HEAD warnings)
2. Verifies all submodules are initialized
3. Checks for uncommitted changes
4. Checks for available updates (when GitHub remotes configured)
5. Generates health report

## Workflow Diagrams

### Standard Development Flow

```
Developer → Push to main → CI Build → Upload Artifact
                ↓
           Submodules updated
                ↓
           Build with DOCS_VERSION=dev
                ↓
           Warning check (make html-check)
                ↓
           Upload build artifact
                ↓
           Deploy to gh-pages/dev/
```

### Release Flow

```
Developer → Create tag (v1.0.0-rc.1) → Versioned Deployment
                ↓
           Build with DOCS_VERSION=1.0.0-rc.1
                ↓
           Deploy to gh-pages/1.0.0-rc.1/
                ↓
           Review (RC banner displayed)
                ↓
Developer → Create tag (v1.0.0) → Stable Deployment
                ↓
           Deploy to gh-pages/1.0.0/
                ↓
           Update latest symlink → 1.0.0
                ↓
           Update versions.json
```

## Setting Up CI/CD

### Prerequisites

**For technical-docs repository:**

1. **Enable GitHub Pages:**
   - Go to Settings → Pages
   - Source: "GitHub Actions"
   - This is required for both dev deployment and tagged releases

3. **Configure environment:**
   - Settings → Environments
   - Create "github-pages" environment
   - Add protection rules if desired

**For cleanroom-website repository:**

Node.js:
- CI uses `.nvmrc` (via `actions/setup-node` `node-version-file`) for the website workflow Node version.

**For individual project repositories:**

No CI/CD setup needed unless you want independent builds.

### Testing Locally Before Push

Use the local CI test script:

```bash
# From cleanroom-website directory
./scripts/test-ci-locally.sh
```

This simulates the GitHub Actions workflow and will:
- Verify all prerequisites
- Check submodule health
- Build all project docs
- Build master docs
- Check for warnings
- Verify cross-references

**Exit codes:**
- `0` - All checks passed
- `1` - Build failed or warnings detected

## Deployment Workflows

### Deploying Documentation Changes

**Scenario 1: Update content in a project**

```bash
# Edit content in project docs
cd technical-docs/<project>
# ... make changes ...
git add .
git commit -m "Update documentation"
git push

# Update submodule reference
cd ..
git add <project>
git commit -m "Update docs submodule"
git push

# This triggers technical-docs CI → deploys to GitHub Pages
```

**Scenario 2: Update master documentation**

```bash
cd technical-docs
# ... edit source/*.rst ...
git add source/
git commit -m "Update master documentation"
git push

# Triggers CI → deploys to GitHub Pages
```

**Scenario 3: Update from parent repository**

```bash
cd cleanroom-website
# ... make changes to technical-docs submodule ...
git add technical-docs
git commit -m "Update technical docs"
git push

# Triggers verify-submodules workflow
# Does NOT trigger technical-docs CI (must push from technical-docs)
```

### Deploying a Release

**Step 1: Create Release Candidate**

```bash
cd technical-docs
git tag v1.0.0-rc.1
git push origin v1.0.0-rc.1
```

This triggers `deploy-tagged.yml` which:
- Builds with `DOCS_VERSION=1.0.0-rc.1`
- Deploys to `gh-pages/1.0.0-rc.1/`
- Updates `versions.json` (no stable flag)
- RC banner is displayed on all pages

**Step 2: Review**

- URL: `https://cleanroom-labs.github.io/technical-docs/1.0.0-rc.1/`
- Verify content, cross-references, formatting
- RC banner should read: "This is a release candidate (1.0.0-rc.1). Report issues before final release."

**Step 3: Create Stable Release**

```bash
cd technical-docs
git tag v1.0.0
git push origin v1.0.0
```

This triggers `deploy-tagged.yml` which:
- Builds with `DOCS_VERSION=1.0.0`
- Deploys to `gh-pages/1.0.0/`
- Updates `latest` symlink to point to `1.0.0`
- Sets `stable: true` in `versions.json`
- No banner (stable version)

**Step 4: Update Parent Repository**

```bash
cd cleanroom-website
cd technical-docs
git checkout v1.0.0
cd ..
git add technical-docs
git commit -m "Release v1.0.0 documentation"
git push
```

## Monitoring Builds

### GitHub Actions Dashboard

1. Navigate to repository → Actions tab
2. View workflow runs:
   - Green checkmark: Success
   - Red X: Failed
   - Yellow circle: In progress

### Common Build Failures

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for build failure solutions.

## Environment Variables

The workflows use these environment variables:

**Automatic (GitHub Actions):**
- `GITHUB_REF` - Git ref (branch or tag)
- `GITHUB_SHA` - Commit SHA
- `GITHUB_REF_NAME` - Branch/tag name
- `GITHUB_EVENT_NAME` - Trigger event (push, pull_request, etc.)

To add additional environment variables:
1. Repository Settings → Secrets and variables → Actions
2. Add repository secret or variable
3. Reference in workflow: `${{ secrets.MY_SECRET }}`

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for CI/CD troubleshooting, including workflow triggers, submodule version issues, and local-vs-CI debugging.

## Advanced Configuration

### Multi-Version Documentation

The documentation system supports multiple versions simultaneously via a build-and-archive approach:

**URL structure:**
```
/docs/dev/           → Latest from main branch (rebuilt on every push)
/docs/1.0.0/         → Stable release (built once from v1.0.0 tag)
/docs/1.0.0-rc.1/    → Release candidate
/docs/latest/        → Symlink to newest stable version
/docs/versions.json  → Version manifest for the version switcher
```

**How it works:**
- Each tagged version is built once and stored permanently on the `gh-pages` branch
- The `dev` version is rebuilt on every push to main
- A version switcher dropdown in the navigation bar lets users switch between versions
- Pre-release banners (dev, beta, RC) warn users when viewing non-stable docs
- `versions.json` tracks all deployed versions and is updated by `scripts/update-versions-json.sh`

**Key files:**
- `common/theme_config.py` — `get_docs_version()` and `get_version_stage()` read version from `DOCS_VERSION` env var
- `common/sphinx/_static/version-switcher.js` — Fetches `versions.json` and populates the dropdown
- `technical-docs/scripts/update-versions-json.sh` — Adds/updates version entries in the manifest
- `technical-docs/.github/workflows/deploy-tagged.yml` — Versioned deployment for tagged releases
- `technical-docs/.github/workflows/sphinx-docs.yml` — Dev deployment on push to main

See [VERSIONING_GUIDE.md](VERSIONING_GUIDE.md) for the full versioning strategy.

### Custom Deployment Target

To deploy somewhere other than GitHub Pages:

1. Replace `actions/deploy-pages@v4` with custom deployment
2. Examples: AWS S3, Netlify, Vercel, self-hosted server

```yaml
- name: Deploy to custom target
  run: |
    # Upload build/html to your server
    rsync -avz build/html/ user@server:/var/www/docs/
```

### Notification on Build Failure

Add notification step:

```yaml
- name: Notify on failure
  if: failure()
  run: |
    # Send notification (Slack, email, etc.)
    curl -X POST $WEBHOOK_URL -d '{"text":"Build failed!"}'
```

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Deployment](https://github.com/actions/deploy-pages)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Git Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)

## Support

For issues with CI/CD:
1. Check workflow logs in Actions tab
2. Run `./scripts/test-ci-locally.sh` to reproduce locally
3. Review this guide for common issues
4. Check the repository Issues tracker (if enabled)
