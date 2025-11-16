#!/bin/bash
# Clean old log files

set -e

# Default: keep logs from last 7 days
DAYS=${1:-7}

echo "=== Cleaning Log Files ==="
echo "Keeping logs from last $DAYS days..."
echo ""

if [ ! -d "logs" ]; then
    echo "No logs directory found."
    exit 0
fi

# Count sessions before cleanup
BEFORE=$(find logs -maxdepth 1 -type d -name "session_*" | wc -l)

# Find and delete old session directories
# Files older than DAYS days
find logs -maxdepth 1 -type d -name "session_*" -mtime +$DAYS -exec rm -rf {} \;

# Count sessions after cleanup
AFTER=$(find logs -maxdepth 1 -type d -name "session_*" | wc -l)
DELETED=$((BEFORE - AFTER))

echo "✓ Cleanup complete"
echo "  Sessions before: $BEFORE"
echo "  Sessions after:  $AFTER"
echo "  Deleted:         $DELETED"
echo ""

# Show disk usage
if [ -d "logs" ]; then
    USAGE=$(du -sh logs | cut -f1)
    echo "Current logs directory size: $USAGE"
fi
