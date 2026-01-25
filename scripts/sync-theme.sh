#!/bin/bash
# scripts/sync-theme.sh
# Synchronizes cleanroom-theme submodule across all locations
#
# Usage:
#   ./scripts/sync-theme.sh           # Sync to latest main from standalone repo
#   ./scripts/sync-theme.sh abc1234   # Sync to specific commit
#   ./scripts/sync-theme.sh --dry-run # Show what would happen

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Validate execution context
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

if [[ ! -f "$REPO_ROOT/scripts/build-docs.mjs" ]]; then
    echo -e "${RED}Error: Must run from cleanroom-website repository${NC}"
    echo "Current directory: $(pwd)"
    exit 1
fi

cd "$REPO_ROOT"

# Parse arguments
DRY_RUN=false
TARGET_COMMIT=""

for arg in "$@"; do
    case $arg in
        --dry-run)
            DRY_RUN=true
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS] [COMMIT]"
            echo ""
            echo "Synchronizes cleanroom-theme submodule to all locations."
            echo ""
            echo "Arguments:"
            echo "  COMMIT     Target commit SHA (defaults to latest main from standalone repo)"
            echo ""
            echo "Options:"
            echo "  --dry-run  Show what would happen without making changes"
            echo "  -h, --help Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                    # Sync to latest main"
            echo "  $0 abc1234            # Sync to specific commit"
            echo "  $0 --dry-run          # Preview changes"
            exit 0
            ;;
        *)
            if [[ -z "$TARGET_COMMIT" && ! "$arg" =~ ^- ]]; then
                TARGET_COMMIT="$arg"
            fi
            ;;
    esac
done

# Standalone theme repo location
STANDALONE_REPO="/Users/andfranklin/Projects/cleanroom-theme"

# Get target commit
if [[ -z "$TARGET_COMMIT" ]]; then
    if [[ ! -d "$STANDALONE_REPO" ]]; then
        echo -e "${RED}Error: Standalone theme repo not found at $STANDALONE_REPO${NC}"
        echo "Please specify a commit SHA explicitly."
        exit 1
    fi
    echo -e "${BLUE}Getting latest from standalone theme repo...${NC}"
    # Try to fetch from origin if available, otherwise use local main
    cd "$STANDALONE_REPO"
    if git remote get-url origin &>/dev/null; then
        git fetch origin main --quiet 2>/dev/null || true
        TARGET_COMMIT=$(git rev-parse origin/main 2>/dev/null || git rev-parse main)
    else
        TARGET_COMMIT=$(git rev-parse main)
    fi
    cd "$REPO_ROOT"
fi

# Validate commit format (basic check)
if [[ ! "$TARGET_COMMIT" =~ ^[a-f0-9]{7,40}$ ]]; then
    echo -e "${RED}Error: Invalid commit SHA: $TARGET_COMMIT${NC}"
    exit 1
fi

echo -e "${BLUE}Target theme commit: ${GREEN}$TARGET_COMMIT${NC}"
echo ""

# Find all cleanroom-theme submodules by searching .gitmodules files
find_theme_submodules() {
    local search_dir="$1"
    local results=()

    # Find all .gitmodules files
    while IFS= read -r gitmodules; do
        local repo_dir="$(dirname "$gitmodules")"
        # Extract paths where submodule URL contains "cleanroom-theme"
        while IFS= read -r subpath; do
            if [[ -n "$subpath" ]]; then
                results+=("$repo_dir/$subpath")
            fi
        done < <(grep -A2 'cleanroom-theme' "$gitmodules" 2>/dev/null | \
            grep 'path' | \
            sed 's/.*path = //')
    done < <(find "$search_dir" -name ".gitmodules" -type f 2>/dev/null)

    printf '%s\n' "${results[@]}"
}

# Discover all theme submodule locations
echo -e "${BLUE}Discovering theme submodule locations...${NC}"
SUBMODULE_PATHS=()
while IFS= read -r path; do
    [[ -n "$path" ]] && SUBMODULE_PATHS+=("$path")
done < <(find_theme_submodules "$REPO_ROOT")

if [[ ${#SUBMODULE_PATHS[@]} -eq 0 ]]; then
    echo -e "${RED}Error: No theme submodules found${NC}"
    exit 1
fi

echo -e "Found ${GREEN}${#SUBMODULE_PATHS[@]}${NC} theme submodule locations:"
for path in "${SUBMODULE_PATHS[@]}"; do
    # Show relative path from repo root
    rel_path="${path#$REPO_ROOT/}"
    echo "  - $rel_path"
done
echo ""

# Check current state of each submodule
echo -e "${BLUE}Current submodule states:${NC}"
for path in "${SUBMODULE_PATHS[@]}"; do
    rel_path="${path#$REPO_ROOT/}"
    if [[ -d "$path/.git" ]] || [[ -f "$path/.git" ]]; then
        current=$(cd "$path" && git rev-parse HEAD 2>/dev/null || echo "unknown")
        current_short="${current:0:7}"
        target_short="${TARGET_COMMIT:0:7}"
        if [[ "$current" == "$TARGET_COMMIT" || "$current_short" == "$target_short" ]]; then
            echo -e "  ${GREEN}✓${NC} $rel_path (already at $current_short)"
        else
            echo -e "  ${YELLOW}→${NC} $rel_path ($current_short → $target_short)"
        fi
    else
        echo -e "  ${RED}?${NC} $rel_path (not initialized)"
    fi
done
echo ""

if $DRY_RUN; then
    echo -e "${YELLOW}Dry run mode - no changes made${NC}"
    exit 0
fi

# Update each submodule to target commit
echo -e "${BLUE}Updating submodules...${NC}"
UPDATED_PATHS=()
for path in "${SUBMODULE_PATHS[@]}"; do
    rel_path="${path#$REPO_ROOT/}"
    if [[ -d "$path/.git" ]] || [[ -f "$path/.git" ]]; then
        current=$(cd "$path" && git rev-parse HEAD 2>/dev/null)
        if [[ "$current" != "$TARGET_COMMIT" ]]; then
            echo "  Updating $rel_path..."
            (cd "$path" && git fetch --all --quiet 2>/dev/null && git checkout "$TARGET_COMMIT" --quiet)
            UPDATED_PATHS+=("$path")
        fi
    fi
done

if [[ ${#UPDATED_PATHS[@]} -eq 0 ]]; then
    echo -e "${GREEN}All submodules already at target commit. Nothing to do.${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}Committing changes bottom-up through hierarchy...${NC}"

# Helper to commit submodule updates in a parent repo
commit_submodule_update() {
    local parent_dir="$1"
    local submodule_rel_path="$2"
    local commit_msg="$3"

    cd "$parent_dir"
    if git diff --quiet "$submodule_rel_path" 2>/dev/null; then
        return 0  # No changes to commit
    fi

    git add "$submodule_rel_path"
    git commit -m "$commit_msg" --quiet
    echo -e "  ${GREEN}✓${NC} Committed in $(basename "$parent_dir"): $commit_msg"
    return 0
}

# Sort paths by depth (deepest first for bottom-up commits)
# This ensures project-docs are committed before technical-docs
IFS=$'\n' SORTED_PATHS=($(printf '%s\n' "${UPDATED_PATHS[@]}" | awk -F/ '{print NF-1, $0}' | sort -rn | cut -d' ' -f2-))

# Track which parent repos need commits (bash 3-compatible parallel arrays)
PARENT_DIRS=()
PARENT_SUBPATHS=()

for path in "${SORTED_PATHS[@]}"; do
    parent_dir="$(dirname "$path")"
    submodule_name="$(basename "$path")"

    # For theme in source/, the parent is the repo containing source/
    if [[ "$submodule_name" == "cleanroom-theme" && "$(basename "$parent_dir")" == "source" ]]; then
        parent_dir="$(dirname "$parent_dir")"
        submodule_rel_path="source/cleanroom-theme"
    else
        submodule_rel_path="$submodule_name"
    fi

    PARENT_DIRS+=("$parent_dir")
    PARENT_SUBPATHS+=("$submodule_rel_path")
done

# Commit in each parent (SORTED_PATHS is already sorted deepest-first)
for i in "${!PARENT_DIRS[@]}"; do
    parent_dir="${PARENT_DIRS[$i]}"
    submodule_rel_path="${PARENT_SUBPATHS[$i]}"
    commit_submodule_update "$parent_dir" "$submodule_rel_path" "chore: update theme submodule"
done

# Now commit project-docs updates in technical-docs if any project-docs were updated
TECH_DOCS="$REPO_ROOT/cleanroom-technical-docs"
cd "$TECH_DOCS"

for project_dir in cleanroom-whisper-docs airgap-deploy-docs airgap-transfer-docs; do
    if [[ -d "$project_dir" ]] && ! git diff --quiet "$project_dir" 2>/dev/null; then
        git add "$project_dir"
    fi
done

if ! git diff --cached --quiet 2>/dev/null; then
    git commit -m "chore: update project-docs submodules (theme sync)" --quiet
    echo -e "  ${GREEN}✓${NC} Committed in technical-docs: project-docs updates"
fi

# Commit technical-docs update in website
cd "$REPO_ROOT"
if ! git diff --quiet cleanroom-technical-docs 2>/dev/null; then
    git add cleanroom-technical-docs
    git commit -m "chore: update technical-docs submodule (theme sync)" --quiet
    echo -e "  ${GREEN}✓${NC} Committed in website: technical-docs update"
fi

# Commit direct theme update in website if present
if ! git diff --quiet cleanroom-theme 2>/dev/null; then
    git add cleanroom-theme
    git commit -m "chore: update theme submodule" --quiet
    echo -e "  ${GREEN}✓${NC} Committed in website: direct theme update"
fi

echo ""
echo -e "${GREEN}✓ Theme sync complete!${NC}"
echo ""
echo -e "${BLUE}Summary:${NC}"
echo "  Target commit: ${TARGET_COMMIT:0:7}"
echo "  Submodules updated: ${#UPDATED_PATHS[@]}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Verify: ./scripts/check-submodules.sh"
echo "  2. Build:  node scripts/build-docs.mjs"
echo "  3. Push:   git push (and push each modified repo)"

