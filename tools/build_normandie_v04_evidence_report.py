#!/usr/bin/env python3
"""Build a consolidated non-public evidence report for Normandie v0.4 promotion work."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = Path("research/normandie-v0.4/external-evidence-matrix.json")
R3_PATH = Path("research/normandie-v0.4/r3-mortain-field-validation.json")
F5ZHA_PATH = Path("research/normandie-v0.4/f5zha-mortain-validation.json")
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.4/generated/evidence")
ACCEPTED = {"high", "unmistakable", "confirmed"}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def valid_sessions(observations: list[dict[str, Any]], frequencies: set[float], minimum_intelligibility: int) -> list[dict[str, Any]]:
    valid: list[dict[str, Any]] = []
    for item in observations:
        try:
            frequency = round(float(item.get("frequency_mhz")), 6)
            intelligibility = int(item.get("intelligibility_0_to_5", -1))
        except (TypeError, ValueError):
            continue
        if frequency not in frequencies:
            continue
        if item.get("signal_detected") is not True:
            continue
        if str(item.get("identification_confidence", "")).lower() not in ACCEPTED:
            continue
        if intelligibility < minimum_intelligibility:
            continue
        if not item.get("date_local") or not item.get("time_local") or not item.get("location_description"):
            continue
        valid.append(item)
    return valid


def independent_count(items: list[dict[str, Any]]) -> int:
    keys = {
        (item.get("date_local"), item.get("time_local"), item.get("location_description"))
        for item in items
    }
    return len(keys)


def build_report(root: Path) -> dict[str, Any]:
    matrix = load_json(root / MATRIX_PATH)
    r3 = load_json(root / R3_PATH)
    f5zha = load_json(root / F5ZHA_PATH)

    if matrix["public_export_allowed"] is not False:
        raise ValueError("External evidence matrix must remain non-public")
    stations = {item["id"]: item for item in matrix["stations"]}
    expected = {"F1ZBX_R3", "F5ZHA_LAVAL", "F1ZOV_EQUEURDREVILLE", "F6ZES_SOURDEVAL"}
    if set(stations) != expected:
        raise ValueError("Unexpected evidence matrix station set")

    r3_required = int(r3["acceptance_gate"]["minimum_independent_sessions"])
    r3_valid = valid_sessions(r3.get("observations", []), {145.675}, 3)
    r3_count = independent_count(r3_valid)

    f5_validation = f5zha["validation"]
    f5_required = int(f5_validation["minimum_independent_sessions_for_useful_coverage"])
    f5_min_intelligibility = int(f5_validation["minimum_intelligibility_0_to_5"])
    f5_current_pair = {round(float(v), 6) for v in f5_validation["current_pair_primary_probes_mhz"]}
    f5_valid = valid_sessions(f5zha.get("observations", []), f5_current_pair, f5_min_intelligibility)
    f5_count = independent_count(f5_valid)
    f5_field_coverage_supported = f5_count >= f5_required
    f5_source_reconciled = stations["F5ZHA_LAVAL"]["local_operator_or_equivalent_reconciliation_found"] is True

    report = {
        "schema_version": "1.0",
        "status": "normandie_v0_4_evidence_report_not_public",
        "public_export_allowed": False,
        "stations": {
            "F1ZBX_R3": {
                "technical_parameters_verified": stations["F1ZBX_R3"]["technical_parameters_verified"],
                "operator_status_verified": stations["F1ZBX_R3"]["operator_status_verified"],
                "valid_mortain_sessions": r3_count,
                "required_mortain_sessions": r3_required,
                "field_gate_supported": r3_count >= r3_required,
                "promotion_allowed": False,
            },
            "F5ZHA_LAVAL": {
                "technical_parameters_verified": stations["F5ZHA_LAVAL"]["technical_parameters_verified"],
                "source_conflict_open": stations["F5ZHA_LAVAL"]["source_conflict_open"],
                "valid_mortain_sessions_on_current_pair": f5_count,
                "required_mortain_sessions": f5_required,
                "field_coverage_supported": f5_field_coverage_supported,
                "authoritative_source_reconciled": f5_source_reconciled,
                "promotion_prerequisites_satisfied": f5_field_coverage_supported and f5_source_reconciled,
                "promotion_allowed": False,
            },
            "F1ZOV_EQUEURDREVILLE": {
                "technical_parameters_verified": stations["F1ZOV_EQUEURDREVILLE"]["technical_parameters_verified"],
                "operator_status": stations["F1ZOV_EQUEURDREVILLE"]["operator_status"],
                "maintenance_cleared": stations["F1ZOV_EQUEURDREVILLE"]["operator_status"] != "maintenance",
                "promotion_allowed": False,
            },
            "F6ZES_SOURDEVAL": {
                "technical_parameters_verified": stations["F6ZES_SOURDEVAL"]["technical_parameters_verified"],
                "frequency_resolved": bool(stations["F6ZES_SOURDEVAL"]["current_frequencies_mhz"]),
                "must_not_guess": True,
                "promotion_allowed": False,
            },
        },
        "rules": {
            "evidence_report_does_not_modify_promotion_gates": True,
            "field_evidence_does_not_close_f5zha_source_conflict": True,
            "operator_maintenance_blocks_f1zov": True,
            "unresolved_f6zes_frequency_blocks_candidate_creation": True,
            "published_v0_3_1_remains_immutable": True,
        },
    }
    return report


def markdown(report: dict[str, Any]) -> str:
    s = report["stations"]
    return "\n".join([
        "# Normandie v0.4 — preuves consolidées",
        "",
        f"- R3 : {s['F1ZBX_R3']['valid_mortain_sessions']}/{s['F1ZBX_R3']['required_mortain_sessions']} sessions Mortain valides.",
        f"- F5ZHA : {s['F5ZHA_LAVAL']['valid_mortain_sessions_on_current_pair']}/{s['F5ZHA_LAVAL']['required_mortain_sessions']} sessions utiles ; conflit source réconcilié : {'oui' if s['F5ZHA_LAVAL']['authoritative_source_reconciled'] else 'non'}.",
        f"- F1ZOV : état opérateur = {s['F1ZOV_EQUEURDREVILLE']['operator_status']}.",
        f"- F6ZES : fréquence résolue = {'oui' if s['F6ZES_SOURDEVAL']['frequency_resolved'] else 'non'}.",
        "",
        "Ce rapport est informatif et ne modifie aucune porte de promotion ni aucun pack public.",
        "",
    ])


def write_report(root: Path, output_dir: Path) -> tuple[Path, Path, dict[str, Any]]:
    report = build_report(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "normandie-v04-evidence.json"
    md_path = output_dir / "normandie-v04-evidence.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(markdown(report), encoding="utf-8")
    return json_path, md_path, report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    root = args.root.resolve()
    output_dir = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    json_path, md_path, report = write_report(root, output_dir)
    print("NORMANDIE V0.4 EVIDENCE: non-public; no promotion gate modified")
    print(json_path)
    print(md_path)


if __name__ == "__main__":
    main()
