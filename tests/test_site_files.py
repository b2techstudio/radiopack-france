import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required_files = [
    "README.md",
    "PROJECT_STATUS.md",
    ".gitignore",
    ".github/workflows/ci.yml",
    "REGIONAL-PACK-WORKFLOW.md",
    "SPRINT-23-MULTI-REGION-GENERATOR.md",
    "SPRINT-24-ISOLATED-GENERATOR-TESTS.md",
    "SPRINT-25-REGIONAL-STARTER.md",
    "SPRINT-26-BRETAGNE-INITIALIZATION.md",
    "SPRINT-27-BRETAGNE-MARITIME-ZONING.md",
    "SPRINT-28-EMERGENCY-ADRASEC-RESEARCH.md",
    "SPRINT-29-MORTAIN-BRETAGNE-RADIO-RESEARCH.md",
    "generator/options.json",
    "generator/generate_chirp_csv.py",
    "tools/create_regional_pack.py",
    "tools/build_normandie_v04_internal_candidate.py",
    "tools/build_normandie_v04_r3_validation_pack.py",
    "tools/record_normandie_v04_r3_observation.py",
    "tools/check_normandie_v04_promotion_gates.py",
    "tools/build_normandie_v04_gate_report.py",
    "tools/build_normandie_v04_f5zha_validation_pack.py",
    "tools/build_normandie_v04_readiness_report.py",
    "tools/build_normandie_v04_promotion_scenarios.py",
    "tools/run_normandie_v04_checks.py",
    "tests/test_generator.py",
    "tests/test_regional_pack_starter.py",
    "tests/test_paired_rx_policy.py",
    "tests/test_bretagne_research_scaffold.py",
    "tests/test_emergency_relay_research.py",
    "tests/test_mortain_bretagne_radio_research.py",
    "tests/test_web_generator.py",
    "tests/test_pack_registry.py",
    "tests/test_built_public_pack_catalog.py",
    "tests/test_normandie_v04_candidate_delta.py",
    "tests/test_normandie_v04_internal_candidate.py",
    "tests/test_normandie_v04_promotion_gates.py",
    "tests/test_normandie_v04_field_tools.py",
    "tests/test_normandie_v04_readiness.py",
    "research/project-resume-state.json",
    "research/paired-rx-policy.json",
    "research/paired-rx-next-version-plan.json",
    "research/emergency-radio-policy.json",
    "research/sprint-30-34-summary.md",
    "research/sprint-35-39-summary.md",
    "research/bretagne-v0.1/README.md",
    "research/bretagne-v0.1/pack-plan.json",
    "research/bretagne-v0.1/source-registry.json",
    "research/bretagne-v0.1/publication-gates.json",
    "research/bretagne-v0.1/memory-plan.json",
    "research/bretagne-v0.1/maritime-zones.json",
    "research/bretagne-v0.1/emergency-relays.json",
    "research/bretagne-v0.1/public-maritime-radio.json",
    "research/normandie-v0.4/README.md",
    "research/normandie-v0.4/pack-plan.json",
    "research/normandie-v0.4/emergency-relays.json",
    "research/normandie-v0.4/mortain-bocage-coverage.json",
    "research/normandie-v0.4/candidate-memory-delta.json",
    "research/normandie-v0.4/internal-candidate-map.json",
    "research/normandie-v0.4/promotion-gates.json",
    "research/normandie-v0.4/blocked-station-revalidation.json",
    "research/normandie-v0.4/r3-mortain-field-validation.json",
    "research/normandie-v0.4/r3-validation-pack.json",
    "research/normandie-v0.4/f5zha-mortain-validation.json",
    "research/annecy-alpes-leman-v0.3/README.md",
    "research/annecy-alpes-leman-v0.3/pack-plan.json",
    "research/annecy-alpes-leman-v0.3/emergency-relays.json",
    "research/annecy-alpes-leman-v0.2/prepublication-plan.json",
    "research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json",
    "website/src/lib/chirpPack.ts",
    "website/src/lib/annecyPack.ts",
    "website/src/lib/packRegistry.ts",
    "website/src/pages/generateur.astro",
    "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv.ts",
    "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv.ts",
    "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv",
    "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv",
    "research/normandie-v0.4/publication-record.json",
    "research/normandie-v0.5/README.md",
    "research/normandie-v0.5/pack-plan.json",
    "research/normandie-v0.5/backlog.json",
    "tests/test_normandie_v04_public_release.py",
    "tests/test_normandie_v05_initialization.py",
    "research/sprint-68-summary.md",
    "research/sprint-69-summary.md",
    "research/sprint-70-summary.md",
]
for relative in required_files:
    path = ROOT / relative
    assert path.is_file(), f"Fichier manquant: {relative}"
    assert path.stat().st_size > 20, f"Fichier vide ou incomplet: {relative}"

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for expected in [
    "État actuel — Sprint 39",
    "Normandie v0.4** — 142 mémoires RX",
    "Annecy–Alpes–Léman v0.2** — 65 mémoires RX",
    "Bretagne v0.1",
    "Normandie v0.4",
    "142 mémoires",
    "147 mémoires",
    "Mortain-Bocage / Sud-Manche",
    "research/paired-rx-policy.json",
    "Duplex=off",
    "Offset=0.000000",
    "research/normandie-v0.4/mortain-bocage-coverage.json",
    "sourdeval_must_not_be_guessed: true",
    "F5ZHY",
    "F6ZES",
    "F6ZCE",
    "F1ZBX",
    "F5ZHA",
    "F1ZOV",
    "research/normandie-v0.4/f5zha-mortain-validation.json",
    "build_normandie_v04_readiness_report.py",
    "build_normandie_v04_promotion_scenarios.py",
    "research/bretagne-v0.1/public-maritime-radio.json",
    "tests\\test_paired_rx_policy.py",
    "tests\\test_mortain_bretagne_radio_research.py",
    "tests\\test_normandie_v04_readiness.py",
    "SPRINT-29-MORTAIN-BRETAGNE-RADIO-RESEARCH.md",
    "research/sprint-30-34-summary.md",
    "research/sprint-35-39-summary.md",
    "nothing to commit, working tree clean",
    "Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint",
]:
    assert expected in readme, f"README non actualisé: {expected}"

gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
assert "research/annecy-alpes-leman-v0.2/generated/" in gitignore
assert "research/normandie-v0.4/generated/" in gitignore
assert "__pycache__/" in gitignore
assert "*.py[cod]" in gitignore

options = json.loads((ROOT / "generator/options.json").read_text(encoding="utf-8"))
assert options["schema_version"] == "3.0"
assert options["status"] == "multi_region_public_generator"
assert options["implementation"]["published_pack_count"] == 2
assert options["implementation"]["public_pack_registry"] == "website/src/lib/packRegistry.ts"
assert {pack["id"] for pack in options["pack_selection"]["packs"]} == {"annecy-alpes-leman", "normandie"}
assert options["options"]["notam_check"]["affects_csv_content"] is False
assert options["options"]["notam_check"]["blocks_generation"] is False

paired_policy = json.loads((ROOT / "research/paired-rx-policy.json").read_text(encoding="utf-8"))
paired_plan = json.loads((ROOT / "research/paired-rx-next-version-plan.json").read_text(encoding="utf-8"))
assert paired_policy["status"] == "active_project_policy"
assert paired_policy["core_rule"]["native_duplex_or_split_pair_exports_both_rx_frequencies"] is True
assert paired_policy["core_rule"]["tx_disabled"] is True
assert paired_policy["core_rule"]["chirp_duplex"] == "off"
assert paired_policy["core_rule"]["chirp_offset"] == "0.000000"
assert paired_policy["deduplication"]["same_rf_frequency_kept_once_per_pack"] is True
assert paired_plan["status"] == "research_plan_not_public"
assert paired_plan["export_contract"]["tx_disabled"] is True
assert paired_plan["export_contract"]["two_rx_memories_when_pair_frequencies_differ"] is True
assert paired_plan["export_contract"]["public_pack_mutation_allowed"] is False
assert {item["id"] for item in paired_plan["regions"]} == {"normandie-v0.4", "annecy-alpes-leman-v0.3", "bretagne-v0.1"}

policy = json.loads((ROOT / "research/emergency-radio-policy.json").read_text(encoding="utf-8"))
assert policy["schema_version"] == "1.1"
assert policy["status"] == "active_research_policy"
assert policy["paired_rx_policy"] == "research/paired-rx-policy.json"
assert policy["publication_rules"]["rx_only"] is True
assert policy["publication_rules"]["duplex"] == "off"
assert policy["publication_rules"]["offset"] == "0.000000"
assert policy["publication_rules"]["native_duplex_or_split_both_directions_rx"] is True
assert policy["publication_rules"]["paired_distinct_frequencies_use_separate_rx_memories"] is True
assert policy["publication_rules"]["same_rf_frequency_deduplicated"] is True
assert policy["publication_rules"]["no_private_operational_channel"] is True
assert policy["publication_rules"]["published_versions_are_immutable"] is True
assert policy["per_region_rules"]["normandie"]["priority_focus"] == "Mortain-Bocage / Sud-Manche"
assert policy["per_region_rules"]["normandie"]["adjacent_departments_to_check"] == [35, 53, 61]

bretagne_plan = json.loads((ROOT / "research/bretagne-v0.1/pack-plan.json").read_text(encoding="utf-8"))
bretagne_sources = json.loads((ROOT / "research/bretagne-v0.1/source-registry.json").read_text(encoding="utf-8"))
bretagne_gates = json.loads((ROOT / "research/bretagne-v0.1/publication-gates.json").read_text(encoding="utf-8"))
bretagne_memory = json.loads((ROOT / "research/bretagne-v0.1/memory-plan.json").read_text(encoding="utf-8"))
bretagne_maritime = json.loads((ROOT / "research/bretagne-v0.1/maritime-zones.json").read_text(encoding="utf-8"))
bretagne_emergency = json.loads((ROOT / "research/bretagne-v0.1/emergency-relays.json").read_text(encoding="utf-8"))
bretagne_public_maritime = json.loads((ROOT / "research/bretagne-v0.1/public-maritime-radio.json").read_text(encoding="utf-8"))

assert bretagne_plan["schema_version"] == "1.2"
assert bretagne_plan["status"] == "internal_candidate_in_progress_not_public"
assert bretagne_plan["paired_rx_policy"] == "research/paired-rx-policy.json"
assert bretagne_plan["rules"]["native_duplex_or_split_both_directions_rx"] is True
assert bretagne_plan["rules"]["paired_distinct_frequencies_use_separate_rx_memories"] is True
assert bretagne_plan["rules"]["same_rf_frequency_deduplicated"] is True
assert bretagne_plan["memory_plan"]["expected_memory_count"] == 135
assert len(bretagne_plan["memory_plan"]["blocks"]) == 5
assert bretagne_plan["publication"]["public_export_allowed"] is False
assert bretagne_plan["publication"]["public_registry_allowed"] is False
assert bretagne_plan["publication"]["public_routes_allowed"] is False
assert bretagne_sources["status"] == "seed_sources_identified_maritime_zoning_in_progress_no_frequency_extraction"
assert len(bretagne_sources["sources"]) == 10
assert all(source["frequency_data_promoted"] is False for source in bretagne_sources["sources"])
assert bretagne_sources["rules"]["maritime_cross_assignment_must_be_zone_specific"] is True
assert bretagne_sources["rules"]["exact_current_srr_boundary_required_before_publication"] is True
assert bretagne_gates["status"] == "internal_candidate_built_publication_still_blocked"
assert bretagne_gates["public_release_allowed"] is False
assert len(bretagne_gates["gates"]) == 8
bretagne_gate_map = {gate["id"]: gate for gate in bretagne_gates["gates"]}
assert bretagne_gate_map["memory_plan"]["status"] == "passed_internal_candidate_135_not_public"
assert all(not gate["status"].startswith("passed_") for gate in bretagne_gates["gates"] if gate["id"] != "memory_plan")
assert bretagne_gate_map["maritime_zoning"]["status"] == "generic_channel_frequencies_validated_local_site_mapping_pending"
assert bretagne_gate_map["emergency_relay_inventory"]["status"] == "adrasec_22_29_35_56_and_regional_relays_pending"
assert bretagne_memory["expected_memory_count"] == 135
assert len(bretagne_memory["blocks"]) == 6

assert bretagne_maritime["schema_version"] == "1.5"
assert bretagne_maritime["status"] == "research_zoning_penmarch_interface_confirmed_vhf_overlap_pending"
assert bretagne_maritime["rules"]["single_bretagne_maritime_zone_forbidden"] is True
assert bretagne_maritime["rules"]["north_south_operational_split_required"] is True
assert bretagne_maritime["rules"]["etel_srr_starts_at_pointe_de_penmarch_primary_sourced"] is True
assert bretagne_maritime["rules"]["corsen_srr_ends_at_pointe_de_penmarch_primary_sourced"] is True
assert bretagne_maritime["rules"]["srr_boundary_endpoints_do_not_imply_radio_overlap"] is True
assert bretagne_maritime["rules"]["corsen_stiff_radio_infrastructure_primary_sourced"] is True
assert bretagne_maritime["rules"]["current_radio_infrastructure_does_not_imply_channel_assignment"] is True
assert bretagne_maritime["rules"]["current_sector_vhf_contact_does_not_identify_transmitter_site"] is True
assert bretagne_maritime["rules"]["planned_cross_ng_reorganisation_does_not_change_current_frequency_validation"] is True
assert bretagne_maritime["rules"]["corsen_detailed_srr_and_vhf_overlap_still_pending"] is True
assert bretagne_maritime["channel_16"]["memory_strategy"] == "do_not_duplicate_same_frequency_only_to_label_cross"
assert bretagne_maritime["channel_16"]["frequency_promoted"] is False
zones = {zone["id"]: zone for zone in bretagne_maritime["zones"]}
north = zones["bretagne-nord-ouest"]
assert north["cross"] == "CROSS Corsen"
assert north["official_extent"] == "Baie du Mont-Saint-Michel (Ille-et-Vilaine) à la pointe de Penmarc'h (Finistère)"
assert north["official_srr_area_approx_km2"] == 50000
assert north["current_operational_center"]["site"] == "Pointe de Corsen / Plouarzel"
assert north["current_operational_center"]["radio_service_or_channel"] is None
assert north["current_operational_coverage_evidence"][0]["sector"].startswith("Pointe du Raz")
assert north["current_operational_coverage_evidence"][0]["transmitter_site_identified"] is False
assert north["current_transition_context"]["target_operational_horizon"] == "2027"
assert zones["bretagne-sud-atlantique"]["cross"] == "CROSS Etel"
assert zones["bretagne-sud-atlantique"]["official_extent"].startswith("Pointe de Penmarc'h")
assert zones["transition-finistere-sud"]["cross"] is None
assert zones["transition-finistere-sud"]["status"] == "corsen_srr_end_and_etel_srr_start_at_penmarch_primary_confirmed_vhf_overlap_pending"

assert bretagne_emergency["schema_version"] == "1.4"
assert {item["id"] for item in bretagne_emergency["organisations"]} == {"ADRASEC-22", "ADRASEC-29", "ADRASEC-35", "ADRASEC-56"}
assert all(item["frequency_promoted_to_public_pack"] is False for item in bretagne_emergency["candidates"])
assert bretagne_emergency["rules"]["private_ppdr_operational_frequencies_excluded"] is True
assert bretagne_emergency["rules"]["north_south_zoning_required"] is True
assert bretagne_emergency["rules"]["adrasec_role_must_not_be_inferred_from_geography_only"] is True
assert bretagne_emergency["rules"]["temporarily_stopped_repeaters_not_active_candidates"] is True
brelays = {item["id"]: item for item in bretagne_emergency["candidates"]}
assert brelays["F5ZZH"]["output_mhz"] == 145.7875
assert brelays["F5ZZH"]["input_mhz"] == 145.1875
assert brelays["F5ZZH"]["rx_pack_candidate"] is False
assert brelays["F5ZIS"]["output_mhz"] == 145.2375
assert brelays["F5ZIT"]["output_mhz"] == 145.2250
assert brelays["F1ZBZ"]["output_mhz"] == 431.2000
assert brelays["F5ZPE"]["output_mhz"] == 145.7375

assert bretagne_public_maritime["schema_version"] == "1.7"
assert bretagne_public_maritime["status"] == "official_channel_frequencies_and_etel_weather_emitters_verified_corsen_sites_pending"
assert bretagne_public_maritime["paired_rx_policy"] == "research/paired-rx-policy.json"
maritime_channels = {item["channel"]: item for item in bretagne_public_maritime["channels"]}
assert maritime_channels[16]["rx_memory_mhz"] == 156.8000
assert len(maritime_channels[16]["rx_memories"]) == 1
expected_pairs = {
    63: (156.1750, 160.7750),
    64: (156.2250, 160.8250),
    79: (156.9750, 161.5750),
    80: (157.0250, 161.6250),
}
for number, (ship_side, coast_side) in expected_pairs.items():
    channel = maritime_channels[number]
    assert channel["ship_tx_mhz"] == ship_side
    assert channel["coast_tx_ship_rx_mhz"] == coast_side
    assert len(channel["rx_memories"]) == 2
    by_direction = {item["direction"]: item["frequency_mhz"] for item in channel["rx_memories"]}
    assert by_direction == {"ship_to_coast": ship_side, "coast_to_ship": coast_side}
assert maritime_channels[79]["historical_corsen_primary_status"] == "channel_79_weather_broadcast_documented_in_2003_requires_current_transmitter_revalidation"
assert maritime_channels[79]["zone_assignment"] == "corsen_current_channel_79_emitter_pending_etel_brittany_schedule_has_no_channel_79_site"
assert maritime_channels[80]["verified_etel_brittany_emitters"] == ["Penmarc'h", "Groix", "Belle-Ile"]
assert maritime_channels[63]["verified_etel_brittany_emitters"] == ["Etel"]
assert maritime_channels[64]["current_ministry_statement_revalidated_2026"] is True
assert maritime_channels[64]["zone_assignment"] == "current_brittany_transmitter_requires_primary_reconciliation"
assert all(item["frequency_promoted_to_public_pack"] is False for item in bretagne_public_maritime["channels"])
assert bretagne_public_maritime["rules"]["rx_only_duplex_channels_include_both_ship_and_coast_frequencies"] is True
assert bretagne_public_maritime["rules"]["paired_distinct_frequencies_use_separate_rx_memories"] is True
assert bretagne_public_maritime["rules"]["all_exported_memories_tx_disabled"] is True
assert bretagne_public_maritime["rules"]["same_rf_frequency_deduplicated"] is True
assert bretagne_public_maritime["rules"]["channel_16_not_duplicated_by_cross_label"] is True
assert bretagne_public_maritime["rules"]["historical_primary_radio_sites_must_be_revalidated_before_current_use"] is True
assert bretagne_public_maritime["rules"]["current_radio_infrastructure_does_not_imply_current_channel_assignment"] is True
assert bretagne_public_maritime["rules"]["current_sector_vhf_contact_does_not_identify_transmitter_site"] is True
assert bretagne_public_maritime["rules"]["current_operational_center_does_not_imply_local_radio_station"] is True
assert bretagne_public_maritime["rules"]["planned_cross_ng_reorganisation_does_not_change_current_frequency_validation"] is True
assert bretagne_public_maritime["rules"]["etel_srr_starts_at_penmarch_primary_verified"] is True
assert bretagne_public_maritime["rules"]["corsen_srr_from_mont_saint_michel_to_penmarch_primary_verified"] is True
assert bretagne_public_maritime["rules"]["srr_boundary_endpoints_do_not_imply_radio_overlap"] is True
assert bretagne_public_maritime["rules"]["channel_64_requires_current_brittany_transmitter_reconciliation"] is True
assert bretagne_public_maritime["rules"]["corsen_stiff_radio_infrastructure_primary_verified"] is True
assert bretagne_public_maritime["rules"]["corsen_pointe_du_raz_sector_vhf_coverage_primary_verified_site_pending"] is True
assert bretagne_public_maritime["rules"]["corsen_current_network_size_known_site_names_partially_revalidated"] is True
assert bretagne_public_maritime["rules"]["public_export_allowed"] is False
crosses = {item["cross"]: item for item in bretagne_public_maritime["cross_zones"]}
corsen = crosses["CROSS Corsen"]
assert corsen["official_srr_extent"] == "Baie du Mont-Saint-Michel (Ille-et-Vilaine) à la pointe de Penmarc'h (Finistère)"
assert corsen["official_srr_area_approx_km2"] == 50000
assert corsen["current_operational_center"]["site"] == "Pointe de Corsen / Plouarzel"
assert corsen["current_operational_center"]["radio_service_or_channel"] is None
assert corsen["current_network_summary"]["vhf_station_count"] == 10
assert corsen["current_network_summary"]["mf_station_count"] == 2
assert corsen["remote_vhf_sites"] == []
assert corsen["remote_vhf_sites_status"] == "official_current_channelled_vhf_site_inventory_pending"
corsen_infra = {item["site"]: item for item in corsen["verified_remote_radio_infrastructure_sites"]}
assert set(corsen_infra) == {"Cap Fréhel", "Stiff / Ouessant"}
assert corsen_infra["Cap Fréhel"]["radio_service_or_channel"] is None
assert corsen_infra["Stiff / Ouessant"]["radio_service_or_channel"] is None
coverage = corsen["current_operational_coverage_evidence"]
assert coverage[0]["evidence_date"] == "2025-09-21"
assert coverage[0]["transmitter_site_identified"] is False
assert coverage[0]["channel_identified"] is False
assert corsen["current_transition_context"]["target_operational_horizon"] == "2027"
historical_sites = {item["site"]: item for item in corsen["historical_primary_radio_architecture"]}
assert set(historical_sites) == {"Stiff / Ouessant", "Pointe du Raz", "Corsen"}
assert historical_sites["Stiff / Ouessant"]["current_validation"] is True
assert historical_sites["Pointe du Raz"]["current_validation"] is False
assert historical_sites["Pointe du Raz"]["current_sector_vhf_coverage_verified"] is True
assert historical_sites["Corsen"]["current_validation"] is False
assert historical_sites["Corsen"]["current_main_operational_center_verified"] is True
etel_sites = {item["site"]: item for item in crosses["CROSS Etel"]["remote_vhf_sites"]}
assert set(etel_sites) == {"Penmarc'h", "Groix", "Belle-Ile", "Etel"}
assert etel_sites["Etel"]["channel"] == 63

normandie_next = json.loads((ROOT / "research/normandie-v0.4/pack-plan.json").read_text(encoding="utf-8"))
normandie_emergency = json.loads((ROOT / "research/normandie-v0.4/emergency-relays.json").read_text(encoding="utf-8"))
mortain_coverage = json.loads((ROOT / "research/normandie-v0.4/mortain-bocage-coverage.json").read_text(encoding="utf-8"))
assert normandie_next["schema_version"] == "1.1"
assert normandie_next["status"] == "research_next_version_not_public"
assert normandie_next["based_on_published_version"] == "0.3.1"
assert normandie_next["published_base_is_immutable"] is True
assert normandie_next["paired_rx"]["published_v0_3_1_maritime_pair_model_already_compliant"] is True
assert normandie_next["paired_rx"]["future_analog_repeaters_and_transponders_include_both_verified_sides"] is True
assert normandie_next["priority_focus"]["label"] == "Mortain-Bocage / Sud-Manche"
assert normandie_next["priority_focus"]["adjacent_departments_to_check"] == [35, 53, 61]
assert normandie_next["memory_plan"]["internal_candidate_memory_count"] == 142
assert normandie_next["memory_plan"]["maximum_internal_memory_count_if_all_current_known_gates_clear"] == 147
assert normandie_next["memory_plan"]["f6zes_excluded_from_known_gate_count_until_frequency_resolved"] is True
assert normandie_next["memory_plan"]["f5zha_validation_file"] == "research/normandie-v0.4/f5zha-mortain-validation.json"
assert normandie_next["memory_plan"]["readiness_report_builder"] == "tools/build_normandie_v04_readiness_report.py"
assert normandie_next["memory_plan"]["promotion_scenario_builder"] == "tools/build_normandie_v04_promotion_scenarios.py"
assert normandie_next["publication"]["public_export_allowed"] is False
nrelays = {item["id"]: item for item in normandie_emergency["candidates"]}
assert nrelays["F5ZHY"]["output_mhz"] == 145.6875
assert nrelays["F6ZES"]["output_mhz"] is None
assert nrelays["F6ZCE"]["department"] == 53
assert nrelays["F1ZBX"]["department"] == 35
assert all(item["frequency_promoted_to_public_pack"] is False for item in normandie_emergency["candidates"])

assert mortain_coverage["status"] == "research_coverage_priorities_not_public"
assert mortain_coverage["focus"]["departments_checked"] == [50, 35, 53, 61]
assert mortain_coverage["rules"]["sourdeval_must_not_be_guessed"] is True
assert mortain_coverage["rules"]["public_export_allowed"] is False
mstations = {item["id"]: item for item in mortain_coverage["stations"]}
assert mstations["F6ZES"]["output_mhz"] is None
assert mstations["F6ZES"]["mode"] is None
assert mstations["F6ZES"]["rx_pack_candidate"] is False
assert mstations["F5ZHY"]["output_mhz"] == 145.6875
assert mstations["F6ZCE"]["output_mhz"] == 145.7000
assert mstations["F1ZBX"]["output_mhz"] == 145.6750
assert mstations["F5ZIX"]["rx_pack_candidate"] is False
assert mstations["F5ZPO"]["rx_pack_candidate"] is False
assert mstations["F1ZKC"]["rx_pack_candidate"] is False
assert mstations["F5ZTQ"]["rx_pack_candidate"] is False

annecy_next = json.loads((ROOT / "research/annecy-alpes-leman-v0.3/pack-plan.json").read_text(encoding="utf-8"))
annecy_emergency = json.loads((ROOT / "research/annecy-alpes-leman-v0.3/emergency-relays.json").read_text(encoding="utf-8"))
assert annecy_next["schema_version"] == "1.1"
assert annecy_next["status"] == "research_next_version_not_public"
assert annecy_next["based_on_published_version"] == "0.2"
assert annecy_next["published_base_is_immutable"] is True
assert annecy_next["paired_rx"]["satellite_uplink_and_downlink_both_rx"] is True
assert annecy_next["paired_rx"]["analog_repeater_input_and_output_both_rx"] is True
assert annecy_next["publication"]["public_export_allowed"] is False
arelays = {item["id"]: item for item in annecy_emergency["candidates"]}
assert arelays["F1ZJV"]["output_mhz"] == 145.7875
assert arelays["F1ZYT"]["output_mhz"] == 145.7875
assert arelays["F1ZYT"]["rx_pack_candidate"] is False
assert arelays["F1ZHG"]["output_mhz"] == 145.2875
assert all(item["frequency_promoted_to_public_pack"] is False for item in annecy_emergency["candidates"])

plan = json.loads((ROOT / "research/annecy-alpes-leman-v0.2/prepublication-plan.json").read_text(encoding="utf-8"))
assert plan["status"] == "published_v0.2"
assert plan["candidate_memory_count"] == 65
assert plan["candidate_memory_count_without_aviation"] == 48
assert plan["public_export_allowed"] is True
review = json.loads((ROOT / "research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json").read_text(encoding="utf-8"))
assert review["expected_memory_count"] == 65
assert review["expected_memory_count_without_aviation"] == 48
assert len(review["rows"]) == 65

regions = json.loads((ROOT / "website/src/data/regions.json").read_text(encoding="utf-8"))
assert len(regions) == 2
assert {region["slug"] for region in regions} == {"annecy-haute-savoie", "normandie"}
assert next(region for region in regions if region["slug"] == "annecy-haute-savoie")["memoryCount"] == 65
assert next(region for region in regions if region["slug"] == "normandie")["memoryCount"] == 142

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
for expected in [
    'id: "annecy-alpes-leman"',
    'id: "normandie"',
    'version: "v0.2"',
    'version: "v0.4"',
    'memoryCount: 65',
    'memoryCount: 48',
    'memoryCount: 142',
]:
    assert expected in registry, f"Registre public incomplet: {expected}"
assert registry.count('downloadUrl: "') == 3
assert 'id: "bretagne"' not in registry
assert 'version: "v0.3"' not in registry
assert not (ROOT / "website/src/pages/regions/bretagne.astro").exists()
assert not (ROOT / "website/public/downloads/bretagne").exists()
assert not (ROOT / "website/src/pages/downloads/bretagne").exists()
assert not (ROOT / "website/src/pages/downloads/normandie/radiopack-france-normandie-v0.4.csv.ts").exists()
assert not (ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv.ts").exists()

chirp_pack = (ROOT / "website/src/lib/chirpPack.ts").read_text(encoding="utf-8")
assert '"off"' in chirp_pack
assert '"0.000000"' in chirp_pack

historical_generator = (ROOT / "generator/generate_chirp_csv.py").read_text(encoding="utf-8")
for expected in ['"--output-root"', "sortie isolée", "Normandie v0.3.1 est un artefact publié figé"]:
    assert expected in historical_generator, f"Isolation générateur absente: {expected}"
assert "radiopack-france-normandie-v0.3.1.csv" not in historical_generator

starter = (ROOT / "tools/create_regional_pack.py").read_text(encoding="utf-8")
for expected in [
    "research_scaffold_not_public",
    '"public_export_allowed": False',
    '"public_registry_allowed": False',
    '"public_routes_allowed": False',
    '"expected_memory_count": None',
    '"no_artificial_fill": True',
    '"published_versions_are_immutable": True',
    '"--output-root"',
    "Le dossier existe déjà",
    "NOT PUBLIC",
]:
    assert expected in starter, f"Starter régional incomplet: {expected}"

emergency_test = (ROOT / "tests/test_emergency_relay_research.py").read_text(encoding="utf-8")
for expected in [
    "Mortain-Bocage / Sud-Manche",
    "F5ZHY",
    "F6ZES",
    "F1ZJV",
    "F1ZYT",
    "ADRASEC-22",
    "ADRASEC-56",
    "F5ZZH",
    "no public mutation OK",
]:
    assert expected in emergency_test, f"Test secours/ADRASEC incomplet: {expected}"

paired_test = (ROOT / "tests/test_paired_rx_policy.py").read_text(encoding="utf-8")
for expected in [
    "native_duplex_or_split_pair_exports_both_rx_frequencies",
    "M01-S",
    "M01-C",
    "SAT-SO50",
    "MARINE-79",
    "TX remains off/zero",
]:
    assert expected in paired_test, f"Test paired RX incomplet: {expected}"

sprint29_test = (ROOT / "tests/test_mortain_bretagne_radio_research.py").read_text(encoding="utf-8")
for expected in [
    "Sourdeval unresolved safely",
    "Etel emitters primary-verified",
    "161.5750",
    "161.6250",
    "160.7750",
    "160.8250",
    "Penmarc'h",
    "Groix",
    "Belle-Ile",
    "Stiff",
    "Pointe du Raz",
    "F5ZZH",
    "F5ZIS",
    "F5ZIT",
    "F1ZBZ",
    "F5ZPE",
    "0 public mutations OK",
]:
    assert expected in sprint29_test, f"Test Sprint 29 incomplet: {expected}"

workflow_doc = (ROOT / "REGIONAL-PACK-WORKFLOW.md").read_text(encoding="utf-8")
for expected in ["chirpPack.ts", "packRegistry.ts", "carte de revue", "artefact immuable", "README.md"]:
    assert expected in workflow_doc, f"Workflow régional incomplet: {expected}"

workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
for expected in [
    "Test CSV generator in isolated output",
    "python tests/test_generator.py",
    "python tests/test_site_files.py",
    "python tests/test_pack_registry.py",
    "Test regional pack research starter",
    "python tests/test_regional_pack_starter.py",
    "Test paired RX policy",
    "python tests/test_paired_rx_policy.py",
    "Test Normandie v0.4 readiness and scenarios",
    "python tests/test_normandie_v04_readiness.py",
    "Test Bretagne research scaffold",
    "python tests/test_bretagne_research_scaffold.py",
    "Test emergency and ADRASEC research",
    "python tests/test_emergency_relay_research.py",
    "Test Mortain and Bretagne public radio research",
    "python tests/test_mortain_bretagne_radio_research.py",
    "python tests/test_web_generator.py",
    "python tests/test_built_public_pack_catalog.py",
    "npm run build",
    "radiopack-ci/complete",
]:
    assert expected in workflow, f"Étape CI absente: {expected}"

print("Tests RadioPack Sprint 39 guards: public packs frozen + paired RX/TX-off + Normandie v0.4 142-memory candidate with guarded 147 known ceiling + F5ZHA diagnostic/readiness tooling + Bretagne research guards OK")
