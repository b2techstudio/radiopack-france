import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"
GENERATOR = ROOT / "website/src/pages/generateur.astro"
REGIONS = ROOT / "website/src/data/regions.json"
NORMANDIE = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv"
BRETAGNE = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"

for path in [REGISTRY, GENERATOR, REGIONS, NORMANDIE, BRETAGNE]:
    assert path.is_file(), f"Fichier multi-régions manquant: {path.relative_to(ROOT)}"

registry = REGISTRY.read_text(encoding="utf-8")
for expected in [
    'id: "annecy-alpes-leman"', 'regionSlug: "annecy-haute-savoie"', 'name: "Annecy–Alpes–Léman"',
    'version: "v0.2"', 'defaultVariant: "full"', 'includedVariant: "full"', 'excludedVariant: "no-aviation"',
    'memoryCount: 65', 'memoryCount: 48', 'id: "normandie"', 'regionSlug: "normandie"', 'version: "v0.4"',
    'defaultVariant: "standard"', 'memoryCount: 142', '/downloads/normandie/radiopack-france-normandie-v0.4.csv',
    'id: "bretagne"', 'regionSlug: "bretagne"', 'memoryCount: 151',
    '/downloads/bretagne/radiopack-france-bretagne-v0.2.csv', 'aviationIncluded: true',
    'export const defaultPublicPackId = "annecy-alpes-leman"', "export const getPublicPack", "export const getPublicVariant",
]:
    assert expected in registry, f"Contrat registre absent: {expected}"

assert registry.count('downloadUrl: "') == 4
assert "annecy-haute-savoie-v0.1" not in registry

page = GENERATOR.read_text(encoding="utf-8")
for expected in [
    'import { defaultPublicPackId, publicPacks } from "../lib/packRegistry"', 'id="radiopack-generator"', 'id="pack-select"',
    'id="pack-summary"', 'id="aviation-fieldset"', 'id="notam-fieldset"', "publicPacks.find((pack) => pack.id === selectedId)",
    "pack.aviationToggle.includedVariant", "pack.aviationToggle.excludedVariant", "aviationFieldset.hidden = !aviationSupported",
    "notamFieldset.hidden = !pack.notamCheck", "downloadLink.href = variant.downloadUrl", 'downloadLink.setAttribute("download", variant.filename)',
    "Normandie · 142", "Bretagne · 151", "Annecy · 65 / 48", 'variant.aviationIncluded ? "Incluse · variante fixe"',
]:
    assert expected in page, f"Contrat générateur multi-régions absent: {expected}"

assert "new Blob" not in page
assert "URL.createObjectURL" not in page

for path, expected_count in [(NORMANDIE, 142), (BRETAGNE, 151)]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == expected_count
    assert all(row["Duplex"] == "off" for row in rows)
    assert all(row["Offset"] == "0.000000" for row in rows)
    assert all(len(row["Name"]) <= 10 for row in rows)
    assert len({row["Location"] for row in rows}) == expected_count
    assert len({row["Name"] for row in rows}) == expected_count

print("Tests RadioPack public pack registry: Annecy 65/48 + Normandie 142 + Bretagne v0.2 151 OK")
