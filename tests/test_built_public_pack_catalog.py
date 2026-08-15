import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "website/dist/downloads"
EXPECTED = {
    DIST / "annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv": 76,
    DIST / "annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv": 59,
    DIST / "normandie/radiopack-france-normandie-v0.4.csv": 142,
    DIST / "bretagne/radiopack-france-bretagne-v0.2.csv": 151,
}
for path, expected_count in EXPECTED.items():
    assert path.is_file(), f"CSV public absent du build Astro: {path.relative_to(ROOT)}"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == expected_count
    assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
    assert all(len(row["Name"]) <= 10 for row in rows)
    assert len({row["Location"] for row in rows}) == expected_count
    assert len({row["Name"] for row in rows}) == expected_count
print("Tests built public pack catalog: Annecy v0.3 76/59 + Normandie 142 + Bretagne v0.2 151 OK")
