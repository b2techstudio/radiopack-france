#!/usr/bin/env python3
"""One-shot Sprint 105 project state finalizer.

This script is intentionally used only on the Sprint 105 feature branch and is
removed before merge. It mutates project-resume-state.json structurally so the
large state file is not edited through brittle text replacement.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "research/project-resume-state.json"
SHA = "14e1d1d95b38ef44d01b9cccb989a3f1567153ac64875594cc24bd4b57a1cdc2"
BASE_SHA = "e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125"

state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
state["updated"] = "2026-08-22"
state["current_sprint"] = 105
state["state_version"] = "0.21.93"

state["public_packs"]["ile_de_france"] = {
    "version": "0.4",
    "memory_count": 64,
    "immutable": True,
    "previous_immutable_version": "0.3",
    "previous_memory_count": 57,
    "publication_record": "research/ile-de-france-v0.4/publication-record.json",
    "public_csv_sha256": SHA,
}

state["active_work"] = {
    "pack": "Île-de-France",
    "target_version": "0.4",
    "status": "published_immutable",
    "public_base_version": "0.3",
    "public_base_memory_count": 57,
    "public_base_sha256": BASE_SHA,
    "candidate_memory_count": 64,
    "candidate_aviation_memory_count": 18,
    "candidate_regional_radio_memory_count": 15,
    "candidate_inland_vhf_memory_count": 7,
    "candidate_memory_delta": 7,
    "candidate_sha256": SHA,
    "public_csv_sha256": SHA,
    "inland_scope_closed": True,
    "inland_rf_deduplicated": True,
    "channel_69_promoted": False,
    "marine_channel_16_promoted": False,
    "aviation_memory_delta": 0,
    "aviation_inherited_unchanged_from_v0_3": True,
    "aviation_new_field_by_field_revalidation_claimed": False,
    "deterministic_candidate_built": True,
    "review_checklist_complete": True,
    "publication_gates_zero_blockers": True,
    "publication_record_frozen": True,
    "publication_ready": True,
    "published": True,
    "published_version_is_immutable": True,
    "public_mutation_performed": True,
    "inland_validation": "research/ile-de-france-v0.4/inland-vhf-validation-2026-08-22.json",
    "aviation_validation": "research/ile-de-france-v0.4/aviation-airac08-publication-2026-08-22.json",
    "candidate_manifest": "research/ile-de-france-v0.4/generated/release-candidate/candidate-manifest.json",
    "candidate_csv": "research/ile-de-france-v0.4/generated/release-candidate/radiopack-france-ile-de-france-v0.4-candidate.csv",
    "public_csv": "website/public/downloads/ile-de-france/radiopack-france-ile-de-france-v0.4.csv",
    "builder": "tools/build_idf_v04_candidate.py",
    "review_checklist": "research/ile-de-france-v0.4/review-checklist.json",
    "publication_gates": "research/ile-de-france-v0.4/publication-gates.json",
    "publication_record": "research/ile-de-france-v0.4/publication-record.json",
    "release_scope": "research/ile-de-france-v0.4/release-scope.json",
    "published_on": "2026-08-22",
    "airac08_publication_allowed_through_inclusive": "2026-09-02",
    "airac09_revalidation_required_on_or_after": "2026-09-03",
}

state["latest_sprint105_idf_v04_publication"] = {
    "sprint": 105,
    "state_version": "0.21.93",
    "completed_on": "2026-08-22",
    "status": "idf_v04_published_immutable",
    "memory_count": 64,
    "previous_public_version": "0.3",
    "previous_memory_count": 57,
    "aviation_memory_count": 18,
    "aviation_memory_delta": 0,
    "regional_radio_memory_count": 15,
    "regional_radio_memory_delta": 0,
    "inland_vhf_memory_count": 7,
    "inland_vhf_memory_delta": 7,
    "inland_channels": [10, 18, 20, 22],
    "channel_69_promoted": False,
    "public_csv_sha256": SHA,
    "publication_record": "research/ile-de-france-v0.4/publication-record.json",
    "summary": "research/sprint-105-summary.md",
    "published": True,
    "published_version_is_immutable": True,
}

entry = {
    "sprint": 105,
    "state_version": "0.21.93",
    "summary": "Île-de-France v0.4 published immutable at 64 RX by adding 7 verified inland-navigation VHF memories to immutable v0.3; aviation 18 and regional radio 15 remain unchanged; channel 69 is not promoted; candidate/public SHA-256 " + SHA + ".",
    "summary_file": "research/sprint-105-summary.md",
}
recent = [item for item in state.get("recent_sprints", []) if item.get("sprint") != 105]
state["recent_sprints"] = [entry] + recent

rules = state.setdefault("resume_rules", {})
rules["inland_navigation_vhf_is_distinct_from_marine_vhf"] = True
rules["shared_inland_marine_rf_must_not_be_duplicated"] = True
rules["undocumented_local_navigation_channel_must_not_be_guessed"] = True
rules["temporary_navigation_channel_requires_current_evidence_before_promotion"] = True

STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Sprint 105 state finalized: IDF v0.4 / 64 RX / +7 inland VHF / 0 blockers")
