import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVALIDATION = ROOT / "research/bretagne-v0.2/amateur-infrastructure-revalidation.json"
PAIRED = ROOT / "research/paired-rx-deduplicated-memory-plan.json"
BUILDER = ROOT / "tools/build_bretagne_v02_internal_candidate.py"
PUBLIC_V02 = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


revalidation = json.loads(REVALIDATION.read_text(encoding="utf-8"))
assert revalidation["status"] == "current_revalidation_not_public"
assert revalidation["pack"] == "Bretagne"
assert revalidation["target_version"] == "0.2"
assert revalidation["checked_on"] == "2026-08-12"
assert revalidation["candidate_memory_count_before"] == 151
assert revalidation["candidate_memory_count_after"] == 151
assert revalidation["candidate_memory_delta"] == 0
assert revalidation["public_export_allowed"] is False

items = {item["id"]: item for item in revalidation["items"]}
assert set(items) == {"F5ZPV", "F5ZZH", "F1ZBZ", "F5ZZC-4"}

zpv = items["F5ZPV"]
assert zpv["operator_status"] == "temporarily_stopped"
assert zpv["directory_status"] == "active"
assert zpv["status_conflict"] is True
assert zpv["operator_status_overrides_directory"] is True
assert zpv["documented_pair_mhz"] == [430.475, 439.875]
assert zpv["internal_candidate_promoted"] is False
assert zpv["candidate_memory_delta"] == 0
assert zpv["decision"] == "exclude_while_local_operator_reports_stopped"

zzh = items["F5ZZH"]
assert zzh["operator_status"] == "temporarily_stopped_searching_new_site"
assert zzh["directory_status"] == "stopped"
assert zzh["status_conflict"] is False
assert zzh["documented_pair_mhz"] == [145.1875, 145.7875]
assert zzh["internal_candidate_promoted"] is False
assert zzh["candidate_memory_delta"] == 0

zbz = items["F1ZBZ"]
assert zbz["directory_status"] == "active_multi_path_transponder"
assert zbz["documented_unique_rf_mhz"] == [145.025, 145.1375, 145.625, 145.7375, 431.2]
assert zbz["all_current_directory_rf_already_represented"] is True
assert zbz["direction_review_creates_new_rf_memory"] is False
assert zbz["candidate_memory_delta"] == 0
assert zbz["decision"] == "rf_inventory_resolved_no_new_memory_required"

paired = json.loads(PAIRED.read_text(encoding="utf-8"))
bretagne = next(region for region in paired["regions"] if region["id"] == "bretagne-v0.1")
by_frequency = {round(float(item["frequency_mhz"]), 6): item for item in bretagne["memories"]}
for frequency in zbz["documented_unique_rf_mhz"]:
    assert round(float(frequency), 6) in by_frequency
assert "F1ZBZ repeater emission path" in by_frequency[145.1375]["roles"]
assert "F1ZBZ repeater reception path" in by_frequency[145.7375]["roles"]
assert by_frequency[431.2]["name_hint"] == "ZBZ-U"
assert by_frequency[145.625]["name_hint"] == "ZBZ-VA"
assert by_frequency[145.025]["name_hint"] == "ZBZ-VB"

zzc = items["F5ZZC-4"]
assert zzc["role"] == "APRS digipeater managed by ADRASEC 35"
assert zzc["current_aprs_frequency_validated"] is False
assert zzc["ref_f5zzc_analog_entry_is_same_service_proven"] is False
assert zzc["ref_f5zzc_analog_entry"]["status"] == "stopped"
assert zzc["ref_f5zzc_analog_entry"]["frequency_mhz"] == 432.975
assert zzc["must_not_conflate_f5zzc_with_f5zzc_dash4_aprs"] is True
assert zzc["internal_candidate_promoted"] is False
assert zzc["candidate_memory_delta"] == 0

summary = revalidation["summary"]
assert summary["reviewed_item_count"] == 4
assert summary["new_active_candidate_count"] == 0
assert summary["resolved_zero_delta_item_count"] == 1
assert summary["resolved_zero_delta_ids"] == ["F1ZBZ"]
assert set(summary["still_blocked_or_unresolved_ids"]) == {"F5ZPV", "F5ZZH", "F5ZZC-4"}
assert summary["candidate_memory_delta"] == 0
assert summary["candidate_memory_count"] == 151

rules = revalidation["rules"]
assert rules["local_operator_status_overrides_general_directory_for_current_state"] is True
assert rules["stopped_infrastructure_not_promoted"] is True
assert rules["directory_active_does_not_override_local_operator_stopped"] is True
assert rules["same_rf_frequency_deduplicated"] is True
assert rules["similar_callsign_does_not_prove_same_service"] is True
assert rules["stale_role_evidence_does_not_validate_current_frequency"] is True
assert rules["public_export_allowed"] is False

builder = load_module("bretagne_v02_sprint76", BUILDER)
candidate = builder.build_candidate(ROOT)
assert candidate["memory_count"] == 151
assert candidate["new_memory_count"] == 16
assert candidate["aviation_memory_count"] == 16
assert candidate["public_export_allowed"] is False
assert not PUBLIC_V02.exists()

print("Sprint 76 Bretagne amateur revalidation: F1ZBZ resolved at zero RF delta; F5ZPV/F5ZZH/F5ZZC-4 remain excluded or unresolved; candidate stays 151 and public v0.2 remains absent OK")
