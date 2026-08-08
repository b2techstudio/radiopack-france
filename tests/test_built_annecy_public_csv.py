import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "website/dist/downloads/annecy-alpes-leman"
REVIEW_MAP = ROOT / "research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json"

STANDARD = DIST / "radiopack-france-annecy-alpes-leman-v0.2.csv"
NO_AVIATION = DIST / "radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv"

for path in [STANDARD, NO_AVIATION, REVIEW_MAP]:
    assert path.is_file(), f"Artefact public manquant après build: {path.relative_to(ROOT)}"
    assert path.stat().st_size > 100, f"Artefact public vide ou incomplet: {path.relative_to(ROOT)}"

review = json.loads(REVIEW_MAP.read_text(encoding="utf-8"))
schema = review["schema"]
reviewed_rows = [dict(zip(schema, row)) for row in review["rows"]]
assert len(reviewed_rows) == 65

AVIATION_BLOCKS = {"Aviation France et bassin genevois", "Aviation Suisse"}
reviewed_no_aviation = [row for row in reviewed_rows if row["block"] not in AVIATION_BLOCKS]
assert len(reviewed_no_aviation) == 48


def read_rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate(rows, expected_rows):
    assert len(rows) == len(expected_rows)
    assert len({row["Location"] for row in rows}) == len(rows)
    assert len({row["Name"] for row in rows}) == len(rows)
    assert len({row["Frequency"] for row in rows}) == len(rows)

    for actual, expected in zip(rows, expected_rows):
        name = expected["name"]
        assert actual["Location"] == str(expected["location"]), f"Location incorrecte pour {name}"
        assert actual["Name"] == name, f"Nom incorrect pour {name}"
        assert actual["Frequency"] == f"{float(expected['frequency_mhz']):.6f}", f"Fréquence incorrecte pour {name}"
        assert actual["Mode"] == expected["mode"], f"Mode incorrect pour {name}"
        assert actual["TStep"] == f"{float(expected['step_khz']):.2f}", f"Pas incorrect pour {name}"
        assert actual["Duplex"] == "off", f"Duplex non bloqué pour {name}"
        assert actual["Offset"] == "0.000000", f"Offset non nul pour {name}"
        assert actual["Tone"] == "", f"Tone TX inattendu pour {name}"
        assert actual["Power"] == "", f"Puissance TX inattendue pour {name}"
        assert len(actual["Name"]) <= 10
        digest = hashlib.sha256(actual["Comment"].encode("utf-8")).hexdigest()
        assert digest == expected["comment_sha256"], f"Commentaire public différent de la revue pour {name}"


standard_rows = read_rows(STANDARD)
no_aviation_rows = read_rows(NO_AVIATION)
validate(standard_rows, reviewed_rows)
validate(no_aviation_rows, reviewed_no_aviation)

assert any(int(row["Location"]) >= 125 for row in standard_rows)
assert all(int(row["Location"]) < 125 for row in no_aviation_rows)

print("Tests built Annecy–Alpes–Léman public CSV: 65/65 + 48/48 OK")
