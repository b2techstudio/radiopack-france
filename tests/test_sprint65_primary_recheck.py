import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "research/sprint-65-primary-recheck.json"
RESUME = ROOT / "research/project-resume-state.json"

assert EVIDENCE.is_file(), f"Missing Sprint 65 evidence: {EVIDENCE}"
evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
assert evidence["sprint"] == 65
assert evidence["state_version"] == "0.21.54"
assert evidence["status"] == "primary_recheck_no_promotion_not_public"
assert evidence["public_export_allowed"] is False
assert evidence["candidate_mutation_allowed"] is False

normandie = evidence["normandie_v04"]
f5zha = normandie["f5zha"]
assert f5zha["current_page_shows_active"] is True
assert f5zha["paired_rx_frequencies_mhz"] == [145.4675, 432.575]
assert f5zha["local_operator_or_equivalent_authoritative_reconciliation_found"] is False
assert f5zha["authoritative_source_gate_cleared"] is False
assert f5zha["mortain_field_gate_cleared"] is False
assert f5zha["candidate_memory_delta"] == 0

f6zes = normandie["f6zes"]
assert f6zes["responsible"] == "F1SMB"
assert f6zes["locator"] == "IN98MR93XV"
assert f6zes["altitude_m"] == 230
assert f6zes["frequency_present_in_current_source"] is False
assert f6zes["mode_present_in_current_source"] is False
assert f6zes["operational_state_present_in_current_source"] is False
assert f6zes["frequency_mode_resolved"] is False
assert f6zes["candidate_memory_delta"] == 0
assert f6zes["must_not_guess_frequency"] is True
assert normandie["gate_cleared_count"] == 0
assert normandie["candidate_memory_count_before"] == 142
assert normandie["candidate_memory_count_after"] == 142
assert normandie["known_ceiling_memory_count"] == 147
assert normandie["eligible_addition_count"] == 0

bretagne = evidence["bretagne_v01"]
ministry = bretagne["ministry_current_vhf_statement"]
assert ministry["page_updated"] == "2026-06-19"
assert ministry["channel16_announces_79_and_80"] is True
assert ministry["channels63_and64_permanent_coastal_weather_in_morbihan"] is True
assert ministry["channel64_transmitter_site_named"] is False
assert ministry["regional_channel_statement_is_site_assignment"] is False

etel = bretagne["cross_etel_current"]
assert etel["page_updated"] == "2025-11-24"
assert etel["scheduled_weather_call_on_16_then_79_or80"] is True
assert etel["etel_and_chassiron_continuous_channel63"] is True
assert etel["channel64_site_named"] is False
assert etel["channel64_current_operation_proven_by_this_source"] is False
assert etel["channel64_stopped_proven_by_this_source"] is False

corsen = bretagne["cross_corsen_current"]
assert corsen["page_updated"] == "2026-03-24"
assert corsen["permanent_vhf_mhf_network_confirmed"] is True
assert corsen["weather_from_coastal_vhf_mhf_stations_confirmed"] is True
assert corsen["channel79_site_mapping_present"] is False
assert corsen["current_channel79_transmitter_site_confirmed"] is False

frehel = bretagne["cap_frehel_current_infrastructure"]
assert frehel["cross_tracking_and_ship_liaison_equipment_confirmed"] is True
assert frehel["channel79_assignment_confirmed"] is False

guide = bretagne["meteofrance_guide_marine_2026"]
assert guide["landing_page_date"] == "2026-08-05"
assert guide["landing_page_says_guide_contains_radio_frequencies_and_vhf_schedules"] is True
assert guide["direct_pdf_identified"] is True
assert guide["pdf_fetch_retried_on"] == "2026-08-11"
assert guide["pdf_content_extracted"] is False
assert guide["pdf_screenshot_available"] is False
assert guide["failure"] == "cache_miss"
assert guide["channel64_inference_from_unread_pdf"] is False
assert guide["channel79_site_inference_from_unread_pdf"] is False

assert bretagne["etel_channel64_pair_rx_frequencies_mhz"] == [156.225, 160.825]
assert bretagne["etel_channel64_required_rx_memory_count_if_published"] == 2
assert bretagne["corsen_channel79_pair_rx_frequencies_mhz"] == [156.975, 161.575]
assert bretagne["corsen_channel79_required_rx_memory_count_if_published"] == 2
assert bretagne["new_site_assignment_count"] == 0
assert bretagne["new_rf_memory_delta"] == 0
assert bretagne["public_promotion_allowed"] is False

for key, value in evidence["rules"].items():
    assert value is True, f"Sprint 65 rule must remain enabled: {key}"

assert evidence["decisions"]["normandie_gate_cleared_count"] == 0
assert evidence["decisions"]["normandie_candidate_mutated"] is False
assert evidence["decisions"]["bretagne_site_assignment_promoted"] is False
assert evidence["decisions"]["public_pack_mutated"] is False
assert evidence["decisions"]["public_export_allowed"] is False

resume = json.loads(RESUME.read_text(encoding="utf-8"))
assert resume["current_sprint"] == 65
assert resume["state_version"] == "0.21.54"
assert resume["active_work"]["internal_candidate_memory_count"] == 142
assert resume["active_work"]["maximum_internal_memory_count_if_all_current_known_gates_clear"] == 147
assert resume["active_work"]["current_guarded_promotion_plan_eligible_addition_count"] == 0
assert resume["active_work"]["public_release_ready"] is False
assert resume["resume_rules"]["current_regional_channel_statement_does_not_identify_transmitter_site"] is True
assert resume["resume_rules"]["current_cross_network_statement_does_not_map_channel_to_station"] is True

public_normandie = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv"
rows = list(csv.DictReader(io.StringIO(public_normandie.read_text(encoding="utf-8"))))
assert len(rows) == 139
registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'version: "v0.4"' not in registry
assert 'id: "bretagne"' not in registry

print(
    "Sprint 65 primary recheck: current Ministry/DIRM statements refresh channel/network context without inventing sites; "
    "F5ZHA remains source+field gated, F6ZES unresolved, Ch64/Ch79 keep two RX memories if eventually publishable, public packs unchanged OK"
)
