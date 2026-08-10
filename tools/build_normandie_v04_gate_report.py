#!/usr/bin/env python3
"""Build a non-public human-readable promotion-gate report for Normandie v0.4."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REVALIDATION_PATH = Path("research/normandie-v0.4/blocked-station-revalidation.json")
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.4/generated/gates")
CHECKER_PATH = Path(__file__).with_name("check_normandie_v04_promotion_gates.py")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_checker():
    spec = importlib.util.spec_from_file_location("normandie_v04_promotion_checker", CHECKER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load promotion gate checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_report(root: Path) -> dict[str, Any]:
    evaluation = load_checker().evaluate(root)
    revalidation = load_json(root / REVALIDATION_PATH)
    stations = {item["id"]: item for item in revalidation["stations"]}

    return {
        "status": "promotion_gate_report_not_public",
        "updated": revalidation["updated"],
        "target_version": "0.4",
        "public_export_allowed": False,
        "current_internal_candidate_memory_count": evaluation["current_internal_candidate_memory_count"],
        "gates": {
            "R3_MORTAIN_RX": {
                "passed": evaluation["r3"]["passed"],
                "valid_session_count": evaluation["r3"]["valid_session_count"],
                "required_session_count": evaluation["r3"]["required_session_count"],
                "state": stations["F1ZBX_R3"]["state"],
                "next_action": "Record independent RX-only sessions on 145.675 MHz from Mortain-Bocage."
            },
            "F5ZHA_SOURCE_AND_COVERAGE": {
                "passed": evaluation["f5zha"]["passed"],
                "state": stations["F5ZHA_LAVAL"]["state"],
                "next_action": "Find a current local/operator-equivalent source closing the frequency conflict and validate useful Mortain relevance."
            },
            "F1ZOV_OPERATIONAL_STATUS": {
                "passed": evaluation["f1zov"]["passed"],
                "state": stations["F1ZOV_EQUEURDREVILLE"]["state"],
                "next_action": "Wait for the local operator to explicitly remove the maintenance status, then revalidate the pair."
            }
        },
        "unresolved_priority": {
            "F6ZES_SOURDEVAL": {
                "state": stations["F6ZES_SOURDEVAL"]["state"],
                "next_action": "Keep searching for a second current source with an explicit frequency and mode; never guess."
            }
        },
        "all_blocked_gates_passed": evaluation["all_blocked_gates_passed"],
        "rules": {
            "report_is_not_publication_approval": True,
            "failed_gate_must_not_be_promoted": True,
            "tx_disabled": True,
            "public_export_allowed": False
        }
    }


def render_markdown(report: dict[str, Any]) -> str:
    gate_lines = []
    for gate_id, gate in report["gates"].items():
        status = "PASS" if gate["passed"] else "BLOCKED"
        detail = ""
        if gate_id == "R3_MORTAIN_RX":
            detail = f" ({gate['valid_session_count']}/{gate['required_session_count']} sessions valides)"
        gate_lines.append(
            f"- **{gate_id}** — {status}{detail} — `{gate['state']}`\n"
            f"  - Prochaine action : {gate['next_action']}"
        )

    f6zes = report["unresolved_priority"]["F6ZES_SOURDEVAL"]
    return (
        "# Normandie v0.4 — rapport local des portes de promotion\n\n"
        f"Mis à jour : **{report['updated']}**\n\n"
        f"Candidat interne : **{report['current_internal_candidate_memory_count']} mémoires**. "
        "Ce rapport est non public et ne constitue jamais une autorisation de publication.\n\n"
        "## Portes\n\n"
        + "\n".join(gate_lines)
        + "\n\n## Priorité non résolue\n\n"
        f"- **F6ZES_SOURDEVAL** — `{f6zes['state']}`\n"
        f"  - Prochaine action : {f6zes['next_action']}\n\n"
        f"**Toutes les portes franchies : {'oui' if report['all_blocked_gates_passed'] else 'non'}**\n"
    )


def write_report(root: Path, output_dir: Path) -> tuple[Path, Path, dict[str, Any]]:
    report = build_report(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "normandie-v0.4-promotion-gates.json"
    md_path = output_dir / "normandie-v0.4-promotion-gates.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
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
        "NORMANDIE V0.4 GATE REPORT: "
        f"candidate={report['current_internal_candidate_memory_count']} "
        f"all_blocked_gates_passed={str(report['all_blocked_gates_passed']).lower()} "
        "public_export_allowed=false"
    )
    print(json_path)
    print(md_path)


if __name__ == "__main__":
    main()
