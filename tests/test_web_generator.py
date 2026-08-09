import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website/src/pages/generateur.astro"
HEADER = ROOT / "website/src/components/Header.astro"
SITEMAP = ROOT / "website/src/pages/sitemap.xml.ts"
OPTIONS = ROOT / "generator/options.json"
GENERIC_LIBRARY = ROOT / "website/src/lib/chirpPack.ts"
ANNECY_LIBRARY = ROOT / "website/src/lib/annecyPack.ts"
STANDARD_ROUTE = ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv.ts"
NO_AIR_ROUTE = ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv.ts"

for path in [PAGE, HEADER, SITEMAP, OPTIONS, GENERIC_LIBRARY, ANNECY_LIBRARY, STANDARD_ROUTE, NO_AIR_ROUTE]:
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
    'id="file-summary"',
    'id="download-csv"',
    "65 avec aviation, 48 sans aviation",
    "Contrôle NOTAM avant génération",
    "J'ai vérifié les NOTAM applicables",
    "Télécharger le CSV · 65 mémoires",
    "SOFIA-Briefing · France",
    "Skybriefing · Suisse",
    "https://sofia-briefing.aviation-civile.gouv.fr/sofia/pages/notamform.html",
    "https://www.skybriefing.com/fr/services/notam-briefing",
]:
    assert expected in page, f"Contrat UI absent: {expected}"

assert 'type="button" disabled' not in page
assert "new Blob" not in page
assert "URL.createObjectURL" not in page
assert "fullCsv" not in page
assert "noAviationCsv" not in page
assert "downloadLink.href = downloadUrl" in page
assert 'downloadLink.setAttribute("download", filename)' in page
assert "Télécharger le CSV · ${memoryTotal} mémoires" in page
assert 'const memoryTotal = includeAviation ? 65 : 48' in page
assert 'aviationSummary.textContent = includeAviation ? "Incluse · 17" : "Exclue · 0"' in page
assert 'confirmZone.hidden = !notam.checked' in page
assert 'confirmed.disabled = !notam.checked' in page
assert 'if (confirmed && notam && !notam.checked)' in page
assert 'confirmed.checked = false' in page
assert 'notamSummary.textContent = "Confirmé"' in page
assert 'notamSummary.textContent = "Demandé · non confirmé"' in page
assert "radiopack-france-annecy-alpes-leman-v0.2.csv" in page
assert "radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv" in page

generic = GENERIC_LIBRARY.read_text(encoding="utf-8")
for expected in [
    "export type PackSource",
    "export const assemblePack",
    "export const validatePlacedChannels",
    "export const buildChirpCsv",
    "verificationAllowList",
    "Pack trop grand",
    "Nom trop long",
    "Location dupliquée",
    '"off"',
    '"0.000000"',
]:
    assert expected in generic, f"Règle générique CHIRP absente: {expected}"

annecy = ANNECY_LIBRARY.read_text(encoding="utf-8")
for expected in [
    'data/national/pmr446.json", start: 0',
    'data/national/amateur-listening-rx.json", start: 20',
    'satellites-fm-inventory.json", start: 26',
    'data/national/amateur-calls-rx.json", start: 30',
    'radioamateur-france-inventory.json", start: 40',
    "radioamateur-switzerland-candidates.json",
    'verificationAllowList: ["verified_current"]',
    "aviation-france-airac-08.json",
    "aviation-switzerland-airac-08.json",
    'group: "aviation"',
    "const expected = includeAviation ? 65 : 48",
    "assemblePack(SOURCES, disabledGroups)",
    "buildChirpCsv(getAnnecyPack(includeAviation))",
]:
    assert expected in annecy, f"Configuration Annecy absente: {expected}"

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
assert implementation["generic_pack_library"] == "website/src/lib/chirpPack.ts"
assert implementation["public_pack_library"] == "website/src/lib/annecyPack.ts"
assert implementation["public_ui_wired"] is True
assert implementation["public_ui_download_locked"] is False
assert implementation["public_download_created"] is True
assert ui_contract["route"] == "/generateur"
assert ui_contract["preview_mode"] is False
assert ui_contract["download_enabled"] is True
assert ui_contract["download_strategy"] == "direct_prerendered_route"
assert "selected_filename" in ui_contract["summary_fields"]
assert options["services"]["FR"]["url"].startswith("https://sofia-briefing.")
assert options["services"]["CH"]["url"] == "https://www.skybriefing.com/fr/services/notam-briefing"
assert options["options"]["include_aviation"]["annecy_memory_count_when_enabled"] == 65
assert options["options"]["include_aviation"]["annecy_memory_count_when_disabled"] == 48
assert options["options"]["notam_check"]["blocks_generation"] is False
assert options["options"]["notam_check"]["affects_csv_content"] is False

print("Tests RadioPack Sprint 22 direct-download generator + reusable pack builder: OK")
