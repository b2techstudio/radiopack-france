#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
state = json.loads((ROOT / "research/project-resume-state.json").read_text(encoding="utf-8"))
readme = (ROOT / "README.md").read_text(encoding="utf-8")
project = (ROOT / "PROJECT_STATUS.md").read_text(encoding="utf-8")
changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
radio = json.loads((ROOT / "research/ile-de-france-v0.3/radio-validation-2026-08-21.json").read_text(encoding="utf-8"))
aviation = json.loads((ROOT / "research/ile-de-france-v0.3/aviation-airac08-2026-08-21.json").read_text(encoding="utf-8"))
scope = json.loads((ROOT / "research/ile-de-france-v0.3/release-scope.json").read_text(encoding="utf-8"))

assert state["updated"] == "2026-08-21"
assert state["current_sprint"] == 101
assert state["state_version"] == "0.21.90"
assert "**État courant : Sprint 101 / 0.21.90" in readme
assert "Sprint courant : **101**" in project
assert "État logique : **0.21.90**" in project
assert changelog.startswith("# Changelog\n\n## 0.21.90 - 2026-08-21")
assert (ROOT / "research/sprint-101-summary.md").is_file()

idf_public = state["public_packs"]["ile_de_france"]
assert idf_public["version"] == "0.2"
assert idf_public["memory_count"] == 58
assert idf_public["immutable"] is True

active = state["active_work"]
assert active["pack"] == "Île-de-France"
assert active["target_version"] == "0.3"
assert active["public_base_version"] == "0.2"
assert active["public_base_memory_count"] == 58
assert active["published_base_aviation_memory_count"] == 18
assert active["working_new_promoted_station_count"] == 2
assert active["publication_ready"] is False
assert active["radio_validation"] == "research/ile-de-france-v0.3/radio-validation-2026-08-21.json"
assert active["aviation_validation"] == "research/ile-de-france-v0.3/aviation-airac08-2026-08-21.json"
assert active["release_scope"] == "research/ile-de-france-v0.3/release-scope.json"

s101 = state["latest_sprint101_idf_v03_research"]
assert s101["sprint"] == 101
assert s101["state_version"] == "0.21.90"
assert s101["public_base_memory_count"] == 58
assert s101["publication_ready"] is False
assert s101["public_csv_mutation"] is False
assert s101["rf_publication_mutation"] is False

assert state["recent_sprints"][0]["sprint"] == 101
assert state["recent_sprints"][0]["state_version"] == "0.21.90"

assert radio["published_base_memory_count"] == 58
assert radio["result"]["working_new_promoted_station_count"] == 2
assert radio["result"]["publication_ready"] is False
assert aviation["published_v0_2_aviation_memory_count"] == 18
assert aviation["current_airac"] == "08/26"
assert aviation["next_airac"]["effective_from"] == "2026-09-03"
assert aviation["gates"]["publication_allowed"] is False
assert scope["publication_ready"] is False

bretagne = state["bretagne_v0_3_airac_handoff"]
assert bretagne["candidate_memory_count"] == 151
assert bretagne["candidate_memory_delta"] == 0
assert bretagne["airac_next_effective_from"] == "2026-09-03"

print("Sprint 101 state sync: IDF v0.3 research active, public v0.2/58 immutable, release gates open OK")
