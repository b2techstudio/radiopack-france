import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools/build_annecy_internal_candidate.py"
RESEARCH = ROOT / "research/annecy-alpes-leman-v0.2"
SATELLITES = RESEARCH / "satellites-fm-inventory.json"
PLAN = RESEARCH / "memory-plan.json"

for path in [BUILDER, SATELLITES, PLAN]:
    assert path.is_file(), f"Fichier Sprint 10 manquant: {path.relative_to(ROOT)}"

satellites = json.loads(SATELLITES.read_text(encoding="utf-8"))
assert satellites["production_ready"] is False
assert satellites["internal_candidate_allowed"] is True
assert len(satellites["channels"]) == 3

sat_by_name = {channel["name"]: channel for channel in satellites["channels"]}
assert set(sat_by_name) == {"SAT-SO50", "SAT-AO91", "SAT-AO123"}
assert sat_by_name["SAT-SO50"]["link"]["uplink_frequency_mhz"] == 145.85
assert sat_by_name["SAT-SO50"]["link"]["downlink_frequency_mhz"] == 436.795
assert sat_by_name["SAT-AO91"]["link"]["uplink_frequency_mhz"] == 435.25
assert sat_by_name["SAT-AO91"]["link"]["downlink_frequency_mhz"] == 145.96
assert sat_by_name["SAT-AO91"]["operating_limit"] == "sunlight_only_due_to_battery"
assert sat_by_name["SAT-AO123"]["link"]["uplink_frequency_mhz"] == 145.85
assert sat_by_name["SAT-AO123"]["link"]["downlink_frequency_mhz"] == 435.4

plan = json.loads(PLAN.read_text(encoding="utf-8"))
assert plan["public_export_allowed"] is False
assert plan["internal_candidate"]["expected_memory_count"] == 48

blocks = plan["blocks"]
for index, block in enumerate(blocks):
    assert 0 <= block["start"] <= block["end"] <= 199
    if index:
        assert blocks[index - 1]["end"] < block["start"], "Blocs mémoire chevauchants"

with tempfile.TemporaryDirectory() as tmp:
    output_dir = Path(tmp)
    subprocess.run(
        [
            sys.executable,
            str(BUILDER),
            "--root",
            str(ROOT),
            "--output-dir",
            str(output_dir),
        ],
        check=True,
    )
    json_path = output_dir / "annecy-alpes-leman-v0.2-internal.json"
    csv_path = output_dir / "annecy-alpes-leman-v0.2-internal.csv"

    candidate = json.loads(json_path.read_text(encoding="utf-8"))
    with csv_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

assert candidate["status"] == "internal_candidate_not_for_publication"
assert candidate["public_export_allowed"] is False
assert candidate["memory_count"] == 48
assert len(rows) == 48
assert all(row["Duplex"] == "off" for row in rows)

by_location = {int(row["Location"]): row for row in rows}
by_name = {row["Name"]: row for row in rows}

assert by_location[0]["Name"] == "PMR01"
assert by_location[15]["Name"] == "PMR16"
assert by_location[20]["Name"] == "APRS-1448"
assert by_location[21]["Name"] == "ISS-VOICE"
assert by_location[25]["Name"] == "ISS-SSTV"
assert by_location[26]["Name"] == "SAT-SO50"
assert by_location[27]["Name"] == "SAT-AO91"
assert by_location[28]["Name"] == "SAT-AO123"
assert by_location[30]["Name"] == "CALL-VHF"
assert by_location[31]["Name"] == "CALL-UHF"
assert by_location[40]["Name"] == "01-F1ZOH"
assert by_location[58]["Name"] == "74-F5ZLV"
assert by_location[90]["Name"] == "CH-HB9G-V"
assert by_location[91]["Name"] == "CH-HB9G-U"

assert by_name["SAT-SO50"]["Frequency"] == "436.795000"
assert by_name["SAT-AO91"]["Frequency"] == "145.960000"
assert by_name["SAT-AO123"]["Frequency"] == "435.400000"

exported_frequencies = {float(row["Frequency"]) for row in rows}
for uplink_only in [145.2, 145.85, 145.99, 435.25]:
    assert uplink_only not in exported_frequencies, f"Montante exportée par erreur: {uplink_only}"

source_datasets = {
    item["channel"]["source_dataset"]
    for item in candidate["memories"]
}
assert "research/annecy-alpes-leman-v0.2/aviation-france-pre-airac-08.json" not in source_datasets
assert "research/annecy-alpes-leman-v0.2/navigation-lakes-findings.json" not in source_datasets

swiss = [
    item["channel"]
    for item in candidate["memories"]
    if item["channel"]["source_dataset"].endswith("radioamateur-switzerland-candidates.json")
]
assert len(swiss) == 2
assert all(channel["verification"] == "verified_current" for channel in swiss)

print("Tests Annecy–Alpes–Léman internal candidate: OK")
