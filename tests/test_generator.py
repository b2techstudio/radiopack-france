import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
subprocess.run(
    [sys.executable, str(ROOT / "generator/generate_chirp_csv.py"), "--root", str(ROOT)],
    check=True,
)

expected = {
    "website/public/downloads/national/radiopack-france-pmr446-rx.csv": 16,
    "website/public/downloads/national/radiopack-france-marine-vhf-rx.csv": 90,
    "website/public/downloads/national/radiopack-france-amateur-listening-rx.csv": 6,
    "website/public/downloads/national/radiopack-france-amateur-calls-rx.csv": 2,
    "website/public/downloads/normandie/radiopack-france-normandie-repeaters-rx.csv": 15,
    "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv": 139,
    "website/public/downloads/annecy-haute-savoie/radiopack-france-annecy-haute-savoie-repeaters-rx.csv": 9,
    "website/public/downloads/annecy-haute-savoie/radiopack-france-annecy-haute-savoie-v0.1.csv": 36,
}

loaded = {}
for relative, expected_count in expected.items():
    path = ROOT / relative
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    loaded[relative] = rows
    assert len(rows) == expected_count, (relative, len(rows), expected_count)
    assert all(row["Duplex"] == "off" for row in rows)
    assert len({row["Name"] for row in rows}) == len(rows)
    assert all(len(row["Name"]) <= 10 for row in rows)

iss_dataset = json.loads(
    (ROOT / "data/national/amateur-listening-rx.json").read_text(encoding="utf-8")
)
iss_channels = {
    channel["name"]: channel
    for channel in iss_dataset["channels"]
    if channel["name"].startswith("ISS-")
}

for name, channel in iss_channels.items():
    assert channel["tx_policy"] == "rx_only", name
    assert float(channel["frequency_mhz"]) == float(channel["link"]["downlink_frequency_mhz"]), name

voice = iss_channels["ISS-VOICE"]
assert voice["link"]["type"] == "split"
assert float(voice["link"]["uplink_frequency_mhz"]) == 145.2
assert float(voice["link"]["downlink_frequency_mhz"]) == 145.8
assert "Region 1" in voice["link"]["uplink_region"]

repeater = iss_channels["ISS-REP"]
assert repeater["link"]["type"] == "crossband_split"
assert float(repeater["link"]["uplink_frequency_mhz"]) == 145.99
assert float(repeater["link"]["uplink_ctcss_hz"]) == 67.0
assert float(repeater["link"]["downlink_frequency_mhz"]) == 437.8

for packet_name, frequency in [("ISS-PKT-V", 145.825), ("ISS-PKT-U", 437.825)]:
    packet = iss_channels[packet_name]
    assert packet["link"]["type"] == "same_frequency_bidirectional"
    assert float(packet["link"]["uplink_frequency_mhz"]) == frequency
    assert float(packet["link"]["downlink_frequency_mhz"]) == frequency

sstv = iss_channels["ISS-SSTV"]
assert sstv["link"]["type"] == "downlink_only_broadcast"
assert "uplink_frequency_mhz" not in sstv["link"]
assert float(sstv["link"]["downlink_frequency_mhz"]) == 437.55

listening = loaded["website/public/downloads/national/radiopack-france-amateur-listening-rx.csv"]
listening_by_name = {row["Name"]: row for row in listening}
exported_frequencies = {float(row["Frequency"]) for row in listening}

assert listening_by_name["ISS-VOICE"]["Frequency"] == "145.800000"
assert listening_by_name["ISS-REP"]["Frequency"] == "437.800000"
assert listening_by_name["ISS-PKT-V"]["Frequency"] == "145.825000"
assert listening_by_name["ISS-PKT-U"]["Frequency"] == "437.825000"
assert listening_by_name["ISS-SSTV"]["Frequency"] == "437.550000"
assert 145.2 not in exported_frequencies
assert 145.99 not in exported_frequencies
assert "montée Région 1 sur 145.200" in listening_by_name["ISS-VOICE"]["Comment"]
assert "montée 145.990 CTCSS 67 Hz" in listening_by_name["ISS-REP"]["Comment"]

normandie = loaded["website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv"]
normandie_by_name = {row["Name"]: row for row in normandie}
normandie_by_location = {int(row["Location"]): row for row in normandie}

assert len(normandie) == 139
assert max(normandie_by_location) == 174
assert normandie_by_name["53-F6ZCE"]["Frequency"] == "145.700000"
assert normandie_by_location[174]["Name"] == "53-F6ZCE"

annecy = loaded["website/public/downloads/annecy-haute-savoie/radiopack-france-annecy-haute-savoie-v0.1.csv"]
annecy_by_name = {row["Name"]: row for row in annecy}
annecy_by_location = {int(row["Location"]): row for row in annecy}

assert len(annecy) == 36
assert min(annecy_by_location) == 0
assert max(annecy_by_location) == 58
assert 16 not in annecy_by_location
assert 19 not in annecy_by_location
assert 26 not in annecy_by_location
assert 29 not in annecy_by_location
assert 32 not in annecy_by_location
assert 39 not in annecy_by_location
assert 43 not in annecy_by_location
assert 49 not in annecy_by_location
assert 59 not in annecy_by_location

assert annecy_by_location[0]["Name"] == "PMR01"
assert annecy_by_location[20]["Name"] == "APRS-1448"
assert annecy_by_location[30]["Name"] == "CALL-VHF"
assert annecy_by_location[40]["Name"] == "AIR-EMERG"
assert annecy_by_location[41]["Name"] == "ANNCY-TWR"
assert annecy_by_location[42]["Name"] == "ANNMS-AA"
assert annecy_by_location[50]["Name"] == "74-F5ZLV"

assert annecy_by_name["ANNCY-TWR"]["Frequency"] == "118.200000"
assert annecy_by_name["ANNMS-AA"]["Frequency"] == "125.875000"
assert annecy_by_name["74-F5ZLV"]["Frequency"] == "145.412500"
assert annecy_by_name["ALP43265"]["Frequency"] == "432.650000"
assert annecy_by_name["01-F1ZOH"]["Frequency"] == "430.225000"
assert annecy_by_name["01-F1ZPY"]["Frequency"] == "430.150000"
assert annecy_by_name["01-F6ZJD"]["Frequency"] == "145.637500"
assert annecy_by_name["73-F1ZHE"]["Frequency"] == "145.262500"
assert annecy_by_name["73-F1ZHG"]["Frequency"] == "145.287500"
assert annecy_by_name["ALP43251"]["Frequency"] == "432.512500"
assert annecy_by_name["73-F5ZGT"]["Frequency"] == "145.450000"
assert annecy_by_name["ANNCY-TWR"]["Mode"] == "AM"
assert annecy_by_name["74-F5ZLV"]["Mode"] == "NFM"

radioamateur_names = {
    row["Name"] for row in annecy
    if 20 <= int(row["Location"]) <= 31 or 50 <= int(row["Location"]) <= 58
}
assert len(radioamateur_names) == 17

print("Tests RadioPack ISS links and Sprint 5: OK")
