#!/usr/bin/env python3
import csv
import hashlib
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V03 = ROOT / "research" / "grand-est-v0.3"
CANDIDATE = V03 / "generated/release-candidate/radiopack-france-grand-est-v0.3-candidate.csv"
PUBLIC = ROOT / "website/public/downloads/grand-est/radiopack-france-grand-est-v0.3.csv"
EXPECTED_SHA = "45aef8547a701e7541e620fa9a2d8394595576921e793b75238146ff6e42e720"

candidate_bytes = CANDIDATE.read_bytes()
public_bytes = PUBLIC.read_bytes()
assert public_bytes == candidate_bytes
assert hashlib.sha256(public_bytes).hexdigest() == EXPECTED_SHA

rows = list(csv.DictReader(io.StringIO(public_bytes.decode("utf-8"))))
assert len(rows) == 84
assert sum(row["Mode"] == "AM" for row in rows) == 19
assert sum(int(row["Location"]) >= 70 for row in rows) == 41
assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
assert len({row["Frequency"] for row in rows}) == 84
assert len({row["Name"] for row in rows}) == 84
assert len({row["Location"] for row in rows}) == 84
assert max(int(row["Location"]) for row in rows) <= 199

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert (
    '{ id: "grand-est", name: "Grand Est", memoryCount: 84, marine: false, aviation: 19, version: "v0.3" }' in registry
    or '{ id: "grand-est", name: "Grand Est", memoryCount: 97, marine: false, aviation: 19, version: "v0.4" }' in registry
)
assert 'item.id === "grand-est"' in registry

region_page = (ROOT / "website/src/pages/regions/[slug].astro").read_text(encoding="utf-8")
# The current page may advance to v0.4, but v0.3 publication bytes remain immutable.
assert ('isGrandEstV03' in region_page) or ('isGrandEstV04' in region_page)
assert (
    'downloads/grand-est/radiopack-france-grand-est-v0.3.csv' in region_page
    or 'downloads/grand-est/radiopack-france-grand-est-v0.4.csv' in region_page
)

aviation = json.loads((V03 / "aviation-airac08-publication-2026-08-22.json").read_text(encoding="utf-8"))
assert aviation["publication_gate_complete"] is True
assert aviation["publication_decision"]["memory_count_after"] == 19
assert aviation["publication_decision"]["frequency_delta"] == 0
assert aviation["method"]["new_field_by_field_revalidation_claimed"] is False

checklist = json.loads((V03 / "review-checklist.json").read_text(encoding="utf-8"))
gates = json.loads((V03 / "publication-gates.json").read_text(encoding="utf-8"))
record = json.loads((V03 / "publication-record.json").read_text(encoding="utf-8"))
assert checklist["reviewed_count"] == checklist["item_count"] == 12
assert checklist["blocker_count"] == 0
assert gates["blocker_count"] == 0
assert gates["public_release_allowed"] is True
assert record["status"] == "published_immutable"
assert record["version"] == "0.3"
assert record["memory_count"] == 84
assert record["public_csv_sha256"] == EXPECTED_SHA
assert record["public_csv_created"] is True
assert record["public_registry_updated"] is True
assert record["published"] is True
assert record["published_version_is_immutable"] is True

print("Grand Est v0.3 historical publication: 84 RX / 19 aviation / 41 regional, public byte identity and SHA preserved across later releases")
