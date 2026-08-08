#!/usr/bin/env python3
"""Check whether Annecy–Alpes–Léman v0.2 may enter public prepublication."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = Path("research/annecy-alpes-leman-v0.2")
OPERATIONS = RESEARCH / "aviation-operational-gates.json"
PLAN = RESEARCH / "prepublication-plan.json"
OPTIONS = Path("generator/options.json")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def passed(status: str) -> bool:
    return status.startswith("passed_")


def evaluate(root: Path) -> dict[str, Any]:
    operations = load_json(root / OPERATIONS)
    plan = load_json(root / PLAN)
    options = load_json(root / OPTIONS)

    blockers: list[dict[str, Any]] = []
    advisories: list[dict[str, Any]] = []

    for gate in operations["gates"]:
        if gate["required_for_public_release"]:
            if not passed(str(gate["status"])):
                blockers.append({
                    "id": gate["id"],
                    "status": gate["status"],
                    "reason": gate.get("reason", ""),
                })
        else:
            advisories.append({
                "id": gate["id"],
                "status": gate["status"],
                "service": gate.get("service"),
            })

    ready = not blockers
    return {
        "pack": "Annecy–Alpes–Léman",
        "target_version": "0.2.0",
        "ready_for_public_prepublication": ready,
        "candidate_memory_count": int(plan["candidate_memory_count"]),
        "blockers": blockers,
        "advisories": advisories,
        "notam_blocks_generation": bool(
            options["options"]["notam_check"]["blocks_generation"]
        ),
        "include_aviation_default": bool(
            options["options"]["include_aviation"]["default"]
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = evaluate(args.root.resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result["ready_for_public_prepublication"]:
            print("READY: Annecy–Alpes–Léman v0.2 may enter public prepublication")
        else:
            print("NOT READY: Annecy–Alpes–Léman v0.2")
            for blocker in result["blockers"]:
                print(f"BLOCKER: {blocker['id']} ({blocker['status']})")
        for advisory in result["advisories"]:
            print(f"ADVISORY: {advisory['id']} ({advisory['status']})")

    raise SystemExit(0 if result["ready_for_public_prepublication"] else 2)


if __name__ == "__main__":
    main()
