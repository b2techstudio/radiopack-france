import importlib.util
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRESHNESS = ROOT / "tools/check_normandie_v04_source_freshness.py"
CHECKLIST = ROOT / "tools/build_normandie_v04_review_checklist.py"
DIFF = ROOT / "tools/build_normandie_v04_candidate_diff.py"
AUDIT = ROOT / "tools/run_normandie_v04_prepublication_audit.py"
POLICY = ROOT / "research/normandie-v0.4/source-freshness-policy.json"

for path in (FRESHNESS, CHECKLIST, DIFF, AUDIT, POLICY):
    assert path.is_file(), f"Missing expected file: {path}"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


freshness = load_module("freshness_test", FRESHNESS)
checklist = load_module("checklist_test", CHECKLIST)
diff = load_module("diff_test", DIFF)
audit = load_module("audit_test", AUDIT)

current_day = date(2026, 8, 10)
fresh = freshness.evaluate(ROOT, current_day)
assert fresh["status"] == "source_freshness_check_not_public"
assert fresh["all_revalidations_fresh"] is True
assert fresh["stale_station_count"] == 0
assert fresh["release_review_freshness_gate_passed"] is True
assert fresh["public_export_allowed"] is False
assert fresh["stations"]["F1ZOV_EQUEURDREVILLE"]["freshness_class"] == "local_operator_status"
assert fresh["stations"]["F1ZOV_EQUEURDREVILLE"]["maximum_age_days"] == 14

stale = freshness.evaluate(ROOT, date(2026, 9, 15))
assert stale["all_revalidations_fresh"] is False
assert stale["stale_station_count"] == 4
assert set(stale["stale_station_ids"]) == {"F1ZBX_R3", "F5ZHA_LAVAL", "F1ZOV_EQUEURDREVILLE", "F6ZES_SOURDEVAL"}
assert stale["release_review_freshness_gate_passed"] is False
assert all(item["stale_state_is_negative_operational_evidence"] is False for item in stale["stations"].values())

review = checklist.build(ROOT, current_day)
assert review["schema_version"] == "1.1"
assert review["status"] == "release_review_checklist_not_public"
assert review["item_count"] == 9
assert review["completed_count"] == 3
assert review["blocking_open_count"] == 6
assert review["release_review_complete"] is False
assert review["public_registry_has_v04"] is False
assert review["public_activation_is_separate_step"] is True
assert review["public_export_allowed"] is False
completed = {item["id"] for item in review["items"] if item["completed"]}
assert completed == {"SOURCE_CONSISTENCY", "SOURCE_FRESHNESS", "PUBLIC_REGISTRY_STILL_PRIVATE"}
assert set(review["blocking_open_ids"]) == {
    "R3_MORTAIN_RX",
    "F5ZHA_SOURCE_AND_COVERAGE",
    "F1ZOV_OPERATIONAL_STATUS",
    "F6ZES_RESOLVED",
    "FINAL_MEMORY_PLAN",
    "FINAL_REVIEW",
}

candidate_diff = diff.build(ROOT)
assert candidate_diff["status"] == "candidate_structural_diff_not_public"
assert candidate_diff["published_base_memory_count"] == 139
assert candidate_diff["current_internal_candidate_memory_count"] == 142
assert candidate_diff["current_internal_addition_count"] == 3
assert candidate_diff["guarded_preview_memory_count"] == 142
assert candidate_diff["currently_eligible_future_addition_count"] == 0
assert candidate_diff["currently_eligible_future_additions"] == []
assert candidate_diff["published_base_is_exact_prefix_of_internal_candidate"] is True
assert candidate_diff["internal_candidate_is_exact_prefix_of_guarded_preview"] is True
assert candidate_diff["candidate_mutated"] is False
assert candidate_diff["public_export_allowed"] is False
assert [row["frequency_mhz"] for row in candidate_diff["current_internal_additions"]] == [145.0875, 145.1, 431.25]
assert all(row["duplex"] == "off" and row["offset"] == "0.000000" for row in candidate_diff["current_internal_additions"])

audit_result = audit.build(ROOT, current_day)
assert audit_result["schema_version"] == "1.1"
assert audit_result["status"] == "prepublication_audit_not_public"
assert audit_result["integrity_ok"] is True
assert audit_result["integrity_error_count"] == 0
assert audit_result["published_base_memory_count"] == 139
assert audit_result["internal_candidate_memory_count"] == 142
assert audit_result["guarded_preview_memory_count"] == 142
assert audit_result["currently_eligible_future_addition_count"] == 0
assert audit_result["review_completed_count"] == 3
assert audit_result["review_item_count"] == 9
assert audit_result["review_blocking_open_count"] == 6
assert audit_result["release_blocking_count"] == 6
assert audit_result["prepublication_ready"] is False
assert audit_result["release_ready"] is False
assert audit_result["public_registry_has_v04"] is False
assert audit_result["public_activation_pending"] is False
assert audit_result["public_export_allowed"] is False
assert all(audit_result["integrity_checks"].values())

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'version: "v0.4"' not in registry
assert not (ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv").exists()

print(
    "Tests Normandie v0.4 prepublication audit: source freshness current/stale behavior guarded, "
    "review checklist is 3/9 with 6 true prepublication blockers, structural diff preserves 139->142->142 exact prefixes, "
    "audit integrity OK while prepublication remains blocked and public v0.4 stays absent, OK"
)
