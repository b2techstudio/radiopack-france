#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
state = json.loads((ROOT / "research/project-resume-state.json").read_text(encoding="utf-8"))
record = json.loads((ROOT / "research/grand-est-v0.3/publication-record.json").read_text(encoding="utf-8"))
scope = json.loads((ROOT / "research/grand-est-v0.3/release-scope.json").read_text(encoding="utf-8"))
aviation = json.loads((ROOT / "research/grand-est-v0.3/aviation-airac08-publication-2026-08-22.json").read_text(encoding="utf-8"))
registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
public_csv = ROOT / "website/public/downloads/grand-est/radiopack-france-grand-est-v0.3.csv"

EXPECTED_SHA = "45aef8547a701e7541e620fa9a2d8394595576921e793b75238146ff6e42e720"

assert state["updated"] == "2026-08-22"
assert state["current_sprint"] == 102
assert state["state_version"] == "0.21.91"

public = state["public_packs"]["grand_est"]
assert public["version"] == "0.3"
assert public["memory_count"] == 84
assert public["immutable"] is True
assert public["previous_immutable_version"] == "0.2"
assert public["previous_memory_count"] == 59
assert public["publication_record"] == "research/grand-est-v0.3/publication-record.json"
assert public["public_csv_sha256"] == EXPECTED_SHA

active = state["active_work"]
assert active["pack"] == "Grand Est"
assert active["target_version"] == "0.3"
assert active["status"] == "published_immutable"
assert active["candidate_memory_count"] == 84
assert active["candidate_aviation_memory_count"] == 19
assert active["candidate_regional_radio_memory_count"] == 41
assert active["candidate_sha256"] == EXPECTED_SHA
assert active["public_csv_sha256"] == EXPECTED_SHA
assert active["aviation_publication_gate_complete"] is True
assert active["aviation_memory_delta"] == 0
assert active["aviation_inherited_unchanged_from_v0_2"] is True
assert active["aviation_new_field_by_field_revalidation_claimed"] is False
assert active["publication_gates_zero_blockers"] is True
assert active["publication_ready"] is True
assert active["published"] is True
assert active["published_version_is_immutable"] is True
assert active["public_mutation_performed"] is True
assert active["airac09_revalidation_required_on_or_after"] == "2026-09-03"

s102 = state["latest_sprint102_grand_est_v03_publication"]
assert s102["sprint"] == 102
assert s102["state_version"] == "0.21.91"
assert s102["status"] == "grand_est_v03_published_immutable"
assert s102["candidate_memory_count"] == 84
assert s102["candidate_aviation_memory_count"] == 19
assert s102["candidate_regional_radio_memory_count"] == 41
assert s102["candidate_sha256"] == EXPECTED_SHA
assert s102["public_csv_sha256"] == EXPECTED_SHA
assert s102["aviation_memory_delta"] == 0
assert s102["aviation_inherited_unchanged_from_v0_2"] is True
assert s102["aviation_new_field_by_field_revalidation_claimed"] is False
assert s102["published"] is True
assert s102["published_version_is_immutable"] is True

assert record["status"] == "published_immutable"
assert record["memory_count"] == 84
assert record["public_csv_sha256"] == EXPECTED_SHA
assert record["candidate_csv_sha256"] == EXPECTED_SHA
assert record["published"] is True
assert record["published_version_is_immutable"] is True
assert scope["status"] == "published_immutable"
assert scope["public"]["memory_count"] == 84
assert scope["public"]["aviation_memory_count"] == 19
assert scope["public"]["regional_radio_memory_count"] == 41
assert scope["public"]["sha256"] == EXPECTED_SHA
assert scope["public"]["byte_identical_to_candidate"] is True
assert aviation["publication_decision"]["memory_count_after"] == 19
assert aviation["publication_decision"]["frequency_delta"] == 0
assert aviation["method"]["new_field_by_field_revalidation_claimed"] is False
assert public_csv.is_file()
assert '{ id: "grand-est", name: "Grand Est", memoryCount: 84, marine: false, aviation: 19, version: "v0.3" }' in registry
assert state["recent_sprints"][0]["sprint"] == 102

print("Sprint 102 state sync: Grand Est v0.3 published immutable 84/19/41, aviation delta=0, exact public SHA OK")
