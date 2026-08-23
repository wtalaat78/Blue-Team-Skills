#!/usr/bin/env python3
"""
Techwaves EGY — Enterprise AppSec PDF Report Generator
======================================================
Generates branded, executive-ready PDF security assessment reports
from Phase 1 Pre-Fix Assessment data.

Company: Techwaves EGY
Contact: info@techwaves-egy.com
Logo:    assets/techwaves-logo.jpg

Usage:
  python scripts/generate_appsec_pdf.py --input <report.md> --output <output.pdf>
  python scripts/generate_appsec_pdf.py --json <data.json> --output <output.pdf>
  python scripts/generate_appsec_pdf.py --sample --output reports/Sample-Pre-Fix-Report.pdf
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        Image, KeepTogether, HRFlowable, PageBreak
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

        self.drawString(40, footer_y, "CONFIDENTIAL  |  Techwaves EGY - Enterprise Application Security Testing")
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
        Paragraph("<font color='#0088CC' size='10'><b>Blue Team Application Security & Defensive Engineering</b></font>", styles['TechSub']),
        Paragraph(f"<font color='#4A5568' size='8'>Email: <b>info@techwaves-egy.com</b>  |  Web: <b>www.techwaves-egy.com</b></font>", styles['TechMeta']),
        Spacer(1, 4),
        Paragraph("<font color='#E53E3E' size='7'><b>CLASSIFICATION: STRICTLY CONFIDENTIAL // SECURITY AUDIT</b></font>", styles['TechMeta']),
    ]

    left_cell = header_text
    right_cell = logo_flowable if logo_flowable else Paragraph("<b>TECHWAVES EGY</b>", styles['Normal'])

    hdr_table = Table([[left_cell, right_cell]], colWidths=[3.6*inch, 3.2*inch])
    hdr_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    return hdr_table


def generate_pdf_report(
    output_path: str,
    app_name: str = "Enterprise Web Application",
    environment: str = "Staging",
    assessment_mode: str = "White Box / SAST & DAST",
    overall_score: float = 6.2,
    domain_scores: list = None,
    findings: list = None,
    executive_summary: str = "",
    logo_path: str = None
):
    """Main PDF generation routine."""
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
        'SectionHeader': ParagraphStyle('SectionHeader', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=NAVY_PRIMARY, spaceAfter=6),
        'Body': ParagraphStyle('Body', fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor("#2D3748")),
        'CodeBlock': ParagraphStyle('CodeBlock', fontName='Courier', fontSize=7.5, leading=10, textColor=colors.HexColor("#1A202C")),
        'TableHead': ParagraphStyle('TableHead', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.white),
        'TableCell': ParagraphStyle('TableCell', fontName='Helvetica', fontSize=8, leading=10, textColor=colors.HexColor("#2D3748")),
        'FindingTitle': ParagraphStyle('FindingTitle', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=NAVY_PRIMARY),
    }

    elements = []
    today = datetime.now().strftime("%Y-%m-%d")

    # 1. Header Banner
    elements.append(build_header(logo_path, app_name, environment, today, styles))
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=CYAN_ACCENT, spaceBefore=2, spaceAfter=10))

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
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 12))

    # 3. Title & Overall Scorecard Banner
    elements.append(Paragraph("Phase 1: Pre-Fix Security Assessment Report", styles['ReportTitle']))
    elements.append(Spacer(1, 6))

    # Overall score badge table
    score_color = get_severity_color(str(overall_score))
    rating_text = "EXEMPLARY" if overall_score >= 9.0 else "GOOD / COMPLIANT" if overall_score >= 7.0 else "MODERATE RISK" if overall_score >= 5.0 else "HIGH RISK" if overall_score >= 3.0 else "CRITICAL EXPOSURE"

    score_card_data = [
        [
            Paragraph("<font size='10'><b>OVERALL APPLICATION SECURITY POSTURE</b></font>", styles['TableCell']),
            Paragraph(f"<font size='16' color='white'><b>{overall_score:.1f} / 10.0</b></font><br/><font size='8' color='white'><b>{rating_text}</b></font>", ParagraphStyle('Score', alignment=1, textColor=colors.white))
        ]
    ]
    score_card = Table(score_card_data, colWidths=[4.8*inch, 2.0*inch])
    score_card.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), LIGHT_BG),
        ('BACKGROUND', (1, 0), (1, 0), score_color),
        ('BOX', (0, 0), (-1, -1), 1, score_color),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
    ]))
    elements.append(score_card)
    elements.append(Spacer(1, 10))

    # 4. Executive Summary
    elements.append(Paragraph("1. Executive Summary", styles['SectionHeader']))
    summary_text = executive_summary or (
        "Techwaves EGY conducted an internal Application Security Assessment evaluating authentication, "
        "authorization boundaries (IDOR/BOLA), input validation, injection defenses, cryptography, API workflow integrity, "
        "and SOC detection readiness across 11 security domains. The assessment identified key vulnerabilities requiring "
        "immediate remediation prior to production deployment."
    )
    elements.append(Paragraph(summary_text, styles['Body']))
    elements.append(Spacer(1, 12))

    # 5. Security Posture Scorecard (11 Domains)
    elements.append(Paragraph("2. 11-Domain Security Scorecard", styles['SectionHeader']))

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
        (9, "Cryptography, Secrets & Config Hygiene", 6.5, "Moderate", "TLS 1.3 active; API key template committed."),
        (10, "Logging, Auditing & SOC Telemetry", 4.0, "High Risk", "Missing failed auth logging & correlation ID."),
        (11, "Software Supply Chain & SCA (CVEs)", 7.0, "Compliant", "Dependencies reviewed against live CVE library.")
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

    score_table = Table(table_data, colWidths=[0.3*inch, 2.2*inch, 0.7*inch, 1.1*inch, 2.5*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_PRIMARY),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
    ]))
    elements.append(score_table)
    elements.append(Spacer(1, 14))

    # 6. Detailed Finding Dockets
    elements.append(Paragraph("3. Detailed Vulnerability Dockets", styles['SectionHeader']))

    default_findings = findings or [
        {
            "id": "APP-001",
            "title": "Insecure Direct Object Reference (IDOR) on Order Retrieval",
            "severity": "High",
            "cvss": "8.6",
            "vector": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N",
            "cwe": "CWE-639",
            "endpoint": "GET /api/v1/orders/{orderId}",
            "desc": "The order retrieval endpoint queries the database by order ID without validating that the requesting authenticated user owns the object or belongs to the authorized tenant.",
            "poc": "GET /api/v1/orders/5002 HTTP/1.1\nHost: app.internal\nAuthorization: Bearer <UserA_Token>\n\nHTTP/1.1 200 OK -> UserB order data returned",
            "remediation": "// VULNERABLE\nvar order = await _context.Orders.FindAsync(id);\n\n// SECURE\nvar userId = _currentUser.GetUserId();\nvar order = await _context.Orders.FirstOrDefaultAsync(o => o.Id == id && o.UserId == userId);",
            "sigma": "title: Suspicious Multi-Order IDOR Enumeration\nlogsource: {category: webserver}\ndetection:\n  selection: {cs_method: GET, cs_uri_stem|re: '^/api/v1/orders/\\d+'}\n  timeframe: 1m\n  condition: selection | count() by c_ip > 15\nlevel: high"
        }
    ]

    for f in default_findings:
        f_elements = []
        sev_color = get_severity_color(f['severity'])

        header_tbl = Table([[
            Paragraph(f"<b>[{f['id']}] {f['title']}</b>", styles['FindingTitle']),
            Paragraph(f"<b>{f['severity'].upper()} (CVSS {f['cvss']})</b>", ParagraphStyle('SevBadge', alignment=2, fontName='Helvetica-Bold', fontSize=9, textColor=sev_color))
        ]], colWidths=[5.0*inch, 1.8*inch])
        header_tbl.setStyle(TableStyle([
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
        ]))
        f_elements.append(header_tbl)

        f_meta = [
            [
                Paragraph(f"<b>Endpoint:</b> <font name='Courier'>{f['endpoint']}</font>", styles['TableCell']),
                Paragraph(f"<b>CWE:</b> {f['cwe']}", styles['TableCell']),
                Paragraph(f"<b>Vector:</b> <font size='6.5' name='Courier'>{f['vector']}</font>", styles['TableCell'])
            ]
        ]
        f_meta_tbl = Table(f_meta, colWidths=[3.2*inch, 1.0*inch, 2.6*inch])
        f_meta_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
            ('BOX', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        f_elements.append(f_meta_tbl)
        f_elements.append(Spacer(1, 4))

        f_elements.append(Paragraph(f"<b>Description:</b> {f['desc']}", styles['Body']))
        f_elements.append(Spacer(1, 3))

        # Proof of Concept box
        poc_tbl = Table([[Paragraph(f"<b>Proof of Concept Trace:</b><br/><font name='Courier' size='7'>{f['poc'].replace(chr(10), '<br/>')}</font>", styles['TableCell'])]], colWidths=[6.8*inch])
        poc_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EDF2F7")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        f_elements.append(poc_tbl)
        f_elements.append(Spacer(1, 4))

        # Defensive Remediation box
        rem_tbl = Table([[Paragraph(f"<b>Defensive Remediation Code:</b><br/><font name='Courier' size='7'>{f['remediation'].replace(chr(10), '<br/>')}</font>", styles['TableCell'])]], colWidths=[6.8*inch])
        rem_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0FFF4")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#9AE6B4")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        f_elements.append(rem_tbl)
        f_elements.append(Spacer(1, 4))

        # SOC Rule box
        soc_tbl = Table([[Paragraph(f"<b>SOC Detection Rule (Sigma):</b><br/><font name='Courier' size='7'>{f['sigma'].replace(chr(10), '<br/>')}</font>", styles['TableCell'])]], colWidths=[6.8*inch])
        soc_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EBF8FF")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#BEE3F8")),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        f_elements.append(soc_tbl)
        f_elements.append(Spacer(1, 10))

        elements.append(KeepTogether(f_elements))

    # 7. Approval Gate & Sign-Off
    elements.append(Spacer(1, 8))
    approval_box_data = [
        [
            Paragraph("<b>4. MANDATORY APPROVAL GATE — AWAITING STAKEHOLDER SIGN-OFF</b><br/>"
                      "<i>This document concludes Phase 1 of the assessment. Per enterprise Blue Team operating principles, "
                      "no application code modifications or remediation scripts will be executed until authorized by the "
                      "technical lead or system owner.</i><br/><br/>"
                      "<b>Next Step:</b> Provide written approval to proceed to Phase 2 (Defensive Remediation & Retesting).", styles['TableCell'])
        ]
    ]
    approval_box = Table(approval_box_data, colWidths=[6.8*inch])
    approval_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FFFAF0")),
        ('BOX', (0, 0), (-1, -1), 1, HIGH_ORANGE),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
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
    parser.add_argument("--mode", default="White Box / SAST & DAST", help="Testing mode")
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
