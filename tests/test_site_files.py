import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required_files = [
    ".github/workflows/ci.yml",
    "tests/test_annecy_research.py",
    "tests/test_annecy_aviation_lakes.py",
    "tests/test_annecy_internal_candidate.py",
    "research/annecy-alpes-leman-v0.2/radioamateur-france-inventory.json",
    "research/annecy-alpes-leman-v0.2/radioamateur-switzerland-candidates.json",
    "research/annecy-alpes-leman-v0.2/aviation-france-pre-airac-08.json",
    "research/annecy-alpes-leman-v0.2/navigation-lakes-findings.json",
    "research/annecy-alpes-leman-v0.2/satellites-fm-inventory.json",
    "research/annecy-alpes-leman-v0.2/memory-plan.json",
    "tools/build_annecy_internal_candidate.py",
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
    "python tests/test_annecy_internal_candidate.py",
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

print("Tests RadioPack Sprint 10: OK")
