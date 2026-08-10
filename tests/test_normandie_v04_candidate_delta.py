import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DELTA_PATH = ROOT / "research/normandie-v0.4/candidate-memory-delta.json"
FIELD_PATH = ROOT / "research/normandie-v0.4/r3-mortain-field-validation.json"
PACK_PLAN_PATH = ROOT / "research/normandie-v0.4/pack-plan.json"
REFRESH_PATH = ROOT / "research/normandie-v0.4/paired-rx-refresh.json"
BASE_CSV = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv"

for path in (DELTA_PATH, FIELD_PATH, PACK_PLAN_PATH, REFRESH_PATH, BASE_CSV):
    assert path.is_file(), f"Missing expected file: {path}"

delta = json.loads(DELTA_PATH.read_text(encoding="utf-8"))
field = json.loads(FIELD_PATH.read_text(encoding="utf-8"))
pack_plan = json.loads(PACK_PLAN_PATH.read_text(encoding="utf-8"))
refresh = json.loads(REFRESH_PATH.read_text(encoding="utf-8"))

assert delta["schema_version"] == "1.0"
assert delta["status"] == "research_candidate_delta_defined_not_public"
assert delta["base"]["version"] == "0.3.1"
assert delta["base"]["memory_count"] == 139
assert delta["base"]["immutable"] is True
assert delta["paired_rx_research_frequency_count"] == 12
assert delta["sources"]["internal_candidate_map"] == "research/normandie-v0.4/internal-candidate-map.json"

with BASE_CSV.open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))

assert len(rows) == 139
base_by_frequency = {round(float(row["Frequency"]), 6): row for row in rows}

expected_existing = {
    145.687500: "50-F5ZHY",
    430.375000: "50-F1ZOV",
    145.250000: "50-F1ZBL",
    145.700000: "53-F6ZCE",
}
assert {round(item["frequency_mhz"], 6): item["published_name"] for item in delta["already_present_in_published_base"]} == expected_existing
for frequency, expected_name in expected_existing.items():
    row = base_by_frequency[frequency]
    assert row["Name"] == expected_name
    assert row["Duplex"] == "off"
    assert row["Offset"] == "0.000000"

new_candidates = delta["new_frequency_candidates"]
assert len(new_candidates) == 8
new_by_name = {item["name_hint"]: item for item in new_candidates}
assert set(new_by_name) == {
    "ZHY-IN", "ZCE-IN", "ZBL-B", "ZBX-IN", "ZBX-OUT", "ZHA-A", "ZHA-B", "ZOV-B"
}
for item in new_candidates:
    assert round(item["frequency_mhz"], 6) not in base_by_frequency
    assert item["publication_allowed"] is False
    assert len(item["name_hint"]) <= 10

assert new_by_name["ZHY-IN"]["frequency_mhz"] == 145.0875
assert new_by_name["ZCE-IN"]["frequency_mhz"] == 145.1000
assert new_by_name["ZBL-B"]["frequency_mhz"] == 431.2500
assert new_by_name["ZOV-B"]["frequency_mhz"] == 431.9750
assert new_by_name["ZBX-IN"]["frequency_mhz"] == 145.0750
assert new_by_name["ZBX-OUT"]["frequency_mhz"] == 145.6750
assert new_by_name["ZHA-A"]["frequency_mhz"] == 145.4675
assert new_by_name["ZHA-B"]["frequency_mhz"] == 432.5750

states = [item["state"] for item in new_candidates]
assert states.count("ready_research_candidate") == 3
assert states.count("local_mortain_validation_required") == 2
assert states.count("source_conflict_and_coverage_validation_required") == 2
assert states.count("operator_maintenance_revalidation_required") == 1

summary = delta["summary"]
assert summary["maximum_new_paired_rx_frequencies_under_current_research"] == 8
assert summary["ready_research_candidates"] == 3
assert summary["local_mortain_validation_required"] == 2
assert summary["source_conflict_and_coverage_validation_required"] == 2
assert summary["operator_maintenance_revalidation_required"] == 1
assert summary["internal_candidate_memory_count"] == 142
assert summary["internal_candidate_new_memory_count"] == 3
assert summary["internal_candidate_positions_assigned_provisionally"] is True
assert summary["final_v0_4_memory_count"] is None
assert summary["memory_positions_assigned"] is False

rules = delta["rules"]
assert rules["frequency_present_in_base_must_not_be_added_again"] is True
assert rules["temporary_maintenance_blocks_new_side_promotion_until_revalidated"] is True
assert rules["internal_candidate_positions_are_not_final_public_positions"] is True
assert rules["all_future_exported_memories_tx_disabled"] is True
assert rules["chirp_duplex"] == "off"
assert rules["chirp_offset"] == "0.000000"
assert rules["public_export_allowed"] is False

assert field["schema_version"] == "1.0"
assert field["status"] == "field_validation_protocol_not_yet_observed"
assert field["station"]["output_rx_mhz"] == 145.6750
assert field["station"]["input_rx_mhz"] == 145.0750
assert field["station"]["mortain_straight_line_distance_km"] == 119.3
assert field["station"]["operator_usage_radius_km"] == 150
assert field["station"]["geometry_is_reception_proof"] is False
assert field["rx_only_contract"]["transmission_forbidden"] is True
assert field["rx_only_contract"]["chirp_duplex"] == "off"
assert field["rx_only_contract"]["chirp_offset"] == "0.000000"
assert field["rx_only_contract"]["input_frequency_does_not_need_to_be_heard_from_mortain_to_keep_paired_rx_policy"] is True
assert field["acceptance_gate"]["actual_reception_from_mortain_verified"] is False
assert field["acceptance_gate"]["repeatable_reception_required"] is True
assert field["acceptance_gate"]["single_weak_carrier_is_sufficient"] is False
assert field["acceptance_gate"]["promotion_to_public_pack_allowed"] is False
assert field["observations"] == []

memory_plan = pack_plan["memory_plan"]
assert pack_plan["schema_version"] == "1.2"
assert pack_plan["project_resume_state"] == "research/project-resume-state.json"
assert pack_plan["project_status_document"] == "PROJECT_STATUS.md"
assert memory_plan["status"] == "internal_candidate_defined_not_public"
assert memory_plan["candidate_delta_file"] == "research/normandie-v0.4/candidate-memory-delta.json"
assert memory_plan["internal_candidate_map_file"] == "research/normandie-v0.4/internal-candidate-map.json"
assert memory_plan["internal_candidate_builder"] == "tools/build_normandie_v04_internal_candidate.py"
assert memory_plan["promotion_gates_file"] == "research/normandie-v0.4/promotion-gates.json"
assert memory_plan["blocked_station_revalidation_file"] == "research/normandie-v0.4/blocked-station-revalidation.json"
assert memory_plan["promotion_gate_report_builder"] == "tools/build_normandie_v04_gate_report.py"
assert memory_plan["r3_field_validation_file"] == "research/normandie-v0.4/r3-mortain-field-validation.json"
assert memory_plan["r3_validation_pack_file"] == "research/normandie-v0.4/r3-validation-pack.json"
assert memory_plan["r3_observation_recorder"] == "tools/record_normandie_v04_r3_observation.py"
assert memory_plan["local_check_runner"] == "tools/run_normandie_v04_checks.py"
assert memory_plan["internal_candidate_memory_count"] == 142
assert memory_plan["internal_candidate_new_memory_count"] == 3
assert memory_plan["internal_candidate_positions_assigned_provisionally"] is True
assert memory_plan["paired_rx_research_frequency_count"] == 12
assert memory_plan["paired_rx_frequencies_already_in_v0_3_1"] == 4
assert memory_plan["maximum_new_paired_rx_frequencies_under_current_research"] == 8
assert memory_plan["ready_research_candidates"] == 3
assert memory_plan["expected_memory_count"] is None
assert memory_plan["memory_positions_assigned"] is False
assert memory_plan["new_blocks"][0]["locations"] == [175, 176, 177]
assert pack_plan["publication"]["public_export_allowed"] is False

assert refresh["schema_version"] == "1.3"
resolved = {item["id"]: item for item in refresh["resolved_pairs"]}
assert set(resolved) == {"F1ZBL", "F1ZOV", "F5ZHA"}
f1zov = resolved["F1ZOV"]
assert f1zov["side_a_rx_mhz"] == 430.3750
assert f1zov["side_b_rx_mhz"] == 431.9750
assert f1zov["source_reconciliation"]["current_local_operator_status"] == "maintenance"
assert f1zov["source_reconciliation"]["publication_blocked_by_operational_status"] is True
assert refresh["rules"]["maintenance_blocks_new_side_promotion_until_revalidated"] is True

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'version: "v0.4"' not in registry

print("Tests Normandie v0.4 candidate delta: frozen v0.3.1 + 8 possible paired sides classified, 3 promoted only into a 142-memory internal candidate with provisional locations 175-177; field/recovery tooling linked; no public mutation OK")
