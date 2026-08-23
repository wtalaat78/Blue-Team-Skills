#!/usr/bin/env bash
# =============================================================================
# Blue-Team-Skills - Universal Installer (Linux, macOS, WSL)
# =============================================================================
# Installs AppSec skill configurations across supported AI agent platforms:
#   - Google Antigravity (~/.gemini/config/skills/)
#   - Claude Code (~/.claude/ or repo CLAUDE.md)
#   - Cursor IDE (.cursorrules & .cursor/rules/)
#   - Windsurf / Cascade (.windsurfrules)
#   - GitHub Copilot (.github/copilot-instructions.md)
#   - Generic Agents (AGENTS.md & .agents/skills/)
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=================================================="
echo "  Blue-Team-Skills Universal Installer"
echo "  Repository Root: $REPO_ROOT"
echo "=================================================="

# 1. Google Antigravity Setup
GEMINI_SKILLS_DIR="$HOME/.gemini/config/skills"
mkdir -p "$GEMINI_SKILLS_DIR/internal-appsec-testing"
mkdir -p "$GEMINI_SKILLS_DIR/appsec"

cp "$REPO_ROOT/skills/internal-appsec-testing/SKILL.md" "$GEMINI_SKILLS_DIR/internal-appsec-testing/SKILL.md"
cp "$REPO_ROOT/skills/appsec/SKILL.md" "$GEMINI_SKILLS_DIR/appsec/SKILL.md"
echo "  [OK] Antigravity skills installed to $GEMINI_SKILLS_DIR"

# 2. Project-level Agent Discovery
PROJECT_AGENTS_DIR="$REPO_ROOT/.agents/skills"
mkdir -p "$PROJECT_AGENTS_DIR/internal-appsec-testing"
mkdir -p "$PROJECT_AGENTS_DIR/appsec"

cp "$REPO_ROOT/skills/internal-appsec-testing/SKILL.md" "$PROJECT_AGENTS_DIR/internal-appsec-testing/SKILL.md"
cp "$REPO_ROOT/skills/appsec/SKILL.md" "$PROJECT_AGENTS_DIR/appsec/SKILL.md"
echo "  [OK] Project-level .agents/ skills synced"

# 3. Claude Code Global Config (if ~/.claude exists)
if [ -d "$HOME/.claude" ]; then
    cp "$REPO_ROOT/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
    echo "  [OK] Claude Code global configuration updated (~/.claude/CLAUDE.md)"
fi

# 4. Git Post-Merge Hook for Auto-Updates
HOOK_DIR="$REPO_ROOT/.git/hooks"
if [ -d "$HOOK_DIR" ]; then
    cat << 'EOF' > "$HOOK_DIR/post-merge"
#!/usr/bin/env bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
if [ -f "$REPO_ROOT/scripts/update.sh" ]; then
    bash "$REPO_ROOT/scripts/update.sh" --skip-pull
fi
EOF
    chmod +x "$HOOK_DIR/post-merge"
    echo "  [OK] Git post-merge auto-update hook installed"
fi

# 5. Make scripts executable
chmod +x "$REPO_ROOT/scripts/"*.sh 2>/dev/null || true
chmod +x "$REPO_ROOT/scripts/"*.py 2>/dev/null || true

echo ""
echo "=================================================="
echo "  Installation Complete!"
echo "  Supported Agents:"
echo "    - Google Antigravity : /appsec"
echo "    - Claude Code        : CLAUDE.md active"
echo "    - Cursor IDE         : .cursorrules & .cursor/rules/ active"
echo "    - Windsurf / Cascade : .windsurfrules active"
echo "    - GitHub Copilot     : .github/copilot-instructions.md active"
echo "    - Generic Agents     : AGENTS.md active"
echo "=================================================="
