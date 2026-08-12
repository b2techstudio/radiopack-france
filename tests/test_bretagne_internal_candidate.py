import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "tools/build_bretagne_internal_candidate.py"
PLAN = ROOT / "research/bretagne-v0.1/memory-plan.json"

plan = json.loads(PLAN.read_text(encoding="utf-8"))
assert plan["status"] in {"internal_candidate_135_not_public", "frozen_candidate_135_prepublication_ready_not_public"}
assert plan["expected_memory_count"] == 135
assert plan["internal_candidate"]["regional_unique_memory_count"] == 21
assert plan["internal_candidate"]["regional_source_memory_count_before_national_deduplication"] == 29
assert plan["internal_candidate"]["generic_marine_memory_count"] == 90
assert plan["rules"]["generic_marine_channel_frequency_does_not_require_local_transmitter_site_claim"] is True

with tempfile.TemporaryDirectory() as tmp:
    output = Path(tmp)
    subprocess.run(
        [sys.executable, str(BUILDER), "--root", str(ROOT), "--output-dir", str(output)],
        check=True,
    )
    candidate = json.loads((output / "bretagne-v0.1-internal.json").read_text(encoding="utf-8"))
    with (output / "bretagne-v0.1-internal.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

assert candidate["status"] == "internal_candidate_not_for_publication"
assert candidate["public_export_allowed"] is False
assert candidate["memory_count"] == 135
assert candidate["regional_source_unique_frequency_count"] == 29
assert candidate["regional_new_memory_count_after_national_deduplication"] == 21
assert candidate["regional_roles_merged_into_national_memories"] == 8
assert candidate["aviation_memory_count"] == 0
assert len(rows) == 135
assert all(row["Duplex"] == "off" for row in rows)
assert all(row["Offset"] == "0.000000" for row in rows)
assert len({float(row["Frequency"]) for row in rows}) == 135
assert all(len(row["Name"]) <= 10 for row in rows)

by_name = {row["Name"]: row for row in rows}
assert by_name["PMR01"]["Location"] == "0"
assert by_name["PMR16"]["Location"] == "15"
assert by_name["M01-S"]["Location"] == "20"
assert by_name["AIS2"]["Location"] == "109"
assert by_name["APRS-1448"]["Location"] == "120"
assert by_name["ISS-SSTV"]["Location"] == "125"
assert by_name["CALL-VHF"]["Location"] == "150"
assert by_name["CALL-UHF"]["Location"] == "151"

for name, freq in {
    "M64-S": 156.225,
    "M64-C": 160.825,
    "M79-S": 156.975,
    "M79-C": 161.575,
}.items():
    assert float(by_name[name]["Frequency"]) == freq
    comment = by_name[name]["Comment"].lower()
    assert "etel" not in comment
    assert "corsen" not in comment
    assert "fréhel" not in comment
    assert "stiff" not in comment
    assert "bodic" not in comment

regional_expected = {
    "ZBX-IN": 145.075,
    "ZBX-OUT": 145.675,
    "ZEB-A": 431.075,
    "ZEB-B": 438.675,
    "ZIS-A": 145.2375,
    "X432650": 432.65,
    "ZIT-A": 145.225,
    "ZIU-A": 145.4625,
    "ZIV-A": 145.4875,
    "ZJR-A": 145.2875,
    "X145262": 145.2625,
    "ZGS-B": 431.425,
    "ZDV-B": 438.7,
    "ZZL-B": 431.375,
    "ZPE-IN": 145.1375,
    "ZPE-OUT": 145.7375,
    "ZMU-OUT": 430.325,
    "ZMU-IN": 439.725,
    "ZBZ-U": 431.2,
    "ZBZ-VA": 145.625,
    "ZBZ-VB": 145.025,
}
for name, freq in regional_expected.items():
    assert float(by_name[name]["Frequency"]) == freq
    assert int(by_name[name]["Location"]) >= 160
    assert by_name[name]["Mode"] == "NFM"

candidate_by_frequency = {
    round(float(item["channel"]["frequency_mhz"]), 6): item["channel"]
    for item in candidate["memories"]
}
for freq in [156.175, 160.775, 156.225, 160.825, 156.975, 161.575, 157.025, 161.625]:
    assert candidate_by_frequency[round(freq, 6)]["regional_roles"]

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8").lower()
assert 'id: "bretagne"' not in registry
assert not (ROOT / "website/public/downloads/bretagne").exists()

print("Bretagne v0.1 internal candidate: 135 RX-only memories, 90 generic marine + 21 regional unique after dedup, Ch64/Ch79 two memories each without invented site, public untouched OK")
