#!/usr/bin/env python3
"""Build a non-public Normandie v0.4 readiness report from repository truth files."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GATES_PATH = Path("research/normandie-v0.4/promotion-gates.json")
REVALIDATION_PATH = Path("research/normandie-v0.4/blocked-station-revalidation.json")
INTERNAL_MAP_PATH = Path("research/normandie-v0.4/internal-candidate-map.json")
F5ZHA_VALIDATION_PATH = Path("research/normandie-v0.4/f5zha-mortain-validation.json")
CHECKER_PATH = Path("tools/check_normandie_v04_promotion_gates.py")
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.4/generated/readiness")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_checker(root: Path):
    path = root / CHECKER_PATH
    spec = importlib.util.spec_from_file_location("normandie_v04_gate_checker", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_report(root: Path) -> dict[str, Any]:
    gates = load_json(root / GATES_PATH)
    revalidation = load_json(root / REVALIDATION_PATH)
    internal_map = load_json(root / INTERNAL_MAP_PATH)
    f5zha_validation = load_json(root / F5ZHA_VALIDATION_PATH)
    checker = load_checker(root)
    evaluated = checker.evaluate(root)

    if gates["rules"]["public_export_allowed"] is not False:
        raise ValueError("Promotion gates unexpectedly allow public export")
    if internal_map["candidate"]["public_export_allowed"] is not False:
        raise ValueError("Internal candidate unexpectedly allows public export")

    station_by_id = {item["id"]: item for item in revalidation["stations"]}
    required = {"F1ZBX_R3", "F5ZHA_LAVAL", "F1ZOV_EQUEURDREVILLE", "F6ZES_SOURDEVAL"}
    if set(station_by_id) != required:
        raise ValueError("Unexpected blocked-station revalidation set")

    current_count = int(internal_map["candidate"]["memory_count"])
    gate_additions = {
        "R3_MORTAIN_RX": 2,
        "F5ZHA_SOURCE_AND_COVERAGE": 2,
        "F1ZOV_OPERATIONAL_STATUS": 1,
    }
    max_count_after_known_gates = current_count + sum(gate_additions.values())

    blockers = []
    if not evaluated["r3"]["passed"]:
        blockers.append({
            "id": "R3_MORTAIN_RX",
            "memory_delta_if_cleared": 2,
            "state": "field_evidence_required",
            "detail": (
                f"{evaluated['r3']['valid_session_count']}/"
                f"{evaluated['r3']['required_session_count']} valid independent Mortain RX sessions"
            ),
        })
    if not evaluated["f5zha"]["passed"]:
        blockers.append({
            "id": "F5ZHA_SOURCE_AND_COVERAGE",
            "memory_delta_if_cleared": 2,
            "state": station_by_id["F5ZHA_LAVAL"]["state"],
            "detail": (
                "Current REF pair remains research-valid but authoritative reconciliation and useful "
                "Mortain reception/relevance are still required. Diagnostic geometry is about "
                f"{float(f5zha_validation['station']['straight_line_distance_to_mortain_km']):.1f} km and is not reception proof."
            ),
        })
    if not evaluated["f1zov"]["passed"]:
        blockers.append({
            "id": "F1ZOV_OPERATIONAL_STATUS",
            "memory_delta_if_cleared": 1,
            "state": station_by_id["F1ZOV_EQUEURDREVILLE"]["state"],
            "detail": "Local operator still marks F1ZOV in maintenance; 431.975 MHz stays excluded.",
        })

    unresolved = {
        "id": "F6ZES_SOURDEVAL",
        "memory_delta_if_resolved": None,
        "state": station_by_id["F6ZES_SOURDEVAL"]["state"],
        "detail": "Site is known but no usable current frequency/mode is verified; no memory can be planned.",
    }

    known_gate_count = len(blockers)
    report = {
        "schema_version": "1.0",
        "status": "normandie_v0_4_readiness_not_public",
        "current_internal_candidate_memory_count": current_count,
        "current_internal_candidate_new_memory_count": int(internal_map["candidate"]["new_memory_count"]),
        "known_blocked_gate_count": known_gate_count,
        "known_blocked_frequency_count": int(gates["blocked_frequency_count"]),
        "maximum_memory_count_if_all_current_known_gates_clear": max_count_after_known_gates,
        "final_public_memory_count": None,
        "f6zes_is_outside_known_gate_delta_until_frequency_resolved": True,
        "blockers": blockers,
        "unresolved_priority": unresolved,
        "all_known_gates_passed": bool(evaluated["all_blocked_gates_passed"]),
        "review_completed": False,
        "public_export_allowed": False,
        "public_release_ready": False,
        "rules": {
            "known_gate_clearance_does_not_auto_publish": True,
            "f6zes_frequency_must_not_be_guessed": True,
            "geometry_is_not_reception_proof": True,
            "published_v0_3_1_remains_immutable": True,
            "tx_disabled": True,
        },
    }
    return report


def markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Normandie v0.4 — readiness interne",
        "",
        f"- Candidat interne actuel : **{report['current_internal_candidate_memory_count']} mémoires**",
        f"- Fréquences bloquées connues : **{report['known_blocked_frequency_count']}**",
        f"- Maximum si les portes connues actuelles passent toutes : **{report['maximum_memory_count_if_all_current_known_gates_clear']} mémoires**",
        "- Taille publique finale : **non définie**",
        "- Publication autorisée : **non**",
        "",
        "## Blocages",
        "",
    ]
    for blocker in report["blockers"]:
        lines.append(
            f"- **{blocker['id']}** (+{blocker['memory_delta_if_cleared']} si levée) — "
            f"{blocker['state']} — {blocker['detail']}"
        )
    lines.extend([
        "",
        "## Priorité non chiffrable",
        "",
        f"- **{report['unresolved_priority']['id']}** — {report['unresolved_priority']['detail']}",
        "",
        "Même si toutes les portes connues sont levées, aucune publication n'est automatique : revue finale et plan public explicite restent obligatoires.",
        "",
    ])
    return "\n".join(lines)


def write_report(root: Path, output_dir: Path) -> tuple[Path, Path, dict[str, Any]]:
    report = build_report(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "normandie-v04-readiness.json"
    md_path = output_dir / "normandie-v04-readiness.md"
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
    print(
        "NORMANDIE V0.4 READINESS: "
        f"current={report['current_internal_candidate_memory_count']} "
        f"known-max={report['maximum_memory_count_if_all_current_known_gates_clear']} "
        "public_release_ready=false"
    )
    print(json_path)
    print(md_path)


if __name__ == "__main__":
    main()
