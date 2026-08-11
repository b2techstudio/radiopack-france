#!/usr/bin/env python3
"""Build the Bretagne v0.1 internal RX-only candidate without publishing it."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

CHIRP_COLUMNS = [
    "Location", "Name", "Frequency", "Duplex", "Offset", "Tone",
    "rToneFreq", "cToneFreq", "DtcsCode", "DtcsPolarity", "RxDtcsCode",
    "CrossMode", "Mode", "TStep", "Skip", "Power", "Comment",
    "URCALL", "RPT1CALL", "RPT2CALL", "DVCODE",
]

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = Path("research/bretagne-v0.1")
PAIRED_PLAN = Path("research/paired-rx-deduplicated-memory-plan.json")

NATIONAL_BLOCKS = [
    ("PMR446 national RX", Path("data/national/pmr446.json"), 0),
    ("VHF marine national RX", Path("data/national/marine-vhf-rx.json"), 20),
    ("APRS et ISS", Path("data/national/amateur-listening-rx.json"), 120),
    ("Canaux d'appel", Path("data/national/amateur-calls-rx.json"), 150),
]
REGIONAL_START = 160

def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)

def chirp_row(location: int, channel: dict[str, Any]) -> dict[str, Any]:
    name = str(channel["name"])
    if len(name) > 10:
        raise ValueError(f"Nom trop long: {name}")
    if channel.get("tx_policy") != "rx_only":
        raise ValueError(f"Politique TX interdite: {name}")
    mode = channel.get("mode", "NFM")
    if mode not in {"FM", "NFM", "AM"}:
        raise ValueError(f"Mode non pris en charge: {mode}")
    return {
        "Location": location,
        "Name": name,
        "Frequency": f"{float(channel['frequency_mhz']):.6f}",
        "Duplex": "off",
        "Offset": "0.000000",
        "Tone": "",
        "rToneFreq": "88.5",
        "cToneFreq": "88.5",
        "DtcsCode": "023",
        "DtcsPolarity": "NN",
        "RxDtcsCode": "023",
        "CrossMode": "Tone->Tone",
        "Mode": mode,
        "TStep": f"{float(channel.get('step_khz', 12.5)):.2f}",
        "Skip": channel.get("skip", ""),
        "Power": "",
        "Comment": channel["comment"],
        "URCALL": "",
        "RPT1CALL": "",
        "RPT2CALL": "",
        "DVCODE": "",
    }

def build_candidate(root: Path) -> dict[str, Any]:
    memory_plan = load_json(root / RESEARCH / "memory-plan.json")
    paired = load_json(root / PAIRED_PLAN)
    region = next(item for item in paired["regions"] if item["id"] == "bretagne-v0.1")

    placed: list[dict[str, Any]] = []
    by_frequency: dict[float, dict[str, Any]] = {}

    for label, path, start in NATIONAL_BLOCKS:
        dataset = load_json(root / path)
        for index, source in enumerate(dataset["channels"]):
            channel = dict(source)
            channel["tx_policy"] = "rx_only"
            channel["source_dataset"] = path.as_posix()
            channel["candidate_block"] = label
            channel.setdefault("regional_roles", [])
            item = {"location": start + index, "channel": channel}
            placed.append(item)
            frequency = round(float(channel["frequency_mhz"]), 6)
            if frequency in by_frequency:
                raise ValueError(f"Fréquence nationale dupliquée: {frequency}")
            by_frequency[frequency] = item

    regional_location = REGIONAL_START
    regional_new_count = 0
    regional_merged_count = 0
    for source in region["memories"]:
        frequency = round(float(source["frequency_mhz"]), 6)
        if frequency in by_frequency:
            target = by_frequency[frequency]["channel"]
            target.setdefault("regional_roles", [])
            for role in source["roles"]:
                if role not in target["regional_roles"]:
                    target["regional_roles"].append(role)
            target.setdefault("regional_selection_statuses", [])
            status = source["selection_status"]
            if status not in target["regional_selection_statuses"]:
                target["regional_selection_statuses"].append(status)
            regional_merged_count += 1
            continue

        channel = {
            "name": source["name_hint"],
            "frequency_mhz": frequency,
            "mode": "NFM",
            "step_khz": 12.5,
            "comment": "Bretagne — " + " / ".join(source["roles"]) + " — RX seule",
            "tx_policy": "rx_only",
            "source_dataset": PAIRED_PLAN.as_posix(),
            "candidate_block": "Radioamateur régional Bretagne",
            "regional_roles": list(source["roles"]),
            "selection_status": source["selection_status"],
        }
        item = {"location": regional_location, "channel": channel}
        placed.append(item)
        by_frequency[frequency] = item
        regional_location += 1
        regional_new_count += 1

    locations = [item["location"] for item in placed]
    names = [item["channel"]["name"] for item in placed]
    frequencies = [round(float(item["channel"]["frequency_mhz"]), 6) for item in placed]
    if len(locations) != len(set(locations)):
        raise ValueError("Conflit de positions mémoire")
    if len(names) != len(set(names)):
        raise ValueError("Noms mémoire dupliqués")
    if len(frequencies) != len(set(frequencies)):
        raise ValueError("Fréquences RF dupliquées")
    if len(placed) != int(memory_plan["expected_memory_count"]):
        raise ValueError(
            f"Total inattendu: {len(placed)} au lieu de {memory_plan['expected_memory_count']}"
        )
    if regional_new_count != 21 or regional_merged_count != 8:
        raise ValueError(
            f"Déduplication Bretagne inattendue: new={regional_new_count} merged={regional_merged_count}"
        )

    return {
        "schema_version": "1.0",
        "pack": "Bretagne",
        "target_version": "0.1",
        "status": "internal_candidate_not_for_publication",
        "public_export_allowed": False,
        "updated": "2026-08-11",
        "memory_count": len(placed),
        "regional_source_unique_frequency_count": int(region["unique_frequency_count"]),
        "regional_new_memory_count_after_national_deduplication": regional_new_count,
        "regional_roles_merged_into_national_memories": regional_merged_count,
        "aviation_memory_count": 0,
        "rules": {
            "rx_only": True,
            "chirp_duplex": "off",
            "chirp_offset": "0.000000",
            "same_rf_frequency_deduplicated": True,
            "generic_marine_channels_do_not_claim_local_transmitter_sites": True,
            "aviation_pending_current_sia_validation": True,
            "public_pack_mutation_allowed": False,
        },
        "memories": sorted(placed, key=lambda item: item["location"]),
    }

def write_candidate(candidate: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "bretagne-v0.1-internal.json"
    csv_path = output_dir / "bretagne-v0.1-internal.csv"
    json_path.write_text(
        json.dumps(candidate, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CHIRP_COLUMNS)
        writer.writeheader()
        for item in candidate["memories"]:
            writer.writerow(chirp_row(item["location"], item["channel"]))

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("research/bretagne-v0.1/generated/internal-candidate"),
    )
    args = parser.parse_args()
    candidate = build_candidate(args.root)
    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = args.root / output_dir
    write_candidate(candidate, output_dir)
    print(
        "BRETAGNE V0.1 INTERNAL CANDIDATE: "
        f"{candidate['memory_count']} RX memories, "
        f"{candidate['regional_new_memory_count_after_national_deduplication']} regional new, "
        f"{candidate['regional_roles_merged_into_national_memories']} regional roles merged, public=false"
    )

if __name__ == "__main__":
    main()
