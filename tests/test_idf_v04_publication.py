#!/usr/bin/env python3
import argparse
import csv
import hashlib
import io
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V04 = ROOT / "research/ile-de-france-v0.4"
CANDIDATE = V04 / "generated/release-candidate/radiopack-france-ile-de-france-v0.4-candidate.csv"
PUBLIC = ROOT / "website/public/downloads/ile-de-france/radiopack-france-ile-de-france-v0.4.csv"
BASE = ROOT / "website/public/downloads/ile-de-france/radiopack-france-ile-de-france-v0.3.csv"
DATASET = ROOT / "data/regional/ile-de-france-inland-vhf-rx.json"
EXPECTED_SHA = "14e1d1d95b38ef44d01b9cccb989a3f1567153ac64875594cc24bd4b57a1cdc2"
BASE_SHA = "e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125"
EXPECTED_INLAND = {
    "156.500000", "156.900000", "161.500000",
    "157.000000", "161.600000", "157.100000", "161.700000",
}
EXPECTED_NAMES = {"FLV10", "FL18-B", "FL18-T", "FL20-B", "FL20-T", "FL22-B", "FL22-T"}

parser = argparse.ArgumentParser()
parser.add_argument("--dist", type=Path, help="Optional Astro dist directory to validate")
args = parser.parse_args()

subprocess.run([sys.executable, str(ROOT / "tools/build_idf_v04_candidate.py"), "--check"], cwd=ROOT, check=True)

candidate_bytes = CANDIDATE.read_bytes()
public_bytes = PUBLIC.read_bytes()
assert public_bytes == candidate_bytes
assert hashlib.sha256(public_bytes).hexdigest() == EXPECTED_SHA
assert hashlib.sha256(BASE.read_bytes()).hexdigest() == BASE_SHA

rows = list(csv.DictReader(io.StringIO(public_bytes.decode("utf-8"), newline="")))
assert len(rows) == 64
assert sum(row["Mode"] == "AM" for row in rows) == 18
assert sum(70 <= int(row["Location"]) <= 84 for row in rows) == 15
inland = [row for row in rows if 120 <= int(row["Location"]) <= 126]
assert len(inland) == 7
assert {row["Frequency"] for row in inland} == EXPECTED_INLAND
assert {row["Name"] for row in inland} == EXPECTED_NAMES
assert all(row["Mode"] == "NFM" and row["TStep"] == "25.00" for row in inland)
assert "156.475000" not in {row["Frequency"] for row in inland}  # channel 69 not promoted
assert "156.800000" not in {row["Frequency"] for row in inland}  # marine channel 16 not added
assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
assert len({row["Frequency"] for row in rows}) == 64
assert len({row["Name"] for row in rows}) == 64
assert len({row["Location"] for row in rows}) == 64
assert max(int(row["Location"]) for row in rows) <= 199

source_data = json.loads(DATASET.read_text(encoding="utf-8"))
assert len(source_data["channels"]) == 7
assert {item["channel"] for item in source_data["local_assignments"]} == {18, 20, 22}
assert {item["site"] for item in source_data["local_assignments"]} == {"Varennes", "Champagne", "La Cave", "Vives-Eaux", "Le Coudray"}
assert {source["authority"] for source in source_data["sources"]} == {"VNF", "ANFR"}

validation = json.loads((V04 / "inland-vhf-validation-2026-08-22.json").read_text(encoding="utf-8"))
assert validation["status"] == "scope_closed_publication_basis"
assert validation["accounting"]["verified_inland_unique_rf_count"] == 7
assert validation["accounting"]["rf_duplicates_against_base"] == 0
assert validation["accounting"]["candidate_memory_count"] == 64
assert validation["blocker_count"] == 0
assert any(item["channel"] == 69 and item["decision"] == "exclude_from_v0_4" for item in validation["explicit_exclusions"])

aviation = json.loads((V04 / "aviation-airac08-publication-2026-08-22.json").read_text(encoding="utf-8"))
assert aviation["publication_gate_complete"] is True
assert aviation["publication_decision"]["memory_count_after"] == 18
assert aviation["publication_decision"]["frequency_delta"] == 0
assert aviation["method"]["new_field_by_field_revalidation_claimed"] is False
assert aviation["airac09_revalidation_required_on_or_after"] == "2026-09-03"

scope = json.loads((V04 / "release-scope.json").read_text(encoding="utf-8"))
checklist = json.loads((V04 / "review-checklist.json").read_text(encoding="utf-8"))
gates = json.loads((V04 / "publication-gates.json").read_text(encoding="utf-8"))
record = json.loads((V04 / "publication-record.json").read_text(encoding="utf-8"))
manifest = json.loads((V04 / "generated/release-candidate/candidate-manifest.json").read_text(encoding="utf-8"))
assert scope["status"] == "published_immutable"
assert scope["candidate"]["memory_count"] == 64 and scope["candidate"]["inland_vhf_memory_count"] == 7
assert scope["public"]["memory_count"] == 64 and scope["public"]["byte_identical_to_candidate"] is True
assert checklist["reviewed_count"] == checklist["item_count"] == 12
assert checklist["blocker_count"] == 0 and all(item["status"] == "passed" for item in checklist["items"])
assert gates["blocker_count"] == 0 and gates["public_release_allowed"] is True
assert record["status"] == "published_immutable"
assert record["memory_count"] == 64
assert record["previous_public_version"] == "0.3"
assert record["previous_public_memory_count"] == 57
assert record["public_csv_sha256"] == EXPECTED_SHA
assert record["candidate_csv_sha256"] == EXPECTED_SHA
assert record["published"] is True and record["published_version_is_immutable"] is True
assert record["inland_vhf"]["memory_count"] == 7
assert record["inland_vhf"]["channel_69_added"] is False
assert record["aviation"]["memory_delta"] == 0
assert manifest["status"] == "published_basis_immutable"
assert manifest["candidate_memory_count"] == 64
assert manifest["candidate_inland_vhf_memory_count"] == 7
assert manifest["public_csv_sha256"] == EXPECTED_SHA
assert manifest["published"] is True and manifest["immutable"] is True

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert '{ id: "ile-de-france", name: "Île-de-France", memoryCount: 64, marine: false, aviation: 18, version: "v0.4" }' in registry
assert '7 mémoires VHF navigation intérieure' in registry

regions = json.loads((ROOT / "website/src/data/regions.json").read_text(encoding="utf-8"))
idf = next(item for item in regions if item["slug"] == "ile-de-france")
assert idf["status"] == "v0.4 disponible" and idf["memoryCount"] == 64
assert "VHF navigation intérieure RX" in idf["categories"]

page = (ROOT / "website/src/pages/regions/[slug].astro").read_text(encoding="utf-8")
assert "isIdfV04" in page
assert 'downloads/ile-de-france/radiopack-france-ile-de-france-v0.4.csv' in page
assert "120–126" in page

if args.dist:
    built = args.dist / "downloads/ile-de-france/radiopack-france-ile-de-france-v0.4.csv"
    assert built.is_file(), f"Built IDF v0.4 CSV missing: {built}"
    assert built.read_bytes() == candidate_bytes
    assert hashlib.sha256(built.read_bytes()).hexdigest() == EXPECTED_SHA

print("IDF v0.4 publication: 64 RX / 18 aviation / 15 regional radio / 7 inland VHF, byte identity and SHA OK")
