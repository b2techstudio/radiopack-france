#!/usr/bin/env python3
"""Build a machine-readable list of every blocker preventing Normandie v0.4 publication."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.4/generated/release-blockers")


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
        {"id": "PUBLIC_REGISTRY", "kind": "publication", "reason": "Normandie v0.4 is intentionally absent from the public pack registry"}
    ])
    return {
        "schema_version": "1.0",
        "status": "release_blockers_not_public",
        "blocking_count": len(blockers),
        "blockers": blockers,
        "release_allowed": False,
        "public_export_allowed": False,
        "rules": {
            "non_eligible_station_decision_remains_release_blocker": True,
            "zero_station_blockers_still_requires_final_review": True,
            "final_memory_plan_must_be_explicit": True,
            "public_registry_change_must_be_separate_and_reviewed": True,
            "published_v0_3_1_remains_immutable": True
        }
    }


def markdown(data: dict[str, Any]) -> str:
    lines = ["# Normandie v0.4 — blocages de publication", "", f"Blocages actifs : **{data['blocking_count']}**", ""]
    lines.extend(f"- **{x['id']}** ({x['kind']}) — {x['reason']}" for x in data["blockers"])
    lines.extend(["", "Publication autorisée : **non**", ""])
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
    print(f"NORMANDIE V0.4 RELEASE BLOCKERS: {data['blocking_count']} active; release=false")
    print(jp)
    print(mp)


if __name__ == "__main__":
    main()
