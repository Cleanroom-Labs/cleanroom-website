# Troubleshooting Guide

This guide consolidates common issues and solutions for the cleanroom-website documentation system.

## Build Issues

### Sphinx Build Failures

**"No module named 'sphinx'"**

The Python virtual environment is not set up or activated.

```bash
cd cleanroom-technical-docs
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**"Sphinx directory not found"**

Submodules are not initialized.

```bash
git submodule update --init --recursive
```

**needflow diagrams not rendering**

Graphviz is not installed.

```bash
# macOS
brew install graphviz

# Ubuntu/Debian
sudo apt-get install graphviz

# Verify installation
dot -V
```

**"Cannot use import statement outside a module"**

Build script needs `.mjs` extension or `"type": "module"` in package.json.

- Ensure build script is named `build-docs.mjs` (not `.js`)
- Or add `"type": "module"` to package.json

**Build warnings detected**

Sphinx detected issues like broken links or missing references. Run locally to see details:

```bash
cd cleanroom-technical-docs
make html
# Review warnings in output
```

### Intersphinx Inventory Warnings (Safe to Ignore)

During local development, you may see warnings like:

```
WARNING: failed to reach any of the inventories with the following issues:
intersphinx inventory 'https://cleanroomlabs.dev/docs/airgap-deploy/objects.inv'
not fetchable due to 404 Client Error
```

**This is expected behavior.** The subproject `conf.py` files have intersphinx mappings pointing to URLs that don't exist yet (e.g., `https://cleanroomlabs.dev/docs/airgap-deploy/`). These URLs will work once the documentation is deployed to cleanroomlabs.dev.

Why this is safe to ignore:
- **Warnings, not errors** - The build completes successfully
- **Self-resolving** - Once docs are deployed, the URLs will work
- **Local builds work** - The master docs use local relative paths during development

The only impact is that cross-project `:ref:` links in subprojects won't resolve during local development. All other documentation features work normally.

## CI/CD Issues

### Workflow Not Triggering

**Check path filters:**

```yaml
on:
  push:
    paths:
      - 'source/**'           # Only triggers for source/ changes
      - '*-docs/**'           # Or submodule changes
```

Solution: Change a matching path or use manual `workflow_dispatch`.

**Check branch filters:**

```yaml
on:
  push:
    branches: [main]  # Only triggers on main branch
```

Solution: Push to `main` or add your branch.

### Common CI Failures

| Error | Cause | Solution |
|-------|-------|----------|
| "Submodule not initialized" | Missing checkout option | Add `submodules: recursive` to checkout action |
| "Resource not accessible by integration" | Wrong permissions | Enable workflow write permissions in Settings > Actions |
| "intersphinx inventory not fetchable" | Build order wrong | Build project docs before master docs |

### Local Build Works, CI Fails

Possible causes:
1. **Missing dependency** - Check `requirements.txt` is complete
2. **System dependency** - Ensure Graphviz is installed in workflow
3. **Path issues** - Use relative paths, not absolute
4. **Case sensitivity** - macOS is case-insensitive, Linux is case-sensitive

Debug approach:
```bash
./scripts/test-ci-locally.sh
```

## Submodule Issues

### Detached HEAD State

This is **normal** for submodules - they point to specific commits, not branches.

To make changes:
```bash
cd cleanroom-technical-docs/<project>-docs
git checkout main
# Now you can commit and push
```

### Changes Not Showing After Pull

Update submodules to their recorded commits:
```bash
git submodule update --recursive --remote
```

### Can't Push Changes

You're likely in detached HEAD state:
```bash
git checkout main
# Now push will work
```

### Submodules at Wrong Version

The parent repository references have not been updated.

```bash
cd cleanroom-technical-docs
git submodule update --remote <project>-docs
# Or manually:
cd <project>-docs
git checkout v1.0.0
cd ..
git add <project>-docs
git commit -m "Update docs to v1.0.0"
```

## Deployment Issues

### 404 Errors on /docs Paths

1. Verify `public/docs/` contains `index.html` after build
2. Check build logs for Sphinx errors
3. Ensure GitHub Pages source is set to "GitHub Actions"

### Old Content Showing After Deploy

- Hard refresh browser (Ctrl+Shift+R / Cmd+Shift+R)
- Wait for CDN cache to expire
- Check deployment actually completed in Actions tab

### Cross-References Broken

Verify intersphinx uses relative paths in `conf.py`.

## Development Issues

### Documentation Not Loading on Localhost

Build docs before starting dev server:
```bash
node scripts/build-docs.mjs
# Then start your dev server
```

### Dev Server Doesn't Show Updated Docs

Documentation is cached. Rebuild:
```bash
node scripts/build-docs.mjs
```

## Quick Diagnostic Commands

```bash
# Check submodule health
./scripts/check-submodules.sh

# Test CI locally
./scripts/test-ci-locally.sh

# Build documentation
node scripts/build-docs.mjs

# Check Python environment
cd cleanroom-technical-docs
source .venv/bin/activate
pip list | grep sphinx
```

## References

- [CI/CD Guide](CI_CD_GUIDE.md) - Workflow configuration
- [Submodules Guide](SUBMODULES_GUIDE.md) - Submodule operations
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Production deployment
- [Architecture](ARCHITECTURE.md) - Design decisions
