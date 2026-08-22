#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "research/project-resume-state.json"
ARA_RECORD = ROOT / "research/auvergne-rhone-alpes-v0.3/publication-record.json"

ARA_BASE_SHA = "60b4f96467419db40e9f3f33076057f4e093853c81d9e3315b8fe7f0459daa53"
ARA_V03_SHA = "b44a95486af5fd89fa72246ed7c8f0ab79e3084f6b0429df5215fba9918d691e"

state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
record = json.loads(ARA_RECORD.read_text(encoding="utf-8"))

assert state["current_sprint"] == 107, state["current_sprint"]
assert state["state_version"] == "0.21.95", state["state_version"]
assert record["status"] == "published_immutable"
assert record["publication_sprint"] == 109
assert record["version"] == "0.3"
assert record["memory_count"] == 71
assert record["previous_public_version"] == "0.2"
assert record["previous_public_memory_count"] == 62
assert record["previous_public_sha256"] == ARA_BASE_SHA
assert record["public_csv_sha256"] == ARA_V03_SHA
assert record["candidate_sha256"] == ARA_V03_SHA
assert record["published_version_is_immutable"] is True

state["updated"] = "2026-08-22"
state["current_sprint"] = 109
state["state_version"] = "0.21.97"

state["public_packs"]["auvergne_rhone_alpes"] = {
    "version": "0.3",
    "memory_count": 71,
    "immutable": True,
    "previous_immutable_version": "0.2",
    "previous_memory_count": 62,
    "publication_record": "research/auvergne-rhone-alpes-v0.3/publication-record.json",
    "public_csv_sha256": ARA_V03_SHA,
}

state["active_work"] = {
    "pack": "Auvergne-Rhône-Alpes",
    "target_version": "0.3",
    "status": "published_immutable",
    "public_base_version": "0.2",
    "public_base_memory_count": 62,
    "public_base_sha256": ARA_BASE_SHA,
    "candidate_memory_count": 71,
    "candidate_aviation_memory_count": 18,
    "candidate_inland_vhf_memory_count": 9,
    "candidate_memory_delta": 9,
    "candidate_sha256": ARA_V03_SHA,
    "public_csv_sha256": ARA_V03_SHA,
    "inland_scope_closed": True,
    "inland_rf_deduplicated": True,
    "channel_18_boat_side_only": True,
    "channel_18_shore_side_promoted": False,
    "marine_channel_16_promoted": False,
    "aviation_memory_delta": 0,
    "aviation_inherited_unchanged_from_v0_2": True,
    "deterministic_candidate_built": True,
    "candidate_public_byte_identity_verified": True,
    "publication_gates_zero_blockers": True,
    "publication_record_frozen": True,
    "publication_ready": True,
    "published": True,
    "published_version_is_immutable": True,
    "public_mutation_performed": True,
    "inland_validation": "research/auvergne-rhone-alpes-v0.3/inland-vhf-validation-2026-08-22.json",
    "candidate_freeze": "research/auvergne-rhone-alpes-v0.3/candidate-freeze.json",
    "release_scope": "research/auvergne-rhone-alpes-v0.3/release-scope.json",
    "publication_gates": "research/auvergne-rhone-alpes-v0.3/publication-gates.json",
    "publication_record": "research/auvergne-rhone-alpes-v0.3/publication-record.json",
    "builder": "tools/build_ara_v03_candidate.py",
    "published_on": "2026-08-22",
    "airac08_publication_allowed_through_inclusive": "2026-09-02",
    "airac09_revalidation_required_on_or_after": "2026-09-03",
}

state["next_priority"] = {
    "pack": "Normandie",
    "target_version": "0.5",
    "status": "field_validation_required_before_any_promotion",
    "public_base_version": "0.4",
    "public_base_memory_count": 142,
    "candidate_memory_count": 142,
    "candidate_memory_delta": 0,
    "known_potential_ceiling_excluding_f6zes": 147,
    "field_required": ["R3_F1ZBX", "F5ZHA"],
    "source_watch": ["F1ZOV", "F6ZES"],
    "evidence": "research/normandie-v0.5/sprint90-source-refresh.json",
    "reason": "ARA closes the verified non-coastal inland-VHF queue from Sprint 103. Bretagne AIRAC 09/26 is not effective before 2026-09-03, so Normandie v0.5 field/source gates are the actionable current priority.",
}

state["latest_sprint108_ara_v03_candidate"] = {
    "sprint": 108,
    "state_version": "0.21.96",
    "completed_on": "2026-08-22",
    "status": "ara_v03_internal_candidate_frozen_not_public",
    "public_base_version": "0.2",
    "public_base_memory_count": 62,
    "candidate_memory_count": 71,
    "candidate_memory_delta": 9,
    "aviation_memory_count": 18,
    "aviation_memory_delta": 0,
    "inland_vhf_memory_count": 9,
    "inland_channels": [10, 12, 18, 19, 20, 22],
    "paired_rx_channels": [19, 20, 22],
    "channel_18_boat_side_only": True,
    "marine_channel_16_promoted": False,
    "candidate_sha256": ARA_V03_SHA,
    "candidate_freeze": "research/auvergne-rhone-alpes-v0.3/candidate-freeze.json",
    "summary": "research/sprint-108-summary.md",
    "published": False,
}

state["latest_sprint109_ara_v03_publication"] = {
    "sprint": 109,
    "state_version": "0.21.97",
    "completed_on": "2026-08-22",
    "status": "ara_v03_published_immutable",
    "memory_count": 71,
    "previous_public_version": "0.2",
    "previous_memory_count": 62,
    "aviation_memory_count": 18,
    "aviation_memory_delta": 0,
    "inland_vhf_memory_count": 9,
    "inland_vhf_memory_delta": 9,
    "inland_channels": [10, 12, 18, 19, 20, 22],
    "paired_rx_channels": [19, 20, 22],
    "channel_18_boat_side_only": True,
    "candidate_public_byte_identity_verified": True,
    "public_csv_sha256": ARA_V03_SHA,
    "publication_record": "research/auvergne-rhone-alpes-v0.3/publication-record.json",
    "summary": "research/sprint-109-summary.md",
    "published": True,
    "published_version_is_immutable": True,
}

source_additions = [
    "data/regional/auvergne-rhone-alpes-inland-vhf-rx.json",
    "research/auvergne-rhone-alpes-v0.3/inland-vhf-validation-2026-08-22.json",
    "research/auvergne-rhone-alpes-v0.3/candidate-freeze.json",
    "research/auvergne-rhone-alpes-v0.3/release-scope.json",
    "research/auvergne-rhone-alpes-v0.3/publication-gates.json",
    "research/auvergne-rhone-alpes-v0.3/publication-record.json",
    "tools/build_ara_v03_candidate.py",
    "tests/test_ara_v03_candidate.py",
    "tests/test_ara_v03_publication.py",
    "website/src/lib/araPack.ts",
    "research/sprint-108-summary.md",
    "research/sprint-109-summary.md",
]
for item in source_additions:
    if item not in state["sources_of_truth"]:
        state["sources_of_truth"].append(item)

recent = [item for item in state["recent_sprints"] if item["sprint"] not in {108, 109}]
state["recent_sprints"] = [
    {
        "sprint": 109,
        "state_version": "0.21.97",
        "summary": "Auvergne-Rhône-Alpes v0.3 published immutable at 71 RX by adding 9 verified inland-navigation VHF memories to immutable v0.2; public Astro CSV is byte-identical to the Sprint 108 frozen candidate at SHA-256 b44a95486af5fd89fa72246ed7c8f0ab79e3084f6b0429df5215fba9918d691e.",
        "summary_file": "research/sprint-109-summary.md",
    },
    {
        "sprint": 108,
        "state_version": "0.21.96",
        "summary": "Auvergne-Rhône-Alpes v0.3 internal candidate frozen at 71 RX with +9 verified inland-navigation VHF memories and SHA-256 b44a95486af5fd89fa72246ed7c8f0ab79e3084f6b0429df5215fba9918d691e; no public mutation in Sprint 108.",
        "summary_file": "research/sprint-108-summary.md",
    },
    *recent,
]

STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Sprint 109 canonical state synchronized: 0.21.97, ARA v0.3=71, next=Normandie v0.5")
