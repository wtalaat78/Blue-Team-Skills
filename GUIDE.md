# User Guide — Internal AppSec Testing Skill
### `internal-appsec-testing` · `/appsec`

**Version:** 3.0 | **Author:** Waleed Talaat / Techwaves-egy  
**Repository:** https://github.com/wtalaat78/Blue-Team-Skills

---

> ⚠️ **Legal Reminder:** This skill is for **authorized security testing only**.  
> Always obtain written permission from the system owner before testing.  
> Use of this skill is governed by the [EULA](./EULA.txt).

---

## Table of Contents

1. [What This Skill Does](#1-what-this-skill-does)
2. [Prerequisites](#2-prerequisites)
3. [Installation & Updates](#3-installation--updates)
4. [How to Invoke the Skill](#4-how-to-invoke-the-skill)
5. [Step-by-Step Usage Walkthrough](#5-step-by-step-usage-walkthrough)
6. [Assessment Modes](#6-assessment-modes)
7. [Understanding the Pre-Fix Report](#7-understanding-the-pre-fix-report)
8. [Understanding the 10-Point Scoring System](#8-understanding-the-10-point-scoring-system)
9. [Using the CVE Library](#9-using-the-cve-library)
10. [Phase 2: Remediation & Retesting](#10-phase-2-remediation--retesting)
11. [Common Use Cases with Examples](#11-common-use-cases-with-examples)
12. [Tips & Best Practices](#12-tips--best-practices)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. What This Skill Does

This skill turns your AI agent (Antigravity/AGY) into a **Senior Application Security Engineer** that can:

| Capability | What It Produces |
| :--- | :--- |
| **Security Assessment** | Structured Pre-Fix Report with scores for 11 security domains |
| **Vulnerability Findings** | Detailed dockets with CVSS score, CWE, PoC, and code-level fix |
| **STRIDE Threat Modeling** | Data flow analysis and trust boundary mapping |
| **Test Case Execution** | Step-by-step tests: auth, IDOR, injection, XSS, SSRF, and more |
| **SOC Detection Rules** | Sigma / KQL / Splunk SPL rules for every finding |
| **CVE Cross-Reference** | Matches your dependencies against a live daily CVE library |
| **Remediation Guidance** | Vulnerable vs. secure code examples in your stack's language |
| **Post-Fix Verification** | Re-tests the fix and reports a score delta (Before → After) |

---

## 2. Prerequisites

Before using this skill, ensure you have:

- ✅ **Antigravity (AGY)** AI agent installed and running
- ✅ **Written authorization** to test the target application (scope document, signed agreement, or bug bounty program participation)
- ✅ **Skill installed** (see Section 3)
- ✅ Test account credentials (for Gray Box / White Box assessment)
- ✅ For White Box: access to the source code repository

> 🔴 **If you do not have written authorization, do not proceed.**  
> The skill will ask you to provide authorization before doing any intrusive testing.

---

## 3. Installation & Updates

### How Updates Work

```
GitHub (source of truth)
        │
        │  3 automatic sync triggers:
        │  ① git pull      → post-merge hook copies SKILL.md instantly
        │  ② Daily 07:00 AM → Scheduled Task pulls + syncs automatically
        │  ③ Manual         → run scripts\update.ps1 anytime
        │
        ▼
~\.gemini\config\skills\internal-appsec-testing\SKILL.md  ← AGY reads this
~\.gemini\config\skills\appsec\SKILL.md                   ← /appsec shortcut
.agents\skills\internal-appsec-testing\SKILL.md           ← project-level copy
```

---

### First-Time Setup (Run Once Per Machine)

**Step 1 — Clone the repository**
```powershell
git clone https://github.com/wtalaat78/Blue-Team-Skills.git
cd Blue-Team-Skills
```

**Step 2 — Run the installer** (as your normal user — no admin needed)
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
.\scripts\install.ps1
```

The installer will:
- ✅ Copy the skill to `~\.gemini\config\skills\` (global AGY install)
- ✅ Install a Git post-merge hook (auto-sync on every `git pull`)
- ✅ Register a **Windows Scheduled Task** to pull updates daily at 07:00 AM
- ✅ Write a version stamp to track your installed version

**Step 3 — Verify**
Open AGY and type `/appsec` — you should see the AppSec Engineer role activate.

---

### Getting Updates

#### Option A — Automatic (recommended)
Do nothing. The **Windows Scheduled Task** runs every morning at 07:00 AM:
```
Task name: BlueTeamSkills-DailyUpdate
Schedule:  Daily at 07:00 AM
Action:    git pull + sync SKILL.md to global install
```

#### Option B — On every `git pull` (automatic via hook)
Whenever you run `git pull` in the repo folder, the post-merge hook fires:
```powershell
git pull   # ← SKILL.md automatically synced after this
```

#### Option C — Manual update (anytime)
```powershell
.\scripts\update.ps1
```
Options:
```powershell
.\scripts\update.ps1 -Verbose    # show detailed file-by-file output
.\scripts\update.ps1 -SkipPull   # sync files without git pull
```

---

### Check Your Current Version
```powershell
# See what version you have installed
Get-Content .skill-version.json

# See the update log
Get-Content .update-log.txt -Tail 20
```

---

### Manage the Scheduled Task
```powershell
# Run the update right now
Start-ScheduledTask -TaskName "BlueTeamSkills-DailyUpdate"

# Check last run status
Get-ScheduledTask -TaskName "BlueTeamSkills-DailyUpdate" | Get-ScheduledTaskInfo

# Disable auto-updates
Disable-ScheduledTask -TaskName "BlueTeamSkills-DailyUpdate"

# Remove completely
Unregister-ScheduledTask -TaskName "BlueTeamSkills-DailyUpdate" -Confirm:$false
```

---

### Install Without Scheduled Task (Silent Mode)
```powershell
.\scripts\install.ps1 -SkipScheduledTask
```

---

### Uninstall
```powershell
# Remove global skill installs
Remove-Item "$env:USERPROFILE\.gemini\config\skills\internal-appsec-testing" -Recurse -Force
Remove-Item "$env:USERPROFILE\.gemini\config\skills\appsec" -Recurse -Force

# Remove scheduled task
Unregister-ScheduledTask -TaskName "BlueTeamSkills-DailyUpdate" -Confirm:$false

# Remove git hook
Remove-Item ".git\hooks\post-merge" -Force
```

---

## 4. How to Invoke the Skill

You can invoke the skill using either shortcut:

| Command | Description |
| :--- | :--- |
| `/appsec` | Short alias — use this for quick invocations |
| `/internal-appsec-testing` | Full name |

### Basic Invocation Examples

```
/appsec assess this web application: https://staging.myapp.internal
```
```
/appsec review this code for security vulnerabilities
```
```
/appsec I need a full security assessment of our REST API — white box, I have source code
```
```
/appsec check our package.json for vulnerable dependencies
```
```
/appsec search the CVE library for SQL injection vulnerabilities
```

---

## 5. Step-by-Step Usage Walkthrough

Here is the complete workflow from invocation to final report.

---

### STEP 1 — Confirm Authorization

When you invoke the skill, the **first thing the agent will check** is authorization.

**What to expect:**
```
Agent: Before I begin, please confirm:
       1. Do you have written authorization to test this application?
       2. What is the authorized scope (which environment / endpoints)?
       3. Is this Development, Test, Staging, or Production?
```

**What to say:**
```
Yes, I am authorized. This is our internal staging environment at
staging.myapp.internal. The scope covers all endpoints under /api/v1/.
Testing window: today, business hours only. I have test accounts for
roles: Standard User, Manager, and Admin.
```

---

### STEP 2 — Choose Your Assessment Mode

Tell the agent what information you have available:

| If you have... | Say... | Mode |
| :--- | :--- | :--- |
| Only a URL / running app | "I only have the URL and a test account" | **Black Box** |
| Test accounts + API docs | "I have test accounts for 3 roles and a Swagger/OpenAPI spec" | **Gray Box** |
| Full source code | "I have the source code repository" | **White Box** |

---

### STEP 3 — Application Inventory

The agent will ask you to describe (or will analyze automatically) the application stack:

```
Agent: Please describe the application:
       - Technology stack (frontend / backend / database)?
       - Authentication method (JWT, Session, OAuth/OIDC)?
       - Cloud provider and services used?
       - Any known integrations (payment, email, storage)?
```

Example answer:
```
Frontend: React 18
Backend: Node.js + Express
Database: PostgreSQL
Auth: JWT with Microsoft Entra ID (OIDC)
Cloud: Azure — App Service, Azure Blob Storage
Integrations: Stripe (payments), SendGrid (email)
```

---

### STEP 4 — Attack Surface Mapping

The agent maps all entry points before testing:

```
Agent will enumerate:
  - API endpoints (from spec or by probing)
  - Authentication flows
  - File upload endpoints
  - Admin / management interfaces
  - External integrations
  - GraphQL schema (if applicable)
```

You can speed this up by providing an OpenAPI/Swagger spec:
```
/appsec Here is our OpenAPI spec: [paste or attach swagger.json]
```

---

### STEP 5 — STRIDE Threat Modeling

For White Box / Gray Box, the agent performs a brief STRIDE analysis:

```
Agent will produce:
  S - Spoofing threats (e.g., JWT algorithm confusion)
  T - Tampering threats (e.g., parameter modification)
  R - Repudiation threats (e.g., missing audit logs)
  I - Info Disclosure (e.g., verbose error messages)
  D - Denial of Service (e.g., missing rate limits)
  E - Elevation of Privilege (e.g., IDOR/BOLA)
```

---

### STEP 6 — Test Domain Execution

The agent systematically tests all 11 security domains using the built-in test case library.

Each test looks like this:

```
[TC-AUTH-001] Account Lockout Enforcement
  Testing: 10 failed login attempts for the same username...
  Result: ✅ PASS — Account locked after 5 attempts (HTTP 429)
  Score contribution: +0.5 to Domain 1

[TC-AUTH-007] JWT Algorithm Confusion (alg:none)
  Testing: Modified JWT header to "alg":"none", removed signature...
  Result: ❌ FAIL — Server accepted tampered token!
  Finding: APP-001 (Critical) — JWT algorithm confusion
```

---

### STEP 7 — Receive the Pre-Fix Assessment Report

After all tests complete, the agent produces the **Pre-Fix Report**.

> 🔴 **The agent will NOT modify any code before this report is shown and approved.**

The report contains:
- Executive Summary
- STRIDE threat summary
- Security Posture Scorecard (11 domains, each with X.X/10 score)
- Detailed finding dockets with CVSS scores and code examples
- SOC detection rules (Sigma/KQL)
- CVE Library matches for your dependencies
- Prioritized remediation roadmap
- Approval gate

---

### STEP 8 — Review and Approve

Read the report carefully. Then choose:

```
"Approved — please proceed to Phase 2 (fix all Critical and High findings)"
```
or
```
"Approved with scope limit — fix APP-001 and APP-003 only for now"
```
or
```
"I want to discuss APP-002 before approving — explain the business impact"
```

---

### STEP 9 — Phase 2: Remediation

Once approved, the agent:
1. Implements the code-level fix
2. Adds a security regression test
3. Re-runs the original test case to confirm the fix
4. Tests bypass vectors
5. Reports verification outcome

---

### STEP 10 — Post-Fix Score Delta

The agent shows the before/after improvement:

```
Domain                 | Before | After  | Delta
Authentication         |  4.0   |  8.5   | +4.5 ↑
Authorization & IDOR   |  2.5   |  9.0   | +6.5 ↑
Injection Defenses     |  7.0   |  9.5   | +2.5 ↑
OVERALL                |  5.8   |  9.1   | +3.3 ↑
```

---

## 6. Assessment Modes

### Black Box — What to Provide

```
/appsec I need a black box assessment of https://api.myapp.com

Scope:
- Environment: Production (read-only; no write operations)
- Test account: testuser@myapp.com / [password]
- Endpoints: anything under /api/v1/ and /api/v2/
- Excluded: /api/v1/admin/ (production admin — do not touch)
```

### Gray Box — What to Provide

```
/appsec Gray box assessment of our staging API

I have:
- Swagger spec: [attach swagger.yaml]
- Test accounts: user@test.com (Standard), manager@test.com (Manager), admin@test.com (Admin)
- Tech stack: Python FastAPI + PostgreSQL
- Auth: JWT (RS256), tokens expire in 4 hours
- Cloud: AWS, S3 for file uploads
```

### White Box — What to Provide

```
/appsec White box security review of this codebase

Available:
- Source code is in the current workspace
- Key files: src/controllers/OrderController.py, src/middleware/auth.py
- Known concern: the order history endpoint may have IDOR
- Database schema: [attach schema.sql]
- Dependencies: requirements.txt attached
```

---

## 7. Understanding the Pre-Fix Report

### Executive Summary
A 2–3 paragraph plain-English summary of the overall risk. Focus on the last paragraph — it states the deployment readiness recommendation.

### Security Posture Scorecard

```
| # | Domain                      | Score   | Rating        |
|---|----------------------------|---------|---------------|
| 1 | Authentication & Session   | 4.0/10  | High Risk     |  ← needs urgent fix
| 2 | Authorization & IDOR/BOLA  | 2.5/10  | Critical      |  ← emergency
| 3 | Input Validation           | 7.0/10  | Good          |  ← OK
```

**How to read the score:**
- `9.0–10.0` 🟢 — No significant action needed
- `7.0–8.9` 🔵 — Fix in next sprint
- `5.0–6.9` 🟡 — Fix within 30 days
- `3.0–4.9` 🟠 — Fix within 7–14 days
- `0.0–2.9` 🔴 — Emergency response (24–48h)

### Finding Dockets

Each finding is numbered `APP-001`, `APP-002`, etc. and contains:

| Field | What It Means |
| :--- | :--- |
| **Severity** | Critical / High / Medium / Low |
| **CVSS Score** | Numeric risk score (0–10); 9+ = Critical |
| **CVSS Vector** | The exact formula that produced the score |
| **CWE** | The class of weakness (e.g., CWE-89 = SQL Injection) |
| **CVE** | A specific known vulnerability, if applicable |
| **Test Case** | Which TC-ID confirmed this finding |
| **PoC** | A non-destructive HTTP request proving the issue |
| **Fix** | Vulnerable code vs. secure code, in your language |
| **SOC Rule** | SIEM detection rule to catch exploitation attempts |
| **Retest** | Exact steps to confirm the fix was successful |

### Remediation Roadmap

```
Immediate (0–48h):   Fix Critical & High findings
Short-Term (7–14d):  Address Medium findings; add audit logging
Medium-Term (30d):   Rotate secrets; add SCA gate to CI/CD
```

---

## 8. Understanding the 10-Point Scoring System

### How Scores Are Calculated

Each domain is scored 0.0 – 10.0 based on a **rubric** (specific criteria for each score band).

Example — Domain 1 (Authentication):

| Score | What It Means for Your App |
| :---: | :--- |
| **9–10** | MFA required, FIDO2 supported, tokens expire in 15min, CISA KEV mitigated |
| **7–8** | MFA enforced, brute-force lockout active, sessions invalidated on logout |
| **5–6** | MFA optional, token expiry is long (1–8h), password reset is secure |
| **3–4** | No MFA, no lockout, sessions survive logout |
| **0–2** | Auth bypass possible, hardcoded credentials, session fixation |

### Overall Score

```
Overall = Sum of all 11 domain scores ÷ 11
```

Or weighted by application type (Section 3.1 of the skill):
- Payments: Authorization and Cryptography weighted x2
- SaaS: Tenant Isolation weighted x3
- Healthcare: Cryptography and Logging weighted x2

### What to Do With the Score

| Overall Score | Recommended Action |
| :---: | :--- |
| **< 3.0** | Do NOT deploy; emergency security remediation required |
| **3.0 – 4.9** | Block deployment; fix all Critical/High before release |
| **5.0 – 6.9** | Conditional release with documented risk acceptance and 30d remediation plan |
| **7.0 – 8.9** | Release approved; fix remaining findings in next sprint |
| **9.0 – 10.0** | Release approved; maintain security posture |

---

## 9. Using the CVE Library

The CVE Library at `references/cve-library/` contains daily-updated Critical and High CVEs  
from NVD/NIST, organized by AppSec domain.

### Searching the Library

```bash
# Find CVEs related to a specific technology
grep -ri "spring" references/cve-library/

# Find all Critical severity CVEs
grep -r "CRITICAL" references/cve-library/ --include="*.md"

# Find CISA Known Exploited Vulnerabilities (highest priority)
grep -r "CISA KEV" references/cve-library/ --include="*.md"

# Find by CWE class
grep -r "CWE-89" references/cve-library/    # SQL Injection
grep -r "CWE-79" references/cve-library/    # XSS
grep -r "CWE-22" references/cve-library/    # Path Traversal
grep -r "CWE-287" references/cve-library/   # Improper Authentication
grep -r "CWE-798" references/cve-library/   # Hardcoded Credentials
```

### Asking the Agent to Check the Library

```
/appsec Check the CVE library for any known vulnerabilities in express@4.18.2
```
```
/appsec Are there any critical CVEs in our current dependencies? [attach package-lock.json]
```

### How the Agent Uses the Library

When the skill is active and finds a dependency-related issue, it automatically:
1. Searches `references/cve-library/` for matching CVEs
2. Links the CVE ID in the finding docket
3. Flags CISA KEV entries as immediate priority
4. Reports the match in Pre-Fix Report Section 4 (CVE Library Check)

### Library Update Schedule

The library updates **automatically every day at 06:00 UTC (09:00 Cairo time)** via GitHub Actions.  
You can trigger a manual update at any time from:  
**GitHub → Actions → Daily CVE Library Update → Run workflow**

---

## 10. Phase 2: Remediation & Retesting

After you approve the Pre-Fix Report, trigger Phase 2:

```
"Approved. Please fix APP-001 (JWT algorithm confusion) and APP-002 (IDOR on orders endpoint)."
```

The agent will:

### For each finding:
1. **Show the fix** — side-by-side: vulnerable code vs. secure code
2. **Apply the fix** — modify the actual source file
3. **Add a security test** — a regression test that would have caught this
4. **Retest** — run the original TC-ID test case again
5. **Report outcome:**
   - ✅ Verified Fixed
   - ⚠️ Partially Fixed (with explanation of remaining gap)
   - ❌ Not Fixed
   - 📋 Accepted Risk (with your sign-off)

### Retesting a specific finding

```
/appsec Retest APP-001 — I've manually updated the JWT validation middleware
```

### Getting a post-fix score

```
/appsec Generate the post-fix score delta for all findings we fixed today
```

---

## 11. Common Use Cases with Examples

---

### Use Case A: Quick Security Check Before Deployment

```
/appsec Quick pre-deployment check for our user registration and login endpoints.
Gray box — I have the source code for auth module only.
Environment: Staging | Stack: Node.js + Express + MongoDB
Focus: Authentication, session management, and input validation only.
```

---

### Use Case B: Full Application Penetration Test

```
/appsec Full white box security assessment of our e-commerce platform.

Authorization: Signed pentest agreement for staging.shopapp.internal
Stack: Django (Python) + PostgreSQL + Redis + AWS S3
Test accounts:
  - customer@test.com (Standard)
  - vendor@test.com (Vendor role)
  - admin@test.com (Admin)
OpenAPI spec: [attach openapi.yaml]
Source code is in the current workspace.
Application profile: Payments / FinTech (use weighted scoring)
```

---

### Use Case C: Code Review for a Specific Endpoint

```
/appsec Review this controller for security vulnerabilities:
[paste code]

Focus: authorization checks, input validation, and SQL query safety.
Stack: C# ASP.NET Core + Entity Framework + Azure SQL
```

---

### Use Case D: Dependency Vulnerability Scan

```
/appsec Scan our dependencies for known CVEs.
[attach package.json or requirements.txt or pom.xml]

Flag anything with CVSS >= 7.0 and suggest remediation versions.
```

---

### Use Case E: SOC Detection Rule Creation

```
/appsec Write Sigma detection rules for IDOR enumeration attacks on our
/api/v1/invoices/{id} endpoint.
Expected normal user: 1–3 invoice lookups per session.
Suspicious: >20 unique invoice IDs requested from same IP in 60 seconds.
```

---

### Use Case F: Post-Incident Security Review

```
/appsec We had a security incident — a user accessed other users' order data.
The endpoint is GET /api/orders/{orderId}.
Stack: Java Spring Boot + JPA + MySQL
Please assess the authorization model, generate a finding, write a fix,
and create SOC detection rules to prevent recurrence.
```

---

## 12. Tips & Best Practices

### Do This

- ✅ Always start by confirming your authorization scope
- ✅ Provide the application profile (Payments / Healthcare / SaaS / etc.) for weighted scoring
- ✅ Attach OpenAPI specs or source code for faster, more accurate assessment
- ✅ Run the CVE library check on your full dependency manifest regularly
- ✅ Save every Pre-Fix Report — it's your audit trail and evidence of due diligence
- ✅ Track posture scores quarterly to show security improvement over time
- ✅ Review AI-generated findings with a human security engineer before sharing externally

### Avoid This

- ❌ Never skip the Pre-Fix Report step — it's the approval gate
- ❌ Do not use this skill against any system you do not own or have written permission to test
- ❌ Do not treat AI security findings as final without human validation
- ❌ Do not run active testing against production without very explicit authorization
- ❌ Do not share raw assessment output externally without review — it may contain sensitive system details

---

## 13. Troubleshooting

### Skill not loading when I type `/appsec`

1. Check that the SKILL.md file exists at:
   ```
   C:\Users\<you>\.gemini\config\skills\appsec\SKILL.md
   ```
2. Verify the frontmatter at the top of the file has `name: appsec`
3. Restart AGY if you recently added the skill file

### Agent is not generating a Pre-Fix Report before making changes

Remind the agent:
```
Stop — do not make code changes yet. Generate the Pre-Fix Assessment Report first.
```

### CVE library is empty or out of date

Run the updater manually:
```bash
python -X utf8 scripts/update_cve_library.py
```
Or trigger the GitHub Actions workflow manually from the Actions tab.

### NVD API rate limit error during CVE update

The script has built-in rate limiting (max 5 requests per 30 seconds per NVD policy).  
If you see 429 errors, wait 30 seconds and re-run. For high-volume use, register for  
a free NVD API key at https://nvd.nist.gov/developers/request-an-api-key and add it  
as the `NVD_API_KEY` environment variable.

### CVSS score seems too high or too low

Ask the agent to justify the score:
```
/appsec Explain the CVSS breakdown for APP-002. Walk me through each metric.
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│           APPSEC SKILL — QUICK REFERENCE                │
├─────────────────────────────────────────────────────────┤
│  INVOKE        /appsec  or  /internal-appsec-testing    │
├─────────────────────────────────────────────────────────┤
│  MODES         Black Box │ Gray Box │ White Box          │
├─────────────────────────────────────────────────────────┤
│  PHASES        Phase 1: Pre-Fix Report (get approval)   │
│                Phase 2: Remediate + Retest              │
├─────────────────────────────────────────────────────────┤
│  DOMAINS (11)  Auth · Authz/IDOR · Injection · XSS      │
│                API · CSRF · SSRF · Upload · Crypto      │
│                Logging · Supply Chain                   │
├─────────────────────────────────────────────────────────┤
│  SCORING       0–10 per domain │ Rubric-based           │
│                Overall = avg(all 11) or weighted        │
├─────────────────────────────────────────────────────────┤
│  CVE LIBRARY   references/cve-library/                  │
│                Updated daily at 06:00 UTC               │
│                grep -r "keyword" references/cve-library │
├─────────────────────────────────────────────────────────┤
│  LEGAL         Authorized targets only │ See EULA.txt   │
└─────────────────────────────────────────────────────────┘
```

---

*Copyright (c) 2025–2026 Waleed Talaat / Techwaves-egy. All rights reserved.*  
*See [EULA.txt](./EULA.txt) for full terms of use.*
