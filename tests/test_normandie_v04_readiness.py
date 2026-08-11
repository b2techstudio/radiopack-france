import csv
import importlib.util
import io
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
F5ZHA_PLAN = ROOT / "research/normandie-v0.4/f5zha-mortain-validation.json"
F5ZHA_BUILDER = ROOT / "tools/build_normandie_v04_f5zha_validation_pack.py"
READINESS_BUILDER = ROOT / "tools/build_normandie_v04_readiness_report.py"
SCENARIO_BUILDER = ROOT / "tools/build_normandie_v04_promotion_scenarios.py"

for path in (F5ZHA_PLAN, F5ZHA_BUILDER, READINESS_BUILDER, SCENARIO_BUILDER):
    assert path.is_file(), f"Missing expected file: {path}"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


f5zha = json.loads(F5ZHA_PLAN.read_text(encoding="utf-8"))
assert f5zha["schema_version"] == "1.1"
assert f5zha["status"] == "diagnostic_validation_pack_not_public"
assert f5zha["station"]["locator"] == "IN98OB86BQ"
assert f5zha["station"]["straight_line_distance_to_mortain_km"] == 65.6
assert f5zha["station"]["geometry_is_reception_proof"] is False
assert f5zha["current_authoritative_pair"]["side_a_mhz"] == 145.4675
assert f5zha["current_authoritative_pair"]["side_b_mhz"] == 432.575
assert f5zha["historical_conflict"]["conflicting_frequency_mhz"] == 431.4125
assert f5zha["historical_conflict"]["diagnostic_only"] is True
assert f5zha["validation"]["promotion_requires_both_useful_coverage_and_authoritative_source_reconciliation"] is True
assert f5zha["observations"] == []
assert f5zha["rules"]["tx_disabled"] is True
assert f5zha["rules"]["public_export_allowed"] is False
assert f5zha["rules"]["source_conflict_remains_open_until_authoritative_reconciliation"] is True

f5zha_builder = load_module("f5zha_builder", F5ZHA_BUILDER)
readiness_builder = load_module("readiness_builder", READINESS_BUILDER)
scenario_builder = load_module("scenario_builder", SCENARIO_BUILDER)

with tempfile.TemporaryDirectory(prefix="radiopack-f5zha-validation-") as tmp:
    json_path, csv_path, manifest = f5zha_builder.write_validation_pack(ROOT, Path(tmp))
    assert json_path.is_file() and csv_path.is_file()
    assert manifest["memory_count"] == 3
    assert manifest["public_export_allowed"] is False
    assert manifest["rules"]["source_conflict_closed"] is False
    rows = list(csv.DictReader(io.StringIO(csv_path.read_text(encoding="utf-8"))))
    assert [(row["Name"], row["Frequency"]) for row in rows] == [
        ("ZHA-VHF", "145.467500"),
        ("ZHA-UHF", "432.575000"),
        ("ZHA-OLD", "431.412500"),
    ]
    for row in rows:
        assert row["Duplex"] == "off"
        assert row["Offset"] == "0.000000"
        assert row["Tone"] == ""
        assert len(row["Name"]) <= 10

report = readiness_builder.build_report(ROOT)
assert report["schema_version"] == "1.0"
assert report["status"] == "normandie_v0_4_readiness_not_public"
assert report["current_internal_candidate_memory_count"] == 142
assert report["current_internal_candidate_new_memory_count"] == 3
assert report["known_blocked_frequency_count"] == 5
assert report["maximum_memory_count_if_all_current_known_gates_clear"] == 147
assert report["final_public_memory_count"] is None
assert report["f6zes_is_outside_known_gate_delta_until_frequency_resolved"] is True
assert report["all_known_gates_passed"] is False
assert report["public_export_allowed"] is False
assert report["public_release_ready"] is False
blockers = {item["id"]: item for item in report["blockers"]}
assert set(blockers) == {"R3_MORTAIN_RX", "F5ZHA_SOURCE_AND_COVERAGE", "F1ZOV_OPERATIONAL_STATUS"}
assert blockers["R3_MORTAIN_RX"]["memory_delta_if_cleared"] == 2
assert blockers["F5ZHA_SOURCE_AND_COVERAGE"]["memory_delta_if_cleared"] == 2
assert blockers["F1ZOV_OPERATIONAL_STATUS"]["memory_delta_if_cleared"] == 1
assert report["unresolved_priority"]["id"] == "F6ZES_SOURDEVAL"

with tempfile.TemporaryDirectory(prefix="radiopack-v04-readiness-") as tmp:
    json_path, md_path, written = readiness_builder.write_report(ROOT, Path(tmp))
    assert json_path.is_file() and md_path.is_file()
    assert written["public_release_ready"] is False
    text = md_path.read_text(encoding="utf-8")
    assert "142 mémoires" in text
    assert "147 mémoires" in text
    assert "Publication autorisée : **non**" in text

scenarios = scenario_builder.build_scenarios(ROOT)
assert scenarios["schema_version"] == "1.0"
assert scenarios["status"] == "promotion_scenarios_not_public"
assert scenarios["base_internal_candidate_memory_count"] == 142
assert scenarios["scenario_count"] == 8
assert scenarios["minimum_known_scenario_memory_count"] == 142
assert scenarios["maximum_known_scenario_memory_count"] == 147
assert scenarios["f6zes_excluded_from_scenario_counts_until_frequency_resolved"] is True
assert all(item["public_export_allowed"] is False for item in scenarios["scenarios"])
assert all(item["requires_explicit_final_review"] is True for item in scenarios["scenarios"])
counts = {item["candidate_memory_count_if_only_these_known_gates_clear"] for item in scenarios["scenarios"]}
assert counts == {142, 143, 144, 145, 146, 147}

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'version: "v0.4"' in registry
assert (ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv").exists()

print(
    "Tests Normandie v0.4 readiness: F5ZHA 3-memory RX-only diagnostic pack guarded, "
    "readiness stays non-public at 142 memories with known-gate ceiling 147, 8 promotion "
    "scenarios remain review-only, F6ZES unresolved and excluded from counts, OK"
)
