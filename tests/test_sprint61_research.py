import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ETEL = ROOT / "research/bretagne-v0.1/etel-channel64-evidence.json"
CORSEN = ROOT / "research/bretagne-v0.1/corsen-channel79-evidence.json"
MORTAIN = ROOT / "research/normandie-v0.4/mortain-adjacent-ref-scan.json"

for path in (ETEL, CORSEN, MORTAIN):
    assert path.is_file(), f"Missing Sprint 61 research file: {path}"

etel = json.loads(ETEL.read_text(encoding="utf-8"))
assert etel["status"] == "primary_current_channel64_conflict_documented_site_unresolved"
assert etel["paired_rx"]["ship_to_coast_mhz"] == 156.225
assert etel["paired_rx"]["coast_to_ship_mhz"] == 160.825
assert etel["paired_rx"]["new_rf_memory_delta"] == 0
assert etel["assessment"]["primary_current_regional_channel64_statement_exists"] is True
assert etel["assessment"]["primary_current_local_cross_channel64_site_exists"] is False
assert etel["assessment"]["primary_current_local_cross_documents_mention_channel64"] is False
assert etel["assessment"]["channel64_site_confirmed"] is False
assert etel["assessment"]["site_assignment_can_be_promoted"] is False
assert etel["network_count_note"]["must_not_be_arithmetically_reconciled_without_source_definition"] is True
assert etel["rules"]["absence_from_current_local_documents_is_not_negative_operational_evidence"] is True
assert etel["rules"]["primary_source_conflict_requires_reconciliation"] is True
assert etel["rules"]["channel64_site_must_not_be_guessed"] is True
assert etel["rules"]["public_export_allowed"] is False

corsen = json.loads(CORSEN.read_text(encoding="utf-8"))
assert corsen["schema_version"] == "1.1"
assert corsen["paired_rx"]["new_rf_memory_delta"] == 0
assert corsen["primary_revalidation_search"]["direct_primary_channel79_site_match_found"] is False
assert corsen["primary_revalidation_search"]["search_failure_is_negative_evidence"] is False
assert corsen["assessment"]["primary_current_channel79_transmitter_site_confirmed"] is False
assert corsen["assessment"]["secondary_clue_sites"] == ["Cap Fréhel", "Bodic"]
assert corsen["assessment"]["site_assignment_can_be_promoted"] is False
assert corsen["rules"]["primary_pdf_identified_but_unread_is_not_negative_evidence"] is True
assert corsen["rules"]["channel79_site_must_not_be_guessed"] is True
assert corsen["rules"]["public_export_allowed"] is False

mortain = json.loads(MORTAIN.read_text(encoding="utf-8"))
assert mortain["status"] == "current_ref_adjacent_department_scan_not_public"
assert mortain["departments_scanned"] == [35, 50, 53, 61]
assert mortain["assessment"]["new_untracked_active_analog_candidate_count"] == 0
assert mortain["assessment"]["candidate_memory_delta"] == 0
assert set(mortain["assessment"]["existing_priority_cases_remain"]) == {"F6ZES", "F1ZBX", "F5ZHA", "F1ZOV"}
for department in mortain["department_findings"]:
    assert department["new_untracked_active_analog_candidate_count"] == 0
assert mortain["rules"]["directory_scan_is_inventory_evidence_not_reception_proof"] is True
assert mortain["rules"]["local_operator_status_overrides_general_directory_for_current_state"] is True
assert mortain["rules"]["unresolved_frequency_must_not_be_guessed"] is True
assert mortain["rules"]["candidate_not_mutated_by_scan"] is True
assert mortain["rules"]["public_export_allowed"] is False

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8").lower()
assert 'id: "bretagne"' not in registry
assert 'version: "0.4"' not in registry

normandie_public = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv"
assert normandie_public.is_file()
rows = normandie_public.read_text(encoding="utf-8").splitlines()
assert len(rows) == 140, "Published Normandie v0.3.1 must remain 139 memories + header"

print(
    "Sprint 61 research guards: Etel channel 64 primary-source conflict documented without site inference, "
    "Corsen channel 79 primary attribution still unresolved despite current secondary Cap Frehel/Bodic clues, "
    "REF scan 35/50/53/61 finds zero new untracked active analog candidates, candidate/public packs unchanged, OK"
)
