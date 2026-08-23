# Blue-Team-Skills

**Enterprise Application Security Testing Skill for AI Agents**  
*Senior AppSec Engineer · Blue Team · Authorized Security Testing*

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](./LICENSE)
[![EULA Required](https://img.shields.io/badge/EULA-Required-orange.svg)](./EULA.txt)
[![CVE Library](https://img.shields.io/badge/CVE%20Library-Daily%20Updates-blue.svg)](./references/cve-library/)
[![User Guide](https://img.shields.io/badge/User%20Guide-Read%20Here-green.svg)](./GUIDE.md)

> 📖 **New to this skill? Start with the [User Guide (GUIDE.md)](./GUIDE.md)** — it covers installation, step-by-step usage, all assessment modes, report reading, CVE library search, and common use cases with examples.

---

> ⚠️ **LEGAL NOTICE**: Use of this repository is subject to the
> [End User License Agreement (EULA)](./EULA.txt).
> By accessing or using this software you agree to its terms.
> **Authorized use on permitted targets only.**

---

## Overview

`Blue-Team-Skills` is a professional AI agent skill suite for enterprise Blue Teams and
Senior Application Security Engineers. It extends AI coding assistants (Antigravity/AGY)
with deep, structured security testing capabilities aligned to OWASP Top 10, CVSS v3.1,
and enterprise reporting standards.

### Key Capabilities

| Feature | Description |
| :--- | :--- |
| **Two-Phase Workflow** | Mandatory Pre-Fix Assessment Report before any code change |
| **11-Domain Scoring** | 0–10 score per domain with exact per-band rubrics |
| **Weighted Scoring** | Application profiles: Payments, Healthcare, SaaS, Admin, API |
| **STRIDE Threat Modeling** | Full DFD + S/T/R/I/D/E analysis before testing |
| **Test Case Library** | Structured test cases: TC-AUTH, TC-AUTHZ, TC-INJ, TC-XSS, TC-SSRF |
| **CVSS v3.1 Guidance** | Embedded scoring breakdown in every finding docket |
| **GraphQL Testing** | Introspection, depth/complexity limits, batching DoS, field-level authz |
| **CI/CD Security** | Pipeline assessment: Gitleaks, CodeQL, Trivy, Checkov, Sigstore |
| **SOC Detection Rules** | Sigma/KQL/SPL rules for every High/Critical finding |
| **CVE Library** | Daily live CVE feed from NVD/NIST — 20 AppSec keyword profiles |
| **Escalation Protocol** | Active exploit stop-and-escalate procedure |
| **Trend Tracking** | Quarterly posture score tracking across assessments |

---

## CVE Library

Located in [`references/cve-library/`](./references/cve-library/), the library is
automatically updated every day at **06:00 UTC** via GitHub Actions, fetching
Critical and High severity CVEs from the
[NVD/NIST API](https://services.nvd.nist.gov) across 20 AppSec keyword profiles.

**AppSec Domains Covered:**
- Authentication & Session
- Authorization, IDOR/BOLA
- Input Validation & Injection
- XSS & Output Encoding
- SSRF & Perimeter
- File Upload & Storage
- Cryptography & Secrets
- API & Business Logic
- Logging & SOC Telemetry
- Software Supply Chain & SCA

---

## Installation

The skill is discovered automatically by the Antigravity (AGY) AI agent from:

```
.agents/skills/internal-appsec-testing/SKILL.md   ← Project-level
~/.gemini/config/skills/internal-appsec-testing/   ← Global (all projects)
```

Invoke via:
```
/appsec [target or request]
/internal-appsec-testing [target or request]
```

---

## Repository Structure

```
Blue-Team-Skills/
├── EULA.txt                            ← End User License Agreement (READ FIRST)
├── LICENSE                             ← Proprietary License Summary
├── README.md                           ← This file
├── GUIDE.md                            ← User Guide (start here)
├── skills/
│   ├── internal-appsec-testing/
│   │   └── SKILL.md                    ← Main AppSec skill (v3.0)
│   └── appsec/
│       └── SKILL.md                    ← Shortcut alias (/appsec)
├── .agents/
│   └── skills/
│       ├── internal-appsec-testing/    ← Project-level agent discovery
│       └── appsec/                     ← Project-level shortcut
├── references/
│   └── cve-library/
│       ├── README.md                   ← CVE index and summary
│       ├── authentication_and_session.md
│       ├── authorization_and_idor_bola.md
│       ├── input_validation_and_injection.md
│       ├── file_upload_and_storage.md
│       └── logging_and_soc_telemetry.md
├── scripts/
│   └── update_cve_library.py           ← CVE library updater
└── .github/
    └── workflows/
        └── daily-cve-update.yml        ← GitHub Actions daily cron
```

---

## Legal

**Copyright (c) 2025–2026 Waleed Talaat / Techwaves-egy. All rights reserved.**

This software is proprietary. Use is subject to the [EULA](./EULA.txt).

**This tool is intended exclusively for authorized security testing.**
Unauthorized use against systems you do not own or have written permission
to test may constitute a criminal offense under applicable law.

The Author is not responsible for any misuse, illegal use, or damages
arising from the use of this Software. See [EULA.txt](./EULA.txt) for full terms.

CVE data sourced from [NVD/NIST](https://nvd.nist.gov) and [CVE.org](https://www.cve.org).
See EULA Article 4 for third-party data terms.
