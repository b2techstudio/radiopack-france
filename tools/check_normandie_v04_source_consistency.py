#!/usr/bin/env python3
"""Check that Normandie v0.4 source, gate and revalidation states remain mutually consistent."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = Path("research/normandie-v0.4/source-consistency-contract.json")
MATRIX = Path("research/normandie-v0.4/external-evidence-matrix.json")
REVALIDATION = Path("research/normandie-v0.4/blocked-station-revalidation.json")
GATES = Path("research/normandie-v0.4/promotion-gates.json")


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate(root: Path) -> dict[str, Any]:
    contract = load(root / CONTRACT)
    matrix = load(root / MATRIX)
    revalidation = load(root / REVALIDATION)
    gates = load(root / GATES)
    if contract["rules"]["public_export_allowed"] is not False:
        raise ValueError("Source consistency contract must remain non-public")

    m = {x["id"]: x for x in matrix["stations"]}
    r = {x["id"]: x for x in revalidation["stations"]}
    g = {x["id"]: x for x in gates["gates"]}
    expected = set(contract["stations"])
    if set(m) != expected or set(r) != expected:
        raise ValueError("Station set differs between source truth files")

    errors: list[str] = []
    if m["F1ZBX_R3"]["primary_source_kind"] != "current_local_operator":
        errors.append("R3 primary source is no longer the local operator")
    if m["F1ZBX_R3"]["current_frequencies_mhz"] != r["F1ZBX_R3"]["frequencies_mhz"]:
        errors.append("R3 frequency pair differs between evidence and revalidation")
    if m["F1ZBX_R3"]["useful_mortain_reception_verified"] is False and g["R3_MORTAIN_RX"]["promotion_to_internal_candidate_allowed"] is True:
        errors.append("R3 gate opened without Mortain reception evidence")

    if m["F5ZHA_LAVAL"]["source_conflict_open"] is True and g["F5ZHA_SOURCE_AND_COVERAGE"]["promotion_to_internal_candidate_allowed"] is True:
        errors.append("F5ZHA gate opened while source conflict is still open")
    if m["F5ZHA_LAVAL"]["current_frequencies_mhz"] != r["F5ZHA_LAVAL"]["frequencies_mhz"]:
        errors.append("F5ZHA pair differs between evidence and revalidation")

    if r["F1ZOV_EQUEURDREVILLE"]["state"] == "operator_maintenance" and g["F1ZOV_OPERATIONAL_STATUS"]["promotion_to_internal_candidate_allowed"] is True:
        errors.append("F1ZOV gate opened while local operator still reports maintenance")
    if m["F1ZOV_EQUEURDREVILLE"]["operator_status"] != "maintenance":
        errors.append("F1ZOV evidence matrix no longer reflects local operator maintenance")

    if m["F6ZES_SOURDEVAL"]["current_frequencies_mhz"] and r["F6ZES_SOURDEVAL"]["must_not_guess_frequency"] is True:
        errors.append("F6ZES frequencies appeared without resolving the guarded source state")
    if not m["F6ZES_SOURDEVAL"]["current_frequencies_mhz"] and r["F6ZES_SOURDEVAL"]["promotion_to_internal_candidate_allowed"] is True:
        errors.append("F6ZES promoted without a verified frequency")

    return {
        "status": "source_consistency_check_not_public",
        "consistent": not errors,
        "error_count": len(errors),
        "errors": errors,
        "public_export_allowed": False,
        "rules": contract["rules"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    result = evaluate(args.root.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result["consistent"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
