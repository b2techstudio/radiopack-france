import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "website/dist/downloads/annecy-alpes-leman"
REVIEW_MAP = ROOT / "research/annecy-alpes-leman-v0.3/prepublication-reviewed-memory-map.json"
RECORD = ROOT / "research/annecy-alpes-leman-v0.3/publication-record.json"
STANDARD = DIST / "radiopack-france-annecy-alpes-leman-v0.3.csv"
NO_AVIATION = DIST / "radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv"

for path in [STANDARD, NO_AVIATION, REVIEW_MAP, RECORD]:
    assert path.is_file(), f"Artefact public manquant après build: {path.relative_to(ROOT)}"

review = json.loads(REVIEW_MAP.read_text(encoding="utf-8"))
schema = review["schema"]
reviewed_rows = [dict(zip(schema, row)) for row in review["rows"]]
assert len(reviewed_rows) == 76
AVIATION_BLOCKS = {"Aviation France et bassin genevois", "Aviation Suisse"}
reviewed_no_aviation = [row for row in reviewed_rows if row["block"] not in AVIATION_BLOCKS]
assert len(reviewed_no_aviation) == 59


def read_rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate(rows, expected_rows):
    assert len(rows) == len(expected_rows)
    assert len({row["Location"] for row in rows}) == len(rows)
    assert len({row["Name"] for row in rows}) == len(rows)
    assert len({row["Frequency"] for row in rows}) == len(rows)
    for actual, expected in zip(rows, expected_rows):
        assert actual["Location"] == str(expected["location"])
        assert actual["Name"] == expected["name"]
        assert actual["Frequency"] == f"{float(expected['frequency_mhz']):.6f}"
        assert actual["Mode"] == expected["mode"]
        assert actual["TStep"] == f"{float(expected['step_khz']):.2f}"
        assert actual["Duplex"] == "off"
        assert actual["Offset"] == "0.000000"
        assert actual["Tone"] == ""
        assert actual["Power"] == ""
        assert len(actual["Name"]) <= 10
        assert hashlib.sha256(actual["Comment"].encode("utf-8")).hexdigest() == expected["comment_sha256"]

standard_rows = read_rows(STANDARD)
no_aviation_rows = read_rows(NO_AVIATION)
validate(standard_rows, reviewed_rows)
validate(no_aviation_rows, reviewed_no_aviation)

record = json.loads(RECORD.read_text(encoding="utf-8"))
assert hashlib.sha256(STANDARD.read_bytes()).hexdigest() == record["public_files"]["full"]["sha256"]
assert hashlib.sha256(NO_AVIATION.read_bytes()).hexdigest() == record["public_files"]["without_aviation"]["sha256"]
print("Tests built Annecy–Alpes–Léman public CSV: v0.3 76/76 + 59/59 OK")
