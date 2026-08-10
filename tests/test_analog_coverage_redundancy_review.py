import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

bretagne_path = ROOT / "research/bretagne-v0.1/analog-coverage-redundancy-review.json"
normandie_path = ROOT / "research/normandie-v0.4/paired-rx-refresh.json"
assert bretagne_path.is_file()
assert normandie_path.is_file()

bretagne = json.loads(bretagne_path.read_text(encoding="utf-8"))
assert bretagne["schema_version"] == "1.0"
assert bretagne["status"] == "research_geometry_and_redundancy_review_not_public"
assert bretagne["method"]["distance_is_coverage"] is False
assert bretagne["method"]["altitude_power_gain_are_coverage"] is False
cluster = bretagne["cluster_432_650"]
assert cluster["shared_frequency_mhz"] == 432.6500
assert cluster["current_ref_active_site_count"] == 5
assert cluster["current_common_responsible"] == "F6HRP"
assert cluster["current_common_ctcss_hz"] == 71.9
assert cluster["current_primary_shared_frequency_verified"] is True
assert cluster["current_primary_linkage_verified"] is False
assert cluster["historical_secondary_linkage_documented"] is True
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
assert bretagne["recommendations"]["retain_432_650_shared_memory_in_research_plan"] is True
assert bretagne["recommendations"]["retain_all_five_unique_vhf_sides_in_research_plan"] is True
assert bretagne["recommendations"]["field_or_propagation_validation_required_before_public_selection"] is True
assert bretagne["rules"]["locator_distance_is_not_radio_coverage"] is True
assert bretagne["rules"]["historical_secondary_linkage_is_not_current_primary_linkage"] is True
assert bretagne["rules"]["public_export_allowed"] is False

normandie = json.loads(normandie_path.read_text(encoding="utf-8"))
assert normandie["schema_version"] == "1.0"
assert normandie["status"] == "current_ref_pair_refresh_research_not_public"
pairs = {item["id"]: item for item in normandie["resolved_pairs"]}
assert set(pairs) == {"F1ZBL", "F5ZHA"}
assert pairs["F1ZBL"]["side_a_rx_mhz"] == 145.2500
assert pairs["F1ZBL"]["side_b_rx_mhz"] == 431.2500
assert pairs["F1ZBL"]["status"] == "current_ref_active_explicit_bidirectional_rows"
assert pairs["F5ZHA"]["side_a_rx_mhz"] == 145.4675
assert pairs["F5ZHA"]["side_b_rx_mhz"] == 432.5750
assert pairs["F5ZHA"]["status"] == "current_ref_active_explicit_pair"
assert [item["id"] for item in normandie["still_unresolved"]] == ["F6ZES"]
assert normandie["rules"]["coverage_still_required_before_public_selection"] is True
assert normandie["rules"]["published_normandie_v0_3_1_immutable"] is True
assert normandie["rules"]["public_export_allowed"] is False

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'id: "bretagne"' not in registry
assert 'version: "v0.4"' not in registry

print("Tests analog coverage/redundancy review: Bretagne 432.650 five-site geometry guarded without coverage inference, F1ZMU/F1ZBZ redundancy reviewed, Normandie F1ZBL/F5ZHA pairs resolved, no public mutation OK")
