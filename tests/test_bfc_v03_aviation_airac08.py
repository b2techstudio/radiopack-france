import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/bourgogne-franche-comte-v0.3"

aviation = json.loads((BASE / "aviation-airac08-2026-08-19.json").read_text(encoding="utf-8"))
plan = json.loads((BASE / "pack-plan.json").read_text(encoding="utf-8"))
backlog = json.loads((BASE / "backlog.json").read_text(encoding="utf-8"))
candidate = json.loads((BASE / "internal-candidate-v0.3.json").read_text(encoding="utf-8"))

assert aviation["status"] == "airac08_aviation_internal_candidate_expansion_not_public"
assert aviation["target_version"] == "0.3"
assert aviation["airac_context"]["cycle"] == "AIRAC 08/26"
assert aviation["airac_context"]["effective_from"] == "2026-08-06"
assert aviation["airac_context"]["effective_until_inclusive"] == "2026-09-02"
assert aviation["airac_context"]["next_cycle"] == "AIRAC 09/26"
assert aviation["airac_context"]["next_cycle_effective_from"] == "2026-09-03"
assert aviation["airac_context"]["current_cycle_product_seen_on_sia"] is True
assert aviation["airac_context"]["direct_airac08_xml_field_extraction_claimed"] is False

assert aviation["published_v0_2_aviation_baseline"]["memory_count"] == 7
assert len(aviation["published_v0_2_aviation_baseline"]["channels"]) == 7

promoted = aviation["validated_new_aviation_memories"]
assert len(promoted) == 6
assert {item["name"] for item in promoted} == {
    "VEZE-AFIS", "SY-APP1", "SY-APP2", "SY-GND", "SY-TWR", "SY-ATIS"
}
expected = {122.205, 119.505, 123.405, 121.805, 122.3, 132.48}
assert {float(item["frequency_mhz"]) for item in promoted} == expected
assert all(item["mode"] == "AM" for item in promoted)
assert {item["icao"] for item in promoted} == {"LFQM", "LFLN"}

leads = aviation["deferred_frequency_leads"]
assert len(leads) == 2
assert {item["icao"] for item in leads} == {"LFLH", "LFLM"}
assert {float(item["frequency_mhz"]) for item in leads} == {118.605, 119.005}

result = aviation["result"]
assert result["candidate_memory_count_before_this_pass"] == 47
assert result["new_aviation_memory_count"] == 6
assert result["candidate_memory_count_after_this_pass"] == 53
assert result["total_internal_delta_from_public_v0_2"] == 16
assert result["public_export_allowed"] is False
assert result["public_registry_allowed"] is False

assert plan["current_candidate_memory_count"] == 53
assert plan["current_new_memory_count"] == 16
assert plan["aviation_research"]["new_internal_memory_count"] == 6
assert plan["aviation_research"]["validated_new_aerodromes"] == ["LFQM", "LFLN"]
assert plan["aviation_research"]["deferred_frequency_leads"] == ["LFLH", "LFLM"]
assert plan["rules"]["airac09_revalidation_required_for_publication_on_or_after_2026_09_03"] is True
assert plan["rules"]["notam_and_sup_aip_review_required_at_publication"] is True

assert backlog["candidate_memory_count"] == 53
assert backlog["candidate_memory_delta"] == 16
assert backlog["radioamateur_candidate_memory_delta"] == 10
assert backlog["aviation_candidate_memory_delta"] == 6

assert candidate["memory_count"] == 53
assert candidate["new_memory_count"] == 16
assert candidate["aviation_expansion"]["memory_count"] == 6
assert candidate["aviation_expansion"]["cycle"] == "AIRAC 08/26"
assert len(candidate["evidence_files"]) == 3
aviation_rows = [row for row in candidate["new_rx_memories"] if row["mode"] == "AM"]
assert len(aviation_rows) == 6
assert {float(row["frequency_mhz"]) for row in aviation_rows} == expected
assert all(row["duplex"] == "off" and row["offset"] == "0.000000" for row in aviation_rows)

all_new_freqs = [round(float(row["frequency_mhz"]), 6) for row in candidate["new_rx_memories"]]
assert len(all_new_freqs) == 16
assert len(set(all_new_freqs)) == 16
assert len({row["name"] for row in candidate["new_rx_memories"]}) == 16
assert candidate["public_export_allowed"] is False
assert candidate["public_registry_allowed"] is False

print("BFC v0.3 aviation AIRAC 08: +6 AM RX (LFQM/LFLN), candidate 53; LFLH/LFLM deferred; AIRAC 09 publication revalidation gate active, OK")
