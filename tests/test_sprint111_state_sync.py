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
assert state["current_sprint"] >= 111
assert tuple(int(part) for part in state["state_version"].split(".")) >= (0, 21, 99)
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

# Sprint 111 snapshot remains historical even when the current state advances.
s111 = state["latest_sprint111_bretagne_airac09_readiness"]
assert s111["sprint"] == 111
assert s111["state_version"] == "0.21.99"
assert s111["completed_on"] == "2026-08-22"
assert s111["status"] == "bretagne_v03_airac09_readiness_prepared_future_cycle_not_current"
assert s111["candidate_memory_count"] == 151
assert s111["candidate_memory_delta"] == 0
assert s111["airac_next_effective_from"] == "2026-09-03"
assert s111["published"] is False

readiness = json.loads(READINESS.read_text(encoding="utf-8"))
assert readiness["status"] == "future_cycle_source_available_not_current_readiness_prepared"
assert readiness["prepared_on"] == "2026-08-22"
assert readiness["public_base"]["version"] == "0.2"
assert readiness["public_base"]["memory_count"] == 151
assert readiness["candidate"]["memory_count"] == 151
assert readiness["candidate"]["memory_delta"] == 0
assert readiness["candidate"]["aviation_memory_count"] == 16
assert readiness["candidate"]["public_export_allowed"] is False
assert readiness["candidate"]["public_release_allowed"] is False
assert readiness["cycle"]["current_on_prepared_date"] == "AIRAC 08/26"
assert readiness["cycle"]["current_until_inclusive"] == "2026-09-02"
assert readiness["cycle"]["required_cycle"] == "AIRAC 09/26"
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

recent = {item["sprint"]: item for item in state["recent_sprints"]}
assert recent[111]["state_version"] == "0.21.99"
assert recent[110]["state_version"] == "0.21.98"

registry = REGISTRY.read_text(encoding="utf-8")
assert "radiopack-france-bretagne-v0.2.csv" in registry
assert "radiopack-france-bretagne-v0.3.csv" not in registry

# The current active work may legitimately be Bretagne while waiting for the
# effective date; Normandie field listening must no longer be forced after the
# Sprint 112 theory-policy change.
if state["current_sprint"] >= 113:
    active = state["active_work"]
    assert active["pack"] == "Bretagne"
    assert active["target_version"] == "0.3"
    assert active["candidate_memory_count"] == 151
    assert active["candidate_memory_delta"] == 0
    assert active["airac_next_effective_from"] == "2026-09-03"
    assert active["publication_allowed_before_airac09_revalidation"] is False

    priority = state["next_priority"]
    assert priority["field_listening_role"] == "optional_quality_feedback"
    assert priority["coverage_policy"] == "documented_theoretical_plausibility_may_close_coverage_gate"

readme = README.read_text(encoding="utf-8")
for token in [
    "## Sprint 111 — Bretagne v0.3 : readiness AIRAC 09/26",
    "16 mémoires aviation",
    "3 septembre 2026",
    "## Sprint 110 — historique Normandie v0.5 : ancien handoff terrain",
]:
    assert token in readme, token
if state["current_sprint"] >= 113:
    assert "Sprint 113 / 0.22.01" in readme
    assert "1595 mémoires RX cumulées" in readme

status = STATUS.read_text(encoding="utf-8")
assert "## Sprint 111 — Bretagne v0.3 AIRAC 09/26 prête pour revalidation" in status
if state["current_sprint"] >= 113:
    assert "Sprint courant : **113**" in status
    assert "État logique : **0.22.01**" in status
    assert "Résumé courant : `research/sprint-113-summary.md`" in status
    assert "écoutes terrain" in status and "facultatif" in status

print("Sprint 111 historical guard: Bretagne AIRAC09 readiness remains exact after Sprint 113; no early v0.3 publication and Normandie field priority may advance OK")
