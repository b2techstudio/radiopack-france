#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research" / "grand-est-v0.2"
V03 = ROOT / "research" / "grand-est-v0.3"

record = json.loads((BASE / "publication-record.json").read_text(encoding="utf-8"))
pass1 = json.loads((V03 / "radio-validation-pass1-2026-08-22.json").read_text(encoding="utf-8"))
backlog = json.loads((V03 / "backlog.json").read_text(encoding="utf-8"))
scope = json.loads((V03 / "release-scope.json").read_text(encoding="utf-8"))
registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")

# Immutable public base.
assert record["status"] == "published_immutable"
assert record["version"] == "0.2"
assert record["memory_count"] == 59
assert record["public_csv_sha256"] == "a50416bd8a88af249bb691daa657ffd4b578daf1324bd0ca4dd632a2f1a0e5c1"
assert record["published_version_is_immutable"] is True

# Public registry must remain on v0.2 during research initialization.
assert '{ id: "grand-est", name: "Grand Est", memoryCount: 59, marine: false, aviation: 19, version: "v0.2" }' in registry
assert not (ROOT / "website/public/downloads/grand-est/radiopack-france-grand-est-v0.3.csv").exists()

# Pass 1 is research-only and preserves the RX contract.
assert pass1["status"] == "research_pass1_no_public_mutation"
assert pass1["rules"]["rx_only"] is True
assert pass1["rules"]["chirp_duplex"] == "off"
assert pass1["rules"]["chirp_offset"] == "0.000000"
assert pass1["rules"]["paired_rx_for_distinct_verified_pairs"] is True
assert pass1["rules"]["same_rf_frequency_deduplicated"] is True
assert pass1["rules"]["maximum_memories"] == 200
assert pass1["rules"]["public_mutation"] is False
assert pass1["rules"]["candidate_built"] is False

summary = pass1["pass1_summary"]
assert summary["v02_repeater_count"] == 8
assert summary["v02_first_pass_safe_carry_count"] == 7
assert summary["v02_mode_conflict_count"] == 1
assert summary["safe_carry_rx_memory_count"] == 14
assert summary["high_confidence_new_link_count"] == 4
assert summary["high_confidence_new_rx_memory_count"] == 8
assert summary["inherited_non_radio_memory_count_before_future_revalidation"] == 43
assert summary["research_floor_if_only_safe_carry_and_high_confidence_new_links_were_used"] == 65
assert summary["research_floor_is_not_a_release_candidate"] is True

safe_calls = {item["call"] for item in pass1["v02_first_pass_safe_carry"]}
assert safe_calls == {"F5ZAU", "F1ZDG", "F5ZDL", "F1ZAE", "F5ZEC", "F5ZCQ", "F1ZPJ"}
conflicts = {item["call"] for item in pass1["v02_conflicts"]}
assert conflicts == {"F1ZAX"}
assert pass1["v02_conflicts"][0]["status"] == "mode_resolution_required"

new_calls = {item["call"] for item in pass1["high_confidence_new_links"]}
assert new_calls == {"F5ZUD", "F1ZUV", "F5ZAW", "F5ZYS"}

# The first safe working set itself has no duplicate RF; wider backlog dedup happens in pass 2.
working_rf = []
for item in pass1["v02_first_pass_safe_carry"] + pass1["high_confidence_new_links"]:
    assert len(item["rf_mhz"]) == 2
    assert item["rf_mhz"][0] != item["rf_mhz"][1]
    working_rf.extend(item["rf_mhz"])
assert len(working_rf) == 22
assert len(set(working_rf)) == 22

blockers = {item["id"] for item in backlog["blocking_conflicts"]}
assert blockers == {"F1ZAX_MODE", "F5ZBD_STATUS"}
assert any("432.5375" in note for note in backlog["dedup_notes"])

# No candidate/publication can be claimed at initialization.
assert scope["status"] == "research_initialization"
assert scope["current_phase"]["radio_pass1_complete"] is True
assert scope["current_phase"]["radio_pass2_required"] is True
assert scope["current_phase"]["aviation_revalidation_started"] is False
assert scope["current_phase"]["deterministic_candidate_built"] is False
assert scope["current_phase"]["publication_ready"] is False
assert scope["current_phase"]["published"] is False
assert scope["current_phase"]["public_mutation_performed"] is False
assert scope["radio_scope"]["final_regional_memory_count"] is None
assert scope["aviation_scope"]["airac09_required_for_any_revision_on_or_after"] == "2026-09-03"

print("Sprint 102 Grand Est v0.3 initialization: immutable v0.2=59 preserved, pass1 radio research guarded, public=false OK")
