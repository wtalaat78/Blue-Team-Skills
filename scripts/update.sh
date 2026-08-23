#!/usr/bin/env bash
# =============================================================================
# Blue-Team-Skills - Universal Updater (Linux, macOS, WSL)
# =============================================================================
# Pulls latest updates from GitHub and synchronizes all skill files.
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

SKIP_PULL=false
if [ "$1" == "--skip-pull" ] || [ "$1" == "-s" ]; then
    SKIP_PULL=true
fi

echo "  Blue-Team-Skills Universal Update"
echo "  Repository: $REPO_ROOT"

# Step 1: Git Pull
if [ "$SKIP_PULL" = false ]; then
    echo "  Pulling latest from GitHub..."
    if git -C "$REPO_ROOT" pull origin main; then
        echo "  [OK] Git repository up to date"
    else
        echo "  [WARN] Git pull failed or offline — syncing local files"
    fi
fi

# Step 2: Sync Antigravity Global Skills
GEMINI_SKILLS_DIR="$HOME/.gemini/config/skills"
if [ -d "$GEMINI_SKILLS_DIR" ] || [ -d "$HOME/.gemini" ]; then
    mkdir -p "$GEMINI_SKILLS_DIR/internal-appsec-testing"
    mkdir -p "$GEMINI_SKILLS_DIR/appsec"
    cp "$REPO_ROOT/skills/internal-appsec-testing/SKILL.md" "$GEMINI_SKILLS_DIR/internal-appsec-testing/SKILL.md"
    cp "$REPO_ROOT/skills/appsec/SKILL.md" "$GEMINI_SKILLS_DIR/appsec/SKILL.md"
    echo "  [OK] Antigravity skills updated"
fi

# Step 3: Sync Project-level .agents
mkdir -p "$REPO_ROOT/.agents/skills/internal-appsec-testing"
mkdir -p "$REPO_ROOT/.agents/skills/appsec"
cp "$REPO_ROOT/skills/internal-appsec-testing/SKILL.md" "$REPO_ROOT/.agents/skills/internal-appsec-testing/SKILL.md"
cp "$REPO_ROOT/skills/appsec/SKILL.md" "$REPO_ROOT/.agents/skills/appsec/SKILL.md"
echo "  [OK] Project-level .agents/ updated"

# Step 4: Sync Claude Code Global (if exists)
if [ -d "$HOME/.claude" ]; then
    cp "$REPO_ROOT/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
    echo "  [OK] ~/.claude/CLAUDE.md updated"
fi

# Step 5: Refresh CVE Library (if python is available)
if command -v python3 &> /dev/null; then
    python3 "$REPO_ROOT/scripts/update_cve_library.py" || true
elif command -v python &> /dev/null; then
    python "$REPO_ROOT/scripts/update_cve_library.py" || true
fi

COMMIT_HASH="$(git -C "$REPO_ROOT" rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
echo "  [OK] Blue-Team-Skills updated to commit: $COMMIT_HASH"
