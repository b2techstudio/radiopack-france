import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research/annecy-alpes-leman-v0.2"

FRANCE = RESEARCH / "aviation-france-airac-08.json"
SWITZERLAND = RESEARCH / "aviation-switzerland-airac-08.json"
PREVIOUS = RESEARCH / "aviation-france-pre-airac-08.json"

for path in [FRANCE, SWITZERLAND, PREVIOUS]:
    assert path.is_file(), f"Fichier aviation manquant: {path.relative_to(ROOT)}"

france = json.loads(FRANCE.read_text(encoding="utf-8"))
switzerland = json.loads(SWITZERLAND.read_text(encoding="utf-8"))
previous = json.loads(PREVIOUS.read_text(encoding="utf-8"))

assert france["production_ready"] is False
assert france["internal_candidate_allowed"] is True
assert france["cycle"]["validation_cycle"] == "AIRAC 08/26"
assert france["cycle"]["effective_from"] == "2026-08-06"
assert france["cycle"]["effective_until_inclusive"] == "2026-09-02"

fr_channels = france["channels"]
assert len(fr_channels) == 7
assert all(
    channel["verification"] == "verified_airac08_public"
    for channel in fr_channels
)
assert all(channel["mode"] == "AM" for channel in fr_channels)
assert all(channel["step_khz"] == 8.33 for channel in fr_channels)
assert all(channel["tx_policy"] == "rx_only" for channel in fr_channels)

fr_by_name = {channel["name"]: channel for channel in fr_channels}
assert set(fr_by_name) == {
    "ANNCY-TWR",
    "ANNMS-A-A",
    "VERSD-A-A",
    "GREN-GND",
    "GREN-TWR",
    "GREN-ATIS",
    "GENEV-INFO",
}
assert fr_by_name["ANNCY-TWR"]["frequency_mhz"] == 118.2
assert fr_by_name["ANNMS-A-A"]["frequency_mhz"] == 125.875
assert fr_by_name["VERSD-A-A"]["frequency_mhz"] == 121.0
assert fr_by_name["GREN-GND"]["frequency_mhz"] == 121.93
assert fr_by_name["GREN-TWR"]["frequency_mhz"] == 119.3
assert fr_by_name["GREN-ATIS"]["frequency_mhz"] == 133.855
assert fr_by_name["GENEV-INFO"]["frequency_mhz"] == 126.35

pending_fr = {item["icao"] for item in france["pending"]}
assert pending_fr == {"LFLB", "LFKA", "LFHM"}
assert {item["icao"] for item in france["excluded"]} == {"LFHZ"}
sallanches = france["excluded"][0]
assert sallanches["status"] == "excluded_closed_aerodrome"
assert sallanches["effective_from"] == "2020-09-01"
assert "LEGIFRANCE-LFHZ-CLOSED-2020" in sallanches["source_ids"]
assert all(
    channel["verification"] == "pre_airac_recheck"
    for channel in previous["channels"]
)

assert switzerland["production_ready"] is False
assert switzerland["internal_candidate_allowed"] is True
assert switzerland["cycle"]["aip_airac_amdt_effective"] == "2026-08-06"

ch_channels = switzerland["channels"]
assert len(ch_channels) == 6
assert all(
    channel["verification"] == "verified_current_public"
    for channel in ch_channels
)
assert all(channel["mode"] == "AM" for channel in ch_channels)
assert all(channel["step_khz"] == 8.33 for channel in ch_channels)
assert all(channel["tx_policy"] == "rx_only" for channel in ch_channels)

ch_by_name = {channel["name"]: channel for channel in ch_channels}
assert set(ch_by_name) == {
    "CH-LSGLAD",
    "CH-LSGLAP",
    "CH-SIONGND",
    "CH-SIONTWR",
    "CH-SIONATI",
    "CH-SIONAPP",
}
assert ch_by_name["CH-LSGLAD"]["frequency_mhz"] == 123.205
assert ch_by_name["CH-LSGLAP"]["frequency_mhz"] == 118.83
assert ch_by_name["CH-SIONGND"]["frequency_mhz"] == 121.705
assert ch_by_name["CH-SIONTWR"]["frequency_mhz"] == 118.275
assert ch_by_name["CH-SIONATI"]["frequency_mhz"] == 130.63
assert ch_by_name["CH-SIONAPP"]["frequency_mhz"] == 126.825
assert {item["icao"] for item in switzerland["pending"]} == {"LSGG"}

excluded_ch = {
    frequency
    for item in switzerland["excluded"]
    for frequency in item["frequencies_mhz"]
}
assert excluded_ch == {131.475, 131.67, 131.955, 110.7, 112.15}

all_channels = fr_channels + ch_channels
assert len({channel["frequency_mhz"] for channel in all_channels}) == len(all_channels)
assert all(len(channel["name"]) <= 10 for channel in all_channels)
assert not excluded_ch.intersection(
    {channel["frequency_mhz"] for channel in ch_channels}
)

print("Tests Annecy–Alpes–Léman AIRAC 08 aviation: OK")
