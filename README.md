# Blue-Team-Skills

**Enterprise Application Security Testing Skill for AI Agents**  
*Senior AppSec Engineer · Blue Team · Authorized Security Testing*

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](./LICENSE)
[![EULA Required](https://img.shields.io/badge/EULA-Required-orange.svg)](./EULA.txt)
[![CVE Library](https://img.shields.io/badge/CVE%20Library-Daily%20Updates-blue.svg)](./references/cve-library/)
[![User Guide](https://img.shields.io/badge/User%20Guide-Read%20Here-green.svg)](./GUIDE.md)

> 📖 **Comprehensive Documentation:** Check out the [User Guide (GUIDE.md)](./GUIDE.md) for full workflows, threat modeling guides, and test case libraries.

---

> ⚠️ **LEGAL NOTICE**: Use of this repository is subject to the
> [End User License Agreement (EULA)](./EULA.txt).
> By accessing or using this software you agree to its terms.
> **Authorized use on permitted targets only.**

---

## Overview

`Blue-Team-Skills` is a professional AI agent skill suite for enterprise Blue Teams and Senior Application Security Engineers. It equips AI coding assistants (such as Google Antigravity / AGY) with rigorous security testing methodologies aligned to OWASP Top 10, CVSS v3.1, STRIDE threat modeling, and defensive engineering standards.

### Key Capabilities

| Feature | Description |
| :--- | :--- |
| **Two-Phase Workflow** | Mandatory Pre-Fix Assessment Report before applying any code remediation |
| **11-Domain Scoring** | 0–10 rating per domain with granular, rubric-driven scoring |
| **Weighted Scoring** | Application profile weighting: Payments, Healthcare, SaaS, Admin, API |
| **STRIDE Threat Modeling** | Automated Data Flow Diagram & S/T/R/I/D/E analysis before testing |
| **Test Case Library** | Standardized test cases: `TC-AUTH`, `TC-AUTHZ`, `TC-INJ`, `TC-XSS`, `TC-SSRF` |
| **CVSS v3.1 Guidance** | Complete vector breakdown and score derivation in finding dockets |
| **GraphQL Security** | Testing introspection, query depth/complexity limits, batching DoS, field authz |
| **CI/CD Security** | Pipeline audit: Gitleaks, CodeQL, Trivy, Checkov, branch protection, Sigstore |
| **SOC Detection Engineering**| Generates Sigma, KQL, and Splunk SPL rules for high/critical findings |
| **Live CVE Library** | Automated daily synchronization with NVD/NIST API & cve.org |
| **Self-Updating Engine** | Live pre-flight check updates skills & CVE intelligence upon invocation |
| **Posture Trend Tracking** | Multi-quarter score delta calculation (`Before` vs `After` remediation) |

---

## 🚀 Installation & Setup

You can install the skill **globally** (accessible across all projects on your machine) or **per-project**.

### Method 1: Automated Installation (Recommended for Windows)

The automated installer configures global discovery in Antigravity, sets up automatic Git sync hooks, and configures a daily background updater.

```powershell
# 1. Clone the repository
git clone https://github.com/wtalaat78/Blue-Team-Skills.git
cd Blue-Team-Skills

# 2. Allow local script execution (if not already enabled)
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force

# 3. Run the installer
.\scripts\install.ps1
```

#### What `install.ps1` does automatically:
1. **Installs Global Skills**: Copies `internal-appsec-testing` and `/appsec` shortcut into `~/.gemini/config/skills/`.
2. **Installs Git Post-Merge Hook**: Ensures running `git pull` automatically updates your local global skills.
3. **Registers Daily Scheduled Task**: Runs background sync every morning at 07:00 AM.
4. **Writes Install Stamp**: Records version metadata for version tracking.

---

### Method 2: Manual Installation (Windows / Linux / macOS)

If you prefer manual configuration or are using Linux / macOS:

#### Option A — Global Installation (Available across all projects)
Copy the skill files into your user agent config directory:

* **Windows:**
  ```powershell
  New-Item -ItemType Directory -Path "$env:USERPROFILE\.gemini\config\skills\internal-appsec-testing" -Force
  New-Item -ItemType Directory -Path "$env:USERPROFILE\.gemini\config\skills\appsec" -Force

  Copy-Item ".\skills\internal-appsec-testing\SKILL.md" "$env:USERPROFILE\.gemini\config\skills\internal-appsec-testing\SKILL.md" -Force
  Copy-Item ".\skills\appsec\SKILL.md" "$env:USERPROFILE\.gemini\config\skills\appsec\SKILL.md" -Force
  ```

* **Linux / macOS:**
  ```bash
  mkdir -p ~/.gemini/config/skills/internal-appsec-testing ~/.gemini/config/skills/appsec
  cp skills/internal-appsec-testing/SKILL.md ~/.gemini/config/skills/internal-appsec-testing/SKILL.md
  cp skills/appsec/SKILL.md ~/.gemini/config/skills/appsec/SKILL.md
  ```

#### Option B — Project-Level Installation (Current workspace only)
Place the skill inside the target project repository under `.agents/skills/`:

```
your-project-repo/
└── .agents/
    └── skills/
        ├── internal-appsec-testing/
        │   └── SKILL.md
        └── appsec/
            └── SKILL.md
```

---

## ⚡ How to Use

Once installed, open your AI coding assistant (Antigravity / AGY) and invoke the skill using slash commands or plain language:

```text
/appsec assess this repository for security vulnerabilities
```
```text
/appsec perform a white-box assessment of src/controllers/OrderController.cs
```
```text
/internal-appsec-testing review our GraphQL schema and auth middleware
```

### Live Self-Update on Invocation
Every time you call `/appsec`, the skill performs a visible **Pre-Flight Self-Update** verifying Git sync and CVE library status:

```text
---
### 🔄 AppSec Skill — Live Self-Update & Verification
[1/3] Git Remote Sync    : Pulling origin/main... (Already up to date: e042117)
[2/3] Local Distribution : Synced -> ~/.gemini/config/skills/ & .agents/skills/
[3/3] CVE Library Feed   : 28 Critical/High CVEs active (references/cve-library/)
[Commit Version]         : e042117 | 2026-08-23 11:28:45
---
```

---

## 🔄 Updating the Skill & CVE Library

To manually pull the latest skills and CVE records from GitHub:

```powershell
# Run the updater script
.\scripts\update.ps1

# Options:
.\scripts\update.ps1 -Verbose    # Detailed file-by-file log
.\scripts\update.ps1 -SkipPull   # Sync local files without pulling from Git
```

To manually refresh the local CVE database from the NVD API:
```powershell
python -X utf8 scripts/update_cve_library.py
```

---

## 📚 CVE Library

Located in [`references/cve-library/`](./references/cve-library/), the repository maintains an offline-first library of Critical and High severity CVEs fetched directly from the [NVD/NIST API](https://services.nvd.nist.gov) and [CVE.org](https://www.cve.org).

**AppSec Domains Categorized:**
- `authentication_and_session.md`
- `authorization_and_idor_bola.md`
- `input_validation_and_injection.md`
- `file_upload_and_storage.md`
- `logging_and_soc_telemetry.md`

*Updated daily via GitHub Actions ([`.github/workflows/daily-cve-update.yml`](./.github/workflows/daily-cve-update.yml)).*

---

## 📁 Repository Structure

```
Blue-Team-Skills/
├── EULA.txt                            ← End User License Agreement (READ FIRST)
├── LICENSE                             ← Proprietary License Summary
├── README.md                           ← Main repository documentation & setup guide
├── GUIDE.md                            ← In-depth User Guide & methodology manual
├── skills/
│   ├── internal-appsec-testing/
│   │   └── SKILL.md                    ← Main AppSec testing skill (v3.0)
│   └── appsec/
│       └── SKILL.md                    ← Shortcut alias (/appsec)
├── .agents/
│   └── skills/
│       ├── internal-appsec-testing/    ← Project-level agent discovery
│       └── appsec/                     ← Project-level shortcut
├── references/
│   └── cve-library/
│       ├── README.md                   ← CVE index and statistics
│       ├── authentication_and_session.md
│       ├── authorization_and_idor_bola.md
│       ├── input_validation_and_injection.md
│       ├── file_upload_and_storage.md
│       └── logging_and_soc_telemetry.md
├── scripts/
│   ├── install.ps1                     ← Automated one-time installer
│   ├── update.ps1                      ← Skill sync & update utility
│   └── update_cve_library.py           ← Live NVD/CVE.org feed updater
└── .github/
    └── workflows/
        └── daily-cve-update.yml        ← GitHub Actions daily CVE sync cron
```

---

## ⚖️ Legal & Disclaimer

**Copyright (c) 2025–2026 Waleed Talaat / Techwaves-egy. All rights reserved.**

This software is proprietary. Use is strictly subject to the [End User License Agreement (EULA)](./EULA.txt).

**Authorized Use Only:** This skill and its guidance are intended exclusively for authorized security testing and defensive engineering on systems you own or have explicit written permission to test. Unauthorized security testing may violate local and international cybercrime laws.

See [EULA.txt](./EULA.txt) for liability limits, AI output disclaimers, and warranty terms.
