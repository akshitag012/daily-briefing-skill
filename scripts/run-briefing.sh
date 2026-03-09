#!/bin/bash
# Wrapper script for automated daily briefing via LaunchAgent/cron
# Reads SKILL.md and passes it directly to Claude as a prompt
# (Claude can't discover custom skills in headless mode)

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_FILE="$SKILL_DIR/SKILL.md"

if [ ! -f "$SKILL_FILE" ]; then
    echo "ERROR: SKILL.md not found at $SKILL_FILE"
    exit 1
fi

SKILL_CONTENT=$(cat "$SKILL_FILE")

/opt/homebrew/bin/claude -p "Execute the following skill instructions now. Today's date is $(date '+%B %d, %Y').

$SKILL_CONTENT" \
    --allowedTools "mcp__claude_ai_Gmail__*,WebSearch,WebFetch,Bash,Read,Write,Glob,Grep,Task"
