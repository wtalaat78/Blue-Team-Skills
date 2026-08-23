# Blue-Team-Skills

**Universal Application Security Testing Skill Suite for AI Agents**  
*Senior AppSec Engineer · Blue Team · Authorized Security Testing*

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](./LICENSE)
[![EULA Required](https://img.shields.io/badge/EULA-Required-orange.svg)](./EULA.txt)
[![Universal Agent Support](https://img.shields.io/badge/Agents-Universal%20Compatibility-brightgreen.svg)](#-agent-compatibility-matrix)
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

`Blue-Team-Skills` is a **universal AI agent security skill suite** designed for enterprise Blue Teams and Senior Application Security Engineers. It equips **any AI coding assistant or autonomous agent** with rigorous security testing methodologies aligned to OWASP Top 10, CVSS v3.1, STRIDE threat modeling, and defensive engineering standards.

---

## 🤖 Agent Compatibility Matrix

`Blue-Team-Skills` supports all major AI coding agents, IDEs, and LLM frameworks out of the box:

| AI Agent / IDE | Configuration File | Discovery / Activation |
| :--- | :--- | :--- |
| **Google Antigravity (AGY)** | `skills/internal-appsec-testing/SKILL.md` | `/appsec` or `/internal-appsec-testing` |
| **Claude Code (CLI & Desktop)** | [`CLAUDE.md`](./CLAUDE.md) | Auto-discovered in repo or `~/.claude/CLAUDE.md` |
| **Cursor IDE** | [`.cursorrules`](./.cursorrules) & [`.cursor/rules/`](./.cursor/rules/) | Native automatic rule indexing |
| **Windsurf / Cascade** | [`.windsurfrules`](./.windsurfrules) | Native automatic rule indexing |
| **GitHub Copilot (Chat & Workspace)** | [`.github/copilot-instructions.md`](./.github/copilot-instructions.md) | Auto-detected in repo |
| **Roo Code / Cline / Devin / AutoGPT** | [`AGENTS.md`](./AGENTS.md) | Universal agent instructions standard |
| **ChatGPT / Custom GPTs / API Agents** | [`prompts/appsec-system-prompt.md`](./prompts/appsec-system-prompt.md) | Portable system prompt |

---

## Key Capabilities

| Feature | Description |
| :--- | :--- |
| **Universal Multi-Agent Support** | Ready for Antigravity, Claude Code, Cursor, Windsurf, Copilot, Cline, and custom agents |
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

### Method 1: Automated Installer

#### Windows (PowerShell)
```powershell
# 1. Clone repository
git clone https://github.com/wtalaat78/Blue-Team-Skills.git
cd Blue-Team-Skills

# 2. Allow local script execution
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force

# 3. Run installer
.\scripts\install.ps1
```

#### Linux / macOS / WSL (Bash)
```bash
# 1. Clone repository
git clone https://github.com/wtalaat78/Blue-Team-Skills.git
cd Blue-Team-Skills

# 2. Run installer
bash scripts/install.sh
```

#### What the installer configures automatically:
1. **Global Antigravity & Agent Skills**: Installs to `~/.gemini/config/skills/` and `.agents/skills/`.
2. **Claude Code Global Config**: Syncs to `~/.claude/CLAUDE.md` if Claude is installed.
3. **IDE Rules**: Configures `.cursorrules`, `.cursor/rules/`, `.windsurfrules`, and `.github/copilot-instructions.md`.
4. **Git Auto-Update Hook**: Ensures `git pull` automatically syncs the latest skills across all locations.
5. **Background Updater**: Registers daily background synchronization (07:00 AM).

---

### Method 2: Manual Setup for Specific Agents

#### For Claude Code
The repository root contains [`CLAUDE.md`](./CLAUDE.md). Claude Code will automatically detect and follow it when running in this workspace.

#### For Cursor IDE
The repository root contains [`.cursorrules`](./.cursorrules) and [`.cursor/rules/internal-appsec-testing.mdc`](./.cursor/rules/internal-appsec-testing.mdc). Cursor will automatically apply these rules.

#### For Windsurf (Cascade)
The repository root contains [`.windsurfrules`](./.windsurfrules). Windsurf will automatically apply these instructions.

#### For GitHub Copilot
The repository contains [`.github/copilot-instructions.md`](./.github/copilot-instructions.md) for custom Copilot Chat behavior.

#### For Generic Agents (Cline, Roo Code, AutoGPT, Devin)
[`AGENTS.md`](./AGENTS.md) provides the universal instruction specification.

#### For ChatGPT / Custom GPTs / LangChain / CrewAI
Copy and paste the portable prompt from [`prompts/appsec-system-prompt.md`](./prompts/appsec-system-prompt.md) into your custom instructions or agent prompt template.

---

## ⚡ How to Use

Invoke the security engineer persona in your favorite agent:

```text
# Antigravity / Slash Commands:
/appsec assess this repository for security vulnerabilities
/appsec perform a white-box assessment of src/controllers/OrderController.cs

# Claude Code / Cursor / Windsurf / Copilot / Generic Prompts:
Perform a full AppSec security review on this codebase following the Two-Phase workflow.
Audit our authentication and authorization logic for IDOR/BOLA vulnerabilities.
Review our GraphQL schema and generate Sigma detection rules for abuse patterns.
```

---

## 🔄 Updating the Skill & CVE Library

```powershell
# Windows
.\scripts\update.ps1

# Linux / macOS
bash scripts/update.sh
```

To refresh the local CVE intelligence database from the NVD/NIST API:
```bash
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
├── AGENTS.md                           ← Universal standard agent instructions
├── CLAUDE.md                           ← Claude Code & Anthropic agent configuration
├── .cursorrules                        ← Cursor IDE configuration
├── .cursor/rules/                      ← Modern Cursor MDC rules
├── .windsurfrules                      ← Windsurf (Codeium Cascade) configuration
├── .github/
│   ├── copilot-instructions.md         ← GitHub Copilot custom instructions
│   └── workflows/
│       └── daily-cve-update.yml        ← GitHub Actions daily CVE sync cron
├── prompts/
│   └── appsec-system-prompt.md         ← Portable prompt for ChatGPT, Custom GPTs, APIs
├── skills/
│   ├── internal-appsec-testing/
│   │   └── SKILL.md                    ← Main AppSec testing skill runbook (v3.0)
│   └── appsec/
│       └── SKILL.md                    ← Shortcut alias (/appsec)
├── references/
│   └── cve-library/                    ← Daily-synced CVE database by domain
└── scripts/
    ├── install.ps1 / install.sh        ← Cross-platform automated installers
    ├── update.ps1 / update.sh          ← Cross-platform auto-updaters
    └── update_cve_library.py           ← Live NVD/CVE.org feed updater
```

---

## ⚖️ Legal & Disclaimer

**Copyright (c) 2025–2026 Waleed Talaat All rights reserved.**

This software is proprietary. Use is strictly subject to the [End User License Agreement (EULA)](./EULA.txt).

**Authorized Use Only:** This skill and its guidance are intended exclusively for authorized security testing and defensive engineering on systems you own or have explicit written permission to test. Unauthorized security testing may violate local and international cybercrime laws.

See [EULA.txt](./EULA.txt) for liability limits, AI output disclaimers, and warranty terms.
