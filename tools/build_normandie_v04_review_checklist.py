#!/usr/bin/env python3
"""Build the Normandie v0.4 release-review checklist, including post-publication replay."""
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
SCOPE = Path("research/normandie-v0.4/release-scope.json")
PUBLICATION_RECORD = Path("research/normandie-v0.4/publication-record.json")
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


def publication_completed(root: Path) -> bool:
    path = root / PUBLICATION_RECORD
    if not path.is_file():
        return False
    record = load_json(path)
    return (
        record.get("status") == "published_immutable"
        and record.get("version") == "0.4"
        and record.get("memory_count") == 142
    )


def build(root: Path, as_of: date | None = None) -> dict[str, Any]:
    consistency = load_module(
        "source_consistency_review", root / "tools/check_normandie_v04_source_consistency.py"
    ).evaluate(root)
    freshness = load_module(
        "source_freshness_review", root / "tools/check_normandie_v04_source_freshness.py"
    ).evaluate(root, as_of)
    evidence = load_module(
        "evidence_review", root / "tools/build_normandie_v04_evidence_report.py"
    ).build_report(root)

    plan = load_json(root / PACK_PLAN)
    scope = load_json(root / SCOPE)
    deferred = set(scope["deferred_gate_ids"])
    station = evidence["stations"]
    registry = (root / REGISTRY).read_text(encoding="utf-8")
    registry_has_v04 = 'version: "v0.4"' in registry
    published = publication_completed(root)
    activation_state_coherent = (published and registry_has_v04) or (
        not published and not registry_has_v04
    )

    final_plan = (
        plan["memory_plan"].get("expected_memory_count")
        == scope["final_memory_count"]
        == 142
        and plan["memory_plan"].get("memory_positions_assigned") is True
        and scope["final_positions_assigned"] is True
    )

    def done(gate: str, actual: bool) -> bool:
        return bool(actual) or gate in deferred

    items = [
        {
            "id": "SOURCE_CONSISTENCY",
            "label": "Les fichiers de vérité et portes sont cohérents.",
            "completed": bool(consistency["consistent"]),
            "blocking_if_false": True,
        },
        {
            "id": "SOURCE_FRESHNESS",
            "label": "Les revalidations externes sont fraîches pour la décision de périmètre.",
            "completed": bool(freshness["release_review_freshness_gate_passed"]),
            "blocking_if_false": True,
        },
        {
            "id": "R3_MORTAIN_RX",
            "label": "R3 est validé ou explicitement reporté hors v0.4.",
            "completed": done("R3_MORTAIN_RX", station["F1ZBX_R3"]["field_gate_supported"]),
            "blocking_if_false": True,
            "deferred": "R3_MORTAIN_RX" in deferred,
        },
        {
            "id": "F5ZHA_SOURCE_AND_COVERAGE",
            "label": "F5ZHA est validé ou explicitement reporté hors v0.4.",
            "completed": done(
                "F5ZHA_SOURCE_AND_COVERAGE",
                station["F5ZHA_LAVAL"]["promotion_prerequisites_satisfied"],
            ),
            "blocking_if_false": True,
            "deferred": "F5ZHA_SOURCE_AND_COVERAGE" in deferred,
        },
        {
            "id": "F1ZOV_OPERATIONAL_STATUS",
            "label": "F1ZOV est validé ou explicitement reporté hors v0.4.",
            "completed": done(
                "F1ZOV_OPERATIONAL_STATUS",
                station["F1ZOV_EQUEURDREVILLE"]["maintenance_cleared"],
            ),
            "blocking_if_false": True,
            "deferred": "F1ZOV_OPERATIONAL_STATUS" in deferred,
        },
        {
            "id": "F6ZES_RESOLVED",
            "label": "F6ZES est résolu ou explicitement reporté hors v0.4.",
            "completed": done(
                "F6ZES_RESOLVED", station["F6ZES_SOURDEVAL"]["frequency_resolved"]
            ),
            "blocking_if_false": True,
            "deferred": "F6ZES_RESOLVED" in deferred,
        },
        {
            "id": "FINAL_MEMORY_PLAN",
            "label": "La taille finale 142 et les positions publiques sont définies.",
            "completed": final_plan,
            "blocking_if_false": True,
        },
        {
            "id": "FINAL_REVIEW",
            "label": "La revue finale du périmètre figé est terminée.",
            "completed": plan["publication"].get("review_completed") is True
            and scope.get("review_completed") is True,
            "blocking_if_false": True,
        },
        {
            "id": "PUBLIC_ACTIVATION_STATE",
            "label": "Le registre public correspond à la phase de publication enregistrée.",
            "completed": activation_state_coherent,
            "blocking_if_false": True,
        },
    ]

    completed = sum(item["completed"] for item in items)
    open_ids = [
        item["id"]
        for item in items
        if item["blocking_if_false"] and not item["completed"]
    ]
    return {
        "schema_version": "1.3",
        "status": "release_review_checklist_not_public",
        "as_of": freshness["as_of"],
        "item_count": len(items),
        "completed_count": completed,
        "blocking_open_count": len(open_ids),
        "blocking_open_ids": open_ids,
        "items": items,
        "deferred_gate_ids": sorted(deferred),
        "release_review_complete": not open_ids,
        "public_registry_has_v04": registry_has_v04,
        "publication_completed": published,
        "public_activation_state_coherent": activation_state_coherent,
        "public_activation_is_separate_step": True,
        "public_export_allowed": False,
        "rules": {
            "deferred_gate_is_not_validation": True,
            "deferred_gate_must_remain_outside_v0_4": True,
            "checklist_completion_does_not_auto_publish": True,
            "postpublication_replay_must_match_publication_record": True,
            "published_v0_3_1_remains_immutable": True,
            "published_v0_4_is_immutable": True,
        },
    }


def markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Normandie v0.4 — checklist de revue",
        "",
        f"- Complétés : **{data['completed_count']}/{data['item_count']}**",
        f"- Blocages ouverts : **{data['blocking_open_count']}**",
        f"- Dossiers reportés : **{len(data['deferred_gate_ids'])}**",
        f"- Publication v0.4 enregistrée : **{'oui' if data['publication_completed'] else 'non'}**",
        "",
    ]
    for item in data["items"]:
        suffix = " — reporté à v0.5" if item.get("deferred") else ""
        lines.append(
            f"- [{'x' if item['completed'] else ' '}] **{item['id']}** — {item['label']}{suffix}"
        )
    lines += [
        "",
        "Le report à v0.5 ferme le périmètre de v0.4 sans valider la fréquence concernée.",
        "Après publication, la checklist reste rejouable et vérifie que le registre correspond au journal de publication.",
        "",
    ]
    return "\n".join(lines)


def write(root: Path, output_dir: Path, as_of: date | None = None):
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
    output = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    jp, mp, data = write(root, output)
    print(
        "NORMANDIE V0.4 REVIEW CHECKLIST: "
        f"{data['completed_count']}/{data['item_count']} complete; "
        f"blockers={data['blocking_open_count']}; "
        f"published={str(data['publication_completed']).lower()}"
    )
    print(jp)
    print(mp)


if __name__ == "__main__":
    main()
