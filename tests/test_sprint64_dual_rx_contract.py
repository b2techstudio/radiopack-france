import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

contract = json.loads((ROOT / "research/sprint-64-dual-rx-contract.json").read_text(encoding="utf-8"))
policy = json.loads((ROOT / "research/paired-rx-policy.json").read_text(encoding="utf-8"))
next_plan = json.loads((ROOT / "research/paired-rx-next-version-plan.json").read_text(encoding="utf-8"))
r3_pack = json.loads((ROOT / "research/normandie-v0.4/r3-validation-pack.json").read_text(encoding="utf-8"))
resume = json.loads((ROOT / "research/project-resume-state.json").read_text(encoding="utf-8"))
normandie_work = resume.get("normandie_v0_5_work", resume["active_work"])

assert contract["status"] == "dual_rx_contract_snapshot_not_public"
assert contract["public_export_allowed"] is False
assert contract["candidate_mutation_allowed"] is False
assert contract["rules"]["distinct_verified_duplex_pair_uses_two_rx_memories"] is True
assert contract["rules"]["two_field_sessions_do_not_mean_two_additional_memories"] is True
assert contract["rules"]["tx_disabled"] is True
assert contract["rules"]["chirp_duplex"] == "off"
assert contract["rules"]["chirp_offset"] == "0.000000"

items = {item["id"]: item for item in contract["contracts"]}
assert set(items) == {"F1ZBX_R3", "CROSS_ETEL_CHANNEL_64", "CROSS_CORSEN_CHANNEL_79"}

r3 = items["F1ZBX_R3"]
assert r3["rx_frequencies_mhz"] == [145.075, 145.675]
assert r3["required_distinct_rx_memory_count_if_promoted"] == 2
assert r3["minimum_independent_field_sessions"] == 2
assert r3["field_sessions_are_evidence_not_memories"] is True
assert r3["field_gate_currently_cleared"] is False
assert r3["promotion_currently_allowed"] is False
assert r3["current_candidate_memory_delta"] == 0
assert r3["memory_delta_if_gate_clears"] == 2

etel64 = items["CROSS_ETEL_CHANNEL_64"]
assert etel64["rx_frequencies_mhz"] == [156.225, 160.825]
assert etel64["required_distinct_rx_memory_count_if_published"] == 2
assert etel64["directions"] == ["ship_to_coast", "coast_to_ship"]
assert etel64["primary_source_conflict_open"] is True
assert etel64["promotion_currently_allowed"] is False
assert etel64["new_rf_memory_delta"] == 0

corsen79 = items["CROSS_CORSEN_CHANNEL_79"]
assert corsen79["rx_frequencies_mhz"] == [156.975, 161.575]
assert corsen79["required_distinct_rx_memory_count_if_published"] == 2
assert corsen79["directions"] == ["ship_to_coast", "coast_to_ship"]
assert corsen79["current_primary_transmitter_context_confirmed"] is False
assert corsen79["promotion_currently_allowed"] is False
assert corsen79["new_rf_memory_delta"] == 0

assert policy["schema_version"] == "1.1"
assert policy["core_rule"]["required_rx_memory_count_when_verified_pair_frequencies_differ"] == 2
assert policy["evidence_vs_memory_contract"]["field_sessions_are_evidence_not_memories"] is True
assert policy["evidence_vs_memory_contract"]["field_session_count_does_not_define_rx_memory_count"] is True
assert policy["locked_examples"]["F1ZBX_R3"]["minimum_independent_field_sessions_for_mortain_gate"] == 2
assert policy["locked_examples"]["F1ZBX_R3"]["required_pair_rx_memory_count_if_promoted"] == 2
assert policy["locked_examples"]["CROSS_ETEL_CHANNEL_64"]["required_pair_rx_memory_count_if_published"] == 2
assert policy["locked_examples"]["CROSS_CORSEN_CHANNEL_79"]["required_pair_rx_memory_count_if_published"] == 2

pair_members = [item for item in r3_pack["memories"] if item["pair_member"]]
assert len(pair_members) == 2
assert {item["name"] for item in pair_members} == {"R3-OUT", "R3-IN"}
assert {item["frequency_mhz"] for item in pair_members} == {145.075, 145.675}
control = next(item for item in r3_pack["memories"] if item["name"] == "CTRL-ZHY")
assert control["pair_member"] is False
assert r3_pack["validation"]["minimum_independent_sessions"] == 2
assert r3_pack["validation"]["field_sessions_are_evidence_not_memories"] is True
assert r3_pack["validation"]["required_r3_pair_rx_memory_count"] == 2
assert r3_pack["validation"]["control_memory_is_part_of_r3_pair"] is False
assert r3_pack["rules"]["if_r3_gate_clears_both_distinct_pair_frequencies_remain_separate_rx_memories"] is True

regions = {region["id"]: region for region in next_plan["regions"]}
normandie_links = {item["id"]: item for item in regions["normandie-v0.4"]["paired_links"]}
bretagne_links = {item["id"]: item for item in regions["bretagne-v0.1"]["paired_links"]}
assert normandie_links["F1ZBX"]["uplink_rx_mhz"] == 145.075
assert normandie_links["F1ZBX"]["downlink_rx_mhz"] == 145.675
assert bretagne_links["MARINE-64"]["ship_to_coast_rx_mhz"] == 156.225
assert bretagne_links["MARINE-64"]["coast_to_ship_rx_mhz"] == 160.825
assert bretagne_links["MARINE-79"]["ship_to_coast_rx_mhz"] == 156.975
assert bretagne_links["MARINE-79"]["coast_to_ship_rx_mhz"] == 161.575

# Public state must remain unchanged while these gates are still closed.
public_normandie = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv"
rows = list(csv.DictReader(io.StringIO(public_normandie.read_text(encoding="utf-8"))))
assert len(rows) == 139
registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'version: "v0.4"' in registry
assert 'id: "bretagne"' not in registry
assert resume["public_packs"]["normandie"]["memory_count"] == 142
assert normandie_work["internal_candidate_memory_count"] == 142
assert normandie_work["current_guarded_promotion_plan_eligible_addition_count"] == 0

print(
    "Tests Sprint 64 dual RX contract: R3 keeps exactly two pair memories independently of its two field sessions, "
    "Etel Ch64 and Corsen Ch79 each keep both maritime RX directions, all gates remain closed and public packs unchanged OK"
)
