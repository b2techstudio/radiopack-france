import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools/build_annecy_prepublication.py"
REVIEW_MAP = ROOT / "research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json"
PLAN = ROOT / "research/annecy-alpes-leman-v0.2/prepublication-plan.json"

for path in [BUILDER, REVIEW_MAP, PLAN]:
    assert path.is_file(), f"Fichier de revue manquant: {path.relative_to(ROOT)}"

review = json.loads(REVIEW_MAP.read_text(encoding="utf-8"))
assert review["status"] == "reviewed_prepublication_not_public"
assert review["expected_memory_count"] == 65
assert review["expected_memory_count_without_aviation"] == 48
assert review["public_export_allowed"] is False
assert review["schema"] == [
    "location", "name", "frequency_mhz", "mode", "step_khz", "block", "comment_sha256"
]

schema = review["schema"]
reviewed_rows = [dict(zip(schema, row)) for row in review["rows"]]
assert len(reviewed_rows) == 65
assert len({row["location"] for row in reviewed_rows}) == 65
assert len({row["name"] for row in reviewed_rows}) == 65
assert len({row["frequency_mhz"] for row in reviewed_rows}) == 65
assert all(len(row["name"]) <= 10 for row in reviewed_rows)

AVIATION_BLOCKS = {"Aviation France et bassin genevois", "Aviation Suisse"}
reviewed_no_aviation = [row for row in reviewed_rows if row["block"] not in AVIATION_BLOCKS]
assert len(reviewed_no_aviation) == 48

plan = json.loads(PLAN.read_text(encoding="utf-8"))
public_output = ROOT / plan["reserved_public_output"]
assert not public_output.exists(), "Le CSV public ne doit pas exister pendant la revue Sprint 19"


def run_builder(*extra_args: str):
    temp = tempfile.TemporaryDirectory()
    output_dir = Path(temp.name)
    completed = subprocess.run(
        [
            sys.executable,
            str(BUILDER),
            "--root",
            str(ROOT),
            "--output-dir",
            str(output_dir),
            *extra_args,
        ],
        text=True,
        capture_output=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    csv_files = list(output_dir.glob("*.csv"))
    json_files = list(output_dir.glob("*.json"))
    assert len(csv_files) == 1
    assert len(json_files) == 1
    csv_bytes = csv_files[0].read_bytes()
    with csv_files[0].open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    manifest = json.loads(json_files[0].read_text(encoding="utf-8"))
    return temp, completed, manifest, rows, csv_bytes


def assert_reviewed_csv(actual_rows, expected_rows):
    assert len(actual_rows) == len(expected_rows)
    for actual, expected in zip(actual_rows, expected_rows):
        location = int(expected["location"])
        name = expected["name"]
        assert actual["Location"] == str(location), f"Location incorrecte pour {name}"
        assert actual["Name"] == name, f"Nom incorrect en mémoire {location}"
        assert actual["Frequency"] == f"{float(expected['frequency_mhz']):.6f}", f"Fréquence incorrecte pour {name}"
        assert actual["Mode"] == expected["mode"], f"Mode incorrect pour {name}"
        assert actual["TStep"] == f"{float(expected['step_khz']):.2f}", f"Pas incorrect pour {name}"
        assert actual["Duplex"] == "off", f"Duplex non bloqué pour {name}"
        assert actual["Offset"] == "0.000000", f"Offset non nul pour {name}"
        assert actual["Tone"] == "", f"Tone TX inattendu pour {name}"
        assert actual["Power"] == "", f"Puissance TX inattendue pour {name}"
        assert actual["URCALL"] == ""
        assert actual["RPT1CALL"] == ""
        assert actual["RPT2CALL"] == ""
        assert actual["DVCODE"] == ""
        assert actual["Comment"], f"Commentaire vide pour {name}"
        digest = hashlib.sha256(actual["Comment"].encode("utf-8")).hexdigest()
        assert digest == expected["comment_sha256"], f"Commentaire modifié sans nouvelle revue pour {name}"


full_temp, full_run, full_manifest, full_rows, full_bytes = run_builder()
try:
    assert full_manifest["memory_count"] == 65
    assert full_manifest["include_aviation"] is True
    assert_reviewed_csv(full_rows, reviewed_rows)
finally:
    full_temp.cleanup()

no_air_temp, _, no_air_manifest, no_air_rows, _ = run_builder("--no-aviation")
try:
    assert no_air_manifest["memory_count"] == 48
    assert no_air_manifest["include_aviation"] is False
    assert_reviewed_csv(no_air_rows, reviewed_no_aviation)
finally:
    no_air_temp.cleanup()

confirmed_temp, _, confirmed_manifest, confirmed_rows, confirmed_bytes = run_builder(
    "--notam-check",
    "user_confirmed",
    "--notam-confirmed-at",
    "2026-08-08T13:15:00+02:00",
)
try:
    assert confirmed_manifest["notam"]["state"] == "user_confirmed"
    assert_reviewed_csv(confirmed_rows, reviewed_rows)
    assert confirmed_bytes == full_bytes, "Le choix NOTAM ne doit jamais modifier le CSV"
finally:
    confirmed_temp.cleanup()

assert "PREPUBLICATION READY: 65 memories" in full_run.stdout
assert not public_output.exists(), "La revue ne doit jamais créer le téléchargement public"

print("Tests Annecy–Alpes–Léman Sprint 19 reviewed CSV: 65/65 OK")
