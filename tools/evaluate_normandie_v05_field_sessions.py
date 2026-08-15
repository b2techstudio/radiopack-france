#!/usr/bin/env python3
"""Evaluate Normandie v0.5 field-session CSV evidence without promoting or publishing anything."""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KIT_PATH = Path("research/normandie-v0.5/field-validation-kit.json")
POLICY_PATH = Path("research/normandie-v0.5/field-evaluation-policy.json")

R3_TARGET = "R3_MORTAIN_RX"
ZHA_TARGET = "F5ZHA_SOURCE_AND_COVERAGE"
CONTROL_TARGET = "CONTROL"
ALLOWED_TARGETS = {R3_TARGET, ZHA_TARGET, CONTROL_TARGET}
FREQ_TOLERANCE_MHZ = 0.000001


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def normalize(value: str | None) -> str:
    return (value or "").strip().lower()


def parse_bool(value: str, policy: dict[str, Any]) -> bool:
    normalized = normalize(value)
    accepted_true = set(policy["input"]["accepted_boolean_true"])
    accepted_false = set(policy["input"]["accepted_boolean_false"])
    if normalized in accepted_true:
        return True
    if normalized in accepted_false:
        return False
    raise ValueError(f"invalid boolean value {value!r}")


def parse_frequency(value: str) -> float:
    try:
        return float(value.strip().replace(",", "."))
    except Exception as exc:  # pragma: no cover - exact exception type is not important here
        raise ValueError(f"invalid frequency {value!r}") from exc


def parse_intelligibility(value: str) -> int:
    try:
        score = int(value.strip())
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"invalid intelligibility {value!r}") from exc
    if not 0 <= score <= 5:
        raise ValueError(f"intelligibility outside 0..5: {score}")
    return score


def freq_matches(value: float, expected: float) -> bool:
    return abs(value - expected) <= FREQ_TOLERANCE_MHZ


def validate_configuration(root: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    kit = load_json(root / KIT_PATH)
    policy = load_json(root / POLICY_PATH)
    if kit["status"] != "field_validation_kit_not_public":
        raise ValueError("Unexpected Normandie field-kit status")
    if policy["status"] != "field_evaluation_policy_not_public":
        raise ValueError("Unexpected Normandie field-evaluation policy status")
    if kit["target_version"] != "0.5" or policy["target_version"] != "0.5":
        raise ValueError("Unexpected Normandie target version")
    if kit["public_export_allowed"] is not False:
        raise ValueError("Field kit must remain non-public")
    if policy["output_rules"]["automatic_publication_allowed"] is not False:
        raise ValueError("Evaluator must never allow automatic publication")
    if policy["output_rules"]["automatic_candidate_mutation_allowed"] is not False:
        raise ValueError("Evaluator must never mutate the candidate automatically")

    r3_kit = kit["gates"][R3_TARGET]
    r3_policy = policy["gates"][R3_TARGET]
    if r3_kit["primary_probe_mhz"] != r3_policy["primary_frequency_mhz"]:
        raise ValueError("R3 primary frequency drift between kit and policy")
    if r3_kit["minimum_independent_sessions"] != r3_policy["minimum_independent_sessions"]:
        raise ValueError("R3 minimum-session drift between kit and policy")

    zha_kit = kit["gates"][ZHA_TARGET]
    zha_policy = policy["gates"][ZHA_TARGET]
    if zha_kit["current_pair_mhz"] != zha_policy["current_pair_mhz"]:
        raise ValueError("F5ZHA current-pair drift between kit and policy")
    if zha_kit["legacy_conflict_probe_mhz"] != zha_policy["legacy_conflict_probe_mhz"]:
        raise ValueError("F5ZHA legacy-probe drift between kit and policy")
    if zha_kit["minimum_independent_sessions"] != zha_policy["minimum_independent_sessions"]:
        raise ValueError("F5ZHA minimum-session drift between kit and policy")
    return kit, policy


def validate_headers(fieldnames: list[str] | None, required: list[str]) -> None:
    if not fieldnames:
        raise ValueError("CSV has no header")
    missing = [name for name in required if name not in fieldnames]
    if missing:
        raise ValueError("CSV missing required columns: " + ", ".join(missing))


def row_frequency_allowed(target: str, frequency: float, policy: dict[str, Any]) -> bool:
    if target == R3_TARGET:
        r3 = policy["gates"][R3_TARGET]
        return freq_matches(frequency, float(r3["primary_frequency_mhz"])) or freq_matches(
            frequency, float(r3["optional_input_frequency_mhz"])
        )
    if target == ZHA_TARGET:
        zha = policy["gates"][ZHA_TARGET]
        return any(freq_matches(frequency, float(item)) for item in zha["current_pair_mhz"]) or freq_matches(
            frequency, float(zha["legacy_conflict_probe_mhz"])
        )
    if target == CONTROL_TARGET:
        return freq_matches(frequency, 145.6875)
    return False


def parse_rows(input_path: Path, kit: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    required_columns = list(kit["session_log_columns"])
    required_metadata = set(policy["input"]["required_session_metadata"])
    normalized_rows: list[dict[str, Any]] = []
    row_errors: list[dict[str, Any]] = []
    session_signatures: dict[str, set[tuple[str, ...]]] = defaultdict(set)

    with input_path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        validate_headers(reader.fieldnames, required_columns)
        for row_number, raw in enumerate(reader, start=2):
            cleaned = {key: (raw.get(key) or "").strip() for key in required_columns}
            try:
                missing_metadata = sorted(key for key in required_metadata if not cleaned[key])
                if missing_metadata:
                    raise ValueError("missing required values: " + ", ".join(missing_metadata))

                target = cleaned["target"]
                if target not in ALLOWED_TARGETS:
                    raise ValueError(f"unknown target {target!r}")

                frequency = parse_frequency(cleaned["frequency_mhz"])
                if not row_frequency_allowed(target, frequency, policy):
                    raise ValueError(f"frequency {frequency:.6f} is not valid for target {target}")

                signal_detected = parse_bool(cleaned["signal_detected"], policy)
                confidence = normalize(cleaned["identification_confidence"])
                intelligibility: int | None = None
                if cleaned["intelligibility_0_to_5"]:
                    intelligibility = parse_intelligibility(cleaned["intelligibility_0_to_5"])
                if signal_detected:
                    if not confidence:
                        raise ValueError("signal detected but identification_confidence is empty")
                    if intelligibility is None:
                        raise ValueError("signal detected but intelligibility_0_to_5 is empty")

                signature = (
                    cleaned["date_local"],
                    cleaned["time_local"],
                    cleaned["location_description"],
                    cleaned["receiver_model"],
                    cleaned["antenna_description"],
                )
                session_signatures[cleaned["session_id"]].add(signature)
                normalized_rows.append(
                    {
                        "row_number": row_number,
                        "session_id": cleaned["session_id"],
                        "target": target,
                        "date_local": cleaned["date_local"],
                        "time_local": cleaned["time_local"],
                        "location_description": cleaned["location_description"],
                        "receiver_model": cleaned["receiver_model"],
                        "antenna_description": cleaned["antenna_description"],
                        "frequency_mhz": frequency,
                        "signal_detected": signal_detected,
                        "identification_confidence": confidence,
                        "intelligibility_0_to_5": intelligibility,
                        "signal_strength_observation": cleaned["signal_strength_observation"],
                        "notes": cleaned["notes"],
                    }
                )
            except ValueError as exc:
                row_errors.append({"row_number": row_number, "error": str(exc)})

    inconsistent_session_ids = sorted(
        session_id for session_id, signatures in session_signatures.items() if len(signatures) > 1
    )
    if inconsistent_session_ids:
        for session_id in inconsistent_session_ids:
            row_errors.append(
                {
                    "session_id": session_id,
                    "error": "same session_id has inconsistent date/time/location/receiver/antenna metadata",
                }
            )
    valid_rows = [row for row in normalized_rows if row["session_id"] not in inconsistent_session_ids]
    return {
        "source_row_count": len(normalized_rows) + len([item for item in row_errors if "row_number" in item]),
        "parsed_row_count": len(normalized_rows),
        "valid_row_count": len(valid_rows),
        "row_errors": row_errors,
        "inconsistent_session_ids": inconsistent_session_ids,
        "rows": valid_rows,
    }


def evaluate_r3(rows: list[dict[str, Any]], policy: dict[str, Any]) -> dict[str, Any]:
    gate = policy["gates"][R3_TARGET]
    primary = float(gate["primary_frequency_mhz"])
    input_freq = float(gate["optional_input_frequency_mhz"])
    accepted = set(gate["accepted_identification_confidence"])
    min_intelligibility = int(gate["high_confidence_requires_minimum_intelligibility_0_to_5"])

    primary_rows = [
        row for row in rows if row["target"] == R3_TARGET and freq_matches(row["frequency_mhz"], primary)
    ]
    input_rows = [
        row for row in rows if row["target"] == R3_TARGET and freq_matches(row["frequency_mhz"], input_freq)
    ]
    qualifying_rows: list[dict[str, Any]] = []
    for row in primary_rows:
        if not row["signal_detected"]:
            continue
        confidence = row["identification_confidence"]
        intelligibility = row["intelligibility_0_to_5"]
        if confidence not in accepted or intelligibility is None:
            continue
        if confidence in {"unmistakable", "confirmed"} or (
            confidence == "high" and intelligibility >= min_intelligibility
        ):
            qualifying_rows.append(row)

    qualifying_session_ids = sorted({row["session_id"] for row in qualifying_rows})
    minimum = int(gate["minimum_independent_sessions"])
    if len(qualifying_session_ids) >= minimum:
        verdict = "satisfied"
    elif primary_rows:
        verdict = "insufficient"
    else:
        verdict = "indeterminate"

    return {
        "verdict": verdict,
        "primary_frequency_mhz": primary,
        "minimum_independent_sessions": minimum,
        "valid_primary_observation_count": len(primary_rows),
        "qualifying_session_ids": qualifying_session_ids,
        "qualifying_session_count": len(qualifying_session_ids),
        "non_detection_observation_count": sum(not row["signal_detected"] for row in primary_rows),
        "optional_input_observation_count": len(input_rows),
        "optional_input_detected_session_ids": sorted(
            {row["session_id"] for row in input_rows if row["signal_detected"]}
        ),
        "field_gate_satisfied": verdict == "satisfied",
        "if_field_gate_satisfied_pair_memory_delta": int(gate["if_field_gate_satisfied_pair_memory_delta"]),
        "operational_negative_evidence": False,
    }


def evaluate_zha(rows: list[dict[str, Any]], policy: dict[str, Any]) -> dict[str, Any]:
    gate = policy["gates"][ZHA_TARGET]
    current_pair = [float(item) for item in gate["current_pair_mhz"]]
    legacy = float(gate["legacy_conflict_probe_mhz"])
    accepted = set(gate["accepted_identification_confidence"])
    min_intelligibility = int(gate["minimum_intelligibility_0_to_5"])

    current_rows = [
        row
        for row in rows
        if row["target"] == ZHA_TARGET
        and any(freq_matches(row["frequency_mhz"], item) for item in current_pair)
    ]
    legacy_rows = [
        row
        for row in rows
        if row["target"] == ZHA_TARGET and freq_matches(row["frequency_mhz"], legacy)
    ]
    qualifying_rows = [
        row
        for row in current_rows
        if row["signal_detected"]
        and row["identification_confidence"] in accepted
        and row["intelligibility_0_to_5"] is not None
        and row["intelligibility_0_to_5"] >= min_intelligibility
    ]
    qualifying_session_ids = sorted({row["session_id"] for row in qualifying_rows})
    heard_frequencies = sorted(
        {
            round(row["frequency_mhz"], 6)
            for row in qualifying_rows
            if any(freq_matches(row["frequency_mhz"], item) for item in current_pair)
        }
    )
    minimum = int(gate["minimum_independent_sessions"])
    if len(qualifying_session_ids) >= minimum:
        verdict = "satisfied"
    elif current_rows:
        verdict = "insufficient"
    else:
        verdict = "indeterminate"

    return {
        "verdict": verdict,
        "current_pair_mhz": current_pair,
        "legacy_conflict_probe_mhz": legacy,
        "minimum_independent_sessions": minimum,
        "valid_current_pair_observation_count": len(current_rows),
        "qualifying_session_ids": qualifying_session_ids,
        "qualifying_session_count": len(qualifying_session_ids),
        "qualifying_current_pair_frequencies_mhz": heard_frequencies,
        "both_current_pair_sides_observed": all(
            any(freq_matches(heard, expected) for heard in heard_frequencies) for expected in current_pair
        ),
        "both_current_pair_sides_required": bool(gate["both_current_pair_sides_must_be_heard_to_satisfy_field_gate"]),
        "legacy_probe_observation_count": len(legacy_rows),
        "legacy_probe_detected_session_ids": sorted(
            {row["session_id"] for row in legacy_rows if row["signal_detected"]}
        ),
        "legacy_probe_counts_for_gate": False,
        "non_detection_observation_count": sum(not row["signal_detected"] for row in current_rows),
        "field_gate_satisfied": verdict == "satisfied",
        "if_field_gate_satisfied_pair_memory_delta": int(gate["if_field_gate_satisfied_pair_memory_delta"]),
        "source_conflict_closed_by_field_evidence": False,
        "operational_negative_evidence": False,
    }


def evaluate_csv(root: Path, input_path: Path) -> dict[str, Any]:
    kit, policy = validate_configuration(root)
    parsed = parse_rows(input_path, kit, policy)
    rows = parsed.pop("rows")
    r3 = evaluate_r3(rows, policy)
    zha = evaluate_zha(rows, policy)
    control_rows = [row for row in rows if row["target"] == CONTROL_TARGET]

    return {
        "schema_version": "1.0",
        "status": "field_session_evaluation_not_public",
        "pack": "Normandie",
        "target_version": "0.5",
        "input_csv": str(input_path),
        "input_summary": parsed,
        "control": {
            "observation_count": len(control_rows),
            "detected_session_ids": sorted({row["session_id"] for row in control_rows if row["signal_detected"]}),
            "counts_for_any_gate": False,
        },
        "gate_results": {
            R3_TARGET: r3,
            ZHA_TARGET: zha,
        },
        "all_field_gates_satisfied": r3["field_gate_satisfied"] and zha["field_gate_satisfied"],
        "promotion_ready": False,
        "automatic_candidate_mutation_allowed": False,
        "automatic_publication_allowed": False,
        "candidate_memory_count": 142,
        "candidate_memory_delta": 0,
        "rules": policy["output_rules"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--input", type=Path, required=True, help="Filled field-session CSV")
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    args = parser.parse_args()

    root = args.root.resolve()
    input_path = args.input if args.input.is_absolute() else Path.cwd() / args.input
    report = evaluate_csv(root, input_path.resolve())
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output_path = args.output if args.output.is_absolute() else Path.cwd() / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
