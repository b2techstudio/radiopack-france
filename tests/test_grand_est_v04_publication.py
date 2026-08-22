#!/usr/bin/env python3
import csv
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V04 = ROOT / "research/grand-est-v0.4"
CANDIDATE = V04 / "generated/release-candidate/radiopack-france-grand-est-v0.4-candidate.csv"
PUBLIC = ROOT / "website/public/downloads/grand-est/radiopack-france-grand-est-v0.4.csv"
EXPECTED_SHA = "ba34604b11b75ae7f0e7aa17e3734053ff37bbe7910218af1ab66e59f3428a5d"
BASE_SHA = "45aef8547a701e7541e620fa9a2d8394595576921e793b75238146ff6e42e720"

candidate_bytes = CANDIDATE.read_bytes()
public_bytes = PUBLIC.read_bytes()
assert public_bytes == candidate_bytes
assert hashlib.sha256(public_bytes).hexdigest() == EXPECTED_SHA

rows = list(csv.DictReader(io.StringIO(public_bytes.decode("utf-8"), newline="")))
assert len(rows) == 97
assert sum(row["Mode"] == "AM" for row in rows) == 19
assert sum(120 <= int(row["Location"]) <= 132 for row in rows) == 13
assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
assert len({row["Frequency"] for row in rows}) == 97
assert len({row["Name"] for row in rows}) == 97
assert len({row["Location"] for row in rows}) == 97
assert max(int(row["Location"]) for row in rows) <= 199
assert "156.800000" not in {row["Frequency"] for row in rows if 120 <= int(row["Location"]) <= 132}

base = ROOT / "website/public/downloads/grand-est/radiopack-france-grand-est-v0.3.csv"
assert hashlib.sha256(base.read_bytes()).hexdigest() == BASE_SHA

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert '{ id: "grand-est", name: "Grand Est", memoryCount: 97, marine: false, aviation: 19, version: "v0.4" }' in registry
assert '13 mémoires VHF navigation intérieure' in registry

region_page = (ROOT / "website/src/pages/regions/[slug].astro").read_text(encoding="utf-8")
assert 'isGrandEstV04' in region_page
assert 'downloads/grand-est/radiopack-france-grand-est-v0.4.csv' in region_page
assert '120–132' in region_page

aviation = json.loads((V04 / "aviation-airac08-publication-2026-08-22.json").read_text(encoding="utf-8"))
assert aviation["publication_gate_complete"] is True
assert aviation["publication_decision"]["memory_count_after"] == 19
assert aviation["publication_decision"]["frequency_delta"] == 0
assert aviation["method"]["new_field_by_field_revalidation_claimed"] is False

scope = json.loads((V04 / "release-scope.json").read_text(encoding="utf-8"))
checklist = json.loads((V04 / "review-checklist.json").read_text(encoding="utf-8"))
gates = json.loads((V04 / "publication-gates.json").read_text(encoding="utf-8"))
record = json.loads((V04 / "publication-record.json").read_text(encoding="utf-8"))
manifest = json.loads((V04 / "generated/release-candidate/candidate-manifest.json").read_text(encoding="utf-8"))

assert scope["status"] == "published_immutable"
assert scope["memory_count"] == 97 and scope["inland_vhf_memory_count"] == 13
assert checklist["reviewed_count"] == checklist["item_count"] == 12
assert checklist["blocker_count"] == 0
assert gates["blocker_count"] == 0 and gates["public_release_allowed"] is True
assert record["status"] == "published_immutable"
assert record["memory_count"] == 97
assert record["previous_public_version"] == "0.3"
assert record["previous_public_memory_count"] == 84
assert record["public_csv_sha256"] == EXPECTED_SHA
assert record["public_csv_created"] is True
assert record["public_registry_updated"] is True
assert record["published"] is True
assert record["published_version_is_immutable"] is True
assert record["inland_vhf"]["memory_count"] == 13
assert record["aviation"]["memory_delta"] == 0
assert manifest["status"] == "published_basis_immutable"
assert manifest["public_csv_sha256"] == EXPECTED_SHA
assert manifest["published"] is True and manifest["immutable"] is True

print("Grand Est v0.4 publication: 97 RX / 19 aviation / 41 regional radio / 13 inland VHF, byte identity and SHA OK")
