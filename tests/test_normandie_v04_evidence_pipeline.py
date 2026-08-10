import importlib.util
import json
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
F5ZHA = ROOT / "research/normandie-v0.4/f5zha-mortain-validation.json"
MATRIX = ROOT / "research/normandie-v0.4/external-evidence-matrix.json"
R3 = ROOT / "research/normandie-v0.4/r3-mortain-field-validation.json"
RECORDER = ROOT / "tools/record_normandie_v04_f5zha_observation.py"
EVIDENCE = ROOT / "tools/build_normandie_v04_evidence_report.py"
PROMOTION = ROOT / "tools/build_normandie_v04_internal_promotion_plan.py"

for path in (F5ZHA, MATRIX, R3, RECORDER, EVIDENCE, PROMOTION):
    assert path.is_file(), f"Missing expected file: {path}"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


f5zha = json.loads(F5ZHA.read_text(encoding="utf-8"))
assert f5zha["schema_version"] == "1.1"
assert f5zha["observations"] == []
assert f5zha["validation"]["promotion_requires_both_useful_coverage_and_authoritative_source_reconciliation"] is True
assert f5zha["rules"]["field_observations_never_close_source_conflict"] is True

matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
assert matrix["status"] == "current_external_evidence_matrix_not_public"
assert matrix["public_export_allowed"] is False
stations = {item["id"]: item for item in matrix["stations"]}
assert set(stations) == {"F1ZBX_R3", "F5ZHA_LAVAL", "F1ZOV_EQUEURDREVILLE", "F6ZES_SOURDEVAL"}
assert stations["F1ZBX_R3"]["operator_status_verified"] is True
assert stations["F5ZHA_LAVAL"]["current_frequencies_mhz"] == [145.4675, 432.575]
assert stations["F5ZHA_LAVAL"]["source_conflict_open"] is True
assert stations["F1ZOV_EQUEURDREVILLE"]["operator_status"] == "maintenance"
assert stations["F6ZES_SOURDEVAL"]["current_frequencies_mhz"] == []
assert all(item["promotion_to_internal_candidate_allowed"] is False for item in matrix["stations"])

recorder = load_module("f5zha_recorder", RECORDER)
evidence = load_module("evidence_report", EVIDENCE)
promotion = load_module("promotion_plan", PROMOTION)

with tempfile.TemporaryDirectory(prefix="radiopack-f5zha-recorder-") as tmp:
    temp_root = Path(tmp)
    research = temp_root / "research/normandie-v0.4"
    research.mkdir(parents=True)
    shutil.copy2(F5ZHA, research / F5ZHA.name)

    observation = {
        "date_local": "2026-08-10",
        "time_local": "17:30",
        "location_description": "Mortain synthetic test fixture",
        "receiver_model": "Quansheng UV-K5 test fixture",
        "antenna_description": "test antenna",
        "frequency_mhz": 145.4675,
        "signal_detected": True,
        "identification_confidence": "confirmed",
        "intelligibility_0_to_5": 4,
        "signal_strength_observation": "repeatable",
        "notes": "synthetic test only",
    }
    assert recorder.append_observation(temp_root, observation) == 1
    saved = json.loads((research / F5ZHA.name).read_text(encoding="utf-8"))
    assert saved["observations"][0]["frequency_mhz"] == 145.4675
    assert saved["observations"][0]["can_close_source_conflict"] is False
    assert saved["observations"][0]["diagnostic_only"] is False

    legacy = dict(observation)
    legacy.update({
        "time_local": "18:00",
        "frequency_mhz": 431.4125,
        "identification_confidence": "low",
        "intelligibility_0_to_5": 1,
    })
    assert recorder.append_observation(temp_root, legacy) == 2
    saved = json.loads((research / F5ZHA.name).read_text(encoding="utf-8"))
    assert saved["observations"][1]["diagnostic_only"] is True
    assert saved["observations"][1]["can_close_source_conflict"] is False

    invalid = dict(observation)
    invalid["frequency_mhz"] = 433.0
    try:
        recorder.validate_observation(temp_root, invalid)
    except ValueError:
        pass
    else:
        raise AssertionError("Recorder accepted a frequency outside the F5ZHA diagnostic pack")

report = evidence.build_report(ROOT)
assert report["status"] == "normandie_v0_4_evidence_report_not_public"
assert report["public_export_allowed"] is False
assert report["stations"]["F1ZBX_R3"]["field_gate_supported"] is False
assert report["stations"]["F5ZHA_LAVAL"]["field_coverage_supported"] is False
assert report["stations"]["F5ZHA_LAVAL"]["authoritative_source_reconciled"] is False
assert report["stations"]["F5ZHA_LAVAL"]["promotion_prerequisites_satisfied"] is False
assert report["stations"]["F1ZOV_EQUEURDREVILLE"]["maintenance_cleared"] is False
assert report["stations"]["F6ZES_SOURDEVAL"]["frequency_resolved"] is False

with tempfile.TemporaryDirectory(prefix="radiopack-v04-evidence-report-") as tmp:
    json_path, md_path, written = evidence.write_report(ROOT, Path(tmp))
    assert json_path.is_file() and md_path.is_file()
    assert written["public_export_allowed"] is False
    assert "ne modifie aucune porte" in md_path.read_text(encoding="utf-8")

plan = promotion.build_plan(ROOT)
assert plan["status"] == "guarded_internal_promotion_plan_not_public"
assert plan["current_internal_candidate_memory_count"] == 142
assert plan["eligible_addition_count"] == 0
assert plan["candidate_memory_count_if_plan_applied_in_future"] == 142
assert plan["additions"] == []
assert plan["plan_applied"] is False
assert plan["internal_candidate_mutated"] is False
assert plan["public_export_allowed"] is False
assert all(value is False for value in plan["gate_status"].values())

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'version: "v0.4"' not in registry

print(
    "Tests Normandie v0.4 evidence pipeline: F5ZHA observations recorded safely without source reconciliation, "
    "external evidence matrix keeps all gates closed, consolidated report stays non-public, guarded promotion "
    "plan has 0 eligible additions and leaves the 142-memory candidate untouched, OK"
)
