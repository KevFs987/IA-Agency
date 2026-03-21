#!/usr/bin/env python3
"""
IA-Agency Architecture PDF Generator
Converts IA-AGENCY-ARCHITECTURE.md to a professional PDF document.

Usage:
    python generate_architecture_pdf.py [input.md] [output.pdf]
"""

import sys
import re
import os
from datetime import datetime

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.lib.colors import HexColor, black, white
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, HRFlowable, KeepTogether
    )
    from reportlab.graphics.shapes import Drawing, Rect, String
    from reportlab.graphics import renderPDF
except ImportError:
    print("ERROR: ReportLab not installed. Run: pip install reportlab")
    sys.exit(1)

# ── Palette ──────────────────────────────────────────────────────────────────
NAVY      = HexColor("#1a1a2e")
BLUE      = HexColor("#0f3460")
TEAL      = HexColor("#16213e")
CORAL     = HexColor("#e94560")
GREEN     = HexColor("#00b894")
YELLOW    = HexColor("#fdcb6e")
LIGHT_BG  = HexColor("#f8f9fa")
MID_GREY  = HexColor("#dee2e6")
DARK_GREY = HexColor("#495057")
TEXT      = HexColor("#212529")
CODE_BG   = HexColor("#f1f3f5")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm

# ── Styles ────────────────────────────────────────────────────────────────────
def make_styles():
    base = getSampleStyleSheet()

    def ps(name, **kw):
        return ParagraphStyle(name, **kw)

    styles = {
        "cover_title": ps("cover_title",
            fontName="Helvetica-Bold", fontSize=28, textColor=white,
            leading=36, spaceAfter=8, alignment=TA_LEFT),

        "cover_sub": ps("cover_sub",
            fontName="Helvetica", fontSize=13, textColor=HexColor("#adb5bd"),
            leading=18, spaceAfter=4, alignment=TA_LEFT),

        "cover_date": ps("cover_date",
            fontName="Helvetica", fontSize=10, textColor=HexColor("#6c757d"),
            leading=14, alignment=TA_LEFT),

        "h1": ps("h1",
            fontName="Helvetica-Bold", fontSize=18, textColor=NAVY,
            leading=24, spaceBefore=18, spaceAfter=8),

        "h2": ps("h2",
            fontName="Helvetica-Bold", fontSize=13, textColor=BLUE,
            leading=18, spaceBefore=14, spaceAfter=5),

        "h3": ps("h3",
            fontName="Helvetica-Bold", fontSize=11, textColor=TEAL,
            leading=15, spaceBefore=10, spaceAfter=4),

        "h4": ps("h4",
            fontName="Helvetica-Bold", fontSize=10, textColor=DARK_GREY,
            leading=14, spaceBefore=8, spaceAfter=3),

        "body": ps("body",
            fontName="Helvetica", fontSize=9.5, textColor=TEXT,
            leading=15, spaceAfter=4),

        "code": ps("code",
            fontName="Courier", fontSize=8, textColor=HexColor("#343a40"),
            leading=12, spaceAfter=2, backColor=CODE_BG,
            leftIndent=8, rightIndent=8),

        "bullet": ps("bullet",
            fontName="Helvetica", fontSize=9.5, textColor=TEXT,
            leading=14, spaceAfter=2, leftIndent=14, bulletIndent=4),

        "table_header": ps("table_header",
            fontName="Helvetica-Bold", fontSize=9, textColor=white,
            leading=12, alignment=TA_CENTER),

        "table_cell": ps("table_cell",
            fontName="Helvetica", fontSize=8.5, textColor=TEXT,
            leading=12, alignment=TA_LEFT),

        "table_cell_c": ps("table_cell_c",
            fontName="Helvetica", fontSize=8.5, textColor=TEXT,
            leading=12, alignment=TA_CENTER),

        "footer": ps("footer",
            fontName="Helvetica", fontSize=8, textColor=HexColor("#adb5bd"),
            leading=10, alignment=TA_CENTER),

        "blockquote": ps("blockquote",
            fontName="Helvetica-Oblique", fontSize=9.5, textColor=DARK_GREY,
            leading=15, leftIndent=16, spaceAfter=6, spaceBefore=4),

        "badge": ps("badge",
            fontName="Helvetica-Bold", fontSize=8.5, textColor=white,
            leading=11, alignment=TA_CENTER),
    }
    return styles

# ── Page decorations ──────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Top accent bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, h - 6*mm, w, 6*mm, fill=1, stroke=0)
    # Footer line
    canvas.setStrokeColor(MID_GREY)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 13*mm, w - MARGIN, 13*mm)
    # Footer text
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(HexColor("#adb5bd"))
    canvas.drawString(MARGIN, 9*mm, "IA-Agency — Architecture & référentiel des skills")
    canvas.drawRightString(w - MARGIN, 9*mm, f"Page {doc.page}")
    canvas.restoreState()

def on_first_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Full dark cover
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    # Coral accent strip
    canvas.setFillColor(CORAL)
    canvas.rect(0, h * 0.38, w, 4*mm, fill=1, stroke=0)
    canvas.restoreState()

# ── Cover page ────────────────────────────────────────────────────────────────
def make_cover(styles):
    items = []
    items.append(Spacer(1, 70*mm))

    items.append(Paragraph("IA-Agency", styles["cover_title"]))
    items.append(Spacer(1, 2*mm))
    items.append(Paragraph("Architecture &amp; référentiel des skills", ParagraphStyle(
        "cover_sub2", fontName="Helvetica", fontSize=16,
        textColor=HexColor("#e9ecef"), leading=22, alignment=TA_LEFT)))
    items.append(Spacer(1, 10*mm))
    items.append(Paragraph(
        "Agence marketing IA locale — Marché polynésien",
        ParagraphStyle("cover_sub3", fontName="Helvetica-Oblique", fontSize=11,
                       textColor=HexColor("#adb5bd"), leading=16, alignment=TA_LEFT)))
    items.append(Spacer(1, 6*mm))
    items.append(Paragraph(
        f"Généré le {datetime.now().strftime('%d/%m/%Y')}",
        ParagraphStyle("cover_date2", fontName="Helvetica", fontSize=9,
                       textColor=HexColor("#6c757d"), leading=13, alignment=TA_LEFT)))
    items.append(PageBreak())
    return items

# ── Table of contents ─────────────────────────────────────────────────────────
def make_toc(styles):
    items = []
    items.append(Paragraph("Table des matières", styles["h1"]))
    items.append(HRFlowable(width="100%", thickness=1, color=CORAL, spaceAfter=8))

    toc_entries = [
        ("Vue d'ensemble", "3"),
        ("Structure de répertoires", "3"),
        ("Principes architecturaux", "4"),
        ("Flux de routage", "5"),
        ("Catalogue des skills", "6"),
        ("  Groupe 1 — Audit GEO (core)", "6"),
        ("  Groupe 2 — Extensions marché polynésien", "8"),
        ("  Groupe 3 — Workflow commercial", "9"),
        ("  Groupe 4 — Production de contenu", "11"),
        ("  Groupe 5 — Rapports et livrables", "12"),
        ("  Groupe 6 — Pilotage interne", "13"),
        ("Les 5 sous-agents", "14"),
        ("Flux commercial complet", "15"),
        ("État d'implémentation", "15"),
    ]

    toc_data = []
    for title, page in toc_entries:
        toc_data.append([
            Paragraph(title, ParagraphStyle("toc_e", fontName="Helvetica",
                fontSize=9.5, textColor=TEXT, leading=14)),
            Paragraph(page, ParagraphStyle("toc_p", fontName="Helvetica",
                fontSize=9.5, textColor=DARK_GREY, leading=14, alignment=TA_RIGHT)),
        ])

    tbl = Table(toc_data, colWidths=["85%", "15%"])
    tbl.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, MID_GREY),
    ]))
    items.append(tbl)
    items.append(PageBreak())
    return items

# ── Helpers ───────────────────────────────────────────────────────────────────
def score_badge_drawing(label, color, w=56, h=20):
    d = Drawing(w, h)
    d.add(Rect(0, 0, w, h, rx=4, ry=4, fillColor=color, strokeColor=None))
    d.add(String(w/2, 5, label, fontName="Helvetica-Bold", fontSize=8,
                 fillColor=white, textAnchor="middle"))
    return d

def make_status_badge(status):
    if "✅" in status or "Complet" in status:
        color, txt = GREEN, "✓ Complet"
    elif "🚧" in status:
        color, txt = YELLOW, "En cours"
    else:
        color, txt = CORAL, "Planifié"
    return Paragraph(f'<font color="white"><b>{txt}</b></font>',
                     ParagraphStyle("badge_p", fontName="Helvetica-Bold",
                                    fontSize=8, textColor=white,
                                    backColor=color, leading=12,
                                    alignment=TA_CENTER,
                                    borderPadding=(2, 6, 2, 6)))

def make_table(headers, rows, styles, col_widths=None):
    s = styles
    header_row = [Paragraph(h, s["table_header"]) for h in headers]
    data = [header_row]
    for row in rows:
        data.append([Paragraph(str(c), s["table_cell"]) for c in row])

    avail = PAGE_W - 2 * MARGIN
    if col_widths is None:
        n = len(headers)
        col_widths = [avail / n] * n
    else:
        col_widths = [avail * r for r in col_widths]

    tbl = Table(data, colWidths=col_widths, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("GRID", (0, 0), (-1, -1), 0.4, MID_GREY),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return tbl

def section_header(title, styles, color=CORAL):
    items = []
    items.append(Spacer(1, 4*mm))
    items.append(Paragraph(title, styles["h1"]))
    items.append(HRFlowable(width="100%", thickness=1.5, color=color, spaceAfter=6))
    return items

def subsection(title, styles):
    return [Paragraph(title, styles["h2"])]

def subsubsection(title, styles):
    return [Paragraph(title, styles["h3"])]

def body(text, styles):
    # Escape & and handle bold markdown
    text = text.replace("&", "&amp;")
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'`(.+?)`', r'<font name="Courier" size="8.5">\1</font>', text)
    return [Paragraph(text, styles["body"])]

def bullet_item(text, styles):
    text = text.replace("&", "&amp;")
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'`(.+?)`', r'<font name="Courier" size="8.5">\1</font>', text)
    return Paragraph(f"• {text}", styles["bullet"])

def blockquote(text, styles):
    text = text.replace("&", "&amp;")
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    items = []
    # Draw left bar via table
    inner = Paragraph(f"<i>{text}</i>", styles["blockquote"])
    tbl = Table([[inner]], colWidths=[PAGE_W - 2*MARGIN - 8*mm])
    tbl.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#fff3cd")),
        ("LINEBEFORE", (0, 0), (0, -1), 3, CORAL),
    ]))
    items.append(tbl)
    items.append(Spacer(1, 3*mm))
    return items

# ── Main content builder ──────────────────────────────────────────────────────
def build_content(styles):
    story = []

    # ── Cover ──
    story += make_cover(styles)

    # ── ToC ──
    story += make_toc(styles)

    # ══════════════════════════════════════════════════════════════════════════
    # 1. Vue d'ensemble
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header("1. Vue d'ensemble", styles)
    story += body(
        "IA-Agency est une <b>agence marketing IA locale</b> construite sur Claude Code, "
        "ciblant le marché polynésien et les marchés émergents similaires. "
        "Extensions commerciales et workflows adaptés aux marchés où la majorité des entreprises n'ont pas de site web.",
        styles)
    story += body(
        "L'outil permet à une seule personne de gérer <b>15 à 20 clients</b> avec les marges "
        "d'un logiciel, pas d'une agence traditionnelle.",
        styles)

    story.append(Spacer(1, 4*mm))

    # Three input types highlight
    kv_data = [
        ["Type", "Description", "Exemple"],
        ["Cas A — URL web", "Site existant → audit GEO classique", "https://monsite.pf"],
        ["Cas B — URL sociale", "Facebook / Instagram / TikTok uniquement", "https://facebook.com/monresto"],
        ["Cas C — Nom seul", "Reconstruction depuis zéro", '"Resto Te Moana Moorea"'],
    ]
    story.append(make_table(
        kv_data[0], kv_data[1:], styles,
        col_widths=[0.22, 0.52, 0.26]))
    story.append(Spacer(1, 6*mm))

    # ══════════════════════════════════════════════════════════════════════════
    # 2. Structure de répertoires
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header("2. Structure de répertoires", styles)

    tree = """\
IA-Agency/
├── CLAUDE.md              → Mémoire stratégique (lire avant tout)
├── README.md              → Présentation publique
├── install.sh             → Installateur one-command
├── geo/
│   └── SKILL.md           → Routage de 50+ commandes /geo
├── agency/
│   └── SKILL.md           → Routage /agency status et /agency new-skill
├── skills/                → 27 sous-skills (implémentations)
│   ├── geo-audit/         ├── geo-social/         ├── geo-readiness/
│   ├── geo-citability/    ├── geo-discover/        ├── geo-outreach/
│   ├── geo-crawlers/      ├── geo-teaser-report/   ├── geo-prep-call/
│   ├── geo-schema/        ├── geo-prospect/        ├── geo-write-article/
│   ├── geo-technical/     ├── geo-rewrite-page/    ├── geo-content-calendar/
│   ├── geo-content/       ├── geo-social-to-site/  ├── geo-report/
│   ├── geo-report-pdf/    ├── geo-proposal/        ├── geo-compare/
│   ├── geo-llmstxt/       ├── geo-brand-mentions/  ├── geo-crawlers-check/
│   ├── agency-status/     ├── skill-creator/       └── autoresearch/
├── agents/                → 5 sous-agents spécialisés
│   ├── geo-technical.md        ├── geo-schema.md
│   ├── geo-platform-analysis.md ├── geo-ai-visibility.md
│   └── geo-content.md
└── scripts/               → Utilitaires Python (PDF, CRM, scrapers)"""

    story.append(Paragraph(
        tree.replace(" ", "&nbsp;").replace("\n", "<br/>"),
        ParagraphStyle("tree", fontName="Courier", fontSize=7.5,
                       textColor=HexColor("#343a40"), leading=11,
                       backColor=CODE_BG, leftIndent=4, rightIndent=4,
                       spaceBefore=4, spaceAfter=8,
                       borderPadding=(6, 6, 6, 6))))

    # ══════════════════════════════════════════════════════════════════════════
    # 3. Principes architecturaux
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header("3. Principes architecturaux", styles)

    principles = [
        ("1. Trois types d'input", "Toutes les skills marché gèrent : URL de site web, URL sociale (FB/IG/TikTok), et nom de marque seul."),
        ("2. Bilingue par défaut", "Tout contenu produit est pensé FR/EN — français pour le marché local, anglais pour les touristes qui cherchent sur ChatGPT avant d'arriver."),
        ("3. GEO avant SEO", "L'accessibilité aux crawlers IA (GPTBot, ClaudeBot, PerplexityBot…) et la citabilité dans les réponses LLM priment sur le SEO traditionnel."),
        ("4. Règle commerciale d'or", "Révéler le problème. Taire la solution. Aucun rapport de prospection ne contient de tarif ni de plan d'action. Les tarifs n'apparaissent que dans /geo prep-call."),
        ("5. Philosophie read-only", "Les skills de pilotage interne (/agency status, /autoresearch) ne modifient aucun fichier existant. Elles lisent, analysent, et produisent de nouveaux rapports."),
    ]

    for title, desc in principles:
        tbl = Table(
            [[Paragraph(f"<b>{title}</b>", ParagraphStyle("pt", fontName="Helvetica-Bold",
                fontSize=9.5, textColor=NAVY, leading=13)),
              Paragraph(desc, ParagraphStyle("pd", fontName="Helvetica",
                fontSize=9, textColor=TEXT, leading=13))]],
            colWidths=[55*mm, PAGE_W - 2*MARGIN - 55*mm])
        tbl.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 0), (0, 0), LIGHT_BG),
            ("LINEBEFORE", (0, 0), (0, 0), 3, CORAL),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("LINEBELOW", (0, 0), (-1, -1), 0.4, MID_GREY),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 1*mm))

    story.append(Spacer(1, 4*mm))

    # GEO Scoring table
    story += subsubsection("Grille de scoring GEO", styles)
    score_rows = [
        ["AI Citability", "25%", "Citabilité des blocs de contenu par les LLMs"],
        ["Brand Authority", "20%", "Reconnaissance de la marque sur le web"],
        ["Content E-E-A-T", "20%", "Expérience, Expertise, Autorité, Confiance"],
        ["Technical", "15%", "Crawlabilité, vitesse, mobile, SSR"],
        ["Structured Data", "10%", "Schémas Schema.org et JSON-LD"],
        ["Platform Optimization", "10%", "Readiness par plateforme IA"],
    ]
    story.append(make_table(
        ["Catégorie", "Poids", "Description"],
        score_rows, styles, col_widths=[0.30, 0.12, 0.58]))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # 4. Flux de routage
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header("4. Flux de routage", styles)
    story += body("Les commandes utilisateur arrivent toutes via l'un des deux orchestrateurs :", styles)

    routing_rows = [
        ["`geo/SKILL.md`", "Routeur principal", "Toutes les commandes `/geo ...`"],
        ["`agency/SKILL.md`", "Routeur interne", "`/agency status`, `/agency new-skill`"],
    ]
    story.append(make_table(
        ["Fichier", "Rôle", "Commandes"],
        routing_rows, styles, col_widths=[0.28, 0.22, 0.50]))

    story.append(Spacer(1, 5*mm))
    story += body("Lors d'un <b>audit complet</b> (`/geo audit`), le skill `geo-audit` orchestre en parallèle les 4 sous-agents spécialisés :", styles)

    agents_flow = [
        ["Sous-agent", "Spécialité"],
        ["`agents/geo-technical.md`", "Core Web Vitals, SSR, crawlabilité"],
        ["`agents/geo-schema.md`", "JSON-LD, sameAs, schémas deprecated"],
        ["`agents/geo-ai-visibility.md`", "Citabilité, brand mentions, Wikipedia"],
        ["`agents/geo-content.md`", "E-E-A-T, détection contenu IA générique"],
    ]
    story.append(make_table(
        agents_flow[0], agents_flow[1:], styles, col_widths=[0.45, 0.55]))

    story.append(Spacer(1, 5*mm))
    story += body("Après agrégation des résultats des 4 sous-agents, `geo-audit` produit le rapport final `GEO-AUDIT-REPORT.md`.", styles)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # 5. Catalogue des skills
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header("5. Catalogue des skills", styles)

    # ── Groupe 1 ──────────────────────────────────────────────────────────────
    story += subsection("Groupe 1 — Audit GEO (core)", styles)

    skills_g1 = [
        {
            "cmd": "/geo audit <url>",
            "skill": "skills/geo-audit/",
            "desc": "Orchestrateur principal. Lance un audit complet GEO+SEO en 3 phases : détection du type de business, lancement en parallèle des 4 sous-agents, synthèse avec score composite et plan d'action priorisé.",
            "output": "GEO-AUDIT-REPORT.md",
        },
        {
            "cmd": "(appelé par geo-audit)",
            "skill": "skills/geo-citability/",
            "desc": "Mesure la citabilité IA du contenu. Scoring en 5 dimensions : Answer Block Quality 30%, Auto-suffisance 25%, Lisibilité structurelle 20%, Densité statistique 15%, Unicité 10%. Cible : blocs de 134-167 mots.",
            "output": "Scores + recommandations",
        },
        {
            "cmd": "(appelé par geo-audit)",
            "skill": "skills/geo-crawlers/",
            "desc": "Analyse l'accès des 14 crawlers IA au site (robots.txt, headers). Tier 1 critique : GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, PerplexityBot. Point clé : ces crawlers n'exécutent pas le JavaScript.",
            "output": "Tableau statuts crawlers",
        },
        {
            "cmd": "(appelé par geo-audit)",
            "skill": "skills/geo-schema/",
            "desc": "Audit et génération de données structurées Schema.org (JSON-LD préféré). 10+ types de schémas. Accent sur la stratégie sameAs (14+ liens plateformes tierces) pour la reconnaissance d'entité LLM.",
            "output": "JSON-LD + score",
        },
        {
            "cmd": "(appelé par geo-audit)",
            "skill": "skills/geo-technical/",
            "desc": "Audit technique SEO en 8 catégories sur 100 pts : Crawlabilité 15, Indexabilité 12, Sécurité 10, URLs 8, Mobile 10, Core Web Vitals 15, SSR 15, Vitesse 15.",
            "output": "Rapport technique + score",
        },
        {
            "cmd": "(appelé par geo-audit)",
            "skill": "skills/geo-content/",
            "desc": "Évaluation E-E-A-T (25 pts par dimension) : Experience, Expertise, Authoritativeness, Trustworthiness. Cible lisibilité Flesch 60-70.",
            "output": "Score E-E-A-T + rapport",
        },
    ]

    for sk in skills_g1:
        tbl = Table([
            [Paragraph(f'<font name="Courier" size="8"><b>{sk["cmd"]}</b></font>',
                        ParagraphStyle("cmd_p", fontName="Courier", fontSize=8,
                                       textColor=BLUE, leading=11)),
             Paragraph(f'<font name="Courier" size="7.5">{sk["skill"]}</font>',
                        ParagraphStyle("sk_p", fontName="Courier", fontSize=7.5,
                                       textColor=DARK_GREY, leading=11, alignment=TA_RIGHT))],
        ], colWidths=[(PAGE_W - 2*MARGIN)*0.6, (PAGE_W - 2*MARGIN)*0.4])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("LINEBEFORE", (0, 0), (0, 0), 3, BLUE),
        ]))
        story.append(tbl)
        story += body(sk["desc"], styles)
        story.append(Paragraph(
            f'<font color="#6c757d">Output : </font><font name="Courier" size="8">{sk["output"]}</font>',
            ParagraphStyle("output_p", fontName="Helvetica", fontSize=8.5,
                           textColor=DARK_GREY, leading=12, spaceAfter=8)))

    story.append(PageBreak())

    # ── Groupe 2 ──────────────────────────────────────────────────────────────
    story += subsection("Groupe 2 — Extensions marché polynésien", styles)

    skills_g2 = [
        {
            "cmd": "/geo audit https://facebook.com/...",
            "skill": "skills/geo-social/",
            "desc": "Audite une présence sociale uniquement (Facebook, Instagram, TikTok) quand l'entreprise n'a pas de site. Extrait : nom de marque, description, fréquence de publication, signaux d'autorité. Identifie les gaps (pas de site, pas de GMB, pas de schéma).",
            "output": "Score maturité 0-100 + roadmap",
        },
        {
            "cmd": '/geo audit "Nom de marque"',
            "skill": "skills/geo-discover/",
            "desc": "Reconstruit une présence digitale complète depuis un simple nom. Cherche sur Google Maps, TripAdvisor, Facebook, Instagram, Pages Jaunes Polynésie, Wikipedia…",
            "output": "Profil consolidé + liens sameAs + score",
        },
        {
            "cmd": "/geo readiness <url-ou-nom>",
            "skill": "skills/geo-readiness/",
            "desc": "Positionne l'entreprise sur un spectre de maturité à 5 niveaux : Niveau 0 (aucune trace), Niveau 1 (social only), Niveau 2 (site basique), Niveau 3 (SEO), Niveau 4 (GEO-ready). Pour chaque niveau : plan d'action + estimation de coût + timeline.",
            "output": "Rapport de maturité + plan d'action",
        },
    ]

    for sk in skills_g2:
        tbl = Table([
            [Paragraph(f'<font name="Courier" size="8"><b>{sk["cmd"]}</b></font>',
                        ParagraphStyle("cmd_p2", fontName="Courier", fontSize=8,
                                       textColor=GREEN, leading=11)),
             Paragraph(f'<font name="Courier" size="7.5">{sk["skill"]}</font>',
                        ParagraphStyle("sk_p2", fontName="Courier", fontSize=7.5,
                                       textColor=DARK_GREY, leading=11, alignment=TA_RIGHT))],
        ], colWidths=[(PAGE_W - 2*MARGIN)*0.6, (PAGE_W - 2*MARGIN)*0.4])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f0fff4")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("LINEBEFORE", (0, 0), (0, 0), 3, GREEN),
        ]))
        story.append(tbl)
        story += body(sk["desc"], styles)
        story.append(Paragraph(
            f'<font color="#6c757d">Output : </font><font name="Courier" size="8">{sk["output"]}</font>',
            ParagraphStyle("output_p2", fontName="Helvetica", fontSize=8.5,
                           textColor=DARK_GREY, leading=12, spaceAfter=8)))

    # Maturity table
    story += subsubsection("Niveaux de maturité (geo-readiness)", styles)
    mat_rows = [
        ["0", "Aucune trace digitale", "Pas d'existence en ligne"],
        ["1", "Social only", "Facebook / Instagram / TikTok uniquement"],
        ["2", "Site basique sans SEO", "Présence web sans optimisation"],
        ["3", "Site avec SEO traditionnel", "Google Search optimisé"],
        ["4", "GEO-ready", "Cible finale — visible sur les LLMs"],
    ]
    story.append(make_table(
        ["Niveau", "Description", "Détail"],
        mat_rows, styles, col_widths=[0.10, 0.30, 0.60]))

    story.append(PageBreak())

    # ── Groupe 3 ──────────────────────────────────────────────────────────────
    story += subsection("Groupe 3 — Workflow commercial (prospecting)", styles)

    story += body(
        "Ces skills implémentent le flux de <b>prospection automatisée</b> — "
        "de la découverte du lead au closing, sans jamais mentionner de tarif dans les documents partagés.",
        styles)
    story.append(Spacer(1, 3*mm))

    skills_g3 = [
        {
            "cmd": '/geo prospect scan "<niche>" "<ville>"',
            "skill": "skills/geo-prospect/",
            "desc": 'CRM-lite intégré. Scrape Google Maps + Pages Jaunes, score 15-25 entreprises locales, filtre les scores < 50. Autres commandes : new, list, show, audit, note, status, won, lost, pipeline. Stockage JSON : ~/.geo-prospects/prospects.json. Pipeline : lead → qualified → proposal → won/lost.',
            "output": "Liste leads priorisés + JSON CRM",
        },
        {
            "cmd": "/geo outreach <url-ou-nom>",
            "skill": "skills/geo-outreach/",
            "desc": "Génère un message de prospection personnalisé basé sur les problèmes réels — pas un template générique. 3 formats : Email (150-200 mots), DM Instagram/Facebook (80-100 mots), WhatsApp (40-60 mots). Disponible FR et EN.",
            "output": "3 messages par canal",
        },
        {
            "cmd": "/geo teaser-report <url-ou-nom>",
            "skill": "skills/geo-teaser-report/",
            "desc": "Rapport PDF 2 pages pour la prospection. Applique la règle « révéler le problème, taire la solution ». Contient : score global, 3 problèmes critiques nommés, impact business estimé, CTA vers un appel. Ne contient pas : solutions, plan d'action, tarifs.",
            "output": "GEO-TEASER-[nom]-[date].md + PDF",
        },
        {
            "cmd": "/geo prep-call <url-ou-nom>",
            "skill": "skills/geo-prep-call/",
            "desc": "Briefing commercial confidentiel avant un RDV prospect. Jamais partagé avec le prospect. Contient : profil du prospect, 3 douleurs à exploiter, 14 questions de découverte, 6 objections avec réponses suggérées, 3 tiers tarifaires (seul endroit où les tarifs apparaissent), structure du RDV (5-45 min).",
            "output": "Document confidentiel (jamais partagé)",
        },
    ]

    for sk in skills_g3:
        tbl = Table([
            [Paragraph(f'<font name="Courier" size="8"><b>{sk["cmd"]}</b></font>',
                        ParagraphStyle("cmd_p3", fontName="Courier", fontSize=8,
                                       textColor=CORAL, leading=11)),
             Paragraph(f'<font name="Courier" size="7.5">{sk["skill"]}</font>',
                        ParagraphStyle("sk_p3", fontName="Courier", fontSize=7.5,
                                       textColor=DARK_GREY, leading=11, alignment=TA_RIGHT))],
        ], colWidths=[(PAGE_W - 2*MARGIN)*0.65, (PAGE_W - 2*MARGIN)*0.35])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#fff5f5")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("LINEBEFORE", (0, 0), (0, 0), 3, CORAL),
        ]))
        story.append(tbl)
        story += body(sk["desc"], styles)
        story.append(Paragraph(
            f'<font color="#6c757d">Output : </font><font name="Courier" size="8">{sk["output"]}</font>',
            ParagraphStyle("output_p3", fontName="Helvetica", fontSize=8.5,
                           textColor=DARK_GREY, leading=12, spaceAfter=8)))

    story.append(PageBreak())

    # ── Groupe 4 ──────────────────────────────────────────────────────────────
    story += subsection("Groupe 4 — Production de contenu", styles)

    skills_g4 = [
        {
            "cmd": '/geo write-article <url> "<sujet>"',
            "skill": "skills/geo-write-article/",
            "desc": "Écrit un article optimisé pour la citabilité IA avec des blocs de 134-167 mots (longueur idéale pour être cité par un LLM). Structure : Intro hero → Réponse directe → Angle unique → Info pratique → FAQ 3 questions → CTA. Signaux E-E-A-T intégrés, bilingue FR/EN (adapté, pas traduit).",
            "output": "Article + version EN",
        },
        {
            "cmd": "/geo rewrite-page <url>",
            "skill": "skills/geo-rewrite-page/",
            "desc": "Réécrit une page existante pour les LLMs : premier paragraphe = réponse directe, chaque H2 = question qu'un utilisateur poserait à ChatGPT, structure lisible par les crawlers IA.",
            "output": "Contenu réécrit + rapport diagnostic avant/après",
        },
        {
            "cmd": "/geo content-calendar <url> <mois>",
            "skill": "skills/geo-content-calendar/",
            "desc": "Calendrier éditorial sur N mois. Intègre les cycles touristiques polynésiens (Heiva juillet, baleines mai-oct, surf mai-sept). Scoring des sujets : Impact citabilité × Volume recherche × Facilité. Stratégie bilingue selon la saison.",
            "output": "Calendrier N mois + scoring sujets",
        },
        {
            "cmd": "/geo social-to-site <url-sociale>",
            "skill": "skills/geo-social-to-site/",
            "desc": "Récupère le contenu d'une page sociale (photos, descriptions, posts) et génère les specs d'un site one-page bilingue FR/EN. Réutilise ce que l'entreprise produit déjà — pas de contenu à créer from scratch.",
            "output": "Specs site one-page FR/EN",
        },
    ]

    for sk in skills_g4:
        tbl = Table([
            [Paragraph(f'<font name="Courier" size="8"><b>{sk["cmd"]}</b></font>',
                        ParagraphStyle("cmd_p4", fontName="Courier", fontSize=8,
                                       textColor=HexColor("#6f42c1"), leading=11)),
             Paragraph(f'<font name="Courier" size="7.5">{sk["skill"]}</font>',
                        ParagraphStyle("sk_p4", fontName="Courier", fontSize=7.5,
                                       textColor=DARK_GREY, leading=11, alignment=TA_RIGHT))],
        ], colWidths=[(PAGE_W - 2*MARGIN)*0.65, (PAGE_W - 2*MARGIN)*0.35])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f8f0ff")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("LINEBEFORE", (0, 0), (0, 0), 3, HexColor("#6f42c1")),
        ]))
        story.append(tbl)
        story += body(sk["desc"], styles)
        story.append(Paragraph(
            f'<font color="#6c757d">Output : </font><font name="Courier" size="8">{sk["output"]}</font>',
            ParagraphStyle("output_p4", fontName="Helvetica", fontSize=8.5,
                           textColor=DARK_GREY, leading=12, spaceAfter=8)))

    story.append(PageBreak())

    # ── Groupe 5 ──────────────────────────────────────────────────────────────
    story += subsection("Groupe 5 — Rapports et livrables", styles)

    skills_g5 = [
        {
            "cmd": "/geo report <url>",
            "skill": "skills/geo-report/",
            "desc": "Rapport client complet en 12 sections. Formule : GEO Score = (Platform×0.25) + (Content×0.25) + (Technical×0.20) + (Schema×0.15) + (Brand×0.15).",
            "output": "GEO-CLIENT-REPORT.md",
        },
        {
            "cmd": "/geo report-pdf <url>",
            "skill": "skills/geo-report-pdf/",
            "desc": "Génère un PDF professionnel via ReportLab (Python). Contient : page de couverture, résumé exécutif, breakdown des scores avec graphiques, tableau crawlers, plan d'action, annexes.",
            "output": "GEO-REPORT-[marque].pdf",
        },
        {
            "cmd": "/geo proposal <url>",
            "skill": "skills/geo-proposal/",
            "desc": "Génère automatiquement une proposition commerciale depuis les données d'audit. 3 tiers : Basic ~2 500 €/mois, Standard ~5 000 €/mois, Premium ~9 500 €/mois.",
            "output": "Proposition commerciale",
        },
        {
            "cmd": "/geo compare <url>",
            "skill": "skills/geo-compare/",
            "desc": "Tracking mensuel — compare deux audits dans le temps. Affiche les deltas : scores, catégories, plateformes, crawlers. Indispensable pour les clients en retainer mensuel.",
            "output": "Rapport delta avant/après",
        },
    ]

    for sk in skills_g5:
        tbl = Table([
            [Paragraph(f'<font name="Courier" size="8"><b>{sk["cmd"]}</b></font>',
                        ParagraphStyle("cmd_p5", fontName="Courier", fontSize=8,
                                       textColor=HexColor("#fd7e14"), leading=11)),
             Paragraph(f'<font name="Courier" size="7.5">{sk["skill"]}</font>',
                        ParagraphStyle("sk_p5", fontName="Courier", fontSize=7.5,
                                       textColor=DARK_GREY, leading=11, alignment=TA_RIGHT))],
        ], colWidths=[(PAGE_W - 2*MARGIN)*0.6, (PAGE_W - 2*MARGIN)*0.4])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#fff8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("LINEBEFORE", (0, 0), (0, 0), 3, HexColor("#fd7e14")),
        ]))
        story.append(tbl)
        story += body(sk["desc"], styles)
        story.append(Paragraph(
            f'<font color="#6c757d">Output : </font><font name="Courier" size="8">{sk["output"]}</font>',
            ParagraphStyle("output_p5", fontName="Helvetica", fontSize=8.5,
                           textColor=DARK_GREY, leading=12, spaceAfter=8)))

    story.append(PageBreak())

    # ── Groupe 6 ──────────────────────────────────────────────────────────────
    story += subsection("Groupe 6 — Pilotage interne", styles)

    skills_g6 = [
        {
            "cmd": "/agency status",
            "skill": "skills/agency-status/",
            "desc": "Auto-diagnostic du dépôt vs le roadmap dans CLAUDE.md. 4 phases : cartographie de l'existant, analyse des ajouts non planifiés, comparaison roadmap vs réalité, génération du rapport. Vérifie les 11 extensions de la roadmap.",
            "output": "AGENCY-STATUS-[AAAA-MM-JJ].md",
        },
        {
            "cmd": "/agency new-skill <nom>",
            "skill": "skills/skill-creator/",
            "desc": "Crée ou améliore des fichiers SKILL.md en suivant les standards du projet. Workflow : Intent → Research → Write SKILL.md → Test cases → Routing update → Iterate. Enforces structure frontmatter, gestion des 3 types d'input, mise à jour du routage dans geo/SKILL.md.",
            "output": "Nouveau SKILL.md + mise à jour routage",
        },
        {
            "cmd": "/autoresearch (interne)",
            "skill": "skills/autoresearch/",
            "desc": "Boucle d'optimisation autonome (inspirée Karpathy). Phase 0 : init et définition de la métrique. Phase 1 : boucle principale — analyser les échecs → backup → modifier UNE seule chose → tester → KEEP ou DISCARD. Phase 2 : rapport. Stop quand pass_rate >= threshold ou iterations >= 30.",
            "output": "Rapport d'optimisation + skills améliorées",
        },
    ]

    for sk in skills_g6:
        tbl = Table([
            [Paragraph(f'<font name="Courier" size="8"><b>{sk["cmd"]}</b></font>',
                        ParagraphStyle("cmd_p6", fontName="Courier", fontSize=8,
                                       textColor=TEAL, leading=11)),
             Paragraph(f'<font name="Courier" size="7.5">{sk["skill"]}</font>',
                        ParagraphStyle("sk_p6", fontName="Courier", fontSize=7.5,
                                       textColor=DARK_GREY, leading=11, alignment=TA_RIGHT))],
        ], colWidths=[(PAGE_W - 2*MARGIN)*0.6, (PAGE_W - 2*MARGIN)*0.4])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f0f4ff")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("LINEBEFORE", (0, 0), (0, 0), 3, TEAL),
        ]))
        story.append(tbl)
        story += body(sk["desc"], styles)
        story.append(Paragraph(
            f'<font color="#6c757d">Output : </font><font name="Courier" size="8">{sk["output"]}</font>',
            ParagraphStyle("output_p6", fontName="Helvetica", fontSize=8.5,
                           textColor=DARK_GREY, leading=12, spaceAfter=8)))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # 6. Les 5 sous-agents
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header("6. Les 5 sous-agents", styles)
    story += body(
        "Les sous-agents sont des spécialistes lancés en <b>parallèle</b> par `geo-audit`. "
        "Chacun produit un rapport partiel qui est ensuite agrégé dans le score composite final.",
        styles)
    story.append(Spacer(1, 4*mm))

    agent_rows = [
        ["geo-technical.md", "Audit technique",
         "Core Web Vitals (LCP <2.5s, INP <200ms, CLS <0.1), crawlabilité, SSR, indexabilité"],
        ["geo-platform-analysis.md", "Optimisation plateforme",
         "Score par plateforme IA : Google AIO, ChatGPT, Perplexity, Gemini, Bing Copilot"],
        ["geo-schema.md", "Données structurées",
         "JSON-LD, sameAs, schémas deprecated (FAQPage restreint août 2023, HowTo retiré sept 2023)"],
        ["geo-ai-visibility.md", "Visibilité IA",
         "Citabilité 5 dimensions, brand mentions, vérification Wikipedia via API"],
        ["geo-content.md", "Qualité contenu",
         "E-E-A-T 4×25 pts, Flesch 50-70, détection contenu IA générique"],
    ]
    story.append(make_table(
        ["Agent", "Rôle", "Spécialité clé"],
        agent_rows, styles, col_widths=[0.25, 0.20, 0.55]))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # 7. Flux commercial complet
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header("7. Flux commercial complet", styles)

    story += body(
        "La règle d'or : <b>le tarif n'apparaît que dans un contexte oral, jamais dans un PDF partagé.</b>",
        styles)
    story.append(Spacer(1, 4*mm))

    flow_rows = [
        ["1", "/geo prospect scan", "Génère 20 leads scorés, filtrés < 50", "Liste priorisée"],
        ["2", "/geo outreach", "Message personnalisé (Email / DM / WhatsApp)", "3 formats FR/EN"],
        ["3", "/geo teaser-report", "PDF 2p : problème sans solution → crée la douleur", "Fichier PDF"],
        ["4", "Prospect rappelle", "Le prospect initie le contact", "—"],
        ["5", "/geo prep-call", "Briefing confidentiel : 14 questions, 6 objections, tarifs", "Doc confidentiel"],
        ["6", "Closing", "Le tarif n'apparaît que dans ce contexte oral", "Contrat signé"],
    ]
    story.append(make_table(
        ["Étape", "Commande", "Action", "Output"],
        flow_rows, styles, col_widths=[0.07, 0.25, 0.43, 0.25]))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # 8. État d'implémentation
    # ══════════════════════════════════════════════════════════════════════════
    story += section_header("8. État d'implémentation", styles)
    story += body(f"Rapport d'état au {datetime.now().strftime('%d/%m/%Y')} — 13/13 extensions (100%)", styles)
    story.append(Spacer(1, 3*mm))

    status_rows = [
        ["geo-social", "/geo audit https://facebook.com/...", "Priorité HAUTE", "✓ Complet"],
        ["geo-discover", '/geo audit "Nom de marque"', "Priorité HAUTE", "✓ Complet"],
        ["geo-readiness", "/geo readiness <url-ou-nom>", "Priorité HAUTE", "✓ Complet"],
        ["geo-outreach", "/geo outreach <url-ou-nom>", "Priorité HAUTE", "✓ Complet"],
        ["geo-teaser-report", "/geo teaser-report <url-ou-nom>", "Priorité HAUTE", "✓ Complet"],
        ["geo-prep-call", "/geo prep-call <url-ou-nom>", "Priorité HAUTE", "✓ Complet"],
        ["geo-social-to-site", "/geo social-to-site <url-sociale>", "Priorité MOYENNE", "✓ Complet"],
        ["geo-write-article", '/geo write-article <url> "<sujet>"', "Priorité MOYENNE", "✓ Complet"],
        ["geo-rewrite-page", "/geo rewrite-page <url>", "Priorité MOYENNE", "✓ Complet"],
        ["geo-content-calendar", "/geo content-calendar <url> <mois>", "Priorité MOYENNE", "✓ Complet"],
        ["geo-prospect scan", '/geo prospect scan "<niche>" "<ville>"', "Commercial", "✓ Complet"],
        ["agency-status", "/agency status", "Pilotage interne", "✓ Complet"],
        ["skill-creator", "/agency new-skill", "Pilotage interne", "✓ Complet"],
    ]

    # Build with colored status column
    header_row = [Paragraph(h, styles["table_header"])
                  for h in ["Extension", "Commande", "Priorité", "Statut"]]
    data = [header_row]
    for row in status_rows:
        status_p = Paragraph(
            f'<b>{row[3]}</b>',
            ParagraphStyle("st_ok", fontName="Helvetica-Bold", fontSize=8.5,
                           textColor=white, leading=12, alignment=TA_CENTER))
        data.append([
            Paragraph(f'<font name="Courier" size="8">{row[0]}</font>',
                      styles["table_cell"]),
            Paragraph(f'<font name="Courier" size="7.5">{row[1]}</font>',
                      styles["table_cell"]),
            Paragraph(row[2], styles["table_cell_c"]),
            status_p,
        ])

    avail = PAGE_W - 2 * MARGIN
    tbl = Table(data, colWidths=[avail*0.20, avail*0.43, avail*0.22, avail*0.15],
                repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT_BG]),
        ("GRID", (0, 0), (-1, -1), 0.4, MID_GREY),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]
    # Color status cells green
    for i in range(1, len(data)):
        style_cmds.append(("BACKGROUND", (3, i), (3, i), GREEN))

    tbl.setStyle(TableStyle(style_cmds))
    story.append(tbl)

    story.append(Spacer(1, 8*mm))
    story += blockquote(
        "Pour un rapport d'état en temps réel : /agency status — "
        "Ce document est la mémoire stratégique du projet. "
        "Le mettre à jour à chaque décision importante.",
        styles)

    return story


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    input_md = sys.argv[1] if len(sys.argv) > 1 else "IA-AGENCY-ARCHITECTURE.md"
    output_pdf = sys.argv[2] if len(sys.argv) > 2 else "IA-AGENCY-ARCHITECTURE.pdf"

    # Resolve paths relative to script location if not absolute
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)

    if not os.path.isabs(output_pdf):
        output_pdf = os.path.join(repo_root, output_pdf)

    print(f"Generating PDF: {output_pdf}")

    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN + 6*mm,
        bottomMargin=20*mm,
        title="IA-Agency — Architecture & référentiel des skills",
        author="IA-Agency",
        subject="Architecture complète et catalogue des skills",
    )

    styles = make_styles()
    story = build_content(styles)

    doc.build(story,
              onFirstPage=on_first_page,
              onLaterPages=on_page)

    size_kb = os.path.getsize(output_pdf) / 1024
    print(f"Done! {output_pdf} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
