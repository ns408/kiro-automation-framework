#!/bin/bash
# Wrapper script for executing action scripts with logging

set -e

SCRIPT="$1"
LOG=".dev/logs/actions.log"
TIMESTAMP=$(date -Iseconds)

if [ -z "$SCRIPT" ]; then
    echo "Usage: ./run-action.sh <action-script>"
    echo ""
    echo "Available actions:"
    ls -1 .dev/actions/*.sh 2>/dev/null || echo "  (none yet)"
    exit 1
fi

if [ ! -f "$SCRIPT" ]; then
    echo "Error: Script not found: $SCRIPT"
    exit 1
fi

mkdir -p .dev/logs

echo "$TIMESTAMP | ACTION: $(basename $SCRIPT .sh)" >> "$LOG"
echo "$TIMESTAMP | EXECUTING: $SCRIPT" >> "$LOG"

if bash "$SCRIPT" 2>&1 | tee -a "$LOG"; then
    echo "$TIMESTAMP | STATUS: ✅ Complete" >> "$LOG"
else
    echo "$TIMESTAMP | STATUS: ❌ Failed" >> "$LOG"
    exit 1
fi

echo "---" >> "$LOG"
