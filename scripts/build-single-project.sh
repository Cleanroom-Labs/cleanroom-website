#!/bin/bash
# scripts/build-single-project.sh
# Usage: ./build-single-project.sh project-1

set -e

PROJECT=$1

if [ -z "$PROJECT" ]; then
    echo "Usage: $0 <project-name>"
    echo "Example: $0 project-1"
    exit 1
fi

echo "Building ${PROJECT} documentation..."

cd technical-docs/${PROJECT}-docs

# Create venv if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

# Activate venv and install dependencies
source .venv/bin/activate
pip install -r requirements.txt

# Build docs
sphinx-build -M html source build

echo ""
echo "✓ Build complete!"
echo "  Open: $(pwd)/build/html/index.html"

# Optionally open in browser
if command -v open &> /dev/null; then
    open build/html/index.html
elif command -v xdg-open &> /dev/null; then
    xdg-open build/html/index.html
fi
