#!/usr/bin/env python3
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "research/annecy-alpes-leman-v0.4/compatibility-and-source-review.json"
BUILDER = ROOT / "tools/build_annecy_v04_candidate.py"
BASE_FULL = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv"
BASE_NO_AIR = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv"
PUB_FULL = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.4.csv"
PUB_NO_AIR = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.4-sans-aviation.csv"
PUB_RECORD = ROOT / "research/annecy-alpes-leman-v0.4/publication-record.json"


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert sha(BASE_FULL) == "fa4095c0af9b4fa5758449e09c9a32eb5c7cc103e0d90b7c9da8e74c77796af7"
assert sha(BASE_NO_AIR) == "e639aff0d045e5a20db3b03fb6175b68452700b4b6ee2e1edf78e9510c2eb649"
review = json.loads(REVIEW.read_text(encoding="utf-8"))
assert review["decision"]["stock_uvk5_receive_baseline_cleared"] is True
assert review["decision"]["chirp_stock_driver_memory_band_cleared"] is True
assert review["decision"]["current_public_rf_source_cleared"] is True
assert review["candidate_frequency_mhz"] == 50.5375

with tempfile.TemporaryDirectory(prefix="annecy-v04-") as td:
    subprocess.run([sys.executable, str(BUILDER), "--output-dir", td], cwd=ROOT, check=True)
    full = Path(td) / "radiopack-france-annecy-alpes-leman-v0.4.csv"
    noair = Path(td) / "radiopack-france-annecy-alpes-leman-v0.4-sans-aviation.csv"
    with full.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    with noair.open(encoding="utf-8", newline="") as f:
        rows_noair = list(csv.DictReader(f))
    assert len(rows) == 77 and len(rows_noair) == 60
    for variant in (rows, rows_noair):
        zth = [row for row in variant if row["Name"] == "ZTH-6M"]
        assert len(zth) == 1
        assert zth[0]["Frequency"] == "50.537500"
        assert zth[0]["Mode"] == "FM"
        assert zth[0]["Duplex"] == "off" and zth[0]["Offset"] == "0.000000"
        assert len({round(float(row["Frequency"]), 6) for row in variant}) == len(variant)
        assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in variant)
    if PUB_RECORD.exists():
        record = json.loads(PUB_RECORD.read_text(encoding="utf-8"))
        assert record["status"] == "published_immutable"
        assert PUB_FULL.is_file() and PUB_NO_AIR.is_file()
        assert sha(PUB_FULL) == sha(full) == record["public_files"]["full"]["sha256"]
        assert sha(PUB_NO_AIR) == sha(noair) == record["public_files"]["without_aviation"]["sha256"]
    else:
        assert not PUB_FULL.exists() and not PUB_NO_AIR.exists()

print("Sprint 89 Annecy v0.4: stock UV-K5/CHIRP 50 MHz gate cleared; deterministic 77/60 RX candidate OK")
