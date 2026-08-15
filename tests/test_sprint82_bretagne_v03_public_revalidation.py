import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research/bretagne-v0.3"
EVIDENCE = json.loads((RESEARCH / "public-service-revalidation.json").read_text(encoding="utf-8"))
BACKLOG = json.loads((RESEARCH / "backlog.json").read_text(encoding="utf-8"))
PLAN = json.loads((RESEARCH / "pack-plan.json").read_text(encoding="utf-8"))
PUBLIC_V02 = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"
PUBLIC_V03 = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.3.csv"
REGISTRY = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")

assert EVIDENCE["status"] == "current_public_revalidation_zero_rf_delta_not_public"
assert EVIDENCE["sprint"] == 82 and EVIDENCE["checked_on"] == "2026-08-15"
assert EVIDENCE["candidate_memory_count_before"] == 151
assert EVIDENCE["candidate_memory_count_after"] == 151
assert EVIDENCE["candidate_memory_delta"] == 0
assert EVIDENCE["public_export_allowed"] is False
assert len(EVIDENCE["reviewed_ids"]) == 6

f = EVIDENCE["findings"]
f1zug = f["F1ZUG_ADRASEC35_TRANSPONDER_FREQUENCY"]
assert f1zug["current_aprs_frequency_mhz"] == 144.8
assert f1zug["current_aprs_frequency_publicly_documented"] is True
assert f1zug["recent_aprs_activity_visible_in_public_index"] is True
assert f1zug["aprs_frequency_already_present_nationally"] is True
assert f1zug["adrasec35_transponder_frequency_publicly_published"] is False
assert f1zug["new_unique_rf_memory_count"] == 0 and f1zug["promoted"] is False

f5zzc4 = f["F5ZZC4_CURRENT_APRS_FREQUENCY"]
assert f5zzc4["historical_ara35_aprs_role_exists"] is True
assert f5zzc4["historical_role_source_is_current_frequency_validation"] is False
assert f5zzc4["current_service_specific_frequency_validated"] is False
assert f5zzc4["absence_of_recent_trace_is_proof_of_stop"] is False
assert f5zzc4["must_not_conflate_with_f5zzc_analog"] is True
assert f5zzc4["new_unique_rf_memory_count"] == 0 and f5zzc4["promoted"] is False

f5zpv = f["F5ZPV_RESTART_REVALIDATION"]
assert f5zpv["local_operator_current_page_reports_stopped"] is True
assert f5zpv["general_directory_reports_active"] is True
assert f5zpv["local_operator_status_overrides_general_directory"] is True
assert f5zpv["restart_evidence_established"] is False

f5zzh = f["F5ZZH_RESTART_REVALIDATION"]
assert f5zzh["local_operator_current_page_reports_stopped"] is True
assert f5zzh["local_operator_searching_new_site"] is True
assert f5zzh["restart_evidence_established"] is False

etel = f["CROSS_ETEL_CH64_LOCAL_MAPPING"]
assert etel["generic_pair_mhz"] == [156.225, 160.825]
assert etel["generic_pair_already_present"] is True
assert etel["ministry_current_regional_channels63_and64_morbihan"] is True
assert etel["ministry_names_channel64_brittany_transmitter_site"] is False
assert etel["cross_etel_current_etel_channel63_mapping"] is True
assert etel["cross_etel_current_etel_channel64_mapping"] is False
assert etel["primary_source_conflict_remains_open"] is True
assert etel["new_unique_rf_memory_count"] == 0 and etel["promoted_local_site_mapping"] is False

corsen = f["CROSS_CORSEN_CH79_LOCAL_MAPPING"]
assert corsen["generic_pair_mhz"] == [156.975, 161.575]
assert corsen["generic_pair_already_present"] is True
assert corsen["current_cross_vhf_mhf_network_confirmed"] is True
assert corsen["primary_current_channel79_transmitter_site_mapping_found"] is False
assert corsen["new_unique_rf_memory_count"] == 0 and corsen["promoted_local_site_mapping"] is False

assert all(f[item]["new_unique_rf_memory_count"] == 0 for item in EVIDENCE["reviewed_ids"])

items = {item["id"]: item for item in BACKLOG["items"]}
assert BACKLOG["latest_public_revalidation"]["sprint"] == 82
assert BACKLOG["latest_public_revalidation"]["candidate_memory_delta"] == 0
assert BACKLOG["latest_public_revalidation"]["promoted_item_count"] == 0
assert items["F1ZUG_ADRASEC35_TRANSPONDER_FREQUENCY"]["adrasec_transponder_frequency_mhz"] is None
assert items["F1ZUG_ADRASEC35_TRANSPONDER_FREQUENCY"]["candidate_memory_delta"] == 0
assert items["F5ZZC4_CURRENT_APRS_FREQUENCY"]["current_service_specific_frequency_validated"] is False
assert items["F5ZPV_RESTART_REVALIDATION"]["local_operator_reports_stopped"] is True
assert items["F5ZZH_RESTART_REVALIDATION"]["local_operator_reports_stopped"] is True
assert items["CROSS_ETEL_CH64_LOCAL_MAPPING"]["candidate_memory_delta"] == 0
assert items["CROSS_CORSEN_CH79_LOCAL_MAPPING"]["candidate_memory_delta"] == 0

assert PLAN["latest_public_revalidation"]["sprint"] == 82
assert PLAN["latest_public_revalidation"]["candidate_memory_delta"] == 0
assert PLAN["current_candidate_memory_count"] == 151 and PLAN["current_new_memory_count"] == 0
assert PLAN["public_export_allowed"] is False and PLAN["public_registry_allowed"] is False

with tempfile.TemporaryDirectory(prefix="radiopack-bretagne-v03-s82-") as td:
    subprocess.run([
        sys.executable,
        str(ROOT / "tools/build_bretagne_v03_internal_candidate.py"),
        "--root",
        str(ROOT),
        "--output-dir",
        td,
    ], check=True)
    candidate = json.loads((Path(td) / "bretagne-v0.3-internal.json").read_text(encoding="utf-8"))
    assert candidate["memory_count"] == 151 and candidate["new_memory_count"] == 0
    assert (Path(td) / "bretagne-v0.3-internal.csv").read_bytes() == PUBLIC_V02.read_bytes()

assert PUBLIC_V02.is_file() and not PUBLIC_V03.exists()
assert "radiopack-france-bretagne-v0.2.csv" in REGISTRY
assert "radiopack-france-bretagne-v0.3.csv" not in REGISTRY

assert EVIDENCE["rules"]["unpublished_service_frequency_must_not_be_inferred"] is True
assert EVIDENCE["rules"]["absence_from_public_live_index_does_not_prove_stopped"] is True
assert EVIDENCE["rules"]["local_operator_status_overrides_general_directory_for_current_state"] is True
assert EVIDENCE["rules"]["generic_rf_pair_not_duplicated_for_local_metadata"] is True
assert EVIDENCE["rules"]["private_operational_ppdr_and_adrasec_data_excluded"] is True

print("Sprint 82 Bretagne v0.3: six non-AIRAC open dossiers revalidated from public sources, zero RF delta, candidate remains exact public v0.2=151, no v0.3 publication OK")
