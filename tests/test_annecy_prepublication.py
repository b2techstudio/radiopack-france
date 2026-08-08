import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools/build_annecy_prepublication.py"
PLAN = ROOT / "research/annecy-alpes-leman-v0.2/prepublication-plan.json"

assert BUILDER.is_file()
assert PLAN.is_file()

plan = json.loads(PLAN.read_text(encoding="utf-8"))
public_output = ROOT / plan["reserved_public_output"]
assert not public_output.exists(), "Le CSV v0.2 public ne doit pas exister pendant la prépublication"


def run_builder(*extra_args: str):
    temp = tempfile.TemporaryDirectory()
    output_dir = Path(temp.name)
    command = [
        sys.executable,
        str(BUILDER),
        "--root",
        str(ROOT),
        "--output-dir",
        str(output_dir),
        *extra_args,
    ]
    completed = subprocess.run(command, text=True, capture_output=True)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    json_files = list(output_dir.glob("*.json"))
    csv_files = list(output_dir.glob("*.csv"))
    assert len(json_files) == 1
    assert len(csv_files) == 1
    manifest = json.loads(json_files[0].read_text(encoding="utf-8"))
    with csv_files[0].open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return temp, completed, manifest, rows


full_temp, full_run, full, full_rows = run_builder()
try:
    assert full["status"] == "prepublication_candidate_not_public"
    assert full["public_export_allowed"] is False
    assert full["generated_from_ready_state"] is True
    assert full["include_aviation"] is True
    assert full["memory_count"] == 65
    assert len(full_rows) == 65
    assert full["notam"]["state"] == "disabled"
    assert full["notam"]["requested"] is False
    assert full["notam"]["confirmed"] is False
    assert "PREPUBLICATION READY: 65 memories" in full_run.stdout
    assert "NOT PUBLIC" in full_run.stdout
    assert all(row["Duplex"] == "off" for row in full_rows)
    assert all(len(row["Name"]) <= 10 for row in full_rows)
    assert len({row["Location"] for row in full_rows}) == 65
    assert len({row["Name"] for row in full_rows}) == 65
    assert len({row["Frequency"] for row in full_rows}) == 65
    assert any(int(row["Location"]) >= 125 for row in full_rows)
finally:
    full_temp.cleanup()


no_air_temp, no_air_run, no_air, no_air_rows = run_builder(
    "--no-aviation",
    "--notam-check",
    "requested_unconfirmed",
)
try:
    assert no_air["include_aviation"] is False
    assert no_air["memory_count"] == 48
    assert len(no_air_rows) == 48
    assert no_air["notam"]["state"] == "requested_unconfirmed"
    assert no_air["notam"]["requested"] is True
    assert no_air["notam"]["confirmed"] is False
    assert no_air["notam"]["confirmed_at"] is None
    assert "PREPUBLICATION READY: 48 memories" in no_air_run.stdout
    assert all(int(row["Location"]) < 125 for row in no_air_rows)
    assert all(row["Duplex"] == "off" for row in no_air_rows)
finally:
    no_air_temp.cleanup()


confirmed_at = "2026-08-08T13:00:00+02:00"
confirmed_temp, _, confirmed, confirmed_rows = run_builder(
    "--notam-check",
    "user_confirmed",
    "--notam-confirmed-at",
    confirmed_at,
)
try:
    assert confirmed["memory_count"] == 65
    assert len(confirmed_rows) == 65
    assert confirmed["notam"]["state"] == "user_confirmed"
    assert confirmed["notam"]["requested"] is True
    assert confirmed["notam"]["confirmed"] is True
    assert confirmed["notam"]["confirmed_at"] == confirmed_at
finally:
    confirmed_temp.cleanup()

assert not public_output.exists(), "Le test de prépublication ne doit jamais créer le CSV public"

print("Tests Annecy–Alpes–Léman prepublication generator: OK")
