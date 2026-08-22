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
NORMANDIE_V05_RECORD = ROOT / "research/normandie-v0.5/publication-record.json"

for path in [STATE, REFRESH, KIT, POLICY, EVALUATOR, README, STATUS, ARA_RECORD, NORMANDIE_V05_RECORD]:
    assert path.is_file(), path

state = json.loads(STATE.read_text(encoding="utf-8"))
assert state["current_sprint"] >= 110
assert state["updated"] == "2026-08-22"
if state["current_sprint"] == 110:
    assert state["state_version"] == "0.21.98"
else:
    assert tuple(int(part) for part in state["state_version"].split(".")) >= (0, 21, 98)

# Sprint 110 remains an immutable historical checkpoint: at that time Normandie
# v0.5 was 142 RX / delta 0 and field sessions were still the coverage handoff.
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
# This flag describes Sprint 110 itself and remains historically false even
# though v0.5 was published later at Sprint 113.
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

# Current state may have advanced. From Sprint 113 onward Normandie v0.5 is
# legitimately public using the separate theory policy introduced at Sprint 112.
normandie_public = state["public_packs"]["normandie"]
assert normandie_public["immutable"] is True
if state["current_sprint"] < 113:
    assert normandie_public["version"] == "0.4"
    assert normandie_public["memory_count"] == 142
else:
    assert normandie_public["version"] == "0.5"
    assert normandie_public["memory_count"] == 146
    assert normandie_public["previous_immutable_version"] == "0.4"
    assert normandie_public["previous_memory_count"] == 142
    assert normandie_public["public_csv_sha256"] == "1d7ce66c7a5faafe98e4ee59791bcd29af1fd1f432ee1bfc1cad7cba3bc5cf59"
    assert normandie_public["coverage_basis"] == "theoretical_documented"
    assert normandie_public["measured_reception_claimed"] is False

    publication = state["normandie_v0_5_publication"]
    assert publication["status"] == "published_immutable_theoretical_coverage"
    assert publication["memory_count"] == 146
    assert publication["memory_delta"] == 4
    assert publication["theoretical_coverage_memory_count"] == 4
    assert publication["field_reception_verified"] is False
    assert publication["field_reception_required_for_publication"] is False
    assert publication["field_sessions_are_optional_quality_feedback"] is True

    record = json.loads(NORMANDIE_V05_RECORD.read_text(encoding="utf-8"))
    assert record["status"] == "published_immutable"
    assert record["publication_sprint"] == 113
    assert record["memory_count"] == 146
    assert record["theoretical_coverage"]["field_reception_required_for_publication"] is False
    assert record["rules"]["field_sessions_are_optional_quality_feedback"] is True

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
assert "## Sprint 110 — historique Normandie v0.5 : ancien handoff terrain" in readme
assert "142 RX / delta 0" in readme
assert "explicitement remplacée au Sprint 112" in readme
if state["current_sprint"] >= 113:
    for token in [
        "État courant : Sprint 113 / 0.22.01",
        "**Normandie v0.5** — 146 mémoires RX",
        "1595 mémoires RX cumulées",
        "contrôle qualité facultatif",
    ]:
        assert token in readme, token

status = STATUS.read_text(encoding="utf-8")
assert "## Sprint 110 — historique Normandie v0.5, ancien handoff terrain" in status
assert "supplanté par la politique théorique du Sprint 112" in status
if state["current_sprint"] >= 113:
    assert "Sprint courant : **113**" in status
    assert "État logique : **0.22.01**" in status
    assert "écoutes terrain deviennent du contrôle qualité facultatif" in status

print("Sprint 110 historical guard: 142/delta0 field handoff remains auditable while later theory-based Normandie v0.5 publication is allowed OK")
