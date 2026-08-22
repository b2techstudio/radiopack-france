#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "research/project-resume-state.json"
EXPECTED_SHA = "02dcba7e14a0cce331b63126ea4e552d41013ebd51aecec19907009f40236a72"
V03_SHA = "b5af25a6766b1181e735d376d3f70ab47ffb9ed67b9e38e35bee15e8a86ae7a5"

state = json.loads(STATE.read_text(encoding="utf-8"))
assert state["updated"] >= "2026-08-22"
assert state["current_sprint"] >= 107
version = tuple(int(part) for part in state["state_version"].split("."))
assert version >= (0, 21, 95)

# Sprint 107 is now a historical publication checkpoint. Later sprints may move
# active_work and next_priority, but BFC v0.4 itself must remain immutable.
bfc = state["public_packs"]["bourgogne_franche_comte"]
assert bfc["version"] == "0.4"
assert bfc["memory_count"] == 61
assert bfc["immutable"] is True
assert bfc["previous_immutable_version"] == "0.3"
assert bfc["previous_memory_count"] == 54
assert bfc["publication_record"] == "research/bourgogne-franche-comte-v0.4/publication-record.json"
assert bfc["public_csv_sha256"] == EXPECTED_SHA

s106 = state["latest_sprint106_bfc_v04_candidate"]
assert s106["sprint"] == 106
assert s106["state_version"] == "0.21.94"
assert s106["status"] == "bfc_v04_release_candidate_frozen_internal"
assert s106["candidate_memory_count"] == 61
assert s106["candidate_memory_delta"] == 7
assert s106["candidate_sha256"] == EXPECTED_SHA
assert s106["published"] is False

s107 = state["latest_sprint107_bfc_v04_publication"]
assert s107["sprint"] == 107
assert s107["state_version"] == "0.21.95"
assert s107["status"] == "bfc_v04_published_immutable"
assert s107["memory_count"] == 61
assert s107["previous_public_version"] == "0.3"
assert s107["previous_memory_count"] == 54
assert s107["aviation_memory_count"] == 14
assert s107["aviation_memory_delta"] == 0
assert s107["inland_vhf_memory_count"] == 7
assert s107["inland_channels"] == [10, 12, 20, 22, 69]
assert s107["paired_rx_channels"] == [20, 22]
assert s107["channel_18_promoted"] is False
assert s107["candidate_public_byte_identity_verified"] is True
assert s107["public_csv_sha256"] == EXPECTED_SHA
assert s107["published"] is True
assert s107["published_version_is_immutable"] is True

record = json.loads((ROOT / "research/bourgogne-franche-comte-v0.4/publication-record.json").read_text(encoding="utf-8"))
scope = json.loads((ROOT / "research/bourgogne-franche-comte-v0.4/release-scope.json").read_text(encoding="utf-8"))
gates = json.loads((ROOT / "research/bourgogne-franche-comte-v0.4/publication-gates.json").read_text(encoding="utf-8"))
assert record["status"] == "published_immutable"
assert record["memory_count"] == 61
assert record["previous_public_version"] == "0.3"
assert record["previous_public_memory_count"] == 54
assert record["previous_public_sha256"] == V03_SHA
assert record["public_csv_sha256"] == EXPECTED_SHA
assert record["candidate_sha256"] == EXPECTED_SHA
assert record["published_version_is_immutable"] is True
assert scope["status"] == "published_immutable"
assert scope["memory_count"] == 61
assert scope["public_csv_sha256"] == EXPECTED_SHA
assert scope["publication"]["candidate_public_byte_identity_verified"] is True
assert gates["status"] == "published_zero_blockers"
assert gates["blocker_count"] == 0
assert gates["public_release_allowed"] is True
assert gates["gates"]["candidate_public_byte_identity_verified"] is True

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert '{ id: "bourgogne-franche-comte", name: "Bourgogne-Franche-Comté", memoryCount: 61, marine: false, aviation: 14, version: "v0.4" }' in registry
regions = json.loads((ROOT / "website/src/data/regions.json").read_text(encoding="utf-8"))
region = next(item for item in regions if item["slug"] == "bourgogne-franche-comte")
assert region["status"] == "v0.4 disponible"
assert region["memoryCount"] == 61
assert "VHF navigation intérieure RX" in region["categories"]

readme = (ROOT / "README.md").read_text(encoding="utf-8")
assert "## Sprint 107 — Bourgogne-Franche-Comté v0.4 publiée" in readme
assert "**Bourgogne-Franche-Comté v0.4** — 61 mémoires RX" in readme
project = (ROOT / "PROJECT_STATUS.md").read_text(encoding="utf-8")
assert "Bourgogne-Franche-Comté v0.4" in project
summary = (ROOT / "research/sprint-107-summary.md").read_text(encoding="utf-8")
assert "61 mémoires RX" in summary
assert EXPECTED_SHA in summary

recent_by_sprint = {item["sprint"]: item for item in state["recent_sprints"]}
assert 107 in recent_by_sprint and 106 in recent_by_sprint
assert recent_by_sprint[107]["state_version"] == "0.21.95"
assert recent_by_sprint[106]["state_version"] == "0.21.94"

# If later ARA publication state exists, it must advance from—not rewrite—the
# Sprint 107 BFC checkpoint.
if state["current_sprint"] >= 109:
    ara = state["public_packs"]["auvergne_rhone_alpes"]
    assert ara["version"] == "0.3"
    assert ara["previous_immutable_version"] == "0.2"
    assert state["latest_sprint109_ara_v03_publication"]["published"] is True

print("Sprint 107 historical guard: BFC v0.4 61 RX remains immutable and byte-identical after later publications OK")
