#!/bin/bash
# scripts/deploy-release.sh
# Usage: ./deploy-release.sh project-1 v1.0.0

set -e

PROJECT=$1
VERSION=$2

if [ -z "$PROJECT" ] || [ -z "$VERSION" ]; then
    echo "Usage: $0 <project-name> <version>"
    echo "Example: $0 project-1 v1.0.0"
    exit 1
fi

echo "Deploying ${PROJECT} ${VERSION} documentation..."

cd technical-docs/${PROJECT}-docs
git fetch --tags
git checkout $VERSION

cd ../..
git add technical-docs
git commit -m "Release ${PROJECT} ${VERSION} documentation"
git push

echo "✓ Deployment triggered for ${PROJECT} ${VERSION}"
echo "  Production: https://cleanroomlabs.dev/docs/${PROJECT}/"
echo "  Monitor: https://vercel.com/cleanroom/website"
