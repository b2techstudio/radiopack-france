import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "research/sprint-66-technical-inventory-boundaries.json"
RESUME = ROOT / "research/project-resume-state.json"
COR = ROOT / "research/bretagne-v0.1/corsen-channel79-evidence.json"
ETEL = ROOT / "research/bretagne-v0.1/etel-channel64-evidence.json"

assert EVIDENCE.is_file()
e = json.loads(EVIDENCE.read_text(encoding="utf-8"))
assert e["sprint"] == 66
assert e["state_version"] == "0.21.55"
assert e["status"] == "technical_inventory_recheck_no_promotion_not_public"
assert e["public_export_allowed"] is False
assert e["candidate_mutation_allowed"] is False

n = e["normandie_v04"]
f5 = n["f5zha"]
assert f5["current_ref_active"] is True
assert f5["paired_rx_frequencies_mhz"] == [145.4675, 432.575]
assert f5["local_association_currently_active_as_association"] is True
assert f5["local_association_current_technical_frequency_publication_found"] is False
assert f5["association_existence_is_frequency_validation"] is False
assert f5["authoritative_source_gate_cleared"] is False
assert f5["mortain_field_gate_cleared"] is False
assert f5["candidate_memory_delta"] == 0

f6 = n["f6zes"]
assert f6["responsible"] == "F1SMB"
assert f6["locator"] == "IN98MR93XV"
assert f6["altitude_m"] == 230
assert f6["frequency_present"] is False
assert f6["mode_present"] is False
assert f6["operational_state_present"] is False
assert f6["second_current_frequency_mode_source_found"] is False
assert f6["must_not_guess_frequency"] is True
assert f6["candidate_memory_delta"] == 0
assert n["gate_cleared_count"] == 0
assert n["candidate_memory_count_before"] == 142
assert n["candidate_memory_count_after"] == 142
assert n["known_ceiling_memory_count"] == 147
assert n["eligible_addition_count"] == 0

b = e["bretagne_v01"]
et = b["cross_etel_technical_maintenance"]
assert et["reference"] == "2026-2341297"
assert et["station_count"] == 17
assert et["mhf_vhf_maintenance_context"] is True
assert et["station_names_listed"] is False
assert et["channels_listed"] is False
assert et["channel64_site_mapping_present"] is False

co = b["cross_corsen_current_infrastructure"]
assert co["director_job_confirms_stiff_radio_communications_equipment"] is True
assert co["place_reference"] == "DGAMPA-SNC1-2025-03_STIFF"
assert co["place_confirms_current_stiff_renovation_project"] is True
assert co["channel79_mapping_present"] is False
assert co["current_channel79_transmitter_site_confirmed"] is False

chain = b["corsen_secondary_full_chain_clue"]
assert chain["reported_channel"] == 79
assert chain["reported_sites"] == ["Cap Fréhel", "Bodic", "Batz", "Stiff", "Pointe du Raz"]
assert chain["publication_date_visible"] is False
assert chain["can_validate_current_primary_site_assignment"] is False
hist = b["corsen_historical_primary"]
assert hist["channels79_and80_documented"] is True
assert hist["current_2026_site_channel_validation"] is False

guide = b["meteofrance_guide_marine_2026"]
assert guide["landing_page_date"] == "2026-08-05"
assert guide["fetch_result"] == "cache_miss"
assert guide["pdf_content_extracted"] is False
assert guide["pdf_screenshot_available"] is False
assert guide["channel64_inference"] is False
assert guide["channel79_site_inference"] is False

assert b["etel_channel64_pair_rx_frequencies_mhz"] == [156.225, 160.825]
assert b["etel_channel64_required_rx_memory_count_if_published"] == 2
assert b["corsen_channel79_pair_rx_frequencies_mhz"] == [156.975, 161.575]
assert b["corsen_channel79_required_rx_memory_count_if_published"] == 2
assert b["new_site_assignment_count"] == 0
assert b["new_rf_memory_delta"] == 0
assert b["public_promotion_allowed"] is False

corsen = json.loads(COR.read_text(encoding="utf-8"))
assert corsen["schema_version"] == "1.2"
assert corsen["assessment"]["primary_current_channel79_transmitter_site_confirmed"] is False
assert corsen["assessment"]["secondary_undated_full_chain_sites"] == ["Cap Fréhel", "Bodic", "Batz", "Stiff / Ouessant", "Pointe du Raz"]
assert corsen["assessment"]["secondary_undated_full_chain_is_current_primary_validation"] is False
assert corsen["rules"]["current_infrastructure_procurement_does_not_imply_channel_assignment"] is True

etel = json.loads(ETEL.read_text(encoding="utf-8"))
assert etel["schema_version"] == "1.1"
assert etel["assessment"]["current_technical_maintenance_scope_17_stations_verified"] is True
assert etel["assessment"]["technical_maintenance_scope_names_channels"] is False
assert etel["rules"]["current_maintenance_scope_does_not_name_station_channels"] is True

for key, value in e["rules"].items():
    assert value is True, key
assert e["decisions"]["normandie_gate_cleared_count"] == 0
assert e["decisions"]["normandie_candidate_mutated"] is False
assert e["decisions"]["bretagne_site_assignment_promoted"] is False
assert e["decisions"]["public_pack_mutated"] is False
assert e["decisions"]["public_export_allowed"] is False

resume = json.loads(RESUME.read_text(encoding="utf-8"))
assert resume["current_sprint"] == 66
assert resume["state_version"] == "0.21.55"
assert resume["active_work"]["internal_candidate_memory_count"] == 142
assert resume["active_work"]["maximum_internal_memory_count_if_all_current_known_gates_clear"] == 147
assert resume["active_work"]["current_guarded_promotion_plan_eligible_addition_count"] == 0
assert resume["active_work"]["latest_technical_inventory_recheck"]["file"] == "research/sprint-66-technical-inventory-boundaries.json"
assert resume["bretagne_research_update"]["etel_2026_technical_maintenance_station_count"] == 17
assert resume["bretagne_research_update"]["corsen_secondary_undated_full_chain_is_current_primary_validation"] is False
for key in [
    "current_maintenance_scope_does_not_name_station_channels",
    "association_existence_does_not_validate_repeater_frequency",
    "undated_secondary_schedule_is_not_current_primary_validation",
    "current_infrastructure_procurement_does_not_assign_channel",
]:
    assert resume["resume_rules"][key] is True

public_normandie = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv"
rows = list(csv.DictReader(io.StringIO(public_normandie.read_text(encoding="utf-8"))))
assert len(rows) == 139
registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'version: "v0.4"' not in registry
assert 'id: "bretagne"' not in registry

print("Sprint 66 technical inventory boundaries: Etel 17-station maintenance scope remains unnamed by channel, Corsen full secondary Ch79 chain stays non-primary, Stiff infrastructure does not assign Ch79, Normandie gates and public packs unchanged OK")
