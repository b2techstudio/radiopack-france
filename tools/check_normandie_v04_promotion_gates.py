#!/usr/bin/env python3
"""Evaluate non-public promotion gates for the Normandie v0.4 internal candidate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GATES_PATH = Path("research/normandie-v0.4/promotion-gates.json")
FIELD_PATH = Path("research/normandie-v0.4/r3-mortain-field-validation.json")

ACCEPTED_IDENTIFICATION = {"high", "unmistakable", "confirmed"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def valid_r3_sessions(field: dict[str, Any]) -> list[dict[str, Any]]:
    sessions: list[dict[str, Any]] = []
    for observation in field.get("observations", []):
        try:
            frequency = round(float(observation.get("frequency_mhz")), 6)
            intelligibility = int(observation.get("intelligibility_0_to_5", -1))
        except (TypeError, ValueError):
            continue
        if frequency != 145.675:
            continue
        if observation.get("signal_detected") is not True:
            continue
        if str(observation.get("identification_confidence", "")).lower() not in ACCEPTED_IDENTIFICATION:
            continue
        if intelligibility < 3:
            continue
        if not observation.get("date_local") or not observation.get("location_description"):
            continue
        sessions.append(observation)
    return sessions


def evaluate(root: Path) -> dict[str, Any]:
    gates = load_json(root / GATES_PATH)
    field = load_json(root / FIELD_PATH)
    gate_by_id = {gate["id"]: gate for gate in gates["gates"]}

    r3_sessions = valid_r3_sessions(field)
    independent_keys = {
        (item.get("date_local"), item.get("time_local"), item.get("location_description"))
        for item in r3_sessions
    }
    r3_required = int(gate_by_id["R3_MORTAIN_RX"]["promotion_requirements"]["minimum_independent_sessions"])
    r3_passed = len(independent_keys) >= r3_required

    results = {
        "status": "promotion_gate_evaluation_not_public",
        "current_internal_candidate_memory_count": gates["current_internal_candidate_memory_count"],
        "r3": {
            "passed": r3_passed,
            "valid_session_count": len(independent_keys),
            "required_session_count": r3_required,
            "frequencies_mhz": gate_by_id["R3_MORTAIN_RX"]["frequencies_mhz"],
        },
        "f5zha": {
            "passed": gate_by_id["F5ZHA_SOURCE_AND_COVERAGE"]["promotion_to_internal_candidate_allowed"] is True,
            "state": gate_by_id["F5ZHA_SOURCE_AND_COVERAGE"]["current_state"],
        },
        "f1zov": {
            "passed": gate_by_id["F1ZOV_OPERATIONAL_STATUS"]["promotion_to_internal_candidate_allowed"] is True,
            "state": gate_by_id["F1ZOV_OPERATIONAL_STATUS"]["current_state"],
        },
        "public_export_allowed": False,
    }
    results["all_blocked_gates_passed"] = results["r3"]["passed"] and results["f5zha"]["passed"] and results["f1zov"]["passed"]
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    result = evaluate(args.root.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
