# GitHub Copilot Custom Instructions: Blue Team AppSec

When analyzing code for security, performing code reviews, or implementing defensive fixes:

1. **Security Standards**: Follow OWASP Top 10, ASVS, CWE, and CISA KEV guidance.
2. **Pre-Fix Reporting & Hard Stop**: Prior to generating code modifications for security findings, summarize the vulnerability, provide the CVSS v3.1 rating, assign domain scores (0-10) across all 11 AppSec categories, outline the remediation plan, generate the branded PDF report via `scripts/generate_appsec_pdf.py` (Techwaves EGY header & `info@techwaves-egy.com`), output the absolute disk file location and link, and STOP. Do not generate code modifications or patches until the user approves the report.
3. **Host Runtime & Engine Infrastructure Bridge**:
   - In Phase 1, actively fingerprint underlying execution runtimes (`php -v`, `node -v`, `python -V`, web servers). Do not stop at package manifests.
   - Cross-reference runtime versions against NVD/CISA KEV for engine vulnerabilities (e.g., Zend Engine RCEs CVE-2026-109618/19).
   - Audit runtime directives (`session.upload_progress.enabled = Off`, `disable_functions`, `allow_url_include = Off`, `expose_php = Off`).
4. **Defensive Coding & Hardening**:
   - Authentication: Server-side validation, secure token handling, MFA support.
   - Authorization: Object-level and tenant-level authorization checks on all endpoints (prevent IDOR/BOLA).
   - Injections: Parameterized queries, ORM entity bindings, strict type checking.
   - Output Encoding: Context-aware sanitization, DOM sink protection, strict CSP.
   - SSRF: Strict URL destination allowlists, RFC 1918 and cloud metadata (`169.254.169.254`) blocking.
   - Cryptography & Engine: Zero hardcoded secrets, TLS 1.3, hardened `php.ini` directives.
   - Logging: Audit security events with Actor, Action, Resource, Status, Correlation ID (no sensitive data in logs).
5. **References**: Refer to `skills/internal-appsec-testing/SKILL.md` and `references/cve-library/` (including `host_runtime_and_engine_sca.md`) for comprehensive domain rubrics and known vulnerability benchmarks.
