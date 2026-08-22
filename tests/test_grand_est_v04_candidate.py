#!/usr/bin/env python3
import csv
import hashlib
import io
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.build_grand_est_v04_candidate import (
    BASE_PUBLIC,
    EXPECTED_BASE_COUNT,
    EXPECTED_BASE_SHA,
    EXPECTED_CANDIDATE_COUNT,
    EXPECTED_INLAND_COUNT,
    INLAND_LOCATION_START,
    ROOT,
    build,
)

candidate, manifest = build(ROOT)
rows = list(csv.DictReader(io.StringIO(candidate.decode("utf-8"), newline="")))

assert manifest["pack"] == "Grand Est"
assert manifest["target_version"] == "0.4"
assert manifest["published_base_version"] == "0.3"
assert manifest["published_base_memory_count"] == EXPECTED_BASE_COUNT == 84
assert manifest["published_base_sha256"] == EXPECTED_BASE_SHA
assert manifest["candidate_memory_count"] == EXPECTED_CANDIDATE_COUNT == 97
assert manifest["candidate_inland_vhf_memory_count"] == EXPECTED_INLAND_COUNT == 13
assert manifest["candidate_memory_delta"] == 13
assert manifest["public_export_allowed"] is False
assert manifest["published"] is False
assert manifest["candidate_sha256"] == hashlib.sha256(candidate).hexdigest()

assert len(rows) == 97
assert all(row["Duplex"] == "off" for row in rows)
assert all(row["Offset"] == "0.000000" for row in rows)
assert len({row["Frequency"] for row in rows}) == 97
assert len({row["Name"] for row in rows}) == 97
assert len({row["Location"] for row in rows}) == 97
assert max(int(row["Location"]) for row in rows) <= 199

inland = [row for row in rows if int(row["Location"]) >= INLAND_LOCATION_START]
assert len(inland) == 13
assert {int(row["Location"]) for row in inland} == set(range(120, 133))
expected_names = {
    "FLV06", "FLV08", "FLV10", "FLV13", "FLV72", "FLV77", "STR-11",
    "FL19-B", "FL19-T", "FL20-B", "FL20-T", "FL22-B", "FL22-T",
}
assert {row["Name"] for row in inland} == expected_names
expected_rf = {
    "156.300000", "156.400000", "156.500000", "156.650000", "156.625000", "156.875000",
    "156.550000", "156.950000", "161.550000", "157.000000", "161.600000", "157.100000", "161.700000",
}
assert {row["Frequency"] for row in inland} == expected_rf
assert "156.800000" not in {row["Frequency"] for row in inland}  # no maritime ch16 in Grand Est inland block

base_raw = (ROOT / BASE_PUBLIC).read_bytes()
assert hashlib.sha256(base_raw).hexdigest() == EXPECTED_BASE_SHA

validation = json.loads((ROOT / "research/grand-est-v0.4/inland-vhf-validation-2026-08-22.json").read_text(encoding="utf-8"))
assert validation["scope"]["memory_count"] == 13
assert validation["scope"]["candidate_memory_count_if_promoted"] == 97
assert validation["scope"]["marine_channel_16_added"] is False

print(f"Grand Est v0.4 candidate: 97 RX / +13 inland VHF / sha256={manifest['candidate_sha256']} / public=false")
