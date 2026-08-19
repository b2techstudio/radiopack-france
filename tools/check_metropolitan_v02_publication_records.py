#!/usr/bin/env python3
import argparse, csv, hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--dist", type=Path, default=ROOT / "website/dist")
args = parser.parse_args()
dist = args.dist if args.dist.is_absolute() else ROOT / args.dist
manifest = json.loads((ROOT / "research/sprint-98-metropolitan-publication-manifest.json").read_text(encoding="utf-8"))
assert manifest["sprint"] == 98 and manifest["region_count"] == 11
for entry in manifest["entries"]:
    slug = entry["id"]
    csv_path = dist / entry["public_route"].lstrip("/")
    assert csv_path.is_file(), csv_path
    digest = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    assert digest == entry["sha256"]
    record = json.loads((ROOT / entry["publication_record"]).read_text(encoding="utf-8"))
    assert record["public_csv_sha256"] == digest
    with csv_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == entry["memory_count"]
    assert all(r["Duplex"] == "off" and r["Offset"] == "0.000000" for r in rows)
print("Sprint 98 metropolitan v0.2 publication records: 11 fresh-build hashes, counts and RX-only contracts OK")
