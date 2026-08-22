#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research" / "grand-est-v0.2"
V03 = ROOT / "research" / "grand-est-v0.3"

record = json.loads((BASE / "publication-record.json").read_text(encoding="utf-8"))
pass1 = json.loads((V03 / "radio-validation-pass1-2026-08-22.json").read_text(encoding="utf-8"))
scope = json.loads((V03 / "release-scope.json").read_text(encoding="utf-8"))
registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")

# Immutable historical public base.
assert record["status"] == "published_immutable"
assert record["version"] == "0.2"
assert record["memory_count"] == 59
assert record["public_csv_sha256"] == "a50416bd8a88af249bb691daa657ffd4b578daf1324bd0ca4dd632a2f1a0e5c1"
assert record["published_version_is_immutable"] is True

# Pass 1 remains immutable research evidence after publication.
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
assert {item["call"] for item in pass1["v02_conflicts"]} == {"F1ZAX"}
assert {item["call"] for item in pass1["high_confidence_new_links"]} == {"F5ZUD", "F1ZUV", "F5ZAW", "F5ZYS"}

working_rf = []
for item in pass1["v02_first_pass_safe_carry"] + pass1["high_confidence_new_links"]:
    working_rf.extend(item["rf_mhz"])
assert len(working_rf) == 22
assert len(set(working_rf)) == 22

# Later legitimate publication must not invalidate the historical initialization facts.
assert scope["status"] == "published_immutable"
assert scope["current_phase"]["radio_pass1_complete"] is True
assert scope["current_phase"]["deterministic_candidate_built"] is True
assert scope["current_phase"]["aviation_publication_gate_complete"] is True
assert scope["current_phase"]["publication_ready"] is True
assert scope["current_phase"]["published"] is True
assert scope["current_phase"]["public_mutation_performed"] is True
assert scope["radio_scope"]["final_regional_memory_count"] == 41
assert scope["aviation_scope"]["memory_count"] == 19
assert scope["aviation_scope"]["airac09_revalidation_required_on_or_after"] == "2026-09-03"

assert '{ id: "grand-est", name: "Grand Est", memoryCount: 84, marine: false, aviation: 19, version: "v0.3" }' in registry
assert (ROOT / "website/public/downloads/grand-est/radiopack-france-grand-est-v0.3.csv").is_file()

print("Sprint 102 Grand Est v0.3 initialization history preserved after publication: v0.2=59 immutable, v0.3=84 public OK")
