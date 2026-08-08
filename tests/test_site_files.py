import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required_files = [
    "README.md",
    ".gitignore",
    ".github/workflows/ci.yml",
    "SPRINT-13-CHAMBERY-VALIDATION.md",
    "SPRINT-15-NOTAM-GENERATOR-OPTIONS.md",
    "SPRINT-16-PREPUBLICATION-READINESS.md",
    "SPRINT-17-SATELLITE-RECHECK.md",
    "SPRINT-18-PREPUBLICATION-GENERATOR.md",
    "generator/options.json",
    "tests/test_annecy_research.py",
    "tests/test_annecy_aviation_lakes.py",
    "tests/test_annecy_airac08.py",
    "tests/test_annecy_internal_candidate.py",
    "tests/test_annecy_release_readiness.py",
    "tests/test_annecy_prepublication.py",
    "research/annecy-alpes-leman-v0.2/radioamateur-france-inventory.json",
    "research/annecy-alpes-leman-v0.2/radioamateur-switzerland-candidates.json",
    "research/annecy-alpes-leman-v0.2/aviation-france-pre-airac-08.json",
    "research/annecy-alpes-leman-v0.2/aviation-france-airac-08.json",
    "research/annecy-alpes-leman-v0.2/aviation-switzerland-airac-08.json",
    "research/annecy-alpes-leman-v0.2/aviation-operational-gates.json",
    "research/annecy-alpes-leman-v0.2/navigation-lakes-findings.json",
    "research/annecy-alpes-leman-v0.2/satellites-fm-inventory.json",
    "research/annecy-alpes-leman-v0.2/memory-plan.json",
    "research/annecy-alpes-leman-v0.2/prepublication-plan.json",
    "tools/build_annecy_internal_candidate.py",
    "tools/build_annecy_prepublication.py",
    "tools/check_annecy_release_readiness.py",
    "research/annecy-alpes-leman-v0.2/source-register.csv",
    "research/annecy-alpes-leman-v0.2/conflicts.csv",
    "website/astro.config.mjs",
    "website/src/layouts/BaseLayout.astro",
    "website/src/components/Header.astro",
    "website/src/components/Footer.astro",
    "website/src/components/RegionCard.astro",
    "website/src/data/regions.json",
    "website/src/pages/index.astro",
    "website/src/pages/404.astro",
    "website/src/pages/telechargements.astro",
    "website/src/pages/versions.astro",
    "website/src/pages/regions/annecy-haute-savoie.astro",
    "website/src/pages/robots.txt.ts",
    "website/src/pages/sitemap.xml.ts",
    "website/public/site.webmanifest",
    "website/public/_headers",
    "website/public/_redirects",
]

for relative in required_files:
    path = ROOT / relative
    assert path.is_file(), f"Fichier manquant: {relative}"
    assert path.stat().st_size > 20, f"Fichier vide ou incomplet: {relative}"

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for expected in [
    "État actuel — Sprint 18",
    "65 mémoires avec aviation",
    "48 mémoires sans aviation",
    "Contrôle NOTAM France/Suisse : **facultatif et non bloquant**",
    "build_annecy_prepublication.py",
    "prépublication reste hors de `website/public`",
    "## Maintenance du projet",
    "Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint",
]:
    assert expected in readme, f"README non actualisé: {expected}"

gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
assert "research/annecy-alpes-leman-v0.2/generated/" in gitignore
assert "__pycache__/" in gitignore
assert "*.py[cod]" in gitignore

options = json.loads((ROOT / "generator/options.json").read_text(encoding="utf-8"))
assert options["status"] == "backend_wired_prepublication_not_public_ui"
assert options["implementation"]["annecy_prepublication_builder"] == "tools/build_annecy_prepublication.py"
assert options["implementation"]["public_ui_wired"] is False
assert options["implementation"]["public_download_created"] is False
assert options["options"]["include_aviation"]["affects_csv_content"] is True
assert options["options"]["include_aviation"]["annecy_memory_count_when_enabled"] == 65
assert options["options"]["include_aviation"]["annecy_memory_count_when_disabled"] == 48
assert options["options"]["notam_check"]["affects_csv_content"] is False
assert options["options"]["notam_check"]["blocks_generation"] is False

prepublication = json.loads(
    (ROOT / "research/annecy-alpes-leman-v0.2/prepublication-plan.json").read_text(encoding="utf-8")
)
assert prepublication["status"] == "prepublication_generator_ready_not_public"
assert prepublication["candidate_memory_count"] == 65
assert prepublication["candidate_memory_count_without_aviation"] == 48
assert prepublication["prepublication_generation_allowed"] is True
assert prepublication["public_file_created"] is False
assert prepublication["public_export_allowed"] is False
assert prepublication["review_required_before_public_export"] is True
assert prepublication["blocking_gates"] == []
assert set(prepublication["passed_blocking_gates"]) == {
    "airac_fr", "airac_ch", "pending_airfields", "dynamic_satellites"
}
assert set(prepublication["advisory_checks"]) == {"notam_fr", "notam_ch"}
assert not (ROOT / prepublication["reserved_public_output"]).exists()

satellites = json.loads(
    (ROOT / "research/annecy-alpes-leman-v0.2/satellites-fm-inventory.json").read_text(encoding="utf-8")
)
assert satellites["release_recheck"]["status"] == "passed_official_amsat_recheck"
assert satellites["release_recheck"]["checked"] == "2026-08-08"
assert satellites["release_recheck"]["ao91_limit_confirmed"] == "sunlight_only_due_to_battery"

astro_config = (ROOT / "website/astro.config.mjs").read_text(encoding="utf-8")
assert 'site: "https://radiopack.b2tech.studio"' in astro_config

layout = (ROOT / "website/src/layouts/BaseLayout.astro").read_text(encoding="utf-8")
for expected in [
    'rel="canonical"',
    'rel="manifest"',
    'rel="sitemap"',
    'property="og:title"',
    'name="twitter:card"',
    'application/ld+json',
    'class="skip-link"',
]:
    assert expected in layout, f"Balise production absente: {expected}"

header = (ROOT / "website/src/components/Header.astro").read_text(encoding="utf-8")
assert 'href="/telechargements">Télécharger</a>' in header
assert 'class="mobile-menu"' in header

footer = (ROOT / "website/src/components/Footer.astro").read_text(encoding="utf-8")
assert 'href="/versions"' in footer
assert 'href="/sitemap.xml"' in footer

robots = (ROOT / "website/src/pages/robots.txt.ts").read_text(encoding="utf-8")
assert "Sitemap:" in robots
assert "radiopack.b2tech.studio" in robots

sitemap = (ROOT / "website/src/pages/sitemap.xml.ts").read_text(encoding="utf-8")
for route in [
    "/regions/normandie",
    "/regions/annecy-haute-savoie",
    "/telechargements",
    "/versions",
]:
    assert route in sitemap, f"Route absente du sitemap: {route}"

headers = (ROOT / "website/public/_headers").read_text(encoding="utf-8")
for expected in [
    "X-Frame-Options: DENY",
    "X-Content-Type-Options: nosniff",
    "Referrer-Policy: strict-origin-when-cross-origin",
    "X-Robots-Tag: noindex, noarchive",
]:
    assert expected in headers, f"En-tete Cloudflare absent: {expected}"

redirects = (ROOT / "website/public/_redirects").read_text(encoding="utf-8")
assert "radiopack-france-normandie-v0.3.csv" in redirects
assert "radiopack-france-normandie-v0.3.1.csv" in redirects

workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
for expected in [
    "actions/checkout@v6",
    "actions/setup-python@v6",
    "actions/setup-node@v6",
    "python tests/test_generator.py",
    "python tests/test_site_files.py",
    "python tests/test_annecy_research.py",
    "python tests/test_annecy_aviation_lakes.py",
    "python tests/test_annecy_airac08.py",
    "python tests/test_annecy_internal_candidate.py",
    "python tests/test_annecy_release_readiness.py",
    "python tests/test_annecy_prepublication.py",
    "npm run build",
    "statuses: write",
    "report-status:",
    "radiopack-ci/complete",
    "always() && github.event_name == 'push'",
]:
    assert expected in workflow, f"Etape CI absente: {expected}"

regions = json.loads((ROOT / "website/src/data/regions.json").read_text(encoding="utf-8"))
annecy = next(region for region in regions if region["slug"] == "annecy-haute-savoie")
assert annecy["name"] == "Annecy–Alpes–Léman"
assert annecy["status"] == "En préparation"
assert annecy["available"] is False
assert annecy["memoryCount"] == 0

region_card = (ROOT / "website/src/components/RegionCard.astro").read_text(encoding="utf-8")
assert "available?: boolean" in region_card
assert "Reconstruction v0.2" in region_card
assert "Suivre la préparation" in region_card

public_pages = [
    "website/src/pages/index.astro",
    "website/src/pages/telechargements.astro",
    "website/src/pages/versions.astro",
    "website/src/pages/regions/annecy-haute-savoie.astro",
]
for relative in public_pages:
    content = (ROOT / relative).read_text(encoding="utf-8")
    assert "/downloads/annecy-haute-savoie/radiopack-france-annecy-haute-savoie-v0.1" not in content, (
        f"Lien public Annecy v0.1 encore present: {relative}"
    )
    assert "annecy-alpes-leman-v0.2-internal" not in content, (
        f"Candidat interne exposé publiquement: {relative}"
    )
    assert "radiopack-france-annecy-alpes-leman-v0.2.csv" not in content, (
        f"Lien public Annecy v0.2 apparu avant revue finale: {relative}"
    )

home = (ROOT / "website/src/pages/index.astro").read_text(encoding="utf-8")
assert "1</strong><span>pack régional disponible" in home
assert "Annecy–Alpes–Léman" in home

downloads = (ROOT / "website/src/pages/telechargements.astro").read_text(encoding="utf-8")
assert "Un pack régional complet est actuellement disponible" in downloads
assert "Future v0.2" in downloads

versions = (ROOT / "website/src/pages/versions.astro").read_text(encoding="utf-8")
assert 'status: "En préparation"' in versions
assert "pack.download &&" in versions

annecy_page = (ROOT / "website/src/pages/regions/annecy-haute-savoie.astro").read_text(encoding="utf-8")
assert "Pas de téléchargement régional Annecy pendant la reconstruction" in annecy_page
assert "F1ZJV" in annecy_page
assert "Duplex=off" in annecy_page

print("Tests RadioPack Sprint 18 + prepublication guards: OK")
