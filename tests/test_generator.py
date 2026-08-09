import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "generator/generate_chirp_csv.py"

expected = {
    "website/public/downloads/national/radiopack-france-pmr446-rx.csv": 16,
    "website/public/downloads/national/radiopack-france-marine-vhf-rx.csv": 90,
    "website/public/downloads/national/radiopack-france-amateur-listening-rx.csv": 6,
    "website/public/downloads/national/radiopack-france-amateur-calls-rx.csv": 2,
    "website/public/downloads/normandie/radiopack-france-normandie-repeaters-rx.csv": 15,
    "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv": 139,
}

published_before = {
    relative: (ROOT / relative).read_bytes()
    for relative in expected
}

loaded = {}
with tempfile.TemporaryDirectory(prefix="radiopack-generator-test-") as temporary:
    output_root = Path(temporary)
    subprocess.run(
        [
            sys.executable,
            str(GENERATOR),
            "--root",
            str(ROOT),
            "--output-root",
            str(output_root),
        ],
        check=True,
    )

    for relative, expected_count in expected.items():
        generated_path = output_root / relative
        published_path = ROOT / relative
        assert generated_path.is_file(), f"Sortie isolée manquante: {relative}"

        with generated_path.open(encoding="utf-8", newline="") as handle:
            generated_rows = list(csv.DictReader(handle))
        with published_path.open(encoding="utf-8", newline="") as handle:
            published_rows = list(csv.DictReader(handle))

        assert generated_rows == published_rows, f"La génération diverge du CSV publié: {relative}"
        loaded[relative] = generated_rows
        assert len(generated_rows) == expected_count, (relative, len(generated_rows), expected_count)
        assert all(row["Duplex"] == "off" for row in generated_rows)
        assert len({row["Name"] for row in generated_rows}) == len(generated_rows)
        assert all(len(row["Name"]) <= 10 for row in generated_rows)

for relative, original_bytes in published_before.items():
    assert (ROOT / relative).read_bytes() == original_bytes, f"Le test a modifié un fichier suivi: {relative}"

generator_source = GENERATOR.read_text(encoding="utf-8")
assert '"--output-root"' in generator_source
assert "output_root / output_relative" in generator_source
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

print("Tests RadioPack isolated generator + ISS links: OK")
