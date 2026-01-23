#!/bin/bash
# Test CI workflow locally
# Simulates the GitHub Actions build process

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "# Testing CI Workflow Locally"
echo ""
echo "Root directory: $ROOT_DIR"
echo ""

# Check prerequisites
echo "## Checking Prerequisites"
echo ""

if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: python3 not found"
    exit 1
fi
echo "✓ Python 3: $(python3 --version)"

if ! command -v pip &> /dev/null; then
    echo "❌ ERROR: pip not found"
    exit 1
fi
echo "✓ pip: $(pip --version)"

if ! command -v sphinx-build &> /dev/null; then
    echo "⚠️  WARNING: sphinx-build not in PATH"
    echo "   Installing dependencies..."
    cd "$ROOT_DIR/cleanroom-technical-docs"
    pip install -r requirements.txt
    cd "$ROOT_DIR"
fi
echo "✓ sphinx-build: $(sphinx-build --version)"

echo ""
echo "## Verifying Submodules"
echo ""

cd "$ROOT_DIR"

# Check submodule status
git submodule status

# Check technical-docs
cd cleanroom-technical-docs

CURRENT=$(git describe --exact-match --tags 2>/dev/null || git branch --show-current || echo "DETACHED")
if [ "$CURRENT" = "DETACHED" ]; then
    echo "⚠️  technical-docs is in DETACHED HEAD state"
    echo "   Commit: $(git rev-parse --short HEAD)"
else
    echo "✓ technical-docs on: $CURRENT"
fi

# Check nested submodules
for submodule in airgap-whisper-docs airgap-deploy-docs airgap-transfer-docs; do
    if [ ! -e "$submodule/.git" ]; then
        echo "❌ ERROR: Submodule $submodule not initialized"
        exit 1
    fi

    cd $submodule
    CURRENT=$(git describe --exact-match --tags 2>/dev/null || git branch --show-current || echo "DETACHED")
    if [ "$CURRENT" = "DETACHED" ]; then
        echo "⚠️  $submodule is in DETACHED HEAD state"
        echo "   Commit: $(git rev-parse --short HEAD)"
    else
        echo "✓ $submodule on: $CURRENT"
    fi
    cd ..
done

cd "$ROOT_DIR"

echo ""
echo "## Building Individual Project Documentation"
echo ""

cd cleanroom-technical-docs

for project in airgap-whisper-docs airgap-deploy-docs airgap-transfer-docs; do
    echo "### Building $project"

    cd $project

    # Install dependencies if needed
    if [ -f requirements.txt ]; then
        pip install -r requirements.txt > /dev/null 2>&1
    fi

    # Build
    sphinx-build -M html source build

    if [ ! -f build/html/index.html ]; then
        echo "❌ ERROR: Build failed for $project"
        exit 1
    fi

    echo "✓ $project built successfully"
    echo ""
    cd ..
done

echo ""
echo "## Building Master Documentation"
echo ""

make html 2>&1 | tee build.log

# Check for warnings
if grep -qi "warning" build.log; then
    echo ""
    echo "⚠️  Build completed with warnings:"
    echo ""
    grep -i "warning" build.log
    echo ""
    WARNINGS="true"
else
    echo "✓ Build completed with no warnings"
    WARNINGS="false"
fi

# Verify cross-references
echo ""
echo "## Verifying Cross-References"
echo ""

cd build/html

if grep -r "airgap-whisper" . >/dev/null 2>&1; then
    echo "✓ airgap-whisper references found"
else
    echo "⚠️  No references to airgap-whisper found"
fi

if grep -r "airgap-deploy" . >/dev/null 2>&1; then
    echo "✓ airgap-deploy references found"
else
    echo "⚠️  No references to airgap-deploy found"
fi

if grep -r "airgap-transfer" . >/dev/null 2>&1; then
    echo "✓ airgap-transfer references found"
else
    echo "⚠️  No references to airgap-transfer found"
fi

cd "$ROOT_DIR"

echo ""
echo "## Summary"
echo ""

if [ "$WARNINGS" = "true" ]; then
    echo "⚠️  CI test completed with warnings"
    echo ""
    echo "The build succeeded but produced warnings."
    echo "Review the build.log above and fix warnings before pushing."
    echo ""
    echo "Build output: cleanroom-technical-docs/build/html/index.html"
    exit 1
else
    echo "✅ CI test passed successfully!"
    echo ""
    echo "All checks passed. The build is ready for CI/CD."
    echo ""
    echo "Build output: cleanroom-technical-docs/build/html/index.html"
    echo ""
    echo "To view the documentation:"
    echo "  open cleanroom-technical-docs/build/html/index.html"
fi
