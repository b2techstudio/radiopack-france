#!/usr/bin/env python3
"""Build a guarded non-public plan for additions whose promotion gates are actually clear."""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DELTA_PATH = Path("research/normandie-v0.4/candidate-memory-delta.json")
MAP_PATH = Path("research/normandie-v0.4/internal-candidate-map.json")
CHECKER_PATH = Path("tools/check_normandie_v04_promotion_gates.py")
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.4/generated/promotion-plan")

GATE_CANDIDATES = {
    "R3_MORTAIN_RX": ["ZBX-IN", "ZBX-OUT"],
    "F5ZHA_SOURCE_AND_COVERAGE": ["ZHA-A", "ZHA-B"],
    "F1ZOV_OPERATIONAL_STATUS": ["ZOV-B"],
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_checker(root: Path):
    path = root / CHECKER_PATH
    spec = importlib.util.spec_from_file_location("normandie_v04_gate_checker_promotion_plan", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_plan(root: Path) -> dict[str, Any]:
    delta = load_json(root / DELTA_PATH)
    internal_map = load_json(root / MAP_PATH)
    checker = load_checker(root)
    evaluated = checker.evaluate(root)

    if delta["rules"]["public_export_allowed"] is not False:
        raise ValueError("Candidate delta unexpectedly allows public export")
    if internal_map["candidate"]["public_export_allowed"] is not False:
        raise ValueError("Internal candidate unexpectedly allows public export")

    candidates = {item["name_hint"]: item for item in delta["new_frequency_candidates"]}
    gate_passed = {
        "R3_MORTAIN_RX": bool(evaluated["r3"]["passed"]),
        "F5ZHA_SOURCE_AND_COVERAGE": bool(evaluated["f5zha"]["passed"]),
        "F1ZOV_OPERATIONAL_STATUS": bool(evaluated["f1zov"]["passed"]),
    }

    current_count = int(internal_map["candidate"]["memory_count"])
    next_location = max(int(item["location"]) for item in internal_map["candidate"]["new_memories"]) + 1
    additions: list[dict[str, Any]] = []
    for gate_id in ("R3_MORTAIN_RX", "F5ZHA_SOURCE_AND_COVERAGE", "F1ZOV_OPERATIONAL_STATUS"):
        if not gate_passed[gate_id]:
            continue
        for name_hint in GATE_CANDIDATES[gate_id]:
            item = candidates[name_hint]
            additions.append({
                "gate_id": gate_id,
                "name_hint": name_hint,
                "frequency_mhz": float(item["frequency_mhz"]),
                "role": item["role"],
                "proposed_internal_location": next_location,
                "location_is_provisional": True,
                "public_export_allowed": False,
            })
            next_location += 1

    return {
        "schema_version": "1.0",
        "status": "guarded_internal_promotion_plan_not_public",
        "current_internal_candidate_memory_count": current_count,
        "gate_status": gate_passed,
        "eligible_addition_count": len(additions),
        "candidate_memory_count_if_plan_applied_in_future": current_count + len(additions),
        "additions": additions,
        "plan_applied": False,
        "internal_candidate_mutated": False,
        "public_export_allowed": False,
        "rules": {
            "only_clear_gates_can_create_plan_entries": True,
            "plan_never_mutates_candidate": True,
            "provisional_locations_are_not_public_positions": True,
            "explicit_separate_apply_step_would_be_required": True,
            "published_v0_3_1_remains_immutable": True,
            "tx_disabled": True,
        },
    }


def write_plan(root: Path, output_dir: Path) -> tuple[Path, dict[str, Any]]:
    plan = build_plan(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "normandie-v04-internal-promotion-plan.json"
    path.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path, plan


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    root = args.root.resolve()
    output_dir = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    path, plan = write_plan(root, output_dir)
    print(
        "NORMANDIE V0.4 INTERNAL PROMOTION PLAN: "
        f"eligible={plan['eligible_addition_count']} "
        f"candidate_if_applied={plan['candidate_memory_count_if_plan_applied_in_future']} "
        "applied=false public_export_allowed=false"
    )
    print(path)


if __name__ == "__main__":
    main()
