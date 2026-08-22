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
record = json.loads((ROOT / "research/ile-de-france-v0.3/publication-record.json").read_text(encoding="utf-8"))
checklist = json.loads((ROOT / "research/ile-de-france-v0.3/review-checklist.json").read_text(encoding="utf-8"))
gates_file = json.loads((ROOT / "research/ile-de-france-v0.3/publication-gates.json").read_text(encoding="utf-8"))
public_csv = ROOT / "website/public/downloads/ile-de-france/radiopack-france-ile-de-france-v0.3.csv"

EXPECTED_SHA = "e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125"

assert state["updated"] == "2026-08-22"
assert state["current_sprint"] == 101
assert state["state_version"] == "0.21.90"
assert "**État courant : Sprint 101 / 0.21.90" in readme
assert "Île-de-France v0.3" in readme
assert "57 RX" in readme
assert "Sprint courant : **101**" in project
assert "État logique : **0.21.90**" in project
assert "Île-de-France v0.3 : **57 mémoires RX**" in project
assert changelog.startswith("# Changelog\n\n## 0.21.90 - 2026-08-22")

idf_public = state["public_packs"]["ile_de_france"]
assert idf_public["version"] == "0.3"
assert idf_public["memory_count"] == 57
assert idf_public["immutable"] is True
assert idf_public["previous_immutable_version"] == "0.2"
assert idf_public["previous_memory_count"] == 58
assert idf_public["publication_record"] == "research/ile-de-france-v0.3/publication-record.json"
assert idf_public["public_csv_sha256"] == EXPECTED_SHA

active = state["active_work"]
assert active["pack"] == "Île-de-France"
assert active["target_version"] == "0.3"
assert active["status"] == "published_immutable"
assert active["public_base_version"] == "0.2"
assert active["public_base_memory_count"] == 58
assert active["candidate_memory_count"] == 57
assert active["candidate_aviation_memory_count"] == 18
assert active["candidate_regional_radio_memory_count"] == 15
assert active["release_candidate_memory_count"] == 57
assert active["candidate_sha256"] == EXPECTED_SHA
assert active["public_csv_sha256"] == EXPECTED_SHA
assert active["radio_source_conflicts_closed"] is True
assert active["radio_memory_accounting_final"] is True
assert active["aviation_revalidation_complete"] is True
assert active["deterministic_candidate_built"] is True
assert active["review_checklist_complete"] is True
assert active["publication_gates_zero_blockers"] is True
assert active["publication_record_frozen"] is True
assert active["publication_ready"] is True
assert active["published"] is True
assert active["published_version_is_immutable"] is True
assert active["public_mutation_performed"] is True
assert active["public_csv"] == "website/public/downloads/ile-de-france/radiopack-france-ile-de-france-v0.3.csv"
assert active["airac08_publication_allowed_through_inclusive"] == "2026-09-02"
assert active["airac09_revalidation_required_on_or_after"] == "2026-09-03"

s101 = state["latest_sprint101_idf_v03_research"]
assert s101["sprint"] == 101
assert s101["state_version"] == "0.21.90"
assert s101["status"] == "ile_de_france_v03_published_immutable"
assert s101["completed_on"] == "2026-08-22"
assert s101["candidate_memory_count"] == 57
assert s101["candidate_aviation_memory_count"] == 18
assert s101["candidate_regional_radio_memory_count"] == 15
assert s101["candidate_sha256"] == EXPECTED_SHA
assert s101["public_csv_sha256"] == EXPECTED_SHA
assert s101["publication_record_frozen"] is True
assert s101["publication_ready"] is True
assert s101["published"] is True
assert s101["published_version_is_immutable"] is True
assert s101["public_mutation_performed"] is True
assert s101["public_csv_mutation"] is True
assert s101["rf_publication_mutation"] is True

assert radio_pass3["result"]["radio_memory_accounting_final"] is True
assert radio_pass3["result"]["working_memory_count_if_aviation_unchanged"] == 57
assert aviation_pass4["final_aviation_decision"]["memory_count"] == 18
assert aviation_pass4["gates"]["aviation_revalidation_complete"] is True
assert aviation_pass4["gates"]["publication_allowed_before_airac09_boundary"] is True

for key in [
    "radio_source_conflicts_closed", "radio_memory_accounting_final", "aviation_revalidation_complete",
    "deterministic_candidate_built", "rx_only_validation_passed", "rf_deduplication_passed", "memory_limit_passed",
    "review_checklist_complete", "publication_gates_zero_blockers", "publication_record_frozen",
    "public_csv_matches_candidate", "public_registry_updated",
]:
    assert scope["publication_gates"][key] is True
assert scope["status"] == "published_immutable"
assert scope["publication_ready"] is True
assert scope["published"] is True
assert scope["public_mutation_performed"] is True
assert scope["published_version_is_immutable"] is True
assert scope["research_evidence"]["candidate_memory_count"] == 57
assert scope["research_evidence"]["candidate_sha256"] == EXPECTED_SHA
assert scope["research_evidence"]["public_csv_sha256"] == EXPECTED_SHA

assert manifest["candidate_memory_count"] == 57
assert manifest["candidate_sha256"] == EXPECTED_SHA
assert manifest["public_csv_sha256"] == EXPECTED_SHA
assert manifest["public_export_allowed"] is True
assert manifest["published"] is True
assert checklist["reviewed_count"] == checklist["item_count"] == 12
assert checklist["published"] is True
assert gates_file["blocker_count"] == 0
assert all(item["pass"] for item in gates_file["checks"])
assert gates_file["published"] is True
assert record["status"] == "published_immutable"
assert record["memory_count"] == 57
assert record["candidate_csv_sha256"] == EXPECTED_SHA
assert record["public_csv_sha256"] == EXPECTED_SHA
assert record["published"] is True
assert record["public_csv_created"] is True
assert record["public_registry_updated"] is True
assert record["published_version_is_immutable"] is True
assert public_csv.is_file()

sources = set(state["sources_of_truth"])
for required in [
    "research/ile-de-france-v0.3/aviation-validation-pass4-2026-08-21.json",
    "research/ile-de-france-v0.3/generated/release-candidate/candidate-manifest.json",
    "research/ile-de-france-v0.3/review-checklist.json",
    "research/ile-de-france-v0.3/publication-gates.json",
    "research/ile-de-france-v0.3/publication-record.json",
    "website/public/downloads/ile-de-france/radiopack-france-ile-de-france-v0.3.csv",
    "tools/build_idf_v03_candidate.py",
    "tests/test_idf_v03_candidate.py",
    "tests/test_idf_v03_publication.py",
]:
    assert required in sources

assert state["recent_sprints"][0]["sprint"] == 101
assert "published immutable at 57 RX / 18 aviation" in state["recent_sprints"][0]["summary"]

bretagne = state["bretagne_v0_3_airac_handoff"]
assert bretagne["candidate_memory_count"] == 151
assert bretagne["airac_next_effective_from"] == "2026-09-03"

print("Sprint 101 state sync: IDF v0.3 published immutable 57/18/15, exact public SHA, historical v0.2/58 retained OK")
