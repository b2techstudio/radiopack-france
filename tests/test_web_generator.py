import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website/src/pages/generateur.astro"
HEADER = ROOT / "website/src/components/Header.astro"
SITEMAP = ROOT / "website/src/pages/sitemap.xml.ts"
OPTIONS = ROOT / "generator/options.json"
LIBRARY = ROOT / "website/src/lib/annecyPack.ts"
STANDARD_ROUTE = ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv.ts"
NO_AIR_ROUTE = ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv.ts"

for path in [PAGE, HEADER, SITEMAP, OPTIONS, LIBRARY, STANDARD_ROUTE, NO_AIR_ROUTE]:
    assert path.is_file(), f"Fichier générateur web manquant: {path.relative_to(ROOT)}"

page = PAGE.read_text(encoding="utf-8")
for expected in [
    'id="annecy-generator"',
    'id="include-aviation"',
    'id="notam-check"',
    'id="notam-confirmed"',
    'id="notam-confirm-zone"',
    'id="memory-count"',
    'id="aviation-summary"',
    'id="notam-summary"',
    'id="notam-warning"',
    'id="download-csv"',
    "65 avec aviation, 48 sans aviation",
    "Contrôle NOTAM avant génération",
    "J'ai vérifié les NOTAM applicables",
    "Générer et télécharger le CSV",
    "Cette option ne modifie jamais",
    "new Blob([csv]",
    "URL.createObjectURL",
]:
    assert expected in page, f"Contrat UI absent: {expected}"

assert 'type="button" disabled' not in page
assert 'aviation.checked ? "65" : "48"' in page
assert 'aviation.checked ? "Incluse · 17" : "Exclue · 0"' in page
assert 'confirmZone.hidden = !notam.checked' in page
assert 'confirmed.disabled = !notam.checked' in page
assert 'if (confirmed && notam && !notam.checked)' in page
assert 'confirmed.checked = false' in page
assert 'notamSummary.textContent = "Confirmé"' in page
assert 'notamSummary.textContent = "Demandé · non confirmé"' in page
assert 'const csv = includeAviation ? fullCsv : noAviationCsv' in page
assert "radiopack-france-annecy-alpes-leman-v0.2.csv" in page
assert "radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv" in page

library = LIBRARY.read_text(encoding="utf-8")
for expected in [
    'data/national/pmr446.json", start: 0',
    'data/national/amateur-listening-rx.json", start: 20',
    'satellites-fm-inventory.json", start: 26',
    'data/national/amateur-calls-rx.json", start: 30',
    'radioamateur-france-inventory.json", start: 40',
    'radioamateur-switzerland-candidates.json", start: 90',
    'aviation-france-airac-08.json", start: 125',
    'aviation-switzerland-airac-08.json", start: 155',
    'channel.verification === "verified_current"',
    'const expected = includeAviation ? 65 : 48',
    '"off"',
    '"0.000000"',
]:
    assert expected in library, f"Règle générateur public absente: {expected}"

for route, include_flag in [(STANDARD_ROUTE, "buildAnnecyCsv(true)"), (NO_AIR_ROUTE, "buildAnnecyCsv(false)")]:
    content = route.read_text(encoding="utf-8")
    assert "export const prerender = true" in content
    assert include_flag in content
    assert '"Content-Type": "text/csv; charset=utf-8"' in content
    assert "Content-Disposition" in content

header = HEADER.read_text(encoding="utf-8")
assert '["/generateur", "Générateur"]' in header
assert 'href="/generateur">Générateur</a>' in header

sitemap = SITEMAP.read_text(encoding="utf-8")
assert '{ path: "/generateur", priority: "0.9", changefreq: "weekly" }' in sitemap

options = json.loads(OPTIONS.read_text(encoding="utf-8"))
implementation = options["implementation"]
ui_contract = options["ui_contract"]
assert options["status"] == "public_generator_wired_v0.2_published"
assert implementation["public_ui_wired"] is True
assert implementation["public_ui_download_locked"] is False
assert implementation["public_download_created"] is True
assert implementation["public_pack_library"] == "website/src/lib/annecyPack.ts"
assert ui_contract["route"] == "/generateur"
assert ui_contract["preview_mode"] is False
assert ui_contract["download_enabled"] is True
assert options["options"]["include_aviation"]["annecy_memory_count_when_enabled"] == 65
assert options["options"]["include_aviation"]["annecy_memory_count_when_disabled"] == 48
assert options["options"]["notam_check"]["blocks_generation"] is False
assert options["options"]["notam_check"]["affects_csv_content"] is False

print("Tests RadioPack Sprint 21 published web generator: OK")
