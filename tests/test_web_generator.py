import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "website/src/pages/generateur.astro"
HEADER = ROOT / "website/src/components/Header.astro"
SITEMAP = ROOT / "website/src/pages/sitemap.xml.ts"
OPTIONS = ROOT / "generator/options.json"
GENERIC_LIBRARY = ROOT / "website/src/lib/chirpPack.ts"
ANNECY_LIBRARY = ROOT / "website/src/lib/annecyPack.ts"
PACK_REGISTRY = ROOT / "website/src/lib/packRegistry.ts"
PACK_SHORTCUT_SCRIPT = ROOT / "website/src/scripts/generator-pack-shortcuts.js"
STANDARD_ROUTE = ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv.ts"
NO_AIR_ROUTE = ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv.ts"
NORMANDIE = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv"
BRETAGNE = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"

for path in [
    PAGE,
    HEADER,
    SITEMAP,
    OPTIONS,
    GENERIC_LIBRARY,
    ANNECY_LIBRARY,
    PACK_REGISTRY,
    PACK_SHORTCUT_SCRIPT,
    STANDARD_ROUTE,
    NO_AIR_ROUTE,
    NORMANDIE,
    BRETAGNE,
]:
    assert path.is_file(), f"Fichier générateur web manquant: {path.relative_to(ROOT)}"

page = PAGE.read_text(encoding="utf-8")
for expected in [
    'id="radiopack-generator"',
    'id="pack-select"',
    'id="pack-badge"',
    'id="pack-status"',
    'id="pack-description"',
    'id="aviation-fieldset"',
    'id="include-aviation"',
    'id="notam-fieldset"',
    'id="notam-check"',
    'id="notam-confirmed"',
    'id="notam-confirm-zone"',
    'id="memory-count"',
    'id="pack-summary"',
    'id="aviation-summary"',
    'id="notam-summary"',
    'id="notam-warning"',
    'id="file-summary"',
    'id="download-csv"',
    "Générateur web · multi-régions",
    "Que signifient ces nombres ?",
    "nombre de mémoires présentes dans le CSV publié",
    "77 mémoires",
    "60 sans aviation",
    "142 mémoires",
    "151 mémoires",
    'data-pack-shortcut="annecy-alpes-leman"',
    'data-pack-shortcut="normandie"',
    'data-pack-shortcut="bretagne"',
    "Sélectionner ce pack ↑",
    'src="../scripts/generator-pack-shortcuts.js"',
    "Contrôle NOTAM avant génération",
    "J'ai vérifié les NOTAM applicables",
    "SOFIA-Briefing · France",
    "Skybriefing · Suisse",
]:
    assert expected in page, f"Contrat UI absent: {expected}"

for expected in [
    "publicPacks.find((pack) => pack.id === selectedId)",
    "pack.aviationToggle.includedVariant",
    "pack.aviationToggle.excludedVariant",
    "aviationFieldset.hidden = !aviationSupported",
    "notamFieldset.hidden = !pack.notamCheck",
    "downloadLink.href = variant.downloadUrl",
    'downloadLink.setAttribute("download", variant.filename)',
    "Télécharger le CSV · ${variant.memoryCount} mémoires",
    'variant.aviationIncluded ? "Incluse · variante fixe" : "Configuration fixe"',
    'notamSummary.textContent = "Non proposé"',
    'notamSummary.textContent = "Confirmé"',
    'notamSummary.textContent = "Demandé · non confirmé"',
]:
    assert expected in page, f"Logique générateur absente: {expected}"

shortcut_script = PACK_SHORTCUT_SCRIPT.read_text(encoding="utf-8")
for expected in [
    'document.querySelectorAll("[data-pack-shortcut]")',
    "shortcut.dataset.packShortcut",
    "packSelect.value = packId",
    'packSelect.dispatchEvent(new Event("change", { bubbles: true }))',
    'generatorForm.scrollIntoView({ behavior: "smooth", block: "start" })',
    'event.key !== "Enter" && event.key !== " "',
]:
    assert expected in shortcut_script, f"Raccourci pack absent: {expected}"

assert "new Blob" not in page
assert "URL.createObjectURL" not in page
assert "fullCsv" not in page
assert "noAviationCsv" not in page

registry = PACK_REGISTRY.read_text(encoding="utf-8")
for expected in [
    "export type PublicPackVariant",
    "export type PublicPack",
    "export const publicPacks",
    'id: "annecy-alpes-leman"',
    'id: "normandie"',
    'id: "bretagne"',
    'memoryCount: 77',
    'memoryCount: 60',
    'memoryCount: 142',
    'memoryCount: 151',
    '/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.4.csv',
    '/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.4-sans-aviation.csv',
    '/downloads/normandie/radiopack-france-normandie-v0.4.csv',
    '/downloads/bretagne/radiopack-france-bretagne-v0.2.csv',
    'export const defaultPublicPackId = "annecy-alpes-leman"',
]:
    assert expected in registry, f"Registre public incomplet: {expected}"

assert registry.count('downloadUrl: "') == 4
assert "annecy-haute-savoie-v0.1" not in registry

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
assert options["schema_version"] == "3.0"
assert options["status"] == "multi_region_public_generator"
assert implementation["generic_pack_library"] == "website/src/lib/chirpPack.ts"
assert implementation["annecy_pack_library"] == "website/src/lib/annecyPack.ts"
assert implementation["public_pack_registry"] == "website/src/lib/packRegistry.ts"
assert implementation["published_pack_count"] == 3
assert implementation["default_pack"] == "annecy-alpes-leman"
assert implementation["public_ui_wired"] is True
assert implementation["public_ui_download_locked"] is False
assert ui_contract["route"] == "/generateur"
assert ui_contract["pack_selector"] is True
assert ui_contract["download_enabled"] is True
assert ui_contract["download_strategy"] == "direct_validated_route"
assert ui_contract["unsupported_options_hidden"] is True
assert options["pack_selection"]["enabled"] is True
assert {pack["id"] for pack in options["pack_selection"]["packs"]} == {"annecy-alpes-leman", "normandie", "bretagne"}
assert next(pack for pack in options["pack_selection"]["packs"] if pack["id"] == "bretagne")["default_memory_count"] == 151
assert next(pack for pack in options["pack_selection"]["packs"] if pack["id"] == "bretagne")["aviation_included"] is True
assert options["options"]["include_aviation"]["scope"] == ["annecy-alpes-leman"]
assert options["options"]["notam_check"]["scope"] == ["annecy-alpes-leman"]
assert options["options"]["notam_check"]["blocks_generation"] is False
assert options["options"]["notam_check"]["affects_csv_content"] is False

print("Tests RadioPack Sprint 23 multi-region public generator: explicit memory counts and selectable pack shortcuts OK")
