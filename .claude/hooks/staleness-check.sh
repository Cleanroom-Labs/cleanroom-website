#!/bin/bash
# Post-edit hook: check staleness after design token or CSS edits
set -euo pipefail

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null || echo "")

# Only run for token or CSS files under common/
case "$FILE_PATH" in
  */common/tokens/*|*/common/css/*)
    cd "$(dirname "$0")/../../common" && npm run check-staleness 2>&1 | tail -5
    ;;
esac
