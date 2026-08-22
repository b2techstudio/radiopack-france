#!/usr/bin/env python3
import argparse
import csv
import hashlib
import io
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.build_bfc_v04_candidate import (
    EXPECTED_BASE_COUNT,
    EXPECTED_BASE_SHA,
    EXPECTED_CANDIDATE_COUNT,
    EXPECTED_INLAND_COUNT,
    INLAND_LOCATION_START,
    ROOT,
    VALIDATION,
    build,
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--dist",
    type=Path,
    default=REPO_ROOT / "website" / "dist",
    help="Astro production dist directory",
)
args = parser.parse_args()

base_csv = args.dist / "downloads" / "bourgogne-franche-comte" / "radiopack-france-bourgogne-franche-comte-v0.3.csv"
candidate, manifest = build(ROOT, base_csv)
rows = list(csv.DictReader(io.StringIO(candidate.decode("utf-8"), newline="")))
base_rows = list(csv.DictReader(io.StringIO(base_csv.read_text(encoding="utf-8"), newline="")))

assert manifest["status"] == "internal_candidate_reproducible"
assert manifest["pack"] == "Bourgogne-Franche-Comté"
assert manifest["target_version"] == "0.4"
assert manifest["published_base_version"] == "0.3"
assert manifest["published_base_memory_count"] == EXPECTED_BASE_COUNT == 54
assert manifest["published_base_sha256"] == EXPECTED_BASE_SHA
assert manifest["candidate_memory_count"] == EXPECTED_CANDIDATE_COUNT == 61
assert manifest["candidate_inland_vhf_memory_count"] == EXPECTED_INLAND_COUNT == 7
assert manifest["candidate_memory_delta"] == 7
assert manifest["public_export_allowed"] is False
assert manifest["published"] is False
assert manifest["immutable"] is False
assert manifest["candidate_sha256"] == hashlib.sha256(candidate).hexdigest()
assert manifest["validation"]["public_base_sha_matches_frozen_record"] is True
assert manifest["validation"]["base_rows_preserved"] is True

assert len(rows) == 61
assert all(row["Duplex"] == "off" for row in rows)
assert all(row["Offset"] == "0.000000" for row in rows)
assert len({row["Frequency"] for row in rows}) == 61
assert len({row["Name"] for row in rows}) == 61
assert len({row["Location"] for row in rows}) == 61
assert max(int(row["Location"]) for row in rows) <= 199

candidate_base_rows = [row for row in rows if int(row["Location"]) < INLAND_LOCATION_START]
assert candidate_base_rows == base_rows
assert hashlib.sha256(base_csv.read_bytes()).hexdigest() == EXPECTED_BASE_SHA

inland = [row for row in rows if int(row["Location"]) >= INLAND_LOCATION_START]
assert len(inland) == 7
assert {int(row["Location"]) for row in inland} == set(range(120, 127))
assert {row["Name"] for row in inland} == {
    "FLV10", "FLV12", "FL20-B", "FL20-T", "FL22-B", "FL22-T", "FLV69",
}
assert {row["Frequency"] for row in inland} == {
    "156.500000", "156.600000", "157.000000", "161.600000",
    "157.100000", "161.700000", "156.475000",
}
assert "156.900000" not in {row["Frequency"] for row in inland}
assert "161.500000" not in {row["Frequency"] for row in inland}

validation = json.loads((ROOT / VALIDATION).read_text(encoding="utf-8"))
assert validation["scope"]["memory_count"] == 7
assert validation["scope"]["candidate_memory_count"] == 61
assert validation["scope"]["channel_18_added"] is False
assert validation["gates"]["public_export_allowed"] is False
assert validation["gates"]["public_release_allowed"] is False

print(
    "BFC v0.4 internal candidate: "
    f"61 RX / +7 inland VHF / sha256={manifest['candidate_sha256']} / public=false"
)
