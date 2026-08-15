import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"
GENERATOR = ROOT / "website/src/pages/generateur.astro"
REGIONS = ROOT / "website/src/data/regions.json"
ANNECY_FULL = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv"
ANNECY_NO_AIR = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv"
NORMANDIE = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv"
BRETAGNE = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"
for path in [REGISTRY, GENERATOR, REGIONS, ANNECY_FULL, ANNECY_NO_AIR, NORMANDIE, BRETAGNE]:
    assert path.is_file(), f"Fichier multi-régions manquant: {path.relative_to(ROOT)}"

registry = REGISTRY.read_text(encoding="utf-8")
for expected in [
    'id: "annecy-alpes-leman"', 'regionSlug: "annecy-haute-savoie"', 'name: "Annecy–Alpes–Léman"',
    'version: "v0.3"', 'defaultVariant: "full"', 'includedVariant: "full"', 'excludedVariant: "no-aviation"',
    'memoryCount: 76', 'memoryCount: 59', 'id: "normandie"', 'regionSlug: "normandie"', 'version: "v0.4"',
    'memoryCount: 142', '/downloads/normandie/radiopack-france-normandie-v0.4.csv',
    'id: "bretagne"', 'regionSlug: "bretagne"', 'memoryCount: 151',
    '/downloads/bretagne/radiopack-france-bretagne-v0.2.csv',
    '/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv',
    '/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv',
    'export const defaultPublicPackId = "annecy-alpes-leman"', "export const getPublicPack", "export const getPublicVariant",
]:
    assert expected in registry
assert registry.count('downloadUrl: "') == 4

page = GENERATOR.read_text(encoding="utf-8")
for expected in ["Normandie · 142", "Bretagne · 151", "Annecy · 76 / 59", "publicPacks.find((pack) => pack.id === selectedId)"]:
    assert expected in page

for path, expected_count in [(ANNECY_FULL, 76), (ANNECY_NO_AIR, 59), (NORMANDIE, 142), (BRETAGNE, 151)]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == expected_count
    assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
    assert len({row["Location"] for row in rows}) == expected_count
    assert len({row["Name"] for row in rows}) == expected_count

print("Tests RadioPack public pack registry: Annecy v0.3 76/59 + Normandie 142 + Bretagne 151 OK")
