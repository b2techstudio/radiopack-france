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
AVIATION_FRANCE = RESEARCH / "aviation-france-airac-08.json"
AVIATION_SWITZERLAND = RESEARCH / "aviation-switzerland-airac-08.json"
PLAN = RESEARCH / "memory-plan.json"

for path in [BUILDER, SATELLITES, AVIATION_FRANCE, AVIATION_SWITZERLAND, PLAN]:
    assert path.is_file(), f"Fichier Sprint 13 manquant: {path.relative_to(ROOT)}"

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
assert plan["internal_candidate"]["expected_memory_count"] == 65

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
assert candidate["memory_count"] == 65
assert len(rows) == 65
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
assert by_location[125]["Name"] == "ANNCY-TWR"
assert by_location[126]["Name"] == "ANNMS-A-A"
assert by_location[127]["Name"] == "CHAM-INFO"
assert by_location[128]["Name"] == "CHAM-APP"
assert by_location[129]["Name"] == "CHAM-TWR"
assert by_location[130]["Name"] == "CHAM-ATIS"
assert by_location[131]["Name"] == "VERSD-A-A"
assert by_location[132]["Name"] == "GREN-GND"
assert by_location[133]["Name"] == "GREN-TWR"
assert by_location[134]["Name"] == "GREN-ATIS"
assert by_location[135]["Name"] == "GENEV-INFO"
assert by_location[155]["Name"] == "CH-LSGLAD"
assert by_location[156]["Name"] == "CH-LSGLAP"
assert by_location[157]["Name"] == "CH-SIONGND"
assert by_location[158]["Name"] == "CH-SIONTWR"
assert by_location[159]["Name"] == "CH-SIONATI"
assert by_location[160]["Name"] == "CH-SIONAPP"

assert by_name["SAT-SO50"]["Frequency"] == "436.795000"
assert by_name["SAT-AO91"]["Frequency"] == "145.960000"
assert by_name["SAT-AO123"]["Frequency"] == "435.400000"
assert by_name["ANNCY-TWR"]["Frequency"] == "118.200000"
assert by_name["ANNMS-A-A"]["Frequency"] == "125.875000"
assert by_name["CHAM-INFO"]["Frequency"] == "123.700000"
assert by_name["CHAM-APP"]["Frequency"] == "121.205000"
assert by_name["CHAM-TWR"]["Frequency"] == "118.300000"
assert by_name["CHAM-ATIS"]["Frequency"] == "127.100000"
assert by_name["VERSD-A-A"]["Frequency"] == "121.000000"
assert by_name["GREN-GND"]["Frequency"] == "121.930000"
assert by_name["GREN-TWR"]["Frequency"] == "119.300000"
assert by_name["GREN-ATIS"]["Frequency"] == "133.855000"
assert by_name["GENEV-INFO"]["Frequency"] == "126.350000"
assert by_name["CH-LSGLAD"]["Frequency"] == "123.205000"
assert by_name["CH-LSGLAP"]["Frequency"] == "118.830000"
assert by_name["CH-SIONGND"]["Frequency"] == "121.705000"
assert by_name["CH-SIONTWR"]["Frequency"] == "118.275000"
assert by_name["CH-SIONATI"]["Frequency"] == "130.630000"
assert by_name["CH-SIONAPP"]["Frequency"] == "126.825000"

aviation_names = [
    "ANNCY-TWR", "ANNMS-A-A", "CHAM-INFO", "CHAM-APP", "CHAM-TWR",
    "CHAM-ATIS", "VERSD-A-A", "GREN-GND", "GREN-TWR", "GREN-ATIS",
    "GENEV-INFO", "CH-LSGLAD", "CH-LSGLAP", "CH-SIONGND", "CH-SIONTWR",
    "CH-SIONATI", "CH-SIONAPP",
]
assert all(by_name[name]["Mode"] == "AM" for name in aviation_names)
assert all(by_name[name]["TStep"] == "8.33" for name in aviation_names)

exported_frequencies = {float(row["Frequency"]) for row in rows}
for uplink_only in [145.2, 145.85, 145.99, 435.25]:
    assert uplink_only not in exported_frequencies, f"Montante exportée par erreur: {uplink_only}"
for excluded_sion in [131.475, 131.67, 131.955, 110.7, 112.15]:
    assert excluded_sion not in exported_frequencies, f"Fréquence Sion exclue exportée: {excluded_sion}"

source_datasets = {
    item["channel"]["source_dataset"]
    for item in candidate["memories"]
}
assert "research/annecy-alpes-leman-v0.2/aviation-france-pre-airac-08.json" not in source_datasets
assert "research/annecy-alpes-leman-v0.2/navigation-lakes-findings.json" not in source_datasets
assert "research/annecy-alpes-leman-v0.2/aviation-france-airac-08.json" in source_datasets
assert "research/annecy-alpes-leman-v0.2/aviation-switzerland-airac-08.json" in source_datasets

swiss_ham = [
    item["channel"]
    for item in candidate["memories"]
    if item["channel"]["source_dataset"].endswith("radioamateur-switzerland-candidates.json")
]
assert len(swiss_ham) == 2
assert all(channel["verification"] == "verified_current" for channel in swiss_ham)

fr_aviation = [
    item["channel"]
    for item in candidate["memories"]
    if item["channel"]["source_dataset"].endswith("aviation-france-airac-08.json")
]
assert len(fr_aviation) == 11
assert all(channel["verification"] == "verified_airac08_public" for channel in fr_aviation)

ch_aviation = [
    item["channel"]
    for item in candidate["memories"]
    if item["channel"]["source_dataset"].endswith("aviation-switzerland-airac-08.json")
]
assert len(ch_aviation) == 6
assert all(channel["verification"] == "verified_current_public" for channel in ch_aviation)

print("Tests Annecy–Alpes–Léman internal candidate: OK")
