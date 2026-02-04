# CI/CD Guide for AirGap Documentation

This guide explains the CI/CD infrastructure for building and deploying the nested submodule documentation architecture.

## Overview

The CI/CD system consists of **three workflows** that handle different aspects of the build and deployment process:

### 1. Build and Verify (Main Branch)
**File:** `technical-docs/.github/workflows/sphinx-docs.yml`

**Triggers:**
- Push to `main` branch (when docs or submodules change)
- Pull requests to `main`
- Manual workflow dispatch

**What it does:**
1. Checks out repository with all nested submodules (requires `SUBMODULE_PAT` secret)
2. Verifies submodule initialization
3. Builds each project's documentation via `make html`
4. Checks for warnings via `make html-check`
5. Verifies project docs are present in build output
6. Verifies cross-references are working
7. Uploads build artifact

**Key features:**
- Full submodule support with `submodules: recursive`
- Individual project builds before master build (enables intersphinx)
- Centralized warning detection via `make html-check` (matches local build behavior)
- Cross-reference verification
- Python 3.14, Graphviz for diagram generation

### 2. Deploy Tagged Release
**File:** `technical-docs/.github/workflows/deploy-tagged.yml`

**Triggers:**
- Git tags matching `v*` (e.g., `v1.0.0`) → Production
- Git tags matching `v*-rc.*` (e.g., `v1.0.0-rc.1`) → Preview

**What it does:**
1. Determines environment (production vs preview) from tag format
2. Checks if submodules have matching tags
3. Builds all documentation
4. Adds version badge to docs
5. Deploys to appropriate environment

**Environments:**
- **Production:** Stable releases (v1.0.0, v2.1.3, etc.)
- **Preview:** Release candidates (v1.0.0-rc.1, v2.0.0-rc.2, etc.)

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
           Individual builds (project submodules)
                ↓
           Master build with intersphinx
                ↓
           Warning check (make html-check)
                ↓
           Upload build artifact
```

### Release Flow

```
Developer → Create tag (v1.0.0-rc.1) → Preview Deployment
                ↓
           Review in preview
                ↓
           Create tag (v1.0.0) → Production Deployment
                ↓
           Update submodule references → CI Build
```

## Setting Up CI/CD

### Prerequisites

**For technical-docs repository:**

1. **Configure `SUBMODULE_PAT` secret:**
   - Go to Settings → Secrets and variables → Actions
   - Add a repository secret named `SUBMODULE_PAT`
   - Value: a GitHub Personal Access Token with `repo` scope (needed to check out private submodules)

2. **Enable GitHub Pages (only if using deploy-tagged workflow):**
   - Go to Settings → Pages
   - Source: "GitHub Actions"
   - Branch: Not needed (Actions deploys directly)

3. **Configure environments (only if using deploy-tagged workflow):**
   - Settings → Environments
   - Create "github-pages-production"
   - Create "github-pages-preview"
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
# Tag the docs
cd technical-docs/<project>
git tag v1.0.0-rc.1
git push origin v1.0.0-rc.1

# Tag the master docs
cd ..
git tag v1.0.0-rc.1
git push origin v1.0.0-rc.1
```

This triggers:
- `deploy-tagged.yml` workflow
- Deploys to **preview** environment
- URL: `https://cleanroom-labs.github.io/technical-docs/` (with RC badge)

**Step 2: Review Preview**

- Test all functionality
- Verify cross-references
- Check formatting

**Step 3: Create Final Release**

```bash
# Tag the docs (final)
cd technical-docs/<project>
git tag v1.0.0
git push origin v1.0.0

# Tag the master docs (final)
cd ..
git tag v1.0.0
git push origin v1.0.0
```

This triggers:
- `deploy-tagged.yml` workflow
- Deploys to **production** environment
- URL: `https://cleanroom-labs.github.io/technical-docs/`

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

**Secrets:**
- `SUBMODULE_PAT` - GitHub Personal Access Token with `repo` scope (required for private submodule checkout)

To add additional environment variables:
1. Repository Settings → Secrets and variables → Actions
2. Add repository secret or variable
3. Reference in workflow: `${{ secrets.MY_SECRET }}`

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for CI/CD troubleshooting, including workflow triggers, submodule version issues, and local-vs-CI debugging.

## Advanced Configuration

### Multi-Version Documentation

To support multiple versions (not yet implemented):

1. Update `deploy-tagged.yml` to preserve old versions
2. Add version switcher to Sphinx theme
3. Configure permalink structure

See the plan file for full multi-version architecture.

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
