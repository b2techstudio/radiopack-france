import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = json.loads((ROOT / "research/normandie-v0.5/pack-plan.json").read_text(encoding="utf-8"))
BACKLOG = json.loads((ROOT / "research/normandie-v0.5/backlog.json").read_text(encoding="utf-8"))
REVALIDATION = json.loads((ROOT / "research/normandie-v0.5/current-blocker-revalidation.json").read_text(encoding="utf-8"))
RECORD = json.loads((ROOT / "research/normandie-v0.4/publication-record.json").read_text(encoding="utf-8"))
PUBLIC_V04 = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv"
PUBLIC_V05 = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.5.csv"
BUILDER = ROOT / "tools/build_normandie_v05_internal_candidate.py"
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"

assert PLAN["status"] == "research_next_version_not_public"
assert PLAN["target_version"] == "0.5" and PLAN["based_on_published_version"] == "0.4"
assert PLAN["published_base_memory_count"] == 142 and PLAN["published_base_is_immutable"] is True
assert PLAN["current_candidate_memory_count"] == 142 and PLAN["current_new_memory_count"] == 0
assert PLAN["known_potential_ceiling_excluding_f6zes"] == 147
assert PLAN["last_revalidated_on"] == "2026-08-15"
assert PLAN["last_revalidation_promoted_item_count"] == 0
assert PLAN["last_revalidation_memory_delta"] == 0
assert PLAN["public_export_allowed"] is False and PLAN["public_registry_allowed"] is False

assert PUBLIC_V04.is_file() and not PUBLIC_V05.exists()
public_sha = hashlib.sha256(PUBLIC_V04.read_bytes()).hexdigest()
assert RECORD["status"] == "published_immutable" and RECORD["version"] == "0.4"
assert RECORD["memory_count"] == 142
assert RECORD["public_csv_sha256"] == public_sha == PLAN["published_base_sha256"]

with tempfile.TemporaryDirectory(prefix="radiopack-normandie-v05-") as td:
    subprocess.run(
        [sys.executable, str(BUILDER), "--root", str(ROOT), "--output-dir", td],
        check=True,
    )
    csv_path = Path(td) / "normandie-v0.5-internal.csv"
    json_path = Path(td) / "normandie-v0.5-internal.json"
    assert csv_path.is_file() and json_path.is_file()
    assert csv_path.read_bytes() == PUBLIC_V04.read_bytes()
    candidate = json.loads(json_path.read_text(encoding="utf-8"))
    assert candidate["target_version"] == "0.5"
    assert candidate["memory_count"] == 142 and candidate["new_memory_count"] == 0
    assert candidate["published_base_version"] == "0.4"
    assert candidate["published_base_sha256"] == public_sha
    assert candidate["known_potential_ceiling_excluding_f6zes"] == 147
    assert candidate["public_export_allowed"] is False
    assert candidate["rules"]["published_v0_4_immutable"] is True
    assert candidate["rules"]["field_evidence_required_where_gate_demands_it"] is True
    assert candidate["rules"]["unresolved_frequency_must_not_be_guessed"] is True

assert REVALIDATION["status"] == "current_blocker_revalidation_zero_promotions_not_public"
assert REVALIDATION["sprint"] == 83 and REVALIDATION["checked_on"] == "2026-08-15"
assert REVALIDATION["candidate_memory_count_before"] == 142
assert REVALIDATION["candidate_memory_count_after"] == 142
assert REVALIDATION["candidate_memory_delta"] == 0
assert REVALIDATION["promoted_item_count"] == 0
assert REVALIDATION["known_potential_ceiling_excluding_f6zes"] == 147

findings = REVALIDATION["findings"]
r3 = findings["R3_MORTAIN_RX"]
assert r3["current_operator_status"] == "operational"
assert r3["current_pair_mhz"] == [145.075, 145.675]
assert r3["field_reception_from_mortain_validated"] is False
assert r3["minimum_independent_rx_sessions_required"] == 2
assert r3["promoted"] is False

zha = findings["F5ZHA_SOURCE_AND_COVERAGE"]
assert zha["current_ref_status"] == "active"
assert zha["current_ref_pair_mhz"] == [145.4675, 432.575]
assert zha["second_current_list_supports_ref_pair"] is True
assert zha["conflicting_repeaterbook_frequency_mhz"] == 431.4125
assert zha["conflicting_repeaterbook_entry_last_verified"] == "2017-02-17"
assert zha["useful_mortain_coverage_verified"] is False
assert zha["promoted"] is False

zov = findings["F1ZOV_OPERATIONAL_STATUS"]
assert zov["local_operator_status"] == "maintenance"
assert zov["local_operator_pair_mhz"] == [430.375, 431.975]
assert zov["ref_directory_status"] == "active"
assert zov["local_operator_status_overrides_general_directory"] is True
assert zov["promoted"] is False

zes = findings["F6ZES_RESOLVED"]
assert zes["current_ref_site_listing_confirmed"] is True
assert zes["usable_frequency_published"] is False
assert zes["mode_published"] is False
assert zes["operational_state_published"] is False
assert zes["promoted"] is False

items = {item["id"]: item for item in BACKLOG["items"]}
assert set(items) == {"R3_MORTAIN_RX", "F5ZHA_SOURCE_AND_COVERAGE", "F1ZOV_OPERATIONAL_STATUS", "F6ZES_RESOLVED"}
assert items["R3_MORTAIN_RX"]["potential_memory_delta"] == 2 and items["R3_MORTAIN_RX"]["promoted"] is False
assert items["F5ZHA_SOURCE_AND_COVERAGE"]["potential_memory_delta"] == 2 and items["F5ZHA_SOURCE_AND_COVERAGE"]["promoted"] is False
assert items["F1ZOV_OPERATIONAL_STATUS"]["potential_memory_delta"] == 1 and items["F1ZOV_OPERATIONAL_STATUS"]["promoted"] is False
assert items["F6ZES_RESOLVED"]["potential_memory_delta"] is None and items["F6ZES_RESOLVED"]["must_not_guess"] is True

registry = REGISTRY.read_text(encoding="utf-8")
assert '/downloads/normandie/radiopack-france-normandie-v0.4.csv' in registry
assert '/downloads/normandie/radiopack-france-normandie-v0.5.csv' not in registry

print("Sprint 83 Normandie v0.5 current blockers revalidated: candidate 142, delta 0, ceiling 147 excluding unresolved F6ZES, no public mutation OK")
