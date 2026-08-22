#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tests/test_site_files.py"
text = PATH.read_text(encoding="utf-8")

replacements = {
    '"Sprint 107 / 0.21.95",': '"Sprint 109 / 0.21.97",\n    "## Sprint 109 — Auvergne-Rhône-Alpes v0.3 publiée",\n    "## Sprint 108 — candidat ARA v0.3 figé",',
    '"**Bourgogne-Franche-Comté v0.4** — 61 mémoires RX",\n    "**1582 mémoires RX cumulées**",': '"**Bourgogne-Franche-Comté v0.4** — 61 mémoires RX",\n    "**Auvergne-Rhône-Alpes v0.3** — 71 mémoires RX",\n    "**1591 mémoires RX cumulées**",',
    'for expected in ["Sprint courant : **107**", "État logique : **0.21.95**", "Bourgogne-Franche-Comté v0.4", "Auvergne-Rhône-Alpes v0.3"]:': 'for expected in ["Sprint courant : **109**", "État logique : **0.21.97**", "Bourgogne-Franche-Comté v0.4", "Auvergne-Rhône-Alpes v0.3", "Normandie v0.5"]:',
    'print("Tests RadioPack repository/site: ARA v0.3 / 71 RX promoted on site; canonical state still Sprint 107 pending dedicated sync, historical releases preserved, RX-only guards OK")': 'print("Tests RadioPack repository/site: canonical Sprint 109 / ARA v0.3 71 RX synchronized, historical releases preserved, RX-only guards OK")',
}

for old, new in replacements.items():
    assert old in text, f"Missing expected pre-sync fragment: {old}"
    text = text.replace(old, new, 1)

PATH.write_text(text, encoding="utf-8")
print("Sprint 109 site guard literals synchronized")
