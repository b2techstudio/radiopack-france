#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "research/project-resume-state.json"
EXPECTED_SHA = "02dcba7e14a0cce331b63126ea4e552d41013ebd51aecec19907009f40236a72"
V03_SHA = "b5af25a6766b1181e735d376d3f70ab47ffb9ed67b9e38e35bee15e8a86ae7a5"

state = json.loads(STATE.read_text(encoding="utf-8"))
assert state["updated"] == "2026-08-22"
assert state["current_sprint"] == 107
assert state["state_version"] == "0.21.95"

bfc = state["public_packs"]["bourgogne_franche_comte"]
assert bfc["version"] == "0.4"
assert bfc["memory_count"] == 61
assert bfc["immutable"] is True
assert bfc["previous_immutable_version"] == "0.3"
assert bfc["previous_memory_count"] == 54
assert bfc["publication_record"] == "research/bourgogne-franche-comte-v0.4/publication-record.json"
assert bfc["public_csv_sha256"] == EXPECTED_SHA

active = state["active_work"]
assert active["pack"] == "Bourgogne-Franche-Comté"
assert active["target_version"] == "0.4"
assert active["status"] == "published_immutable"
assert active["public_base_version"] == "0.3"
assert active["public_base_memory_count"] == 54
assert active["public_base_sha256"] == V03_SHA
assert active["candidate_memory_count"] == 61
assert active["candidate_inland_vhf_memory_count"] == 7
assert active["candidate_memory_delta"] == 7
assert active["candidate_sha256"] == EXPECTED_SHA
assert active["public_csv_sha256"] == EXPECTED_SHA
assert active["candidate_public_byte_identity_verified"] is True
assert active["publication_gates_zero_blockers"] is True
assert active["published"] is True
assert active["published_version_is_immutable"] is True

next_priority = state["next_priority"]
assert next_priority["pack"] == "Auvergne-Rhône-Alpes"
assert next_priority["target_version"] == "0.3"
assert next_priority["public_base_version"] == "0.2"
assert next_priority["public_base_memory_count"] == 62
assert next_priority["minimum_verified_inland_vhf_rf_delta"] == 9

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
assert "Sprint 107 / 0.21.95" in readme
assert "## Sprint 107 — Bourgogne-Franche-Comté v0.4 publiée" in readme
assert "**1582 mémoires RX cumulées**" in readme
project = (ROOT / "PROJECT_STATUS.md").read_text(encoding="utf-8")
assert "Sprint courant : **107**" in project
assert "État logique : **0.21.95**" in project
summary = (ROOT / "research/sprint-107-summary.md").read_text(encoding="utf-8")
assert "61 mémoires RX" in summary
assert EXPECTED_SHA in summary

assert state["recent_sprints"][0]["sprint"] == 107
assert state["recent_sprints"][1]["sprint"] == 106

print("Sprint 107 state sync: BFC v0.4 61 RX published immutable, byte-identical frozen SHA, ARA v0.3 next priority OK")
