import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

plan = json.loads((ROOT / "research/paired-rx-deduplicated-memory-plan.json").read_text(encoding="utf-8"))
source_plan = json.loads((ROOT / "research/paired-rx-next-version-plan.json").read_text(encoding="utf-8"))
linked = json.loads((ROOT / "research/bretagne-v0.1/rennes-broceliande-linked-system.json").read_text(encoding="utf-8"))
mortain_data = json.loads((ROOT / "research/normandie-v0.4/mortain-bocage-coverage.json").read_text(encoding="utf-8"))
assert plan["schema_version"] == "1.3"
assert source_plan["schema_version"] == "1.3"
assert plan["status"] == "research_deduplicated_memory_plan_not_public"
assert plan["source_plan"] == "research/paired-rx-next-version-plan.json"
assert plan["policy"] == "research/paired-rx-policy.json"
assert plan["export_contract"]["chirp_duplex"] == "off"
assert plan["export_contract"]["chirp_offset"] == "0.000000"
assert plan["export_contract"]["tx_disabled"] is True
assert plan["export_contract"]["same_rf_frequency_kept_once_per_region"] is True
assert plan["export_contract"]["memory_positions_assigned"] is False
assert plan["export_contract"]["public_pack_mutation_allowed"] is False

regions = {region["id"]: region for region in plan["regions"]}
assert set(regions) == {"normandie-v0.4", "annecy-alpes-leman-v0.3", "bretagne-v0.1"}
assert regions["normandie-v0.4"]["unique_frequency_count"] == 12
assert regions["annecy-alpes-leman-v0.3"]["unique_frequency_count"] == 10
assert regions["bretagne-v0.1"]["unique_frequency_count"] == 29

for region in regions.values():
    memories = region["memories"]
    assert len(memories) == region["unique_frequency_count"]
    frequencies = [item["frequency_mhz"] for item in memories]
    assert len(frequencies) == len(set(frequencies)), f"Duplicate RF frequency in {region['id']}"
    for item in memories:
        assert len(item["name_hint"]) <= 10
        assert item["roles"]
        assert item["selection_status"]

normandie = {item["name_hint"]: item for item in regions["normandie-v0.4"]["memories"]}
for name, frequency in {
    "ZHY-IN": 145.0875,
    "ZHY-OUT": 145.6875,
    "ZCE-IN": 145.1000,
    "ZCE-OUT": 145.7000,
    "ZBX-IN": 145.0750,
    "ZBX-OUT": 145.6750,
    "ZHA-A": 145.4675,
    "ZHA-B": 432.5750,
    "ZBL-A": 145.2500,
    "ZBL-B": 431.2500,
    "ZOV-A": 430.3750,
    "ZOV-B": 431.9750,
}.items():
    assert normandie[name]["frequency_mhz"] == frequency
assert "F5ZEB R71 to R3 bridge RX role" in normandie["ZBX-IN"]["roles"]
assert "F1ZBX R3 to F5ZEB R71 bridge RX role" in normandie["ZBX-OUT"]["roles"]
assert normandie["ZBX-IN"]["selection_status"] == "operator_supported_long_range_candidate_local_mortain_validation_required"
assert normandie["ZBX-OUT"]["selection_status"] == "operator_supported_long_range_candidate_local_mortain_validation_required"
excluded_normandie = "\n".join(regions["normandie-v0.4"]["excluded_or_unresolved"])
assert "F6ZES" in excluded_normandie
assert "F1ZBL" not in excluded_normandie
assert "F5ZHA" not in excluded_normandie

annecy = {item["name_hint"]: item for item in regions["annecy-alpes-leman-v0.3"]["memories"]}
assert annecy["SAT-UP850"]["frequency_mhz"] == 145.8500
assert set(annecy["SAT-UP850"]["roles"]) == {"SO-50 uplink RX", "AO-123 uplink RX"}
assert annecy["X432512"]["frequency_mhz"] == 432.5125
assert set(annecy["X432512"]["roles"]) == {"F1ZHG transponder side B", "F5ZGT transponder side B"}

bretagne = {item["name_hint"]: item for item in regions["bretagne-v0.1"]["memories"]}
expected_marine = {
    "M63-S": 156.1750,
    "M63-C": 160.7750,
    "M64-S": 156.2250,
    "M64-C": 160.8250,
    "M79-S": 156.9750,
    "M79-C": 161.5750,
    "M80-S": 157.0250,
    "M80-C": 161.6250,
}
for name, frequency in expected_marine.items():
    assert bretagne[name]["frequency_mhz"] == frequency

assert bretagne["X432650"]["frequency_mhz"] == 432.6500
assert set(bretagne["X432650"]["roles"]) == {
    "F5ZIS transponder side B",
    "F5ZIT transponder side B",
    "F5ZIU transponder side B",
    "F5ZIV transponder side B",
    "F5ZJR transponder side B",
}
for name, frequency in {
    "ZIU-A": 145.4625,
    "ZIV-A": 145.4875,
    "ZJR-A": 145.2875,
    "ZMU-OUT": 430.3250,
    "ZMU-IN": 439.7250,
    "ZBZ-U": 431.2000,
    "ZBZ-VA": 145.6250,
    "ZBZ-VB": 145.0250,
}.items():
    assert bretagne[name]["frequency_mhz"] == frequency

assert bretagne["X145262"]["frequency_mhz"] == 145.2625
assert set(bretagne["X145262"]["roles"]) == {
    "F1ZGS transponder side A",
    "F5ZDV transponder side A",
    "F5ZZL transponder side A",
}
assert set(bretagne["ZPE-IN"]["roles"]) == {"F5ZPE repeater input", "F1ZBZ repeater emission path"}
assert set(bretagne["ZPE-OUT"]["roles"]) == {"F5ZPE repeater output", "F1ZBZ repeater reception path"}
assert bretagne["ZBX-IN"]["roles"] == ["F1ZBX R3 input", "F5ZEB R71 to F1ZBX R3 bridge RX role"]
assert bretagne["ZBX-OUT"]["roles"] == ["F1ZBX R3 output", "F1ZBX R3 to F5ZEB R71 bridge RX role"]
assert bretagne["ZEB-A"]["roles"] == ["F5ZEB R71 user input RX"]
assert bretagne["ZEB-B"]["roles"] == ["F5ZEB R71 output RX"]
assert bretagne["ZEB-A"]["selection_status"] == "current_operator_operational_linked_system_temporary_site_review_required"
assert bretagne["ZEB-B"]["selection_status"] == "current_operator_operational_linked_system_temporary_site_review_required"

linked_system = linked["system"]
assert linked["schema_version"] == "1.0"
assert linked_system["current_operator_linkage_verified"] is True
assert linked_system["unique_rx_frequency_count"] == 4
assert linked_system["new_bretagne_rf_memories_required"] == 0
assert linked_system["r3_operator_usage_radius_km"] == 150
assert linked_system["r3_operator_usage_radius_is_reception_guarantee"] is False
assert linked_system["r3_to_r71_operator_link_distance_km"] == 46.51
assert {item["frequency_mhz"] for item in linked_system["rf_paths"]} == {145.0750, 145.6750, 431.0750, 438.6750}
mortain_relevance = linked_system["mortain_relevance"]
assert mortain_relevance["straight_line_distance_km"] == 119.3
assert mortain_relevance["inside_operator_usage_radius_geometrically"] is True
assert mortain_relevance["operator_usage_radius_margin_km"] == 30.7
assert mortain_relevance["actual_reception_from_mortain_verified"] is False
assert linked["export_contract"]["chirp_duplex"] == "off"
assert linked["export_contract"]["chirp_offset"] == "0.000000"
assert linked["export_contract"]["tx_disabled"] is True
assert linked["rules"]["linked_system_does_not_require_duplicate_rf_memories"] is True
assert linked["rules"]["operator_usage_radius_is_not_guaranteed_coverage"] is True
assert linked["rules"]["geometric_inclusion_in_operator_radius_is_not_reception_proof"] is True
assert linked["rules"]["public_export_allowed"] is False

mortain_stations = {item["id"]: item for item in mortain_data["stations"]}
r3 = mortain_stations["F1ZBX"]
assert r3["field_validation_priority"] == "immediate"
assert r3["straight_line_distance_to_mortain_km"] == 119.3
assert r3["inside_operator_usage_radius_geometrically"] is True
assert r3["operator_usage_radius_margin_km"] == 30.7
assert r3["actual_reception_from_mortain_verified"] is False
assert mortain_data["rules"]["geometric_inclusion_in_operator_radius_is_not_reception_proof"] is True

excluded_bretagne = "\n".join(regions["bretagne-v0.1"]["excluded_or_unresolved"])
assert "F5ZPV" in excluded_bretagne
assert "F5ZZH" in excluded_bretagne
assert "F1ZUG" in excluded_bretagne
assert "F1ZBZ" not in excluded_bretagne
assert all(name not in bretagne for name in ("ZPV-IN", "ZPV-OUT", "ZZH-IN", "ZZH-OUT"))

assert plan["rules"]["counts_are_research_counts_not_pack_targets"] is True
assert plan["rules"]["memory_names_are_hints_not_final_public_names"] is True
assert plan["rules"]["linked_system_roles_must_not_create_duplicate_rf_memories"] is True
assert plan["rules"]["stopped_or_unresolved_links_excluded_from_active_memory_list"] is True
assert plan["rules"]["no_public_export"] is True

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'id: "bretagne"' not in registry
assert 'version: "v0.4"' in registry
assert 'version: "v0.3"' not in registry

print("Tests RadioPack paired RX deduplicated memory research plan: Normandie 12, Annecy 10, Bretagne 29 unique RX frequencies, R3/R71 four-frequency linked system deduplicated and R3 at 119.3 km from Mortain inside the operator 150 km usage radius geometrically without claiming reception, TX-off contract and no public mutation OK")
