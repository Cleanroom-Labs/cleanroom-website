#!/bin/bash
# scripts/update-project-docs.sh
# Usage: ./update-project-docs.sh project-1 v1.2.0

set -e

PROJECT=$1
VERSION=$2

if [ -z "$PROJECT" ] || [ -z "$VERSION" ]; then
    echo "Usage: $0 <project-name> <version>"
    echo "Example: $0 project-1 v1.2.0"
    exit 1
fi

echo "Updating ${PROJECT} documentation to ${VERSION}..."

# Navigate to technical docs
cd cleanroom-technical-docs

# Navigate to project submodule
cd ${PROJECT}-docs

# Fetch latest tags
git fetch --tags

# Checkout specific version
git checkout $VERSION

# Return to technical docs
cd ..

# Commit the submodule update
git add ${PROJECT}-docs
git commit -m "Update ${PROJECT} docs to ${VERSION}"

# Return to website root
cd ..

# Commit the technical-docs update
git add cleanroom-technical-docs
git commit -m "Update technical docs (${PROJECT} ${VERSION})"

echo "✓ Submodules updated successfully"
echo ""
echo "Next steps:"
echo "  1. Review changes: git log -2"
echo "  2. Push to trigger deployment: git push"
echo "  3. Monitor build: https://vercel.com/cleanroom/website"
