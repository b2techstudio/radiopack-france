#!/usr/bin/env python3
import importlib.util
import json
import tempfile
from copy import deepcopy
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READINESS = ROOT / "research/bretagne-v0.3/airac09-readiness.json"
TEMPLATE = ROOT / "research/bretagne-v0.3/airac09-revalidation-template.json"
BASELINE = ROOT / "research/bretagne-v0.2/aviation-airac-08.json"
PUBLIC_RECORD = ROOT / "research/bretagne-v0.2/publication-record.json"
VALIDATOR = ROOT / "tools/check_bretagne_v03_airac09_revalidation.py"

for path in [READINESS, TEMPLATE, BASELINE, PUBLIC_RECORD, VALIDATOR]:
    assert path.is_file(), path

readiness = json.loads(READINESS.read_text(encoding="utf-8"))
template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
public_record = json.loads(PUBLIC_RECORD.read_text(encoding="utf-8"))

assert readiness["status"] == "future_cycle_source_available_not_current_readiness_prepared"
assert readiness["pack"] == "Bretagne"
assert readiness["target_version"] == "0.3"
assert readiness["prepared_on"] == "2026-08-22"
assert readiness["public_base"]["version"] == "0.2"
assert readiness["public_base"]["memory_count"] == 151
assert readiness["public_base"]["sha256"] == "73aa3d530ae9f6c572eb01794b0861ecba61df0faf7884ee766085d3de7601a4"
assert readiness["public_base"]["immutable"] is True
assert readiness["candidate"]["memory_count"] == 151
assert readiness["candidate"]["memory_delta"] == 0
assert readiness["candidate"]["aviation_memory_count"] == 16
assert readiness["candidate"]["public_export_allowed"] is False
assert readiness["candidate"]["public_release_allowed"] is False
assert readiness["cycle"]["current_on_prepared_date"] == "AIRAC 08/26"
assert readiness["cycle"]["current_until_inclusive"] == "2026-09-02"
assert readiness["cycle"]["required_cycle"] == "AIRAC 09/26"
assert readiness["cycle"]["effective_from"] == "2026-09-03"
assert readiness["cycle"]["effective_until_inclusive"] == "2026-09-30"
assert readiness["cycle"]["must_not_be_treated_as_current_before"] == "2026-09-03"

sia = next(source for source in readiness["future_cycle_sources"] if source["authority"] == "SIA France")
assert sia["title"] == "Données aéronautiques XML AIRAC 09/26"
assert sia["observed_available_on"] == "2026-08-22"
assert sia["effective_from"] == "2026-09-03"
assert sia["effective_until_inclusive"] == "2026-09-30"
assert sia["available_before_effective_date"] is True
assert sia["current_evidence_on_observed_date"] is False
assert sia["xml_export_bytes_extracted_in_repository_workflow"] is False
assert readiness["rules"]["future_airac_source_availability_is_not_current_evidence"] is True
assert readiness["rules"]["future_airac_must_not_be_promoted_before_effective_date"] is True
assert readiness["rules"]["direct_xml_field_match_must_not_be_claimed_without_xml_extraction"] is True
assert readiness["rules"]["public_v0_3_created"] is False

assert public_record["status"] == "published_immutable"
assert public_record["version"] == "0.2"
assert public_record["memory_count"] == 151
assert public_record["public_csv_sha256"] == readiness["public_base"]["sha256"]
assert public_record["published_version_is_immutable"] is True
assert public_record["aviation"]["memory_count"] == 16
assert public_record["aviation"]["cycle"] == "AIRAC 08/26"
assert public_record["aviation"]["valid_through_inclusive"] == "2026-09-02"

baseline_by_name = {
    item["name"]: round(float(item["frequency_mhz"]), 6)
    for item in baseline["channels"]
}
assert len(baseline_by_name) == 16
assert len(template["memories"]) == 16
assert [item["location"] for item in template["memories"]] == list(range(130, 146))
assert [item["name"] for item in template["memories"]] == readiness["baseline_aviation"]["names"]
for item in template["memories"]:
    assert round(float(item["baseline_frequency_mhz"]), 6) == baseline_by_name[item["name"]]
    assert item["decision"] is None
    assert item["current_frequency_mhz"] is None
    assert item["source_cycle"] is None
    assert item["source_effective_from"] is None
    assert item["source_url"] is None
    assert item["evidence_note"] is None

spec = importlib.util.spec_from_file_location("bretagne_airac09", VALIDATOR)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

blank_before = module.evaluate(ROOT, TEMPLATE, date(2026, 8, 22))
assert blank_before["cycle_phase"] == "future_not_current"
assert blank_before["cycle_is_current"] is False
assert blank_before["resolved_memory_count"] == 0
assert blank_before["unresolved_memory_count"] == 16
assert blank_before["candidate_rebuild_allowed"] is False
assert blank_before["automatic_candidate_mutation_allowed"] is False
assert blank_before["automatic_publication_allowed"] is False
assert blank_before["public_release_allowed"] is False
assert blank_before["next_action"] == "wait_until_2026_09_03"

blank_effective = module.evaluate(ROOT, TEMPLATE, date(2026, 9, 3))
assert blank_effective["cycle_phase"] == "current"
assert blank_effective["cycle_is_current"] is True
assert blank_effective["resolved_memory_count"] == 0
assert blank_effective["unresolved_memory_count"] == 16
assert blank_effective["candidate_rebuild_allowed"] is False
assert blank_effective["next_action"] == "complete_current_airac09_primary_revalidation_and_human_review"

# Synthetic complete fixture verifies validator logic only; it is not repository evidence.
complete = deepcopy(template)
complete["status"] = "synthetic_complete_test_fixture"
complete["current_cycle_primary_source_verified"] = True
complete["current_cycle_primary_source_verified_on"] = "2026-09-03"
complete["human_review"] = {
    "completed": True,
    "reviewed_on": "2026-09-03",
    "reviewer_note": "Synthetic CI fixture only; not aeronautical evidence.",
}
for item in complete["memories"]:
    item["decision"] = "unchanged"
    item["current_frequency_mhz"] = item["baseline_frequency_mhz"]
    item["source_cycle"] = "AIRAC 09/26"
    item["source_effective_from"] = "2026-09-03"
    item["source_url"] = "https://example.invalid/synthetic-ci-fixture"
    item["evidence_note"] = "Synthetic CI fixture only; not real AIRAC evidence."

with tempfile.TemporaryDirectory(prefix="radiopack-bretagne-airac09-") as td:
    fixture = Path(td) / "complete.json"
    fixture.write_text(json.dumps(complete, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    complete_before = module.evaluate(ROOT, fixture, date(2026, 8, 22))
    assert complete_before["cycle_is_current"] is False
    assert complete_before["candidate_rebuild_allowed"] is False
    assert complete_before["public_release_allowed"] is False

    complete_effective = module.evaluate(ROOT, fixture, date(2026, 9, 3))
    assert complete_effective["cycle_is_current"] is True
    assert complete_effective["primary_cycle_source_verification_valid"] is True
    assert complete_effective["resolved_memory_count"] == 16
    assert complete_effective["unresolved_memory_count"] == 0
    assert complete_effective["human_review_valid"] is True
    assert complete_effective["validation_errors"] == []
    assert complete_effective["candidate_rebuild_allowed"] is True
    assert complete_effective["candidate_rebuild_is_publication"] is False
    assert complete_effective["automatic_candidate_mutation_allowed"] is False
    assert complete_effective["automatic_publication_allowed"] is False
    assert complete_effective["public_release_allowed"] is False
    assert complete_effective["next_action"] == "rebuild_internal_candidate_then_run_separate_prepublication_gates"

expired = module.evaluate(ROOT, TEMPLATE, date(2026, 10, 1))
assert expired["cycle_phase"] == "expired_require_newer_cycle"
assert expired["cycle_is_current"] is False
assert expired["candidate_rebuild_allowed"] is False
assert expired["next_action"] == "use_newer_current_cycle"

print("Sprint 111 Bretagne AIRAC 09/26 readiness: 16-memory matrix complete, future-cycle hard block before 2026-09-03, no automatic publication OK")
