# Production Deployment Guide

**Target:** Deploy nested submodule documentation to GitHub Pages
**Prerequisites:** Completed Weeks 1-3, local builds passing
**Estimated time:** 30-45 minutes (first time), 5 minutes (subsequent deployments)

## Pre-Deployment Checklist

Before deploying to production, verify:

- [ ] All builds passing locally (`./scripts/test-ci-locally.sh`)
- [ ] Submodules in healthy state (`./scripts/check-submodules.sh`)
- [ ] Master documentation builds with 0 warnings
- [ ] Cross-references working between projects
- [ ] All changes committed and pushed locally
- [ ] Team trained on submodule workflows (`docs/TEAM_TRAINING.md`)

## Deployment Overview

**Current state:** Local development fully functional with file:// URLs
**Target state:** GitHub repositories with HTTPS URLs, automated CI/CD

**Architecture after deployment:**
```
GitHub Organization: cleanroom-website
├── cleanroom-website (parent repo)
├── cleanroom-technical-docs (docs aggregator)
├── airgap-whisper-docs (project docs)
├── airgap-deploy-docs (project docs)
└── airgap-transfer-docs (project docs)
```

## Step 1: Create GitHub Repositories (10 minutes)

### 1.1 Create Organization Repositories

On GitHub (github.com/cleanroom-website or your organization):

**Create these 5 repositories:**

1. **cleanroom-website**
   - Description: "Parent repository for AirGap project suite"
   - Visibility: Public (or Private)
   - Initialize: **Do not** initialize (we're pushing existing code)

2. **cleanroom-technical-docs**
   - Description: "Aggregated technical documentation for AirGap projects"
   - Visibility: Public (recommended for docs)
   - Initialize: **Do not** initialize

3. **airgap-whisper-docs**
   - Description: "Documentation for AirGap Whisper (offline audio transcription)"
   - Visibility: Public
   - Initialize: **Do not** initialize

4. **airgap-deploy-docs**
   - Description: "Documentation for AirGap Deploy (deployment packaging tool)"
   - Visibility: Public
   - Initialize: **Do not** initialize

5. **airgap-transfer-docs**
   - Description: "Documentation for AirGap Transfer (file transfer utility)"
   - Visibility: Public
   - Initialize: **Do not** initialize

### 1.2 Configure Deploy Keys (Optional)

If using private repositories, set up deploy keys or configure organization access.

For public repositories, this is not necessary.

## Step 2: Push Local Repositories to GitHub (10 minutes)

### 2.1 Push Project Documentation Repositories

```bash
# airgap-whisper-docs
cd /Users/andfranklin/Projects/airgap-whisper-docs
git remote add origin git@github.com:cleanroom-website/airgap-whisper-docs.git
git push -u origin main
git push --tags  # Push any existing tags

# airgap-deploy-docs
cd /Users/andfranklin/Projects/airgap-deploy-docs
git remote add origin git@github.com:cleanroom-website/airgap-deploy-docs.git
git push -u origin main
git push --tags

# airgap-transfer-docs
cd /Users/andfranklin/Projects/airgap-transfer-docs
git remote add origin git@github.com:cleanroom-website/airgap-transfer-docs.git
git push -u origin main
git push --tags
```

**Verify:** Check that each repository shows files on GitHub.

### 2.2 Update cleanroom-technical-docs Submodule URLs

```bash
cd /Users/andfranklin/Projects/cleanroom-website/cleanroom-technical-docs

# Edit .gitmodules
cat > .gitmodules <<'EOF'
[submodule "airgap-whisper-docs"]
	path = airgap-whisper-docs
	url = git@github.com:cleanroom-website/airgap-whisper-docs.git
[submodule "airgap-deploy-docs"]
	path = airgap-deploy-docs
	url = git@github.com:cleanroom-website/airgap-deploy-docs.git
[submodule "airgap-transfer-docs"]
	path = airgap-transfer-docs
	url = git@github.com:cleanroom-website/airgap-transfer-docs.git
EOF

# Update submodule configuration
git submodule sync --recursive
git add .gitmodules
git commit -m "Update submodule URLs to GitHub"
```

### 2.3 Push cleanroom-technical-docs

```bash
cd /Users/andfranklin/Projects/cleanroom-website/cleanroom-technical-docs
git remote add origin git@github.com:cleanroom-website/cleanroom-technical-docs.git
git push -u origin main
git push --tags
```

**Verify:** Check that technical-docs shows on GitHub with submodules listed.

### 2.4 Update cleanroom-website Submodule URL

```bash
cd /Users/andfranklin/Projects/cleanroom-website

# Edit .gitmodules
cat > .gitmodules <<'EOF'
[submodule "cleanroom-technical-docs"]
	path = cleanroom-technical-docs
	url = git@github.com:cleanroom-website/cleanroom-technical-docs.git
EOF

# Update submodule configuration
git submodule sync --recursive
git add .gitmodules
git commit -m "Update technical-docs submodule URL to GitHub"
```

### 2.5 Push cleanroom-website

```bash
cd /Users/andfranklin/Projects/cleanroom-website
git remote add origin git@github.com:cleanroom-website/cleanroom-website.git
git push -u origin main
git push --tags
```

**Verify:** All 5 repositories visible on GitHub.

## Step 3: Configure GitHub Pages (5 minutes)

### 3.1 Enable GitHub Pages for cleanroom-technical-docs

1. Navigate to: `https://github.com/cleanroom-website/cleanroom-technical-docs`
2. Click **Settings** → **Pages**
3. Under "Build and deployment":
   - **Source:** Select "GitHub Actions"
   - (Not "Deploy from a branch")
4. Click **Save**

**Note:** No other repositories need GitHub Pages configured. Only the technical-docs repository deploys documentation.

### 3.2 Verify Workflow Permissions

1. Still in **Settings** → **Actions** → **General**
2. Under "Workflow permissions":
   - Select: "Read and write permissions"
   - Check: "Allow GitHub Actions to create and approve pull requests"
3. Click **Save**

This ensures workflows can deploy to GitHub Pages.

## Step 4: Trigger First Deployment (5 minutes)

### 4.1 Create Empty Commit to Trigger CI

```bash
cd /Users/andfranklin/Projects/cleanroom-website/cleanroom-technical-docs
git commit --allow-empty -m "Trigger initial GitHub Pages deployment"
git push
```

### 4.2 Monitor Build

1. Navigate to: `https://github.com/cleanroom-website/cleanroom-technical-docs/actions`
2. Click on the running workflow: "Build and Deploy Sphinx Documentation"
3. Watch the build progress:
   - "build" job should complete successfully
   - "deploy" job should deploy to GitHub Pages

**Expected duration:** 2-3 minutes

**If build fails:** Check workflow logs, compare with local build results.

### 4.3 Verify Deployment

**Your documentation will be available at:**
```
https://cleanroom-website.github.io/cleanroom-technical-docs/
```

**Check that:**
- [ ] Home page loads correctly
- [ ] Navigation works (Projects → Whisper/Deploy/Transfer)
- [ ] Cross-references work (click intersphinx links)
- [ ] Styling matches local build
- [ ] Search works

## Step 5: Configure Environments (Optional, 5 minutes)

For tag-based deployments with preview/production separation:

### 5.1 Create Environments

1. Repository **Settings** → **Environments**
2. Click **New environment**

**Create two environments:**

**Production Environment:**
- Name: `github-pages-production`
- No protection rules needed (optional: require approvals)

**Preview Environment:**
- Name: `github-pages-preview`
- Protection rules (optional): None, or require approval for RC deployments

### 5.2 Test Tagged Deployment

```bash
cd /Users/andfranklin/Projects/cleanroom-website/cleanroom-technical-docs
git tag v0.1.0-rc.1
git push origin v0.1.0-rc.1
```

This triggers `deploy-tagged.yml` workflow.

Check Actions tab to verify preview deployment.

## Step 6: Update Local Repositories (5 minutes)

### 6.1 Clone Fresh from GitHub

To verify everything works from GitHub:

```bash
# Somewhere outside your current work directory
cd ~/tmp
git clone --recurse-submodules git@github.com:cleanroom-website/cleanroom-website.git
cd cleanroom-website

# Verify
./scripts/check-submodules.sh
./scripts/test-ci-locally.sh
```

**This should work identically to your local development environment.**

### 6.2 Update Team Workflow

From now on, team members should:

```bash
# Clone (first time)
git clone --recurse-submodules git@github.com:cleanroom-website/cleanroom-website.git

# Pull updates (daily)
git pull --recurse-submodules
```

## Deployment Workflows

### Deploying Documentation Updates

**Scenario:** You fixed content in whisper docs.

```bash
# 1. Make changes in project repo
cd cleanroom-technical-docs/airgap-whisper-docs
git checkout main
# ... edit files ...
git add .
git commit -m "Fix documentation error"
git push origin main

# 2. Update technical-docs submodule reference
cd ..
git add airgap-whisper-docs
git commit -m "Update whisper docs"
git push origin main

# This triggers CI → builds and deploys to GitHub Pages
```

**Check deployment:**
- Actions tab shows green checkmark
- Documentation updates at `https://cleanroom-website.github.io/cleanroom-technical-docs/`

### Deploying a Release

**Scenario:** Release whisper docs v1.0.0.

**Step 1: Release Candidate (optional)**

```bash
cd cleanroom-technical-docs/airgap-whisper-docs
git tag v1.0.0-rc.1
git push origin v1.0.0-rc.1

cd ..
git tag v1.0.0-rc.1
git push origin v1.0.0-rc.1
```

**Result:** Deploys to preview environment (same URL with RC badge).

**Step 2: Final Release**

```bash
cd cleanroom-technical-docs/airgap-whisper-docs
git tag v1.0.0
git push origin v1.0.0

cd ..
git add airgap-whisper-docs  # Update to tagged version
git commit -m "Release whisper docs v1.0.0"
git tag v1.0.0
git push origin main
git push origin v1.0.0
```

**Result:** Deploys to production GitHub Pages.

## Monitoring and Maintenance

### Daily Monitoring

**Check GitHub Actions tab:**
- `https://github.com/cleanroom-website/cleanroom-technical-docs/actions`

**Look for:**
- All builds passing (green checkmarks)
- No warning failures
- Deployment succeeds

**Weekly verification:**
- Run `verify-submodules.yml` workflow manually
- Review submodule health report

### Common Issues

**Issue: Build fails with "submodule not initialized"**

**Cause:** Workflow missing `submodules: recursive`

**Fix:** Verify workflow has:
```yaml
- uses: actions/checkout@v4
  with:
    submodules: recursive
```

**Issue: Deployment fails with "resource not accessible"**

**Cause:** Workflow permissions not set

**Fix:**
1. Settings → Actions → General
2. Workflow permissions: "Read and write permissions"
3. Save and re-run workflow

**Issue: GitHub Pages shows old content**

**Cause:** Caching or deployment delay

**Fix:**
1. Hard refresh browser (Cmd+Shift+R / Ctrl+Shift+R)
2. Wait 1-2 minutes for CDN cache to clear
3. Check Actions tab to verify deployment completed

**Issue: Cross-references broken after deployment**

**Cause:** Intersphinx mappings using local paths

**Fix:** This should not happen with current configuration (uses relative paths). If it does, verify `source/conf.py`:
```python
intersphinx_mapping = {
    'airgap-whisper': ('../airgap-whisper-docs/build/html/', None),
    # ... not absolute URLs
}
```

## Rollback Procedures

### Rollback a Bad Deployment

**Immediate rollback:**

```bash
cd cleanroom-technical-docs
git revert HEAD
git push origin main
```

**Rollback to specific version:**

```bash
cd cleanroom-technical-docs
git reset --hard <good-commit-sha>
git push --force origin main  # Use with caution
```

**Rollback a submodule:**

```bash
cd cleanroom-technical-docs
cd airgap-whisper-docs
git checkout <previous-tag-or-commit>
cd ..
git add airgap-whisper-docs
git commit -m "Rollback whisper docs to <version>"
git push origin main
```

### Emergency: Disable Deployment

If deployments are failing repeatedly:

1. Navigate to workflow file on GitHub
2. Edit `.github/workflows/sphinx-docs.yml`
3. Change trigger to manual only:
   ```yaml
   on:
     workflow_dispatch:  # Manual only
   ```
4. Commit directly to main
5. Fix issues locally
6. Re-enable automatic triggers

## Success Criteria

Deployment is successful when:

- [ ] All 5 repositories on GitHub
- [ ] Submodules using GitHub URLs (not file://)
- [ ] GitHub Pages enabled for technical-docs
- [ ] CI builds passing automatically on push
- [ ] Documentation accessible at `cleanroom-website.github.io/cleanroom-technical-docs/`
- [ ] Cross-references working
- [ ] Tag-based deployments working (optional, test with RC tag)
- [ ] Team can clone and work with repositories
- [ ] Fresh clone builds successfully with `./scripts/test-ci-locally.sh`

## Post-Deployment

### Update Documentation Links

Update any external links to point to new GitHub Pages URL:
- README files
- Project websites
- Internal wikis

### Configure Custom Domain (Optional)

To use a custom domain (e.g., docs.cleanroomlabs.com):

1. Add CNAME record in DNS:
   ```
   docs.cleanroomlabs.com → cleanroom-website.github.io
   ```

2. In repository Settings → Pages:
   - Custom domain: `docs.cleanroomlabs.com`
   - Check "Enforce HTTPS"

3. Wait for DNS propagation (up to 24 hours)

4. Update intersphinx mappings to use custom domain

### Set Up Notifications (Optional)

Configure Slack/email notifications for build failures:

1. Create webhook URL (Slack/Discord/etc.)
2. Add to repository secrets
3. Add notification step to workflows:
   ```yaml
   - name: Notify on failure
     if: failure()
     run: |
       curl -X POST ${{ secrets.SLACK_WEBHOOK }} \
         -d '{"text":"Documentation build failed!"}'
   ```

## Ongoing Operations

### Regular Tasks

**Daily:**
- Monitor Actions tab for build status
- Review and merge documentation PRs

**Weekly:**
- Run `verify-submodules.yml` workflow
- Review submodule health report
- Update dependencies if needed

**Monthly:**
- Review GitHub Pages usage/limits
- Archive old artifacts
- Update documentation as needed

**Per Release:**
- Tag project docs (v1.0.0-rc.1, v1.0.0)
- Tag technical-docs to match
- Update parent repo reference
- Verify deployment
- Communicate to team

### Scaling for More Projects

When adding project #4, #5, etc.:

1. Create new project-docs repository on GitHub
2. Add as submodule: `./scripts/add-new-project.sh <name> <github-url>`
3. Update intersphinx mappings
4. Update master index
5. Verify build
6. Push and deploy

## Support and Resources

**Documentation:**
- Architecture: `docs/ARCHITECTURE.md`
- CI/CD Guide: `docs/CI_CD_GUIDE.md`
- Team Training: `docs/TEAM_TRAINING.md`
- Submodules: `docs/SUBMODULES_GUIDE.md`

**Tools:**
- Check health: `./scripts/check-submodules.sh`
- Test CI: `./scripts/test-ci-locally.sh`
- Update project: `./scripts/update-project-docs.sh`
- Build project: `./scripts/build-single-project.sh`

**External Resources:**
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Git Submodules Book](https://git-scm.com/book/en/v2/Git-Tools-Submodules)
- [Sphinx Documentation](https://www.sphinx-doc.org/)

## Troubleshooting Deployment

**If deployment fails, check in order:**

1. **Local build:** Does `./scripts/test-ci-locally.sh` pass?
2. **Workflow logs:** What does GitHub Actions show?
3. **Submodules:** Does `./scripts/check-submodules.sh` report issues?
4. **Permissions:** Are workflow permissions set correctly?
5. **Pages config:** Is GitHub Pages source set to "GitHub Actions"?
6. **Network:** Can GitHub reach external resources (if any)?

**Still stuck?** Compare against working local environment—what's different?

---

**Deployment guide complete. Your documentation is now live!**
