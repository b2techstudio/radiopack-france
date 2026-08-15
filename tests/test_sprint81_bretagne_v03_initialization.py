import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = json.loads((ROOT / "research/bretagne-v0.3/pack-plan.json").read_text(encoding="utf-8"))
BACKLOG = json.loads((ROOT / "research/bretagne-v0.3/backlog.json").read_text(encoding="utf-8"))
AIRAC = json.loads((ROOT / "research/bretagne-v0.3/airac-transition-policy.json").read_text(encoding="utf-8"))
RECORD = json.loads((ROOT / "research/bretagne-v0.2/publication-record.json").read_text(encoding="utf-8"))
PUBLIC_V02 = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"
PUBLIC_V03 = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.3.csv"
BUILDER = ROOT / "tools/build_bretagne_v03_internal_candidate.py"
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"

assert PLAN["status"].startswith("research_next_version_not_public")
assert PLAN["target_version"] == "0.3" and PLAN["based_on_published_version"] == "0.2"
assert PLAN["published_base_memory_count"] == 151 and PLAN["published_base_is_immutable"] is True
assert PLAN["current_candidate_memory_count"] == 151 and PLAN["current_new_memory_count"] == 0
assert PLAN["public_export_allowed"] is False and PLAN["public_registry_allowed"] is False
assert PLAN["initialization"]["candidate_is_exact_public_v0_2_base"] is True
assert PLAN["initialization"]["new_rf_promoted"] is False
assert PLAN["initialization"]["new_metadata_promoted"] is False

assert PUBLIC_V02.is_file() and not PUBLIC_V03.exists()
public_sha = hashlib.sha256(PUBLIC_V02.read_bytes()).hexdigest()
assert RECORD["status"] == "published_immutable"
assert RECORD["version"] == "0.2" and RECORD["memory_count"] == 151
assert RECORD["public_csv_sha256"] == public_sha == PLAN["published_base_sha256"]

with PUBLIC_V02.open(encoding="utf-8", newline="") as handle:
    public_rows = list(csv.DictReader(handle))
assert len(public_rows) == 151
assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in public_rows)
assert len({int(row["Location"]) for row in public_rows}) == 151
assert len({row["Name"] for row in public_rows}) == 151
assert len({round(float(row["Frequency"]), 6) for row in public_rows}) == 151

with tempfile.TemporaryDirectory(prefix="radiopack-bretagne-v03-") as td:
    subprocess.run(
        [sys.executable, str(BUILDER), "--root", str(ROOT), "--output-dir", td],
        check=True,
    )
    csv_path = Path(td) / "bretagne-v0.3-internal.csv"
    json_path = Path(td) / "bretagne-v0.3-internal.json"
    assert csv_path.is_file() and json_path.is_file()
    assert csv_path.read_bytes() == PUBLIC_V02.read_bytes()
    candidate = json.loads(json_path.read_text(encoding="utf-8"))
    assert candidate["target_version"] == "0.3"
    assert candidate["memory_count"] == 151 and candidate["new_memory_count"] == 0
    assert candidate["published_base_version"] == "0.2"
    assert candidate["published_base_sha256"] == public_sha
    assert candidate["public_export_allowed"] is False
    assert candidate["rules"]["published_v0_2_immutable"] is True
    assert candidate["rules"]["post_2026_09_02_aviation_publication_requires_revalidation"] is True

assert AIRAC["status"] == "transition_policy_not_public"
assert AIRAC["current_cycle"]["cycle"] == "AIRAC 08/26"
assert AIRAC["current_cycle"]["effective_until_inclusive"] == "2026-09-02"
assert AIRAC["current_cycle"]["current_on_checked_date"] is True
assert AIRAC["next_cycle"]["cycle"] == "AIRAC 09/26"
assert AIRAC["next_cycle"]["effective_from"] == "2026-09-03"
assert AIRAC["next_cycle"]["effective_until_inclusive"] == "2026-09-30"
assert AIRAC["policy"]["published_v0_2_remains_immutable_after_airac08_expiry"] is True
assert AIRAC["policy"]["publication_on_or_after_2026_09_03_requires_airac09_revalidation"] is True
assert AIRAC["policy"]["direct_xml_field_match_must_not_be_claimed_without_xml_extraction"] is True

items = {item["id"]: item for item in BACKLOG["items"]}
assert set(items) == {
    "AIRAC_09_BRETAGNE_REVALIDATION",
    "F1ZUG_ADRASEC35_TRANSPONDER_FREQUENCY",
    "CROSS_ETEL_CH64_LOCAL_MAPPING",
    "CROSS_CORSEN_CH79_LOCAL_MAPPING",
    "F5ZPV_RESTART_REVALIDATION",
    "F5ZZH_RESTART_REVALIDATION",
    "F5ZZC4_CURRENT_APRS_FREQUENCY",
}
assert items["AIRAC_09_BRETAGNE_REVALIDATION"]["potential_memory_delta"] is None
assert items["F1ZUG_ADRASEC35_TRANSPONDER_FREQUENCY"]["private_operational_research_allowed"] is False
assert items["F1ZUG_ADRASEC35_TRANSPONDER_FREQUENCY"]["adrasec_transponder_frequency_mhz"] is None
for item_id in ("CROSS_ETEL_CH64_LOCAL_MAPPING", "CROSS_CORSEN_CH79_LOCAL_MAPPING"):
    assert items[item_id]["generic_memory_already_present_in_published_base"] is True
    assert items[item_id]["potential_new_rf_memory_delta"] == 0
    assert items[item_id]["promoted_local_site_mapping"] is False
for item_id in ("F5ZPV_RESTART_REVALIDATION", "F5ZZH_RESTART_REVALIDATION", "F5ZZC4_CURRENT_APRS_FREQUENCY"):
    assert items[item_id]["potential_memory_delta"] in (None, 0)
    assert items[item_id]["promoted"] is False

assert set(PLAN["resolved_v0_2_items_not_reopened"]) == {
    "ADRASEC_PUBLIC_DATA_REVALIDATION",
    "F1ZBZ_RF_DIRECTION_REVIEW",
}
assert BACKLOG["rules"]["resolved_zero_delta_item_is_not_reopened_without_new_evidence"] is True
assert BACKLOG["rules"]["private_ppdr_operational_data_excluded"] is True

registry = REGISTRY.read_text(encoding="utf-8")
assert '/downloads/bretagne/radiopack-france-bretagne-v0.2.csv' in registry
assert '/downloads/bretagne/radiopack-france-bretagne-v0.3.csv' not in registry
assert 'memoryCount: 151' in registry

print("Sprint 81 Bretagne v0.3 initialization remains auditable after later zero-delta revalidations: immutable public v0.2=151, AIRAC transition guarded, no public v0.3 OK")
