import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

bretagne_path = ROOT / "research/bretagne-v0.1/analog-coverage-redundancy-review.json"
normandie_path = ROOT / "research/normandie-v0.4/paired-rx-refresh.json"
assert bretagne_path.is_file()
assert normandie_path.is_file()

bretagne = json.loads(bretagne_path.read_text(encoding="utf-8"))
assert bretagne["schema_version"] == "1.2"
assert bretagne["status"] == "research_geometry_redundancy_topology_and_operational_status_review_not_public"
assert bretagne["method"]["distance_is_coverage"] is False
assert bretagne["method"]["altitude_power_gain_are_coverage"] is False
assert bretagne["method"]["independent_site_directory_is_linkage_proof"] is False
assert bretagne["method"]["local_operator_page_preferred_for_operational_status"] is True
cluster = bretagne["cluster_432_650"]
assert cluster["shared_frequency_mhz"] == 432.6500
assert cluster["current_ref_active_site_count"] == 5
assert cluster["current_common_responsible"] == "F6HRP"
assert cluster["current_common_ctcss_hz"] == 71.9
assert cluster["current_primary_shared_frequency_verified"] is True
assert cluster["current_independent_site_set_corroborated"] is True
assert cluster["current_primary_linkage_verified"] is False
assert cluster["current_association_linkage_verified"] is False
assert cluster["historical_secondary_linkage_documented"] is True
assert cluster["topology_status"] == "five_current_sites_and_shared_rf_confirmed_current_interconnection_still_unverified"
assert cluster["locator_span_max_km"] == 90.6
assert set(cluster["max_span_sites"]) == {"F5ZIS Matignon", "F5ZIT Perros-Guirec"}
assert cluster["selection_priority"] == "high_memory_efficiency_research_candidate"
sites = {item["id"]: item for item in cluster["sites"]}
assert set(sites) == {"F5ZIS", "F5ZIT", "F5ZIU", "F5ZIV", "F5ZJR"}
assert sites["F5ZIS"]["vhf_side_mhz"] == 145.2375
assert sites["F5ZIT"]["vhf_side_mhz"] == 145.2250
assert sites["F5ZIU"]["vhf_side_mhz"] == 145.4625
assert sites["F5ZIV"]["vhf_side_mhz"] == 145.4875
assert sites["F5ZJR"]["vhf_side_mhz"] == 145.2875
assert all(item["coverage_claim"] is None for item in sites.values())
checks = {(item["from"], item["to"]): item["distance_km"] for item in cluster["selected_geometry_checks_km"]}
assert checks[("F5ZIS", "F5ZIT")] == 90.6
assert checks[("F5ZIU", "F5ZIV")] == 23.0
assert checks[("F5ZJR", "F5ZIV")] == 26.8
morbihan = bretagne["morbihan_review"]
assert morbihan["F1ZMU"]["pair_mhz"] == [439.7250, 430.3250]
assert morbihan["F1ZMU"]["distance_to_f5zpe_km"] == 19.0
assert morbihan["F1ZMU"]["coverage_claim"] is None
assert morbihan["F1ZBZ"]["new_unique_rf_after_f5zpe_deduplication"] == [431.2000, 145.6250, 145.0250]
assert morbihan["F1ZBZ"]["shared_with_f5zpe_mhz"] == [145.7375, 145.1375]
assert morbihan["F1ZBZ"]["coverage_claim"] is None
rennes = bretagne["rennes_operational_status_reconciliation"]
assert rennes["F5ZEB"]["paired_rx_mhz"] == [431.0750, 438.6750]
assert rennes["F5ZEB"]["local_operator_status"] == "operational_since_2025_09_25_on_temporary_site"
assert rennes["F5ZEB"]["ref_directory_status"] == "arret"
assert rennes["F5ZEB"]["effective_research_status"] == "operational_local_operator_source_preferred"
assert rennes["F5ZEB"]["status_conflict"] is True
assert rennes["F5ZEB"]["coverage_claim"] is None
assert rennes["F5ZEB"]["rx_pack_candidate"] is False
assert rennes["F5ZPV"]["paired_rx_mhz"] == [430.4750, 439.8750]
assert rennes["F5ZPV"]["local_operator_status"] == "temporarily_stopped_no_restart_currently_confirmed"
assert rennes["F5ZPV"]["ref_directory_status"] == "actif"
assert rennes["F5ZPV"]["effective_research_status"] == "stopped_local_operator_source_preferred"
assert rennes["F5ZPV"]["status_conflict"] is True
assert rennes["F5ZPV"]["rx_pack_candidate"] is False
assert rennes["F5ZZH"]["paired_rx_mhz"] == [145.1875, 145.7875]
assert rennes["F5ZZH"]["local_operator_status"] == "temporarily_stopped_searching_new_site"
assert rennes["F5ZZH"]["ref_directory_status"] == "arret"
assert rennes["F5ZZH"]["status_conflict"] is False
assert rennes["F5ZZH"]["rx_pack_candidate"] is False
assert bretagne["recommendations"]["retain_432_650_shared_memory_in_research_plan"] is True
assert bretagne["recommendations"]["retain_all_five_unique_vhf_sides_in_research_plan"] is True
assert bretagne["recommendations"]["retain_f5zeb_pair_as_operational_research_metadata"] is True
assert bretagne["recommendations"]["keep_f5zpv_and_f5zzh_out_of_active_candidates"] is True
assert bretagne["recommendations"]["field_or_propagation_validation_required_before_public_selection"] is True
assert bretagne["rules"]["locator_distance_is_not_radio_coverage"] is True
assert bretagne["rules"]["independent_site_corroboration_is_not_linkage_proof"] is True
assert bretagne["rules"]["historical_secondary_linkage_is_not_current_primary_linkage"] is True
assert bretagne["rules"]["local_operator_current_status_overrides_directory_status_when_conflicting"] is True
assert bretagne["rules"]["directory_status_conflict_is_recorded_not_silently_discarded"] is True
assert bretagne["rules"]["operational_status_does_not_imply_coverage"] is True
assert bretagne["rules"]["stopped_relay_is_not_active_candidate"] is True
assert bretagne["rules"]["public_export_allowed"] is False

normandie = json.loads(normandie_path.read_text(encoding="utf-8"))
assert normandie["schema_version"] == "1.3"
assert normandie["status"] == "current_pair_refresh_with_source_and_operational_reconciliation_research_not_public"
source_authorities = {item["authority"] for item in normandie["sources"]}
assert {"Radio Club Nord Cotentin F6KFW", "ARA50", "Association des Radioamateurs de la Sarthe (ARAS72)", "manuel.la-radio.eu"} <= source_authorities
pairs = {item["id"]: item for item in normandie["resolved_pairs"]}
assert set(pairs) == {"F1ZBL", "F1ZOV", "F5ZHA"}
assert pairs["F1ZBL"]["side_a_rx_mhz"] == 145.2500
assert pairs["F1ZBL"]["side_b_rx_mhz"] == 431.2500
assert pairs["F1ZBL"]["status"] == "current_ref_and_local_club_explicit_bidirectional_pair"
assert pairs["F1ZBL"]["source_reconciliation"]["current_secondary_manual_pair_mhz"] == [145.2500, 431.2500]
assert pairs["F1ZBL"]["source_reconciliation"]["secondary_repeaterbook_conflict_mhz"] == 431.2250
assert pairs["F1ZBL"]["source_reconciliation"]["publication_blocked_by_source_conflict"] is False
assert pairs["F1ZOV"]["side_a_rx_mhz"] == 430.3750
assert pairs["F1ZOV"]["side_b_rx_mhz"] == 431.9750
assert pairs["F1ZOV"]["status"] == "pair_currently_verified_local_operator_marks_station_in_maintenance"
assert pairs["F1ZOV"]["source_reconciliation"]["current_local_operator_status"] == "maintenance"
assert pairs["F1ZOV"]["source_reconciliation"]["current_ref_status"] == "active"
assert pairs["F1ZOV"]["source_reconciliation"]["publication_blocked_by_operational_status"] is True
assert pairs["F5ZHA"]["side_a_rx_mhz"] == 145.4675
assert pairs["F5ZHA"]["side_b_rx_mhz"] == 432.5750
assert pairs["F5ZHA"]["status"] == "current_ref_pair_independently_corroborated_secondary_old_conflict_still_open"
assert pairs["F5ZHA"]["source_reconciliation"]["current_secondary_manual_pair_mhz"] == [145.4675, 432.5750]
assert pairs["F5ZHA"]["source_reconciliation"]["independent_current_index_corroborates_ref_pair"] is True
assert pairs["F5ZHA"]["source_reconciliation"]["secondary_repeaterbook_conflict_mhz"] == 431.4125
assert pairs["F5ZHA"]["source_reconciliation"]["publication_blocked_by_source_conflict"] is True
assert pairs["F5ZHA"]["selection_status"] == "research_pair_retained_publication_local_reconciliation_required"
additional = {item["id"]: item for item in normandie["additional_current_pairs"]}
assert set(additional) == {"F5ZHY", "F6ZCE"}
assert additional["F5ZHY"]["new_side_candidate_mhz"] == 145.0875
assert additional["F6ZCE"]["new_side_candidate_mhz"] == 145.1000
assert [item["id"] for item in normandie["still_unresolved"]] == ["F6ZES"]
assert normandie["still_unresolved"][0]["current_ref_rechecked"] == "2026-08-10"
assert normandie["still_unresolved"][0]["resolution_status"] == "still_unresolved_after_targeted_recheck_2026_08_10"
assert normandie["rules"]["coverage_still_required_before_public_selection"] is True
assert normandie["rules"]["current_primary_or_association_source_preferred_over_old_secondary_directory"] is True
assert normandie["rules"]["current_local_operator_status_preferred_for_operational_state"] is True
assert normandie["rules"]["independent_secondary_corroboration_strengthens_but_does_not_replace_local_validation"] is True
assert normandie["rules"]["secondary_directory_conflict_must_be_reconciled_before_publication"] is True
assert normandie["rules"]["maintenance_blocks_new_side_promotion_until_revalidated"] is True
assert normandie["rules"]["published_normandie_v0_3_1_immutable"] is True
assert normandie["rules"]["public_export_allowed"] is False

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'id: "bretagne"' not in registry
assert 'version: "v0.4"' not in registry

print("Tests analog coverage/redundancy review: Bretagne 432.650 linkage remains unverified, Rennes status conflicts stay conservative, Normandie F1ZBL/F1ZOV/F5ZHA source and operational gates are explicit, no public mutation OK")
