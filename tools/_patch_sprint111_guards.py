#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tests/test_site_files.py"
text = PATH.read_text(encoding="utf-8")

old = '    "research/sprint-109-summary.md", "research/sprint-110-summary.md",\n]'
new = '    "research/sprint-109-summary.md", "research/sprint-110-summary.md", "research/sprint-111-summary.md",\n    "research/bretagne-v0.3/airac09-readiness.json",\n    "research/bretagne-v0.3/airac09-revalidation-template.json",\n    "tools/check_bretagne_v03_airac09_revalidation.py",\n    "tests/test_sprint111_bretagne_airac09_readiness.py",\n]'
assert old in text
text = text.replace(old, new, 1)

old = '    "Sprint 110 / 0.21.98",\n    "## Sprint 110 — Normandie v0.5 : sources revalidées, handoff terrain",'
new = '    "Sprint 111 / 0.21.99",\n    "## Sprint 111 — Bretagne v0.3 : readiness AIRAC 09/26",\n    "## Sprint 110 — Normandie v0.5 : sources revalidées, handoff terrain",'
assert old in text
text = text.replace(old, new, 1)

old = 'for expected in ["Sprint courant : **110**", "État logique : **0.21.98**", "Bourgogne-Franche-Comté v0.4", "Auvergne-Rhône-Alpes v0.3", "Normandie v0.5"]:'
new = 'for expected in ["Sprint courant : **111**", "État logique : **0.21.99**", "Bourgogne-Franche-Comté v0.4", "Auvergne-Rhône-Alpes v0.3", "Normandie v0.5", "Bretagne v0.3 AIRAC 09/26"]:'
assert old in text
text = text.replace(old, new, 1)

old = 'print("Tests RadioPack repository/site: canonical Sprint 110 / Normandie v0.5 zero-delta field handoff synchronized, public releases preserved, RX-only guards OK")'
new = 'print("Tests RadioPack repository/site: canonical Sprint 111 / Bretagne AIRAC readiness synchronized, Normandie field priority and public releases preserved, RX-only guards OK")'
assert old in text
text = text.replace(old, new, 1)

PATH.write_text(text, encoding="utf-8")
print("Sprint 111 site guard patched")
