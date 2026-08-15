import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = json.loads((ROOT / "research/normandie-v0.5/field-validation-kit.json").read_text(encoding="utf-8"))
POLICY = json.loads((ROOT / "research/normandie-v0.5/field-evaluation-policy.json").read_text(encoding="utf-8"))
EVALUATOR = ROOT / "tools/evaluate_normandie_v05_field_sessions.py"
COLUMNS = KIT["session_log_columns"]


def make_row(
    session_id: str,
    target: str,
    frequency: float,
    *,
    detected: str = "yes",
    confidence: str = "high",
    intelligibility: str = "4",
    date: str = "2026-08-15",
    time: str = "10:00",
    location: str = "Mortain-Bocage centre",
    receiver: str = "Quansheng UV-K5",
    antenna: str = "antenne fouet",
    strength: str = "S3",
    notes: str = "",
) -> dict[str, str]:
    return {
        "session_id": session_id,
        "target": target,
        "date_local": date,
        "time_local": time,
        "location_description": location,
        "receiver_model": receiver,
        "antenna_description": antenna,
        "frequency_mhz": f"{frequency:.6f}",
        "signal_detected": detected,
        "identification_confidence": confidence,
        "intelligibility_0_to_5": intelligibility,
        "signal_strength_observation": strength,
        "notes": notes,
    }


def evaluate(rows: list[dict[str, str]]) -> dict:
    with tempfile.TemporaryDirectory(prefix="radiopack-s85-eval-") as td:
        root = Path(td)
        input_path = root / "sessions.csv"
        output_path = root / "report.json"
        with input_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=COLUMNS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        result = subprocess.run(
            [
                sys.executable,
                str(EVALUATOR),
                "--root",
                str(ROOT),
                "--input",
                str(input_path),
                "--output",
                str(output_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        report = json.loads(output_path.read_text(encoding="utf-8"))
        assert json.loads(result.stdout) == report
        return report


assert POLICY["status"] == "field_evaluation_policy_not_public"
assert POLICY["target_version"] == "0.5" and POLICY["sprint"] == 85
assert POLICY["output_rules"]["promotion_ready_is_always_false"] is True
assert POLICY["output_rules"]["automatic_candidate_mutation_allowed"] is False
assert POLICY["output_rules"]["automatic_publication_allowed"] is False
assert POLICY["output_rules"]["field_non_reception_is_negative_operational_evidence"] is False
assert POLICY["output_rules"]["legacy_probe_can_close_source_conflict"] is False

empty = evaluate([])
assert empty["gate_results"]["R3_MORTAIN_RX"]["verdict"] == "indeterminate"
assert empty["gate_results"]["F5ZHA_SOURCE_AND_COVERAGE"]["verdict"] == "indeterminate"
assert empty["promotion_ready"] is False and empty["candidate_memory_delta"] == 0

r3_one = evaluate([make_row("R3-A", "R3_MORTAIN_RX", 145.675)])
assert r3_one["gate_results"]["R3_MORTAIN_RX"]["verdict"] == "insufficient"
assert r3_one["gate_results"]["R3_MORTAIN_RX"]["qualifying_session_count"] == 1

r3_two = evaluate(
    [
        make_row("R3-A", "R3_MORTAIN_RX", 145.675, date="2026-08-15", time="10:00"),
        make_row("R3-B", "R3_MORTAIN_RX", 145.675, confidence="confirmed", intelligibility="2", date="2026-08-16", time="18:30"),
        make_row("R3-B", "R3_MORTAIN_RX", 145.075, detected="no", confidence="", intelligibility="", date="2026-08-16", time="18:30"),
    ]
)
r3_result = r3_two["gate_results"]["R3_MORTAIN_RX"]
assert r3_result["verdict"] == "satisfied"
assert r3_result["qualifying_session_ids"] == ["R3-A", "R3-B"]
assert r3_result["optional_input_observation_count"] == 1
assert r3_result["if_field_gate_satisfied_pair_memory_delta"] == 2

r3_same_session = evaluate(
    [
        make_row("R3-ONE", "R3_MORTAIN_RX", 145.675),
        make_row("R3-ONE", "R3_MORTAIN_RX", 145.675, notes="second row, same session"),
    ]
)
assert r3_same_session["gate_results"]["R3_MORTAIN_RX"]["verdict"] == "insufficient"
assert r3_same_session["gate_results"]["R3_MORTAIN_RX"]["qualifying_session_count"] == 1

r3_weak = evaluate(
    [
        make_row("R3-W1", "R3_MORTAIN_RX", 145.675, confidence="high", intelligibility="2"),
        make_row("R3-W2", "R3_MORTAIN_RX", 145.675, confidence="low", intelligibility="5", date="2026-08-16"),
    ]
)
assert r3_weak["gate_results"]["R3_MORTAIN_RX"]["verdict"] == "insufficient"
assert r3_weak["gate_results"]["R3_MORTAIN_RX"]["qualifying_session_count"] == 0

zha_two_same_side = evaluate(
    [
        make_row("ZHA-A", "F5ZHA_SOURCE_AND_COVERAGE", 145.4675, date="2026-08-15", time="11:00"),
        make_row("ZHA-B", "F5ZHA_SOURCE_AND_COVERAGE", 145.4675, confidence="unmistakable", intelligibility="3", date="2026-08-16", time="19:00"),
    ]
)
zha_result = zha_two_same_side["gate_results"]["F5ZHA_SOURCE_AND_COVERAGE"]
assert zha_result["verdict"] == "satisfied"
assert zha_result["qualifying_session_count"] == 2
assert zha_result["qualifying_current_pair_frequencies_mhz"] == [145.4675]
assert zha_result["both_current_pair_sides_observed"] is False
assert zha_result["both_current_pair_sides_required"] is False
assert zha_result["source_conflict_closed_by_field_evidence"] is False

zha_both_sides = evaluate(
    [
        make_row("ZHA-C", "F5ZHA_SOURCE_AND_COVERAGE", 145.4675, date="2026-08-17", time="09:00"),
        make_row("ZHA-D", "F5ZHA_SOURCE_AND_COVERAGE", 432.575, confidence="confirmed", intelligibility="5", date="2026-08-18", time="20:00"),
    ]
)
assert zha_both_sides["gate_results"]["F5ZHA_SOURCE_AND_COVERAGE"]["verdict"] == "satisfied"
assert zha_both_sides["gate_results"]["F5ZHA_SOURCE_AND_COVERAGE"]["both_current_pair_sides_observed"] is True

zha_legacy_only = evaluate(
    [
        make_row("OLD-A", "F5ZHA_SOURCE_AND_COVERAGE", 431.4125),
        make_row("OLD-B", "F5ZHA_SOURCE_AND_COVERAGE", 431.4125, date="2026-08-16"),
    ]
)
legacy_result = zha_legacy_only["gate_results"]["F5ZHA_SOURCE_AND_COVERAGE"]
assert legacy_result["verdict"] == "indeterminate"
assert legacy_result["legacy_probe_observation_count"] == 2
assert legacy_result["legacy_probe_counts_for_gate"] is False
assert legacy_result["qualifying_session_count"] == 0

zha_non_detection = evaluate(
    [
        make_row("ZHA-N1", "F5ZHA_SOURCE_AND_COVERAGE", 145.4675, detected="no", confidence="", intelligibility=""),
        make_row("ZHA-N2", "F5ZHA_SOURCE_AND_COVERAGE", 432.575, detected="no", confidence="", intelligibility="", date="2026-08-16"),
    ]
)
non_detection_result = zha_non_detection["gate_results"]["F5ZHA_SOURCE_AND_COVERAGE"]
assert non_detection_result["verdict"] == "insufficient"
assert non_detection_result["non_detection_observation_count"] == 2
assert non_detection_result["operational_negative_evidence"] is False

control_only = evaluate([make_row("CTRL-1", "CONTROL", 145.6875)])
assert control_only["control"]["observation_count"] == 1
assert control_only["control"]["counts_for_any_gate"] is False
assert control_only["gate_results"]["R3_MORTAIN_RX"]["verdict"] == "indeterminate"
assert control_only["gate_results"]["F5ZHA_SOURCE_AND_COVERAGE"]["verdict"] == "indeterminate"

inconsistent = evaluate(
    [
        make_row("SAME", "R3_MORTAIN_RX", 145.675, location="Mortain centre"),
        make_row("SAME", "R3_MORTAIN_RX", 145.675, location="Mortain hauteur"),
    ]
)
assert "SAME" in inconsistent["input_summary"]["inconsistent_session_ids"]
assert inconsistent["gate_results"]["R3_MORTAIN_RX"]["verdict"] == "indeterminate"

with tempfile.TemporaryDirectory(prefix="radiopack-s85-bad-schema-") as td:
    bad = Path(td) / "bad.csv"
    bad.write_text("session_id,target\nX,R3_MORTAIN_RX\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(EVALUATOR), "--root", str(ROOT), "--input", str(bad)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "missing required columns" in result.stderr

assert not (ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.5.csv").exists()
registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert "radiopack-france-normandie-v0.4.csv" in registry
assert "radiopack-france-normandie-v0.5.csv" not in registry

print("Sprint 85 Normandie v0.5: field-session evaluator classifies R3/F5ZHA gates reproducibly, ignores diagnostics for promotion, never auto-mutates or publishes OK")
