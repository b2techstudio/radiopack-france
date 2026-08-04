#!/usr/bin/env python3
"""Generate the Annecy / Haute-Savoie pack guide PDF.

Dependency:
    pip install -r requirements-generator.txt
"""
from __future__ import annotations

import csv
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "website/public/downloads/annecy-haute-savoie/radiopack-france-annecy-haute-savoie-v0.1.csv"
PDF_PATH = ROOT / "website/public/downloads/annecy-haute-savoie/radiopack-france-annecy-haute-savoie-v0.1-guide.pdf"

PURPLE = colors.HexColor("#6E3DE8")
CYAN = colors.HexColor("#00A7BB")
BLUE = colors.HexColor("#1687E9")
ORANGE = colors.HexColor("#F09A20")
INK = colors.HexColor("#182230")
MUTED = colors.HexColor("#5C6878")
LIGHT = colors.HexColor("#F1F5FA")
LINE = colors.HexColor("#D8E0EA")

def header_footer(canvas, doc):
    canvas.saveState()
    width, height = landscape(A4)
    canvas.setFillColor(LIGHT)
    canvas.rect(0, height - 17 * mm, width, 17 * mm, fill=1, stroke=0)
    canvas.setFillColor(CYAN)
    canvas.rect(0, height - 17 * mm, 7 * mm, 17 * mm, fill=1, stroke=0)
    canvas.setFillColor(INK)
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(13 * mm, height - 10.5 * mm, "B2Tech Studio - RadioPack France")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(width - 12 * mm, height - 10.5 * mm, "Annecy & Haute-Savoie v0.1 - reception seule")
    canvas.setStrokeColor(LINE)
    canvas.line(12 * mm, 12 * mm, width - 12 * mm, 12 * mm)
    canvas.drawString(12 * mm, 7 * mm, "Donnees verifiees le 4 aout 2026")
    canvas.drawRightString(width - 12 * mm, 7 * mm, f"Page {doc.page}")
    canvas.restoreState()

def build():
    with CSV_PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    doc = BaseDocTemplate(
        str(PDF_PATH),
        pagesize=landscape(A4),
        rightMargin=12 * mm,
        leftMargin=12 * mm,
        topMargin=22 * mm,
        bottomMargin=16 * mm,
        title="RadioPack France - Annecy et Haute-Savoie v0.1",
        author="B2Tech Studio",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=header_footer)])

    styles = getSampleStyleSheet()
    title = ParagraphStyle("TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=28, leading=32, textColor=INK, spaceAfter=8)
    subtitle = ParagraphStyle("Subtitle", parent=title, fontSize=18, leading=22, textColor=CYAN)
    h1 = ParagraphStyle("H1Custom", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=CYAN, spaceAfter=8)
    h2 = ParagraphStyle("H2Custom", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=BLUE, spaceBefore=4, spaceAfter=6)
    body = ParagraphStyle("BodyCustom", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.2, leading=13, textColor=INK)
    small = ParagraphStyle("SmallCustom", parent=body, fontSize=7.4, leading=9.2, textColor=MUTED)
    callout = ParagraphStyle("Callout", parent=body, backColor=colors.HexColor("#FFF4DF"), borderColor=ORANGE, borderWidth=0.7, borderPadding=7, spaceBefore=7, spaceAfter=9)

    story = [
        Spacer(1, 9 * mm),
        Paragraph("RadioPack France", title),
        Paragraph("Annecy & Haute-Savoie v0.1", subtitle),
        Spacer(1, 3 * mm),
        Paragraph("Codeplug CHIRP pour Quansheng UV-K5 - 36 memoires - reception seule", h2),
        Spacer(1, 4 * mm),
        Paragraph(
            "Ce premier pack Alpes du Nord regroupe les bases nationales utiles, l'aviation "
            "d'Annecy-Meythet et d'Annemasse, ainsi que neuf sorties de relais ou de "
            "transpondeurs analogiques verifiees en Haute-Savoie, dans l'Ain et en Savoie.",
            body,
        ),
        Spacer(1, 6 * mm),
    ]

    stats = [
        ["PMR446", "16", "0-15"],
        ["APRS / ISS", "6", "20-25"],
        ["Appels amateur", "2", "30-31"],
        ["Aviation", "3", "40-42"],
        ["Sorties analogiques", "9", "50-58"],
        ["Total", "36", "0-58 avec intervalles"],
    ]
    summary = Table([["Categorie", "Memoires", "Positions"]] + stats, colWidths=[75 * mm, 35 * mm, 75 * mm])
    summary.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), CYAN),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#DDF7F8")),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, LIGHT]),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story += [
        Paragraph("Organisation des memoires", h1),
        summary,
        Spacer(1, 5 * mm),
        Paragraph(
            "<b>Important :</b> toutes les lignes utilisent <b>Duplex=off</b>. "
            "Le fichier public est destine a l'ecoute et ne constitue pas une autorisation d'emettre.",
            callout,
        ),
        PageBreak(),
        Paragraph("Sorties analogiques verifiees", h1),
        Paragraph(
            "Les frequences partagees par plusieurs transpondeurs ne sont inscrites qu'une seule fois. "
            "Les indicatifs associes sont conserves dans le commentaire de la memoire.",
            body,
        ),
        Spacer(1, 3 * mm),
    ]

    repeaters = [row for row in rows if 50 <= int(row["Location"]) <= 58]
    repeater_table_data = [["Memoire", "Nom", "Frequence", "Mode", "Description"]]
    for row in repeaters:
        repeater_table_data.append([
            row["Location"],
            row["Name"],
            row["Frequency"],
            row["Mode"],
            Paragraph(row["Comment"], small),
        ])
    repeater_table = Table(repeater_table_data, colWidths=[18 * mm, 27 * mm, 30 * mm, 19 * mm, 174 * mm], repeatRows=1)
    repeater_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("FONTSIZE", (0, 0), (3, -1), 7.4),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story += [repeater_table, PageBreak(), Paragraph("Liste complete des memoires", h1)]

    groups = [
        ("PMR446", 0, 15),
        ("APRS et ISS", 20, 25),
        ("Canaux d'appel radioamateur", 30, 31),
        ("Aviation", 40, 42),
        ("Relais et transpondeurs analogiques", 50, 58),
    ]
    for label, start, end in groups:
        group = [row for row in rows if start <= int(row["Location"]) <= end]
        story.append(Paragraph(f"{label} - memoires {start} a {end}", h2))
        data = [["Mem.", "Nom", "Frequence MHz", "Mode", "Pas", "Description"]]
        for row in group:
            data.append([
                row["Location"],
                row["Name"],
                row["Frequency"],
                row["Mode"],
                row["TStep"],
                Paragraph(row["Comment"], small),
            ])
        table = Table(data, colWidths=[15 * mm, 25 * mm, 30 * mm, 17 * mm, 17 * mm, 164 * mm], repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3E4F65")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.3, LINE),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
            ("FONTSIZE", (0, 0), (4, -1), 7.1),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 2.5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ]))
        story += [table, Spacer(1, 4 * mm)]

    story += [
        PageBreak(),
        Paragraph("Sources principales", h1),
        Paragraph("<b>Relais :</b> tableau officiel du REF, derniere mise a jour indiquee le 13 mai 2026.", body),
        Paragraph("<b>Annecy-Meythet :</b> SIA eAIP AIRAC 07/26, frequence 118,200 MHz.", body),
        Paragraph("<b>Annemasse :</b> SIA eAIP AIRAC 07/26, frequence A-A 125,875 MHz.", body),
        Spacer(1, 5 * mm),
        Paragraph(
            "Les etats des relais et les donnees aeronautiques peuvent changer. "
            "Verifier les versions plus recentes du REF, de l'eAIP et les NOTAM.",
            callout,
        ),
        Paragraph("Procedure CHIRP", h1),
        Paragraph(
            "1. Lire la radio et sauvegarder son image d'origine. "
            "2. Importer le CSV Annecy v0.1. "
            "3. Verifier les positions et les modes. "
            "4. Ecrire vers la radio. "
            "5. Tester d'abord la reception.",
            body,
        ),
    ]

    PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.build(story)
    print(PDF_PATH)

if __name__ == "__main__":
    build()
