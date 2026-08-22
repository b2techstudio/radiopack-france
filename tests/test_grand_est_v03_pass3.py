#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V03 = ROOT / "research" / "grand-est-v0.3"

pass1 = json.loads((V03 / "radio-validation-pass1-2026-08-22.json").read_text(encoding="utf-8"))
pass2 = json.loads((V03 / "radio-validation-pass2-2026-08-22.json").read_text(encoding="utf-8"))
pass3 = json.loads((V03 / "radio-validation-pass3-2026-08-22.json").read_text(encoding="utf-8"))
backlog = json.loads((V03 / "backlog.json").read_text(encoding="utf-8"))
scope = json.loads((V03 / "release-scope.json").read_text(encoding="utf-8"))
registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")

assert pass3["status"] == "radio_scope_closed_non_exhaustive_no_public_mutation"
assert pass3["public_base"]["version"] == "0.2"
assert pass3["public_base"]["memory_count"] == 59
assert pass3["public_base"]["non_regional_memory_count"] == 43
assert pass3["public_base"]["immutable"] is True
assert {item["call"] for item in pass3["validated_in_pass3"]} == {"F1ZFL", "F5ZCC", "F1ZJS"}
assert {item["call"] for item in pass3["explicitly_deferred_at_scope_closure"]} == {"F5ZRP", "F5ZTY", "F5ZUK", "F1ZFN", "F1ZEF"}

rf = []
for item in pass1["v02_first_pass_safe_carry"]:
    rf.extend(item["rf_mhz"])
for item in pass1["high_confidence_new_links"]:
    rf.extend(item["rf_mhz"])
for item in pass2["validated_in_pass2"]:
    rf.extend(item["rf_mhz"])
for item in pass3["validated_in_pass3"]:
    rf.extend(item["rf_mhz"])
assert rf.count(432.5375) == 4
assert len(set(rf)) == 41

accounting = pass3["closed_radio_scope_accounting"]
assert accounting["safe_v02_unique_rf"] == 14
assert accounting["pass1_new_unique_rf"] == 8
assert accounting["pass2_unique_rf_added"] == 13
assert accounting["pass3_unique_rf_added"] == 6
assert accounting["regional_unique_rf_final_for_this_scope"] == 41
assert accounting["inherited_non_regional_memories_before_candidate_rebuild"] == 43
assert accounting["research_scope_total_if_non_regional_base_is_preserved"] == 84
assert accounting["final_radio_scope_frozen"] is True
assert accounting["scope_is_non_exhaustive"] is True
assert accounting["candidate_built"] is False
assert accounting["publication_ready"] is False

assert backlog["validated_radio_scope"]["regional_unique_rf_count"] == 41
assert {item.get("call") for item in backlog["excluded_from_analog_scope"] if item.get("call")} >= {"F1ZBU", "F5ZTC", "F5ZWR"}
assert any("F1ZCV" == item.get("call") for item in backlog["deferred_from_v03_radio_scope"])

# Pass3 facts remain frozen while later releases may advance the current pack.
assert scope["status"] == "published_immutable"
assert scope["current_phase"]["radio_pass3_complete"] is True
assert scope["current_phase"]["radio_scope_closed"] is True
assert scope["radio_scope"]["final_regional_memory_count"] == 41
assert scope["candidate"]["memory_count"] == 84
assert scope["candidate"]["regional_radio_memory_count"] == 41
assert scope["public"]["memory_count"] == 84
assert scope["current_phase"]["published"] is True
assert scope["current_phase"]["public_mutation_performed"] is True

for key in ["rx_only", "paired_rx_for_distinct_verified_pairs", "same_rf_frequency_deduplicated", "no_artificial_fill"]:
    assert pass3["rules"][key] is True
assert pass3["rules"]["chirp_duplex"] == "off"
assert pass3["rules"]["chirp_offset"] == "0.000000"
assert pass3["rules"]["maximum_memories"] == 200
assert pass3["rules"]["public_mutation"] is False

assert (
    '{ id: "grand-est", name: "Grand Est", memoryCount: 84, marine: false, aviation: 19, version: "v0.3" }' in registry
    or '{ id: "grand-est", name: "Grand Est", memoryCount: 97, marine: false, aviation: 19, version: "v0.4" }' in registry
)
assert (ROOT / "website/public/downloads/grand-est/radiopack-france-grand-est-v0.3.csv").is_file()

print("Sprint 102 Grand Est v0.3 pass3 historical radio scope preserved: 41 RF / v0.3 84 public evidence intact")
