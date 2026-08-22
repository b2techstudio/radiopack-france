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
    "website/src/pages/downloads/bourgogne-franche-comte/radiopack-france-bourgogne-franche-comte-v0.4.csv.ts",
    "website/src/pages/downloads/centre-val-de-loire/radiopack-france-centre-val-de-loire-v0.3.csv.ts",
    "research/project-resume-state.json", "research/paired-rx-policy.json",
    "research/bourgogne-franche-comte-v0.3/publication-record.json",
    "research/bourgogne-franche-comte-v0.4/publication-record.json",
    "research/bourgogne-franche-comte-v0.4/release-scope.json",
    "research/bourgogne-franche-comte-v0.4/publication-gates.json",
    "research/centre-val-de-loire-v0.3/publication-record.json",
    "research/ile-de-france-v0.3/publication-record.json",
    "research/ile-de-france-v0.4/publication-record.json",
    "research/grand-est-v0.4/publication-record.json",
    "research/sprint-99-summary.md", "research/sprint-100-summary.md", "research/sprint-101-summary.md",
    "research/sprint-103-summary.md", "research/sprint-104-summary.md", "research/sprint-105-summary.md",
    "research/sprint-106-summary.md", "research/sprint-107-summary.md",
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
    "hauts-de-france": (144, "v0.2"),
    "ile-de-france": (64, "v0.4"),
    "grand-est": (97, "v0.4"),
    "centre-val-de-loire": (51, "v0.3"),
    "pays-de-la-loire": (130, "v0.2"),
    "bourgogne-franche-comte": (61, "v0.4"),
    "nouvelle-aquitaine": (151, "v0.2"),
    "auvergne-rhone-alpes": (62, "v0.2"),
    "occitanie": (156, "v0.2"),
    "provence-alpes-cote-d-azur": (159, "v0.2"),
    "corse": (137, "v0.2"),
}
for slug, (count, version) in current_public.items():
    region = region_by_slug[slug]
    assert region["memoryCount"] == count, (slug, region["memoryCount"], count)
    assert region["status"] == f"{version} disponible"
    assert "Aviation RX" in region["categories"]

for slug in ["bourgogne-franche-comte", "ile-de-france", "grand-est"]:
    assert "VHF navigation intérieure RX" in region_by_slug[slug]["categories"]

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

# Historical v0.3 publications remain immutable after later promotions.
for folder, expected_count, previous_count in [
    ("bourgogne-franche-comte", 54, 37),
    ("centre-val-de-loire", 51, 42),
]:
    record = json.loads((ROOT / f"research/{folder}-v0.3/publication-record.json").read_text(encoding="utf-8"))
    assert record["status"] == "published_immutable"
    assert record["version"] == "0.3"
    assert record["memory_count"] == expected_count
    assert record["previous_public_memory_count"] == previous_count
    assert record["published_version_is_immutable"] is True
    assert len(record["public_csv_sha256"]) == 64

bfc_v04 = json.loads((ROOT / "research/bourgogne-franche-comte-v0.4/publication-record.json").read_text(encoding="utf-8"))
assert bfc_v04["status"] == "published_immutable"
assert bfc_v04["version"] == "0.4"
assert bfc_v04["memory_count"] == 61
assert bfc_v04["previous_public_version"] == "0.3"
assert bfc_v04["previous_public_memory_count"] == 54
assert bfc_v04["public_csv_sha256"] == "02dcba7e14a0cce331b63126ea4e552d41013ebd51aecec19907009f40236a72"
assert bfc_v04["published_version_is_immutable"] is True

idf_v03 = json.loads((ROOT / "research/ile-de-france-v0.3/publication-record.json").read_text(encoding="utf-8"))
idf_v04 = json.loads((ROOT / "research/ile-de-france-v0.4/publication-record.json").read_text(encoding="utf-8"))
assert idf_v03["status"] == "published_immutable" and idf_v03["memory_count"] == 57
assert idf_v04["status"] == "published_immutable" and idf_v04["memory_count"] == 64
assert idf_v04["previous_public_version"] == "0.3" and idf_v04["previous_public_memory_count"] == 57

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
for expected in [
    '{ id: "ile-de-france", name: "Île-de-France", memoryCount: 64, marine: false, aviation: 18, version: "v0.4" }',
    '{ id: "grand-est", name: "Grand Est", memoryCount: 97, marine: false, aviation: 19, version: "v0.4" }',
    '{ id: "centre-val-de-loire", name: "Centre-Val de Loire", memoryCount: 51, marine: false, aviation: 7, version: "v0.3" }',
    '{ id: "bourgogne-franche-comte", name: "Bourgogne-Franche-Comté", memoryCount: 61, marine: false, aviation: 14, version: "v0.4" }',
    '7 mémoires VHF navigation intérieure',
    '13 mémoires VHF navigation intérieure',
    'export const defaultPublicPackId = "annecy-alpes-leman"',
]:
    assert expected in registry, f"Registre public incomplet: {expected}"

metro = (ROOT / "website/src/lib/metropolitanPack.ts").read_text(encoding="utf-8")
for expected in ["buildMetropolitanPackV01", "buildMetropolitanPackV02", "buildMetropolitanPackCsv", "validatePlacedChannels(placed)"]:
    assert expected in metro

bfc_builder = (ROOT / "website/src/lib/bfcPack.ts").read_text(encoding="utf-8")
for expected in ["buildBfcV03Pack", "bfcV03MemoryCount = 54", "buildBfcV04Pack", "bfcV04MemoryCount = 61", "INLAND_VHF_V04"]:
    assert expected in bfc_builder
centre_builder = (ROOT / "website/src/lib/centrePack.ts").read_text(encoding="utf-8")
assert "buildCentreV03Pack" in centre_builder and "centreV03MemoryCount = 51" in centre_builder

chirp = (ROOT / "website/src/lib/chirpPack.ts").read_text(encoding="utf-8")
for expected in ["validatePlacedChannels", "Pack trop grand", "Fréquence dupliquée", '"off"', '"0.000000"']:
    assert expected in chirp

region_route = (ROOT / "website/src/pages/regions/[slug].astro").read_text(encoding="utf-8")
for expected in [
    "buildMetropolitanPack", "buildBfcV03Pack", "buildBfcV04Pack", "buildCentreV03Pack", "getPublicPack", "ChannelGroupDetails",
    "Duplex=off", "AIRAC 08/26", "isBfcV04", "isIdfV04", "isGrandEstV04", "120–126", "120–132",
    "radiopack-france-ile-de-france-v0.4.csv", "radiopack-france-grand-est-v0.4.csv",
]:
    assert expected in region_route

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for expected in [
    "Sprint 107 / 0.21.95",
    "## Sprint 107 — Bourgogne-Franche-Comté v0.4 publiée",
    "## Sprint 106 — candidat BFC v0.4 figé",
    "## Sprint 105 — Île-de-France v0.4 publiée",
    "## Sprint 104 — Grand Est v0.4 publiée",
    "## Sprint 103 — audit VHF navigation intérieure",
    "## Sprint 101 — Île-de-France v0.3 publiée",
    "## Sprint 100 — Centre-Val de Loire v0.3",
    "## Sprint 99 — Bourgogne-Franche-Comté v0.3",
    "**Normandie v0.4** — 142 mémoires RX",
    "**Annecy–Alpes–Léman v0.4** — 77 mémoires RX",
    "**Bretagne v0.2** — 151 mémoires RX",
    "**Île-de-France v0.4** — 64 mémoires RX",
    "**Grand Est v0.4** — 97 mémoires RX",
    "**Centre-Val de Loire v0.3** — 51 mémoires RX",
    "**Bourgogne-Franche-Comté v0.4** — 61 mémoires RX",
    "**1582 mémoires RX cumulées**",
    "research/paired-rx-policy.json",
    "Duplex=off", "Offset=0.000000",
    "Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint",
]:
    assert expected in readme, f"README courant/historique incomplet: {expected}"

status = (ROOT / "PROJECT_STATUS.md").read_text(encoding="utf-8")
for expected in ["Sprint courant : **107**", "État logique : **0.21.95**", "Bourgogne-Franche-Comté v0.4", "Auvergne-Rhône-Alpes v0.3"]:
    assert expected in status

print("Tests RadioPack repository/site: state Sprint 107, BFC/IDF/Grand Est v0.4 current, historical releases preserved, RX-only guards OK")
