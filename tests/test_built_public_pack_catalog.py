import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "website/dist/downloads"
EXPECTED = {
    DIST / "annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv": 76,
    DIST / "annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv": 59,
    DIST / "normandie/radiopack-france-normandie-v0.4.csv": 142,
    DIST / "bretagne/radiopack-france-bretagne-v0.2.csv": 151,
    DIST / "hauts-de-france/radiopack-france-hauts-de-france-v0.2.csv": 144,
    DIST / "ile-de-france/radiopack-france-ile-de-france-v0.2.csv": 58,
    DIST / "grand-est/radiopack-france-grand-est-v0.2.csv": 59,
    DIST / "centre-val-de-loire/radiopack-france-centre-val-de-loire-v0.2.csv": 42,
    DIST / "pays-de-la-loire/radiopack-france-pays-de-la-loire-v0.2.csv": 130,
    DIST / "bourgogne-franche-comte/radiopack-france-bourgogne-franche-comte-v0.2.csv": 37,
    DIST / "nouvelle-aquitaine/radiopack-france-nouvelle-aquitaine-v0.2.csv": 151,
    DIST / "auvergne-rhone-alpes/radiopack-france-auvergne-rhone-alpes-v0.2.csv": 62,
    DIST / "occitanie/radiopack-france-occitanie-v0.2.csv": 156,
    DIST / "provence-alpes-cote-d-azur/radiopack-france-provence-alpes-cote-d-azur-v0.2.csv": 159,
    DIST / "corse/radiopack-france-corse-v0.2.csv": 137,
}

metropolitan_hashes = {}
for path, expected_count in EXPECTED.items():
    assert path.is_file(), f"CSV public absent du build Astro: {path.relative_to(ROOT)}"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == expected_count
    assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
    assert all(len(row["Name"]) <= 10 for row in rows)
    assert len({row["Location"] for row in rows}) == expected_count
    assert len({row["Name"] for row in rows}) == expected_count

    if path.name.endswith("-v0.2.csv") and path.parent.name not in {"bretagne"}:
        metropolitan_hashes[path.parent.name] = {
            "memory_count": expected_count,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }

assert len(metropolitan_hashes) == 11
print("SPRINT98_METROPOLITAN_HASHES=" + json.dumps(metropolitan_hashes, sort_keys=True))
print("Tests built public pack catalog: mature packs + 11 metropolitan v0.2 generated CSVs, RX-only and unique, OK")
