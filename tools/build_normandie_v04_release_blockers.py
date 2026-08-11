#!/usr/bin/env python3
"""Build release blockers for the frozen Normandie v0.4 scope."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.4/generated/release-blockers")
SCOPE = Path("research/normandie-v0.4/release-scope.json")
PLAN = Path("research/normandie-v0.4/pack-plan.json")
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


def build(root: Path) -> dict[str, Any]:
    dossier = load_module(
        "decision_dossier_blockers", root / "tools/build_normandie_v04_decision_dossier.py"
    ).build(root)
    scope = load_json(root / SCOPE)
    plan = load_json(root / PLAN)
    deferred = set(scope["deferred_gate_ids"])
    station_to_gate = {
        "F1ZBX_R3": "R3_MORTAIN_RX",
        "F5ZHA_LAVAL": "F5ZHA_SOURCE_AND_COVERAGE",
        "F1ZOV_EQUEURDREVILLE": "F1ZOV_OPERATIONAL_STATUS",
        "F6ZES_SOURDEVAL": "F6ZES_RESOLVED",
    }
    blockers = []
    for station, item in dossier["station_decisions"].items():
        gate = station_to_gate[station]
        if item["decision"] != "eligible_for_internal_plan" and gate not in deferred:
            blockers.append(
                {"id": station, "kind": item["decision"], "reason": item["reason"]}
            )

    if (
        plan["memory_plan"].get("expected_memory_count") != scope["final_memory_count"]
        or not plan["memory_plan"].get("memory_positions_assigned")
    ):
        blockers.append(
            {
                "id": "FINAL_MEMORY_PLAN",
                "kind": "planning",
                "reason": "final public memory count or positions are not defined",
            }
        )
    if (
        plan["publication"].get("review_completed") is not True
        or scope.get("review_completed") is not True
    ):
        blockers.append(
            {
                "id": "FINAL_REVIEW",
                "kind": "review",
                "reason": "explicit final review has not been completed",
            }
        )

    registry_text = (root / REGISTRY).read_text(encoding="utf-8")
    registry_has_v04 = 'version: "v0.4"' in registry_text
    record_path = root / PUBLICATION_RECORD
    published = False
    if record_path.is_file():
        record = load_json(record_path)
        published = (
            record.get("status") == "published_immutable"
            and record.get("version") == "0.4"
            and record.get("memory_count") == 142
        )

    prepublication_ready = not blockers
    activation_state_coherent = (published and registry_has_v04) or (
        not published and not registry_has_v04
    )
    return {
        "schema_version": "1.3",
        "status": "prepublication_blockers_not_public",
        "blocking_count": len(blockers),
        "blockers": blockers,
        "deferred_gate_count": len(deferred),
        "deferred_gate_ids": sorted(deferred),
        "prepublication_ready": prepublication_ready,
        "public_registry_has_v04": registry_has_v04,
        "publication_completed": published,
        "public_activation_state_coherent": activation_state_coherent,
        "public_activation_pending": prepublication_ready and not published and not registry_has_v04,
        "public_activation_completed": published and registry_has_v04,
        "release_allowed": False,
        "public_export_allowed": False,
        "rules": {
            "deferred_gate_is_not_validation": True,
            "deferred_gate_does_not_block_frozen_v0_4_scope": True,
            "final_memory_plan_must_be_explicit": True,
            "public_registry_activation_is_separate_and_reviewed": True,
            "postpublication_replay_does_not_reopen_closed_scope": True,
            "published_v0_3_1_remains_immutable": True,
            "published_v0_4_is_immutable": True,
        },
    }


def markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Normandie v0.4 — blocages de prépublication",
        "",
        f"Blocages actifs : **{data['blocking_count']}**",
        f"Dossiers reportés : **{data['deferred_gate_count']}**",
        f"Prépublication prête : **{'oui' if data['prepublication_ready'] else 'non'}**",
        f"Publication enregistrée : **{'oui' if data['publication_completed'] else 'non'}**",
        "",
    ]
    lines += [
        f"- **{item['id']}** ({item['kind']}) — {item['reason']}"
        for item in data["blockers"]
    ]
    lines += [
        "",
        "Un dossier reporté à v0.5 n'est pas validé pour v0.4 et ne peut pas être ajouté à ses 142 mémoires.",
        "",
    ]
    return "\n".join(lines)


def write(root: Path, output_dir: Path):
    data = build(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    jp = output_dir / "normandie-v04-release-blockers.json"
    mp = output_dir / "normandie-v04-release-blockers.md"
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
        "NORMANDIE V0.4 PREPUBLICATION BLOCKERS: "
        f"{data['blocking_count']} active; deferred={data['deferred_gate_count']}; "
        f"ready={str(data['prepublication_ready']).lower()}; "
        f"published={str(data['publication_completed']).lower()}"
    )
    print(jp)
    print(mp)


if __name__ == "__main__":
    main()
