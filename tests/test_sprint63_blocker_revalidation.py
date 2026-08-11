import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "research/sprint-63-source-revalidation.json"
RESUME = ROOT / "research/project-resume-state.json"

assert EVIDENCE.is_file(), f"Missing Sprint 63 evidence: {EVIDENCE}"
evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
assert evidence["sprint"] == 63
assert evidence["state_version"] == "0.21.52"
assert evidence["status"] == "source_revalidation_no_gate_cleared_not_public"

normandie = evidence["normandie_v04"]
assert normandie["f1zov"]["operator_status"] == "En Maintenance"
assert normandie["f1zov"]["operator_status_gate_cleared"] is False
assert normandie["f1zov"]["candidate_memory_delta"] == 0

f5zha = normandie["f5zha"]
assert f5zha["current_ref"]["paired_rx_frequencies_mhz"] == [145.4675, 432.575]
assert f5zha["conflicting_repeaterbook"]["conflicting_frequency_mhz"] == 431.4125
assert f5zha["conflicting_repeaterbook"]["verification_date_shown"] == "2017-02-17"
assert f5zha["conflicting_repeaterbook"]["classified_as_stale_secondary_conflict"] is True
assert f5zha["current_local_operator_or_equivalent_authoritative_frequency_source_found"] is False
assert f5zha["stale_secondary_conflict_alone_closes_authoritative_reconciliation_gate"] is False
assert f5zha["source_gate_cleared"] is False
assert f5zha["coverage_gate_cleared"] is False
assert f5zha["candidate_memory_delta"] == 0

f6zes = normandie["f6zes"]
assert f6zes["current_ref_unresolved_fields"] == ["operational_state", "band", "tx_mhz", "rx_mhz", "mode"]
assert f6zes["second_current_frequency_mode_source_found"] is False
assert f6zes["frequency_resolved"] is False
assert f6zes["mode_resolved"] is False
assert f6zes["candidate_memory_delta"] == 0
assert f6zes["must_not_guess_frequency"] is True

assert normandie["r3"]["field_gate_state"] == "field_evidence_required"
assert normandie["r3"]["new_field_observation_available_in_repository"] is False
assert normandie["candidate_memory_count_before"] == 142
assert normandie["candidate_memory_count_after"] == 142
assert normandie["known_ceiling_memory_count"] == 147
assert normandie["review_completed_count"] == 3
assert normandie["review_item_count"] == 9
assert normandie["release_blocker_count"] == 6
assert normandie["eligible_addition_count"] == 0

bretagne = evidence["bretagne_v01"]
guide = bretagne["meteofrance_guide_marine_2026"]
assert guide["landing_page_date"] == "2026-08-05"
assert guide["pdf_content_extracted"] is False
assert guide["pdf_screenshot_available"] is False
assert guide["channel64_conclusion_from_unread_pdf"] is False
assert guide["channel79_site_conclusion_from_unread_pdf"] is False
assert bretagne["etel_channel64_site_confirmed"] is False
assert bretagne["corsen_channel79_site_confirmed"] is False
assert bretagne["new_rf_memory_delta"] == 0

assert evidence["decisions"]["normandie_gate_cleared_count"] == 0
assert evidence["decisions"]["normandie_candidate_mutated"] is False
assert evidence["decisions"]["public_pack_mutated"] is False
assert evidence["decisions"]["public_export_allowed"] is False

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8").lower()
assert 'id: "bretagne"' not in registry
assert 'version: "0.4"' not in registry

normandie_public = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv"
assert normandie_public.is_file()
assert len(normandie_public.read_text(encoding="utf-8").splitlines()) == 140

resume = json.loads(RESUME.read_text(encoding="utf-8"))
assert resume["current_sprint"] == 63
assert resume["state_version"] == "0.21.52"
assert resume["active_work"]["internal_candidate_memory_count"] == 142
assert resume["active_work"]["current_guarded_promotion_plan_eligible_addition_count"] == 0
assert resume["active_work"]["public_release_ready"] is False
assert resume["resume_rules"]["stale_secondary_conflict_does_not_replace_required_authoritative_reconciliation"] is True

print("Sprint 63 blocker revalidation: no gate cleared, stale F5ZHA secondary conflict correctly bounded, F1ZOV/F6ZES still blocked, unread Guide Marine produces no inference, public packs unchanged, OK")
