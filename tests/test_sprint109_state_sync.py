#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "research/project-resume-state.json"
ARA_V02_RECORD = ROOT / "research/auvergne-rhone-alpes-v0.2/publication-record.json"
ARA_V03_RECORD = ROOT / "research/auvergne-rhone-alpes-v0.3/publication-record.json"
ARA_FREEZE = ROOT / "research/auvergne-rhone-alpes-v0.3/candidate-freeze.json"
README = ROOT / "README.md"
STATUS = ROOT / "PROJECT_STATUS.md"
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"
REGIONS = ROOT / "website/src/data/regions.json"

ARA_V02_SHA = "60b4f96467419db40e9f3f33076057f4e093853c81d9e3315b8fe7f0459daa53"
ARA_V03_SHA = "b44a95486af5fd89fa72246ed7c8f0ab79e3084f6b0429df5215fba9918d691e"

for path in [STATE, ARA_V02_RECORD, ARA_V03_RECORD, ARA_FREEZE, README, STATUS, REGISTRY, REGIONS]:
    assert path.is_file(), path

state = json.loads(STATE.read_text(encoding="utf-8"))
assert state["current_sprint"] == 109
assert state["state_version"] == "0.21.97"
assert state["updated"] == "2026-08-22"

ara = state["public_packs"]["auvergne_rhone_alpes"]
assert ara["version"] == "0.3"
assert ara["memory_count"] == 71
assert ara["immutable"] is True
assert ara["previous_immutable_version"] == "0.2"
assert ara["previous_memory_count"] == 62
assert ara["publication_record"] == "research/auvergne-rhone-alpes-v0.3/publication-record.json"
assert ara["public_csv_sha256"] == ARA_V03_SHA

active = state["active_work"]
assert active["pack"] == "Auvergne-Rhône-Alpes"
assert active["target_version"] == "0.3"
assert active["status"] == "published_immutable"
assert active["public_base_version"] == "0.2"
assert active["public_base_memory_count"] == 62
assert active["public_base_sha256"] == ARA_V02_SHA
assert active["candidate_memory_count"] == 71
assert active["candidate_aviation_memory_count"] == 18
assert active["candidate_inland_vhf_memory_count"] == 9
assert active["candidate_memory_delta"] == 9
assert active["candidate_sha256"] == ARA_V03_SHA
assert active["public_csv_sha256"] == ARA_V03_SHA
assert active["channel_18_boat_side_only"] is True
assert active["channel_18_shore_side_promoted"] is False
assert active["marine_channel_16_promoted"] is False
assert active["aviation_memory_delta"] == 0
assert active["aviation_inherited_unchanged_from_v0_2"] is True
assert active["candidate_public_byte_identity_verified"] is True
assert active["publication_gates_zero_blockers"] is True
assert active["published"] is True
assert active["published_version_is_immutable"] is True
assert active["public_mutation_performed"] is True
assert active["airac08_publication_allowed_through_inclusive"] == "2026-09-02"
assert active["airac09_revalidation_required_on_or_after"] == "2026-09-03"

priority = state["next_priority"]
assert priority["pack"] == "Normandie"
assert priority["target_version"] == "0.5"
assert priority["status"] == "field_validation_required_before_any_promotion"
assert priority["public_base_version"] == "0.4"
assert priority["public_base_memory_count"] == 142
assert priority["candidate_memory_count"] == 142
assert priority["candidate_memory_delta"] == 0
assert priority["known_potential_ceiling_excluding_f6zes"] == 147
assert priority["field_required"] == ["R3_F1ZBX", "F5ZHA"]
assert priority["source_watch"] == ["F1ZOV", "F6ZES"]
assert priority["evidence"] == "research/normandie-v0.5/sprint90-source-refresh.json"

s108 = state["latest_sprint108_ara_v03_candidate"]
assert s108["sprint"] == 108
assert s108["state_version"] == "0.21.96"
assert s108["status"] == "ara_v03_internal_candidate_frozen_not_public"
assert s108["candidate_memory_count"] == 71
assert s108["candidate_memory_delta"] == 9
assert s108["candidate_sha256"] == ARA_V03_SHA
assert s108["published"] is False

s109 = state["latest_sprint109_ara_v03_publication"]
assert s109["sprint"] == 109
assert s109["state_version"] == "0.21.97"
assert s109["status"] == "ara_v03_published_immutable"
assert s109["memory_count"] == 71
assert s109["previous_public_version"] == "0.2"
assert s109["previous_memory_count"] == 62
assert s109["inland_vhf_memory_count"] == 9
assert s109["paired_rx_channels"] == [19, 20, 22]
assert s109["channel_18_boat_side_only"] is True
assert s109["candidate_public_byte_identity_verified"] is True
assert s109["public_csv_sha256"] == ARA_V03_SHA
assert s109["published"] is True
assert s109["published_version_is_immutable"] is True

assert state["recent_sprints"][0]["sprint"] == 109
assert state["recent_sprints"][0]["state_version"] == "0.21.97"
assert state["recent_sprints"][1]["sprint"] == 108
assert state["recent_sprints"][1]["state_version"] == "0.21.96"
for source in [
    "research/auvergne-rhone-alpes-v0.3/candidate-freeze.json",
    "research/auvergne-rhone-alpes-v0.3/publication-record.json",
    "tests/test_ara_v03_publication.py",
    "website/src/lib/araPack.ts",
    "research/sprint-108-summary.md",
    "research/sprint-109-summary.md",
]:
    assert source in state["sources_of_truth"]

v02 = json.loads(ARA_V02_RECORD.read_text(encoding="utf-8"))
assert v02["status"] == "published_immutable"
assert v02["version"] == "0.2"
assert v02["memory_count"] == 62
assert v02["public_csv_sha256"] == ARA_V02_SHA
assert v02["published_version_is_immutable"] is True

freeze = json.loads(ARA_FREEZE.read_text(encoding="utf-8"))
assert freeze["status"] == "internal_candidate_frozen_not_public"
assert freeze["candidate_memory_count"] == 71
assert freeze["candidate_sha256"] == ARA_V03_SHA
assert freeze["published"] is False

v03 = json.loads(ARA_V03_RECORD.read_text(encoding="utf-8"))
assert v03["status"] == "published_immutable"
assert v03["publication_sprint"] == 109
assert v03["version"] == "0.3"
assert v03["memory_count"] == 71
assert v03["previous_public_version"] == "0.2"
assert v03["previous_public_memory_count"] == 62
assert v03["previous_public_sha256"] == ARA_V02_SHA
assert v03["candidate_sha256"] == ARA_V03_SHA
assert v03["public_csv_sha256"] == ARA_V03_SHA
assert v03["published_version_is_immutable"] is True

bretagne = state["bretagne_v0_3_airac_handoff"]
assert bretagne["airac_current_until_inclusive"] == "2026-09-02"
assert bretagne["airac_next_effective_from"] == "2026-09-03"
assert bretagne["publication_allowed_before_airac09_revalidation"] is False

registry = REGISTRY.read_text(encoding="utf-8")
assert '{ id: "auvergne-rhone-alpes", name: "Auvergne-Rhône-Alpes", memoryCount: 71, marine: false, aviation: 18, version: "v0.3" }' in registry
regions = json.loads(REGIONS.read_text(encoding="utf-8"))
ara_region = next(item for item in regions if item["slug"] == "auvergne-rhone-alpes")
assert ara_region["status"] == "v0.3 disponible"
assert ara_region["memoryCount"] == 71

readme = README.read_text(encoding="utf-8")
for token in [
    "Sprint 109 / 0.21.97",
    "Auvergne-Rhône-Alpes v0.3",
    "71 mémoires RX",
    "1591 mémoires RX cumulées",
    "## Sprint 109 — Auvergne-Rhône-Alpes v0.3 publiée",
    "## Sprint 108 — candidat ARA v0.3 figé",
    "Normandie v0.5",
]:
    assert token in readme, token

status = STATUS.read_text(encoding="utf-8")
for token in [
    "Sprint courant : **109**",
    "État logique : **0.21.97**",
    "Auvergne-Rhône-Alpes v0.3 : **71 mémoires RX**",
    "**Priorité actionnable actuelle.**",
    "Normandie v0.5",
]:
    assert token in status, token

print("Sprint 109 state sync: ARA v0.3=71 immutable, v0.2=62 historical, byte identity SHA frozen, next priority Normandie v0.5 OK")
