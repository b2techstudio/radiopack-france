import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.1.csv"
RECORD = ROOT / "research/bretagne-v0.1/publication-record.json"
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"

with tempfile.TemporaryDirectory() as td:
    subprocess.run([sys.executable, str(ROOT / "tools/build_bretagne_internal_candidate.py"), "--root", str(ROOT), "--output-dir", td], check=True)
    candidate = Path(td) / "bretagne-v0.1-internal.csv"
    assert PUBLIC.read_bytes() == candidate.read_bytes()

with PUBLIC.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 135
assert all(r["Duplex"] == "off" and r["Offset"] == "0.000000" for r in rows)
assert all(len(r["Name"]) <= 10 for r in rows)
assert len({r["Location"] for r in rows}) == 135
assert len({r["Name"] for r in rows}) == 135
assert len({round(float(r["Frequency"]), 6) for r in rows}) == 135
by_name = {r["Name"]: r for r in rows}
for name, freq in {"M64-S":156.225,"M64-C":160.825,"M79-S":156.975,"M79-C":161.575}.items():
    assert round(float(by_name[name]["Frequency"]),6) == freq
    comment = by_name[name]["Comment"].lower()
    assert all(site not in comment for site in ["etel","corsen","fréhel","stiff","bodic"])

record = json.loads(RECORD.read_text(encoding="utf-8"))
assert record["status"] == "published_immutable"
assert record["version"] == "0.1" and record["memory_count"] == 135
assert record["public_csv_sha256"] == hashlib.sha256(PUBLIC.read_bytes()).hexdigest()
assert record["published_version_is_immutable"] is True
assert len(record["deferred_to_v0_2"]) == 4

# v0.1 remains immutable and downloadable from the repository even after v0.2 becomes current.
registry = REGISTRY.read_text(encoding="utf-8")
assert 'id: "bretagne"' in registry
state = json.loads((ROOT / "research/project-resume-state.json").read_text(encoding="utf-8"))
if state["current_sprint"] < 80:
    assert 'memoryCount: 135' in registry
    assert '/downloads/bretagne/radiopack-france-bretagne-v0.1.csv' in registry
else:
    assert state["public_packs"]["bretagne"]["version"] == "0.2"
    assert state["public_packs"]["bretagne"]["memory_count"] == 151
    assert 'memoryCount: 151' in registry
    assert '/downloads/bretagne/radiopack-france-bretagne-v0.2.csv' in registry
assert PUBLIC.is_file()
assert (ROOT / "website/src/pages/regions/bretagne.astro").is_file()
print("Bretagne v0.1 public release: immutable 135-memory RX-only historical CSV still exactly matches reviewed candidate after later Bretagne publication OK")
