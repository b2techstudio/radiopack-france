import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required_files = [
    "README.md",
    ".gitignore",
    ".github/workflows/ci.yml",
    "REGIONAL-PACK-WORKFLOW.md",
    "SPRINT-21-PUBLICATION-V0.2.md",
    "SPRINT-22-POST-PUBLICATION.md",
    "SPRINT-23-MULTI-REGION-GENERATOR.md",
    "SPRINT-24-ISOLATED-GENERATOR-TESTS.md",
    "generator/options.json",
    "generator/generate_chirp_csv.py",
    "tests/test_generator.py",
    "tests/test_web_generator.py",
    "tests/test_pack_registry.py",
    "tests/test_built_public_pack_catalog.py",
    "research/annecy-alpes-leman-v0.2/prepublication-plan.json",
    "research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json",
    "website/src/lib/chirpPack.ts",
    "website/src/lib/annecyPack.ts",
    "website/src/lib/packRegistry.ts",
    "website/src/pages/generateur.astro",
    "website/src/pages/telechargements.astro",
    "website/src/pages/versions.astro",
    "website/src/pages/index.astro",
    "website/src/pages/regions/annecy-haute-savoie.astro",
    "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv.ts",
    "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv.ts",
    "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv",
    "website/src/pages/sitemap.xml.ts",
    "website/public/_headers",
    "website/public/_redirects",
]
for relative in required_files:
    path = ROOT / relative
    assert path.is_file(), f"Fichier manquant: {relative}"
    assert path.stat().st_size > 20, f"Fichier vide ou incomplet: {relative}"

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for expected in [
    "État actuel — Sprint 24",
    "Normandie v0.3.1** — 139 mémoires RX",
    "Annecy–Alpes–Léman v0.2** — 65 mémoires RX",
    "48 mémoires sans aviation",
    "générateur public multi-régions",
    "website/src/lib/packRegistry.ts",
    "website/src/lib/chirpPack.ts",
    "website/src/lib/annecyPack.ts",
    "Tests de génération isolés — Sprint 24",
    "--output-root <dossier>",
    "les tests du générateur n'écrivent plus dans les CSV suivis par Git",
    "nothing to commit, working tree clean",
    "SPRINT-24-ISOLATED-GENERATOR-TESTS.md",
    "Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint",
]:
    assert expected in readme, f"README non actualisé: {expected}"

gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
assert "research/annecy-alpes-leman-v0.2/generated/" in gitignore
assert "__pycache__/" in gitignore
assert "*.py[cod]" in gitignore

options = json.loads((ROOT / "generator/options.json").read_text(encoding="utf-8"))
assert options["schema_version"] == "3.0"
assert options["status"] == "multi_region_public_generator"
implementation = options["implementation"]
assert implementation["generic_pack_library"] == "website/src/lib/chirpPack.ts"
assert implementation["annecy_pack_library"] == "website/src/lib/annecyPack.ts"
assert implementation["public_pack_registry"] == "website/src/lib/packRegistry.ts"
assert implementation["published_pack_count"] == 2
assert implementation["default_pack"] == "annecy-alpes-leman"
assert implementation["public_ui_wired"] is True
assert implementation["public_ui_download_locked"] is False
assert options["ui_contract"]["pack_selector"] is True
assert options["ui_contract"]["download_enabled"] is True
assert options["ui_contract"]["download_strategy"] == "direct_validated_route"
assert options["ui_contract"]["unsupported_options_hidden"] is True
assert {pack["id"] for pack in options["pack_selection"]["packs"]} == {"annecy-alpes-leman", "normandie"}
assert options["options"]["include_aviation"]["scope"] == ["annecy-alpes-leman"]
assert options["options"]["notam_check"]["scope"] == ["annecy-alpes-leman"]
assert options["options"]["notam_check"]["affects_csv_content"] is False
assert options["options"]["notam_check"]["blocks_generation"] is False

plan = json.loads((ROOT / "research/annecy-alpes-leman-v0.2/prepublication-plan.json").read_text(encoding="utf-8"))
assert plan["status"] == "published_v0.2"
assert plan["public_file_created"] is True
assert plan["public_export_allowed"] is True
assert plan["publication_completed"] is True
assert plan["candidate_memory_count"] == 65
assert plan["candidate_memory_count_without_aviation"] == 48
assert plan["blocking_gates"] == []
assert set(plan["advisory_checks"]) == {"notam_fr", "notam_ch"}

review = json.loads((ROOT / "research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json").read_text(encoding="utf-8"))
assert review["expected_memory_count"] == 65
assert review["expected_memory_count_without_aviation"] == 48
assert len(review["rows"]) == 65

regions = json.loads((ROOT / "website/src/data/regions.json").read_text(encoding="utf-8"))
assert len(regions) == 2
annecy = next(region for region in regions if region["slug"] == "annecy-haute-savoie")
normandie = next(region for region in regions if region["slug"] == "normandie")
assert annecy["name"] == "Annecy–Alpes–Léman"
assert annecy["available"] is True
assert annecy["memoryCount"] == 65
assert normandie["name"] == "Normandie"
assert normandie["available"] is True
assert normandie["memoryCount"] == 139

generic_library = (ROOT / "website/src/lib/chirpPack.ts").read_text(encoding="utf-8")
for expected in [
    "export type PackSource",
    "export const assemblePack",
    "export const validatePlacedChannels",
    "export const buildChirpCsv",
    "verificationAllowList",
    '"off"',
    '"0.000000"',
]:
    assert expected in generic_library, f"Moteur générique incomplet: {expected}"

annecy_library = (ROOT / "website/src/lib/annecyPack.ts").read_text(encoding="utf-8")
assert "assemblePack(SOURCES, disabledGroups)" in annecy_library
assert "buildChirpCsv(getAnnecyPack(includeAviation))" in annecy_library
assert 'verificationAllowList: ["verified_current"]' in annecy_library
assert 'group: "aviation"' in annecy_library
assert "const expected = includeAviation ? 65 : 48" in annecy_library

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
for expected in [
    'id: "annecy-alpes-leman"',
    'id: "normandie"',
    'memoryCount: 65',
    'memoryCount: 48',
    'memoryCount: 139',
    '/downloads/normandie/radiopack-france-normandie-v0.3.1.csv',
    'export const defaultPublicPackId = "annecy-alpes-leman"',
]:
    assert expected in registry, f"Registre public incomplet: {expected}"
assert registry.count('downloadUrl: "') == 3
assert "annecy-haute-savoie-v0.1" not in registry

generator_source = (ROOT / "generator/generate_chirp_csv.py").read_text(encoding="utf-8")
for expected in [
    '"--output-root"',
    "output_root = args.output_root.resolve() if args.output_root is not None else root",
    "output = output_root / output_relative",
    "sortie isolée",
]:
    assert expected in generator_source, f"Isolation générateur absente: {expected}"

generator_test = (ROOT / "tests/test_generator.py").read_text(encoding="utf-8")
for expected in [
    "tempfile.TemporaryDirectory",
    '"--output-root"',
    "published_before",
    "generated_rows == published_rows",
    "read_bytes() == original_bytes",
    "Tests RadioPack isolated generator + ISS links: OK",
]:
    assert expected in generator_test, f"Garde-fou test isolé absent: {expected}"

standard_route = (ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv.ts").read_text(encoding="utf-8")
no_air_route = (ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv.ts").read_text(encoding="utf-8")
assert "buildAnnecyCsv(true)" in standard_route
assert "buildAnnecyCsv(false)" in no_air_route
assert "export const prerender = true" in standard_route
assert "export const prerender = true" in no_air_route

home = (ROOT / "website/src/pages/index.astro").read_text(encoding="utf-8")
assert "2</strong><span>packs régionaux disponibles" in home
assert "Annecy–Alpes–Léman v0.2" in home

downloads = (ROOT / "website/src/pages/telechargements.astro").read_text(encoding="utf-8")
assert "Deux packs régionaux sont disponibles" in downloads
assert "CSV Annecy v0.2" in downloads
assert "/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv" in downloads

versions = (ROOT / "website/src/pages/versions.astro").read_text(encoding="utf-8")
assert 'name: "Annecy–Alpes–Léman"' in versions
assert 'status: "Disponible"' in versions
assert "memories: 65" in versions

annecy_page = (ROOT / "website/src/pages/regions/annecy-haute-savoie.astro").read_text(encoding="utf-8")
assert "Disponible — v0.2" in annecy_page
assert "65 mémoires avec aviation · 48 sans aviation" in annecy_page
assert "F1ZJV" in annecy_page
assert "Duplex=off" in annecy_page

generator_page = (ROOT / "website/src/pages/generateur.astro").read_text(encoding="utf-8")
for expected in [
    'id="pack-select"',
    "Générateur web · multi-régions",
    "Normandie · 139",
    "Annecy · 65 / 48",
    "downloadLink.href = variant.downloadUrl",
    "aviationFieldset.hidden = !aviationSupported",
    "notamFieldset.hidden = !pack.notamCheck",
]:
    assert expected in generator_page, f"Générateur multi-régions incomplet: {expected}"
assert "new Blob" not in generator_page
assert "URL.createObjectURL" not in generator_page

legacy_paths = [
    "data/regions/annecy-haute-savoie/pack.json",
    "data/regions/annecy-haute-savoie/aviation-rx.json",
    "data/regions/annecy-haute-savoie/repeaters-analog-rx.json",
    "website/public/downloads/annecy-haute-savoie/radiopack-france-annecy-haute-savoie-v0.1.csv",
    "website/public/downloads/annecy-haute-savoie/radiopack-france-annecy-haute-savoie-repeaters-rx.csv",
    "website/public/downloads/annecy-haute-savoie/radiopack-france-annecy-haute-savoie-v0.1-guide.pdf",
]
for relative in legacy_paths:
    assert not (ROOT / relative).exists(), f"Fichier Annecy v0.1 encore actif: {relative}"

redirects = (ROOT / "website/public/_redirects").read_text(encoding="utf-8")
assert "radiopack-france-annecy-haute-savoie-v0.1.csv /downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv 301" in redirects

workflow_doc = (ROOT / "REGIONAL-PACK-WORKFLOW.md").read_text(encoding="utf-8")
for expected in ["chirpPack.ts", "<pack>Pack.ts", "packRegistry.ts", "carte de revue", "routes Astro prérendues", "README.md"]:
    assert expected in workflow_doc, f"Workflow régional incomplet: {expected}"

workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
for expected in [
    "Test CSV generator in isolated output",
    "python tests/test_generator.py",
    "python tests/test_site_files.py",
    "python tests/test_pack_registry.py",
    "python tests/test_web_generator.py",
    "python tests/test_built_annecy_public_csv.py",
    "python tests/test_built_public_pack_catalog.py",
    "npm run build",
    "radiopack-ci/complete",
]:
    assert expected in workflow, f"Étape CI absente: {expected}"

print("Tests RadioPack Sprint 24 isolated generator + multi-region architecture: OK")
