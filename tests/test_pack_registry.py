import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"
GENERATOR = ROOT / "website/src/pages/generateur.astro"
DOWNLOADS_PAGE = ROOT / "website/src/pages/telechargements.astro"
VERSIONS_PAGE = ROOT / "website/src/pages/versions.astro"
REGIONS = ROOT / "website/src/data/regions.json"
CHANNEL_DETAILS_COMPONENT = ROOT / "website/src/components/ChannelGroupDetails.astro"
CHANNEL_DETAILS_HELPER = ROOT / "website/src/lib/channelDetails.ts"
REGIONAL_PAGES = [
    ROOT / "website/src/pages/regions/bretagne.astro",
    ROOT / "website/src/pages/regions/normandie.astro",
    ROOT / "website/src/pages/regions/annecy-haute-savoie.astro",
]
ANNECY_FULL = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.4.csv"
ANNECY_NO_AIR = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.4-sans-aviation.csv"
ANNECY_V03_FULL = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv"
ANNECY_V03_NO_AIR = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv"
NORMANDIE = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv"
BRETAGNE = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"
for path in [
    REGISTRY,
    GENERATOR,
    DOWNLOADS_PAGE,
    VERSIONS_PAGE,
    REGIONS,
    CHANNEL_DETAILS_COMPONENT,
    CHANNEL_DETAILS_HELPER,
    *REGIONAL_PAGES,
    ANNECY_FULL,
    ANNECY_NO_AIR,
    ANNECY_V03_FULL,
    ANNECY_V03_NO_AIR,
    NORMANDIE,
    BRETAGNE,
]:
    assert path.is_file(), f"Fichier multi-régions manquant: {path.relative_to(ROOT)}"

registry = REGISTRY.read_text(encoding="utf-8")
for expected in [
    'id: "annecy-alpes-leman"', 'regionSlug: "annecy-haute-savoie"', 'name: "Annecy–Alpes–Léman"',
    'version: "v0.4"', 'defaultVariant: "full"', 'includedVariant: "full"', 'excludedVariant: "no-aviation"',
    'memoryCount: 77', 'memoryCount: 60', 'id: "normandie"', 'regionSlug: "normandie"', 'version: "v0.4"',
    'memoryCount: 142', '/downloads/normandie/radiopack-france-normandie-v0.4.csv',
    'id: "bretagne"', 'regionSlug: "bretagne"', 'memoryCount: 151',
    '/downloads/bretagne/radiopack-france-bretagne-v0.2.csv',
    '/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.4.csv',
    '/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.4-sans-aviation.csv',
    'export const defaultPublicPackId = "annecy-alpes-leman"', "export const getPublicPack", "export const getPublicVariant",
]:
    assert expected in registry
assert registry.count('downloadUrl: "') == 4

page = GENERATOR.read_text(encoding="utf-8")
for expected in ["Normandie · 142", "Bretagne · 151", "Annecy · 77 / 60", "publicPacks.find((pack) => pack.id === selectedId)"]:
    assert expected in page

# Public catalog/status pages must source regional versions from the same registry.
for catalog_page in [DOWNLOADS_PAGE, VERSIONS_PAGE]:
    content = catalog_page.read_text(encoding="utf-8")
    assert 'from "../lib/packRegistry"' in content
    assert "publicPacks" in content
    for stale in [
        "radiopack-france-bretagne-v0.1.csv",
        "radiopack-france-annecy-alpes-leman-v0.2.csv",
        "65 / 200 mémoires",
        "135 / 200 mémoires",
    ]:
        assert stale not in content, f"Métadonnée régionale obsolète dans {catalog_page.name}: {stale}"

# Every regional page must expose collapsible channel details sourced from its public CSV.
component = CHANNEL_DETAILS_COMPONENT.read_text(encoding="utf-8")
helper = CHANNEL_DETAILS_HELPER.read_text(encoding="utf-8")
assert '<details class="channel-group"' in component
assert "group.memories.length" in component
assert "memory.frequency" in component
assert "memory.mode" in component
assert "memory.comment" in component
assert "readFileSync" in helper
assert "../../public/" in helper
assert "buildStandardChannelGroups" in helper
assert "buildBretagneChannelGroups" in helper

for regional_page in REGIONAL_PAGES:
    content = regional_page.read_text(encoding="utf-8")
    assert "ChannelGroupDetails" in content, regional_page.name
    assert "loadPublicPackMemories" in content, regional_page.name
    assert "Tous les canaux du pack" in content, regional_page.name

bretagne_page = REGIONAL_PAGES[0].read_text(encoding="utf-8")
assert "buildBretagneChannelGroups" in bretagne_page
assert "Clique sur Rennes, Brest, Dinard, Quimper" in bretagne_page

for path, expected_count in [
    (ANNECY_FULL, 77),
    (ANNECY_NO_AIR, 60),
    (ANNECY_V03_FULL, 76),
    (ANNECY_V03_NO_AIR, 59),
    (NORMANDIE, 142),
    (BRETAGNE, 151),
]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == expected_count
    assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
    assert len({row["Location"] for row in rows}) == expected_count
    assert len({row["Name"] for row in rows}) == expected_count

with BRETAGNE.open(encoding="utf-8", newline="") as handle:
    bretagne_rows = list(csv.DictReader(handle))

assert len([row for row in bretagne_rows if row["Name"].startswith("RNS-")]) == 7
brest_rows = [row for row in bretagne_rows if row["Name"].startswith("BES-")]
assert len(brest_rows) == 5
assert [row["Frequency"] for row in brest_rows] == [
    "119.575000",
    "135.830000",
    "125.860000",
    "120.105000",
    "129.355000",
]
assert len([row for row in bretagne_rows if row["Name"].startswith("DIN-")]) == 2
assert len([row for row in bretagne_rows if row["Name"].startswith("QUIM-")]) == 1
assert len([row for row in bretagne_rows if row["Name"] == "AIR-EMERG"]) == 1

print("Tests RadioPack public pack registry: current packs, registry-backed catalog and CSV-backed regional channel details OK")
