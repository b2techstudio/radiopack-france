#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research" / "ile-de-france-v0.3"
CANDIDATE = RESEARCH / "generated/release-candidate/radiopack-france-ile-de-france-v0.3-candidate.csv"
PUBLIC = ROOT / "website/public/downloads/ile-de-france/radiopack-france-ile-de-france-v0.3.csv"
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"
METROPOLITAN = ROOT / "website/src/lib/metropolitanPack.ts"
REGION_PAGE = ROOT / "website/src/pages/regions/[slug].astro"
EXPECTED_SHA = "e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125"
BASE_SHA = "dbcadbcef403d7272dc374a7010def7276b06048a8e863277fcdb3558a8f624d"
PUBLIC_RELATIVE = Path("downloads/ile-de-france/radiopack-france-ile-de-france-v0.3.csv")

parser = argparse.ArgumentParser()
parser.add_argument("--dist", type=Path, help="Optional Astro dist directory to validate after a production build")
args = parser.parse_args()

assert CANDIDATE.is_file(), "Frozen IDF v0.3 candidate missing"
assert PUBLIC.is_file(), "Public IDF v0.3 CSV missing"
assert PUBLIC.read_bytes() == CANDIDATE.read_bytes(), "Public CSV differs byte-for-byte from frozen candidate"
assert hashlib.sha256(PUBLIC.read_bytes()).hexdigest() == EXPECTED_SHA

with PUBLIC.open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))

assert len(rows) == 57
assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
assert len({row["Frequency"] for row in rows}) == 57
assert len({row["Name"] for row in rows}) == 57
assert len({row["Location"] for row in rows}) == 57
assert max(int(row["Location"]) for row in rows) <= 199
assert sum(row["Mode"] == "AM" for row in rows) == 18
assert sum(int(row["Location"]) >= 70 for row in rows) == 15

registry = REGISTRY.read_text(encoding="utf-8")
assert '{ id: "ile-de-france", name: "Île-de-France", memoryCount: 57, marine: false, aviation: 18, version: "v0.3" }' in registry
assert 'item.id === "ile-de-france"' in registry
assert 'radiopack-france-${item.id}-${item.version}.csv' in registry

# The historical v0.2 generator remains untouched so its old route stays reproducible.
metropolitan = METROPOLITAN.read_text(encoding="utf-8")
assert 'id: "ile-de-france"' in metropolitan
assert 'version: "v0.2"' in metropolitan
assert 'memoryCount: 58' in metropolitan
assert 'filename: "radiopack-france-ile-de-france-v0.2.csv"' in metropolitan

page = REGION_PAGE.read_text(encoding="utf-8")
assert 'const isIdfV03 = pack.id === "ile-de-france" && publicPack?.version === "v0.3";' in page
assert 'loadPublicPackMemories("downloads/ile-de-france/radiopack-france-ile-de-france-v0.3.csv")' in page

record = json.loads((RESEARCH / "publication-record.json").read_text(encoding="utf-8"))
manifest = json.loads((RESEARCH / "generated/release-candidate/candidate-manifest.json").read_text(encoding="utf-8"))
scope = json.loads((RESEARCH / "release-scope.json").read_text(encoding="utf-8"))
gates = json.loads((RESEARCH / "publication-gates.json").read_text(encoding="utf-8"))
checklist = json.loads((RESEARCH / "review-checklist.json").read_text(encoding="utf-8"))

assert record["status"] == "published_immutable"
assert record["public_csv_sha256"] == EXPECTED_SHA
assert record["candidate_csv_sha256"] == EXPECTED_SHA
assert record["base_public_csv_sha256"] == BASE_SHA
assert record["public_csv_created"] is True
assert record["public_registry_updated"] is True
assert record["published"] is True
assert record["published_version_is_immutable"] is True
assert manifest["public_csv_sha256"] == EXPECTED_SHA
assert manifest["public_export_allowed"] is True
assert manifest["published"] is True
assert scope["status"] == "published_immutable"
assert scope["published"] is True
assert scope["public_mutation_performed"] is True
assert gates["status"] == "published_zero_blockers"
assert gates["blocker_count"] == 0
assert all(check["pass"] for check in gates["checks"])
assert checklist["reviewed_count"] == checklist["item_count"] == 12
assert checklist["published"] is True

if args.dist:
    built = args.dist / PUBLIC_RELATIVE
    assert built.is_file(), f"Built IDF v0.3 CSV missing: {built}"
    assert built.read_bytes() == CANDIDATE.read_bytes(), "Astro-built IDF v0.3 CSV differs from frozen candidate"
    assert hashlib.sha256(built.read_bytes()).hexdigest() == EXPECTED_SHA

print(f"IDF v0.3 publication: 57 RX, 18 aviation, 15 regional, exact candidate/public SHA {EXPECTED_SHA} OK")
