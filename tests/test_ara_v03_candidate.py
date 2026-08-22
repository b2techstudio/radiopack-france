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

from tools.build_ara_v03_candidate import (
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
parser.add_argument("--dist", type=Path, default=REPO_ROOT / "website" / "dist")
args = parser.parse_args()

base_csv = args.dist / "downloads" / "auvergne-rhone-alpes" / "radiopack-france-auvergne-rhone-alpes-v0.2.csv"
candidate, manifest = build(ROOT, base_csv)
rows = list(csv.DictReader(io.StringIO(candidate.decode("utf-8"), newline="")))
base_rows = list(csv.DictReader(io.StringIO(base_csv.read_text(encoding="utf-8"), newline="")))

assert manifest["status"] == "internal_candidate_reproducible"
assert manifest["pack"] == "Auvergne-Rhône-Alpes"
assert manifest["target_version"] == "0.3"
assert manifest["published_base_version"] == "0.2"
assert manifest["published_base_memory_count"] == EXPECTED_BASE_COUNT == 62
assert manifest["published_base_sha256"] == EXPECTED_BASE_SHA
assert manifest["candidate_memory_count"] == EXPECTED_CANDIDATE_COUNT == 71
assert manifest["candidate_inland_vhf_memory_count"] == EXPECTED_INLAND_COUNT == 9
assert manifest["candidate_memory_delta"] == 9
assert manifest["candidate_sha256"] == hashlib.sha256(candidate).hexdigest()
assert manifest["public_export_allowed"] is False
assert manifest["published"] is False
assert manifest["immutable"] is False
assert manifest["validation"]["public_base_sha_matches_frozen_record"] is True
assert manifest["validation"]["base_rows_preserved"] is True
assert manifest["validation"]["channel_18_boat_side_only"] is True

assert len(rows) == 71
assert all(row["Duplex"] == "off" for row in rows)
assert all(row["Offset"] == "0.000000" for row in rows)
assert len({row["Frequency"] for row in rows}) == 71
assert len({row["Name"] for row in rows}) == 71
assert len({row["Location"] for row in rows}) == 71
assert max(int(row["Location"]) for row in rows) <= 199
assert hashlib.sha256(base_csv.read_bytes()).hexdigest() == EXPECTED_BASE_SHA

candidate_base_rows = [row for row in rows if int(row["Location"]) < INLAND_LOCATION_START]
assert candidate_base_rows == base_rows

inland = [row for row in rows if int(row["Location"]) >= INLAND_LOCATION_START]
assert len(inland) == 9
assert {int(row["Location"]) for row in inland} == set(range(120, 129))
assert {row["Name"] for row in inland} == {
    "FLV10", "FLV12", "FLV18", "FL19-B", "FL19-T", "FL20-B", "FL20-T", "FL22-B", "FL22-T",
}
assert {row["Frequency"] for row in inland} == {
    "156.500000", "156.600000", "156.900000", "156.950000", "161.550000",
    "157.000000", "161.600000", "157.100000", "161.700000",
}
assert "161.500000" not in {row["Frequency"] for row in inland}
assert "156.800000" not in {row["Frequency"] for row in inland}

validation = json.loads((ROOT / VALIDATION).read_text(encoding="utf-8"))
assert validation["scope"]["memory_count"] == 9
assert validation["scope"]["candidate_memory_count"] == 71
assert validation["scope"]["paired_rx_channels"] == [19, 20, 22]
assert validation["scope"]["channel_18_boat_side_only"] is True
assert validation["scope"]["channel_18_shore_side_added"] is False
assert validation["scope"]["marine_channel_16_added"] is False
assert validation["gates"]["public_export_allowed"] is False
assert validation["gates"]["public_release_allowed"] is False

print(
    "ARA v0.3 internal candidate: "
    f"71 RX / +9 inland VHF / sha256={manifest['candidate_sha256']} / public=false"
)
