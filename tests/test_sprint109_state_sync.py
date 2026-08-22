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
assert state["current_sprint"] >= 109
assert state["state_version"].startswith("0.21.")
assert state["updated"] == "2026-08-22"

ara = state["public_packs"]["auvergne_rhone_alpes"]
assert ara["version"] == "0.3"
assert ara["memory_count"] == 71
assert ara["immutable"] is True
assert ara["previous_immutable_version"] == "0.2"
assert ara["previous_memory_count"] == 62
assert ara["publication_record"] == "research/auvergne-rhone-alpes-v0.3/publication-record.json"
assert ara["public_csv_sha256"] == ARA_V03_SHA

# Current active work may advance after Sprint 109; the ARA publication snapshot below is historical.

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

recent_by_sprint = {item["sprint"]: item for item in state["recent_sprints"]}
assert recent_by_sprint[109]["state_version"] == "0.21.97"
assert recent_by_sprint[108]["state_version"] == "0.21.96"
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
    "## Sprint 109 — Auvergne-Rhône-Alpes v0.3 publiée",
    "Auvergne-Rhône-Alpes v0.3 : **71 mémoires RX**",
    "**Priorité actionnable actuelle.**",
    "Normandie v0.5",
]:
    assert token in status, token

print("Sprint 109 historical guard: ARA v0.3=71 immutable, v0.2=62 historical, byte identity SHA frozen after later state advances OK")
