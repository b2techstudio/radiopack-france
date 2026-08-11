import importlib.util
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVALIDATION = ROOT / "research/normandie-v0.4/blocked-station-revalidation.json"
FIELD = ROOT / "research/normandie-v0.4/r3-mortain-field-validation.json"
PACK = ROOT / "research/normandie-v0.4/r3-validation-pack.json"
GATES = ROOT / "research/normandie-v0.4/promotion-gates.json"
RESUME = ROOT / "research/project-resume-state.json"
STATUS_DOC = ROOT / "PROJECT_STATUS.md"
RECORDER = ROOT / "tools/record_normandie_v04_r3_observation.py"
REPORTER = ROOT / "tools/build_normandie_v04_gate_report.py"
RUNNER = ROOT / "tools/run_normandie_v04_checks.py"

for path in (REVALIDATION, FIELD, PACK, GATES, RESUME, STATUS_DOC, RECORDER, REPORTER, RUNNER):
    assert path.is_file(), f"Missing expected file: {path}"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


revalidation = json.loads(REVALIDATION.read_text(encoding="utf-8"))
assert revalidation["schema_version"] == "1.0"
assert revalidation["status"] == "current_revalidation_snapshot_not_public"
assert revalidation["public_export_allowed"] is False
stations = {item["id"]: item for item in revalidation["stations"]}
assert set(stations) == {"F1ZBX_R3", "F5ZHA_LAVAL", "F1ZOV_EQUEURDREVILLE", "F6ZES_SOURDEVAL"}
assert stations["F1ZBX_R3"]["promotion_to_internal_candidate_allowed"] is False
assert stations["F5ZHA_LAVAL"]["local_operator_source_found"] is False
assert stations["F5ZHA_LAVAL"]["local_operator_search_failure_is_negative_evidence"] is False
assert stations["F1ZOV_EQUEURDREVILLE"]["state"] == "operator_maintenance"
assert stations["F6ZES_SOURDEVAL"]["must_not_guess_frequency"] is True

resume = json.loads(RESUME.read_text(encoding="utf-8"))
normandie_work = resume.get("normandie_v0_5_work", resume["active_work"])
assert resume["current_sprint"] >= 68
assert resume["state_version"] >= "0.21.57"
assert resume["public_packs"]["normandie"]["memory_count"] == 142
assert normandie_work["internal_candidate_memory_count"] == 142
assert normandie_work["blocked_frequency_count"] == 5
assert normandie_work["maximum_internal_memory_count_if_all_current_known_gates_clear"] == 147
assert normandie_work["current_guarded_promotion_plan_eligible_addition_count"] == 0
assert normandie_work["current_candidate_preview_memory_count"] == 142
assert normandie_work["current_release_blocker_count"] == 0
assert normandie_work["current_review_checklist_completed_count"] == 9
assert normandie_work["current_review_checklist_item_count"] == 9
assert normandie_work["current_review_blocking_open_count"] == 0
assert normandie_work["source_truth_consistent"] is True
assert normandie_work["source_revalidations_fresh_as_of_2026_08_10"] is True
assert normandie_work["source_revalidations_fresh_as_of_2026_08_11"] is True
assert normandie_work["prepublication_integrity_ok"] is True
assert normandie_work["prepublication_release_ready"] is True
assert normandie_work["public_export_allowed"] is False
assert normandie_work["public_release_ready"] is False
assert normandie_work["adjacent_ref_scan"]["new_untracked_active_analog_candidate_count"] == 0
assert normandie_work["adjacent_ref_scan"]["candidate_memory_delta"] == 0
assert normandie_work["latest_source_revalidation"]["gate_cleared_count"] == 0
assert normandie_work["latest_source_revalidation"]["f1zov_operator_status"] == "En Maintenance"
assert normandie_work["latest_source_revalidation"]["f5zha_repeaterbook_verification_date_shown"] == "2017-02-17"
assert normandie_work["latest_source_revalidation"]["f5zha_authoritative_reconciliation_complete"] is False
assert normandie_work["latest_source_revalidation"]["f6zes_frequency_mode_resolved"] is False
assert normandie_work["dual_rx_contract"]["r3_pair_frequencies_mhz"] == [145.075, 145.675]
assert normandie_work["dual_rx_contract"]["r3_required_rx_memory_count_if_promoted"] == 2
assert normandie_work["dual_rx_contract"]["r3_minimum_independent_field_sessions"] == 2
assert normandie_work["dual_rx_contract"]["r3_sessions_are_evidence_not_memories"] is True
assert normandie_work["dual_rx_contract"]["r3_control_memory_is_pair_member"] is False
assert normandie_work["dual_rx_contract"]["r3_memory_delta_if_gate_clears"] == 2
assert normandie_work["latest_primary_recheck"]["file"] == "research/sprint-65-primary-recheck.json"
assert normandie_work["latest_primary_recheck"]["f5zha_current_ref_pair_mhz"] == [145.4675, 432.575]
assert normandie_work["latest_primary_recheck"]["f5zha_current_ref_active"] is True
assert normandie_work["latest_primary_recheck"]["f5zha_authoritative_reconciliation_complete"] is False
assert normandie_work["latest_primary_recheck"]["f6zes_frequency_mode_resolved"] is False
assert normandie_work["latest_primary_recheck"]["normandie_gate_cleared_count"] == 0
assert normandie_work["latest_primary_recheck"]["candidate_memory_delta"] == 0
assert normandie_work["latest_technical_inventory_recheck"]["file"] == "research/sprint-66-technical-inventory-boundaries.json"
assert normandie_work["latest_technical_inventory_recheck"]["f5zha_authoritative_reconciliation_complete"] is False
assert normandie_work["latest_technical_inventory_recheck"]["f6zes_frequency_mode_resolved"] is False
assert normandie_work["latest_technical_inventory_recheck"]["normandie_gate_cleared_count"] == 0
assert normandie_work["latest_technical_inventory_recheck"]["candidate_memory_delta"] == 0
assert normandie_work["latest_current_reference_synthesis"]["file"] == "research/sprint-67-current-reference-synthesis.json"
assert normandie_work["latest_current_reference_synthesis"]["candidate_memory_delta"] == 0
assert resume["resume_rules"]["published_versions_are_immutable"] is True
assert resume["resume_rules"]["geometry_is_not_reception_proof"] is True
assert resume["resume_rules"]["field_observations_do_not_close_source_conflicts"] is True
assert resume["resume_rules"]["field_session_count_does_not_define_memory_count"] is True
assert resume["resume_rules"]["verified_distinct_pair_uses_two_rx_memories"] is True
assert resume["resume_rules"]["optional_control_memory_is_not_pair_member"] is True
assert resume["resume_rules"]["local_operator_status_overrides_general_directory_for_current_state"] is True
assert resume["resume_rules"]["stale_secondary_conflict_does_not_replace_required_authoritative_reconciliation"] is True
assert resume["resume_rules"]["stale_source_blocks_release_review_completion"] is True
assert resume["resume_rules"]["prepublication_integrity_ok_does_not_mean_release_ready"] is True
assert resume["resume_rules"]["secondary_source_clue_does_not_replace_required_primary_validation"] is True
assert resume["resume_rules"]["primary_source_conflict_requires_reconciliation"] is True
assert resume["resume_rules"]["primary_pdf_identified_but_unread_is_not_negative_evidence"] is True
assert resume["resume_rules"]["unread_primary_reference_is_not_negative_evidence"] is True
assert resume["resume_rules"]["local_channel63_convergence_does_not_disprove_channel64"] is True
assert resume["resume_rules"]["current_radio_infrastructure_does_not_imply_channel_assignment"] is True
assert resume["resume_rules"]["historical_primary_channel_assignment_is_not_current_validation"] is True
assert resume["resume_rules"]["current_regional_channel_statement_does_not_identify_transmitter_site"] is True
assert resume["resume_rules"]["current_cross_network_statement_does_not_map_channel_to_station"] is True
assert resume["resume_rules"]["current_maintenance_scope_does_not_name_station_channels"] is True
assert resume["resume_rules"]["association_existence_does_not_validate_repeater_frequency"] is True
assert resume["resume_rules"]["undated_secondary_schedule_is_not_current_primary_validation"] is True
assert resume["resume_rules"]["current_infrastructure_procurement_does_not_assign_channel"] is True
assert resume["resume_rules"]["current_primary_channel_confirmation_without_site_name_does_not_assign_transmitter"] is True
assert resume["resume_rules"]["secondary_source_convergence_does_not_become_primary_validation"] is True
assert resume["resume_rules"]["current_display_badge_does_not_override_dated_verification_provenance"] is True
assert resume["resume_rules"]["network_counting_units_must_not_be_reconciled_without_definition"] is True
assert normandie_work["unresolved_priority"]["station"] == "F6ZES Sourdeval"
assert normandie_work["unresolved_priority"]["candidate_memory_delta"] == 0
assert resume["bretagne_research_update"]["primary_current_channel79_transmitter_site_confirmed"] is False
assert resume["bretagne_research_update"]["current_primary_corsen_infrastructure_sites_verified"] == ["Cap Fréhel", "Stiff / Ouessant"]
assert resume["bretagne_research_update"]["historical_primary_channel79_context_exists"] is True
assert resume["bretagne_research_update"]["historical_primary_channel79_context_is_current_validation"] is False
assert resume["bretagne_research_update"]["secondary_current_clue_sites"] == ["Cap Fréhel", "Bodic"]
assert resume["bretagne_research_update"]["paired_rx_frequencies_mhz"] == [156.975, 161.575]
assert resume["bretagne_research_update"]["corsen_channel79_required_rx_memory_count_if_published"] == 2
assert resume["bretagne_research_update"]["new_rf_memory_delta"] == 0
assert resume["bretagne_research_update"]["site_assignment_promoted"] is False
assert resume["bretagne_research_update"]["etel_channel64_current_brittany_site_identified"] is False
assert resume["bretagne_research_update"]["etel_channel64_primary_source_conflict_open"] is True
assert resume["bretagne_research_update"]["etel_local_operational_sources_converge_on_channel63"] is True
assert resume["bretagne_research_update"]["etel_channel64_current_operation_proven"] is False
assert resume["bretagne_research_update"]["etel_channel64_stopped_proven"] is False
assert resume["bretagne_research_update"]["etel_channel64_required_rx_memory_count_if_published"] == 2
assert resume["bretagne_research_update"]["etel_channel64_new_rf_memory_delta"] == 0
assert resume["bretagne_research_update"]["meteofrance_guide_2026_fetch_retried_2026_08_11"] is True
assert resume["bretagne_research_update"]["meteofrance_guide_2026_content_extracted"] is False
assert resume["bretagne_research_update"]["latest_primary_recheck_file"] == "research/sprint-65-primary-recheck.json"
assert resume["bretagne_research_update"]["ministry_vhf_statement_page_updated"] == "2026-06-19"
assert resume["bretagne_research_update"]["ministry_current_channels63_and64_permanent_in_morbihan"] is True
assert resume["bretagne_research_update"]["ministry_current_channel64_site_named"] is False
assert resume["bretagne_research_update"]["cross_etel_current_etel_chassiron_channel63"] is True
assert resume["bretagne_research_update"]["cross_etel_current_channel64_site_named"] is False
assert resume["bretagne_research_update"]["cross_corsen_current_coastal_station_network_confirmed"] is True
assert resume["bretagne_research_update"]["cross_corsen_current_channel79_site_mapping_present"] is False
assert resume["bretagne_research_update"]["latest_technical_inventory_recheck_file"] == "research/sprint-66-technical-inventory-boundaries.json"
assert resume["bretagne_research_update"]["etel_2026_technical_maintenance_station_count"] == 17
assert resume["bretagne_research_update"]["etel_2026_technical_maintenance_names_channels_listed"] is False
assert resume["bretagne_research_update"]["corsen_stiff_2026_radio_infrastructure_revalidated"] is True
assert resume["bretagne_research_update"]["corsen_stiff_2026_channel79_mapping_present"] is False
assert resume["bretagne_research_update"]["corsen_secondary_undated_full_chain_sites"] == ["Cap Fréhel", "Bodic", "Batz", "Stiff / Ouessant", "Pointe du Raz"]
assert resume["bretagne_research_update"]["corsen_secondary_undated_full_chain_is_current_primary_validation"] is False

status_text = STATUS_DOC.read_text(encoding="utf-8")
assert "Sprint courant : **71**" in status_text
assert "État logique : **0.21.60**" in status_text
assert "python tools\\run_normandie_v04_checks.py" in status_text
assert "147 mémoires" in status_text
assert "0 ajout éligible" in status_text
assert "blocages de prépublication sont à **0**" in status_text
assert "revue v0.4 est **9/9**" in status_text
assert "publication enregistrée" in status_text
assert "Cap Fréhel" in status_text
assert "Bodic" in status_text
assert "Stiff / Ouessant" in status_text
assert "delta candidat **0**" in status_text
assert "conflit primaire actuel" in status_text
assert "convergence opérationnelle locale sur Ch63" in status_text
assert "16 stations VHF + 2 MF" in status_text
assert "17 stations radio" in status_text
assert "Guide Marine 2026" in status_text
assert "2017-02-17" in status_text
assert "2 mémoires RX" in status_text
assert "2 sessions" in status_text
assert "19 juin 2026" in status_text
assert "Sprint 66" in status_text

recorder = load_module("r3_recorder", RECORDER)
reporter = load_module("gate_reporter", REPORTER)

valid_observation = {
    "date_local": "2026-08-10",
    "time_local": "16:30",
    "location_description": "Mortain test fixture",
    "receiver_model": "Quansheng UV-K5 test fixture",
    "antenna_description": "test antenna",
    "frequency_mhz": 145.675,
    "signal_detected": True,
    "identification_confidence": "confirmed",
    "intelligibility_0_to_5": 4,
    "signal_strength_observation": "repeatable",
    "notes": "synthetic test only",
}

with tempfile.TemporaryDirectory(prefix="radiopack-v04-field-tools-") as tmp:
    temp_root = Path(tmp)
    research = temp_root / "research/normandie-v0.4"
    research.mkdir(parents=True)
    for source in (FIELD, PACK, GATES, REVALIDATION):
        shutil.copy2(source, research / source.name)

    count = recorder.append_observation(temp_root, dict(valid_observation))
    assert count == 1
    logged = json.loads((research / FIELD.name).read_text(encoding="utf-8"))
    assert len(logged["observations"]) == 1
    assert logged["observations"][0]["frequency_mhz"] == 145.675
    assert logged["rules"]["public_export_allowed"] is False

    no_signal = dict(valid_observation)
    no_signal.update({"frequency_mhz": 145.075, "signal_detected": False, "identification_confidence": "none", "intelligibility_0_to_5": 0})
    assert recorder.append_observation(temp_root, no_signal) == 2

    invalid_frequency = dict(valid_observation)
    invalid_frequency["frequency_mhz"] = 146.0
    try:
        recorder.validate_observation(temp_root, invalid_frequency)
    except ValueError:
        pass
    else:
        raise AssertionError("Recorder accepted a frequency outside the validation mini-pack")

    invalid_no_signal = dict(no_signal)
    invalid_no_signal["intelligibility_0_to_5"] = 1
    try:
        recorder.validate_observation(temp_root, invalid_no_signal)
    except ValueError:
        pass
    else:
        raise AssertionError("Recorder accepted intelligibility > 0 for a no-signal observation")

    report = reporter.build_report(temp_root)
    assert report["public_export_allowed"] is False
    assert report["current_internal_candidate_memory_count"] == 142
    assert report["gates"]["R3_MORTAIN_RX"]["passed"] is False
    assert report["gates"]["R3_MORTAIN_RX"]["valid_session_count"] == 1
    assert report["gates"]["F5ZHA_SOURCE_AND_COVERAGE"]["passed"] is False
    assert report["gates"]["F1ZOV_OPERATIONAL_STATUS"]["passed"] is False
    assert report["all_blocked_gates_passed"] is False

    out = temp_root / "out"
    json_path, md_path, written = reporter.write_report(temp_root, out)
    assert json_path.is_file() and md_path.is_file()
    assert written["public_export_allowed"] is False
    assert "Toutes les portes franchies : non" in md_path.read_text(encoding="utf-8")

print(
    "Tests Normandie v0.4 field tools: current external revalidation snapshot guarded, "
    "R3 observation recorder validates/atomically appends RX-only evidence, gate report stays "
    "non-public, recovery state is self-contained through sprint 71, OK"
)
