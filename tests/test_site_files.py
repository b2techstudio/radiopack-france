import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

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
    "website/src/lib/bfcPack.ts",
    "website/src/lib/centrePack.ts",
    "website/src/lib/packRegistry.ts",
    "website/src/data/regions.json",
    "website/src/pages/index.astro",
    "website/src/pages/regions/index.astro",
    "website/src/pages/regions/[slug].astro",
    "website/src/pages/downloads/[slug]/[file].csv.ts",
    "website/src/pages/downloads/bourgogne-franche-comte/radiopack-france-bourgogne-franche-comte-v0.3.csv.ts",
    "website/src/pages/downloads/centre-val-de-loire/radiopack-france-centre-val-de-loire-v0.3.csv.ts",
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
    "research/metropolitan-regions-v0.2-enrichment.md",
    "research/paired-rx-policy.json",
    "research/project-resume-state.json",
    "research/bourgogne-franche-comte-v0.3/publication-record.json",
]
for relative in required_files:
    path = ROOT / relative
    assert path.is_file(), f"Fichier manquant: {relative}"
    assert path.stat().st_size > 20, f"Fichier vide ou incomplet: {relative}"

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
    "normandie", "bretagne", "hauts-de-france", "ile-de-france", "grand-est",
    "centre-val-de-loire", "pays-de-la-loire", "bourgogne-franche-comte",
    "nouvelle-aquitaine", "auvergne-rhone-alpes", "occitanie",
    "provence-alpes-cote-d-azur", "corse",
}
assert expected_admin.issubset(region_slugs)
assert "annecy-haute-savoie" in region_slugs
assert all(region["available"] is True for region in regions)
assert next(region for region in regions if region["slug"] == "annecy-haute-savoie")["memoryCount"] == 77
assert next(region for region in regions if region["slug"] == "normandie")["memoryCount"] == 142
assert next(region for region in regions if region["slug"] == "bretagne")["memoryCount"] == 151

# Sprint-98 v0.2 files remain immutable historical bases; BFC and Centre have since advanced to v0.3.
historical_v02 = {
    "hauts-de-france": (144, True),
    "ile-de-france": (58, False),
    "grand-est": (59, False),
    "centre-val-de-loire": (42, False),
    "pays-de-la-loire": (130, True),
    "bourgogne-franche-comte": (37, False),
    "nouvelle-aquitaine": (151, True),
    "auvergne-rhone-alpes": (62, False),
    "occitanie": (156, True),
    "provence-alpes-cote-d-azur": (159, True),
    "corse": (137, True),
}
current_public = {
    "hauts-de-france": (144, "v0.2"),
    "ile-de-france": (58, "v0.2"),
    "grand-est": (59, "v0.2"),
    "centre-val-de-loire": (51, "v0.3"),
    "pays-de-la-loire": (130, "v0.2"),
    "bourgogne-franche-comte": (54, "v0.3"),
    "nouvelle-aquitaine": (151, "v0.2"),
    "auvergne-rhone-alpes": (62, "v0.2"),
    "occitanie": (156, "v0.2"),
    "provence-alpes-cote-d-azur": (159, "v0.2"),
    "corse": (137, "v0.2"),
}
for slug, (historical_count, marine) in historical_v02.items():
    region = next(item for item in regions if item["slug"] == slug)
    current_count, current_version = current_public[slug]
    assert region["memoryCount"] == current_count, (slug, region["memoryCount"], current_count)
    assert region["status"] == f"{current_version} disponible"
    categories = region["categories"]
    assert "Aviation RX" in categories
    assert ("VHF marine RX" in categories) is marine
    plan = json.loads((ROOT / f"research/{slug}-v0.2/pack-plan.json").read_text(encoding="utf-8"))
    assert plan["status"] == "published_v0.2"
    assert plan["current_memory_count"] == historical_count
    assert plan["based_on_published_version"] == "0.1"
    assert plan["published_base_is_immutable"] is True
    assert plan["rules"]["rx_only"] is True
    assert plan["rules"]["no_artificial_fill"] is True
    assert plan["rules"]["private_ppdr_operational_data_excluded"] is True
    assert plan["blocks"]["marine"]["included"] is marine
    assert plan["blocks"]["aviation"]["memory_count"] > 0
    assert (ROOT / f"research/{slug}-v0.2/README.md").is_file()

bfc03 = json.loads((ROOT / "research/bourgogne-franche-comte-v0.3/publication-record.json").read_text(encoding="utf-8"))
assert bfc03["status"] == "published_immutable"
assert bfc03["version"] == "0.3"
assert bfc03["memory_count"] == 54
assert bfc03["previous_public_version"] == "0.2"
assert bfc03["previous_public_memory_count"] == 37
assert bfc03["published_version_is_immutable"] is True

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
for expected in [
    'id: "annecy-alpes-leman"', 'id: "normandie"', 'id: "bretagne"',
    'memoryCount: 77', 'memoryCount: 60', 'memoryCount: 142', 'memoryCount: 151',
    'const metropolitanMetadata = [', 'version: "v0.2"',
    '{ id: "bourgogne-franche-comte", name: "Bourgogne-Franche-Comté", memoryCount: 54, marine: false, aviation: 14, version: "v0.3" }',
    '{ id: "centre-val-de-loire", name: "Centre-Val de Loire", memoryCount: 51, marine: false, aviation: 7, version: "v0.3" }',
    'downloadUrl: `/downloads/${item.id}/${filename}`',
    'export const defaultPublicPackId = "annecy-alpes-leman"',
]:
    assert expected in registry, f"Registre public incomplet: {expected}"
for slug in historical_v02:
    assert f'id: "{slug}"' in registry, f"Pack régional absent du registre: {slug}"

metro = (ROOT / "website/src/lib/metropolitanPack.ts").read_text(encoding="utf-8")
for expected in [
    "export const metropolitanV01PackDefinitions",
    "export const metropolitanPackDefinitions",
    "buildMetropolitanPackV01",
    "buildMetropolitanPackV02",
    "buildMetropolitanPackCsv",
    "validatePlacedChannels(placed)",
    'loadChannels("data/national/pmr446.json")',
    'loadChannels("data/national/amateur-calls-rx.json")',
    'loadChannels("data/national/amateur-listening-rx.json")',
    'loadChannels("data/national/marine-vhf-rx.json")',
    'block: "REGIONAL_2M"',
    "repeater.output - 0.6",
    "https://www.repeaterbook.com/",
    "https://f5aib.net/",
    "https://www.r-e-f.org/",
    "https://www.sia.aviation-civile.gouv.fr/",
    "2026-08-19",
]:
    assert expected in metro, f"Contrat métropolitain v0.2 absent: {expected}"
for slug in historical_v02:
    assert metro.count(f'id: "{slug}"') >= 1, f"Définition RF absente: {slug}"

bfc_builder = (ROOT / "website/src/lib/bfcPack.ts").read_text(encoding="utf-8")
for expected in ["buildBfcV03Pack", "bfcV03MemoryCount = 54", 'name: "CHAL-INFO"', "frequency_mhz: 118.605"]:
    assert expected in bfc_builder, f"Builder BFC v0.3 incomplet: {expected}"

centre_builder = (ROOT / "website/src/lib/centrePack.ts").read_text(encoding="utf-8")
for expected in ["buildCentreV03Pack", "centreV03MemoryCount = 51", 'name: "CHR-TWR1"', "frequency_mhz: 125.88", 'name: "SDH-AFIS"', "frequency_mhz: 122.405"]:
    assert expected in centre_builder, f"Builder Centre v0.3 incomplet: {expected}"

chirp_pack = (ROOT / "website/src/lib/chirpPack.ts").read_text(encoding="utf-8")
for expected in ["validatePlacedChannels", "Pack trop grand", "Nom trop long", "Fréquence dupliquée", '"off"', '"0.000000"']:
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
assert "metropolitanV01PackDefinitions" in download_route
assert "buildMetropolitanPackCsv" in download_route
assert "version: pack.version" in download_route
assert '"Content-Type": "text/csv; charset=utf-8"' in download_route

region_route = (ROOT / "website/src/pages/regions/[slug].astro").read_text(encoding="utf-8")
for expected in ["getStaticPaths", "metropolitanPackDefinitions", "buildMetropolitanPack", "buildBfcV03Pack", "buildCentreV03Pack", "getPublicPack", "ChannelGroupDetails", "Duplex=off", "AIRAC 08/26", "VHF marine"]:
    assert expected in region_route

release_v01 = (ROOT / "research/metropolitan-regions-v0.1-release.md").read_text(encoding="utf-8")
for expected in ["13/13", "onze régions administratives métropolitaines", "paired RX", "Duplex=off", "Offset=0.000000", "non exhaustive", "RepeaterBook", "F5AIB/REF"]:
    assert expected in release_v01, f"Documentation historique v0.1 incomplète: {expected}"

release_v02 = (ROOT / "research/metropolitan-regions-v0.2-enrichment.md").read_text(encoding="utf-8")
for expected in ["onze packs", "v0.2 enrichie", "AIRAC 08/26", "VHF marine", "paired RX", "v0.1 restent", "UHF", "PPDR", "pack-plan.json"]:
    assert expected in release_v02, f"Documentation v0.2 incomplète: {expected}"

paired_policy = json.loads((ROOT / "research/paired-rx-policy.json").read_text(encoding="utf-8"))
assert paired_policy["status"] == "active_project_policy"
assert paired_policy["core_rule"]["native_duplex_or_split_pair_exports_both_rx_frequencies"] is True
assert paired_policy["core_rule"]["tx_disabled"] is True
assert paired_policy["core_rule"]["chirp_duplex"] == "off"
assert paired_policy["core_rule"]["chirp_offset"] == "0.000000"
assert paired_policy["deduplication"]["same_rf_frequency_kept_once_per_pack"] is True

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for expected in [
    "**État courant : Sprint 98 / 0.21.87", "## État actuel — Sprint 98 / 0.21.87", "## Sprint 97 —",
    "Normandie v0.4** — 142 mémoires RX", "Annecy–Alpes–Léman v0.4** — 77 mémoires RX",
    "Bretagne v0.2** — 151 mémoires RX", "research/paired-rx-policy.json", "Duplex=off", "Offset=0.000000",
    "Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint",
]:
    assert expected in readme, f"README historique incomplet: {expected}"

print("Tests RadioPack repository/site: 13/13 metropolitan admin regions, BFC v0.3=54 and Centre v0.3=51, historical v0.1/v0.2 preserved, aviation/marine/paired-RX guards OK")
