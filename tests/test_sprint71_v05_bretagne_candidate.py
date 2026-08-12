import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "research/sprint-71-v05-bretagne-candidate.json"
STATE = ROOT / "research/project-resume-state.json"

e = json.loads(EVIDENCE.read_text(encoding="utf-8"))
assert e["sprint"] == 71
assert e["state_version"] == "0.21.60"
assert e["normandie_v0_5"]["published_base_memory_count"] == 142
assert e["normandie_v0_5"]["candidate_memory_count"] == 142
assert e["normandie_v0_5"]["eligible_addition_count"] == 0
assert e["normandie_v0_5"]["gate_cleared_count"] == 0

r3 = e["normandie_v0_5"]["r3"]
assert r3["pair_mhz"] == [145.075, 145.675]
assert r3["current_operator_pair_revalidated"] is True
assert r3["two_independent_mortain_rx_sessions_present_in_repository"] is False
assert r3["promotion"] is False

zha = e["normandie_v0_5"]["f5zha"]
assert zha["pair_mhz"] == [145.4675, 432.575]
assert zha["current_ref_active"] is True
assert zha["local_or_equivalent_authoritative_reconciliation_complete"] is False
assert zha["mortain_field_relevance_verified"] is False
assert zha["promotion"] is False

zov = e["normandie_v0_5"]["f1zov"]
assert zov["local_operator_status"] == "En Maintenance"
assert zov["promotion"] is False

zes = e["normandie_v0_5"]["f6zes"]
assert zes["current_ref_frequency_present"] is False
assert zes["current_ref_mode_present"] is False
assert zes["must_not_guess"] is True
assert zes["promotion"] is False

b = e["bretagne_v0_1"]
assert b["internal_candidate_memory_count"] == 135
assert b["national_blocks"] == {
    "pmr446": 16,
    "marine_vhf": 90,
    "amateur_listening": 6,
    "amateur_calls": 2,
}
assert b["regional_unique_memories_after_national_deduplication"] == 21
assert b["regional_source_unique_count"] == 29
assert b["marine_policy"]["channel64_pair_mhz"] == [156.225, 160.825]
assert b["marine_policy"]["channel79_pair_mhz"] == [156.975, 161.575]
assert b["marine_policy"]["channel64_two_generic_rx_memories_in_candidate"] is True
assert b["marine_policy"]["channel79_two_generic_rx_memories_in_candidate"] is True
assert b["marine_policy"]["channel64_local_site_claimed"] is False
assert b["marine_policy"]["channel79_local_site_claimed"] is False
assert b["aviation"]["memory_count"] == 0
assert b["aviation"]["status"] == "pending_current_sia_extraction"

assert e["rules"]["internal_candidate_is_not_publication"] is True
assert e["rules"]["tx_disabled"] is True

state = json.loads(STATE.read_text(encoding="utf-8"))
assert state["current_sprint"] >= 71
assert state["state_version"] >= "0.21.60"
assert state["active_work"]["pack"] == "Bretagne"
assert state["active_work"]["target_version"] == "0.1"
assert state["active_work"]["internal_candidate_memory_count"] == 135
assert state["active_work"]["public_export_allowed"] is False

print("Sprint 71: Normandie v0.5 revalidated with 0 promotion; Bretagne v0.1 internal candidate advanced to 135 RX-only memories, public untouched OK")
