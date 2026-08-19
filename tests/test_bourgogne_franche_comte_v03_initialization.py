#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/bourgogne-franche-comte-v0.3"

for name in ["README.md", "pack-plan.json", "backlog.json", "current-ref-audit.json"]:
    path = BASE / name
    assert path.is_file(), f"Missing BFC v0.3 research file: {path.relative_to(ROOT)}"
    assert path.stat().st_size > 20

plan = json.loads((BASE / "pack-plan.json").read_text(encoding="utf-8"))
backlog = json.loads((BASE / "backlog.json").read_text(encoding="utf-8"))
audit = json.loads((BASE / "current-ref-audit.json").read_text(encoding="utf-8"))

# Initialization baseline remains immutable even when the research candidate advances.
assert plan["target_version"] == "0.3"
assert plan["based_on_published_version"] == "0.2"
assert plan["published_base_memory_count"] == 37
assert plan["published_base_is_immutable"] is True
assert plan["current_candidate_memory_count"] >= 37
assert plan["current_new_memory_count"] == plan["current_candidate_memory_count"] - 37
assert plan["public_export_allowed"] is False
assert plan["public_registry_allowed"] is False
assert plan["research_lead_station_count"] == 10
assert plan["research_lead_max_memory_delta_before_deduplication"] == 20
assert plan["rules"]["rx_only"] is True
assert plan["rules"]["chirp_duplex"] == "off"
assert plan["rules"]["chirp_offset"] == "0.000000"
assert plan["rules"]["paired_rx_for_distinct_verified_pairs"] is True
assert plan["rules"]["directory_lead_requires_current_second_source_or_operator_confirmation_before_promotion"] is True

assert backlog["candidate_memory_count"] >= 37
assert backlog["candidate_memory_delta"] == backlog["candidate_memory_count"] - 37
assert backlog["lead_station_count"] == 10
assert backlog["potential_memory_delta_if_every_lead_clears_and_remains_unique"] == 20
assert all(item["memory_delta_if_cleared"] == 2 for item in backlog["items"])
assert len({item["call"] for item in backlog["items"]}) == 10
frequencies = [freq for item in backlog["items"] for freq in item["frequencies_mhz"]]
assert len(frequencies) == 20
assert len(set(frequencies)) == 20

# The Sprint-98/initial v0.3 directory audit itself remains a zero-delta historical record.
assert audit["departments_reviewed"] == [21, 25, 39, 58, 70, 71, 89, 90]
assert len(audit["published_v0_2_repeaters_rechecked"]) == 3
assert all(item["state"] == "Actif" for item in audit["published_v0_2_repeaters_rechecked"])
assert len(audit["new_analog_leads"]) == 10
assert all(item["state"] == "Actif" and item["mode"] == "FM" for item in audit["new_analog_leads"])
assert audit["decision"]["new_rf_promoted"] is False
assert audit["decision"]["candidate_memory_delta"] == 0

print("Bourgogne-Franche-Comté v0.3 initialization baseline preserved: immutable v0.2=37, 10 original analog leads, public export still blocked, OK")
