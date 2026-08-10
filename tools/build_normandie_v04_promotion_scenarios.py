#!/usr/bin/env python3
"""Build all non-public Normandie v0.4 known-gate promotion count scenarios."""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INTERNAL_MAP_PATH = Path("research/normandie-v0.4/internal-candidate-map.json")
GATES_PATH = Path("research/normandie-v0.4/promotion-gates.json")
DEFAULT_OUTPUT = Path("research/normandie-v0.4/generated/readiness/normandie-v04-promotion-scenarios.json")

GATE_DELTAS = {
    "R3_MORTAIN_RX": 2,
    "F5ZHA_SOURCE_AND_COVERAGE": 2,
    "F1ZOV_OPERATIONAL_STATUS": 1,
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def build_scenarios(root: Path) -> dict[str, Any]:
    internal_map = load_json(root / INTERNAL_MAP_PATH)
    gates = load_json(root / GATES_PATH)
    current = int(internal_map["candidate"]["memory_count"])
    gate_ids = [gate["id"] for gate in gates["gates"]]
    if set(gate_ids) != set(GATE_DELTAS):
        raise ValueError("Promotion gate set no longer matches the scenario model")

    scenarios = []
    for enabled_bits in itertools.product([False, True], repeat=len(gate_ids)):
        cleared = [gate_id for gate_id, enabled in zip(gate_ids, enabled_bits) if enabled]
        delta = sum(GATE_DELTAS[gate_id] for gate_id in cleared)
        scenarios.append({
            "cleared_gates": cleared,
            "known_gate_memory_delta": delta,
            "candidate_memory_count_if_only_these_known_gates_clear": current + delta,
            "public_export_allowed": False,
            "requires_explicit_final_review": True,
        })

    scenarios.sort(key=lambda item: (item["known_gate_memory_delta"], item["cleared_gates"]))
    return {
        "schema_version": "1.0",
        "status": "promotion_scenarios_not_public",
        "base_internal_candidate_memory_count": current,
        "known_gate_deltas": GATE_DELTAS,
        "scenario_count": len(scenarios),
        "minimum_known_scenario_memory_count": current,
        "maximum_known_scenario_memory_count": current + sum(GATE_DELTAS.values()),
        "f6zes_excluded_from_scenario_counts_until_frequency_resolved": True,
        "scenarios": scenarios,
        "rules": {
            "scenario_is_not_promotion_approval": True,
            "scenario_is_not_publication_approval": True,
            "final_public_memory_count_remains_undefined": True,
            "published_v0_3_1_remains_immutable": True,
            "public_export_allowed": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    result = build_scenarios(root)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        "NORMANDIE V0.4 PROMOTION SCENARIOS: "
        f"{result['scenario_count']} scenarios; "
        f"range={result['minimum_known_scenario_memory_count']}..{result['maximum_known_scenario_memory_count']}; "
        "public_export_allowed=false"
    )
    print(output)


if __name__ == "__main__":
    main()
