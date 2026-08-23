# =============================================================================
# Blue-Team-Skills — Update Script
# =============================================================================
# Run this anytime to pull the latest skill version from GitHub and sync it
# to all local install locations.
#
# Also called automatically by:
#   - The Git post-merge hook (after every "git pull")
#   - The Windows Scheduled Task (daily at 07:00 AM)
#
# Usage:
#   .\scripts\update.ps1              # Normal update
#   .\scripts\update.ps1 -Verbose     # Show detailed output
#   .\scripts\update.ps1 -SkipPull    # Sync files only (no git pull)
# =============================================================================

param(
    [switch]$SkipPull,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

# ── Helpers ──────────────────────────────────────────────────────────────────

function Write-OK($text)   { Write-Host "  [OK]  $text" -ForegroundColor Green }
function Write-WARN($text) { Write-Host "  [!!]  $text" -ForegroundColor Yellow }
function Write-ERR($text)  { Write-Host "  [XX]  $text" -ForegroundColor Red }
function Write-INFO($text) { Write-Host "  [**]  $text" -ForegroundColor White }

function Get-FileHash256($path) {
    if (Test-Path $path) {
        return (Get-FileHash -Path $path -Algorithm SHA256).Hash
    }
    return $null
}

# ── Locate repository root ───────────────────────────────────────────────────

$RepoRoot = Split-Path -Parent $PSScriptRoot
$LogFile  = "$RepoRoot\.update-log.txt"
$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

function Write-Log($msg) {
    $line = "[$Timestamp] $msg"
    Add-Content -Path $LogFile -Value $line -Encoding UTF8
    if ($Verbose) { Write-INFO $msg }
}

Write-Host ""
Write-Host "  Blue-Team-Skills Update — $Timestamp" -ForegroundColor Cyan
Write-Host "  Repository: $RepoRoot" -ForegroundColor Gray

# ── Step 1: Git pull ─────────────────────────────────────────────────────────

if ($SkipPull) {
    Write-WARN "Skipping git pull (-SkipPull flag set). Syncing local files only."
    Write-Log "Update started (SkipPull mode)"
} else {
    Write-Host ""
    Write-Host "  Pulling latest from GitHub..." -ForegroundColor Cyan

    try {
        $pullOutput = git -C $RepoRoot pull origin main 2>&1
        $exitCode   = $LASTEXITCODE

        if ($exitCode -ne 0) {
            Write-ERR "git pull failed (exit code $exitCode):"
            Write-ERR $pullOutput
            Write-Log "ERROR: git pull failed — $pullOutput"
            exit 1
        }

        if ($pullOutput -match "Already up to date") {
            Write-OK "Repository is already up to date — no changes from GitHub."
            Write-Log "git pull: already up to date"
        } else {
            Write-OK "Pulled latest changes from GitHub."
            Write-Log "git pull: $pullOutput"
        }

    } catch {
        Write-ERR "Git pull error: $_"
        Write-Log "ERROR: git exception — $_"
        exit 1
    }
}

# ── Step 2: Sync skill files to global AGY config ────────────────────────────

Write-Host ""
Write-Host "  Syncing skill files to global install..." -ForegroundColor Cyan

$GlobalSkillsDir = "$env:USERPROFILE\.gemini\config\skills"

$SkillPairs = @(
    @{ Src = "$RepoRoot\skills\internal-appsec-testing\SKILL.md"
       Dst = "$GlobalSkillsDir\internal-appsec-testing\SKILL.md"
       Name = "internal-appsec-testing" },
    @{ Src = "$RepoRoot\skills\appsec\SKILL.md"
       Dst = "$GlobalSkillsDir\appsec\SKILL.md"
       Name = "appsec (shortcut)" }
)

$updatedCount = 0
$skippedCount = 0

foreach ($pair in $SkillPairs) {
    if (-not (Test-Path $pair.Src)) {
        Write-WARN "Source not found, skipping: $($pair.Src)"
        Write-Log "SKIP: source missing — $($pair.Src)"
        continue
    }

    # Compare hashes to detect actual changes
    $srcHash = Get-FileHash256 $pair.Src
    $dstHash = Get-FileHash256 $pair.Dst

    if ($srcHash -eq $dstHash) {
        Write-OK "$($pair.Name): already up to date (no changes)"
        Write-Log "SKIP: $($pair.Name) — hash unchanged"
        $skippedCount++
    } else {
        $dstDir = Split-Path -Parent $pair.Dst
        if (-not (Test-Path $dstDir)) {
            New-Item -ItemType Directory -Path $dstDir -Force | Out-Null
        }
        Copy-Item $pair.Src $pair.Dst -Force
        Write-OK "$($pair.Name): updated successfully"
        Write-Log "UPDATED: $($pair.Name)"
        $updatedCount++
    }
}

# ── Step 3: Record current version ───────────────────────────────────────────

$CurrentCommit  = git -C $RepoRoot rev-parse --short HEAD 2>$null
$CurrentVersion = git -C $RepoRoot log -1 --format="%s" 2>$null

$VersionFile = "$RepoRoot\.skill-version.json"
@{
    last_updated = $Timestamp
    git_commit   = $CurrentCommit
    commit_msg   = $CurrentVersion
    updated_by   = $env:USERNAME
    skills_updated = $updatedCount
    skills_skipped = $skippedCount
} | ConvertTo-Json -Depth 2 | Set-Content -Path $VersionFile -Encoding UTF8

Write-Log "Version stamp written: commit=$CurrentCommit"

# ── Step 4: Summary ──────────────────────────────────────────────────────────

Write-Host ""
Write-Host "  ──────────────────────────────────────" -ForegroundColor Gray
Write-Host "  Update Summary" -ForegroundColor Cyan
Write-Host "  ──────────────────────────────────────" -ForegroundColor Gray
Write-OK   "  Skills updated : $updatedCount"
Write-INFO "  Already current: $skippedCount"
Write-INFO "  Git commit     : $CurrentCommit"
Write-INFO "  Log file       : $LogFile"
Write-Host ""

if ($updatedCount -gt 0) {
    Write-Host "  Skill files updated. Restart AGY to load the new version." -ForegroundColor Yellow
} else {
    Write-Host "  All skill files are already at the latest version." -ForegroundColor Green
}
Write-Host ""
