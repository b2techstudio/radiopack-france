from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required_files = [
    ".github/workflows/ci.yml",
    "website/astro.config.mjs",
    "website/src/layouts/BaseLayout.astro",
    "website/src/components/Header.astro",
    "website/src/components/Footer.astro",
    "website/src/pages/404.astro",
    "website/src/pages/versions.astro",
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
    "npm run build",
]:
    assert expected in workflow, f"Etape CI absente: {expected}"

print("Tests RadioPack Sprint 6: OK")
