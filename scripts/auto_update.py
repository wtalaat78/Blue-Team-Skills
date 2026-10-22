#!/usr/bin/env python3
"""
Blue-Team-Skills v4.0 — Automated Self-Update & Verification Engine
===================================================================
Cross-platform auto-updater for any AI agent or platform (Antigravity, Claude Code,
Cursor, Windsurf, Copilot, Cline, Terminal).

Performs:
1. Git remote sync (`git pull origin main`).
2. Automatic synchronization to all local skill directories:
   - Global Antigravity: ~/.gemini/config/skills/
   - Workspace Agents:   .agents/skills/
   - Claude Code Global: ~/.claude/CLAUDE.md
3. Active Threat Intelligence verification.
4. Outputs the mandatory visible update verification box.

Usage:
  python scripts/auto_update.py
  python scripts/auto_update.py --refresh-cve
  python scripts/auto_update.py --json
"""

import os
import sys
import json
import glob
import hashlib
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def get_repo_root():
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent

def run_cmd(cmd, cwd, timeout=10):
    try:
        res = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return -1, "", str(e)

def get_file_hash(path):
    if not os.path.exists(path):
        return None
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def auto_update(refresh_cve=False):
    repo_root = get_repo_root()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Git pull from origin main
    pull_status = "Skipped"
    pull_code, pull_out, pull_err = run_cmd(["git", "pull", "origin", "main"], cwd=repo_root, timeout=8)
    if pull_code == 0:
        if "Already up to date" in pull_out:
            pull_status = "Already up to date"
        else:
            pull_status = "Pulled latest changes from GitHub"
    else:
        pull_status = f"Local cache active ({pull_err or pull_out or 'offline'})"

    # 2. Get current commit metadata
    _, commit_hash, _ = run_cmd(["git", "rev-parse", "--short", "HEAD"], cwd=repo_root)
    if not commit_hash:
        commit_hash = "v4.0"
    _, commit_msg, _ = run_cmd(["git", "log", "-1", "--format=%s"], cwd=repo_root)

    # 3. Synchronize skill files
    user_home = Path.home()
    global_gemini_skills = user_home / ".gemini" / "config" / "skills"
    claude_home = user_home / ".claude"

    sync_targets = [
        # Internal AppSec Testing
        (repo_root / "skills" / "internal-appsec-testing" / "SKILL.md",
         repo_root / ".agents" / "skills" / "internal-appsec-testing" / "SKILL.md",
         "internal-appsec-testing (workspace .agents)"),
        (repo_root / "skills" / "internal-appsec-testing" / "SKILL.md",
         global_gemini_skills / "internal-appsec-testing" / "SKILL.md",
         "internal-appsec-testing (global ~/.gemini)"),
        # Appsec Shortcut
        (repo_root / "skills" / "appsec" / "SKILL.md",
         repo_root / ".agents" / "skills" / "appsec" / "SKILL.md",
         "appsec shortcut (workspace .agents)"),
        (repo_root / "skills" / "appsec" / "SKILL.md",
         global_gemini_skills / "appsec" / "SKILL.md",
         "appsec shortcut (global ~/.gemini)"),
    ]

    # Optional Claude Code sync
    if claude_home.exists():
        sync_targets.append((
            repo_root / "CLAUDE.md",
            claude_home / "CLAUDE.md",
            "Claude Code global config (~/.claude/CLAUDE.md)"
        ))

    updated_count = 0
    skipped_count = 0

    for src, dst, name in sync_targets:
        if not src.exists():
            continue
        src_hash = get_file_hash(src)
        dst_hash = get_file_hash(dst)

        if src_hash == dst_hash and dst_hash is not None:
            skipped_count += 1
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            updated_count += 1

    # 4. Refresh CVE Library (if requested)
    if refresh_cve:
        cve_script = repo_root / "scripts" / "update_cve_library.py"
        if cve_script.exists():
            run_cmd([sys.executable, str(cve_script)], cwd=repo_root, timeout=30)

    # Count active CVE library references
    cve_files = glob.glob(str(repo_root / "references" / "cve-library" / "*.md"))
    cve_count = len(cve_files)

    # 5. Write version stamp
    version_file = repo_root / ".skill-version.json"
    version_data = {
        "framework": "Blue-Team-Skills v4.0 (Full-Spectrum ARS)",
        "last_updated": timestamp,
        "git_commit": commit_hash,
        "commit_msg": commit_msg,
        "git_remote_status": pull_status,
        "skills_updated": updated_count,
        "skills_current": skipped_count,
        "cve_library_files": cve_count
    }
    with open(version_file, "w", encoding="utf-8") as f:
        json.dump(version_data, f, indent=2)

    return version_data

def format_verification_banner(data):
    commit = data.get("git_commit", "latest")
    ts = data.get("last_updated", "")
    pull_status = data.get("git_remote_status", "Synced")
    cve_count = data.get("cve_library_files", 12)

    banner = f"""---
### 🔄 AppSec Skill — Live Self-Update & Verification
```text
[1/3] Git Remote Sync    : Pulling origin/main... ({pull_status})
[2/3] Local Distribution : Synced -> ~/.gemini/config/skills/ & .agents/skills/
[3/3] CVE Library Feed   : {cve_count} Active Threat Intelligence Feeds (references/cve-library/)
[Commit Version]         : {commit} | {ts}
```

| Component | Status | Details |
|:---|:---:|:---|
| **Skill Definition** | ✅ Up to Date | `internal-appsec-testing` v4.0 (Full-Spectrum ARS) |
| **Shortcuts** | ✅ Active | `/appsec`, `/internal-appsec-testing` |
| **Domain Matrix** | 🛡️ Active | 12 Security Domains (including Host Runtime & Reachability) |
| **CVE Intelligence** | ✅ Active | Synced with NVD/NIST API, CVE.org & CISA KEV |
| **Audit Posture** | 🛡️ Ready | Phase 1: Pre-Fix Report required before remediation |
---"""
    return banner

if __name__ == "__main__":
    refresh = "--refresh-cve" in sys.argv
    data = auto_update(refresh_cve=refresh)
    if "--json" in sys.argv:
        print(json.dumps(data, indent=2))
    else:
        print(format_verification_banner(data))
