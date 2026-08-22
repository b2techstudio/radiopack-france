#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "research/project-resume-state.json"
REFRESH = ROOT / "research/normandie-v0.5/sprint110-source-field-refresh.json"
KIT = ROOT / "research/normandie-v0.5/field-validation-kit.json"
POLICY = ROOT / "research/normandie-v0.5/field-evaluation-policy.json"
EVALUATOR = ROOT / "tools/evaluate_normandie_v05_field_sessions.py"
README = ROOT / "README.md"
STATUS = ROOT / "PROJECT_STATUS.md"
ARA_RECORD = ROOT / "research/auvergne-rhone-alpes-v0.3/publication-record.json"

for path in [STATE, REFRESH, KIT, POLICY, EVALUATOR, README, STATUS, ARA_RECORD]:
    assert path.is_file(), path

state = json.loads(STATE.read_text(encoding="utf-8"))
assert state["current_sprint"] == 110
assert state["state_version"] == "0.21.98"
assert state["updated"] == "2026-08-22"

normandie_public = state["public_packs"]["normandie"]
assert normandie_public["version"] == "0.4"
assert normandie_public["memory_count"] == 142
assert normandie_public["immutable"] is True

active = state["active_work"]
assert active["pack"] == "Normandie"
assert active["target_version"] == "0.5"
assert active["status"] == "current_sources_refreshed_zero_delta_field_blocked"
assert active["public_base_version"] == "0.4"
assert active["public_base_memory_count"] == 142
assert active["candidate_memory_count"] == 142
assert active["candidate_memory_delta"] == 0
assert active["known_potential_ceiling_excluding_f6zes"] == 147
assert active["field_required"] == ["R3_F1ZBX", "F5ZHA"]
assert active["source_watch"] == ["F1ZOV", "F6ZES"]
assert active["r3_minimum_independent_sessions"] == 2
assert active["f5zha_minimum_independent_sessions"] == 2
assert active["field_gate_can_be_evaluated_automatically"] is True
assert active["automatic_candidate_mutation_allowed"] is False
assert active["automatic_publication_allowed"] is False
assert active["public_export_allowed"] is False
assert active["public_release_ready"] is False
assert active["published"] is False
assert active["public_mutation_performed"] is False
assert active["rf_data_mutation"] is False
assert active["published_v0_4_immutable"] is True

priority = state["next_priority"]
assert priority["pack"] == "Normandie"
assert priority["target_version"] == "0.5"
assert priority["status"] == "collect_real_mortain_bocage_field_sessions"
assert priority["candidate_memory_count"] == 142
assert priority["candidate_memory_delta"] == 0
assert priority["field_required"] == ["R3_F1ZBX", "F5ZHA"]
assert priority["required_independent_sessions_per_target"] == 2
assert priority["source_watch"] == ["F1ZOV", "F6ZES"]
assert priority["field_evaluator"] == "tools/evaluate_normandie_v05_field_sessions.py"

s110 = state["latest_sprint110_normandie_v05_refresh"]
assert s110["sprint"] == 110
assert s110["state_version"] == "0.21.98"
assert s110["status"] == "normandie_v05_sources_refreshed_zero_delta_field_handoff"
assert s110["public_base_memory_count"] == 142
assert s110["candidate_memory_count"] == 142
assert s110["candidate_memory_delta"] == 0
assert s110["known_potential_ceiling_excluding_f6zes"] == 147
assert s110["r3_public_pair_mhz"] == [145.675, 145.075]
assert s110["f5zha_public_pair_mhz"] == [145.4675, 432.575]
assert s110["f1zov_operator_status"] == "maintenance"
assert s110["f6zes_frequency_resolved"] is False
assert s110["f6zes_mode_resolved"] is False
assert s110["promotion_count"] == 0
assert s110["public_csv_mutation"] is False
assert s110["rf_data_mutation"] is False
assert s110["public_v0_4_immutable"] is True

refresh = json.loads(REFRESH.read_text(encoding="utf-8"))
assert refresh["pack"] == "Normandie"
assert refresh["target_version"] == "0.5"
assert refresh["candidate_memory_count_before"] == 142
assert refresh["candidate_memory_count_after"] == 142
assert refresh["candidate_memory_delta"] == 0
assert refresh["promotion_count"] == 0
assert refresh["public_v0_4_immutable"] is True
assert refresh["public_v0_5_created"] is False
assert refresh["rules"]["public_mutation_performed"] is False
assert refresh["rules"]["no_frequency_inference"] is True

kit = json.loads(KIT.read_text(encoding="utf-8"))
assert kit["gates"]["R3_MORTAIN_RX"]["minimum_independent_sessions"] == 2
assert kit["gates"]["F5ZHA_SOURCE_AND_COVERAGE"]["minimum_independent_sessions"] == 2
assert kit["rules"]["public_export_allowed"] is False

policy = json.loads(POLICY.read_text(encoding="utf-8"))
assert policy["output_rules"]["field_gate_can_be_evaluated_automatically"] is True
assert policy["output_rules"]["automatic_candidate_mutation_allowed"] is False
assert policy["output_rules"]["automatic_publication_allowed"] is False
assert policy["output_rules"]["human_source_review_still_required_after_satisfied_field_gate"] is True

ara = state["public_packs"]["auvergne_rhone_alpes"]
assert ara["version"] == "0.3"
assert ara["memory_count"] == 71
assert ara["immutable"] is True
assert ara["public_csv_sha256"] == "b44a95486af5fd89fa72246ed7c8f0ab79e3084f6b0429df5215fba9918d691e"
ara_record = json.loads(ARA_RECORD.read_text(encoding="utf-8"))
assert ara_record["published_version_is_immutable"] is True
assert ara_record["memory_count"] == 71

recent = {item["sprint"]: item for item in state["recent_sprints"]}
assert recent[110]["state_version"] == "0.21.98"
assert recent[109]["state_version"] == "0.21.97"

for source in [
    "research/normandie-v0.5/sprint110-source-field-refresh.json",
    "research/normandie-v0.5/field-validation-kit.json",
    "research/normandie-v0.5/field-evaluation-policy.json",
    "tools/evaluate_normandie_v05_field_sessions.py",
    "tests/test_sprint110_normandie_v05_refresh.py",
    "research/sprint-110-summary.md",
]:
    assert source in state["sources_of_truth"], source

readme = README.read_text(encoding="utf-8")
for token in [
    "Sprint 110 / 0.21.98",
    "## Sprint 110 — Normandie v0.5 : sources revalidées, handoff terrain",
    "142 RX / delta 0",
    "R3/F1ZBX",
    "F5ZHA",
    "1591 mémoires RX cumulées",
]:
    assert token in readme, token

status = STATUS.read_text(encoding="utf-8")
for token in [
    "Sprint courant : **110**",
    "État logique : **0.21.98**",
    "Résumé courant : `research/sprint-110-summary.md`",
    "## Sprint 110 — Normandie v0.5 revalidée, zéro delta",
    "collecte de vraies sessions terrain",
]:
    assert token in status, token

print("Sprint 110 state sync: Normandie v0.5=142 RX delta 0, field gates preserved, no public mutation, ARA v0.3 immutable OK")
