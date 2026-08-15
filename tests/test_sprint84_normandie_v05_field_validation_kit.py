import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = json.loads((ROOT / "research/normandie-v0.5/field-validation-kit.json").read_text(encoding="utf-8"))
PUBLIC_V04 = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv"
PUBLIC_V05 = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.5.csv"
REGISTRY = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
BUILDER = ROOT / "tools/build_normandie_v05_field_validation_kit.py"

assert KIT["status"] == "field_validation_kit_not_public"
assert KIT["sprint"] == 84 and KIT["target_version"] == "0.5"
assert KIT["candidate_memory_count_before"] == 142
assert KIT["candidate_memory_count_after"] == 142
assert KIT["candidate_memory_delta"] == 0
assert KIT["public_export_allowed"] is False
assert len(KIT["memories"]) == 6

memories = {item["name"]: item for item in KIT["memories"]}
assert set(memories) == {"R3-OUT", "R3-IN", "ZHA-VHF", "ZHA-UHF", "ZHA-OLD", "CTRL-ZHY"}
assert memories["R3-OUT"]["frequency_mhz"] == 145.675
assert memories["R3-IN"]["frequency_mhz"] == 145.075
assert memories["ZHA-VHF"]["frequency_mhz"] == 145.4675
assert memories["ZHA-UHF"]["frequency_mhz"] == 432.575
assert memories["ZHA-OLD"]["frequency_mhz"] == 431.4125 and memories["ZHA-OLD"]["diagnostic_only"] is True
assert memories["CTRL-ZHY"]["frequency_mhz"] == 145.6875 and memories["CTRL-ZHY"]["diagnostic_only"] is True
assert len({item["location"] for item in KIT["memories"]}) == 6
assert len({item["frequency_mhz"] for item in KIT["memories"]}) == 6
assert all(len(item["name"]) <= 10 for item in KIT["memories"])

r3 = KIT["gates"]["R3_MORTAIN_RX"]
assert r3["primary_probe_mhz"] == 145.675
assert r3["minimum_independent_sessions"] == 2
assert r3["repeatable_identified_reception_required"] is True
assert r3["single_weak_carrier_is_sufficient"] is False
assert r3["input_probe_is_optional_for_coverage_gate"] is True
assert r3["if_gate_clears_pair_memory_delta"] == 2

zha = KIT["gates"]["F5ZHA_SOURCE_AND_COVERAGE"]
assert zha["current_pair_mhz"] == [145.4675, 432.575]
assert zha["legacy_conflict_probe_mhz"] == 431.4125
assert zha["minimum_independent_sessions"] == 2
assert zha["minimum_intelligibility_0_to_5"] == 3
assert zha["legacy_probe_is_promotion_evidence"] is False
assert zha["field_non_reception_is_negative_operational_evidence"] is False
assert zha["if_gate_clears_pair_memory_delta"] == 2

rules = KIT["rules"]
assert rules["chirp_duplex"] == "off" and rules["chirp_offset"] == "0.000000"
assert rules["tx_disabled"] is True and rules["ctcss_rx_filter_enabled"] is False
assert rules["field_sessions_are_evidence_not_memories"] is True
assert rules["web_research_cannot_satisfy_field_gate"] is True
assert rules["published_v0_4_immutable"] is True

with tempfile.TemporaryDirectory(prefix="radiopack-normandie-v05-field-") as td:
    subprocess.run(
        [sys.executable, str(BUILDER), "--root", str(ROOT), "--output-dir", td],
        check=True,
    )
    out = Path(td)
    chirp_path = out / "normandie-v0.5-field-rx.csv"
    log_path = out / "normandie-v0.5-field-session-template.csv"
    manifest_path = out / "normandie-v0.5-field-kit-manifest.json"
    assert chirp_path.is_file() and log_path.is_file() and manifest_path.is_file()

    with chirp_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 6
    assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
    assert all(row["Tone"] == "" for row in rows)
    assert len({row["Frequency"] for row in rows}) == 6
    assert [row["Name"] for row in rows] == ["R3-OUT", "R3-IN", "ZHA-VHF", "ZHA-UHF", "ZHA-OLD", "CTRL-ZHY"]

    with log_path.open(encoding="utf-8", newline="") as handle:
        log_rows = list(csv.reader(handle))
    assert len(log_rows) == 1
    assert log_rows[0] == KIT["session_log_columns"]

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["status"] == "field_validation_kit_built_not_public"
    assert manifest["memory_count"] == 6
    assert manifest["candidate_memory_count"] == 142
    assert manifest["candidate_memory_delta"] == 0
    assert manifest["public_export_allowed"] is False

assert PUBLIC_V04.is_file() and not PUBLIC_V05.exists()
assert "/downloads/normandie/radiopack-france-normandie-v0.4.csv" in REGISTRY
assert "/downloads/normandie/radiopack-france-normandie-v0.5.csv" not in REGISTRY

print("Sprint 84 Normandie v0.5 field kit: 6 RX diagnostic memories + empty session log template, candidate remains 142, no public mutation OK")
