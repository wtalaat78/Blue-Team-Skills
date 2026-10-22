#!/usr/bin/env python3
"""
Techwaves EGY — Enterprise AppSec PDF Report Generator
======================================================
Blue-Team-Skills v4.0: Full-Spectrum Application & Runtime Security (ARS)
Generates branded, executive-ready PDF security assessment reports
from Phase 1 Pre-Fix Assessment data.

Company: Techwaves EGY
Contact: info@techwaves-egy.com
Logo:    assets/techwaves-logo.jpg

Usage:
  python scripts/generate_appsec_pdf.py --output reports/Pre-Fix-AppSec-Report.pdf
  python scripts/generate_appsec_pdf.py --sample --output reports/Pre-Fix-AppSec-Report-Sample.pdf
"""

import os
import sys
import html
import argparse
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        Image, KeepTogether, HRFlowable
    )
    from reportlab.pdfgen import canvas
except ImportError:
    print("[!] Error: reportlab library not found. Run: pip install reportlab", file=sys.stderr)
    sys.exit(1)

# ── Color Palette ─────────────────────────────────────────────────────────────
NAVY_PRIMARY = colors.HexColor("#0B1B3D")
CYAN_ACCENT  = colors.HexColor("#0088CC")
SLATE_GRAY   = colors.HexColor("#4A5568")
LIGHT_BG     = colors.HexColor("#F7FAFC")
BORDER_COLOR = colors.HexColor("#E2E8F0")

CRITICAL_RED = colors.HexColor("#E53E3E")
HIGH_ORANGE  = colors.HexColor("#DD6B20")
MEDIUM_YELLOW= colors.HexColor("#D69E2E")
GOOD_BLUE    = colors.HexColor("#3182CE")
HARDENED_GRN = colors.HexColor("#38A169")


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas for dynamic total page count."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))

        # Footer
        footer_y = 30
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(40, footer_y + 12, 572, footer_y + 12)

        self.drawString(40, footer_y, "CONFIDENTIAL  |  Techwaves EGY - Enterprise Application & Runtime Security (ARS)")
        self.drawRightString(572, footer_y, f"Page {self._pageNumber} of {page_count}")
        self.drawCentredString(306, footer_y - 10, "Contact: info@techwaves-egy.com  |  www.techwaves-egy.com")

        self.restoreState()


def get_severity_color(sev_text: str):
    s = str(sev_text).upper()
    if "CRIT" in s or "0." in s or "1." in s or "2." in s:
        return CRITICAL_RED
    if "HIGH" in s or "3." in s or "4." in s:
        return HIGH_ORANGE
    if "MED" in s or "MOD" in s or "5." in s or "6." in s:
        return MEDIUM_YELLOW
    if "GOOD" in s or "COMP" in s or "7." in s or "8." in s:
        return GOOD_BLUE
    return HARDENED_GRN


def build_header(logo_path: str, app_name: str, env: str, date_str: str, styles: dict):
    """Builds the Techwaves EGY branded report header table."""
    logo_flowable = None
    if logo_path and os.path.exists(logo_path):
        try:
            logo_flowable = Image(logo_path, width=2.4*inch, height=2.4*inch)
        except Exception:
            logo_flowable = None

    header_text = [
        Paragraph("<font color='#0B1B3D' size='18'><b>TECHWAVES EGY</b></font>", styles['TechTitle']),
        Paragraph("<font color='#0088CC' size='10'><b>Blue Team Application & Runtime Security (ARS) v4.0</b></font>", styles['TechSub']),
        Paragraph(f"<font color='#4A5568' size='8'>Email: <b>info@techwaves-egy.com</b>  |  Web: <b>www.techwaves-egy.com</b></font>", styles['TechMeta']),
        Spacer(1, 4),
        Paragraph("<font color='#E53E3E' size='7'><b>CLASSIFICATION: STRICTLY CONFIDENTIAL // SECURITY AUDIT</b></font>", styles['TechMeta']),
    ]

    left_cell = header_text
    right_cell = logo_flowable if logo_flowable else Paragraph("<b>TECHWAVES EGY</b>", styles['Normal'])

    hdr_table = Table([[left_cell, right_cell]], colWidths=[4.4*inch, 2.4*inch])
    hdr_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    return hdr_table


def _esc_code(text):
    return html.escape(str(text), quote=False).replace('\n', '<br/>')


def generate_pdf_report(
    output_path: str,
    app_name: str = "Enterprise Web Application",
    environment: str = "Staging",
    assessment_mode: str = "White Box / Full-Spectrum ARS",
    overall_score: float = 6.2,
    domain_scores: list = None,
    infrastructure_stack: list = None,
    findings: list = None,
    cisa_alert: dict = None,
    executive_summary: str = "",
    logo_path: str = None
):
    """Main PDF generation routine for Blue-Team-Skills v4.0."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=55
    )

    base_styles = getSampleStyleSheet()

    styles = {
        'TechTitle': ParagraphStyle('TechTitle', parent=base_styles['Normal'], fontName='Helvetica-Bold', leading=22),
        'TechSub':   ParagraphStyle('TechSub', parent=base_styles['Normal'], fontName='Helvetica-Bold', leading=13),
        'TechMeta':  ParagraphStyle('TechMeta', parent=base_styles['Normal'], fontName='Helvetica', leading=11),
        'ReportTitle': ParagraphStyle('ReportTitle', fontName='Helvetica-Bold', fontSize=15, leading=18, textColor=NAVY_PRIMARY),
        'SectionHeader': ParagraphStyle('SectionHeader', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=NAVY_PRIMARY, spaceAfter=5),
        'Body': ParagraphStyle('Body', fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor("#2D3748")),
        'CodeBlock': ParagraphStyle('CodeBlock', fontName='Courier', fontSize=7, leading=9.5, textColor=colors.HexColor("#1A202C")),
        'TableHead': ParagraphStyle('TableHead', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white),
        'TableCell': ParagraphStyle('TableCell', fontName='Helvetica', fontSize=7.5, leading=9.5, textColor=colors.HexColor("#2D3748")),
        'FindingTitle': ParagraphStyle('FindingTitle', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=NAVY_PRIMARY),
    }

    elements = []
    today = datetime.now().strftime("%Y-%m-%d")

    # 1. Header Banner
    elements.append(build_header(logo_path, app_name, environment, today, styles))
    elements.append(Spacer(1, 6))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=CYAN_ACCENT, spaceBefore=2, spaceAfter=8))

    # 2. Report Meta Banner
    meta_data = [
        [
            Paragraph(f"<b>Application:</b> {app_name}", styles['TableCell']),
            Paragraph(f"<b>Environment:</b> {environment}", styles['TableCell']),
            Paragraph(f"<b>Mode:</b> {assessment_mode}", styles['TableCell']),
            Paragraph(f"<b>Date:</b> {today}", styles['TableCell']),
        ]
    ]
    meta_table = Table(meta_data, colWidths=[2.1*inch, 1.6*inch, 1.8*inch, 1.3*inch])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 8))

    # 3. Title & Overall Scorecard Banner
    elements.append(Paragraph("Phase 1: Pre-Fix Security Assessment Report (ARS v4.0)", styles['ReportTitle']))
    elements.append(Spacer(1, 5))

    # Overall score badge table
    score_color = get_severity_color(str(overall_score))
    rating_text = (
        "EXEMPLARY" if overall_score >= 9.0 else
        "GOOD / COMPLIANT" if overall_score >= 7.0 else
        "MODERATE RISK" if overall_score >= 5.0 else
        "HIGH RISK" if overall_score >= 3.0 else
        "CRITICAL EXPOSURE"
    )

    score_card_data = [
        [
            Paragraph("<font size='9.5'><b>OVERALL APPLICATION & HOST RUNTIME SECURITY POSTURE</b></font><br/>"
                      "<font size='7.5' color='#718096'>Assessed across 12 Security Domains, Host Runtime Engines, and CISA KEV Threat Intel</font>", styles['TableCell']),
            Paragraph(f"<font size='15' color='white'><b>{overall_score:.1f} / 10.0</b></font><br/><font size='7.5' color='white'><b>{rating_text}</b></font>",
                      ParagraphStyle('Score', alignment=1, textColor=colors.white))
        ]
    ]
    score_card = Table(score_card_data, colWidths=[4.9*inch, 1.9*inch])
    score_card.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), LIGHT_BG),
        ('BACKGROUND', (1, 0), (1, 0), score_color),
        ('BOX', (0, 0), (-1, -1), 1, score_color),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
    ]))
    elements.append(score_card)
    elements.append(Spacer(1, 8))

    # CISA KEV / Real-World Weaponization Alert Box
    active_cisa = cisa_alert or {
        "active": True,
        "title": "CISA KEV & ACTIVE CISA KEV THREAT ALERT: PHP Zend Engine RCE (CVE-2026-109618)",
        "details": "Host runtime discovery identified PHP 8.5.4 (vulnerable range 8.5.0–8.5.11). This flaw is actively cataloged in CISA KEV with observed in-the-wild exploitation. An automatic Emergency Priority (P1 / Critical SLA: 24–48h) has been enforced."
    }
    if active_cisa.get("active"):
        cisa_box_data = [
            [
                Paragraph(f"<font color='#9B2C2C'><b>⚠️ {active_cisa['title']}</b></font><br/>"
                          f"<font size='7.5' color='#742A2A'>{active_cisa['details']}</font>", styles['TableCell'])
            ]
        ]
        cisa_box = Table(cisa_box_data, colWidths=[6.8*inch])
        cisa_box.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FFF5F5")),
            ('BOX', (0, 0), (-1, -1), 1, CRITICAL_RED),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(cisa_box)
        elements.append(Spacer(1, 8))

    # 4. Executive Summary
    elements.append(Paragraph("1. Executive Summary", styles['SectionHeader']))
    summary_text = executive_summary or (
        "Techwaves EGY performed an enterprise Application & Runtime Security (ARS) assessment evaluating application logic, "
        "authorization boundaries, cryptographic hygiene, API integrity, software dependencies, and underlying host execution "
        "runtimes (PHP Zend Engine, Node.js V8, Web Server daemons) across 12 security domains. The assessment identified critical "
        "vulnerabilities in both application-level access control and the host execution engine requiring immediate remediation."
    )
    elements.append(Paragraph(summary_text, styles['Body']))
    elements.append(Spacer(1, 8))

    # 5. Security Posture Scorecard (12 Domains)
    elements.append(Paragraph("2. 12-Domain Security Scorecard", styles['SectionHeader']))

    table_data = [
        [
            Paragraph("<b>#</b>", styles['TableHead']),
            Paragraph("<b>Security Domain</b>", styles['TableHead']),
            Paragraph("<b>Score</b>", styles['TableHead']),
            Paragraph("<b>Rating</b>", styles['TableHead']),
            Paragraph("<b>Primary Observation</b>", styles['TableHead'])
        ]
    ]

    default_domains = domain_scores or [
        (1, "Authentication & Session Security", 8.0, "Compliant", "MFA active; token lifetime needs shortening."),
        (2, "Authorization, RBAC & Tenant Isolation (IDOR)", 3.0, "High Risk", "Missing object ownership check on API endpoints."),
        (3, "Input Validation & Injection Defenses", 4.5, "High Risk", "Dynamic query concatenation identified in search."),
        (4, "Output Encoding & XSS Defenses", 9.0, "Hardened", "React auto-encoding; strict CSP active."),
        (5, "API & Business Logic Integrity", 6.0, "Moderate", "Mass assignment on user update DTO."),
        (6, "State-Changing Security & CSRF", 8.0, "Compliant", "SameSite=Strict cookies active."),
        (7, "SSRF & Perimeter Defenses", 5.0, "Moderate", "Webhook endpoint lacks RFC 1918 block."),
        (8, "File Upload, Path Traversal & Storage", 7.5, "Compliant", "S3 isolated storage; needs magic-byte check."),
        (9, "Cryptography, Secrets & Transport Security", 7.0, "Compliant", "TLS 1.3 active; secrets in Azure KV; key rotation needed."),
        (10, "Security Logging, Auditing & SOC Telemetry", 4.0, "High Risk", "Missing failed auth logging & correlation ID."),
        (11, "Application Supply Chain & Package SCA", 7.0, "Compliant", "Dependencies pinned; reachability analysis verified."),
        (12, "Host Runtime Engine, Daemon & Infrastructure", 2.5, "Critical Exposure", "PHP 8.5.4 vulnerable to Zend Engine RCE (CVE-2026-109618).")
    ]

    for idx, name, score, rating, obs in default_domains:
        badge_color = get_severity_color(str(score))
        table_data.append([
            Paragraph(f"<b>{idx}</b>", styles['TableCell']),
            Paragraph(name, styles['TableCell']),
            Paragraph(f"<b>{score:.1f}/10</b>", ParagraphStyle('ScoreCol', parent=styles['TableCell'], textColor=badge_color)),
            Paragraph(f"<b>{rating}</b>", ParagraphStyle('RateCol', parent=styles['TableCell'], textColor=badge_color)),
            Paragraph(obs, styles['TableCell'])
        ])

    score_table = Table(table_data, colWidths=[0.25*inch, 2.35*inch, 0.65*inch, 1.05*inch, 2.5*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
    ]))
    elements.append(score_table)
    elements.append(Spacer(1, 10))

    # 6. Infrastructure & Runtime Execution Stack Table
    elements.append(Paragraph("3. Infrastructure & Host Runtime Execution Stack", styles['SectionHeader']))
    infra_data = [
        [
            Paragraph("<b>Component</b>", styles['TableHead']),
            Paragraph("<b>Detected Version</b>", styles['TableHead']),
            Paragraph("<b>Build / Architecture</b>", styles['TableHead']),
            Paragraph("<b>Threat Intel / CISA KEV</b>", styles['TableHead']),
            Paragraph("<b>Posture Status</b>", styles['TableHead'])
        ]
    ]

    default_infra = infrastructure_stack or [
        ("Host Runtime (PHP)", "PHP 8.5.4", "Zend Engine v4.5.4 (NTS x64)", "⚠️ CISA KEV / CVE-2026-109618", "🔴 CRITICAL EXPOSURE"),
        ("Web Server Daemon", "Nginx 1.26.1", "OpenSSL 3.0.13, HTTP/2 (x64)", "Clean / No KEV", "🟢 COMPLIANT"),
        ("Database Engine", "PostgreSQL 16.3", "Debian 16.3-1.pgdg120+1 (x64)", "Clean / No KEV", "🟢 COMPLIANT"),
        ("Native SSL Library", "OpenSSL 3.0.13", "System Shared Library (x64)", "Clean / No KEV", "🟢 COMPLIANT")
    ]

    for comp, ver, bld, intel, stat in default_infra:
        stat_color = get_severity_color(stat)
        infra_data.append([
            Paragraph(f"<b>{comp}</b>", styles['TableCell']),
            Paragraph(ver, styles['TableCell']),
            Paragraph(bld, styles['TableCell']),
            Paragraph(intel, styles['TableCell']),
            Paragraph(f"<b>{stat}</b>", ParagraphStyle('StatCol', parent=styles['TableCell'], textColor=stat_color))
        ])

    infra_table = Table(infra_data, colWidths=[1.6*inch, 1.2*inch, 1.5*inch, 1.4*inch, 1.1*inch])
    infra_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
    ]))
    elements.append(infra_table)
    elements.append(Spacer(1, 10))

    # 7. Detailed Finding Dockets with 4-Tier Defensive Shield
    elements.append(Paragraph("4. Detailed Vulnerability Dockets & Defensive Shields", styles['SectionHeader']))

    default_findings = findings or [
        {
            "id": "APP-001",
            "title": "Insecure Direct Object Reference (IDOR) on Order Retrieval",
            "severity": "High",
            "cvss": "8.6",
            "vector": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N",
            "epss": "0.742 (74.2% percentile)",
            "reachability": "[DIRECTLY REACHABLE]",
            "cisa_kev": "No",
            "cwe": "CWE-639",
            "asvs": "V1.4.1, V5.1.3",
            "pci": "Req 6.2.4",
            "nist": "AC-3, SA-11",
            "iso": "Control A.8.28",
            "endpoint": "GET /api/v1/orders/{orderId}",
            "desc": "The order retrieval endpoint queries the database by order ID without validating that the requesting authenticated user owns the object or belongs to the authorized tenant.",
            "poc": "GET /api/v1/orders/5002 HTTP/1.1\nHost: app.internal\nAuthorization: Bearer <UserA_Token>\n\nHTTP/1.1 200 OK -> UserB order data returned (IDOR confirmed)",
            "patch": "// VULNERABLE\nvar order = await _context.Orders.FindAsync(id);\n\n// SECURE (DEFENSIVE CODE)\nvar userId = _currentUser.GetUserId();\nvar order = await _context.Orders.FirstOrDefaultAsync(o => o.Id == id && o.UserId == userId);",
            "waf": "SecRule REQUEST_URI \"@rx ^/api/v1/orders/(\\d+)\" \"id:100201,phase:2,t:none,pass,nolog,setvar:tx.target_order_id=%{tx.1}\"\n# Enforce JWT subject tenancy validation in reverse proxy/WAF",
            "sigma": "title: Suspicious Multi-Order IDOR Enumeration Attempt\nlogsource: {category: webserver}\ndetection:\n  selection: {cs_method: GET, cs_uri_stem|re: '^/api/v1/orders/\\d+'}\n  timeframe: 1m\n  condition: selection | count() by c_ip > 15\nlevel: high\ntags: [attack.t1083, attack.t1078]",
            "workaround": "Deploy API gateway parameter validation filter mapping authenticated tenant claim to request context before upstream forwarding."
        },
        {
            "id": "APP-002",
            "title": "Host Runtime: PHP Zend Engine Multipart Parser Remote Execution Defect / RCE",
            "severity": "Critical",
            "cvss": "9.8",
            "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
            "epss": "0.965 (96.5% percentile)",
            "reachability": "[DIRECTLY REACHABLE]",
            "cisa_kev": "YES (Known In-The-Wild Exploitation)",
            "cwe": "CWE-122",
            "asvs": "V14.2.1",
            "pci": "Req 6.2",
            "nist": "SI-2, SA-11",
            "iso": "Control A.8.8",
            "endpoint": "Host Runtime: PHP 8.5.4 via Nginx FastCGI",
            "desc": "Host runtime discovery identified PHP 8.5.4 (Zend Engine v4.5.4). This release suffers from improper boundary calculation and buffer validation flaw in the core multipart body parser. Active CISA KEV in-the-wild exploitation allows remote unauthenticated attackers to execute arbitrary code via specially crafted multipart chunk boundaries.",
            "poc": "$ php -v\nPHP 8.5.4 (cli) (built: Feb 12 2026 14:22:10) (NTS)\nZend Engine v4.5.4, Copyright (c) Zend Technologies\n[!] Version falls within known vulnerable range: PHP 8.5.0 - 8.5.11 (CVE-2026-109618)",
            "patch": "# Host Runtime Upgrade Procedure\napt-get update && apt-get install --only-upgrade php8.5 php8.5-fpm php8.5-cli\nsystemctl restart php8.5-fpm && nginx -s reload\n# Verify: php -v >= 8.5.12",
            "waf": "SecRule REQUEST_HEADERS:Content-Type \"@rx (?i)multipart/form-data;.*boundary=.{128,}\" \"id:100301,phase:1,deny,status:400,log,msg:'Potential Zend Engine Multipart RCE Probe (CVE-2026-109618)'\"",
            "sigma": "title: Zend Engine Multipart Boundary Exploit Probe\nlogsource: {category: webserver}\ndetection:\n  selection: {cs_method: POST, c_content_type|contains: 'multipart/form-data'}\n  suspicious_boundary: {cs_header|re: 'boundary=[\\-\\=]{60,}[^\\r\\n]{128,}'}\n  condition: selection and suspicious_boundary\nlevel: critical\ntags: [attack.t1190, attack.t1203]",
            "workaround": "In php.ini: session.upload_progress.enabled = Off; post_max_size = 10M; upload_max_filesize = 10M; max_file_uploads = 5"
        }
    ]

    for f in default_findings:
        f_elements = []
        sev_color = get_severity_color(f['severity'])

        # Title bar with Reachability Badge
        reach_badge = f.get('reachability', '[REACHABLE]')
        header_tbl = Table([[
            Paragraph(f"<b>[{f['id']}] {f['title']}</b> <font size='7' color='#2B6CB0'><b>{reach_badge}</b></font>", styles['FindingTitle']),
            Paragraph(f"<b>{f['severity'].upper()} (CVSS {f['cvss']})</b>", ParagraphStyle('SevBadge', alignment=2, fontName='Helvetica-Bold', fontSize=8.5, textColor=sev_color))
        ]], colWidths=[5.1*inch, 1.7*inch])
        header_tbl.setStyle(TableStyle([
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
        ]))
        f_elements.append(header_tbl)

        # Meta row 1: Endpoint, CWE, Vector
        f_meta1 = [
            [
                Paragraph(f"<b>Target:</b> <font name='Courier'>{f['endpoint']}</font>", styles['TableCell']),
                Paragraph(f"<b>CWE:</b> {f['cwe']}", styles['TableCell']),
                Paragraph(f"<b>Vector:</b> <font size='6.5' name='Courier'>{f['vector']}</font>", styles['TableCell'])
            ]
        ]
        f_meta_tbl1 = Table(f_meta1, colWidths=[3.2*inch, 1.0*inch, 2.6*inch])
        f_meta_tbl1.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
            ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        f_elements.append(f_meta_tbl1)

        # Meta row 2: Threat Intel & Compliance Mapping
        kev_txt = f"<font color='#E53E3E'><b>{f.get('cisa_kev', 'No')}</b></font>" if 'YES' in f.get('cisa_kev', '').upper() else f.get('cisa_kev', 'No')
        f_meta2 = [
            [
                Paragraph(f"<b>EPSS:</b> {f.get('epss', 'N/A')}", styles['TableCell']),
                Paragraph(f"<b>CISA KEV:</b> {kev_txt}", styles['TableCell']),
                Paragraph(f"<b>ASVS:</b> {f.get('asvs', 'N/A')}  |  <b>PCI:</b> {f.get('pci', 'N/A')}  |  <b>NIST:</b> {f.get('nist', 'N/A')}", styles['TableCell'])
            ]
        ]
        f_meta_tbl2 = Table(f_meta2, colWidths=[1.8*inch, 1.6*inch, 3.4*inch])
        f_meta_tbl2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0F4F8")),
            ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        f_elements.append(f_meta_tbl2)
        f_elements.append(Spacer(1, 3))

        f_elements.append(Paragraph(f"<b>Description & Analysis:</b> {html.escape(f['desc'], quote=False)}", styles['Body']))
        f_elements.append(Spacer(1, 3))

        # Proof of Concept box
        poc_tbl = Table([[Paragraph(f"<b>Proof of Concept Trace:</b><br/><font name='Courier' size='6.5'>{_esc_code(f['poc'])}</font>", styles['TableCell'])]], colWidths=[6.8*inch])
        poc_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EDF2F7")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        f_elements.append(poc_tbl)
        f_elements.append(Spacer(1, 3))

        # 4-Tier Defensive Shield: Tier 1 - Patch
        shield_row1 = [
            [
                Paragraph(f"<b>Tier 1: Code-Level / Binary Patch:</b><br/><font name='Courier' size='6.5'>{_esc_code(f.get('patch', f.get('remediation', '')))}</font>", styles['TableCell']),
            ]
        ]
        shield_tbl1 = Table(shield_row1, colWidths=[6.8*inch])
        shield_tbl1.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0FFF4")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#9AE6B4")),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        f_elements.append(shield_tbl1)
        f_elements.append(Spacer(1, 3))

        # Tier 2 - WAF Rule & Tier 3 - SOC Detection Rule
        shield_row2 = [
            [
                Paragraph(f"<b>Tier 2: WAF Rule (ModSec / Cloudflare):</b><br/><font name='Courier' size='6.5'>{_esc_code(f.get('waf', 'N/A'))}</font>", styles['TableCell']),
                Paragraph(f"<b>Tier 3: SOC Detection Rule (Sigma):</b><br/><font name='Courier' size='6.5'>{_esc_code(f.get('sigma', 'N/A'))}</font>", styles['TableCell'])
            ]
        ]
        shield_tbl2 = Table(shield_row2, colWidths=[3.4*inch, 3.4*inch])
        shield_tbl2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EBF8FF")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#BEE3F8")),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        f_elements.append(shield_tbl2)
        f_elements.append(Spacer(1, 3))

        # Tier 4 - Temporary Config Workaround
        if f.get('workaround'):
            workaround_row = [
                [
                    Paragraph(f"<b>Tier 4: Immediate Config Workaround (Hotfix):</b> <font name='Courier' size='7'>{_esc_code(f['workaround'])}</font>", styles['TableCell'])
                ]
            ]
            workaround_tbl = Table(workaround_row, colWidths=[6.8*inch])
            workaround_tbl.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FEFCBF")),
                ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#D69E2E")),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            f_elements.append(workaround_tbl)

        f_elements.append(Spacer(1, 8))
        elements.append(KeepTogether(f_elements))

    # 8. Approval Gate & Sign-Off with Interactive Checkboxes
    elements.append(Spacer(1, 6))
    approval_box_data = [
        [
            Paragraph("<b>5. MANDATORY APPROVAL GATE — AWAITING STAKEHOLDER SIGN-OFF</b><br/>"
                      "<i>This document concludes Phase 1 of the Blue-Team-Skills v4.0 assessment. Per enterprise Blue Team "
                      "operating principles, no application code modifications or remediation scripts will be executed until authorized "
                      "by the technical lead or system owner.</i><br/><br/>"
                      "<b>Verification Checkboxes:</b><br/>"
                      "&nbsp;&nbsp;<b>[ &nbsp; ]</b> &nbsp; <b>Technical Lead Verification:</b> All 12 domain scores, CVSS calculations, and reachability traces verified.<br/>"
                      "&nbsp;&nbsp;<b>[ &nbsp; ]</b> &nbsp; <b>Architecture & Change Control:</b> Maintenance window, backup status, and rollback playbooks approved.<br/>"
                      "&nbsp;&nbsp;<b>[ &nbsp; ]</b> &nbsp; <b>Authorization to Proceed:</b> Stakeholder clearance granted to initiate Phase 2 (Defensive Remediation & Retesting).<br/><br/>"
                      "<b>Next Step:</b> Reply with explicit approval (e.g., <i>'Approved to proceed with Phase 2'</i>) to start defensive remediation.", styles['TableCell'])
        ]
    ]
    approval_box = Table(approval_box_data, colWidths=[6.8*inch])
    approval_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FFFAF0")),
        ('BOX', (0, 0), (-1, -1), 1, HIGH_ORANGE),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(approval_box)

    # Build Document
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"[✓] Enterprise PDF Report generated successfully:")
    print(f"    Path: {os.path.abspath(output_path)}")
    return os.path.abspath(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Techwaves EGY AppSec PDF Report Generator")
    parser.add_argument("--output", "-o", default="reports/Pre-Fix-AppSec-Report.pdf", help="Output PDF file path")
    parser.add_argument("--app", default="Enterprise Web Application", help="Application name")
    parser.add_argument("--env", default="Staging", help="Environment")
    parser.add_argument("--mode", default="White Box / Full-Spectrum ARS", help="Testing mode")
    parser.add_argument("--score", type=float, default=6.2, help="Overall score out of 10")
    parser.add_argument("--logo", default="assets/techwaves-logo.jpg", help="Path to company logo image")
    parser.add_argument("--sample", action="store_true", help="Generate sample report")

    args = parser.parse_args()

    logo_path = os.path.abspath(args.logo) if os.path.exists(args.logo) else None
    generate_pdf_report(
        output_path=args.output,
        app_name=args.app,
        environment=args.env,
        assessment_mode=args.mode,
        overall_score=args.score,
        logo_path=logo_path
    )
