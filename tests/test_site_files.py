import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required_files = [
    "README.md",
    ".gitignore",
    ".github/workflows/ci.yml",
    "SPRINT-19-PREPUBLICATION-REVIEW.md",
    "SPRINT-20-WEB-GENERATOR.md",
    "SPRINT-21-PUBLICATION-V0.2.md",
    "generator/options.json",
    "generator/generate_chirp_csv.py",
    "tests/test_web_generator.py",
    "research/annecy-alpes-leman-v0.2/prepublication-plan.json",
    "research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json",
    "website/src/lib/annecyPack.ts",
    "website/src/pages/generateur.astro",
    "website/src/pages/telechargements.astro",
    "website/src/pages/versions.astro",
    "website/src/pages/index.astro",
    "website/src/pages/regions/annecy-haute-savoie.astro",
    "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv.ts",
    "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv.ts",
    "website/src/pages/sitemap.xml.ts",
    "website/public/_headers",
]
for relative in required_files:
    path = ROOT / relative
    assert path.is_file(), f"Fichier manquant: {relative}"
    assert path.stat().st_size > 20, f"Fichier vide ou incomplet: {relative}"

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for expected in [
    "État actuel — Sprint 21",
    "Annecy–Alpes–Léman v0.2** — 65 mémoires RX",
    "published_v0.2",
    "65/65 mémoires",
    "48 mémoires sans aviation",
    "Le contrôle NOTAM est **informatif et non bloquant**",
    "website/src/lib/annecyPack.ts",
    "/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv",
    "Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint",
]:
    assert expected in readme, f"README non actualisé: {expected}"

gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
assert "research/annecy-alpes-leman-v0.2/generated/" in gitignore
assert "__pycache__/" in gitignore
assert "*.py[cod]" in gitignore

options = json.loads((ROOT / "generator/options.json").read_text(encoding="utf-8"))
assert options["status"] == "public_generator_wired_v0.2_published"
implementation = options["implementation"]
assert implementation["public_ui_wired"] is True
assert implementation["public_ui_download_locked"] is False
assert implementation["public_download_created"] is True
assert implementation["public_pack_library"] == "website/src/lib/annecyPack.ts"
assert options["ui_contract"]["download_enabled"] is True
assert options["options"]["include_aviation"]["annecy_memory_count_when_enabled"] == 65
assert options["options"]["include_aviation"]["annecy_memory_count_when_disabled"] == 48
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
annecy = next(region for region in regions if region["slug"] == "annecy-haute-savoie")
assert annecy["name"] == "Annecy–Alpes–Léman"
assert annecy["status"] == "v0.2 disponible"
assert annecy["available"] is True
assert annecy["memoryCount"] == 65

library = (ROOT / "website/src/lib/annecyPack.ts").read_text(encoding="utf-8")
assert "const expected = includeAviation ? 65 : 48" in library
assert 'channel.verification === "verified_current"' in library
assert '"off"' in library
assert '"0.000000"' in library

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

public_pages = [
    ROOT / "website/src/pages/index.astro",
    ROOT / "website/src/pages/generateur.astro",
    ROOT / "website/src/pages/telechargements.astro",
    ROOT / "website/src/pages/versions.astro",
    ROOT / "website/src/pages/regions/annecy-haute-savoie.astro",
]
for path in public_pages:
    content = path.read_text(encoding="utf-8")
    assert "/downloads/annecy-haute-savoie/radiopack-france-annecy-haute-savoie-v0.1" not in content, f"Lien v0.1 public: {path.name}"
    assert "annecy-alpes-leman-v0.2-internal" not in content, f"Candidat interne exposé: {path.name}"

historical_generator = (ROOT / "generator/generate_chirp_csv.py").read_text(encoding="utf-8")
assert "radiopack-france-annecy-haute-savoie-v0.1.csv" not in historical_generator
assert "data/regions/annecy-haute-savoie/pack.json" not in historical_generator

headers = (ROOT / "website/public/_headers").read_text(encoding="utf-8")
for expected in ["X-Frame-Options: DENY", "X-Content-Type-Options: nosniff", "Referrer-Policy: strict-origin-when-cross-origin"]:
    assert expected in headers

workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
for expected in [
    "python tests/test_generator.py",
    "python tests/test_site_files.py",
    "python tests/test_annecy_prepublication_review.py",
    "python tests/test_web_generator.py",
    "npm run build",
    "radiopack-ci/complete",
]:
    assert expected in workflow, f"Étape CI absente: {expected}"

print("Tests RadioPack Sprint 21 publication v0.2: OK")
