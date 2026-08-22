#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "research/project-resume-state.json"
READINESS = ROOT / "research/bretagne-v0.3/airac09-readiness.json"
TEMPLATE = ROOT / "research/bretagne-v0.3/airac09-revalidation-template.json"
PUBLIC_RECORD = ROOT / "research/bretagne-v0.2/publication-record.json"
PUBLIC_V02 = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"
PUBLIC_V03 = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.3.csv"
README = ROOT / "README.md"
STATUS = ROOT / "PROJECT_STATUS.md"
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"

for path in [STATE, READINESS, TEMPLATE, PUBLIC_RECORD, PUBLIC_V02, README, STATUS, REGISTRY]:
    assert path.is_file(), path

state = json.loads(STATE.read_text(encoding="utf-8"))
assert state["current_sprint"] == 111
assert state["state_version"] == "0.21.99"
assert state["updated"] == "2026-08-22"

bretagne = state["public_packs"]["bretagne"]
assert bretagne["version"] == "0.2"
assert bretagne["memory_count"] == 151
assert bretagne["immutable"] is True

public_record = json.loads(PUBLIC_RECORD.read_text(encoding="utf-8"))
assert public_record["status"] == "published_immutable"
assert public_record["version"] == "0.2"
assert public_record["memory_count"] == 151
assert public_record["public_csv_sha256"] == "73aa3d530ae9f6c572eb01794b0861ecba61df0faf7884ee766085d3de7601a4"
assert public_record["published_version_is_immutable"] is True
assert public_record["aviation"]["memory_count"] == 16
assert public_record["aviation"]["cycle"] == "AIRAC 08/26"
assert public_record["aviation"]["valid_through_inclusive"] == "2026-09-02"
assert not PUBLIC_V03.exists()

active = state["active_work"]
assert active["pack"] == "Normandie"
assert active["target_version"] == "0.5"
assert active["status"] == "current_sources_refreshed_zero_delta_field_blocked"
assert active["candidate_memory_count"] == 142
assert active["candidate_memory_delta"] == 0
assert active["field_required"] == ["R3_F1ZBX", "F5ZHA"]
assert active["automatic_candidate_mutation_allowed"] is False
assert active["automatic_publication_allowed"] is False
assert active["published"] is False

priority = state["next_priority"]
assert priority["pack"] == "Normandie"
assert priority["target_version"] == "0.5"
assert priority["status"] == "collect_real_mortain_bocage_field_sessions"
assert priority["field_required"] == ["R3_F1ZBX", "F5ZHA"]

handoff = state["bretagne_v0_3_airac_handoff"]
assert handoff["status"] == "airac09_future_source_available_readiness_prepared_waiting_effective_date"
assert handoff["public_base_version"] == "0.2"
assert handoff["public_base_memory_count"] == 151
assert handoff["candidate_memory_count"] == 151
assert handoff["candidate_memory_delta"] == 0
assert handoff["airac_current"] == "08/26"
assert handoff["airac_current_until_inclusive"] == "2026-09-02"
assert handoff["airac_next_required"] == "09/26"
assert handoff["airac_next_effective_from"] == "2026-09-03"
assert handoff["airac_next_effective_until_inclusive"] == "2026-09-30"
assert handoff["future_cycle_source_available"] is True
assert handoff["future_cycle_source_observed_on"] == "2026-08-22"
assert handoff["future_cycle_source_is_current_evidence"] is False
assert handoff["baseline_aviation_memory_count"] == 16
assert handoff["required_explicit_memory_decision_count"] == 16
assert handoff["candidate_rebuild_allowed_before_effective_date"] is False
assert handoff["automatic_candidate_mutation_allowed"] is False
assert handoff["automatic_publication_allowed"] is False
assert handoff["publication_allowed_before_airac09_revalidation"] is False
assert handoff["readiness"] == "research/bretagne-v0.3/airac09-readiness.json"
assert handoff["revalidation_template"] == "research/bretagne-v0.3/airac09-revalidation-template.json"
assert handoff["validator"] == "tools/check_bretagne_v03_airac09_revalidation.py"

s111 = state["latest_sprint111_bretagne_airac09_readiness"]
assert s111["sprint"] == 111
assert s111["state_version"] == "0.21.99"
assert s111["completed_on"] == "2026-08-22"
assert s111["status"] == "bretagne_v03_airac09_readiness_prepared_future_cycle_not_current"
assert s111["public_base_version"] == "0.2"
assert s111["public_base_memory_count"] == 151
assert s111["candidate_memory_count"] == 151
assert s111["candidate_memory_delta"] == 0
assert s111["baseline_aviation_cycle"] == "AIRAC 08/26"
assert s111["baseline_aviation_memory_count"] == 16
assert s111["baseline_locations"] == [130, 145]
assert s111["required_cycle"] == "AIRAC 09/26"
assert s111["future_sia_product_available"] is True
assert s111["future_sia_product_is_current_evidence"] is False
assert s111["effective_from"] == "2026-09-03"
assert s111["effective_until_inclusive"] == "2026-09-30"
assert s111["explicit_memory_decision_count_required"] == 16
assert s111["candidate_rebuild_allowed_before_effective_date"] is False
assert s111["automatic_candidate_mutation_allowed"] is False
assert s111["automatic_publication_allowed"] is False
assert s111["public_csv_mutation"] is False
assert s111["rf_data_mutation"] is False
assert s111["public_v0_3_created"] is False

readiness = json.loads(READINESS.read_text(encoding="utf-8"))
assert readiness["status"] == "future_cycle_source_available_not_current_readiness_prepared"
assert readiness["prepared_on"] == "2026-08-22"
assert readiness["candidate"]["memory_count"] == 151
assert readiness["candidate"]["memory_delta"] == 0
assert readiness["candidate"]["aviation_memory_count"] == 16
assert readiness["candidate"]["public_export_allowed"] is False
assert readiness["candidate"]["public_release_allowed"] is False
assert readiness["cycle"]["effective_from"] == "2026-09-03"
assert readiness["cycle"]["effective_until_inclusive"] == "2026-09-30"
assert readiness["rules"]["future_airac_source_availability_is_not_current_evidence"] is True
assert readiness["rules"]["future_airac_must_not_be_promoted_before_effective_date"] is True
assert readiness["rules"]["public_v0_3_created"] is False

template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
assert template["status"] == "not_executed_future_cycle"
assert template["cycle"] == "AIRAC 09/26"
assert len(template["memories"]) == 16
assert [item["location"] for item in template["memories"]] == list(range(130, 146))
assert all(item["decision"] is None for item in template["memories"])
assert template["current_cycle_primary_source_verified"] is False
assert template["human_review"]["completed"] is False
assert template["rules"]["automatic_candidate_mutation_allowed"] is False
assert template["rules"]["automatic_publication_allowed"] is False

recent = state["recent_sprints"]
assert recent[0]["sprint"] == 111 and recent[0]["state_version"] == "0.21.99"
assert recent[1]["sprint"] == 110 and recent[1]["state_version"] == "0.21.98"

for source in [
    "research/bretagne-v0.3/airac09-readiness.json",
    "research/bretagne-v0.3/airac09-revalidation-template.json",
    "tools/check_bretagne_v03_airac09_revalidation.py",
    "tests/test_sprint111_bretagne_airac09_readiness.py",
    ".github/workflows/sprint111-bretagne-airac09-readiness.yml",
    "research/sprint-111-summary.md",
]:
    assert source in state["sources_of_truth"], source

assert state["resume_rules"]["future_airac_source_availability_is_not_current_evidence"] is True
assert state["resume_rules"]["candidate_rebuild_after_airac_revalidation_is_not_publication"] is True
assert state["resume_rules"]["airac_revalidation_requires_explicit_decision_for_every_scoped_aviation_memory"] is True

registry = REGISTRY.read_text(encoding="utf-8")
assert "radiopack-france-bretagne-v0.2.csv" in registry
assert "radiopack-france-bretagne-v0.3.csv" not in registry

readme = README.read_text(encoding="utf-8")
for token in [
    "Sprint 111 / 0.21.99",
    "## Sprint 111 — Bretagne v0.3 : readiness AIRAC 09/26",
    "16 mémoires aviation",
    "3 septembre 2026",
    "## Sprint 110 — Normandie v0.5 : sources revalidées, handoff terrain",
    "1591 mémoires RX cumulées",
]:
    assert token in readme, token

status = STATUS.read_text(encoding="utf-8")
for token in [
    "Sprint courant : **111**",
    "État logique : **0.21.99**",
    "Résumé courant : `research/sprint-111-summary.md`",
    "## Sprint 111 — Bretagne v0.3 AIRAC 09/26 prête pour revalidation",
    "La priorité immédiatement actionnable reste **Normandie v0.5 terrain**",
]:
    assert token in status, token

print("Sprint 111 state sync: Bretagne AIRAC 09/26 readiness canonical, public v0.2 immutable, Normandie field priority preserved, no RF/public mutation OK")
