import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "generator/generate_chirp_csv.py"
subprocess.run([sys.executable, str(GENERATOR), "--root", str(ROOT)], check=True)

expected = {
    "website/public/downloads/national/radiopack-france-pmr446-rx.csv": 16,
    "website/public/downloads/national/radiopack-france-marine-vhf-rx.csv": 90,
    "website/public/downloads/national/radiopack-france-amateur-listening-rx.csv": 6,
    "website/public/downloads/national/radiopack-france-amateur-calls-rx.csv": 2,
    "website/public/downloads/normandie/radiopack-france-normandie-repeaters-rx.csv": 15,
    "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv": 139,
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

generator_source = GENERATOR.read_text(encoding="utf-8")
assert "data/regions/annecy-haute-savoie/pack.json" not in generator_source
assert "radiopack-france-annecy-haute-savoie-v0.1.csv" not in generator_source
assert "website/src/lib/annecyPack.ts" in generator_source

iss_dataset = json.loads((ROOT / "data/national/amateur-listening-rx.json").read_text(encoding="utf-8"))
iss_channels = {channel["name"]: channel for channel in iss_dataset["channels"] if channel["name"].startswith("ISS-")}
for name, channel in iss_channels.items():
    assert channel["tx_policy"] == "rx_only", name
    assert float(channel["frequency_mhz"]) == float(channel["link"]["downlink_frequency_mhz"]), name

voice = iss_channels["ISS-VOICE"]
assert float(voice["link"]["uplink_frequency_mhz"]) == 145.2
assert float(voice["link"]["downlink_frequency_mhz"]) == 145.8
repeater = iss_channels["ISS-REP"]
assert float(repeater["link"]["uplink_frequency_mhz"]) == 145.99
assert float(repeater["link"]["uplink_ctcss_hz"]) == 67.0
assert float(repeater["link"]["downlink_frequency_mhz"]) == 437.8

for packet_name, frequency in [("ISS-PKT-V", 145.825), ("ISS-PKT-U", 437.825)]:
    packet = iss_channels[packet_name]
    assert float(packet["link"]["uplink_frequency_mhz"]) == frequency
    assert float(packet["link"]["downlink_frequency_mhz"]) == frequency

sstv = iss_channels["ISS-SSTV"]
assert "uplink_frequency_mhz" not in sstv["link"]
assert float(sstv["link"]["downlink_frequency_mhz"]) == 437.55

listening = loaded["website/public/downloads/national/radiopack-france-amateur-listening-rx.csv"]
listening_by_name = {row["Name"]: row for row in listening}
exported_frequencies = {float(row["Frequency"]) for row in listening}
assert listening_by_name["ISS-VOICE"]["Frequency"] == "145.800000"
assert listening_by_name["ISS-REP"]["Frequency"] == "437.800000"
assert listening_by_name["ISS-SSTV"]["Frequency"] == "437.550000"
assert 145.2 not in exported_frequencies
assert 145.99 not in exported_frequencies

normandie = loaded["website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv"]
normandie_by_name = {row["Name"]: row for row in normandie}
normandie_by_location = {int(row["Location"]): row for row in normandie}
assert len(normandie) == 139
assert max(normandie_by_location) == 174
assert normandie_by_name["53-F6ZCE"]["Frequency"] == "145.700000"
assert normandie_by_location[174]["Name"] == "53-F6ZCE"

print("Tests RadioPack generic generator + ISS links: OK")
