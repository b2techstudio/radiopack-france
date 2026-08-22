#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFRESH = ROOT / "research/normandie-v0.5/sprint110-source-field-refresh.json"
KIT = ROOT / "research/normandie-v0.5/field-validation-kit.json"
POLICY = ROOT / "research/normandie-v0.5/field-evaluation-policy.json"
BACKLOG = ROOT / "research/normandie-v0.5/backlog.json"
LOCAL_README = ROOT / "research/normandie-v0.5/README.md"
STATE = ROOT / "research/project-resume-state.json"
PUBLIC_V04 = ROOT / "research/normandie-v0.4/publication-record.json"

for path in [REFRESH, KIT, POLICY, BACKLOG, LOCAL_README, STATE, PUBLIC_V04]:
    assert path.is_file(), path

# Sprint 110 evidence remains immutable historical evidence even if later policy changes
# legitimately move the current v0.5 candidate beyond the former field-gated state.
refresh = json.loads(REFRESH.read_text(encoding="utf-8"))
assert refresh["status"] == "current_sources_revalidated_zero_delta_field_handoff_confirmed"
assert refresh["pack"] == "Normandie"
assert refresh["target_version"] == "0.5"
assert refresh["sprint"] == 110
assert refresh["checked_on"] == "2026-08-22"
assert refresh["candidate_memory_count_before"] == 142
assert refresh["candidate_memory_count_after"] == 142
assert refresh["candidate_memory_delta"] == 0
assert refresh["promotion_count"] == 0
assert refresh["known_potential_ceiling_excluding_f6zes"] == 147
assert refresh["public_v0_4_immutable"] is True
assert refresh["public_v0_5_created"] is False

by_id = {item["id"]: item for item in refresh["dossiers"]}
assert set(by_id) == {"R3_F1ZBX", "F5ZHA", "F1ZOV", "F6ZES"}

r3 = by_id["R3_F1ZBX"]
assert r3["source"] == "https://ara35.fr/frequences/relais-phonie/r3/"
assert r3["source_findings"]["callsign"] == "F1ZBX"
assert r3["source_findings"]["output_mhz"] == 145.675
assert r3["source_findings"]["input_mhz"] == 145.075
assert r3["field_gate_status"] == "still_required"
assert r3["web_research_can_close"] is False
assert "two independent" in r3["required_next_evidence"]

zha = by_id["F5ZHA"]
assert zha["source_findings"]["state"] == "Actif"
assert zha["source_findings"]["pair_mhz"] == [145.4675, 432.575]
assert zha["field_gate_status"] == "still_required"
assert zha["web_research_can_close"] is False
assert ">=3/5" in zha["required_next_evidence"]

zov = by_id["F1ZOV"]
assert zov["source"] == "https://f6kfw.fr/"
assert zov["source_findings"]["operator_status"] == "En Maintenance"
assert zov["source_findings"]["rx_mhz"] == 430.375
assert zov["source_findings"]["tx_mhz"] == 431.975
assert "no promotion" in zov["decision"]
assert zov["source_priority"] == "current local operator status overrides general directory"

zes = by_id["F6ZES"]
assert zes["source_findings"]["site"] == "Sourdeval"
assert zes["source_findings"]["responsible"] == "F1SMB"
assert zes["source_findings"]["locator"] == "IN98MR93XV"
assert zes["source_findings"]["frequency_mhz"] is None
assert zes["source_findings"]["mode"] is None
assert zes["no_frequency_inference"] is True
assert "exclude from candidate" in zes["decision"]

kit = json.loads(KIT.read_text(encoding="utf-8"))
assert kit["status"] == "field_validation_kit_not_public"
assert kit["candidate_memory_count_before"] == 142
assert kit["candidate_memory_count_after"] == 142
assert kit["candidate_memory_delta"] == 0
assert kit["public_export_allowed"] is False
assert kit["gates"]["R3_MORTAIN_RX"]["minimum_independent_sessions"] == 2
assert kit["gates"]["R3_MORTAIN_RX"]["primary_probe_mhz"] == 145.675
assert kit["gates"]["F5ZHA_SOURCE_AND_COVERAGE"]["minimum_independent_sessions"] == 2
assert kit["gates"]["F5ZHA_SOURCE_AND_COVERAGE"]["current_pair_mhz"] == [145.4675, 432.575]
assert kit["gates"]["F5ZHA_SOURCE_AND_COVERAGE"]["minimum_intelligibility_0_to_5"] == 3
assert kit["rules"]["web_research_cannot_satisfy_field_gate"] is True
assert kit["rules"]["must_not_be_appended_to_internal_candidate_automatically"] is True
assert kit["rules"]["published_v0_4_immutable"] is True

policy = json.loads(POLICY.read_text(encoding="utf-8"))
assert policy["status"] == "field_evaluation_policy_not_public"
assert policy["gates"]["R3_MORTAIN_RX"]["minimum_independent_sessions"] == 2
assert policy["gates"]["F5ZHA_SOURCE_AND_COVERAGE"]["minimum_independent_sessions"] == 2
assert policy["output_rules"]["field_gate_can_be_evaluated_automatically"] is True
assert policy["output_rules"]["promotion_ready_is_always_false"] is True
assert policy["output_rules"]["automatic_candidate_mutation_allowed"] is False
assert policy["output_rules"]["automatic_publication_allowed"] is False
assert policy["output_rules"]["human_source_review_still_required_after_satisfied_field_gate"] is True

handoff = refresh["field_handoff"]
assert handoff["kit"] == "research/normandie-v0.5/field-validation-kit.json"
assert handoff["evaluation_policy"] == "research/normandie-v0.5/field-evaluation-policy.json"
assert handoff["kit_already_covers_required_gates"] is True
assert handoff["new_diagnostic_memories_required"] is False
assert handoff["r3_required_independent_sessions"] == 2
assert handoff["f5zha_required_independent_sessions"] == 2
assert handoff["automatic_promotion_allowed"] is False
assert handoff["automatic_publication_allowed"] is False

# Current backlog may have advanced after Sprint 110. Preserve the historical refresh,
# while requiring any later state to keep the same source constraints and immutable v0.4 base.
backlog = json.loads(BACKLOG.read_text(encoding="utf-8"))
assert backlog["last_revalidated_on"] == "2026-08-22"
assert backlog["known_potential_ceiling_excluding_f6zes"] == 147
assert backlog["latest_source_refresh"] == "research/normandie-v0.5/sprint110-source-field-refresh.json"
assert backlog["public_export_allowed"] is False
backlog_by_id = {item["id"]: item for item in backlog["items"]}
assert set(backlog_by_id) == {"R3_MORTAIN_RX", "F5ZHA_SOURCE_AND_COVERAGE", "F1ZOV_OPERATIONAL_STATUS", "F6ZES_RESOLVED"}
assert all(item["last_checked_on"] == "2026-08-22" for item in backlog["items"])
assert backlog_by_id["F1ZOV_OPERATIONAL_STATUS"]["local_operator_status"] == "maintenance"
assert backlog_by_id["F6ZES_RESOLVED"]["usable_frequency_published"] is False
assert backlog["rules"]["automatic_candidate_mutation_allowed"] is False
assert backlog["rules"]["automatic_publication_allowed"] is False

if backlog["schema_version"] == "1.3":
    assert backlog["current_candidate_memory_count"] == 142
    assert backlog["current_candidate_memory_delta"] == 0
    assert backlog_by_id["R3_MORTAIN_RX"]["web_research_can_close_field_gate"] is False
    assert backlog_by_id["F5ZHA_SOURCE_AND_COVERAGE"]["web_research_can_close_field_gate"] is False
else:
    assert backlog["schema_version"] == "1.4"
    assert backlog["current_candidate_memory_count"] == 146
    assert backlog["current_candidate_memory_delta"] == 4
    assert backlog["theoretical_coverage_policy"] == "research/normandie-v0.5/theoretical-coverage-policy.json"
    assert backlog["field_validation_role"] == "optional_post_publication_quality_feedback"
    assert backlog_by_id["R3_MORTAIN_RX"]["promoted"] is True
    assert backlog_by_id["F5ZHA_SOURCE_AND_COVERAGE"]["promoted"] is True
    assert backlog["rules"]["theory_is_not_measured_reception"] is True

local_readme = LOCAL_README.read_text(encoding="utf-8")
assert "Aucune fréquence n'est inférée" in local_readme or "aucune fréquence" in local_readme.lower()
assert "F1ZOV" in local_readme and "F6ZES" in local_readme
if "Sprint 112" in local_readme:
    assert "146 mémoires RX" in local_readme
    assert "couverture théorique" in local_readme
    assert "retour qualité facultatif" in local_readme
else:
    for token in [
        "Sprint 110 / 0.21.98",
        "sources revalidées le 22 août 2026",
        "sprint110-source-field-refresh.json",
        "normandie-v0.5-field-session-template.csv",
        "vraies écoutes",
        "promotion_ready=false",
    ]:
        assert token in local_readme, token

public = json.loads(PUBLIC_V04.read_text(encoding="utf-8"))
assert public["status"] == "published_immutable"
assert public["version"] == "0.4"
assert public["memory_count"] == 142
assert public["published_version_is_immutable"] is True

state = json.loads(STATE.read_text(encoding="utf-8"))
assert state["current_sprint"] >= 110
assert state["public_packs"]["normandie"]["version"] == "0.4"
assert state["public_packs"]["normandie"]["memory_count"] == 142
assert state["public_packs"]["normandie"]["immutable"] is True

for rule in [
    "no_frequency_inference",
    "field_gates_not_closed_by_web",
    "local_operator_status_priority",
    "field_non_reception_is_not_negative_proof",
    "diagnostic_legacy_frequency_never_promoted",
    "published_v0_4_immutable",
]:
    assert refresh["rules"][rule] is True, rule
assert refresh["rules"]["public_mutation_performed"] is False

print("Sprint 110 historical Normandie v0.5 refresh remains auditable; later theoretical coverage policy may advance current candidate without rewriting Sprint 110 evidence OK")
