#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
state = json.loads((ROOT / "research/project-resume-state.json").read_text(encoding="utf-8"))
readme = (ROOT / "README.md").read_text(encoding="utf-8")
project = (ROOT / "PROJECT_STATUS.md").read_text(encoding="utf-8")
changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
radio_pass3 = json.loads((ROOT / "research/ile-de-france-v0.3/radio-validation-pass3-2026-08-21.json").read_text(encoding="utf-8"))
aviation_pass4 = json.loads((ROOT / "research/ile-de-france-v0.3/aviation-validation-pass4-2026-08-21.json").read_text(encoding="utf-8"))
scope = json.loads((ROOT / "research/ile-de-france-v0.3/release-scope.json").read_text(encoding="utf-8"))
manifest = json.loads((ROOT / "research/ile-de-france-v0.3/generated/release-candidate/candidate-manifest.json").read_text(encoding="utf-8"))

assert state["updated"] == "2026-08-21"
assert state["current_sprint"] == 101
assert state["state_version"] == "0.21.90"
assert "**État courant : Sprint 101 / 0.21.90" in readme
assert "Sprint courant : **101**" in project
assert "État logique : **0.21.90**" in project
assert "candidat déterministe **57 RX**" in project
assert changelog.startswith("# Changelog\n\n## 0.21.90 - 2026-08-21")

idf_public = state["public_packs"]["ile_de_france"]
assert idf_public["version"] == "0.2"
assert idf_public["memory_count"] == 58
assert idf_public["immutable"] is True

active = state["active_work"]
assert active["pack"] == "Île-de-France"
assert active["target_version"] == "0.3"
assert active["status"] == "release_candidate_built_prepublication_open"
assert active["public_base_version"] == "0.2"
assert active["public_base_memory_count"] == 58
assert active["published_base_aviation_memory_count"] == 18
assert active["candidate_memory_count"] == 57
assert active["candidate_aviation_memory_count"] == 18
assert active["candidate_regional_radio_memory_count"] == 15
assert active["release_candidate_memory_count"] == 57
assert active["candidate_sha256"] == "e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125"
assert active["radio_source_conflicts_closed"] is True
assert active["radio_memory_accounting_final"] is True
assert active["aviation_revalidation_complete"] is True
assert active["deterministic_candidate_built"] is True
assert active["publication_record_frozen"] is False
assert active["publication_ready"] is False
assert active["radio_validation"] == "research/ile-de-france-v0.3/radio-validation-pass3-2026-08-21.json"
assert active["aviation_validation"] == "research/ile-de-france-v0.3/aviation-validation-pass4-2026-08-21.json"
assert active["candidate_manifest"] == "research/ile-de-france-v0.3/generated/release-candidate/candidate-manifest.json"
assert active["candidate_csv"] == "research/ile-de-france-v0.3/generated/release-candidate/radiopack-france-ile-de-france-v0.3-candidate.csv"
assert active["builder"] == "tools/build_idf_v03_candidate.py"
assert active["airac08_publication_allowed_through_inclusive"] == "2026-09-02"
assert active["airac09_revalidation_required_on_or_after"] == "2026-09-03"

s101 = state["latest_sprint101_idf_v03_research"]
assert s101["sprint"] == 101
assert s101["state_version"] == "0.21.90"
assert s101["status"] == "ile_de_france_v03_release_candidate_built_prepublication_open"
assert s101["candidate_memory_count"] == 57
assert s101["candidate_aviation_memory_count"] == 18
assert s101["candidate_regional_radio_memory_count"] == 15
assert s101["candidate_sha256"] == active["candidate_sha256"]
assert s101["radio_source_conflicts_closed"] is True
assert s101["radio_memory_accounting_final"] is True
assert s101["aviation_revalidation_complete"] is True
assert s101["deterministic_candidate_built"] is True
assert s101["publication_record_frozen"] is False
assert s101["publication_ready"] is False
assert s101["public_csv_mutation"] is False
assert s101["rf_publication_mutation"] is False

assert radio_pass3["result"]["radio_source_conflicts_closed_for_current_release_scope"] is True
assert radio_pass3["result"]["radio_memory_accounting_final"] is True
assert radio_pass3["result"]["working_memory_count_if_aviation_unchanged"] == 57
assert aviation_pass4["final_aviation_decision"]["memory_count"] == 18
assert aviation_pass4["gates"]["aviation_revalidation_complete"] is True
assert aviation_pass4["gates"]["frequency_delta_validated"] is True
assert aviation_pass4["gates"]["publication_allowed_before_airac09_boundary"] is True

for key in [
    "radio_source_conflicts_closed", "radio_memory_accounting_final", "aviation_revalidation_complete",
    "deterministic_candidate_built", "rx_only_validation_passed", "rf_deduplication_passed", "memory_limit_passed",
]:
    assert scope["publication_gates"][key] is True
assert scope["publication_gates"]["publication_record_frozen"] is False
assert scope["publication_ready"] is False
assert scope["research_evidence"]["candidate_memory_count"] == 57
assert scope["research_evidence"]["candidate_sha256"] == active["candidate_sha256"]
assert manifest["candidate_memory_count"] == 57
assert manifest["candidate_aviation_memory_count"] == 18
assert manifest["candidate_regional_radio_memory_count"] == 15
assert manifest["candidate_sha256"] == active["candidate_sha256"]
assert manifest["public_export_allowed"] is False

sources = set(state["sources_of_truth"])
for required in [
    "research/ile-de-france-v0.3/radio-validation-pass3-2026-08-21.json",
    "research/ile-de-france-v0.3/aviation-validation-pass4-2026-08-21.json",
    "research/ile-de-france-v0.3/generated/release-candidate/candidate-manifest.json",
    "research/ile-de-france-v0.3/generated/release-candidate/radiopack-france-ile-de-france-v0.3-candidate.csv",
    "tools/build_idf_v03_candidate.py",
    "tests/test_idf_v03_candidate.py",
]:
    assert required in sources

assert state["recent_sprints"][0]["sprint"] == 101
assert "release candidate built deterministically at 57 RX" in state["recent_sprints"][0]["summary"]

bretagne = state["bretagne_v0_3_airac_handoff"]
assert bretagne["candidate_memory_count"] == 151
assert bretagne["candidate_memory_delta"] == 0
assert bretagne["airac_next_effective_from"] == "2026-09-03"

print("Sprint 101 state sync: IDF v0.3 candidate 57/18 built, AIRAC08 aviation gate closed, prepublication open, public v0.2/58 immutable OK")
