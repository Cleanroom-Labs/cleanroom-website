#!/bin/bash
# scripts/add-new-project.sh
# Usage: ./add-new-project.sh project-4 git@github.com:cleanroom/project-4-docs.git

set -e

PROJECT=$1
DOCS_REPO=$2

if [ -z "$PROJECT" ] || [ -z "$DOCS_REPO" ]; then
    echo "Usage: $0 <project-name> <docs-repo-url>"
    echo "Example: $0 project-4 git@github.com:cleanroom/project-4-docs.git"
    exit 1
fi

echo "Adding new project: ${PROJECT}..."

# Navigate to technical docs
cd cleanroom-technical-docs

# Add as submodule
git submodule add $DOCS_REPO ${PROJECT}-docs

# Initialize and update
git submodule update --init --recursive

# Commit
git add .gitmodules ${PROJECT}-docs
git commit -m "Add ${PROJECT} documentation as submodule"

# Return to website root
cd ..

# Commit technical-docs update
git add cleanroom-technical-docs
git commit -m "Add ${PROJECT} to technical documentation"

echo "✓ Project added successfully"
echo ""
echo "Next steps:"
echo "  1. Update cleanroom-technical-docs/source/index.rst to include ${PROJECT}"
echo "  2. Configure intersphinx in ${PROJECT}-docs/source/conf.py"
echo "  3. Test build: npm run build-docs"
echo "  4. Push changes: git push --recurse-submodules=on-demand"
