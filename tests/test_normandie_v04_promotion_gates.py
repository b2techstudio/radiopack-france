import csv
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATES_PATH = ROOT / "research/normandie-v0.4/promotion-gates.json"
FIELD_PATH = ROOT / "research/normandie-v0.4/r3-mortain-field-validation.json"
PACK_PATH = ROOT / "research/normandie-v0.4/r3-validation-pack.json"
INTERNAL_MAP_PATH = ROOT / "research/normandie-v0.4/internal-candidate-map.json"
BUILDER = ROOT / "tools/build_normandie_v04_r3_validation_pack.py"
CHECKER = ROOT / "tools/check_normandie_v04_promotion_gates.py"

for path in (GATES_PATH, FIELD_PATH, PACK_PATH, INTERNAL_MAP_PATH, BUILDER, CHECKER):
    assert path.is_file(), f"Missing expected file: {path}"

gates = json.loads(GATES_PATH.read_text(encoding="utf-8"))
field = json.loads(FIELD_PATH.read_text(encoding="utf-8"))
pack = json.loads(PACK_PATH.read_text(encoding="utf-8"))
internal_map = json.loads(INTERNAL_MAP_PATH.read_text(encoding="utf-8"))

assert gates["schema_version"] == "1.0"
assert gates["status"] == "promotion_gates_defined_not_public"
assert gates["current_internal_candidate_memory_count"] == 142
assert gates["current_internal_candidate_new_memory_count"] == 3
assert gates["blocked_frequency_count"] == 5
assert gates["rules"]["public_export_allowed"] is False
assert gates["rules"]["tx_disabled"] is True
assert gates["rules"]["chirp_duplex"] == "off"
assert gates["rules"]["chirp_offset"] == "0.000000"

gate_by_id = {gate["id"]: gate for gate in gates["gates"]}
assert set(gate_by_id) == {"R3_MORTAIN_RX", "F5ZHA_SOURCE_AND_COVERAGE", "F1ZOV_OPERATIONAL_STATUS"}
assert gate_by_id["R3_MORTAIN_RX"]["frequencies_mhz"] == [145.075, 145.675]
assert gate_by_id["R3_MORTAIN_RX"]["promotion_requirements"]["minimum_independent_sessions"] == 2
assert gate_by_id["R3_MORTAIN_RX"]["promotion_to_internal_candidate_allowed"] is False
assert gate_by_id["F5ZHA_SOURCE_AND_COVERAGE"]["frequencies_mhz"] == [145.4675, 432.575]
assert gate_by_id["F5ZHA_SOURCE_AND_COVERAGE"]["promotion_to_internal_candidate_allowed"] is False
assert gate_by_id["F1ZOV_OPERATIONAL_STATUS"]["frequencies_mhz"] == [431.975]
assert gate_by_id["F1ZOV_OPERATIONAL_STATUS"]["promotion_to_internal_candidate_allowed"] is False

assert pack["schema_version"] == "1.0"
assert pack["status"] == "field_validation_pack_not_public"
assert pack["rules"]["public_export_allowed"] is False
assert pack["rules"]["tx_disabled"] is True
assert pack["validation"]["primary_probe_mhz"] == 145.675
assert pack["validation"]["minimum_independent_sessions"] == 2
assert [(item["location"], item["name"], item["frequency_mhz"]) for item in pack["memories"]] == [
    (0, "R3-OUT", 145.675),
    (1, "R3-IN", 145.075),
    (2, "CTRL-ZHY", 145.6875),
]
assert all(len(item["name"]) <= 10 for item in pack["memories"])

excluded = {
    round(float(freq), 6)
    for group in internal_map["excluded_from_internal_candidate"]
    for freq in group["frequencies_mhz"]
}
assert excluded == {145.075, 145.675, 145.4675, 432.575, 431.975}

with tempfile.TemporaryDirectory(prefix="radiopack-r3-validation-") as tmp:
    out = Path(tmp) / "out"
    subprocess.run(
        [sys.executable, str(BUILDER), "--root", str(ROOT), "--output-dir", str(out)],
        check=True,
        capture_output=True,
        text=True,
    )
    csv_path = out / "r3-mortain-rx-validation.csv"
    json_path = out / "r3-mortain-rx-validation.json"
    assert csv_path.is_file() and json_path.is_file()
    with csv_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 3
    assert [row["Name"] for row in rows] == ["R3-OUT", "R3-IN", "CTRL-ZHY"]
    assert [row["Frequency"] for row in rows] == ["145.675000", "145.075000", "145.687500"]
    for row in rows:
        assert row["Duplex"] == "off"
        assert row["Offset"] == "0.000000"
        assert row["Tone"] == ""
    manifest = json.loads(json_path.read_text(encoding="utf-8"))
    assert manifest["memory_count"] == 3
    assert manifest["public_export_allowed"] is False
    assert manifest["rules"]["tx_disabled"] is True
    assert manifest["rules"]["ctcss_rx_filter_enabled"] is False

spec = importlib.util.spec_from_file_location("promotion_checker", CHECKER)
assert spec and spec.loader
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
current = checker.evaluate(ROOT)
assert current["r3"]["passed"] is False
assert current["r3"]["valid_session_count"] == 0
assert current["f5zha"]["passed"] is False
assert current["f1zov"]["passed"] is False
assert current["all_blocked_gates_passed"] is False
assert current["public_export_allowed"] is False

with tempfile.TemporaryDirectory(prefix="radiopack-r3-gate-") as tmp:
    temp_root = Path(tmp)
    research = temp_root / "research/normandie-v0.4"
    research.mkdir(parents=True)
    shutil.copy2(GATES_PATH, research / "promotion-gates.json")
    simulated_field = json.loads(FIELD_PATH.read_text(encoding="utf-8"))
    simulated_field["observations"] = [
        {
            "date_local": "2026-08-10",
            "time_local": "10:00",
            "location_description": "Mortain centre",
            "receiver_model": "test",
            "antenna_description": "test",
            "frequency_mhz": 145.675,
            "signal_detected": True,
            "identification_confidence": "confirmed",
            "intelligibility_0_to_5": 4,
            "signal_strength_observation": "repeatable",
            "notes": "synthetic test fixture"
        },
        {
            "date_local": "2026-08-11",
            "time_local": "18:00",
            "location_description": "Mortain elevated location",
            "receiver_model": "test",
            "antenna_description": "test",
            "frequency_mhz": 145.675,
            "signal_detected": True,
            "identification_confidence": "high",
            "intelligibility_0_to_5": 3,
            "signal_strength_observation": "repeatable",
            "notes": "synthetic test fixture"
        }
    ]
    (research / "r3-mortain-field-validation.json").write_text(
        json.dumps(simulated_field, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    simulated = checker.evaluate(temp_root)
    assert simulated["r3"]["passed"] is True
    assert simulated["r3"]["valid_session_count"] == 2
    assert simulated["f5zha"]["passed"] is False
    assert simulated["f1zov"]["passed"] is False
    assert simulated["all_blocked_gates_passed"] is False

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'version: "v0.4"' in registry
assert (ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv").exists()

print("Tests Normandie v0.4 promotion gates: 5 blocked frequencies remain excluded, R3 standalone 3-memory RX-only validation pack builds safely, two independent confirmed sessions are required, F5ZHA/F1ZOV remain source-gated, no public mutation OK")
