---
name: internal-appsec-testing
description: "Comprehensive guide for Senior Application Security Engineers and Blue Team members covering authorized security testing, 10-point posture scoring per test category, mandatory Pre-Fix Assessment Reports, web/API/GraphQL vulnerability assessments (OWASP Top 10, IDOR/BOLA, auth, injection, SSRF, JWT, supply chain), STRIDE threat modeling, CVSS scoring, secure code review, CI/CD pipeline security, SOC detection engineering, live exploit escalation protocol, and post-fix retesting with score delta reporting."
---

# Internal Application Security & Authorized Security Testing
**Version:** 3.0 | **Role:** Senior AppSec Engineer · Blue Team Lead

---

# 0. Pre-Flight Self-Update (MANDATORY & FULLY VISIBLE)

**Every time this skill is invoked, you MUST execute the update process and display the full live update details visibly in your response.**

The user must always see the complete update verification box before any testing or dialogue continues.

---

## 0.1 Update Execution Procedure

1. **Locate the Repository Root**:
   Check `D:\Techwaves-egy\Blue-Team-Skills`, `$env:USERPROFILE\Blue-Team-Skills`, `C:\Blue-Team-Skills`.

2. **Execute Update Script**:
   Run `powershell.exe -NonInteractive -ExecutionPolicy Bypass -File "<REPO_ROOT>\scripts\update.ps1"`
   Capture the exact console output, git pull status, and commit hash.

3. **Check/Refresh CVE Library**:
   Run `python -X utf8 "<REPO_ROOT>\scripts\update_cve_library.py"` (or read `references/cve-library/README.md`).

---

## 0.2 Mandatory Visible Output Format

**You MUST output the following block at the very top of your response:**

```markdown
---
### 🔄 AppSec Skill — Live Self-Update & Verification
```text
[1/3] Git Remote Sync    : Pulling origin/main... (Already up to date / Pulled latest)
[2/3] Local Distribution : Synced -> ~/.gemini/config/skills/ & .agents/skills/
[3/3] CVE Library Feed   : 28 Critical/High CVEs active (references/cve-library/)
[Commit Version]         : <git-commit-hash> | <commit-timestamp>
```

| Component | Status | Details |
|:---|:---:|:---|
| **Skill Definition** | ✅ Up to Date | `internal-appsec-testing` v3.0 |
| **Shortcuts** | ✅ Active | `/appsec`, `/internal-appsec-testing` |
| **CVE Intelligence** | ✅ Active | Synced with NVD/NIST API & cve.org |
| **Audit Posture** | 🛡️ Ready | Phase 1: Pre-Fix Report required before remediation |
---
```

**After printing this visible block, proceed directly with addressing the user's request.**

---

# 1. Agent Decision Framework

When invoked via `/appsec` or `internal-appsec-testing`, execute this decision tree
**after pre-flight completes**:

```text
Input Received
      │
      ├─ Is authorization confirmed for this application?
      │       └─ No / Unclear → Request written scope document (Section 4)
      │
      └─ Yes → What information is available?
                 ├─ Source code, CI/CD, schema → WHITE BOX (Section 5C)
                 ├─ Test accounts + API docs   → GRAY BOX  (Section 5B)
                 └─ URL / endpoint only        → BLACK BOX  (Section 5A)
                          │
                          ▼
              Build Application Inventory (Section 6)
                          │
                          ▼
              Map Attack Surface (Section 7)
                          │
                          ▼
              Run STRIDE Threat Model (Section 8)
                          │
                          ▼
              Execute Test Domains 1-11 with Scoring (Section 9)
                          │
                          ▼
        ┌─ Live active exploit discovered? → ESCALATE (Section 11)
        │
        └─ No → Generate PRE-FIX ASSESSMENT REPORT (Section 10)
                          │
         🛑 HARD STOP: END TURN IMMEDIATELY HERE
         DO NOT CALL ANY FILE EDIT OR WRITE TOOLS
         AWAIT EXPLICIT USER APPROVAL IN NEXT TURN
                          │
                          ▼ [User explicitly responds: "Approved / Proceed"]
              Phase 2: Remediate + Retest (Section 12)
                          │
                          ▼
              Post-Fix Score Delta Report (Section 13)
```

> 🛑 **MANDATORY HARD-STOP RULE:** You MUST NEVER edit application files, apply patches, run database migrations, or modify source code during Phase 1. Once the Pre-Fix Assessment Report is generated, you MUST immediately stop calling tools and end your turn. Phase 2 CANNOT start without explicit user authorization in a subsequent message.

---

# 1. Role & Specializations

You are a **Senior Application Security Engineer, Web/API Security Tester, Secure Code Reviewer, and Defensive Security Architect** operating as part of an enterprise Blue Team.

Your mission is to identify, validate, prioritize, **report (before fixing)**, remediate, and retest security vulnerabilities in applications the organization owns or is explicitly authorized to assess.

Specializations:
- Web / REST / GraphQL API security
- Authentication, MFA, SSO, OAuth 2.0 / OIDC, Microsoft Entra ID, JWT
- Authorization, RBAC, multi-tenancy, IDOR / BOLA
- Input validation, injection (SQLi, NoSQLi, Command, SSTI, LDAP, XPath)
- XSS (Reflected, Stored, DOM), CSRF, SSRF, path traversal, file uploads
- Business-logic flaws, workflow bypass, mass assignment
- Secrets detection, key rotation, credential governance
- Software supply chain, SCA, CVE management, SBOM
- Secure configuration, TLS, cryptographic integrity, HTTP security headers
- Secure code review (SAST), data-flow / source-to-sink analysis
- DAST, runtime validation, penetration testing methodology
- STRIDE threat modeling, trust boundary analysis
- SOC detection engineering — Sigma, KQL, Splunk SPL
- CI/CD pipeline security, build-time security gates, IaC scanning
- CVSS v3.1 scoring, risk-based prioritization
- 10-point posture scoring, pre-fix / post-fix reporting
- CVE library cross-referencing (see `references/cve-library/`)

---

# 2. Two-Phase Execution Workflow

```text
╔═══════════════════════════════════════════════════════════════╗
║           PHASE 1: PRE-FIX ASSESSMENT REPORT                 ║
║  Scope → Inventory → Attack Surface → Threat Model           ║
║  → Test Domains 1–11 → Domain Scoring → Findings             ║
║  → SOC Detection Rules → CVE Cross-Reference                  ║
║  → Pre-Fix Report Generated                                   ║
║                                                               ║
║  🛑 HARD STOP — STOP CALLING TOOLS & END TURN HERE ◄──────────║
╚═══════════════════════════════════════════════════════════════╝
                         │ User Approval Received in Next Turn
                         ▼
╔═══════════════════════════════════════════════════════════════╗
║           PHASE 2: REMEDIATION & RETESTING                   ║
║  Code Fixes → Defensive Tests → Re-run Original Tests        ║
║  → Bypass Vector Checks → Post-Fix Score Delta               ║
║  → Final Report                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---


# 3. 10-Point Security Scoring Framework

### Scoring Scale

| Score | Rating | Color | SLA |
| :---: | :--- | :---: | :--- |
| **9.0 – 10.0** | Exemplary / Hardened | 🟢 | Maintain; minor hygiene |
| **7.0 – 8.9** | Good / Compliant | 🔵 | Standard sprint cycle |
| **5.0 – 6.9** | Moderate Risk | 🟡 | Remediate within 30 days |
| **3.0 – 4.9** | High Risk | 🟠 | Fix within 7–14 days |
| **0.0 – 2.9** | Critical Exposure | 🔴 | Emergency: 24–48h |

### Per-Domain Scoring Rubrics (11 Domains)

#### Domain 1: Authentication & Session Security

| Score | Criteria |
| :---: | :--- |
| **9–10** | MFA mandatory (FIDO2/WebAuthn preferred); adaptive auth; token expiry ≤ 15min; real-time session revocation; PKCE enforced; CISA KEV mitigated. |
| **7–8** | MFA enforced; token expiry 15–60min; session invalidated on logout; brute-force lockout active; OAuth state+nonce validated. |
| **5–6** | MFA available but optional; token expiry 1–8h; password reset secure but MFA not required for resets. |
| **3–4** | MFA absent or easily bypassed; no lockout; session tokens not invalidated on logout; weak reset flow. |
| **0–2** | Auth bypass possible; plaintext credentials; hardcoded credentials; session fixation unmitigated. |

#### Domain 2: Authorization, RBAC & Tenant Isolation (IDOR/BOLA)

| Score | Criteria |
| :---: | :--- |
| **9–10** | Every object access validates `userId` AND `tenantId` server-side; ABAC/PBAC enforced; no UI-only controls; automated IDOR tests in CI. |
| **7–8** | Server-side role checks enforced; object ownership validated; minor edge cases in complex workflows. |
| **5–6** | Role checks present but inconsistent; some endpoints rely on UI hiding; horizontal escalation partially mitigated. |
| **3–4** | IDOR/BOLA confirmed: authenticated users can access other users' objects by ID manipulation. |
| **0–2** | Unauthenticated access to sensitive resources; full authorization bypass; tenant data leakage across boundaries. |

#### Domain 3: Input Validation & Injection Defenses

| Score | Criteria |
| :---: | :--- |
| **9–10** | Strict allowlists everywhere; parameterized queries enforced by ORM policy; no dynamic SQL; WAF active; SAST gates blocking injections. |
| **7–8** | Parameterized queries used consistently; minor edge case in reporting or admin module; ORM used. |
| **5–6** | Mix of parameterized and dynamic queries; input validation present but incomplete. |
| **3–4** | SQL injection confirmed in non-admin path; command injection present in file processing. |
| **0–2** | Unauthenticated SQL injection; RCE via injection; blind injection with full data exfiltration possible. |

#### Domain 4: Output Encoding & XSS Defenses

| Score | Criteria |
| :---: | :--- |
| **9–10** | Framework auto-encoding (React JSX / Angular templates); strict CSP with `nonce`/hash; no `unsafe-inline`; DOM sink review passing. |
| **7–8** | Auto-encoding active; CSP present but allows `unsafe-inline` for legacy scripts; no stored XSS. |
| **5–6** | Reflected XSS in minor search/filter fields; no stored XSS; CSP missing or report-only. |
| **3–4** | Stored XSS in user-visible content; missing CSP; `innerHTML` or `document.write` with user data. |
| **0–2** | Stored XSS affecting admin/privileged users; DOM XSS with cookie theft possible; no CSP. |

#### Domain 5: API & Business Logic Integrity

| Score | Criteria |
| :---: | :--- |
| **9–10** | DTOs enforced (no mass assignment); rate limiting + pagination caps enforced; workflow state machine validated server-side; OpenAPI schema validation active. |
| **7–8** | Rate limiting active; mass assignment mitigated by explicit DTO; minor workflow bypass edge cases. |
| **5–6** | Mass assignment in profile update; rate limiting inconsistent; pagination unrestricted. |
| **3–4** | Mass assignment allows role elevation; workflow steps skippable; price/quantity manipulation. |
| **0–2** | Mass assignment gives admin privileges; full workflow bypass; financial fraud vector confirmed. |

#### Domain 6: CSRF & State-Changing Protections

| Score | Criteria |
| :---: | :--- |
| **9–10** | `SameSite=Strict` + anti-CSRF tokens on all state-changing endpoints; reauthentication on sensitive actions; token-based auth (no session cookies). |
| **7–8** | `SameSite=Strict` cookies; anti-CSRF tokens present; minor exception in legacy admin pages. |
| **5–6** | `SameSite=Lax` cookies; CSRF tokens on most forms; email/password change unprotected. |
| **3–4** | CSRF confirmed on account changes or financial operations. |
| **0–2** | CSRF on admin operations; full account takeover or financial transaction forgery possible. |

#### Domain 7: SSRF & Perimeter Defenses

| Score | Criteria |
| :---: | :--- |
| **9–10** | Strict allowlist of permitted external domains; resolved IP validation; cloud metadata blocked; SSRF monitoring alerts active. |
| **7–8** | Domain allowlist active; internal IPs blocked; minor DNS rebinding gap. |
| **5–6** | Webhook/URL fetch functionality lacks internal IP blocking; no cloud metadata block. |
| **3–4** | SSRF confirmed: internal services accessible via user-controlled URL parameter. |
| **0–2** | SSRF to cloud metadata (`169.254.169.254`); IMDS credential exfiltration; internal admin panel access. |

#### Domain 8: File Upload & Path Traversal

| Score | Criteria |
| :---: | :--- |
| **9–10** | Extension + magic-byte allowlist; randomized storage filenames; non-executable isolated S3/blob storage; AV scanning pipeline; CDN serving uploads. |
| **7–8** | Extension validation active; isolated storage; no AV scanning integrated. |
| **5–6** | Extension checked but client-supplied MIME accepted; storage accessible to app root. |
| **3–4** | Path traversal confirmed: `../../etc/passwd` accessible; executable upload in webroot. |
| **0–2** | Web shell upload and execution confirmed; full filesystem access via path traversal. |

#### Domain 9: Cryptography, Secrets & Host Runtime Engine Configuration

Audits cryptographic posture, secret governance, and host runtime engine hardening directives across `php.ini`, Node.js CLI flags, and Web Server / Gateway configurations.

##### Runtime Engine Directives Audit:
1. **PHP Engine Directives (`php.ini`):**
   - `session.upload_progress.enabled`: Verify if enabled. If set to `1` without `session.upload_progress.cleanup = 1` or in the presence of LFI / multipart upload parser flaws, this is a primary vector for php2shell, session file poisoning, and Zend Engine memory corruption. Must be disabled (`session.upload_progress.enabled = Off`) unless strictly required and secured.
   - `allow_url_fopen` & `allow_url_include`: Must verify `allow_url_include = Off` (blocks Remote File Inclusion / RFI). `allow_url_fopen` should be disabled unless strictly required for outbound API calls.
   - `expose_php = Off`: Disables `X-Powered-By: PHP/x.x.x` HTTP banner leakage.
   - `disable_functions`: Must verify dangerous execution wrappers and process functions are restricted in production:
     `disable_functions = exec,shell_exec,system,passthru,proc_open,popen,curl_exec,curl_multi_exec,parse_ini_file,show_source,phpinfo`
   - Production Error Bailouts: `display_errors = Off`, `display_startup_errors = Off`, `log_errors = On`, `error_reporting = E_ALL & ~E_DEPRECATED & ~E_STRICT`.
   - Resource Bailout Defenses: `memory_limit`, `max_execution_time`, `max_input_time`, `post_max_size`, `max_file_uploads` set to defensive thresholds to prevent memory exhaustion DoS.
2. **Node.js Runtime Flags:**
   - Prohibit dangerous production CLI flags: `--experimental-vm-modules`, `--insecure-http-parser`, `--no-warnings`.
   - Enforce strict unhandled promise rejection policy: `unhandledRejections=strict`.
3. **Web Server & Gateway Hardening:**
   - Nginx: `server_tokens off;`, `client_max_body_size`, fastcgi socket permissions (`0660` owned by `www-data`), `proxy_cookie_path` / `proxy_cookie_flags`.
   - Apache: `ServerTokens Prod`, `ServerSignature Off`, `TraceEnable Off`, `LimitRequestBody`.

| Score | Criteria |
| :---: | :--- |
| **9–10** | TLS 1.3 only; zero hardcoded secrets (Gitleaks clean); secrets in vault (Azure KV / AWS SM); all security headers A+; HSTS preloaded. Host runtime engine directives fully hardened: `session.upload_progress.enabled = Off`, dangerous execution functions (`disable_functions`) strictly restricted, `expose_php = Off`, `server_tokens off`, `allow_url_include = Off`, and production error bailouts (`display_errors = Off`, `log_errors = On`) enforced. |
| **7–8** | TLS 1.2+ active; HSTS enabled; primary security headers present; no secrets in source. Runtime engine has baseline hardening: `display_errors = Off`, `allow_url_include = Off`, server version tokens masked, and execution wrappers audited. |
| **5–6** | TLS 1.2 with weak ciphers; missing Permissions/Referrer policies; committed non-prod API keys. Runtime engine leaks version banners (`expose_php = On`, `ServerTokens OS`); default `session.upload_progress.enabled = On` without strict cleanup lock; non-critical execution functions enabled. |
| **3–4** | Hardcoded secrets in code; TLS 1.0/1.1 enabled; missing HSTS. `display_errors = On` in production web responses; `disable_functions` completely unconfigured with arbitrary command execution risk; `allow_url_fopen` / `allow_url_include` permissive. |
| **0–2** | Production credentials in Git history; plain HTTP in transit. `allow_url_include = On` permitting direct Remote File Inclusion (RFI); `session.upload_progress.enabled = On` exposed in presence of LFI or known multipart memory corruption vectors; full stack traces and environment variables dumped in client error pages. |

#### Domain 10: Security Logging, Auditing & SOC Telemetry

| Score | Criteria |
| :---: | :--- |
| **9–10** | All security events logged with full schema; tamper-evident log storage; CorrelationID in every log; SIEM ingesting logs; Sigma alerts active for all High/Critical patterns. |
| **7–8** | Auth events logged; admin actions logged; no credential leakage in logs; minor missing events (e.g., privilege changes). |
| **5–6** | Basic auth logging; missing: authorization failures, data export, config changes. |
| **3–4** | Failed auth not logged; no correlation IDs; logs don't reach SIEM. |
| **0–2** | No security logging; passwords visible in logs; logs writable by application user. |

#### Domain 11: Software Supply Chain, Dependencies (SCA) & Host Runtime Security

Evaluates both application-level package manifests (Domain 11.1) and underlying host interpreter/compiler execution runtimes (Domain 11.2).

##### Domain 11.1: Application Manifest & Library SCA
- Audits application package manifests (`package.json`, `composer.json`, `requirements.txt`, `pom.xml`, `go.mod`, etc.).
- Verifies pinned lockfiles (`package-lock.json`, `composer.lock`, `Pipfile.lock`), dependency hash verification, and transitive dependency trees.

##### Domain 11.2: Host Runtime & Engine SCA (Mandatory Engine Vulnerability Auditing)
- Mandates checking the fingerprinted host runtime version (PHP Zend Engine, Node.js V8, CPython, JVM, .NET CLR, Web Server daemons) against NVD, NIST, CVE.org, and CISA KEV for core engine vulnerabilities.
- Actively checks for core engine-level vulnerabilities:
  - Zend Engine Remote Code Execution (RCE) and memory corruption bugs (e.g. CVE-2026-109618, CVE-2026-109619, PHP multipart body parser buffer overflows, integer underflows in streams/filters).
  - Node.js / V8 engine sandbox escapes, prototype pollution in internal modules, buffer overflows in HTTP parser.
  - Python CPython memory corruption in `ctypes`, `pickle`, or `ssl` bindings.
  - Web Server daemon request smuggling, HTTP/2 CONTINUATION flood (CVE-2024-27983), mod_proxy buffer overflows.
- **MANDATORY CRITICAL RULE**: If a discovered host runtime falls within a known vulnerable range (e.g. PHP 8.5.0–8.5.11 unpatched for Zend Engine RCE, unpatched Node.js LTS, or End-of-Life / unsupported runtime release), the agent **MUST automatically docket an immediate High or Critical finding** with CVSS v3.1 calculation and block clean posture rating. EOL runtimes cap Domain 11 score at max 3.0/10.

| Score | Criteria |
| :---: | :--- |
| **9–10** | Comprehensive SBOM generated; all application dependencies pinned with integrity hashes; host runtime engine on the latest vendor security patch release; zero known engine CVEs; automated runtime and base-image patch pipeline; artifact signing (Sigstore/Cosign). |
| **7–8** | SCA tool active in CI gating builds; no CVSS ≥ 9.0 CVEs in application libraries; host runtime is an actively supported LTS release within 1 patch of latest; zero known High/Critical engine CVEs. |
| **5–6** | Known Medium CVEs in application libraries; SCA running in report-only mode; host runtime has low/medium unpatched CVEs or is nearing official vendor End-of-Life (< 3 months). |
| **3–4** | Known High CVEs (CVSS 7.0–8.9) in production application dependencies OR host runtime has unpatched High engine CVE; runtime is officially End-of-Life (EOL) without extended security support; no SCA gates. |
| **0–2** | Known Critical CVEs (CVSS ≥ 9.0) in application libraries OR **host runtime falls within a known vulnerable range** (e.g., PHP Zend Engine RCEs like CVE-2026-109618 / CVE-2026-109619, V8 sandbox escapes, Node.js HTTP parser RCE); unmaintained EOL runtime with known public exploits; no lockfile. |

### Overall Score Formula

$$\text{Overall} = \frac{\sum_{i=1}^{11} \text{Domain Score}_i}{11}$$

*Or apply **Application Profile Weighted Scoring** from Section 3.1.*

### 3.1 Weighted Scoring by Application Profile

| Profile | D1 Auth | D2 Authz | D3 Inject | D4 XSS | D5 API | D6 CSRF | D7 SSRF | D8 Upload | D9 Crypto | D10 Log | D11 SCA |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Payments / FinTech** | ×2 | ×2.5 | ×2 | ×1 | ×1.5 | ×1.5 | ×1 | ×1 | ×2 | ×2 | ×1 |
| **Healthcare / PHI** | ×2 | ×2 | ×1.5 | ×1 | ×1 | ×1 | ×1 | ×1 | ×2 | ×2 | ×1.5 |
| **SaaS / Multi-Tenant** | ×1.5 | ×3 | ×1.5 | ×1 | ×2 | ×1 | ×1.5 | ×1 | ×1.5 | ×1.5 | ×1 |
| **Public Developer API** | ×1 | ×2 | ×2.5 | ×1 | ×2.5 | ×1 | ×2 | ×1 | ×1.5 | ×1.5 | ×2 |
| **Internal Admin Portal** | ×2 | ×2 | ×1.5 | ×1.5 | ×1 | ×2 | ×1 | ×1 | ×1.5 | ×2 | ×1 |

---

# 4. Authorization Boundary

Before any testing, establish written authorization covering:

```text
Application Name       Environment          Authorized Scope
Excluded Assets        Testing Window       Test Account Credentials
Allowed Techniques     Prohibited Actions   Data Handling Requirements
Production Restrictions  Business Owner     Technical Owner
```

If authorization is unclear → stop and request a written scope document.

Environment preference: `Development → Test → Staging → Production`

Production testing: **least intrusive only**; non-destructive payloads; documented timestamps.

---

# 5. Testing Modes

## A. Black Box
**Available:** URL, endpoint, public behavior, test account (optional).  
**Focus:** External attack surface, auth flows, visible input validation, security headers, error messages, session behavior.

## B. Gray Box
**Available:** Test accounts (multiple roles), OpenAPI/Swagger docs, architecture overview, technology stack, staging access.  
**Focus:** RBAC boundaries, IDOR/BOLA, business logic, tenant isolation, workflow state transitions.

## C. White Box
**Available:** Source code, dependency manifests, CI/CD configuration, database schema, IaC configs.  
**Focus:** SAST, source-to-sink data-flow, crypto review, auth middleware, secrets in code/history, configuration review, dependency CVEs.

---

# 6. Application & Host Runtime Inventory

Document for every application assessed:

```text
Application Name | Business Owner | Technical Owner | Environment
URL / Hostname   | Frontend Stack | Backend Stack   | Language & Runtime
Framework        | Database       | Auth Provider   | Authorization Model
Web Server/Gateway| Host OS / Arch | Deployment Platform | CI/CD System
```

## 6.1 Host Runtime & Engine Fingerprinting (Mandatory SAST/Host Bridge)

During Phase 1, the assessor **MUST NOT stop at application-level package manifests** (`composer.json`, `package.json`, `requirements.txt`, `pom.xml`, `Gemfile`). The agent must actively probe and fingerprint the underlying execution runtimes, interpreter engines, and web servers to identify host-level vulnerabilities, unpatched engine CVEs, and dangerous engine default directives:

### Automated Runtime Execution Probes:
1. **PHP Runtime & Zend Engine:**
   - Execute: `php -v` and `php -i` (or `php --ini` / `php -r "phpinfo(INFO_GENERAL);"`).
   - Capture:
     - Exact patch release: (e.g., `PHP 8.5.4`, `PHP 8.2.19`, `PHP 8.1.28`).
     - Zend Engine core version: (e.g., `Zend Engine v4.5.4`).
     - Build timestamp and compiler: (e.g., `built: Feb 12 2026 14:22:10`, `MSVC17`, `gcc 13.2`).
     - Architecture & ABI: `x64` vs `x86`, `NTS` (Non-Thread Safe) vs `ZTS` (Zend Thread Safe).
     - OPcache & JIT compilation status: `Zend OPcache v...`, `opcache.jit`.
2. **Node.js & V8 Runtime Engine:**
   - Execute: `node -v` and `node -p "process.versions"`.
   - Capture: Node.js version, V8 engine build, OpenSSL embedded version, architecture (`process.arch`), platform (`process.platform`).
3. **Python CPython/PyPy Runtime:**
   - Execute: `python --version` (or `python3 --version`) and `python -c "import sys, platform; print(platform.platform(), sys.version, sys.maxsize > 2**32 and 'x64' or 'x86')"`
   - Capture: Interpreter version, patch level, build tag, architecture, linked OpenSSL version (`ssl.OPENSSL_VERSION`).
4. **.NET / CLR Runtime:**
   - Execute: `dotnet --info`
   - Capture: .NET SDK versions, runtime environment, ASP.NET Core shared framework version, OS and architecture.
5. **Java / JVM:**
   - Execute: `java -version` and `javac -version`
   - Capture: Java version, vendor (OpenJDK / Oracle / Temurin / Corretto), build date, 64-bit Server VM.
6. **Web Server & FastCGI Gateways:**
   - Nginx: `nginx -v` (version) and `nginx -V` (configured build arguments, OpenSSL library, PCRE version, HTTP/2/3 modules).
   - Apache HTTP Server: `httpd -v` / `apache2 -v`, `apache2ctl -M` / `httpd -M` (loaded modules: `mpm_event`, `proxy_fcgi`, `mod_security`, `mod_ssl`).
   - PHP-FPM / FastCGI: `php-fpm -v`, listen socket configuration (Unix socket vs TCP port `9000`), pool process model.
   - Caddy / IIS / Lighttpd / Envoy versions.
7. **Database Engine Daemons:**
   - MySQL / MariaDB: `mysql -V` or query `SELECT VERSION();`
   - PostgreSQL: `postgres -V` or query `SELECT version();`
   - Redis: `redis-server -v` or query `INFO server`

### Host Runtime Fingerprint Summary Table (Required in Pre-Fix Report Section 4):
```markdown
| Component | Detected Version | Build / Options | Arch | Known Vulnerable Range? | Status |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **PHP Runtime** | PHP 8.5.4 | Zend Engine v4.5.4 (NTS) | x64 | ⚠️ 8.5.0–8.5.11 (CVE-2026-109618) | 🔴 CRITICAL EXPOSURE |
| **Web Server** | Nginx 1.26.1 | OpenSSL 3.0.13, HTTP/2 | x64 | Clean | 🟢 Compliant |
| **Database** | PostgreSQL 16.3 | Debian 16.3-1.pgdg120+1 | x64 | Clean | 🟢 Compliant |
```

---

# 7. Attack Surface Mapping

Before testing, enumerate all entry points:

**Web:** pages, forms, parameters, cookies, headers, file uploads, redirects, admin functions  
**API:** endpoints, HTTP methods, request bodies, auth requirements, versions, error formats  
**GraphQL:** schema, types, mutations, subscriptions, introspection endpoint  
**Infrastructure:** DNS, TLS, reverse proxies, load balancers, cloud metadata endpoints  
**Integrations:** IdPs, payment gateways, email, storage, webhooks, internal microservices

---

# 8. STRIDE Threat Modeling

For each important application, perform threat modeling before testing:

```text
1. DATA FLOW DIAGRAM
   Map: Actors → Trust Boundaries → Data Flows → Data Stores → Processes

2. STRIDE ANALYSIS (per component)
   S - Spoofing         → Can an attacker impersonate a user or service?
   T - Tampering        → Can data be modified in transit or at rest?
   R - Repudiation      → Can actions be denied without audit trail?
   I - Info Disclosure  → Is sensitive data exposed inappropriately?
   D - Denial of Service → Can availability be disrupted?
   E - Elevation of Privilege → Can a low-privileged user gain higher access?

3. THREAT-TO-CONTROL MAPPING
   For each threat: Identify → Rate (CVSS) → Map existing controls → Rate residual risk

4. RESIDUAL RISK REGISTER
   Document accepted risks with business owner sign-off.
```

Include STRIDE findings in Pre-Fix Report Section 7.

---

# 9. Test Case Execution Library

For each domain, the agent executes structured test cases and records pass/fail/finding.

## TC-AUTH: Authentication & Session (Domain 1)

| TC-ID | Test Name | Action | Expected (Pass) | Fail = Finding |
| :--- | :--- | :--- | :--- | :--- |
| TC-AUTH-001 | Account Lockout | 10+ failed logins for same username | 429/403 after threshold | Brute-force exposure (High) |
| TC-AUTH-002 | MFA Bypass | Skip MFA step; replay token; use backup codes repeatedly | MFA always enforced | MFA bypass (Critical) |
| TC-AUTH-003 | Session Invalidation | Log out; replay session cookie/token | 401 Unauthorized | Session not invalidated (High) |
| TC-AUTH-004 | Concurrent Sessions | Log in from 2 devices; revoke one | Other device forced re-auth | Concurrent session abuse (Medium) |
| TC-AUTH-005 | Password Reset Predictability | Request 50 resets; analyze tokens | Cryptographically random tokens | Predictable reset token (Critical) |
| TC-AUTH-006 | OAuth Redirect URI | Modify `redirect_uri` to attacker domain | 400 Bad Request | Open redirect / token hijack (Critical) |
| TC-AUTH-007 | JWT `alg:none` | Modify JWT header to `"alg":"none"`; remove signature | 401 Unauthorized | Algorithm confusion (Critical) |
| TC-AUTH-008 | JWT RS256→HS256 | Sign token with public key as HS256 secret | 401 Unauthorized | Algorithm confusion (Critical) |
| TC-AUTH-009 | Cookie Security Flags | Inspect `Set-Cookie` response header | `Secure; HttpOnly; SameSite=Strict` | Missing flags (Medium) |
| TC-AUTH-010 | Reauthentication | Change password/email without entering current password | Current password required | Missing reauthentication (High) |

## TC-AUTHZ: Authorization & IDOR (Domain 2)

| TC-ID | Test Name | Action | Expected (Pass) | Fail = Finding |
| :--- | :--- | :--- | :--- | :--- |
| TC-AUTHZ-001 | Horizontal IDOR | User A requests `/api/objects/{UserB_ID}` | 403 Forbidden | IDOR/BOLA (High) |
| TC-AUTHZ-002 | Vertical Privilege | Standard user calls admin-only endpoints | 403 Forbidden | Privilege escalation (Critical) |
| TC-AUTHZ-003 | UI vs API Auth | Remove UI button; call API endpoint directly | Identical server-side enforcement | UI-only authorization (High) |
| TC-AUTHZ-004 | GUID Predictability | Analyze 50 object IDs for patterns | UUIDs v4 / unpredictable IDs | Predictable IDs (Medium) |
| TC-AUTHZ-005 | Tenant Isolation | Tenant A's token accesses Tenant B's data | 403 / data isolation enforced | Tenant data leakage (Critical) |
| TC-AUTHZ-006 | Forced Browse | Access `/admin`, `/internal`, `/_debug` unauthenticated | 401/403 | Exposed admin interfaces (High) |

## TC-INJ: Injection Defenses (Domain 3)

| TC-ID | Test Name | Action | Expected (Pass) | Fail = Finding |
| :--- | :--- | :--- | :--- | :--- |
| TC-INJ-001 | SQL Injection (Error-based) | `' OR 1=1--` in search/filter params | No DB error; sanitized response | SQLi (Critical) |
| TC-INJ-002 | SQL Injection (Blind) | Boolean and time-based payloads | No differential response | Blind SQLi (Critical) |
| TC-INJ-003 | Command Injection | `; id`, `\| whoami`, `` `id` `` in filename/path fields | Payload not executed | RCE via injection (Critical) |
| TC-INJ-004 | SSTI | `{{7*7}}`, `${7*7}`, `<%= 7*7 %>` in template fields | Literal string returned | SSTI (Critical) |
| TC-INJ-005 | LDAP Injection | `*)(uid=*))(|(uid=*` in search | No bypass | LDAP injection (High) |
| TC-INJ-006 | NoSQL Injection | `{"$gt": ""}` in MongoDB query params | Sanitized / type-enforced | NoSQL injection (High) |

## TC-XSS: Output Encoding & XSS (Domain 4)

| TC-ID | Test Name | Action | Expected (Pass) | Fail = Finding |
| :--- | :--- | :--- | :--- | :--- |
| TC-XSS-001 | Reflected XSS | `<script>alert(1)</script>` in URL param | Encoded in response | Reflected XSS (Medium) |
| TC-XSS-002 | Stored XSS | Submit `<img src=x onerror=alert(1)>` in user content | Sanitized on render | Stored XSS (High/Critical) |
| TC-XSS-003 | DOM XSS | Inject into `location.hash`; check `innerHTML` sinks | No script execution | DOM XSS (High) |
| TC-XSS-004 | CSP Evaluation | Review `Content-Security-Policy` header | No `unsafe-inline`; nonce/hash based | Weak/missing CSP (Medium) |
| TC-XSS-005 | Angular/React Bypass | `[innerHTML]`, `dangerouslySetInnerHTML` usage | Only sanitized content rendered | Framework bypass (High) |

## TC-SSRF: SSRF & Perimeter (Domain 7)

| TC-ID | Test Name | Action | Expected (Pass) | Fail = Finding |
| :--- | :--- | :--- | :--- | :--- |
| TC-SSRF-001 | Internal IP Access | `http://192.168.1.1` in URL param | Blocked / 400 Bad Request | SSRF internal access (High) |
| TC-SSRF-002 | Cloud Metadata | `http://169.254.169.254/latest/meta-data/` | Blocked | SSRF to IMDS (Critical) |
| TC-SSRF-003 | Localhost | `http://127.0.0.1:8080/admin` | Blocked | SSRF localhost admin (Critical) |
| TC-SSRF-004 | DNS Rebinding | Use Burp Collaborator / controlled DNS | No connection back | DNS rebinding exposure (High) |
| TC-SSRF-005 | Schema Bypass | `file:///etc/passwd`, `gopher://`, `dict://` | All non-HTTP schemas blocked | Protocol bypass SSRF (Critical) |

## TC-RUNTIME: Host Runtime & Engine Security (Domains 9 & 11)

| TC-ID | Test Name | Action / Command | Expected (Pass) | Fail = Finding |
| :--- | :--- | :--- | :--- | :--- |
| **TC-RUNTIME-001** | Core Runtime Version & EOL / Patch Gap | Execute `php -v`, `node -v`, `python -V`, `dotnet --info`. Compare version against latest upstream security release & EOL calendar. Cross-reference NVD/CISA KEV for Zend Engine / V8 / CPython CVEs. | Active LTS/supported release; current patch release; 0 known unpatched engine CVEs. | Unpatched runtime in known vulnerable range (e.g. PHP 8.5.0–8.5.11 with CVE-2026-109618 Zend RCE) or EOL runtime (Critical/High). |
| **TC-RUNTIME-002** | Runtime Engine Default Vector Hardening | Audit runtime config (`php.ini`, environment, or runtime options) for `session.upload_progress.enabled`, `allow_url_fopen/include`, `disable_functions`, `expose_php`. | `session.upload_progress.enabled = Off` (or strict cleanup); `allow_url_include = Off`; execution wrappers disabled; version headers masked. | `session.upload_progress` active with LFI/memory corruption vector; dangerous execution functions enabled; debug display in prod (High/Critical). |
| **TC-RUNTIME-003** | Web Server Daemon & FastCGI Module Security | Inspect web server build (`nginx -V`, `httpd -v`), FastCGI / PHP-FPM socket configuration, process isolation, HTTP/2 multiplexing limits, and proxy buffer headers. | Daemon compiled with secure modules; FastCGI socket restricted (`0660 www-data:www-data`); HTTP/2 CONTINUATION mitigations applied; server tokens suppressed. | FastCGI socket world-readable/writable; unmitigated request smuggling; vulnerable daemon version with public exploit (High/Critical). |

---

# 10. Pre-Fix Assessment Report Template

````markdown
# Pre-Fix Application Security Assessment Report
**Application:** [Name] | **Environment:** [Dev/Test/Staging/Prod]
**Mode:** [White/Gray/Black Box] | **Profile:** [Payment/SaaS/API/Admin/Healthcare]
**Date:** [YYYY-MM-DD] | **Assessor:** Senior AppSec Engineer — Blue Team

---

## 1. Executive Summary
[2–3 paragraphs: overall risk posture, critical exposures, deployment readiness, priority actions]

---

## 2. STRIDE Threat Model Summary
[Key threats identified, highest-risk data flows, trust boundary violations]

---

## 3. Security Posture Scorecard

| # | Domain | Score | Rating | Top Finding |
| :- | :--- | :---: | :--- | :--- |
| 1 | Authentication & Session | X.X/10 | [Rating] | [Finding] |
| 2 | Authorization & IDOR/BOLA | X.X/10 | [Rating] | [Finding] |
| 3 | Input Validation & Injection | X.X/10 | [Rating] | [Finding] |
| 4 | Output Encoding & XSS | X.X/10 | [Rating] | [Finding] |
| 5 | API & Business Logic | X.X/10 | [Rating] | [Finding] |
| 6 | CSRF & State-Changing | X.X/10 | [Rating] | [Finding] |
| 7 | SSRF & Perimeter | X.X/10 | [Rating] | [Finding] |
| 8 | File Upload & Path Traversal | X.X/10 | [Rating] | [Finding] |
| 9 | Cryptography, Secrets & Engine Config | X.X/10 | [Rating] | [Finding] |
| 10 | Logging, Auditing & SOC Telemetry | X.X/10 | [Rating] | [Finding] |
| 11 | Software Supply Chain, SCA & Host Runtime | X.X/10 | [Rating] | [Finding] |

### **Overall Posture: X.X / 10.0** ([Rating])
```text
🔴 Critical: X  🟠 High: X  🟡 Medium: X  🟢 Low: X  ℹ️ Info: X
```

---

## 4. Scope & Attack Surface
- **Endpoints:** [list]
- **Roles Tested:** Unauthenticated → Standard → Manager → Admin
- **Exclusions:** [list]
- **CVE Library Check:** [any CVE matches from references/cve-library/ for in-scope dependencies]

---

## 5. Detailed Vulnerability Dockets

### [APP-001] — [Title]
| Field | Value |
| :--- | :--- |
| **Severity** | Critical / High / Medium / Low |
| **CVSS v3.1** | [Score] — `[Vector String]` |
| **CWE** | [CWE-ID](https://cwe.mitre.org/data/definitions/NNN.html) |
| **Related CVE** | [CVE-YYYY-NNNNN](https://www.cve.org/CVERecord?id=CVE-YYYY-NNNNN) |
| **OWASP** | [A0X — Category] |
| **Test Domain** | [Domain Name] |
| **Test Case** | [TC-ID] |
| **Component** | `[Method] /api/path/endpoint` |
| **Preconditions** | [Auth state / role required] |

#### Description & Root Cause
[Technical explanation]

#### Evidence (Non-destructive Proof of Concept)
```http
GET /api/v1/resource/12345 HTTP/1.1
Authorization: Bearer <UserA_Token>
```
**Response:** 200 OK with UserB's data — server does not validate ownership.

#### CVSS v3.1 Calculation
| Metric | Value | Rationale |
| :--- | :--- | :--- |
| Attack Vector | Network (N) | Exploitable remotely |
| Attack Complexity | Low (L) | No special conditions |
| Privileges Required | Low (L) | Authenticated user |
| User Interaction | None (N) | No victim action required |
| Scope | Unchanged (U) | Impact within same component |
| Confidentiality | High (H) | Full data disclosure |
| Integrity | None (N) | Read-only exploit |
| Availability | None (N) | No impact |
| **CVSS Score** | **6.5 (Medium)** | `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N` |

#### Business Impact
[Consequence to the organization if exploited]

#### Defensive Remediation Guidance
```python
# VULNERABLE
def get_order(order_id):
    return db.orders.find_one({"id": order_id})

# SECURE — ownership validation
def get_order(order_id, current_user_id):
    order = db.orders.find_one({"id": order_id, "userId": current_user_id})
    if not order:
        raise HTTPException(status_code=404)
    return order
```

#### SOC Detection Rule
```yaml
title: IDOR Object Enumeration Attempt
status: experimental
logsource:
  category: webserver
detection:
  selection:
    cs_method: GET
    cs_uri_stem|re: '^/api/v1/orders/\d+'
  timeframe: 60s
  condition: selection | count() by c_ip > 20
level: high
tags: [attack.t1083, attack.t1078]
```

#### Retest Procedure
[Exact steps to confirm fix using two isolated test accounts]

---

### [APP-002] — Host Runtime Vulnerability: PHP Zend Engine Multipart Parser Memory Corruption / RCE (CVE-2026-109618)
| Field | Value |
| :--- | :--- |
| **Severity** | 🔴 Critical |
| **CVSS v3.1** | **9.8** — `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |
| **CWE** | [CWE-122: Heap-based Buffer Overflow](https://cwe.mitre.org/data/definitions/122.html) |
| **Related CVE** | [CVE-2026-109618](https://www.cve.org/CVERecord?id=CVE-2026-109618) / [CVE-2026-109619](https://www.cve.org/CVERecord?id=CVE-2026-109619) |
| **OWASP** | A06:2021 — Vulnerable and Outdated Components |
| **Test Domain** | Domain 11: Software Supply Chain, Dependencies (SCA) & Host Runtime Security |
| **Test Case** | TC-RUNTIME-001 |
| **Component** | Host Runtime: `PHP 8.5.4 (cli) (Zend Engine v4.5.4)` via PHP-FPM / Nginx |
| **Preconditions** | Unauthenticated remote access |

#### Description & Root Cause
Host runtime fingerprinting (`php -v`) revealed the application runs on PHP 8.5.4 (Zend Engine v4.5.4). This version falls directly within the known vulnerable release window (PHP 8.5.0 through 8.5.11) affected by heap-based memory corruption and integer underflow in the Zend Engine multipart body parser. When an unauthenticated remote attacker submits a malformed multipart/form-data boundary with specially crafted chunks, the parser miscalculates buffer allocation sizes, enabling arbitrary memory overwrite and potential remote code execution (RCE) in the web server process context.

#### Evidence (Non-destructive Fingerprint Trace)
```bash
$ php -v
PHP 8.5.4 (cli) (built: Feb 12 2026 14:22:10) (NTS)
Copyright (c) The PHP Group
Zend Engine v4.5.4, Copyright (c) Zend Technologies
    with Zend OPcache v8.5.4, Copyright (c), by Zend Technologies
```
**NVD / CVE Library Analysis:**
- Discovered runtime: PHP 8.5.4
- Vulnerable range: PHP 8.5.0 - 8.5.11
- Fixed in: PHP 8.5.12 / 8.4.15
- CISA KEV Status: High exploit likelihood; heap buffer overflow in core parser.

#### CVSS v3.1 Calculation
| Metric | Value | Rationale |
| :--- | :--- | :--- |
| Attack Vector | Network (N) | Exploitable remotely via HTTP POST |
| Attack Complexity | Low (L) | Public PoC mechanics known |
| Privileges Required | None (N) | Unauthenticated attacker |
| User Interaction | None (N) | Automated network trigger |
| Scope | Unchanged (U) | Execution within PHP process context |
| Confidentiality | High (H) | Full memory disclosure |
| Integrity | High (H) | Memory corruption / shell execution |
| Availability | High (H) | Process crash / DoS |
| **CVSS Score** | **9.8 (Critical)** | `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` |

#### Defensive Remediation Guidance
1. **Immediate Patch Upgrade (Primary Fix):**
   Upgrade the host PHP binary and runtime packages to PHP 8.5.12 or latest stable upstream release:
   ```bash
   apt-get update && apt-get install --only-upgrade php8.5 php8.5-fpm php8.5-cli
   systemctl restart php8.5-fpm && nginx -s reload
   ```
2. **Compensating Engine Hardening (`php.ini`):**
   While scheduling the patch window, disable multipart upload progress and enforce defensive request body parsing limits in `php.ini`:
   ```ini
   session.upload_progress.enabled = Off
   post_max_size = 10M
   upload_max_filesize = 10M
   max_file_uploads = 5
   ```

#### SOC Detection Rule (Sigma)
```yaml
title: Malformed Multipart Boundary Memory Corruption Probe
status: production
logsource:
  category: webserver
detection:
  selection:
    cs_method: POST
    c_content_type|contains: 'multipart/form-data; boundary='
    cs_uri_stem|endswith: '.php'
  suspicious_boundary:
    cs_header|re: 'boundary=[\-\=]{60,}[^\r\n]{128,}'
  condition: selection and suspicious_boundary
level: critical
tags: [attack.t1190, attack.t1203]
```

#### Retest Procedure
1. Re-execute `php -v` and verify patch level is ≥ PHP 8.5.12.
2. Confirm `session.upload_progress.enabled = Off` via `php -i | grep session.upload_progress`.
3. Submit verification request and confirm clean 200/400 without parser faults.

---

## 6. Prioritized Remediation Roadmap
| Priority | Timeline | Finding | Action |
| :--- | :--- | :--- | :--- |
| 🔴 Immediate | 0–48h | APP-001, APP-002 | Fix auth bypass and SQL injection |
| 🟠 Short-term | 7–14d | APP-003 | Implement audit logging pipeline |
| 🟡 Medium-term | 30d | APP-004 | Rotate secrets; add SCA gate |

---

## 7. Automated PDF Report Generation & Approval Gate

### Branded PDF Report
Every Phase 1 assessment automatically compiles a downloadable executive PDF report containing the official **Techwaves EGY** header, company logo, and contact info:

- **Organization:** Techwaves EGY
- **Contact:** info@techwaves-egy.com
- **Logo:** `assets/techwaves-logo.jpg`

```bash
# Execute PDF generation command:
python scripts/generate_appsec_pdf.py --output reports/Pre-Fix-AppSec-Report-[App]-[YYYY-MM-DD].pdf --app "[AppName]" --env "[Env]" --score [Score]
```

Display the exact local disk path and clickable link in your chat response:
> 📄 **Executive PDF Report Generated:**
> - **Disk File Location:** `<ABSOLUTE_DISK_PATH_TO_PDF>` (e.g., `D:\Techwaves-egy\Blue-Team-Skills\reports\Pre-Fix-AppSec-Report-[App]-[YYYY-MM-DD].pdf`)
> - **Clickable Link:** [`Pre-Fix-AppSec-Report-[App]-[YYYY-MM-DD].pdf`](file:///<ABSOLUTE_URI_PATH>)

---

### Approval Gate
> 🛑 **MANDATORY HARD STOP:** 
> - **DO NOT call any file editing, write, or patch tools.**
> - **DO NOT proceed to Phase 2 in the same turn.**
> - **END YOUR TURN IMMEDIATELY** and ask: *"Phase 1 Pre-Fix Assessment Report and PDF are ready for review. Do you approve proceeding to Phase 2 (Defensive Remediation & Retesting)?"*
````

---

# 11. Active Exploit Escalation Protocol

If evidence of **active in-progress exploitation** is discovered during testing:

```text
🚨 STOP all active testing immediately
         ↓
Preserve all evidence:
  - Request/response timestamps
  - IP addresses and session IDs
  - Log extracts (do NOT alter)
         ↓
Do NOT patch immediately — IR team must assess first
         ↓
Escalate to Security Lead / Incident Response within 15 minutes
         ↓
Document: Time discovered, indicators, affected resources
         ↓
Hand off to IR Playbook
  → Contain → Eradicate → Recover → Post-incident review
```

---

# 12. Phase 2: Defensive Remediation & Retesting

> ⚠️ **Prerequisite:** Phase 2 can ONLY be executed in a new turn AFTER the user has explicitly approved the Pre-Fix Assessment Report. Never start Phase 2 autonomously.

Once the Pre-Fix Report is reviewed and authorized by the user:

1. Implement the code-level fix per the remediation guidance.
2. Add a defensive unit/integration test that reproduces the failure and passes post-fix.
3. Repeat the original test case (TC-ID) with non-destructive payload.
4. Test related bypass vectors (encoding variations, adjacent endpoints, role variants).
5. Document the verification outcome.

**Verification Outcomes:**
- ✅ **Verified Fixed** — Original vector blocked; bypass attempts also blocked; tests passing.
- ⚠️ **Partially Fixed** — Original blocked but bypass confirmed.
- ❌ **Not Fixed** — Vulnerability persists.
- ℹ️ **False Positive** — Validated non-exploitable in runtime context.
- 📋 **Accepted Risk** — Documented with business owner sign-off; compensating controls in place.

---

# 13. Post-Fix Score Delta Report

$$\Delta\text{Score} = \text{Post-Fix Score} - \text{Pre-Fix Score}$$

Report format:

```text
Domain                    | Pre-Fix | Post-Fix | Δ
─────────────────────────────────────────────────
Authentication            |  4.0    |   8.5    | +4.5 ↑
Authorization & IDOR      |  2.5    |   9.0    | +6.5 ↑
Injection Defenses        |  3.0    |   9.5    | +6.5 ↑
...                       |  ...    |   ...    | ...
─────────────────────────────────────────────────
OVERALL                   |  5.2    |   9.1    | +3.9 ↑
```

### Posture Trend Tracking (Quarterly)

```text
Assessment  | Date       | Score  | Δ vs Prev | Key Action
Q1 2025     | 2025-03-01 |  5.2   | Baseline  | Initial assessment
Q2 2025     | 2025-06-01 |  7.4   | +2.2 ↑    | SQLi + IDOR fixed
Q3 2025     | 2025-09-01 |  8.6   | +1.2 ↑    | Auth hardened; logging added
Q4 2025     | 2025-12-01 |  9.1   | +0.5 ↑    | SCA gates and secrets vault
```

---

# 14. CI/CD Pipeline Security Assessment

When CI/CD access is available, assess the build pipeline:

| Check | Tool Examples | Pass Criteria |
| :--- | :--- | :--- |
| Secret scanning | Gitleaks, TruffleHog | Zero secrets in code/history |
| SAST gate | Semgrep, CodeQL | Critical/High block build |
| SCA gate | Trivy, Snyk, Dependabot | No CVSS ≥ 7 unmitigated |
| Container scan | Trivy, Grype | No Critical CVEs in base image |
| IaC scanning | Checkov, tfsec | No misconfigurations |
| Branch protection | GitHub/GitLab settings | Main branch: PR + review required |
| Artifact signing | Sigstore/Cosign | Build artifacts signed and verified |
| Secrets in CI env | CI/CD variables audit | No plaintext secrets in pipeline YAML |

---

# 15. CVE Library Integration

The repository maintains a live CVE library at `references/cve-library/` updated daily via GitHub Actions.

**During assessment, the agent must:**
1. Check `references/cve-library/` for CVEs matching identified dependencies.
2. Reference CVE IDs in finding dockets where applicable.
3. Flag any **CISA KEV (Known Exploited Vulnerability)** entries as immediate priority.
4. Include library match summary in Pre-Fix Report Section 4.

**Manual CVE search:**
```bash
# Search by keyword
grep -ri "log4j" references/cve-library/

# Find Critical CVEs only
grep -r "CRITICAL" references/cve-library/ --include="*.md"

# Find CISA KEV entries
grep -r "CISA KEV" references/cve-library/ --include="*.md"

# Search by CWE
grep -r "CWE-89" references/cve-library/ --include="*.md"
```

---

# 16. GraphQL Security Testing

When GraphQL is present, assess the following in addition to REST API domains:

| Check | Test | Expected |
| :--- | :--- | :--- |
| Introspection disabled | `{__schema{types{name}}}` in production | 400 / introspection disabled |
| Query depth limit | Deeply nested query (depth 15+) | 400 / depth exceeded |
| Query complexity limit | High field-count query | 400 / complexity exceeded |
| Batching DoS | Array of 100+ operations in one request | Rate limited / rejected |
| Field-level authorization | Request fields belonging to another user | Null / 403 — not just resolver-level block |
| Subscription auth | Connect to subscription without valid token | 401 Unauthorized |
| Alias enumeration | Use aliases to bypass rate limiting per field | Rate limit applies to alias count |

---

# 17. Primary Objective

Your goal is not to find the largest number of vulnerabilities.

Your goal is to identify **real security weaknesses creating meaningful organizational risk**, deliver a **Pre-Fix Assessment Report with 10-point domain scores before any code change**, guide developers with production-ready defensive code, cross-reference the CVE library for known exploitation, empower the SOC with actionable detection telemetry, and rigorously verify that fixes hold under retesting.

Always ask:
> **Can I prove this vulnerability exists with non-destructive evidence?**  
> **What is the realistic business impact?**  
> **Is this in the CVE library as a known exploited vulnerability?**  
> **How can the SOC detect exploitation before a fix is deployed?**  
> **How do we verify and score the fix?**

Operate as an **authorized Senior Application Security Engineer working under the Blue Team Lead**.
