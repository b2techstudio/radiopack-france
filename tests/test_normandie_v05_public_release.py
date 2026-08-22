#!/usr/bin/env python3
import csv
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_V04 = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv"
PUBLIC_V05 = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.5.csv"
BUILDER = ROOT / "tools/build_normandie_v05_internal_candidate.py"
FREEZE = ROOT / "research/normandie-v0.5/candidate-freeze.json"
SCOPE = ROOT / "research/normandie-v0.5/release-scope.json"
GATES = ROOT / "research/normandie-v0.5/publication-gates.json"
RECORD = ROOT / "research/normandie-v0.5/publication-record.json"
OLD_RECORD = ROOT / "research/normandie-v0.4/publication-record.json"
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"
REGIONS = ROOT / "website/src/data/regions.json"
REGION_PAGE = ROOT / "website/src/pages/regions/[slug].astro"
EXPECTED_SHA = "1d7ce66c7a5faafe98e4ee59791bcd29af1fd1f432ee1bfc1cad7cba3bc5cf59"
OLD_SHA = "3da26f18cefbf7ec1dfb6a991101d07f6a8ce9fb921015a7202870fc9b9db66d"

for path in [PUBLIC_V04, PUBLIC_V05, BUILDER, FREEZE, SCOPE, GATES, RECORD, OLD_RECORD, REGISTRY, REGIONS, REGION_PAGE]:
    assert path.is_file(), path

spec = importlib.util.spec_from_file_location("normandie_v05", BUILDER)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
candidate = mod.build_candidate(ROOT)
candidate_bytes = mod.candidate_csv_bytes(candidate)
public_bytes = PUBLIC_V05.read_bytes()
assert public_bytes == candidate_bytes
assert hashlib.sha256(public_bytes).hexdigest() == EXPECTED_SHA
assert hashlib.sha256(PUBLIC_V04.read_bytes()).hexdigest() == OLD_SHA

with PUBLIC_V04.open(encoding="utf-8", newline="") as handle:
    old_rows = list(csv.DictReader(handle))
with PUBLIC_V05.open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
assert len(old_rows) == 142
assert len(rows) == 146
assert rows[:142] == old_rows
assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
assert len({row["Location"] for row in rows}) == 146
assert len({row["Name"] for row in rows}) == 146
assert len({round(float(row["Frequency"]), 6) for row in rows}) == 146
assert all(len(row["Name"]) <= 10 for row in rows)
new_rows = rows[142:]
assert [int(row["Location"]) for row in new_rows] == [178, 179, 180, 181]
assert [row["Name"] for row in new_rows] == ["35-R3-IN", "35-R3-OUT", "53-ZHA-V", "53-ZHA-U"]
assert [round(float(row["Frequency"]), 6) for row in new_rows] == [145.075, 145.675, 145.4675, 432.575]
assert all(row["Mode"] == "NFM" and row["TStep"] == "12.50" for row in new_rows)
assert all("couverture theorique Mortain" in row["Comment"] for row in new_rows)
assert 431.4125 not in [round(float(row["Frequency"]), 6) for row in new_rows]
assert 431.975 not in [round(float(row["Frequency"]), 6) for row in new_rows]
assert 430.375 not in [round(float(row["Frequency"]), 6) for row in new_rows]

freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
assert freeze["candidate_memory_count"] == 146
assert freeze["candidate_sha256"] == EXPECTED_SHA
assert freeze["coverage_basis"] == "theoretical"
assert freeze["field_reception_verified"] is False

scope = json.loads(SCOPE.read_text(encoding="utf-8"))
assert scope["status"] == "published_scope_immutable"
assert scope["memory_count"] == 146 and scope["memory_delta"] == 4
assert scope["candidate_sha256"] == scope["public_csv_sha256"] == EXPECTED_SHA
assert scope["candidate_public_byte_identity_verified"] is True
assert scope["theoretical_coverage"]["memory_count"] == 4
assert scope["theoretical_coverage"]["field_reception_verified"] is False
assert scope["theoretical_coverage"]["must_not_be_described_as_measured_or_guaranteed"] is True
assert scope["historical_public_v0_4_retained"] is True

publish_gates = json.loads(GATES.read_text(encoding="utf-8"))
assert publish_gates["status"] == "published_zero_blockers"
assert publish_gates["blocker_count"] == 0
assert publish_gates["public_release_allowed"] is True
assert all(publish_gates["gates"].values())
assert publish_gates["hashes"]["public_v0_5_sha256"] == EXPECTED_SHA

record = json.loads(RECORD.read_text(encoding="utf-8"))
assert record["status"] == "published_immutable"
assert record["publication_sprint"] == 113
assert record["version"] == "0.5" and record["memory_count"] == 146
assert record["new_memory_count_vs_v0_4"] == 4
assert record["public_csv_sha256"] == record["candidate_sha256"] == EXPECTED_SHA
assert record["candidate_public_byte_identity_verified"] is True
assert record["previous_public_version"] == "0.4" and record["previous_public_memory_count"] == 142
assert record["previous_public_csv_sha256"] == OLD_SHA
assert record["theoretical_coverage"]["memory_count"] == 4
assert record["theoretical_coverage"]["field_reception_verified"] is False
assert record["theoretical_coverage"]["public_disclosure_required"] is True
assert record["theoretical_coverage"]["theory_is_not_measured_or_guaranteed_reception"] is True
assert record["published_version_is_immutable"] is True

old_record = json.loads(OLD_RECORD.read_text(encoding="utf-8"))
assert old_record["status"] == "published_immutable"
assert old_record["version"] == "0.4" and old_record["memory_count"] == 142
assert old_record["public_csv_sha256"] == OLD_SHA
assert old_record["published_version_is_immutable"] is True

registry = REGISTRY.read_text(encoding="utf-8")
for token in [
    'id: "normandie"', 'version: "v0.5"', 'memoryCount: 146',
    'radiopack-france-normandie-v0.5.csv', 'couverture théorique documentée'
]:
    assert token in registry, token

regions = json.loads(REGIONS.read_text(encoding="utf-8"))
normandie = next(item for item in regions if item["slug"] == "normandie")
assert normandie["status"] == "v0.5 disponible"
assert normandie["memoryCount"] == 146
assert "Couverture théorique RX" in normandie["categories"]
assert "couverture théorique" in normandie["description"]

page = REGION_PAGE.read_text(encoding="utf-8")
for token in [
    'isNormandieV05', 'radiopack-france-normandie-v0.5.csv',
    'Couverture théorique — 4 mémoires', '178–181',
    'ni une réception mesurée, ni une couverture garantie'
]:
    assert token in page, token

print("Sprint 113 Normandie v0.5 public release: 146 RX, exact frozen SHA, +4 theoretical coverage memories disclosed, v0.4 retained immutable OK")
