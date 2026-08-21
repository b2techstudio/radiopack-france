#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
state = json.loads((ROOT / "research/project-resume-state.json").read_text(encoding="utf-8"))
readme = (ROOT / "README.md").read_text(encoding="utf-8")
project = (ROOT / "PROJECT_STATUS.md").read_text(encoding="utf-8")
changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
radio_pass3 = json.loads((ROOT / "research/ile-de-france-v0.3/radio-validation-pass3-2026-08-21.json").read_text(encoding="utf-8"))
aviation_pass3 = json.loads((ROOT / "research/ile-de-france-v0.3/aviation-validation-pass3-2026-08-21.json").read_text(encoding="utf-8"))
scope = json.loads((ROOT / "research/ile-de-france-v0.3/release-scope.json").read_text(encoding="utf-8"))

assert state["updated"] == "2026-08-21"
assert state["current_sprint"] == 101
assert state["state_version"] == "0.21.90"
assert "**État courant : Sprint 101 / 0.21.90" in readme
assert "Sprint courant : **101**" in project
assert "État logique : **0.21.90**" in project
assert "57 RX si le bloc aviation reste à 18" in project
assert changelog.startswith("# Changelog\n\n## 0.21.90 - 2026-08-21")

idf_public = state["public_packs"]["ile_de_france"]
assert idf_public["version"] == "0.2"
assert idf_public["memory_count"] == 58
assert idf_public["immutable"] is True

active = state["active_work"]
assert active["pack"] == "Île-de-France"
assert active["target_version"] == "0.3"
assert active["status"] == "research_pass3_radio_final_aviation_open_not_release_candidate"
assert active["public_base_version"] == "0.2"
assert active["public_base_memory_count"] == 58
assert active["published_base_aviation_memory_count"] == 18
assert active["provisional_working_memory_count"] == 57
assert active["provisional_aviation_memory_count"] == 18
assert active["release_candidate_memory_count"] is None
assert active["radio_source_conflicts_closed"] is True
assert active["radio_memory_accounting_final"] is True
assert active["aviation_revalidation_complete"] is False
assert active["publication_ready"] is False
assert active["radio_validation"] == "research/ile-de-france-v0.3/radio-validation-pass3-2026-08-21.json"
assert active["aviation_validation"] == "research/ile-de-france-v0.3/aviation-validation-pass3-2026-08-21.json"
assert active["release_scope"] == "research/ile-de-france-v0.3/release-scope.json"

s101 = state["latest_sprint101_idf_v03_research"]
assert s101["sprint"] == 101
assert s101["state_version"] == "0.21.90"
assert s101["status"] == "ile_de_france_v03_pass3_radio_final_aviation_open"
assert s101["provisional_working_memory_count"] == 57
assert s101["provisional_aviation_memory_count"] == 18
assert s101["radio_source_conflicts_closed"] is True
assert s101["radio_memory_accounting_final"] is True
assert s101["aviation_revalidation_complete"] is False
assert s101["publication_ready"] is False
assert s101["public_csv_mutation"] is False
assert s101["rf_publication_mutation"] is False

assert radio_pass3["result"]["radio_source_conflicts_closed_for_current_release_scope"] is True
assert radio_pass3["result"]["radio_memory_accounting_final"] is True
assert radio_pass3["result"]["working_memory_count_if_aviation_unchanged"] == 57
assert radio_pass3["result"]["publication_ready"] is False
assert aviation_pass3["provisional_aviation_decision"]["working_memory_count"] == 18
assert aviation_pass3["gates"]["full_current_airac_scoped_revalidation_complete"] is False
assert aviation_pass3["gates"]["publication_allowed"] is False
assert scope["publication_gates"]["radio_source_conflicts_closed"] is True
assert scope["publication_gates"]["radio_memory_accounting_final"] is True
assert scope["publication_gates"]["aviation_revalidation_complete"] is False
assert scope["publication_ready"] is False

sources = set(state["sources_of_truth"])
for required in [
    "research/ile-de-france-v0.3/radio-validation-pass3-2026-08-21.json",
    "research/ile-de-france-v0.3/aviation-validation-pass3-2026-08-21.json",
]:
    assert required in sources

bretagne = state["bretagne_v0_3_airac_handoff"]
assert bretagne["candidate_memory_count"] == 151
assert bretagne["candidate_memory_delta"] == 0
assert bretagne["airac_next_effective_from"] == "2026-09-03"

print("Sprint 101 state sync: IDF v0.3 pass 3 radio final at 57, aviation 18 still gated, public v0.2/58 immutable OK")
