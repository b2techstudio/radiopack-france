import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/bourgogne-franche-comte-v0.3"

plan = json.loads((BASE / "pack-plan.json").read_text(encoding="utf-8"))
backlog = json.loads((BASE / "backlog.json").read_text(encoding="utf-8"))
pass1 = json.loads((BASE / "second-source-validation-2026-08-19.json").read_text(encoding="utf-8"))
pass2 = json.loads((BASE / "second-source-validation-pass2-2026-08-19.json").read_text(encoding="utf-8"))
candidate = json.loads((BASE / "internal-candidate-v0.3.json").read_text(encoding="utf-8"))
record = json.loads((ROOT / "research/bourgogne-franche-comte-v0.2/publication-record.json").read_text(encoding="utf-8"))

assert record["version"] == "0.2"
assert record["memory_count"] == 37
assert record["public_csv_sha256"] == "828af205aa07fe6685e3ad395ec2f0f56222fcfb5bb2f7b8f6a0bd4082714c0a"
assert record["published_version_is_immutable"] is True

assert pass1["result"]["validated_station_count"] == 3
assert pass1["result"]["validated_memory_delta"] == 6
assert pass1["result"]["internal_candidate_memory_count"] == 43
assert {item["call"] for item in pass1["validated_for_internal_candidate"]} == {"F5ZIQ", "F5ZVA", "F5ZFQ"}

assert pass2["result"]["validated_station_count_this_pass"] == 2
assert pass2["result"]["validated_memory_delta_this_pass"] == 4
assert pass2["result"]["cumulative_validated_station_count"] == 5
assert pass2["result"]["cumulative_validated_memory_delta"] == 10
assert pass2["result"]["internal_candidate_memory_count"] == 47
assert pass2["result"]["remaining_unpromoted_station_count"] == 5
assert {item["call"] for item in pass2["validated_this_pass"]} == {"F1ZCA", "F5ZXZ"}
assert {item["id"].split("_")[0] for item in pass2["still_blocked_after_pass2"]} == {"F5ZNS", "F5ZFE", "F5ZKM", "F5ZMS", "F5ZTJ"}

assert plan["status"] == "published_immutable_54"
assert plan["current_candidate_memory_count"] == 54
assert plan["current_new_memory_count"] == 17
assert plan["promoted_internal_station_count"] == 5
assert plan["promoted_internal_memory_count"] == 10
assert plan["remaining_unpromoted_lead_station_count"] == 5
assert plan["radioamateur_research"]["promoted_internal_station_count"] == 5
assert plan["radioamateur_research"]["promoted_internal_memory_count"] == 10
assert plan["radioamateur_research"]["scope_closed_with_deferred_leads"] is True
assert plan["public_export_allowed"] is True
assert plan["public_registry_allowed"] is True
assert plan["published_version_is_immutable"] is True

assert candidate["status"] == "published_immutable"
assert candidate["published_base_memory_count"] == 37
assert candidate["published_base_sha256"] == record["public_csv_sha256"]
assert candidate["memory_count"] == 54
assert candidate["new_memory_count"] == 17
assert candidate["radioamateur_expansion"]["station_count"] == 5
assert candidate["radioamateur_expansion"]["memory_count"] == 10
assert candidate["public_export_allowed"] is True
assert candidate["public_registry_allowed"] is True
assert len(candidate["promoted_stations"]) == 5

radio_rows = [row for row in candidate["new_rx_memories"] if row["mode"] == "FM"]
expected_radio_freqs = {145.45, 432.55, 145.25, 431.25, 145.2625, 430.125, 430.3, 431.9, 145.2125, 431.1}
assert {float(row["frequency_mhz"]) for row in radio_rows} == expected_radio_freqs
assert len(radio_rows) == 10
assert all(row["duplex"] == "off" and row["offset"] == "0.000000" for row in radio_rows)

states = {item["call"]: item["state"] for item in backlog["items"]}
for call in ["F5ZIQ", "F5ZVA", "F5ZFQ"]:
    assert states[call] == "cleared_for_internal_candidate_second_source_pass1"
for call in ["F1ZCA", "F5ZXZ"]:
    assert states[call] == "cleared_for_internal_candidate_second_source_pass2"
for call in ["F5ZNS", "F5ZFE", "F5ZKM", "F5ZMS", "F5ZTJ"]:
    assert "cleared_for_internal_candidate" not in states[call]
    assert states[call].startswith("deferred_v0_3_")
assert backlog["radioamateur_candidate_memory_delta"] == 10
assert backlog["promoted_internal_station_count"] == 5
assert backlog["remaining_unpromoted_station_count"] == 5
assert backlog["release_decision"]["scope_closed"] is True
assert backlog["release_decision"]["deferred_leads_block_release"] is False

print("BFC v0.3 radio publication guard: 5 stations / 10 RX, 5 leads deferred, published pack 54 RX immutable, v0.2 immutable OK")
