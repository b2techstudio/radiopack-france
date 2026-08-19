import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/bourgogne-franche-comte-v0.3"

plan = json.loads((BASE / "pack-plan.json").read_text(encoding="utf-8"))
backlog = json.loads((BASE / "backlog.json").read_text(encoding="utf-8"))
evidence = json.loads((BASE / "second-source-validation-2026-08-19.json").read_text(encoding="utf-8"))
candidate = json.loads((BASE / "internal-candidate-v0.3.json").read_text(encoding="utf-8"))
record = json.loads((ROOT / "research/bourgogne-franche-comte-v0.2/publication-record.json").read_text(encoding="utf-8"))

assert record["version"] == "0.2"
assert record["memory_count"] == 37
assert record["public_csv_sha256"] == "828af205aa07fe6685e3ad395ec2f0f56222fcfb5bb2f7b8f6a0bd4082714c0a"
assert record["published_version_is_immutable"] is True

assert plan["target_version"] == "0.3"
assert plan["based_on_published_version"] == "0.2"
assert plan["published_base_memory_count"] == 37
assert plan["published_base_is_immutable"] is True
assert plan["current_candidate_memory_count"] == 43
assert plan["current_new_memory_count"] == 6
assert plan["promoted_internal_station_count"] == 3
assert plan["promoted_internal_memory_count"] == 6
assert plan["remaining_unpromoted_lead_station_count"] == 7
assert plan["public_export_allowed"] is False
assert plan["public_registry_allowed"] is False
assert plan["rules"]["rx_only"] is True
assert plan["rules"]["chirp_duplex"] == "off"
assert plan["rules"]["chirp_offset"] == "0.000000"
assert plan["rules"]["conflicting_secondary_evidence_blocks_promotion"] is True

validated = evidence["validated_for_internal_candidate"]
assert evidence["result"]["validated_station_count"] == 3
assert evidence["result"]["validated_memory_delta"] == 6
assert evidence["result"]["internal_candidate_memory_count"] == 43
assert len(validated) == 3
assert {item["call"] for item in validated} == {"F5ZIQ", "F5ZVA", "F5ZFQ"}
assert {item["decision"] for item in validated} == {"promote_to_internal_candidate"}
assert len(evidence["not_yet_validated"]) == 7

assert candidate["status"] == "internal_candidate_not_for_publication"
assert candidate["published_base_version"] == "0.2"
assert candidate["published_base_memory_count"] == 37
assert candidate["published_base_sha256"] == record["public_csv_sha256"]
assert candidate["memory_count"] == 43
assert candidate["new_memory_count"] == 6
assert candidate["public_export_allowed"] is False
assert candidate["public_registry_allowed"] is False
assert len(candidate["promoted_stations"]) == 3
assert len(candidate["new_rx_memories"]) == 6

expected_freqs = {145.45, 432.55, 145.25, 431.25, 145.2625, 430.125}
actual_freqs = {float(row["frequency_mhz"]) for row in candidate["new_rx_memories"]}
assert actual_freqs == expected_freqs
assert len(actual_freqs) == 6
assert all(row["mode"] == "FM" for row in candidate["new_rx_memories"])
assert all(row["duplex"] == "off" for row in candidate["new_rx_memories"])
assert all(row["offset"] == "0.000000" for row in candidate["new_rx_memories"])

states = {item["call"]: item["state"] for item in backlog["items"]}
for call in ["F5ZIQ", "F5ZVA", "F5ZFQ"]:
    assert states[call] == "cleared_for_internal_candidate_second_source_pass1"
for call in ["F1ZCA", "F5ZNS", "F5ZXZ", "F5ZFE", "F5ZKM", "F5ZMS", "F5ZTJ"]:
    assert "cleared_for_internal_candidate" not in states[call]
assert backlog["candidate_memory_count"] == 43
assert backlog["candidate_memory_delta"] == 6
assert backlog["promoted_internal_station_count"] == 3
assert backlog["remaining_unpromoted_station_count"] == 7

print("BFC v0.3 second-source validation: 3 stations / 6 RX promoted internally, candidate 43, 7 leads still blocked, public v0.2 immutable OK")
