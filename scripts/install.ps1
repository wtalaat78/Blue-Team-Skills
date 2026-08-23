# =============================================================================
# Blue-Team-Skills - Install Script
# =============================================================================
# Run this ONCE to install the AppSec skill globally on your machine.
# After this, run update.ps1 (or let the scheduled task handle it) to get
# new versions automatically.
#
# Usage:
#   .\scripts\install.ps1
#
# What this does:
#   1. Checks that this is a valid Blue-Team-Skills repository
#   2. Installs the skill to ~/.gemini/config/skills/ (global AGY install)
#   3. Sets up a Git post-merge hook so "git pull" auto-syncs the skill
#   4. Optionally registers a Windows Scheduled Task for daily auto-update
#
# Requirements: PowerShell 5.1+, Git
# =============================================================================

param(
    [switch]$SkipScheduledTask,
    [switch]$Quiet
)

$ErrorActionPreference = "Stop"

# -- Helpers ------------------------------------------------------------------

function Write-Header($text) {
    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "  $text" -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan
}

function Write-OK($text)   { Write-Host "  [OK]  $text" -ForegroundColor Green }
function Write-WARN($text) { Write-Host "  [!!]  $text" -ForegroundColor Yellow }
function Write-ERR($text)  { Write-Host "  [XX]  $text" -ForegroundColor Red }
function Write-INFO($text) { Write-Host "  [**]  $text" -ForegroundColor White }

# -- Locate repository root ---------------------------------------------------

$RepoRoot = Split-Path -Parent $PSScriptRoot

if (-not (Test-Path "$RepoRoot\skills\internal-appsec-testing\SKILL.md")) {
    Write-ERR "Cannot find SKILL.md - are you running this from the Blue-Team-Skills repo?"
    exit 1
}

Write-Header "Blue-Team-Skills Installer"
Write-INFO "Repository root: $RepoRoot"

# -- Define paths -------------------------------------------------------------

$GlobalSkillsDir = "$env:USERPROFILE\.gemini\config\skills"
$SkillDest       = "$GlobalSkillsDir\internal-appsec-testing"
$AppsecDest      = "$GlobalSkillsDir\appsec"
$SkillSrc        = "$RepoRoot\skills\internal-appsec-testing"
$AppsecSrc       = "$RepoRoot\skills\appsec"
$HookDir         = "$RepoRoot\.git\hooks"
$HookFile        = "$HookDir\post-merge"

# -- Step 1: Create global skill directories -----------------------------------

Write-Header "Step 1 of 4 - Installing skill to global AGY config"

@($SkillDest, $AppsecDest) | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
        Write-OK "Created: $_"
    }
}

# Copy SKILL.md files
Copy-Item "$SkillSrc\SKILL.md" "$SkillDest\SKILL.md" -Force
Write-OK "Installed: $SkillDest\SKILL.md"

Copy-Item "$AppsecSrc\SKILL.md" "$AppsecDest\SKILL.md" -Force
Write-OK "Installed: $AppsecDest\SKILL.md"

# Also sync to Claude Code if ~/.claude directory exists
$ClaudeDir = "$env:USERPROFILE\.claude"
if (Test-Path $ClaudeDir) {
    Copy-Item "$RepoRoot\CLAUDE.md" "$ClaudeDir\CLAUDE.md" -Force
    Write-OK "Installed Claude Code config: $ClaudeDir\CLAUDE.md"
}

# -- Step 2: Install Git post-merge hook ---------------------------------------

Write-Header "Step 2 of 4 - Installing Git post-merge hook"

if (-not (Test-Path $HookDir)) {
    Write-WARN "No .git/hooks directory found - skipping hook (not a git repo?)"
} else {
    $HookContent = @"
#!/bin/sh
# Blue-Team-Skills: auto-sync skill after git pull
# Installed by scripts/install.ps1

REPO_ROOT="`$(git rev-parse --show-toplevel)"
GLOBAL_DIR="`$HOME/.gemini/config/skills"

# Sync internal-appsec-testing skill
if [ -f "`$REPO_ROOT/skills/internal-appsec-testing/SKILL.md" ]; then
    mkdir -p "`$GLOBAL_DIR/internal-appsec-testing"
    cp "`$REPO_ROOT/skills/internal-appsec-testing/SKILL.md" "`$GLOBAL_DIR/internal-appsec-testing/SKILL.md"
    echo "[Blue-Team-Skills] internal-appsec-testing skill updated."
fi

# Sync appsec shortcut
if [ -f "`$REPO_ROOT/skills/appsec/SKILL.md" ]; then
    mkdir -p "`$GLOBAL_DIR/appsec"
    cp "`$REPO_ROOT/skills/appsec/SKILL.md" "`$GLOBAL_DIR/appsec/SKILL.md"
    echo "[Blue-Team-Skills] appsec shortcut updated."
fi
"@

    Set-Content -Path $HookFile -Value $HookContent -Encoding UTF8
    Write-OK "Git post-merge hook installed at: $HookFile"
    Write-INFO "The skill will now auto-sync every time you run 'git pull'."
}

# -- Step 3: Write version stamp -----------------------------------------------

Write-Header "Step 3 of 4 - Recording install metadata"

$InstallMeta = @{
    installed_by     = $env:USERNAME
    installed_at     = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
    repo_root        = $RepoRoot
    global_skill_dir = $GlobalSkillsDir
    git_commit       = (git -C $RepoRoot rev-parse --short HEAD 2>$null)
} | ConvertTo-Json -Depth 2

$MetaFile = "$RepoRoot\.skill-install.json"
Set-Content -Path $MetaFile -Value $InstallMeta -Encoding UTF8
Write-OK "Install metadata saved: $MetaFile"

# -- Step 4: Optional Scheduled Task -------------------------------------------

Write-Header "Step 4 of 4 - Windows Scheduled Task (daily auto-update)"

if ($SkipScheduledTask) {
    Write-WARN "Skipping scheduled task setup (-SkipScheduledTask flag set)."
    Write-INFO "To update manually anytime, run: .\scripts\update.ps1"
} else {

    $TaskName    = "BlueTeamSkills-DailyUpdate"
    $UpdateScript = "$RepoRoot\scripts\update.ps1"
    $TaskExists  = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

    if ($TaskExists) {
        Write-WARN "Scheduled task '$TaskName' already exists - skipping creation."
    } else {
        try {
            $Action  = New-ScheduledTaskAction `
                -Execute "powershell.exe" `
                -Argument "-NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$UpdateScript`""

            $Trigger = New-ScheduledTaskTrigger -Daily -At "07:00AM"

            $Settings = New-ScheduledTaskSettingsSet `
                -ExecutionTimeLimit (New-TimeSpan -Minutes 10) `
                -StartWhenAvailable `
                -RunOnlyIfNetworkAvailable

            Register-ScheduledTask `
                -TaskName $TaskName `
                -Action $Action `
                -Trigger $Trigger `
                -Settings $Settings `
                -Description "Daily update for Blue-Team-Skills AppSec skill from GitHub" `
                -RunLevel Limited `
                -Force | Out-Null

            Write-OK "Scheduled task '$TaskName' created - runs daily at 07:00 AM."
            Write-INFO "To run immediately: Start-ScheduledTask -TaskName '$TaskName'"
            Write-INFO "To remove:         Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false"

        } catch {
            Write-WARN "Could not create scheduled task: $_"
            Write-INFO "Run update.ps1 manually to get updates: .\scripts\update.ps1"
        }
    }
}

# -- Done ----------------------------------------------------------------------

Write-Header "Installation Complete"
Write-OK "Skill installed globally at:  $SkillDest"
Write-OK "Shortcut installed at:        $AppsecDest"
Write-OK "Git hook installed at:        $HookFile"
Write-Host ""
Write-Host "  Next steps:" -ForegroundColor Cyan
Write-Host "  1. Open AGY and type: /appsec" -ForegroundColor White
Write-Host "  2. To get updates manually: .\scripts\update.ps1" -ForegroundColor White
Write-Host "  3. Updates auto-apply on every 'git pull'" -ForegroundColor White
Write-Host "  4. Daily auto-update runs at 07:00 AM (Windows Task Scheduler)" -ForegroundColor White
Write-Host ""
