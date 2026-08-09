import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "website/dist/downloads"

EXPECTED = {
    DIST / "annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv": 65,
    DIST / "annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv": 48,
    DIST / "normandie/radiopack-france-normandie-v0.3.1.csv": 139,
}

for path, expected_count in EXPECTED.items():
    assert path.is_file(), f"CSV public absent du build Astro: {path.relative_to(ROOT)}"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == expected_count, (
        f"Nombre de mémoires incorrect pour {path.name}: {len(rows)} != {expected_count}"
    )
    assert all(row["Duplex"] == "off" for row in rows), f"Duplex non off: {path.name}"
    assert all(row["Offset"] == "0.000000" for row in rows), f"Offset non nul: {path.name}"
    assert all(len(row["Name"]) <= 10 for row in rows), f"Nom > 10 caractères: {path.name}"
    assert len({row["Location"] for row in rows}) == expected_count, f"Location dupliquée: {path.name}"
    assert len({row["Name"] for row in rows}) == expected_count, f"Nom dupliqué: {path.name}"

print("Tests built public pack catalog: Annecy 65/48 + Normandie 139 OK")
