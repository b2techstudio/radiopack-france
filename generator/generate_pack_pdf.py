#!/usr/bin/env python3
"""Generate the Normandie pack guide PDF.

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
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv"
PDF_PATH = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1-guide.pdf"

PURPLE = colors.HexColor("#6E3DE8")
BLUE = colors.HexColor("#1687E9")
ORANGE = colors.HexColor("#F09A20")
INK = colors.HexColor("#182230")
MUTED = colors.HexColor("#5C6878")
LIGHT = colors.HexColor("#F1F5FA")
LINE = colors.HexColor("#D8E0EA")

def clean(value: str) -> str:
    return value.replace("—", "-").replace("’", "'").replace("œ", "oe")

def header_footer(canvas, doc):
    canvas.saveState()
    w, h = landscape(A4)
    canvas.setFillColor(LIGHT)
    canvas.rect(0, h - 17 * mm, w, 17 * mm, fill=1, stroke=0)
    canvas.setFillColor(PURPLE)
    canvas.rect(0, h - 17 * mm, 7 * mm, 17 * mm, fill=1, stroke=0)
    canvas.setFillColor(INK)
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(13 * mm, h - 10.5 * mm, "B2Tech Studio - RadioPack France")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(w - 12 * mm, h - 10.5 * mm, "Normandie v0.3.1 - reception seule")
    canvas.setStrokeColor(LINE)
    canvas.line(12 * mm, 12 * mm, w - 12 * mm, 12 * mm)
    canvas.setFillColor(MUTED)
    canvas.drawString(12 * mm, 7 * mm, "Donnees verifiees le 4 aout 2026")
    canvas.drawRightString(w - 12 * mm, 7 * mm, f"Page {doc.page}")
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
        title="RadioPack France - Normandie v0.3.1",
        author="B2Tech Studio",
        subject="Guide du codeplug CHIRP Normandie pour Quansheng UV-K5",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=header_footer)])

    styles = getSampleStyleSheet()
    title = ParagraphStyle("TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold",
                           fontSize=28, leading=32, textColor=INK, spaceAfter=9)
    h1 = ParagraphStyle("H1Custom", parent=styles["Heading1"], fontName="Helvetica-Bold",
                        fontSize=17, leading=21, textColor=PURPLE, spaceBefore=3, spaceAfter=8)
    h2 = ParagraphStyle("H2Custom", parent=styles["Heading2"], fontName="Helvetica-Bold",
                        fontSize=12, leading=15, textColor=BLUE, spaceBefore=4, spaceAfter=6)
    body = ParagraphStyle("BodyCustom", parent=styles["BodyText"], fontName="Helvetica",
                          fontSize=9.2, leading=13, textColor=INK)
    small = ParagraphStyle("SmallCustom", parent=body, fontSize=7.4, leading=9.2, textColor=MUTED)
    callout = ParagraphStyle("Callout", parent=body, backColor=colors.HexColor("#FFF4DF"),
                             borderColor=ORANGE, borderWidth=0.7, borderPadding=7, spaceBefore=7, spaceAfter=9)

    story = [
        Spacer(1, 9 * mm),
        Paragraph("RadioPack France", title),
        Paragraph("Pack Normandie v0.3.1", ParagraphStyle(
            "Subtitle", parent=title, fontSize=19, leading=23, textColor=PURPLE)),
        Spacer(1, 3 * mm),
        Paragraph("Codeplug CHIRP pour Quansheng UV-K5 - 139 memoires - reception seule", h2),
        Spacer(1, 4 * mm),
        Paragraph(
            "Cette version ajoute deux canaux d'appel radioamateur et quinze sorties de relais "
            "ou voies de transpondeurs analogiques verifiees en Normandie. Les plages de memoires "
            "restent separees par categorie pour faciliter la navigation sur le poste.",
            body,
        ),
        Spacer(1, 6 * mm),
    ]

    stats = [
        ["PMR446", "16", "0-15"],
        ["VHF marine", "90", "20-109"],
        ["APRS / ISS", "6", "120-125"],
        ["Aviation", "10", "130-139"],
        ["Appels amateur", "2", "150-151"],
        ["Relais analogiques", "15", "160-174"],
        ["Total", "139", "0-174 avec intervalles"],
    ]
    t = Table([["Categorie", "Memoires", "Positions"]] + stats, colWidths=[75 * mm, 35 * mm, 70 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PURPLE),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTNAME", (0,-1), (-1,-1), "Helvetica-Bold"),
        ("BACKGROUND", (0,-1), (-1,-1), colors.HexColor("#EDE6FF")),
        ("GRID", (0,0), (-1,-1), 0.4, LINE),
        ("ROWBACKGROUNDS", (0,1), (-1,-2), [colors.white, LIGHT]),
        ("FONTSIZE", (0,0), (-1,-1), 9),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    story.extend([
        Paragraph("Organisation des memoires", h1),
        t,
        Spacer(1, 5 * mm),
        Paragraph(
            "<b>Important :</b> toutes les lignes du CSV public utilisent <b>Duplex=off</b>. "
            "Ce guide ne constitue ni une autorisation d'emettre, ni une homologation du UV-K5 "
            "pour les services PMR446, maritime ou aeronautique.",
            callout,
        ),
        PageBreak(),
        Paragraph("Relais analogiques verifies", h1),
        Paragraph(
            "La liste suivante reprend uniquement des sorties de relais ou voies d'ecoute de "
            "transpondeurs analogiques publiees par le REF ou par les associations gestionnaires. "
            "Aucune tonalite d'acces n'est appliquee en reception.",
            body,
        ),
        Spacer(1, 3 * mm),
    ])

    repeater_rows = [row for row in rows if int(row["Location"]) >= 160]
    rep_table = [["Memoire", "Nom", "Frequence", "Mode", "Description"]]
    for row in repeater_rows:
        rep_table.append([
            row["Location"], row["Name"], row["Frequency"], row["Mode"],
            Paragraph(clean(row["Comment"]), small),
        ])
    t2 = Table(rep_table, colWidths=[18*mm, 27*mm, 30*mm, 19*mm, 174*mm], repeatRows=1)
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), BLUE),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID", (0,0), (-1,-1), 0.35, LINE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]),
        ("FONTSIZE", (0,0), (3,-1), 7.4),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]))
    story.extend([t2, PageBreak(), Paragraph("Liste complete des memoires", h1)])

    categories = [
        ("PMR446", 0, 15),
        ("VHF marine", 20, 109),
        ("APRS et ISS", 120, 125),
        ("Aviation Normandie", 130, 139),
        ("Canaux d'appel radioamateur", 150, 151),
        ("Relais analogiques Normandie", 160, 174),
    ]
    for category, start, end in categories:
        group = [row for row in rows if start <= int(row["Location"]) <= end]
        story.append(Paragraph(f"{category} - memoires {start} a {end}", h2))
        table_data = [["Mem.", "Nom", "Frequence MHz", "Mode", "Pas", "Description"]]
        for row in group:
            table_data.append([
                row["Location"], row["Name"], row["Frequency"], row["Mode"], row["TStep"],
                Paragraph(clean(row["Comment"]), small),
            ])
        table = Table(table_data, colWidths=[15*mm, 25*mm, 30*mm, 17*mm, 17*mm, 164*mm], repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#3E4F65")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("GRID", (0,0), (-1,-1), 0.3, LINE),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, LIGHT]),
            ("FONTSIZE", (0,0), (4,-1), 7.1),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("TOPPADDING", (0,0), (-1,-1), 2.5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 2.5),
        ]))
        story.extend([table, Spacer(1, 4*mm)])

    story.extend([
        PageBreak(),
        Paragraph("Sources principales", h1),
        Paragraph("<b>Relais Manche :</b> ARA50, page mise a jour en 2026.", body),
        Paragraph("<b>Relais Calvados et Seine-Maritime :</b> tableau des relais du REF, mise a jour mai 2026.", body),
        Paragraph("<b>Le Havre :</b> SHTSF, page des relais.", body),
        Paragraph("<b>Dieppe et Rouen :</b> radio-club F8KII.", body),
        Paragraph("<b>Plans de bande :</b> Commission THF du REF pour 144-146 MHz et 430-440 MHz.", body),
        Spacer(1, 5*mm),
        Paragraph(
            "Les etats des relais peuvent changer. Une mise a jour de RadioPack France doit "
            "toujours conserver la date de verification et la source de chaque groupe de donnees.",
            callout,
        ),
        Paragraph("Procedure CHIRP", h1),
        Paragraph(
            "1. Lire d'abord la radio avec CHIRP et sauvegarder l'image d'origine. "
            "2. Importer le CSV Normandie v0.3. "
            "3. Verifier les positions et les modes. "
            "4. Ecrire vers la radio. "
            "5. Tester d'abord la reception sans activer l'emission.",
            body,
        ),
    ])

    PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.build(story)
    print(PDF_PATH)

if __name__ == "__main__":
    build()
