#!/usr/bin/env python3
"""Build machine-readable blockers that prevent Normandie v0.4 from becoming activation-ready."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.4/generated/release-blockers")
REGISTRY = Path("website/src/lib/packRegistry.ts")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(root: Path) -> dict[str, Any]:
    dossier = load_module("decision_dossier_blockers", root / "tools/build_normandie_v04_decision_dossier.py").build(root)
    blockers = []
    for station, item in dossier["station_decisions"].items():
        if item["decision"] != "eligible_for_internal_plan":
            blockers.append({"id": station, "kind": item["decision"], "reason": item["reason"]})
    blockers.extend([
        {"id": "FINAL_REVIEW", "kind": "review", "reason": "explicit final review has not been completed"},
        {"id": "FINAL_MEMORY_PLAN", "kind": "planning", "reason": "final public memory count and public positions are not defined"},
    ])
    registry_text = (root / REGISTRY).read_text(encoding="utf-8")
    registry_has_v04 = 'version: "v0.4"' in registry_text
    prepublication_ready = len(blockers) == 0 and not registry_has_v04
    return {
        "schema_version": "1.1",
        "status": "prepublication_blockers_not_public",
        "blocking_count": len(blockers),
        "blockers": blockers,
        "prepublication_ready": prepublication_ready,
        "public_registry_has_v04": registry_has_v04,
        "public_activation_pending": not registry_has_v04,
        "release_allowed": False,
        "public_export_allowed": False,
        "rules": {
            "non_eligible_station_decision_remains_prepublication_blocker": True,
            "zero_station_blockers_still_requires_final_review": True,
            "final_memory_plan_must_be_explicit": True,
            "public_registry_must_remain_private_until_prepublication_ready": True,
            "public_registry_activation_is_separate_and_reviewed": True,
            "prepublication_ready_does_not_publish": True,
            "published_v0_3_1_remains_immutable": True,
        },
    }


def markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Normandie v0.4 — blocages de prépublication",
        "",
        f"Blocages actifs : **{data['blocking_count']}**",
        f"Prépublication prête : **{'oui' if data['prepublication_ready'] else 'non'}**",
        f"Activation registre public en attente : **{'oui' if data['public_activation_pending'] else 'non'}**",
        "",
    ]
    lines.extend(f"- **{x['id']}** ({x['kind']}) — {x['reason']}" for x in data["blockers"])
    lines.extend([
        "",
        "L'activation du registre public est une étape séparée après prépublication prête ; ce rapport ne publie rien.",
        "",
    ])
    return "\n".join(lines)


def write(root: Path, output_dir: Path) -> tuple[Path, Path, dict[str, Any]]:
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
    out = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    jp, mp, data = write(root, out)
    print(
        "NORMANDIE V0.4 PREPUBLICATION BLOCKERS: "
        f"{data['blocking_count']} active; ready={str(data['prepublication_ready']).lower()}; public=false"
    )
    print(jp)
    print(mp)


if __name__ == "__main__":
    main()
