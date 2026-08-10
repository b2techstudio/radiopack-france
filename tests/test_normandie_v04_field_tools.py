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
assert resume["current_sprint"] == 39
assert resume["state_version"] == "0.21.28"
assert resume["public_packs"]["normandie"]["memory_count"] == 139
assert resume["active_work"]["internal_candidate_memory_count"] == 142
assert resume["active_work"]["blocked_frequency_count"] == 5
assert resume["active_work"]["maximum_internal_memory_count_if_all_current_known_gates_clear"] == 147
assert resume["active_work"]["public_export_allowed"] is False
assert resume["active_work"]["public_release_ready"] is False
assert resume["resume_rules"]["published_versions_are_immutable"] is True
assert resume["resume_rules"]["geometry_is_not_reception_proof"] is True

status_text = STATUS_DOC.read_text(encoding="utf-8")
assert "Sprint courant : **39**" in status_text
assert "État logique : **0.21.28**" in status_text
assert "python tools\\run_normandie_v04_checks.py" in status_text
assert "147 mémoires" in status_text

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
    no_signal.update({
        "frequency_mhz": 145.075,
        "signal_detected": False,
        "identification_confidence": "none",
        "intelligibility_0_to_5": 0,
    })
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
    "non-public, recovery state is self-contained at sprint 39, OK"
)
