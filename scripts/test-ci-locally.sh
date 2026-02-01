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

TECH_DOCS_DIR="$ROOT_DIR/technical-docs"
VENV_DIR="$TECH_DOCS_DIR/.venv"
PIP="$VENV_DIR/bin/pip"
SPHINX_BUILD="$VENV_DIR/bin/sphinx-build"

if [ ! -x "$SPHINX_BUILD" ]; then
    echo "Setting up Sphinx virtualenv at $VENV_DIR ..."
    python3 -m venv "$VENV_DIR"
    "$PIP" install -r "$TECH_DOCS_DIR/requirements.txt"
fi
echo "✓ sphinx-build: $("$SPHINX_BUILD" --version)"

echo ""
echo "## Verifying Submodules"
echo ""

cd "$ROOT_DIR"

# Check submodule status
git submodule status

# Check technical-docs
cd technical-docs

CURRENT=$(git describe --exact-match --tags 2>/dev/null || git branch --show-current || echo "DETACHED")
if [ "$CURRENT" = "DETACHED" ]; then
    echo "⚠️  technical-docs is in DETACHED HEAD state"
    echo "   Commit: $(git rev-parse --short HEAD)"
else
    echo "✓ technical-docs on: $CURRENT"
fi

# Check nested submodules
for submodule in whisper deploy transfer; do
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
echo "## Building All Documentation (Projects + Master)"
echo ""

cd technical-docs

# Use the Makefile which handles building projects + master + copying
make html SPHINXBUILD="$SPHINX_BUILD" 2>&1 | tee build.log

# Check for errors/warnings (treat intersphinx inventory fetch warnings as informational)
ERRORS_ALL="$(grep -E 'ERROR:' build.log || true)"
WARNINGS_ALL="$(grep -E 'WARNING:' build.log || true)"
WARNINGS_NON_IGNORED="$(echo "$WARNINGS_ALL" | grep -viE 'failed to reach any of the inventories|intersphinx inventory' || true)"

if [ -n "$ERRORS_ALL" ]; then
    echo ""
    echo "❌ Build completed with errors:"
    echo ""
    echo "$ERRORS_ALL"
    echo ""
    WARNINGS="true"
elif [ -n "$WARNINGS_NON_IGNORED" ]; then
    echo ""
    echo "⚠️  Build completed with warnings:"
    echo ""
    echo "$WARNINGS_NON_IGNORED"
    echo ""
    WARNINGS="true"
elif [ -n "$WARNINGS_ALL" ]; then
    echo ""
    echo "ℹ️  Build produced intersphinx inventory warnings (ignored for local runs):"
    echo ""
    echo "$WARNINGS_ALL"
    echo ""
    WARNINGS="false"
else
    echo "✓ Build completed with no warnings"
    WARNINGS="false"
fi

# Verify project docs were copied
echo ""
echo "## Verifying Project Documentation"
echo ""

for project in whisper deploy transfer; do
    if [ ! -f build/html/$project/index.html ]; then
        echo "❌ ERROR: $project docs not found in master build"
        exit 1
    fi
    echo "✓ $project documentation present"
done

# Verify cross-references
echo ""
echo "## Verifying Cross-References"
echo ""

cd build/html

for project in whisper deploy transfer; do
    if grep -r "$project" . >/dev/null 2>&1; then
        echo "✓ $project references found"
    else
        echo "⚠️  No references to $project found"
    fi
done

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
    echo "Build output: technical-docs/build/html/index.html"
    exit 1
else
    echo "✅ CI test passed successfully!"
    echo ""
    echo "All checks passed. The build is ready for CI/CD."
    echo ""
    echo "Build output: technical-docs/build/html/index.html"
    echo ""
    echo "To view the documentation:"
    echo "  open technical-docs/build/html/index.html"
fi
