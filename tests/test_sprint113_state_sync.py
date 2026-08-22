#!/usr/bin/env python3
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "research/project-resume-state.json"
RECORD = ROOT / "research/normandie-v0.5/publication-record.json"
FREEZE = ROOT / "research/normandie-v0.5/candidate-freeze.json"
PUBLIC = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.5.csv"
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"
REGIONS = ROOT / "website/src/data/regions.json"
OPTIONS = ROOT / "generator/options.json"
README = ROOT / "README.md"
STATUS = ROOT / "PROJECT_STATUS.md"
CHANGELOG = ROOT / "CHANGELOG.md"
SUMMARY = ROOT / "research/sprint-113-summary.md"

EXPECTED_SHA = "1d7ce66c7a5faafe98e4ee59791bcd29af1fd1f432ee1bfc1cad7cba3bc5cf59"

for path in [STATE, RECORD, FREEZE, PUBLIC, REGISTRY, REGIONS, OPTIONS, README, STATUS, CHANGELOG, SUMMARY]:
    assert path.is_file(), path

state = json.loads(STATE.read_text(encoding="utf-8"))
assert state["schema_version"] == "1.5"
assert state["updated"] == "2026-08-22"
assert state["current_sprint"] == 113
assert state["state_version"] == "0.22.01"

normandie = state["public_packs"]["normandie"]
assert normandie["version"] == "0.5"
assert normandie["memory_count"] == 146
assert normandie["immutable"] is True
assert normandie["previous_immutable_version"] == "0.4"
assert normandie["previous_memory_count"] == 142
assert normandie["publication_record"] == "research/normandie-v0.5/publication-record.json"
assert normandie["public_csv_sha256"] == EXPECTED_SHA
assert normandie["coverage_basis"] == "theoretical_documented"
assert normandie["measured_reception_claimed"] is False

s112 = state["latest_sprint112_normandie_v05_theoretical_candidate"]
assert s112["sprint"] == 112
assert s112["state_version"] == "0.22.00"
assert s112["status"] == "normandie_v05_theoretical_candidate_frozen_internal"
assert s112["candidate_memory_count"] == 146
assert s112["candidate_memory_delta"] == 4
assert s112["theoretical_coverage_memory_count"] == 4
assert s112["candidate_sha256"] == EXPECTED_SHA
assert s112["published"] is False

s113 = state["latest_sprint113_normandie_v05_publication"]
assert s113["sprint"] == 113
assert s113["state_version"] == "0.22.01"
assert s113["status"] == "normandie_v05_published_immutable_theoretical_coverage"
assert s113["memory_count"] == 146
assert s113["previous_public_version"] == "0.4"
assert s113["previous_memory_count"] == 142
assert s113["memory_delta"] == 4
assert s113["theoretical_coverage_memory_count"] == 4
assert s113["candidate_public_byte_identity_verified"] is True
assert s113["public_csv_sha256"] == EXPECTED_SHA
assert s113["field_reception_required_for_publication"] is False
assert s113["field_sessions_are_optional_quality_feedback"] is True
assert s113["published"] is True
assert s113["published_version_is_immutable"] is True

publication = state["normandie_v0_5_publication"]
assert publication["memory_count"] == 146
assert publication["memory_delta"] == 4
assert publication["candidate_public_byte_identity_verified"] is True
assert publication["field_reception_verified"] is False
assert publication["field_reception_required_for_publication"] is False
assert publication["field_sessions_are_optional_quality_feedback"] is True
assert publication["deferred_after_v0_5"] == ["F1ZOV_OPERATIONAL_STATUS", "F6ZES_RESOLVED"]

rules = state["resume_rules"]
assert rules["theoretical_coverage_may_close_coverage_gate_when_source_and_operational_status_are_documented"] is True
assert rules["theory_is_not_measured_or_guaranteed_reception"] is True
assert rules["field_listening_is_optional_quality_feedback_for_coverage"] is True
assert rules["maintenance_status_must_not_be_overridden_by_theory"] is True
assert rules["unresolved_frequency_or_mode_must_not_be_guessed"] is True

priority = state["next_priority"]
assert priority["coverage_policy"] == "documented_theoretical_plausibility_may_close_coverage_gate"
assert priority["field_listening_role"] == "optional_quality_feedback"
assert priority["must_not_claim_measured_reception_without_measurement"] is True
assert priority["must_not_override_maintenance_status"] is True
assert priority["must_not_guess_unresolved_frequency_or_mode"] is True
assert priority["normandie_source_watch"] == ["F1ZOV", "F6ZES"]

bretagne = state["bretagne_v0_3_airac_handoff"]
assert bretagne["candidate_memory_count"] == 151
assert bretagne["candidate_memory_delta"] == 0
assert bretagne["airac_current"] == "08/26"
assert bretagne["airac_current_until_inclusive"] == "2026-09-02"
assert bretagne["airac_next_required"] == "09/26"
assert bretagne["airac_next_effective_from"] == "2026-09-03"
assert bretagne["publication_allowed_before_airac09_revalidation"] is False
assert bretagne["candidate_rebuild_allowed_before_effective_date"] is False

record = json.loads(RECORD.read_text(encoding="utf-8"))
assert record["status"] == "published_immutable"
assert record["publication_sprint"] == 113
assert record["state_version"] == "0.22.01"
assert record["version"] == "0.5"
assert record["memory_count"] == 146
assert record["new_memory_count_vs_v0_4"] == 4
assert record["public_csv_sha256"] == EXPECTED_SHA
assert record["candidate_sha256"] == EXPECTED_SHA
assert record["candidate_public_byte_identity_verified"] is True
assert record["previous_public_version"] == "0.4"
assert record["previous_public_memory_count"] == 142
assert record["theoretical_coverage"]["memory_count"] == 4
assert record["theoretical_coverage"]["locations"] == [178, 179, 180, 181]
assert record["theoretical_coverage"]["field_reception_verified"] is False
assert record["theoretical_coverage"]["field_reception_required_for_publication"] is False
assert record["theoretical_coverage"]["theory_is_not_measured_or_guaranteed_reception"] is True
assert record["rules"]["field_sessions_are_optional_quality_feedback"] is True
assert record["rules"]["maintenance_status_not_overridden_by_theory"] is True
assert record["published_version_is_immutable"] is True

freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
assert freeze["candidate_memory_count"] == 146
assert freeze["candidate_sha256"] == EXPECTED_SHA

assert hashlib.sha256(PUBLIC.read_bytes()).hexdigest() == EXPECTED_SHA
with PUBLIC.open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
assert len(rows) == 146
assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
assert len({row["Location"] for row in rows}) == 146
assert len({row["Name"] for row in rows}) == 146
new_rows = rows[-4:]
assert [row["Location"] for row in new_rows] == ["178", "179", "180", "181"]
assert [row["Name"] for row in new_rows] == ["35-R3-IN", "35-R3-OUT", "53-ZHA-V", "53-ZHA-U"]
assert [round(float(row["Frequency"]), 6) for row in new_rows] == [145.075, 145.675, 145.4675, 432.575]

registry = REGISTRY.read_text(encoding="utf-8")
for token in [
    'id: "normandie"',
    'version: "v0.5"',
    'memoryCount: 146',
    '/downloads/normandie/radiopack-france-normandie-v0.5.csv',
    'couverture théorique',
]:
    assert token in registry, token

regions = json.loads(REGIONS.read_text(encoding="utf-8"))
region = next(item for item in regions if item["slug"] == "normandie")
assert region["status"] == "v0.5 disponible"
assert region["memoryCount"] == 146
assert "théorique" in region["description"].lower()

options = json.loads(OPTIONS.read_text(encoding="utf-8"))
normandie_option = next(item for item in options["pack_selection"]["packs"] if item["id"] == "normandie")
assert normandie_option["version"] == "v0.5"
assert normandie_option["default_memory_count"] == 146
assert normandie_option["coverage_basis"] == "theoretical_documented"
assert normandie_option["measured_reception_claimed"] is False
assert any("écoutes terrain" in rule.lower() and "facultatif" in rule.lower() for rule in options["rules"])

readme = README.read_text(encoding="utf-8")
for token in [
    "État courant : Sprint 113 / 0.22.01",
    "**Normandie v0.5** — 146 mémoires RX",
    "1595 mémoires RX cumulées",
    "## Sprint 113 — Normandie v0.5 publiée sur couverture théorique",
    "## Sprint 112 — Normandie v0.5 : candidat théorique figé",
    "contrôle qualité facultatif",
]:
    assert token in readme, token

status = STATUS.read_text(encoding="utf-8")
for token in [
    "Sprint courant : **113**",
    "État logique : **0.22.01**",
    "Normandie v0.5 : **146 mémoires RX**",
    "## Sprint 113 — Normandie v0.5 publiée",
    "couverture théorique documentée",
]:
    assert token in status, token

changelog = CHANGELOG.read_text(encoding="utf-8")
assert "## 0.22.01 - 2026-08-22" in changelog
assert "**Sprint 113**" in changelog.split("## 0.22.00", 1)[0]
assert EXPECTED_SHA in changelog

summary = SUMMARY.read_text(encoding="utf-8")
assert "146 mémoires RX" in summary
assert EXPECTED_SHA in summary
assert "couverture théorique" in summary

print("Sprint 113 canonical state: Normandie v0.5 146 RX immutable/theoretical, exact SHA, site/generator synchronized, Bretagne AIRAC09 gate preserved OK")
