#!/usr/bin/env python3
"""Build the non-public Annecy–Alpes–Léman v0.3 paired-RX candidate."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

import build_annecy_prepublication as base

ROOT = Path(__file__).resolve().parents[1]
EXPANSION = Path("research/annecy-alpes-leman-v0.3/paired-rx-expansion.json")
DEFAULT_OUTPUT_DIR = Path("research/annecy-alpes-leman-v0.3/generated/internal-candidate")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def build_candidate(root: Path, include_aviation: bool = True) -> dict[str, Any]:
    expansion = load_json(root / EXPANSION)
    if expansion["status"] != "paired_rx_expansion_reviewed_sprint86_not_public":
        raise ValueError("Unexpected Annecy v0.3 paired-RX expansion status")
    if expansion["target_version"] != "0.3":
        raise ValueError("Unexpected Annecy target version")
    if expansion["based_on"]["version"] != "0.2" or expansion["based_on"]["immutable"] is not True:
        raise ValueError("Annecy v0.3 must be based on immutable public v0.2")
    if expansion["rules"]["published_v0_2_immutable"] is not True:
        raise ValueError("Published Annecy v0.2 immutability rule missing")
    if expansion["rules"]["rx_only"] is not True:
        raise ValueError("Annecy v0.3 must remain RX-only")
    if expansion["rules"]["chirp_duplex"] != "off" or expansion["rules"]["chirp_offset"] != "0.000000":
        raise ValueError("Annecy v0.3 paired-RX contract must use Duplex=off and Offset=0")

    base_candidate = base.build_prepublication(root, include_aviation, "disabled")
    memories = [
        {
            "location": int(item["location"]),
            "channel": dict(item["channel"]),
            "origin": "published_v0.2_immutable_base",
        }
        for item in base_candidate["memories"]
    ]

    additions = [
        item for item in expansion["candidate_additions"]
        if item.get("candidate_status") == "promote_internal_candidate"
    ]
    if len(additions) != 11:
        raise ValueError(f"Expected 11 paired-RX additions, got {len(additions)}")

    base_locations = {item["location"] for item in memories}
    base_names = {item["channel"]["name"] for item in memories}
    base_freqs = {round(float(item["channel"]["frequency_mhz"]), 6) for item in memories}
    new_locations: set[int] = set()
    new_names: set[str] = set()
    new_freqs: set[float] = set()

    for item in additions:
        location = int(item["location"])
        name = str(item["name"])
        frequency = round(float(item["frequency_mhz"]), 6)
        if location in base_locations or location in new_locations:
            raise ValueError(f"Duplicate or occupied v0.3 location: {location}")
        if name in base_names or name in new_names or len(name) > 10:
            raise ValueError(f"Invalid or duplicate v0.3 memory name: {name}")
        if frequency in base_freqs or frequency in new_freqs:
            raise ValueError(f"RF frequency is not unique after deduplication: {frequency:.6f}")
        if item["mode"] not in {"FM", "NFM"}:
            raise ValueError(f"Unsupported paired-RX mode: {item['mode']}")

        channel = {
            "name": name,
            "frequency_mhz": frequency,
            "mode": item["mode"],
            "step_khz": float(item["step_khz"]),
            "tx_policy": "rx_only",
            "verification": "sprint86_current_public_source",
            "source_ids": list(item["source_ids"]),
            "source_dataset": EXPANSION.as_posix(),
            "candidate_block": "Paired RX v0.3 expansion",
            "comment": item["comment"],
        }
        memories.append({"location": location, "channel": channel, "origin": "sprint86_paired_rx_expansion"})
        new_locations.add(location)
        new_names.add(name)
        new_freqs.add(frequency)

    deferred_freqs = {
        round(float(item["frequency_mhz"]), 6)
        for item in expansion["deferred"]
        if item.get("frequency_mhz") is not None
    }
    if deferred_freqs.intersection(new_freqs):
        raise ValueError("Deferred RF frequency was promoted into Annecy v0.3")

    locations = [item["location"] for item in memories]
    names = [item["channel"]["name"] for item in memories]
    frequencies = [round(float(item["channel"]["frequency_mhz"]), 6) for item in memories]
    if len(locations) != len(set(locations)):
        raise ValueError("Annecy v0.3 location collision")
    if len(names) != len(set(names)):
        raise ValueError("Annecy v0.3 duplicate memory name")
    if len(frequencies) != len(set(frequencies)):
        raise ValueError("Annecy v0.3 duplicate RF frequency")

    expected = 76 if include_aviation else 59
    expected_base = 65 if include_aviation else 48
    if len(memories) != expected:
        raise ValueError(f"Unexpected Annecy v0.3 count: {len(memories)} instead of {expected}")
    if len(memories) - expected_base != 11:
        raise ValueError("Annecy v0.3 delta must remain exactly 11 unique RF memories")

    return {
        "schema_version": "1.0",
        "pack": "Annecy–Alpes–Léman",
        "target_version": "0.3",
        "status": "internal_candidate_not_for_publication",
        "public_export_allowed": False,
        "public_registry_allowed": False,
        "include_aviation": include_aviation,
        "based_on_public_version": "0.2",
        "base_memory_count": expected_base,
        "memory_count": len(memories),
        "new_unique_rf_memory_count": 11,
        "potential_ceiling_if_f1zth_50m_clears": 77 if include_aviation else 60,
        "deferred_frequency_mhz": sorted(deferred_freqs),
        "rules": {
            "rx_only": True,
            "chirp_duplex": "off",
            "chirp_offset": "0.000000",
            "same_rf_frequency_deduplicated": True,
            "published_v0_2_immutable": True,
            "automatic_publication_allowed": False,
        },
        "memories": sorted(memories, key=lambda row: int(row["location"])),
    }


def write_candidate(candidate: dict[str, Any], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    suffix = "" if candidate["include_aviation"] else "-no-aviation"
    json_path = output_dir / f"annecy-alpes-leman-v0.3-internal{suffix}.json"
    csv_path = output_dir / f"annecy-alpes-leman-v0.3-internal{suffix}.csv"

    json_path.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=base.internal.CHIRP_COLUMNS, lineterminator="\n")
        writer.writeheader()
        for item in candidate["memories"]:
            writer.writerow(base.internal.chirp_row(item["location"], item["channel"]))
    return json_path, csv_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--aviation",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Include or remove the immutable v0.2 aviation blocks; paired-RX additions remain non-aviation.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    output_dir = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    candidate = build_candidate(root, args.aviation)
    json_path, csv_path = write_candidate(candidate, output_dir)
    print(
        f"ANNECY V0.3 INTERNAL: {candidate['memory_count']} RX memories, "
        f"new_unique_rf={candidate['new_unique_rf_memory_count']}, public=false"
    )
    print(json_path)
    print(csv_path)


if __name__ == "__main__":
    main()
