import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required_files = [
    "README.md", "PROJECT_STATUS.md", "CHANGELOG.md", ".github/workflows/ci.yml",
    "REGIONAL-PACK-WORKFLOW.md", "website/src/lib/chirpPack.ts",
    "website/src/lib/metropolitanPack.ts", "website/src/lib/bfcPack.ts",
    "website/src/lib/centrePack.ts", "website/src/lib/packRegistry.ts",
    "website/src/data/regions.json", "website/src/pages/regions/[slug].astro",
    "website/src/pages/downloads/[slug]/[file].csv.ts",
    "website/src/pages/downloads/bourgogne-franche-comte/radiopack-france-bourgogne-franche-comte-v0.3.csv.ts",
    "website/src/pages/downloads/centre-val-de-loire/radiopack-france-centre-val-de-loire-v0.3.csv.ts",
    "research/project-resume-state.json", "research/paired-rx-policy.json",
    "research/bourgogne-franche-comte-v0.3/publication-record.json",
    "research/centre-val-de-loire-v0.3/publication-record.json",
    "research/ile-de-france-v0.3/radio-validation-2026-08-21.json",
    "research/ile-de-france-v0.3/aviation-airac08-2026-08-21.json",
    "research/ile-de-france-v0.3/release-scope.json",
    "research/grand-est-v0.4/publication-record.json",
    "research/sprint-99-summary.md", "research/sprint-100-summary.md", "research/sprint-101-summary.md",
    "research/sprint-103-summary.md", "research/sprint-104-summary.md",
]
for relative in required_files:
    path = ROOT / relative
    assert path.is_file(), f"Fichier manquant: {relative}"
    assert path.stat().st_size > 20, f"Fichier vide ou incomplet: {relative}"

regions = json.loads((ROOT / "website/src/data/regions.json").read_text(encoding="utf-8"))
assert len(regions) == 14
expected_admin = {
    "normandie", "bretagne", "hauts-de-france", "ile-de-france", "grand-est",
    "centre-val-de-loire", "pays-de-la-loire", "bourgogne-franche-comte",
    "nouvelle-aquitaine", "auvergne-rhone-alpes", "occitanie",
    "provence-alpes-cote-d-azur", "corse",
}
region_by_slug = {item["slug"]: item for item in regions}
assert expected_admin.issubset(region_by_slug)
assert "annecy-haute-savoie" in region_by_slug
assert all(item["available"] is True for item in regions)

current_public = {
    "hauts-de-france": (144, "v0.2"), "ile-de-france": (57, "v0.3"),
    "grand-est": (97, "v0.4"), "centre-val-de-loire": (51, "v0.3"),
    "pays-de-la-loire": (130, "v0.2"), "bourgogne-franche-comte": (54, "v0.3"),
    "nouvelle-aquitaine": (151, "v0.2"), "auvergne-rhone-alpes": (62, "v0.2"),
    "occitanie": (156, "v0.2"), "provence-alpes-cote-d-azur": (159, "v0.2"),
    "corse": (137, "v0.2"),
}
for slug, (count, version) in current_public.items():
    region = region_by_slug[slug]
    assert region["memoryCount"] == count, (slug, region["memoryCount"], count)
    assert region["status"] == f"{version} disponible"
    assert "Aviation RX" in region["categories"]
assert "VHF navigation intérieure RX" in region_by_slug["grand-est"]["categories"]

historical_v02 = {
    "hauts-de-france": 144, "ile-de-france": 58, "grand-est": 59,
    "centre-val-de-loire": 42, "pays-de-la-loire": 130,
    "bourgogne-franche-comte": 37, "nouvelle-aquitaine": 151,
    "auvergne-rhone-alpes": 62, "occitanie": 156,
    "provence-alpes-cote-d-azur": 159, "corse": 137,
}
for slug, count in historical_v02.items():
    plan = json.loads((ROOT / f"research/{slug}-v0.2/pack-plan.json").read_text(encoding="utf-8"))
    assert plan["status"] == "published_v0.2"
    assert plan["current_memory_count"] == count
    assert plan["published_base_is_immutable"] is True
    assert plan["rules"]["rx_only"] is True
    assert plan["rules"]["no_artificial_fill"] is True
    assert plan["blocks"]["aviation"]["memory_count"] > 0
    for name in ["release-scope.json", "review-checklist.json", "publication-gates.json", "publication-record.json"]:
        assert (ROOT / f"research/{slug}-v0.2/{name}").is_file()

for folder, expected_count, previous_count in [
    ("bourgogne-franche-comte", 54, 37), ("centre-val-de-loire", 51, 42)
]:
    record = json.loads((ROOT / f"research/{folder}-v0.3/publication-record.json").read_text(encoding="utf-8"))
    assert record["status"] == "published_immutable"
    assert record["version"] == "0.3"
    assert record["memory_count"] == expected_count
    assert record["previous_public_memory_count"] == previous_count
    assert record["published_version_is_immutable"] is True
    assert len(record["public_csv_sha256"]) == 64

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
for expected in [
    '{ id: "ile-de-france", name: "Île-de-France", memoryCount: 57, marine: false, aviation: 18, version: "v0.3" }',
    '{ id: "grand-est", name: "Grand Est", memoryCount: 97, marine: false, aviation: 19, version: "v0.4" }',
    '{ id: "centre-val-de-loire", name: "Centre-Val de Loire", memoryCount: 51, marine: false, aviation: 7, version: "v0.3" }',
    '{ id: "bourgogne-franche-comte", name: "Bourgogne-Franche-Comté", memoryCount: 54, marine: false, aviation: 14, version: "v0.3" }',
    'export const defaultPublicPackId = "annecy-alpes-leman"',
]:
    assert expected in registry, f"Registre public incomplet: {expected}"

metro = (ROOT / "website/src/lib/metropolitanPack.ts").read_text(encoding="utf-8")
for expected in ["buildMetropolitanPackV01", "buildMetropolitanPackV02", "buildMetropolitanPackCsv", "validatePlacedChannels(placed)"]:
    assert expected in metro

bfc_builder = (ROOT / "website/src/lib/bfcPack.ts").read_text(encoding="utf-8")
assert "buildBfcV03Pack" in bfc_builder and "bfcV03MemoryCount = 54" in bfc_builder
centre_builder = (ROOT / "website/src/lib/centrePack.ts").read_text(encoding="utf-8")
assert "buildCentreV03Pack" in centre_builder and "centreV03MemoryCount = 51" in centre_builder

chirp = (ROOT / "website/src/lib/chirpPack.ts").read_text(encoding="utf-8")
for expected in ["validatePlacedChannels", "Pack trop grand", "Fréquence dupliquée", '"off"', '"0.000000"']:
    assert expected in chirp

region_route = (ROOT / "website/src/pages/regions/[slug].astro").read_text(encoding="utf-8")
for expected in ["buildMetropolitanPack", "buildBfcV03Pack", "buildCentreV03Pack", "getPublicPack", "ChannelGroupDetails", "Duplex=off", "AIRAC 08/26", "isGrandEstV04", "120–132"]:
    assert expected in region_route

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for expected in [
    "**État courant : Sprint 104 / 0.21.92", "## Sprint 104 —", "## Sprint 103 —", "## Sprint 102 —", "## Sprint 101 —", "## Sprint 100 —", "## Sprint 99 —", "## Sprint 98 —", "## Sprint 97 —",
    "Normandie v0.4** — 142 mémoires RX", "Annecy–Alpes–Léman v0.4** — 77 mémoires RX",
    "Bretagne v0.2** — 151 mémoires RX", "Île-de-France v0.3** — 57 mémoires RX", "Île-de-France v0.2** — 58 mémoires RX",
    "Grand Est v0.4** — 97 mémoires RX", "Grand Est v0.3** — 84 mémoires RX",
    "Centre-Val de Loire v0.3** — 51 mémoires RX", "Bourgogne-Franche-Comté v0.3** — 54 mémoires RX",
    "research/paired-rx-policy.json", "research/ile-de-france-v0.3/",
    "Duplex=off", "Offset=0.000000", "Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint",
]:
    assert expected in readme, f"README courant/historique incomplet: {expected}"

print("Tests RadioPack repository/site: state Sprint 104, IDF v0.3 and Grand Est v0.4 current, historical releases preserved, RX-only guards OK")
