import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/bourgogne-franche-comte-v0.3"

aviation = json.loads((BASE / "aviation-airac08-2026-08-19.json").read_text(encoding="utf-8"))
plan = json.loads((BASE / "pack-plan.json").read_text(encoding="utf-8"))
backlog = json.loads((BASE / "backlog.json").read_text(encoding="utf-8"))
candidate = json.loads((BASE / "internal-candidate-v0.3.json").read_text(encoding="utf-8"))

assert aviation["status"] == "airac08_aviation_release_candidate_expansion"
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
assert len(promoted) == 7
assert {item["name"] for item in promoted} == {"VEZE-AFIS", "SY-APP1", "SY-APP2", "SY-GND", "SY-TWR", "SY-ATIS", "CHAL-INFO"}
expected = {122.205, 119.505, 123.405, 121.805, 122.3, 132.48, 118.605}
assert {float(item["frequency_mhz"]) for item in promoted} == expected
assert all(item["mode"] == "AM" for item in promoted)
assert {item["icao"] for item in promoted} == {"LFQM", "LFLN", "LFLH"}

leads = aviation["deferred_frequency_leads"]
assert len(leads) == 1
assert leads[0]["icao"] == "LFLM"
assert float(leads[0]["frequency_mhz"]) == 119.005

result = aviation["result"]
assert result["candidate_memory_count_before_this_pass"] == 47
assert result["new_aviation_memory_count"] == 7
assert result["candidate_memory_count_after_this_pass"] == 54
assert result["total_internal_delta_from_public_v0_2"] == 17

assert plan["status"] == "published_immutable_54"
assert plan["current_candidate_memory_count"] == 54
assert plan["current_new_memory_count"] == 17
assert plan["aviation_research"]["new_internal_memory_count"] == 7
assert plan["aviation_research"]["validated_new_aerodromes"] == ["LFQM", "LFLN", "LFLH"]
assert plan["aviation_research"]["deferred_frequency_leads"] == ["LFLM"]
assert plan["rules"]["airac09_revalidation_required_for_publication_on_or_after_2026_09_03"] is True
assert plan["rules"]["notam_and_sup_aip_review_required_at_publication"] is True
assert plan["public_export_allowed"] is True
assert plan["public_registry_allowed"] is True

assert backlog["candidate_memory_count"] == 54
assert backlog["candidate_memory_delta"] == 17
assert backlog["radioamateur_candidate_memory_delta"] == 10
assert backlog["aviation_candidate_memory_delta"] == 7

assert candidate["status"] == "published_immutable"
assert candidate["memory_count"] == 54
assert candidate["new_memory_count"] == 17
assert candidate["aviation_expansion"]["memory_count"] == 7
assert candidate["aviation_expansion"]["cycle"] == "AIRAC 08/26"
assert len(candidate["evidence_files"]) == 3
aviation_rows = [row for row in candidate["new_rx_memories"] if row["mode"] == "AM"]
assert len(aviation_rows) == 7
assert {float(row["frequency_mhz"]) for row in aviation_rows} == expected
assert all(row["duplex"] == "off" and row["offset"] == "0.000000" for row in aviation_rows)

all_new_freqs = [round(float(row["frequency_mhz"]), 6) for row in candidate["new_rx_memories"]]
assert len(all_new_freqs) == 17
assert len(set(all_new_freqs)) == 17
assert len({row["name"] for row in candidate["new_rx_memories"]}) == 17
assert candidate["public_export_allowed"] is True
assert candidate["public_registry_allowed"] is True

print("BFC v0.3 aviation publication guard: +7 AM RX (LFQM/LFLN/LFLH), published pack 54; LFLM deferred; AIRAC 09 future revalidation gate active, OK")
