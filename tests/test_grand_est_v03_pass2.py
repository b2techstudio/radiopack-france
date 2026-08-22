#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V03 = ROOT / "research" / "grand-est-v0.3"

pass1 = json.loads((V03 / "radio-validation-pass1-2026-08-22.json").read_text(encoding="utf-8"))
pass2 = json.loads((V03 / "radio-validation-pass2-2026-08-22.json").read_text(encoding="utf-8"))
backlog = json.loads((V03 / "backlog.json").read_text(encoding="utf-8"))
scope = json.loads((V03 / "release-scope.json").read_text(encoding="utf-8"))
registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")

# Pass 2 is immutable historical research evidence even when pass 3 later closes scope.
assert pass2["status"] == "second_source_pass_complete_with_backlog_no_public_mutation"
assert pass2["public_base"]["version"] == "0.2"
assert pass2["public_base"]["memory_count"] == 59
assert pass2["public_base"]["non_regional_memory_count"] == 43
assert pass2["public_base"]["public_csv_sha256"] == "a50416bd8a88af249bb691daa657ffd4b578daf1324bd0ca4dd632a2f1a0e5c1"
assert pass2["public_base"]["immutable"] is True

validated_calls = {item["call"] for item in pass2["validated_in_pass2"]}
assert validated_calls == {"F1ZEK", "F1ZXX", "F5ZFT", "F1ZGN", "F1ZGP", "F5ZDJ", "F1ZDA", "F1ZBV"}

rf = []
for item in pass1["v02_first_pass_safe_carry"]:
    rf.extend(item["rf_mhz"])
for item in pass1["high_confidence_new_links"]:
    rf.extend(item["rf_mhz"])
for item in pass2["validated_in_pass2"]:
    assert len(item["rf_mhz"]) == 2
    assert item["rf_mhz"][0] != item["rf_mhz"][1]
    rf.extend(item["rf_mhz"])

assert rf.count(432.5375) == 4
assert len(set(rf)) == 35
assert pass2["pass2_rf_accounting"]["shared_rf_mhz"] == [432.5375]
assert pass2["pass2_rf_accounting"]["shared_rf_occurrence_count"] == 4
assert pass2["pass2_rf_accounting"]["unique_rf_added_by_pass2"] == 13
assert pass2["pass2_rf_accounting"]["regional_unique_rf_working_count"] == 35
assert pass2["pass2_rf_accounting"]["validated_working_memory_count"] == 78
assert pass2["pass2_rf_accounting"]["validated_working_memory_count_is_release_candidate"] is False
assert pass2["pass2_rf_accounting"]["final_count_frozen"] is False

resolved = {item["call"]: item["decision"] for item in pass2["resolved_as_excluded_or_deferred"]}
assert resolved == {
    "F1ZAX": "defer",
    "F5ZBD": "exclude_while_off_service",
    "F1ZBU": "exclude_from_analog_scope",
    "F1ZCV": "defer_attribution_zero_rf_delta",
}
assert set(pass2["still_open_for_fresh_local_corroboration"]) == {
    "F5ZRP", "F5ZTY", "F1ZFL", "F5ZCC", "F1ZJS", "F5ZUK", "F1ZFN", "F1ZEF"
}

for key in ["rx_only", "paired_rx_for_distinct_verified_pairs", "same_rf_frequency_deduplicated", "no_artificial_fill"]:
    assert pass2["rules"][key] is True
assert pass2["rules"]["chirp_duplex"] == "off"
assert pass2["rules"]["chirp_offset"] == "0.000000"
assert pass2["rules"]["maximum_memories"] == 200
assert pass2["rules"]["public_mutation"] is False
assert pass2["rules"]["candidate_built"] is False

# Current research may be later than pass 2, but cannot regress public safety.
assert scope["current_phase"]["radio_pass2_complete"] is True
assert scope["current_phase"]["deterministic_candidate_built"] is False
assert scope["current_phase"]["publication_ready"] is False
assert scope["current_phase"]["public_mutation_performed"] is False
assert backlog["status"] in {"pass2_reduced_backlog", "radio_scope_closed_with_explicit_deferrals"}

assert '{ id: "grand-est", name: "Grand Est", memoryCount: 59, marine: false, aviation: 19, version: "v0.2" }' in registry
assert not (ROOT / "website/public/downloads/grand-est/radiopack-france-grand-est-v0.3.csv").exists()

print("Sprint 102 Grand Est v0.3 pass2 historical evidence: 8 links / 35 regional RF checkpoint preserved across later scope closure, public=false OK")
