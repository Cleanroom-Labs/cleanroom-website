#!/bin/bash
# scripts/check-submodules.sh
# Verifies all submodules are correctly configured and not in detached HEAD

set -e

echo "Checking submodule health..."
echo ""

# Check technical-docs submodule
cd cleanroom-technical-docs

# Check if on a branch or tag
CURRENT=$(git describe --exact-match --tags 2>/dev/null || git branch --show-current)
if [ -z "$CURRENT" ]; then
    echo "⚠️  technical-docs is in detached HEAD state"
    echo "    Current commit: $(git rev-parse --short HEAD)"
else
    echo "✓ technical-docs is on: $CURRENT"
fi

# Check each project submodule
for PROJECT_DIR in */; do
    if [ -d "$PROJECT_DIR/.git" ] || [ -f "$PROJECT_DIR/.git" ]; then
        PROJECT=${PROJECT_DIR%/}
        cd $PROJECT_DIR

        CURRENT=$(git describe --exact-match --tags 2>/dev/null || git branch --show-current)
        if [ -z "$CURRENT" ]; then
            echo "⚠️  ${PROJECT} is in detached HEAD state"
            echo "    Current commit: $(git rev-parse --short HEAD)"
        else
            echo "✓ ${PROJECT} is on: $CURRENT"
        fi

        cd ..
    fi
done

echo ""
echo "Submodule status:"
git submodule status

echo ""
echo "To fix detached HEAD state:"
echo "  cd cleanroom-technical-docs/<project>-docs"
echo "  git checkout <branch-or-tag>"
echo "  cd ../.."
echo "  git add cleanroom-technical-docs"
echo "  git commit -m \"Update submodule reference\""
