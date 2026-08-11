import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "research/sprint-67-current-reference-synthesis.json"
RESUME = ROOT / "research/project-resume-state.json"
COR = ROOT / "research/bretagne-v0.1/corsen-channel79-evidence.json"
ETEL = ROOT / "research/bretagne-v0.1/etel-channel64-evidence.json"

assert EVIDENCE.is_file()
e = json.loads(EVIDENCE.read_text(encoding="utf-8"))
assert e["sprint"] == 67
assert e["state_version"] == "0.21.56"
assert e["status"] == "current_reference_synthesis_no_promotion_not_public"
assert e["public_export_allowed"] is False
assert e["candidate_mutation_allowed"] is False

n = e["normandie_v04"]
f5 = n["f5zha"]
assert f5["working_pair_mhz"] == [145.4675, 432.575]
assert f5["repeaterbook_current_display_frequency_mhz"] == 431.4125
assert f5["repeaterbook_current_display_shows_green_status"] is True
assert f5["repeaterbook_verification_date_shown"] == "2017-02-17"
assert f5["repeaterbook_verification_page_shows_off_air"] is True
assert f5["current_display_state_overrides_dated_verification_provenance"] is False
assert f5["authoritative_source_reconciliation_complete"] is False
assert f5["mortain_field_gate_cleared"] is False
assert f5["candidate_memory_delta"] == 0

assert n["f6zes"]["frequency_mode_operational_state_resolved"] is False
assert n["f6zes"]["must_not_guess_frequency"] is True
r3 = n["r3"]
assert r3["pair_rx_frequencies_mhz"] == [145.075, 145.675]
assert r3["required_rx_memory_count_if_promoted"] == 2
assert r3["minimum_independent_field_sessions"] == 2
assert r3["field_sessions_are_evidence_not_memories"] is True
assert r3["field_gate_cleared"] is False
assert n["candidate_memory_count_before"] == 142
assert n["candidate_memory_count_after"] == 142
assert n["known_ceiling_memory_count"] == 147
assert n["review_completed_count"] == 3
assert n["review_item_count"] == 9
assert n["release_blocker_count"] == 6
assert n["eligible_addition_count"] == 0

b = e["bretagne_v01"]
guide = b["ministry_leisure_guide_2026"]
assert guide["source_class"] == "current_primary"
assert guide["source_page_updated"] == "2026-06-19"
assert guide["pdf_extracted"] is True
assert guide["pdf_page_visually_checked"] is True
assert guide["confirms_cross_weather_channels_79_80"] is True
assert guide["confirms_permanent_coastal_weather_channels_63_64"] is True
assert guide["names_channel64_transmitter_site"] is False
assert guide["names_channel79_transmitter_site"] is False
assert guide["channel_level_confirmation_is_site_assignment"] is False

etel = b["cross_etel_channel64"]
assert etel["pair_rx_frequencies_mhz"] == [156.225, 160.825]
assert etel["required_rx_memory_count_if_published"] == 2
assert etel["current_primary_regional_channel_confirmation"] is True
assert etel["current_local_cross_channel63_convergence"] is True
assert etel["current_channel64_site_confirmed"] is False
assert etel["current_channel64_operation_at_named_site_confirmed"] is False
assert etel["current_channel64_stopped_proven"] is False
assert etel["primary_conflict_open"] is True

corsen = b["cross_corsen_channel79"]
assert corsen["pair_rx_frequencies_mhz"] == [156.975, 161.575]
assert corsen["required_rx_memory_count_if_published"] == 2
assert corsen["current_primary_channel_level_confirmation"] is True
assert corsen["current_primary_transmitter_site_confirmed"] is False
assert corsen["current_primary_infrastructure_sites"] == ["Cap Fréhel", "Stiff / Ouessant"]
assert corsen["current_local_secondary_sites"] == ["Cap Fréhel", "Bodic"]
assert corsen["secondary_full_chain_sites"] == ["Cap Fréhel", "Bodic", "Batz", "Stiff / Ouessant", "Pointe du Raz"]
assert corsen["secondary_current_stiff_channel79_clue_exists"] is True
assert corsen["secondary_convergence_can_promote_current_primary_site_assignment"] is False
assert corsen["priority_primary_revalidation_sites"][0] == "Stiff / Ouessant"
assert b["new_site_assignment_count"] == 0
assert b["new_rf_memory_delta"] == 0
assert b["public_promotion_allowed"] is False

# Existing detailed dossiers must remain conservative.
cor = json.loads(COR.read_text(encoding="utf-8"))
assert cor["assessment"]["primary_current_channel79_transmitter_site_confirmed"] is False
assert cor["assessment"]["site_assignment_can_be_promoted"] is False
et = json.loads(ETEL.read_text(encoding="utf-8"))
assert et["assessment"]["channel64_site_confirmed"] is False
assert et["assessment"]["site_assignment_can_be_promoted"] is False

for key, value in e["rules"].items():
    assert value is True, key
assert e["decisions"]["normandie_gate_cleared_count"] == 0
assert e["decisions"]["normandie_candidate_mutated"] is False
assert e["decisions"]["bretagne_site_assignment_promoted"] is False
assert e["decisions"]["public_pack_mutated"] is False
assert e["decisions"]["public_export_allowed"] is False

resume = json.loads(RESUME.read_text(encoding="utf-8"))
normandie_work = resume.get("normandie_v0_5_work", resume["active_work"])
assert resume["current_sprint"] >= 67
assert resume["state_version"] >= "0.21.56"
assert normandie_work["internal_candidate_memory_count"] == 142
assert normandie_work["maximum_internal_memory_count_if_all_current_known_gates_clear"] == 147
assert normandie_work["current_guarded_promotion_plan_eligible_addition_count"] == 0
assert normandie_work["latest_current_reference_synthesis"]["file"] == "research/sprint-67-current-reference-synthesis.json"
assert resume["bretagne_research_update"]["ministry_leisure_guide_2026_pdf_extracted"] is True
assert resume["bretagne_research_update"]["ministry_leisure_guide_2026_names_transmitter_sites"] is False
assert resume["bretagne_research_update"]["corsen_secondary_current_stiff_channel79_clue_exists"] is True
assert resume["resume_rules"]["current_primary_channel_confirmation_without_site_name_does_not_assign_transmitter"] is True
assert resume["resume_rules"]["secondary_source_convergence_does_not_become_primary_validation"] is True
assert resume["resume_rules"]["current_display_badge_does_not_override_dated_verification_provenance"] is True

public_normandie = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv"
rows = list(csv.DictReader(io.StringIO(public_normandie.read_text(encoding="utf-8"))))
assert len(rows) == 139
registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'id: "bretagne"' not in registry

print("Sprint 67 current reference synthesis: 2026 ministry guide confirms channel level only, secondary Ch79 convergence stays non-primary, RepeaterBook display badge cannot override stale provenance, candidate/public packs unchanged OK")
