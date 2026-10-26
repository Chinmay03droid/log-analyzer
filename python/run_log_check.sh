#!/bin/bash

LOG_FILE="${1:-sample.log}"

OUTPUT=$(docker run --rm -v "$PWD:/app" log-analyzer "$LOG_FILE" --json 2>/dev/null)
STATUS=$?

if [ "$STATUS" -ne 0 ] && [ "$STATUS" -ne 2 ]; then
    echo "ERROR: Docker or analyzer execution failed (exit code: $STATUS)"
    exit 1
fi

if ! printf '%s\n' "$OUTPUT" | jq -e 'type == "object"' >/dev/null 2>&1; then
    echo "ERROR: Analyzer did not produce valid JSON:"
    printf '%s\n' "$OUTPUT"
    exit 1
fi

ERRORS=$(printf '%s\n' "$OUTPUT" | jq -r '.ERROR // 0')
WARNS=$(printf '%s\n' "$OUTPUT" | jq -r '.WARN // 0')

if [ "$ERRORS" -gt 0 ]; then
    echo "Pipeline FAILED: ERROR count = $ERRORS"
    exit 1
fi

if [ "$WARNS" -gt 5 ]; then
    echo "Pipeline WARNING: WARN count = $WARNS"
    exit 0
fi

echo "Pipeline PASSED: logs are healthy."
exit 0
