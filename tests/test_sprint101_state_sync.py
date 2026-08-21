#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
state = json.loads((ROOT / "research/project-resume-state.json").read_text(encoding="utf-8"))
readme = (ROOT / "README.md").read_text(encoding="utf-8")
project = (ROOT / "PROJECT_STATUS.md").read_text(encoding="utf-8")
changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
radio_initial = json.loads((ROOT / "research/ile-de-france-v0.3/radio-validation-2026-08-21.json").read_text(encoding="utf-8"))
radio_pass2 = json.loads((ROOT / "research/ile-de-france-v0.3/radio-validation-pass2-2026-08-21.json").read_text(encoding="utf-8"))
aviation_initial = json.loads((ROOT / "research/ile-de-france-v0.3/aviation-airac08-2026-08-21.json").read_text(encoding="utf-8"))
aviation_pass2 = json.loads((ROOT / "research/ile-de-france-v0.3/aviation-validation-pass2-2026-08-21.json").read_text(encoding="utf-8"))
scope = json.loads((ROOT / "research/ile-de-france-v0.3/release-scope.json").read_text(encoding="utf-8"))

assert state["updated"] == "2026-08-21"
assert state["current_sprint"] == 101
assert state["state_version"] == "0.21.90"
assert "**État courant : Sprint 101 / 0.21.90" in readme
assert "Sprint courant : **101**" in project
assert "État logique : **0.21.90**" in project
assert "Compteur de travail provisoire **57 RX**" in project
assert changelog.startswith("# Changelog\n\n## 0.21.90 - 2026-08-21")
assert (ROOT / "research/sprint-101-summary.md").is_file()

idf_public = state["public_packs"]["ile_de_france"]
assert idf_public["version"] == "0.2"
assert idf_public["memory_count"] == 58
assert idf_public["immutable"] is True

active = state["active_work"]
assert active["pack"] == "Île-de-France"
assert active["target_version"] == "0.3"
assert active["status"] == "research_pass2_open_not_release_candidate"
assert active["public_base_version"] == "0.2"
assert active["public_base_memory_count"] == 58
assert active["published_base_aviation_memory_count"] == 18
assert active["provisional_working_memory_count"] == 57
assert active["provisional_aviation_memory_count"] == 18
assert active["release_candidate_memory_count"] is None
assert active["radio_source_conflicts_closed"] is False
assert active["radio_memory_accounting_final"] is False
assert active["aviation_revalidation_complete"] is False
assert active["publication_ready"] is False
assert active["initial_radio_validation"] == "research/ile-de-france-v0.3/radio-validation-2026-08-21.json"
assert active["radio_validation"] == "research/ile-de-france-v0.3/radio-validation-pass2-2026-08-21.json"
assert active["initial_aviation_validation"] == "research/ile-de-france-v0.3/aviation-airac08-2026-08-21.json"
assert active["aviation_validation"] == "research/ile-de-france-v0.3/aviation-validation-pass2-2026-08-21.json"
assert active["release_scope"] == "research/ile-de-france-v0.3/release-scope.json"

s101 = state["latest_sprint101_idf_v03_research"]
assert s101["sprint"] == 101
assert s101["state_version"] == "0.21.90"
assert s101["status"] == "ile_de_france_v03_pass2_research_checkpoint_open"
assert s101["public_base_memory_count"] == 58
assert s101["provisional_working_memory_count"] == 57
assert s101["provisional_aviation_memory_count"] == 18
assert s101["publication_ready"] is False
assert s101["public_csv_mutation"] is False
assert s101["rf_publication_mutation"] is False

assert state["recent_sprints"][0]["sprint"] == 101
assert state["recent_sprints"][0]["state_version"] == "0.21.90"
assert "provisional 57 RX" in state["recent_sprints"][0]["summary"]

assert radio_initial["published_base_memory_count"] == 58
assert radio_initial["result"]["publication_ready"] is False
assert radio_pass2["result"]["provisional_working_memory_count"] == 57
assert radio_pass2["result"]["publication_ready"] is False
assert aviation_initial["published_v0_2_aviation_memory_count"] == 18
assert aviation_initial["current_airac"] == "08/26"
assert aviation_initial["next_airac"]["effective_from"] == "2026-09-03"
assert aviation_initial["gates"]["publication_allowed"] is False
assert aviation_pass2["provisional_aviation_decision"]["working_memory_count"] == 18
assert aviation_pass2["gates"]["lfpg_published_subset_revalidated"] is True
assert aviation_pass2["gates"]["full_scoped_ad2_18_recheck_complete"] is False
assert aviation_pass2["gates"]["publication_allowed"] is False
assert scope["research_evidence"]["provisional_working_memory_count"] == 57
assert scope["research_evidence"]["provisional_aviation_memory_count"] == 18
assert scope["publication_ready"] is False

sources = set(state["sources_of_truth"])
for required in [
    "research/ile-de-france-v0.3/radio-validation-pass2-2026-08-21.json",
    "research/ile-de-france-v0.3/aviation-validation-pass2-2026-08-21.json",
]:
    assert required in sources

bretagne = state["bretagne_v0_3_airac_handoff"]
assert bretagne["candidate_memory_count"] == 151
assert bretagne["candidate_memory_delta"] == 0
assert bretagne["airac_next_effective_from"] == "2026-09-03"

print("Sprint 101 state sync: IDF v0.3 pass 2 active, provisional 57/18, public v0.2/58 immutable, release gates open OK")
