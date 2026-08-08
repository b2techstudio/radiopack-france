import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website/src/pages/generateur.astro"
HEADER = ROOT / "website/src/components/Header.astro"
SITEMAP = ROOT / "website/src/pages/sitemap.xml.ts"
OPTIONS = ROOT / "generator/options.json"
PUBLIC_CSV = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv"

for path in [PAGE, HEADER, SITEMAP, OPTIONS]:
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
    "65 avec aviation, 48 sans aviation",
    "Contrôle NOTAM avant génération",
    "J'ai vérifié les NOTAM applicables",
    "Génération CSV Annecy bientôt disponible",
    "Cette option ne modifie jamais",
    'type="button" disabled',
]:
    assert expected in page, f"Contrat UI absent: {expected}"

assert 'aviation.checked ? "65" : "48"' in page
assert 'aviation.checked ? "Incluse · 17" : "Exclue · 0"' in page
assert 'confirmZone.hidden = !notam.checked' in page
assert 'confirmed.disabled = !notam.checked' in page
assert 'const renderSummary = () =>' in page
assert 'notam?.addEventListener("change", () =>' in page
assert 'if (confirmed && notam && !notam.checked)' in page
assert 'confirmed.checked = false' in page
assert 'confirmed?.addEventListener("change", renderSummary)' in page
assert '.notam-confirm[hidden] { display: none; }' in page
assert 'class="notam-confirm-check"' in page
assert 'notamSummary.textContent = "Confirmé"' in page
assert 'notamSummary.textContent = "Demandé · non confirmé"' in page
assert "radiopack-france-annecy-alpes-leman-v0.2.csv" not in page

header = HEADER.read_text(encoding="utf-8")
assert '["/generateur", "Générateur"]' in header
assert 'href="/generateur">Générateur</a>' in header

sitemap = SITEMAP.read_text(encoding="utf-8")
assert '{ path: "/generateur", priority: "0.9", changefreq: "weekly" }' in sitemap

options = json.loads(OPTIONS.read_text(encoding="utf-8"))
implementation = options["implementation"]
ui_contract = options["ui_contract"]
assert options["status"] == "backend_wired_prepublication_not_public_ui"
assert implementation["public_ui_wired"] is False
assert implementation["public_ui_preview_wired"] is True
assert implementation["public_ui_preview_route"] == "/generateur"
assert implementation["public_ui_download_locked"] is True
assert implementation["public_download_created"] is False
assert ui_contract["route"] == "/generateur"
assert ui_contract["preview_mode"] is True
assert ui_contract["download_enabled"] is False
assert options["options"]["include_aviation"]["annecy_memory_count_when_enabled"] == 65
assert options["options"]["include_aviation"]["annecy_memory_count_when_disabled"] == 48
assert options["options"]["notam_check"]["blocks_generation"] is False
assert options["options"]["notam_check"]["affects_csv_content"] is False

assert not PUBLIC_CSV.exists(), "Le générateur web ne doit pas publier le CSV Annecy v0.2"

print("Tests RadioPack Sprint 20 web generator preview + NOTAM confirmation interaction: OK")
