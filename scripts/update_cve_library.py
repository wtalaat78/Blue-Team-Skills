#!/usr/bin/env python3
"""
CVE Library Updater for Blue-Team-Skills
=========================================
Fetches recent and critical web application CVEs from the NVD (NIST) API
and saves them as structured Markdown files in references/cve-library/.

Sources:
  - NVD CVE API 2.0: https://services.nvd.nist.gov/rest/json/cves/2.0
  - CVE.org: https://www.cve.org

Usage:
  python scripts/update_cve_library.py

Scheduled via: .github/workflows/daily-cve-update.yml
"""

import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
import urllib.request
import urllib.parse

# ─── Configuration ────────────────────────────────────────────────────────────

NVD_BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
OUTPUT_DIR   = Path(__file__).parent.parent / "references" / "cve-library"
INDEX_FILE   = OUTPUT_DIR / "README.md"
LAST_RUN     = OUTPUT_DIR / ".last_run"

# AppSec-relevant keyword groups mapped to OWASP categories
SEARCH_PROFILES = [
    {"keyword": "sql injection",               "owasp": "A03-Injection",              "domain": "Input Validation & Injection"},
    {"keyword": "command injection",           "owasp": "A03-Injection",              "domain": "Input Validation & Injection"},
    {"keyword": "XSS cross-site scripting",    "owasp": "A03-Injection",              "domain": "XSS & Output Encoding"},
    {"keyword": "SSRF server-side request",    "owasp": "A10-SSRF",                   "domain": "SSRF & Perimeter"},
    {"keyword": "authentication bypass",       "owasp": "A07-AuthFailures",           "domain": "Authentication & Session"},
    {"keyword": "broken access control IDOR",  "owasp": "A01-BrokenAccessControl",    "domain": "Authorization & IDOR/BOLA"},
    {"keyword": "JWT token forgery",           "owasp": "A07-AuthFailures",           "domain": "Authentication & Session"},
    {"keyword": "file upload",                 "owasp": "A04-InsecureDesign",         "domain": "File Upload & Storage"},
    {"keyword": "path traversal directory",    "owasp": "A01-BrokenAccessControl",    "domain": "File Upload & Storage"},
    {"keyword": "deserialization",             "owasp": "A08-DataIntegrity",          "domain": "Input Validation & Injection"},
    {"keyword": "hardcoded credential secret", "owasp": "A02-CryptographicFailures",  "domain": "Cryptography & Secrets"},
    {"keyword": "TLS SSL weak cipher",         "owasp": "A02-CryptographicFailures",  "domain": "Cryptography & Secrets"},
    {"keyword": "CSRF cross-site request",     "owasp": "A01-BrokenAccessControl",    "domain": "CSRF & State-Changing"},
    {"keyword": "privilege escalation",        "owasp": "A01-BrokenAccessControl",    "domain": "Authorization & IDOR/BOLA"},
    {"keyword": "log injection",               "owasp": "A09-LoggingFailures",        "domain": "Logging & SOC Telemetry"},
    {"keyword": "supply chain dependency",     "owasp": "A06-VulnerableComponents",   "domain": "Supply Chain & SCA"},
    {"keyword": "GraphQL introspection",       "owasp": "A05-SecurityMisconfiguration","domain": "API & Business Logic"},
    {"keyword": "OAuth OIDC redirect",         "owasp": "A07-AuthFailures",           "domain": "Authentication & Session"},
    {"keyword": "open redirect",               "owasp": "A01-BrokenAccessControl",    "domain": "Authorization & IDOR/BOLA"},
    {"keyword": "mass assignment",             "owasp": "A04-InsecureDesign",         "domain": "API & Business Logic"},
]

SEVERITY_LEVELS = ["CRITICAL", "HIGH"]
DAYS_LOOKBACK   = 7    # fetch CVEs from last N days (daily run uses 2, first run uses 7)
MAX_PER_QUERY   = 50   # NVD API limit per request

# ─── Helpers ──────────────────────────────────────────────────────────────────

def nvd_get(params: dict, retries: int = 3) -> dict:
    """Call NVD API with retry logic and rate limiting."""
    url = f"{NVD_BASE_URL}?{urllib.parse.urlencode(params)}"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "BlueTeamSkills-CVELibrary/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
                time.sleep(0.6)  # NVD rate limit: max 5 req/30s without API key
                return data
        except Exception as e:
            print(f"  [!] Attempt {attempt+1} failed: {e}")
            time.sleep(3)
    return {}


def severity_badge(score: float) -> str:
    if score >= 9.0: return "🔴 CRITICAL"
    if score >= 7.0: return "🟠 HIGH"
    if score >= 4.0: return "🟡 MEDIUM"
    return "🟢 LOW"


def cwe_link(cwe_id: str) -> str:
    if cwe_id.startswith("CWE-"):
        num = cwe_id.replace("CWE-", "")
        return f"[{cwe_id}](https://cwe.mitre.org/data/definitions/{num}.html)"
    return cwe_id


def extract_cvss(metrics: dict) -> tuple[float, str]:
    """Extract highest available CVSS score and vector."""
    for key in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
        items = metrics.get(key, [])
        for item in items:
            data = item.get("cvssData", {})
            score = data.get("baseScore", 0.0)
            vector = data.get("vectorString", "N/A")
            if score > 0:
                return score, vector
    return 0.0, "N/A"


def format_cve_markdown(cve: dict, profile: dict) -> str:
    """Format a single CVE as Markdown."""
    c = cve.get("cve", {})
    cve_id    = c.get("id", "N/A")
    published = c.get("published", "")[:10]
    modified  = c.get("lastModified", "")[:10]
    status    = c.get("vulnStatus", "Unknown")

    desc = next(
        (d["value"] for d in c.get("descriptions", []) if d.get("lang") == "en"),
        "No description available."
    )

    score, vector = extract_cvss(c.get("metrics", {}))
    badge = severity_badge(score)

    weaknesses = []
    for w in c.get("weaknesses", []):
        for d in w.get("description", []):
            val = d.get("value", "")
            if val and val != "NVD-CWE-noinfo":
                weaknesses.append(val)
    cwe_str = " | ".join(cwe_link(w) for w in set(weaknesses)) if weaknesses else "Not specified"

    refs = c.get("references", [])[:3]
    ref_lines = "\n".join(f"  - <{r['url']}>" for r in refs)

    cisa_note = ""
    if c.get("cisaExploitAdd"):
        cisa_note = f"\n> ⚠️ **CISA KEV**: Added {c['cisaExploitAdd']} — {c.get('cisaVulnerabilityName', '')}. Action due: {c.get('cisaActionDue', 'N/A')}.\n"

    return f"""---

## {cve_id} {badge}

| Field | Value |
| :--- | :--- |
| **CVE ID** | [{cve_id}](https://www.cve.org/CVERecord?id={cve_id}) |
| **CVSS v3 Score** | **{score:.1f}** / 10.0 |
| **CVSS Vector** | `{vector}` |
| **Published** | {published} |
| **Last Modified** | {modified} |
| **Status** | {status} |
| **CWE** | {cwe_str} |
| **OWASP Category** | {profile['owasp']} |
| **AppSec Domain** | {profile['domain']} |

{cisa_note}
### Description
{desc}

### References
{ref_lines if ref_lines else '  - See CVE record for details.'}

"""


def fetch_profile_cves(profile: dict, pub_start: str, pub_end: str) -> list[dict]:
    """Fetch CVEs for a given keyword profile within date window."""
    results = []
    for severity in SEVERITY_LEVELS:
        params = {
            "keywordSearch":   profile["keyword"],
            "pubStartDate":    pub_start,
            "pubEndDate":      pub_end,
            "cvssV3Severity":  severity,
            "resultsPerPage":  MAX_PER_QUERY,
            "startIndex":      0,
        }
        data = nvd_get(params)
        vulns = data.get("vulnerabilities", [])
        results.extend(vulns)
    # deduplicate
    seen, unique = set(), []
    for v in results:
        cid = v.get("cve", {}).get("id")
        if cid and cid not in seen:
            seen.add(cid)
            unique.append(v)
    return unique


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    now     = datetime.now(timezone.utc)
    lookback = DAYS_LOOKBACK
    if LAST_RUN.exists():
        lookback = 2  # incremental run

    pub_end   = now.strftime("%Y-%m-%dT%H:%M:%S.000")
    pub_start = (now - timedelta(days=lookback)).strftime("%Y-%m-%dT%H:%M:%S.000")

    sys.stdout.reconfigure(encoding='utf-8', errors='replace') if hasattr(sys.stdout, 'reconfigure') else None
    print(f"[*] CVE Library Update - {now.strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"[*] Window: {pub_start[:10]} to {pub_end[:10]}")
    print(f"[*] Profiles: {len(SEARCH_PROFILES)} | Severity: {SEVERITY_LEVELS}")

    all_cves_by_domain: dict[str, list] = {}
    total_fetched = 0

    for profile in SEARCH_PROFILES:
        domain = profile["domain"]
        print(f"  → Fetching: [{profile['owasp']}] {profile['keyword']}")
        cves = fetch_profile_cves(profile, pub_start, pub_end)
        total_fetched += len(cves)
        if domain not in all_cves_by_domain:
            all_cves_by_domain[domain] = []
        for cve in cves:
            all_cves_by_domain[domain].append((cve, profile))

    print(f"[*] Total CVEs fetched (raw): {total_fetched}")

    # ── Write per-domain files ──────────────────────────────────────────────
    index_entries = []

    for domain, cve_list in sorted(all_cves_by_domain.items()):
        if not cve_list:
            continue

        # Sort by CVSS score descending
        cve_list.sort(key=lambda x: extract_cvss(x[0].get("cve", {}).get("metrics", {}))[0], reverse=True)

        safe_name = domain.replace(" ", "_").replace("/", "_").replace("&", "and").lower()
        domain_file = OUTPUT_DIR / f"{safe_name}.md"

        lines = [
            f"# CVE Library — {domain}\n",
            f"**Last Updated:** {now.strftime('%Y-%m-%d %H:%M UTC')}  \n",
            f"**Source:** [NVD / NIST](https://nvd.nist.gov) & [CVE.org](https://www.cve.org)  \n",
            f"**Entries:** {len(cve_list)} CVEs  \n",
            "\n---\n",
        ]

        for (cve, prof) in cve_list[:100]:  # cap per file
            lines.append(format_cve_markdown(cve, prof))

        domain_file.write_text("".join(lines), encoding="utf-8")
        print(f"  ✓ Written {len(cve_list)} CVEs → {domain_file.name}")

        index_entries.append({
            "domain": domain,
            "file":   domain_file.name,
            "count":  len(cve_list),
        })

    # ── Write index README ──────────────────────────────────────────────────
    critical_count = sum(1 for entries in all_cves_by_domain.values()
                         for (cve, _) in entries
                         if extract_cvss(cve.get("cve", {}).get("metrics", {}))[0] >= 9.0)
    high_count     = sum(1 for entries in all_cves_by_domain.values()
                         for (cve, _) in entries
                         if 7.0 <= extract_cvss(cve.get("cve", {}).get("metrics", {}))[0] < 9.0)

    index_lines = [
        "# 📚 CVE Library — Blue Team AppSec Reference\n\n",
        f"> **Last Updated:** {now.strftime('%Y-%m-%d %H:%M UTC')}\n",
        f"> **Data Sources:** [NVD/NIST CVE API 2.0](https://nvd.nist.gov) · [CVE.org](https://www.cve.org)\n",
        f"> **Update Schedule:** Daily via GitHub Actions (`.github/workflows/daily-cve-update.yml`)\n\n",
        "---\n\n",
        "## Summary\n\n",
        f"| Metric | Count |\n",
        f"| :--- | :---: |\n",
        f"| 🔴 Critical CVEs (CVSS ≥ 9.0) | **{critical_count}** |\n",
        f"| 🟠 High CVEs (CVSS 7.0–8.9) | **{high_count}** |\n",
        f"| Total Entries | **{total_fetched}** |\n",
        f"| AppSec Domains Covered | **{len(index_entries)}** |\n\n",
        "---\n\n",
        "## CVE Library by AppSec Domain\n\n",
        "| AppSec Domain | CVEs | File |\n",
        "| :--- | :---: | :--- |\n",
    ]

    for entry in sorted(index_entries, key=lambda x: x["count"], reverse=True):
        index_lines.append(
            f"| {entry['domain']} | {entry['count']} | [{entry['file']}](./{entry['file']}) |\n"
        )

    index_lines += [
        "\n---\n\n",
        "## How the Skill Uses This Library\n\n",
        "When the `internal-appsec-testing` / `/appsec` skill is active, the agent:\n\n",
        "1. **Checks this library** when analyzing dependencies or assessing known-vulnerable versions.\n",
        "2. **Cross-references findings** against CVE IDs to confirm known exploitability.\n",
        "3. **References CVSS scores** in the Pre-Fix Assessment Report for each finding.\n",
        "4. **Highlights CISA KEV entries** (Known Exploited Vulnerabilities) as immediate priority.\n\n",
        "---\n\n",
        "## Manual Search\n\n",
        "Search this library using:\n",
        "```bash\n",
        "# Find all CRITICAL CVEs in the library\n",
        "grep -r 'CRITICAL' references/cve-library/ --include='*.md'\n\n",
        "# Find CVEs by CWE\n",
        "grep -r 'CWE-89' references/cve-library/ --include='*.md'\n\n",
        "# Find CISA KEV entries\n",
        "grep -r 'CISA KEV' references/cve-library/ --include='*.md'\n",
        "```\n",
    ]

    INDEX_FILE.write_text("".join(index_lines), encoding="utf-8")
    LAST_RUN.write_text(now.isoformat(), encoding="utf-8")

    print(f"\n[✓] CVE Library update complete.")
    print(f"    Critical: {critical_count} | High: {high_count} | Total: {total_fetched}")
    print(f"    Index: {INDEX_FILE}")


if __name__ == "__main__":
    main()
