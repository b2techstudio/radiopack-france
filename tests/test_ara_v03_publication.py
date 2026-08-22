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
    build,
)

EXPECTED_CANDIDATE_SHA = "b44a95486af5fd89fa72246ed7c8f0ab79e3084f6b0429df5215fba9918d691e"
FREEZE = ROOT / "research/auvergne-rhone-alpes-v0.3/candidate-freeze.json"
RELEASE_SCOPE = ROOT / "research/auvergne-rhone-alpes-v0.3/release-scope.json"
PUBLICATION_GATES = ROOT / "research/auvergne-rhone-alpes-v0.3/publication-gates.json"
PUBLICATION_RECORD = ROOT / "research/auvergne-rhone-alpes-v0.3/publication-record.json"
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"
REGIONS = ROOT / "website/src/data/regions.json"
REGION_PAGE = ROOT / "website/src/pages/regions/[slug].astro"
PUBLIC_ROUTE = ROOT / "website/src/pages/downloads/auvergne-rhone-alpes/radiopack-france-auvergne-rhone-alpes-v0.3.csv.ts"
PACK_BUILDER = ROOT / "website/src/lib/araPack.ts"

parser = argparse.ArgumentParser()
parser.add_argument("--dist", type=Path, default=REPO_ROOT / "website" / "dist")
args = parser.parse_args()

base_csv = args.dist / "downloads" / "auvergne-rhone-alpes" / "radiopack-france-auvergne-rhone-alpes-v0.2.csv"
public_v03_csv = args.dist / "downloads" / "auvergne-rhone-alpes" / "radiopack-france-auvergne-rhone-alpes-v0.3.csv"

for path in [FREEZE, RELEASE_SCOPE, PUBLICATION_GATES, PUBLICATION_RECORD, REGISTRY, REGIONS, REGION_PAGE, PUBLIC_ROUTE, PACK_BUILDER]:
    assert path.is_file(), f"Missing Sprint 109 publication dependency: {path.relative_to(ROOT)}"

candidate, manifest = build(ROOT, base_csv)
candidate_sha = hashlib.sha256(candidate).hexdigest()
assert candidate_sha == EXPECTED_CANDIDATE_SHA
assert manifest["candidate_memory_count"] == EXPECTED_CANDIDATE_COUNT == 71
assert manifest["candidate_inland_vhf_memory_count"] == EXPECTED_INLAND_COUNT == 9
assert manifest["published_base_memory_count"] == EXPECTED_BASE_COUNT == 62
assert manifest["published_base_sha256"] == EXPECTED_BASE_SHA

freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
assert freeze["status"] == "internal_candidate_frozen_not_public"
assert freeze["candidate_sha256"] == EXPECTED_CANDIDATE_SHA
assert freeze["candidate_memory_count"] == 71
assert freeze["public_release_allowed"] is False
assert freeze["published"] is False

assert public_v03_csv.is_file(), "Astro did not produce the ARA v0.3 public CSV"
public_bytes = public_v03_csv.read_bytes()
public_sha = hashlib.sha256(public_bytes).hexdigest()
assert public_bytes == candidate, "ARA v0.3 public CSV differs byte-for-byte from frozen Sprint 108 candidate"
assert public_sha == EXPECTED_CANDIDATE_SHA

rows = list(csv.DictReader(io.StringIO(public_bytes.decode("utf-8"), newline="")))
base_rows = list(csv.DictReader(io.StringIO(base_csv.read_text(encoding="utf-8"), newline="")))
assert len(rows) == 71
assert len(base_rows) == 62
assert hashlib.sha256(base_csv.read_bytes()).hexdigest() == EXPECTED_BASE_SHA
assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
assert len({row["Frequency"] for row in rows}) == 71
assert len({row["Name"] for row in rows}) == 71
assert len({row["Location"] for row in rows}) == 71
assert max(int(row["Location"]) for row in rows) <= 199

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

scope = json.loads(RELEASE_SCOPE.read_text(encoding="utf-8"))
assert scope["status"] == "published_immutable"
assert scope["version"] == "0.3"
assert scope["based_on_public_version"] == "0.2"
assert scope["base_memory_count"] == 62
assert scope["base_public_sha256"] == EXPECTED_BASE_SHA
assert scope["memory_count"] == 71
assert scope["memory_delta"] == 9
assert scope["aviation_memory_count"] == 18
assert scope["aviation_memory_delta"] == 0
assert scope["inland_vhf_memory_count"] == 9
assert scope["candidate_sha256"] == EXPECTED_CANDIDATE_SHA
assert scope["public_csv_sha256"] == EXPECTED_CANDIDATE_SHA
assert scope["inland_scope"]["paired_rx_channels"] == [19, 20, 22]
assert scope["inland_scope"]["channel_18_boat_side_only"] is True
assert scope["inland_scope"]["channel_18_shore_side_added"] is False
assert scope["inland_scope"]["marine_channel_16_added"] is False
assert scope["publication"]["public_release_allowed"] is True
assert scope["publication"]["candidate_public_byte_identity_verified"] is True
assert scope["publication"]["historical_v0_2_retained"] is True

gates = json.loads(PUBLICATION_GATES.read_text(encoding="utf-8"))
assert gates["status"] == "published_zero_blockers"
assert gates["blocker_count"] == 0
assert gates["public_release_allowed"] is True
assert gates["candidate_sha256"] == EXPECTED_CANDIDATE_SHA
assert gates["public_csv_sha256"] == EXPECTED_CANDIDATE_SHA
for gate in [
    "immutable_v0_2_base_verified",
    "base_public_sha_verified",
    "base_rows_preserved",
    "inland_scope_verified",
    "local_assignments_verified",
    "paired_rx_contract_verified",
    "channel_18_boat_side_only_verified",
    "marine_channel_16_excluded",
    "rf_deduplication_verified",
    "rx_only_verified",
    "memory_limit_verified",
    "aviation_zero_delta_verified",
    "airac08_current_window_verified",
    "candidate_reproducibility_verified",
    "candidate_sha_frozen",
    "public_route_created",
    "candidate_public_byte_identity_verified",
    "registry_update_verified",
    "region_page_update_verified",
    "historical_v0_2_retained",
]:
    assert gates["gates"][gate] is True, gate

publication = json.loads(PUBLICATION_RECORD.read_text(encoding="utf-8"))
assert publication["status"] == "published_immutable"
assert publication["publication_sprint"] == 109
assert publication["version"] == "0.3"
assert publication["memory_count"] == 71
assert publication["previous_public_version"] == "0.2"
assert publication["previous_public_memory_count"] == 62
assert publication["previous_public_sha256"] == EXPECTED_BASE_SHA
assert publication["public_csv_sha256"] == EXPECTED_CANDIDATE_SHA
assert publication["candidate_sha256"] == EXPECTED_CANDIDATE_SHA
assert publication["published_version_is_immutable"] is True

registry = REGISTRY.read_text(encoding="utf-8")
assert '{ id: "auvergne-rhone-alpes", name: "Auvergne-Rhône-Alpes", memoryCount: 71, marine: false, aviation: 18, version: "v0.3" }' in registry
assert 'item.id === "auvergne-rhone-alpes" && item.version === "v0.3" ? ["9 mémoires VHF navigation intérieure"]' in registry

regions = json.loads(REGIONS.read_text(encoding="utf-8"))
ara = next(region for region in regions if region["slug"] == "auvergne-rhone-alpes")
assert ara["status"] == "v0.3 disponible"
assert ara["memoryCount"] == 71
assert "VHF navigation intérieure RX" in ara["categories"]

page = REGION_PAGE.read_text(encoding="utf-8")
assert 'import { buildAraV03Pack } from "../../lib/araPack";' in page
assert 'const isAraV03 = pack.id === "auvergne-rhone-alpes" && publicPack?.version === "v0.3";' in page
assert '? buildAraV03Pack()' in page
assert 'isAraV03 ? 9 : 0' in page
assert 'isAraV03 ? "120–128"' in page

print(
    "ARA v0.3 published immutable: "
    f"71 RX / +9 inland VHF / sha256={EXPECTED_CANDIDATE_SHA} / byte_identity=true / public=true"
)
