#!/usr/bin/env python3
"""Build the Bretagne v0.2 internal RX-only candidate without publishing it."""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE_BUILDER = Path("tools/build_bretagne_internal_candidate.py")
AVIATION = Path("research/bretagne-v0.2/aviation-airac-08.json")
DELTA = Path("research/bretagne-v0.2/candidate-memory-delta.json")
AVIATION_START = 130


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_base_builder(root: Path):
    path = root / BASE_BUILDER
    spec = importlib.util.spec_from_file_location("bretagne_v01_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load base builder: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_candidate(root: Path) -> dict[str, Any]:
    base_builder = load_base_builder(root)
    base = base_builder.build_candidate(root)
    aviation = load_json(root / AVIATION)
    delta = load_json(root / DELTA)

    if base["target_version"] != "0.1" or base["memory_count"] != 135:
        raise ValueError("Bretagne v0.1 base is not the expected immutable 135-memory candidate")
    if aviation["status"] != "verified_for_internal_candidate_not_public":
        raise ValueError("Aviation evidence is not eligible for the internal candidate")
    if aviation["cycle"]["validation_cycle"] != "AIRAC 08/26":
        raise ValueError("Unexpected aviation AIRAC cycle")
    if aviation["methodology"]["public_export_allowed"] is not False:
        raise ValueError("Aviation evidence unexpectedly allows public export")

    placed = [
        {"location": int(item["location"]), "channel": dict(item["channel"])}
        for item in base["memories"]
    ]
    locations = {item["location"] for item in placed}
    frequencies = {
        round(float(item["channel"]["frequency_mhz"]), 6) for item in placed
    }
    names = {str(item["channel"]["name"]) for item in placed}

    aviation_added = 0
    for index, source in enumerate(aviation["channels"]):
        location = AVIATION_START + index
        frequency = round(float(source["frequency_mhz"]), 6)
        name = str(source["name"])
        if location in locations:
            raise ValueError(f"Aviation location already occupied: {location}")
        if frequency in frequencies:
            raise ValueError(f"Aviation frequency duplicates base RF: {frequency}")
        if name in names:
            raise ValueError(f"Aviation memory name duplicates base: {name}")
        if len(name) > 10:
            raise ValueError(f"Aviation memory name too long: {name}")
        if source.get("tx_policy") != "rx_only":
            raise ValueError(f"Aviation memory is not RX-only: {name}")
        if source.get("mode") != "AM":
            raise ValueError(f"Aviation memory is not AM: {name}")
        if float(source.get("step_khz", 0)) != 8.33:
            raise ValueError(f"Aviation memory does not use 8.33 kHz step: {name}")
        if source.get("verification") != "verified_airac08_latest_effective_public":
            raise ValueError(f"Aviation verification status rejected: {name}")

        channel = dict(source)
        channel["source_dataset"] = AVIATION.as_posix()
        channel["candidate_block"] = "Aviation Bretagne AIRAC 08/26"
        placed.append({"location": location, "channel": channel})
        locations.add(location)
        frequencies.add(frequency)
        names.add(name)
        aviation_added += 1

    expected_added = int(delta["delta"]["aviation_airac08_memory_count"])
    expected_total = int(delta["delta"]["candidate_memory_count"])
    if aviation_added != expected_added:
        raise ValueError(f"Aviation delta mismatch: {aviation_added} != {expected_added}")
    if len(placed) != expected_total:
        raise ValueError(f"Candidate total mismatch: {len(placed)} != {expected_total}")
    if len(placed) > int(delta["rules"]["max_memories"]):
        raise ValueError("Candidate exceeds maximum memory count")

    return {
        "schema_version": "1.0",
        "pack": "Bretagne",
        "target_version": "0.2",
        "status": "internal_candidate_not_for_publication",
        "public_export_allowed": False,
        "updated": "2026-08-12",
        "published_base_version": "0.1",
        "published_base_memory_count": 135,
        "memory_count": len(placed),
        "new_memory_count": aviation_added,
        "aviation_memory_count": aviation_added,
        "aviation_cycle": aviation["cycle"]["validation_cycle"],
        "rules": {
            "rx_only": True,
            "chirp_duplex": "off",
            "chirp_offset": "0.000000",
            "same_rf_frequency_deduplicated": True,
            "published_v0_1_immutable": True,
            "no_artificial_fill": True,
            "public_pack_mutation_allowed": False,
        },
        "memories": sorted(placed, key=lambda item: item["location"]),
    }


def write_candidate(candidate: dict[str, Any], output_dir: Path, root: Path) -> None:
    base_builder = load_base_builder(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "bretagne-v0.2-internal.json"
    csv_path = output_dir / "bretagne-v0.2-internal.csv"
    json_path.write_text(
        json.dumps(candidate, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=base_builder.CHIRP_COLUMNS)
        writer.writeheader()
        for item in candidate["memories"]:
            writer.writerow(base_builder.chirp_row(item["location"], item["channel"]))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("research/bretagne-v0.2/generated/internal-candidate"),
    )
    args = parser.parse_args()
    root = args.root.resolve()
    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = root / output_dir
    candidate = build_candidate(root)
    write_candidate(candidate, output_dir, root)
    print(
        "BRETAGNE V0.2 INTERNAL CANDIDATE: "
        f"{candidate['memory_count']} RX memories, "
        f"+{candidate['new_memory_count']} aviation AIRAC 08/26, public=false"
    )


if __name__ == "__main__":
    main()
