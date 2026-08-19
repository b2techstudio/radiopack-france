import argparse
import csv
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--dist", type=Path, default=Path("website/dist"))
args = parser.parse_args()

csv_path = args.dist / "downloads/bourgogne-franche-comte/radiopack-france-bourgogne-franche-comte-v0.3.csv"
assert csv_path.is_file(), f"Missing built BFC v0.3 CSV: {csv_path}"
raw = csv_path.read_bytes()
sha256 = hashlib.sha256(raw).hexdigest()
expected_sha = "b5af25a6766b1181e735d376d3f70ab47ffb9ed67b9e38e35bee15e8a86ae7a5"
assert sha256 == expected_sha, (sha256, expected_sha)

record_path = Path("research/bourgogne-franche-comte-v0.3/publication-record.json")
record = json.loads(record_path.read_text(encoding="utf-8"))
assert record["status"] == "published_immutable"
assert record["memory_count"] == 54
assert record["public_csv_sha256"] == sha256
assert record["published_version_is_immutable"] is True

with csv_path.open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))

assert len(rows) == 54, len(rows)
assert len({int(row["Location"]) for row in rows}) == 54
assert len({row["Name"] for row in rows}) == 54
assert len({round(float(row["Frequency"]), 6) for row in rows}) == 54
assert all(row["Duplex"] == "off" for row in rows)
assert all(row["Offset"] == "0.000000" for row in rows)

by_name = {row["Name"]: row for row in rows}
expected_new = {
    "F5ZIQ-V": 145.45, "F5ZIQ-U": 432.55,
    "F5ZVA-V": 145.25, "F5ZVA-U": 431.25,
    "F5ZFQ-V": 145.2625, "F5ZFQ-U": 430.125,
    "F1ZCA-A": 430.3, "F1ZCA-B": 431.9,
    "F5ZXZ-V": 145.2125, "F5ZXZ-U": 431.1,
    "VEZE-AFIS": 122.205,
    "SY-APP1": 119.505, "SY-APP2": 123.405,
    "SY-GND": 121.805, "SY-TWR": 122.3, "SY-ATIS": 132.48,
    "CHAL-INFO": 118.605,
}
for name, frequency in expected_new.items():
    assert name in by_name, name
    assert round(float(by_name[name]["Frequency"]), 6) == round(frequency, 6)

for name in ["VEZE-AFIS", "SY-APP1", "SY-APP2", "SY-GND", "SY-TWR", "SY-ATIS", "CHAL-INFO"]:
    assert by_name[name]["Mode"] == "AM"

print(f"BFC v0.3 built CSV: 54 RX, immutable SHA-256 matches publication record; BFC_V03_SHA256={sha256}")
