#!/bin/bash
#
# Claude Code Template — Quick Setup Script
#
# Usage:
#   ./setup.sh /path/to/your-project "My Project Name"
#   ./setup.sh .                     "My Project Name"   (current directory)
#
# What it does:
#   1. Copies .claude/ directory and CLAUDE.md to target project
#   2. Replaces {PROJECT_NAME} with your project name
#   3. Creates agent-memory directories
#   4. Makes scripts executable
#   5. Adds recommended .gitignore entries
#

set -e

# ── Args ──
TARGET="${1:-.}"
PROJECT_NAME="${2:-My Project}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ ! -d "$TARGET" ]; then
  echo "Error: Target directory '$TARGET' does not exist."
  echo "Usage: ./setup.sh /path/to/your-project \"Project Name\""
  exit 1
fi

TARGET="$(cd "$TARGET" && pwd)"
echo ""
echo "  ⚡ Claude Code Template Setup"
echo "  ────────────────────────────────"
echo "  Target:  $TARGET"
echo "  Project: $PROJECT_NAME"
echo ""

# ── Check for existing .claude ──
if [ -d "$TARGET/.claude" ]; then
  echo "  ⚠  $TARGET/.claude already exists."
  read -p "  Overwrite? (y/N) " confirm
  if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "  Aborted."
    exit 0
  fi
fi

# ── Copy files ──
echo "  [1/7] Copying .claude/ directory..."
cp -r "$SCRIPT_DIR/.claude" "$TARGET/.claude"

echo "  [2/7] Copying CLAUDE.md + example..."
cp "$SCRIPT_DIR/CLAUDE.md" "$TARGET/CLAUDE.md"
cp "$SCRIPT_DIR/CLAUDE.example.md" "$TARGET/CLAUDE.example.md"

# ── Replace placeholders ──
echo "  [3/7] Replacing {PROJECT_NAME} → '$PROJECT_NAME'..."
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS sed requires '' after -i
  sed -i '' "s/{PROJECT_NAME}/$PROJECT_NAME/g" "$TARGET/CLAUDE.md"
else
  sed -i "s/{PROJECT_NAME}/$PROJECT_NAME/g" "$TARGET/CLAUDE.md"
fi

# ── Create agent-memory dirs ──
echo "  [4/7] Creating agent-memory directories..."
mkdir -p "$TARGET/.claude/agent-memory"

# ── Make scripts executable ──
echo "  [5/7] Making scripts executable..."
chmod +x "$TARGET/.claude/watch-agents.sh" 2>/dev/null || true
chmod +x "$TARGET/.claude/watch-agents-ui.js" 2>/dev/null || true

# ── Add .gitignore entries ──
echo "  [6/7] Adding .gitignore entries..."
GITIGNORE="$TARGET/.gitignore"
ENTRIES=(
  "# Claude Code runtime files"
  ".claude/agent-activity.log"
  ".claude/agent-activity.jsonl"
  ".claude/.agent-timers/"
  ".claude/.session-pushed"
  ".claude/.lead-last-log"
  ".claude/.hook-errors.log"
)

if [ -f "$GITIGNORE" ]; then
  # Only add entries that don't already exist
  for entry in "${ENTRIES[@]}"; do
    if ! grep -qF "$entry" "$GITIGNORE" 2>/dev/null; then
      echo "$entry" >> "$GITIGNORE"
    fi
  done
else
  printf '%s\n' "${ENTRIES[@]}" > "$GITIGNORE"
fi

echo ""
echo "  ✅ Setup complete!"
echo ""
echo "  Next steps:"
echo "  ────────────────────────────────"
echo "  1. Open CLAUDE.md and fill in the <!-- CUSTOMIZE --> sections"
echo "     (see CLAUDE.example.md for a fully filled-in reference)"
echo "  2. Edit .claude/languages.json — set your project's languages"
echo "  3. Create domain agents:"
echo "     cp .claude/agents/_template-domain.md .claude/agents/backend.md"
echo "     cp .claude/agents/_template-domain.md .claude/agents/frontend.md"
echo "  4. Edit each agent file with your project's scope and patterns"
echo "  5. Add project-specific permissions to .claude/settings.local.json"
echo "  6. Start Claude Code and test: /status-check"
echo "  7. Launch the dashboard: node .claude/watch-agents-ui.js"
echo ""
