import argparse
import csv
import hashlib
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--dist", type=Path, default=Path("website/dist"))
args = parser.parse_args()

csv_path = args.dist / "downloads/centre-val-de-loire/radiopack-france-centre-val-de-loire-v0.3.csv"
assert csv_path.is_file(), f"Missing built Centre v0.3 CSV: {csv_path}"
raw = csv_path.read_bytes()
sha256 = hashlib.sha256(raw).hexdigest()

with csv_path.open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))

assert len(rows) == 51, len(rows)
assert len({int(row["Location"]) for row in rows}) == 51
assert len({row["Name"] for row in rows}) == 51
assert len({round(float(row["Frequency"]), 6) for row in rows}) == 51
assert all(row["Duplex"] == "off" for row in rows)
assert all(row["Offset"] == "0.000000" for row in rows)

by_name = {row["Name"]: row for row in rows}
expected = {
    "CHR-TWR1": 125.88,
    "SDH-AFIS": 122.405,
    "F5ZSQ-O": 430.275,
    "F5ZSQ-I": 431.875,
    "F5ZXW-V": 145.2875,
    "F5ZXW-U": 431.0875,
    "F6ZAW-V": 145.575,
    "F6ZAW-U": 433.5375,
    "F5ZUZ-O": 430.3375,
    "F5ZUZ-I": 439.7375,
    "F5ZAP-O": 430.375,
    "F5ZAP-I": 439.775,
    "F1ZFY-O": 433.3,
    "F1ZFY-I": 434.9,
}
for name, frequency in expected.items():
    assert name in by_name, name
    assert round(float(by_name[name]["Frequency"]), 6) == round(frequency, 6)

assert "F5ZQY-O" not in by_name and "F5ZQY-I" not in by_name
assert "F5ZNX-O" not in by_name and "F5ZNX-I" not in by_name
assert all(round(float(row["Frequency"]), 6) != 125.875 for row in rows)
assert len([row for row in rows if row["Mode"] == "AM"]) == 7

print(f"Centre-Val de Loire v0.3 built CSV: 51 RX, revised AIRAC and analog paired-RX scope OK; CENTRE_V03_SHA256={sha256}")
