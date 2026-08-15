import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research/annecy-alpes-leman-v0.3"
RECORD = RESEARCH / "publication-record.json"
SCOPE = RESEARCH / "release-scope.json"
REVIEW = RESEARCH / "review-checklist.json"
MAP = RESEARCH / "prepublication-reviewed-memory-map.json"
FULL = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv"
NO_AIR = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv"
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"
PAGE = ROOT / "website/src/pages/regions/annecy-haute-savoie.astro"
V04_RECORD = ROOT / "research/annecy-alpes-leman-v0.4/publication-record.json"
OLD_FULL_ROUTE = ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv.ts"
OLD_NO_AIR_ROUTE = ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv.ts"

for path in [RECORD, SCOPE, REVIEW, MAP, FULL, NO_AIR, REGISTRY, PAGE, OLD_FULL_ROUTE, OLD_NO_AIR_ROUTE]:
    assert path.is_file(), f"Missing Annecy v0.3 publication file: {path.relative_to(ROOT)}"

record = json.loads(RECORD.read_text(encoding="utf-8"))
assert record["status"] == "published_immutable"
assert record["version"] == "0.3"
assert record["full_memory_count"] == 76
assert record["without_aviation_memory_count"] == 59
assert record["aviation_memory_count"] == 17
assert record["new_unique_rf_memory_count"] == 11
assert record["rules"]["immutable"] is True
assert record["rules"]["rx_only"] is True
assert record["rules"]["unpublished_adrasec_frequency_inferred"] is False

assert hashlib.sha256(FULL.read_bytes()).hexdigest() == record["public_files"]["full"]["sha256"]
assert hashlib.sha256(NO_AIR.read_bytes()).hexdigest() == record["public_files"]["without_aviation"]["sha256"]
assert hashlib.sha256(MAP.read_bytes()).hexdigest() == record["review_map"]["sha256"]


def rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))

full_rows = rows(FULL)
no_air_rows = rows(NO_AIR)
assert len(full_rows) == 76
assert len(no_air_rows) == 59
for data, count in [(full_rows, 76), (no_air_rows, 59)]:
    assert all(row["Duplex"] == "off" for row in data)
    assert all(row["Offset"] == "0.000000" for row in data)
    assert all(row["Tone"] == "" and row["Power"] == "" for row in data)
    assert all(len(row["Name"]) <= 10 for row in data)
    assert len({row["Location"] for row in data}) == count
    assert len({row["Name"] for row in data}) == count
    assert len({row["Frequency"] for row in data}) == count
    assert "50.537500" not in {row["Frequency"] for row in data}

expected_new = {
    "145.850000", "435.250000", "439.625000", "145.037500", "145.050000",
    "430.325000", "431.425000", "145.187500", "145.787500", "145.125000", "431.500000",
}
assert expected_new.issubset({row["Frequency"] for row in full_rows})
assert expected_new.issubset({row["Frequency"] for row in no_air_rows})

review_map = json.loads(MAP.read_text(encoding="utf-8"))
assert review_map["expected_memory_count"] == 76
assert review_map["expected_memory_count_without_aviation"] == 59
assert len(review_map["rows"]) == 76

scope = json.loads(SCOPE.read_text(encoding="utf-8"))
review = json.loads(REVIEW.read_text(encoding="utf-8"))
assert scope["publication_blocker_count"] == 0
assert review["completed"] == review["total"] == 12
assert review["blocker_count"] == 0

registry = REGISTRY.read_text(encoding="utf-8")
page = PAGE.read_text(encoding="utf-8")
if V04_RECORD.exists():
    current = json.loads(V04_RECORD.read_text(encoding="utf-8"))
    assert current["status"] == "published_immutable"
    assert current["version"] == "0.4"
    assert 'version: "v0.4"' in registry
    assert 'memoryCount: 77' in registry
    assert 'memoryCount: 60' in registry
    assert '/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.4.csv' in registry
    assert "Disponible — v0.4" in page
    assert "77 mémoires avec aviation" in page
    assert "60 sans aviation" in page
else:
    assert 'version: "v0.3"' in registry
    assert 'memoryCount: 76' in registry
    assert 'memoryCount: 59' in registry
    assert '/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv' in registry
    assert '/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv' in registry
    assert "Disponible — v0.3" in page
    assert "76 mémoires avec aviation" in page
    assert "59 sans aviation" in page

assert "F1ZTH" in page and "50.5375" in page
print("Annecy–Alpes–Léman v0.3 public release: immutable 76/59 RX history preserved across later releases")
