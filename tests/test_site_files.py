import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# High-level repository contract. Detailed historical RF rules remain covered by
# their dedicated sprint tests in CI; this guard follows the current public site.
required_files = [
    "README.md",
    "PROJECT_STATUS.md",
    ".github/workflows/ci.yml",
    "REGIONAL-PACK-WORKFLOW.md",
    "generator/options.json",
    "generator/generate_chirp_csv.py",
    "website/src/lib/chirpPack.ts",
    "website/src/lib/annecyPack.ts",
    "website/src/lib/metropolitanPack.ts",
    "website/src/lib/packRegistry.ts",
    "website/src/data/regions.json",
    "website/src/pages/index.astro",
    "website/src/pages/regions/index.astro",
    "website/src/pages/regions/[slug].astro",
    "website/src/pages/downloads/[slug]/[file].csv.ts",
    "website/src/pages/generateur.astro",
    "website/src/pages/telechargements.astro",
    "website/src/pages/versions.astro",
    "website/src/pages/sitemap.xml.ts",
    "website/src/pages/regions/normandie.astro",
    "website/src/pages/regions/bretagne.astro",
    "website/src/pages/regions/annecy-haute-savoie.astro",
    "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv",
    "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv",
    "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.4.csv",
    "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.4-sans-aviation.csv",
    "research/metropolitan-regions-v0.1-release.md",
    "research/paired-rx-policy.json",
    "research/project-resume-state.json",
]

for relative in required_files:
    path = ROOT / relative
    assert path.is_file(), f"Fichier manquant: {relative}"
    assert path.stat().st_size > 20, f"Fichier vide ou incomplet: {relative}"

# Existing immutable public versions must remain present.
for relative in [
    "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv",
    "website/public/downloads/bretagne/radiopack-france-bretagne-v0.1.csv",
    "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv",
    "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv",
]:
    assert (ROOT / relative).is_file(), f"Version historique immuable manquante: {relative}"

regions = json.loads((ROOT / "website/src/data/regions.json").read_text(encoding="utf-8"))
assert len(regions) == 14
region_slugs = {region["slug"] for region in regions}
expected_admin = {
    "normandie",
    "bretagne",
    "hauts-de-france",
    "ile-de-france",
    "grand-est",
    "centre-val-de-loire",
    "pays-de-la-loire",
    "bourgogne-franche-comte",
    "nouvelle-aquitaine",
    "auvergne-rhone-alpes",
    "occitanie",
    "provence-alpes-cote-d-azur",
    "corse",
}
assert expected_admin.issubset(region_slugs)
assert "annecy-haute-savoie" in region_slugs
assert all(region["available"] is True for region in regions)
assert next(region for region in regions if region["slug"] == "annecy-haute-savoie")["memoryCount"] == 77
assert next(region for region in regions if region["slug"] == "normandie")["memoryCount"] == 142
assert next(region for region in regions if region["slug"] == "bretagne")["memoryCount"] == 151

expected_v01_counts = {
    "hauts-de-france": 36,
    "ile-de-france": 34,
    "grand-est": 36,
    "centre-val-de-loire": 32,
    "pays-de-la-loire": 30,
    "bourgogne-franche-comte": 30,
    "nouvelle-aquitaine": 42,
    "auvergne-rhone-alpes": 38,
    "occitanie": 44,
    "provence-alpes-cote-d-azur": 42,
    "corse": 28,
}
for slug, count in expected_v01_counts.items():
    region = next(item for item in regions if item["slug"] == slug)
    assert region["memoryCount"] == count, (slug, region["memoryCount"], count)
    assert region["status"] == "v0.1 disponible"

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
for expected in [
    'id: "annecy-alpes-leman"',
    'id: "normandie"',
    'id: "bretagne"',
    'memoryCount: 77',
    'memoryCount: 60',
    'memoryCount: 142',
    'memoryCount: 151',
    'const metropolitanMetadata = [',
    'version: "v0.1"',
    'downloadUrl: `/downloads/${item.id}/${filename}`',
    'export const defaultPublicPackId = "annecy-alpes-leman"',
]:
    assert expected in registry, f"Registre public incomplet: {expected}"
for slug in expected_v01_counts:
    assert f'id: "{slug}"' in registry, f"Pack v0.1 absent du registre: {slug}"

metro = (ROOT / "website/src/lib/metropolitanPack.ts").read_text(encoding="utf-8")
for expected in [
    "export const metropolitanPackDefinitions",
    "buildMetropolitanPack",
    "buildMetropolitanPackCsv",
    "validatePlacedChannels(placed)",
    'loadChannels("data/national/pmr446.json")',
    'loadChannels("data/national/amateur-calls-rx.json")',
    'loadChannels("data/national/amateur-listening-rx.json")',
    'block: "REGIONAL_2M"',
    "repeater.output - 0.6",
    "https://www.repeaterbook.com/",
    "https://f5aib.net/",
    "https://www.r-e-f.org/",
    "2026-08-19",
]:
    assert expected in metro, f"Contrat métropolitain absent: {expected}"
for slug in expected_v01_counts:
    assert f'id: "{slug}"' in metro, f"Définition RF v0.1 absente: {slug}"

chirp_pack = (ROOT / "website/src/lib/chirpPack.ts").read_text(encoding="utf-8")
for expected in [
    "validatePlacedChannels",
    "Pack trop grand",
    "Nom trop long",
    "Fréquence dupliquée",
    '"off"',
    '"0.000000"',
]:
    assert expected in chirp_pack, f"Garde CHIRP absent: {expected}"

for page_name in ["index.astro", "generateur.astro", "telechargements.astro", "versions.astro"]:
    content = (ROOT / f"website/src/pages/{page_name}").read_text(encoding="utf-8")
    assert "publicPacks" in content, f"Registre non utilisé par {page_name}"

home = (ROOT / "website/src/pages/index.astro").read_text(encoding="utf-8")
assert "13 régions administratives métropolitaines" in home
assert "metropolitanCount" in home
assert "packs.map" in home

generator = (ROOT / "website/src/pages/generateur.astro").read_text(encoding="utf-8")
assert "13 régions métropolitaines" in generator
assert "metroPacks.map" in generator
assert 'data-pack-shortcut={pack.id}' in generator

download_route = (ROOT / "website/src/pages/downloads/[slug]/[file].csv.ts").read_text(encoding="utf-8")
assert "getStaticPaths" in download_route
assert "metropolitanPackDefinitions" in download_route
assert "buildMetropolitanPackCsv" in download_route
assert '"Content-Type": "text/csv; charset=utf-8"' in download_route

region_route = (ROOT / "website/src/pages/regions/[slug].astro").read_text(encoding="utf-8")
assert "getStaticPaths" in region_route
assert "metropolitanPackDefinitions" in region_route
assert "buildMetropolitanPack" in region_route
assert "ChannelGroupDetails" in region_route
assert "Duplex=off" in region_route

release = (ROOT / "research/metropolitan-regions-v0.1-release.md").read_text(encoding="utf-8")
for expected in [
    "13/13",
    "onze régions administratives métropolitaines",
    "paired RX",
    "Duplex=off",
    "Offset=0.000000",
    "non exhaustive",
    "RepeaterBook",
    "F5AIB/REF",
]:
    assert expected in release, f"Documentation release métropolitaine incomplète: {expected}"

paired_policy = json.loads((ROOT / "research/paired-rx-policy.json").read_text(encoding="utf-8"))
assert paired_policy["status"] == "active_project_policy"
assert paired_policy["core_rule"]["native_duplex_or_split_pair_exports_both_rx_frequencies"] is True
assert paired_policy["core_rule"]["tx_disabled"] is True
assert paired_policy["core_rule"]["chirp_duplex"] == "off"
assert paired_policy["core_rule"]["chirp_offset"] == "0.000000"
assert paired_policy["deduplication"]["same_rf_frequency_kept_once_per_pack"] is True

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for expected in [
    "**État courant : Sprint 97 / 0.21.86",
    "## État actuel — Sprint 97 / 0.21.86",
    "Normandie v0.4** — 142 mémoires RX",
    "Annecy–Alpes–Léman v0.4** — 77 mémoires RX",
    "Bretagne v0.2** — 151 mémoires RX",
    "research/paired-rx-policy.json",
    "Duplex=off",
    "Offset=0.000000",
    "Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint",
]:
    assert expected in readme, f"README historique incomplet: {expected}"

print("Tests RadioPack repository/site: 13/13 metropolitan admin regions + Annecy specialized, registry-backed UI, deterministic v0.1 RX-only routes and historical guards OK")
