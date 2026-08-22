#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "research/project-resume-state.json"
EXPECTED_SHA = "ba34604b11b75ae7f0e7aa17e3734053ff37bbe7910218af1ab66e59f3428a5d"
V03_SHA = "45aef8547a701e7541e620fa9a2d8394595576921e793b75238146ff6e42e720"

state = json.loads(STATE.read_text(encoding="utf-8"))
assert state["current_sprint"] == 104
assert state["state_version"] == "0.21.92"

current = state["public_packs"]["grand_est"]
assert current["version"] == "0.4"
assert current["memory_count"] == 97
assert current["immutable"] is True
assert current["previous_immutable_version"] == "0.3"
assert current["previous_memory_count"] == 84
assert current["publication_record"] == "research/grand-est-v0.4/publication-record.json"
assert current["public_csv_sha256"] == EXPECTED_SHA

active = state["active_work"]
assert active["pack"] == "Grand Est"
assert active["target_version"] == "0.4"
assert active["status"] == "published_immutable"
assert active["public_base_version"] == "0.3"
assert active["public_base_memory_count"] == 84
assert active["public_base_sha256"] == V03_SHA
assert active["candidate_memory_count"] == 97
assert active["candidate_aviation_memory_count"] == 19
assert active["candidate_regional_radio_memory_count"] == 41
assert active["candidate_inland_vhf_memory_count"] == 13
assert active["candidate_memory_delta"] == 13
assert active["candidate_sha256"] == EXPECTED_SHA
assert active["public_csv_sha256"] == EXPECTED_SHA
assert active["inland_scope_closed"] is True
assert active["inland_rf_deduplicated"] is True
assert active["aviation_memory_delta"] == 0
assert active["aviation_inherited_unchanged_from_v0_3"] is True
assert active["aviation_new_field_by_field_revalidation_claimed"] is False
assert active["deterministic_candidate_built"] is True
assert active["review_checklist_complete"] is True
assert active["publication_gates_zero_blockers"] is True
assert active["publication_record_frozen"] is True
assert active["publication_ready"] is True
assert active["published"] is True
assert active["published_version_is_immutable"] is True
assert active["public_mutation_performed"] is True
assert active["airac08_publication_allowed_through_inclusive"] == "2026-09-02"
assert active["airac09_revalidation_required_on_or_after"] == "2026-09-03"

s103 = state["latest_sprint103_inland_vhf_audit"]
assert s103["sprint"] == 103
assert s103["status"] == "national_inland_vhf_audit_completed_no_public_mutation"
assert s103["grand_est_candidate_memory_count"] == 97
assert s103["grand_est_verified_inland_vhf_delta"] == 13
assert s103["public_csv_mutation"] is False

s104 = state["latest_sprint104_grand_est_v04_publication"]
assert s104["sprint"] == 104
assert s104["state_version"] == "0.21.92"
assert s104["status"] == "grand_est_v04_published_immutable"
assert s104["memory_count"] == 97
assert s104["previous_public_version"] == "0.3"
assert s104["previous_memory_count"] == 84
assert s104["aviation_memory_count"] == 19
assert s104["aviation_memory_delta"] == 0
assert s104["regional_radio_memory_count"] == 41
assert s104["inland_vhf_memory_count"] == 13
assert s104["public_csv_sha256"] == EXPECTED_SHA

rules = state["resume_rules"]
assert rules["inland_navigation_vhf_is_distinct_from_marine_vhf"] is True
assert rules["shared_inland_marine_rf_must_not_be_duplicated"] is True
assert rules["undocumented_local_navigation_channel_must_not_be_guessed"] is True

record = json.loads((ROOT / "research/grand-est-v0.4/publication-record.json").read_text(encoding="utf-8"))
assert record["status"] == "published_immutable"
assert record["version"] == "0.4"
assert record["memory_count"] == 97
assert record["previous_public_version"] == "0.3"
assert record["previous_public_memory_count"] == 84
assert record["public_csv_sha256"] == EXPECTED_SHA
assert record["published_version_is_immutable"] is True

v03_record = json.loads((ROOT / "research/grand-est-v0.3/publication-record.json").read_text(encoding="utf-8"))
assert v03_record["status"] == "published_immutable"
assert v03_record["version"] == "0.3"
assert v03_record["memory_count"] == 84
assert v03_record["public_csv_sha256"] == V03_SHA

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert '{ id: "grand-est", name: "Grand Est", memoryCount: 97, marine: false, aviation: 19, version: "v0.4" }' in registry

readme = (ROOT / "README.md").read_text(encoding="utf-8")
assert "Sprint 104 / 0.21.92" in readme
assert "**Grand Est v0.4** — 97 mémoires RX" in readme
assert "**1568 mémoires RX cumulées**" in readme
assert "## Sprint 103 — audit VHF navigation intérieure" in readme
assert "## Sprint 102 — Grand Est v0.3 publiée" in readme

status = (ROOT / "PROJECT_STATUS.md").read_text(encoding="utf-8")
assert "Sprint courant : **104**" in status
assert "État logique : **0.21.92**" in status
assert "Grand Est v0.4 : **97 mémoires RX**" in status

summary = (ROOT / "research/sprint-104-summary.md").read_text(encoding="utf-8")
assert "97 mémoires RX" in summary
assert "+13 mémoires VHF de navigation intérieure" in summary
assert EXPECTED_SHA in summary

print("Sprint 104 state sync: Grand Est v0.4 / 97 RX / +13 inland VHF published immutable and historical states preserved OK")
