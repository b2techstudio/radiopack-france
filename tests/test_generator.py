import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(ROOT / "generator/generate_chirp_csv.py"), "--root", str(ROOT)], check=True)

for relative in [
    "website/public/downloads/national/radiopack-france-pmr446-rx.csv",
    "website/public/downloads/normandie/radiopack-france-normandie-preview.csv",
]:
    path = ROOT / relative
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 16, (relative, len(rows))
    assert rows[0]["Frequency"] == "446.006250"
    assert rows[-1]["Frequency"] == "446.193750"
    assert all(row["Duplex"] == "off" for row in rows)
    assert all(row["Mode"] == "NFM" for row in rows)
    assert all(row["TStep"] == "12.50" for row in rows)
print("Tests RadioPack Sprint 2: OK")
