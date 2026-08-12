import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"
RECORD = ROOT / "research/bretagne-v0.2/publication-record.json"
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"

with tempfile.TemporaryDirectory() as td:
    subprocess.run([sys.executable, str(ROOT / "tools/build_bretagne_v02_internal_candidate.py"), "--root", str(ROOT), "--output-dir", td], check=True)
    candidate = Path(td) / "bretagne-v0.2-internal.csv"
    assert PUBLIC.read_bytes() == candidate.read_bytes()

with PUBLIC.open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
assert len(rows) == 151
assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
assert all(len(row["Name"]) <= 10 for row in rows)
assert len({row["Location"] for row in rows}) == 151
assert len({row["Name"] for row in rows}) == 151
assert len({round(float(row["Frequency"]), 6) for row in rows}) == 151
by_name = {row["Name"]: row for row in rows}
for name, freq in {"M64-S":156.225,"M64-C":160.825,"M79-S":156.975,"M79-C":161.575}.items():
    assert round(float(by_name[name]["Frequency"]), 6) == freq
    comment = by_name[name]["Comment"].lower()
    assert all(site not in comment for site in ["etel","corsen","fréhel","stiff","bodic"])
aviation = [row for row in rows if row["Name"].startswith(("AIR-", "RNS-", "BES-", "DIN-", "QUIM-"))]
assert len(aviation) == 16
assert all(row["Mode"] == "AM" and row["TStep"] == "8.33" for row in aviation)

record = json.loads(RECORD.read_text(encoding="utf-8"))
assert record["status"] == "published_immutable"
assert record["version"] == "0.2" and record["memory_count"] == 151
assert record["new_memory_count_vs_v0_1"] == 16
assert record["public_csv_sha256"] == hashlib.sha256(PUBLIC.read_bytes()).hexdigest()
assert record["published_version_is_immutable"] is True
assert record["aviation"]["cycle"] == "AIRAC 08/26"
assert record["aviation"]["valid_through_inclusive"] == "2026-09-02"
assert record["aviation"]["direct_xml_field_match_claimed"] is False
registry = REGISTRY.read_text(encoding="utf-8")
assert 'id: "bretagne"' in registry
assert 'memoryCount: 151' in registry
assert '/downloads/bretagne/radiopack-france-bretagne-v0.2.csv' in registry
assert (ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.1.csv").is_file()
print("Bretagne v0.2 public release: immutable 151-memory RX-only CSV exactly matches frozen candidate OK")
