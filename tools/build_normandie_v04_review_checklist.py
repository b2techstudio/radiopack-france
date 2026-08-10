#!/usr/bin/env python3
"""Build a non-public Normandie v0.4 release-review checklist from current repository truth."""
from __future__ import annotations

import argparse
import importlib.util
import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.4/generated/review-checklist")
PACK_PLAN = Path("research/normandie-v0.4/pack-plan.json")
REGISTRY = Path("website/src/lib/packRegistry.ts")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build(root: Path, as_of: date | None = None) -> dict[str, Any]:
    consistency = load_module("source_consistency_review", root / "tools/check_normandie_v04_source_consistency.py").evaluate(root)
    freshness = load_module("source_freshness_review", root / "tools/check_normandie_v04_source_freshness.py").evaluate(root, as_of)
    evidence = load_module("evidence_review", root / "tools/build_normandie_v04_evidence_report.py").build_report(root)
    plan = load_json(root / PACK_PLAN)
    registry_text = (root / REGISTRY).read_text(encoding="utf-8")

    station = evidence["stations"]
    publication = plan["publication"]
    final_memory_plan_defined = plan["memory_plan"].get("expected_memory_count") is not None and plan["memory_plan"].get("memory_positions_assigned") is True
    public_registry_has_v04 = 'version: "v0.4"' in registry_text

    items = [
        {"id": "SOURCE_CONSISTENCY", "label": "Les fichiers de vérité et portes sont cohérents.", "completed": bool(consistency["consistent"]), "blocking_if_false": True},
        {"id": "SOURCE_FRESHNESS", "label": "Les revalidations externes ne sont pas périmées selon la politique interne.", "completed": bool(freshness["release_review_freshness_gate_passed"]), "blocking_if_false": True},
        {"id": "R3_MORTAIN_RX", "label": "La preuve de réception R3 depuis Mortain satisfait le protocole.", "completed": bool(station["F1ZBX_R3"]["field_gate_supported"]), "blocking_if_false": True},
        {"id": "F5ZHA_SOURCE_AND_COVERAGE", "label": "F5ZHA a à la fois une couverture utile documentée et une réconciliation autoritative du conflit.", "completed": bool(station["F5ZHA_LAVAL"]["promotion_prerequisites_satisfied"]), "blocking_if_false": True},
        {"id": "F1ZOV_OPERATIONAL_STATUS", "label": "L'exploitant local ne marque plus F1ZOV en maintenance.", "completed": bool(station["F1ZOV_EQUEURDREVILLE"]["maintenance_cleared"]), "blocking_if_false": True},
        {"id": "F6ZES_RESOLVED", "label": "F6ZES dispose d'une fréquence et d'un mode vérifiés sans valeur devinée.", "completed": bool(station["F6ZES_SOURDEVAL"]["frequency_resolved"]), "blocking_if_false": True},
        {"id": "FINAL_MEMORY_PLAN", "label": "La taille finale et les positions publiques sont explicitement définies.", "completed": final_memory_plan_defined, "blocking_if_false": True},
        {"id": "FINAL_REVIEW", "label": "La revue finale explicite a été terminée.", "completed": publication["review_completed"] is True, "blocking_if_false": True},
        {
            "id": "PUBLIC_REGISTRY_STILL_PRIVATE",
            "label": "Normandie v0.4 reste absente du registre public pendant la prépublication.",
            "completed": not public_registry_has_v04,
            "blocking_if_false": True,
        },
    ]
    completed = sum(1 for item in items if item["completed"])
    blocking_open = [item["id"] for item in items if item["blocking_if_false"] and not item["completed"]]
    return {
        "schema_version": "1.1",
        "status": "release_review_checklist_not_public",
        "as_of": freshness["as_of"],
        "item_count": len(items),
        "completed_count": completed,
        "blocking_open_count": len(blocking_open),
        "blocking_open_ids": blocking_open,
        "items": items,
        "release_review_complete": not blocking_open,
        "public_registry_has_v04": public_registry_has_v04,
        "public_activation_is_separate_step": True,
        "public_export_allowed": False,
        "rules": {
            "checklist_never_mutates_repository_state": True,
            "checklist_completion_does_not_auto_publish": True,
            "public_registry_must_remain_unchanged_during_prepublication_review": True,
            "public_registry_activation_is_a_separate_reviewed_change": True,
            "published_v0_3_1_remains_immutable": True,
        },
    }


def markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Normandie v0.4 — checklist de revue",
        "",
        f"- Complétés : **{data['completed_count']}/{data['item_count']}**",
        f"- Blocages ouverts : **{data['blocking_open_count']}**",
        f"- Revue prépublication complète : **{'oui' if data['release_review_complete'] else 'non'}**",
        "",
    ]
    for item in data["items"]:
        mark = "x" if item["completed"] else " "
        lines.append(f"- [{mark}] **{item['id']}** — {item['label']}")
    lines.extend([
        "",
        "La présence de v0.4 dans le registre public n'est pas une condition préalable : son activation est une étape séparée, après revue complète.",
        "Cette checklist est informative et ne publie rien.",
        "",
    ])
    return "\n".join(lines)


def write(root: Path, output_dir: Path, as_of: date | None = None) -> tuple[Path, Path, dict[str, Any]]:
    data = build(root, as_of)
    output_dir.mkdir(parents=True, exist_ok=True)
    jp = output_dir / "normandie-v04-review-checklist.json"
    mp = output_dir / "normandie-v04-review-checklist.md"
    jp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mp.write_text(markdown(data), encoding="utf-8")
    return jp, mp, data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    root = args.root.resolve()
    out = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    jp, mp, data = write(root, out)
    print(f"NORMANDIE V0.4 REVIEW CHECKLIST: {data['completed_count']}/{data['item_count']} complete; prepublication={str(data['release_review_complete']).lower()}")
    print(jp)
    print(mp)


if __name__ == "__main__":
    main()
