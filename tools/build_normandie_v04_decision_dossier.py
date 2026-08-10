#!/usr/bin/env python3
"""Build a single non-public Normandie v0.4 decision dossier from all current truth files."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.4/generated/decision-dossier")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(root: Path) -> dict[str, Any]:
    source_check = load_module("source_consistency", root / "tools/check_normandie_v04_source_consistency.py").evaluate(root)
    evidence = load_module("evidence", root / "tools/build_normandie_v04_evidence_report.py").build_report(root)
    readiness = load_module("readiness", root / "tools/build_normandie_v04_readiness_report.py").build_report(root)
    promotion = load_module("promotion", root / "tools/build_normandie_v04_internal_promotion_plan.py").build_plan(root)
    if not source_check["consistent"]:
        raise ValueError("Source truth is inconsistent")

    station_decisions = {
        "F1ZBX_R3": {
            "decision": "blocked",
            "reason": "Mortain field evidence incomplete",
            "evidence": evidence["stations"]["F1ZBX_R3"],
        },
        "F5ZHA_LAVAL": {
            "decision": "blocked",
            "reason": "authoritative source reconciliation and useful Mortain evidence both required",
            "evidence": evidence["stations"]["F5ZHA_LAVAL"],
        },
        "F1ZOV_EQUEURDREVILLE": {
            "decision": "blocked",
            "reason": "local operator still reports maintenance",
            "evidence": evidence["stations"]["F1ZOV_EQUEURDREVILLE"],
        },
        "F6ZES_SOURDEVAL": {
            "decision": "unresolved",
            "reason": "frequency and mode remain unresolved",
            "evidence": evidence["stations"]["F6ZES_SOURDEVAL"],
        },
    }

    return {
        "schema_version": "1.0",
        "status": "internal_decision_dossier_not_public",
        "source_truth_consistent": True,
        "current_internal_candidate_memory_count": readiness["current_internal_candidate_memory_count"],
        "known_gate_ceiling": readiness["maximum_memory_count_if_all_current_known_gates_clear"],
        "eligible_addition_count": promotion["eligible_addition_count"],
        "candidate_memory_count_if_current_plan_applied": promotion["candidate_memory_count_if_plan_applied_in_future"],
        "station_decisions": station_decisions,
        "review_required": True,
        "review_completed": False,
        "public_release_ready": False,
        "public_export_allowed": False,
        "rules": {
            "decision_dossier_never_opens_gates": True,
            "eligible_additions_do_not_equal_public_approval": True,
            "published_v0_3_1_remains_immutable": True,
            "tx_disabled": True
        }
    }


def markdown(d: dict[str, Any]) -> str:
    lines = [
        "# Normandie v0.4 — dossier de décision interne",
        "",
        f"- Cohérence des sources : **{'OK' if d['source_truth_consistent'] else 'ERREUR'}**",
        f"- Candidat interne : **{d['current_internal_candidate_memory_count']} mémoires**",
        f"- Ajouts actuellement éligibles : **{d['eligible_addition_count']}**",
        f"- Plafond connu si toutes les portes actuelles passent : **{d['known_gate_ceiling']}**",
        "- Publication autorisée : **non**",
        "",
        "## Décisions",
        ""
    ]
    for station, item in d["station_decisions"].items():
        lines.append(f"- **{station}** — {item['decision']} — {item['reason']}")
    lines.extend(["", "Une revue explicite reste obligatoire avant toute mutation du candidat ou publication.", ""])
    return "\n".join(lines)


def write(root: Path, output_dir: Path) -> tuple[Path, Path, dict[str, Any]]:
    d = build(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    jp = output_dir / "normandie-v04-decision-dossier.json"
    mp = output_dir / "normandie-v04-decision-dossier.md"
    jp.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mp.write_text(markdown(d), encoding="utf-8")
    return jp, mp, d


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    root = args.root.resolve()
    out = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    jp, mp, d = write(root, out)
    print(f"NORMANDIE V0.4 DECISION DOSSIER: eligible={d['eligible_addition_count']} public=false")
    print(jp)
    print(mp)


if __name__ == "__main__":
    main()
