import csv
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
    "website/public/downloads/normandie/radiopack-france-normandie-v0.2.csv": 122,
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

pmr = loaded["website/public/downloads/national/radiopack-france-pmr446-rx.csv"]
assert pmr[0]["Frequency"] == "446.006250"
assert pmr[-1]["Frequency"] == "446.193750"
assert all(row["Mode"] == "NFM" for row in pmr)

marine = loaded["website/public/downloads/national/radiopack-france-marine-vhf-rx.csv"]
marine_by_name = {row["Name"]: row for row in marine}
assert marine_by_name["M16"]["Frequency"] == "156.800000"
assert marine_by_name["AIS1"]["Frequency"] == "161.975000"
assert marine_by_name["AIS2"]["Frequency"] == "162.025000"
assert marine_by_name["M01-C"]["Frequency"] == "160.650000"
assert marine_by_name["M70"]["Skip"] == "S"

normandie = loaded["website/public/downloads/normandie/radiopack-france-normandie-v0.2.csv"]
normandie_by_name = {row["Name"]: row for row in normandie}
assert normandie_by_name["CAEN-TWR"]["Frequency"] == "134.530000"
assert normandie_by_name["DVL-TWR"]["Frequency"] == "118.305000"
assert normandie_by_name["CHER-AFIS"]["Frequency"] == "119.630000"
assert normandie_by_name["LEH-AFIS"]["Frequency"] == "135.205000"
assert normandie_by_name["ROUEN-TWR"]["Frequency"] == "120.200000"
assert normandie_by_name["ISS-VOICE"]["Frequency"] == "145.800000"
assert normandie_by_name["CAEN-TWR"]["Mode"] == "AM"

print("Tests RadioPack Sprint 3: OK")
