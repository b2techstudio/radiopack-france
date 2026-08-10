#!/usr/bin/env python3
"""Build the non-public RX-only F5ZHA/Mortain diagnostic mini-pack."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = Path("research/normandie-v0.4/f5zha-mortain-validation.json")
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.4/generated/f5zha-validation")

CHIRP_COLUMNS = [
    "Location", "Name", "Frequency", "Duplex", "Offset", "Tone", "rToneFreq",
    "cToneFreq", "DtcsCode", "DtcsPolarity", "RxDtcsCode", "CrossMode", "Mode",
    "TStep", "Skip", "Power", "Comment", "URCALL", "RPT1CALL", "RPT2CALL", "DVCODE",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def chirp_row(item: dict[str, Any]) -> dict[str, str]:
    return {
        "Location": str(item["location"]),
        "Name": item["name"],
        "Frequency": f"{float(item['frequency_mhz']):.6f}",
        "Duplex": "off",
        "Offset": "0.000000",
        "Tone": "",
        "rToneFreq": "88.5",
        "cToneFreq": "88.5",
        "DtcsCode": "023",
        "DtcsPolarity": "NN",
        "RxDtcsCode": "023",
        "CrossMode": "Tone->Tone",
        "Mode": item["mode"],
        "TStep": f"{float(item['tstep_khz']):.2f}",
        "Skip": "",
        "Power": "",
        "Comment": item["comment"],
        "URCALL": "",
        "RPT1CALL": "",
        "RPT2CALL": "",
        "DVCODE": "",
    }


def build_validation_pack(root: Path) -> dict[str, Any]:
    config = load_json(root / MAP_PATH)
    if config["status"] != "diagnostic_validation_pack_not_public":
        raise ValueError("Unexpected F5ZHA validation pack status")
    rules = config["rules"]
    if rules["public_export_allowed"] is not False or rules["tx_disabled"] is not True:
        raise ValueError("F5ZHA validation pack must remain RX-only and non-public")
    if rules["source_conflict_remains_open_until_authoritative_reconciliation"] is not True:
        raise ValueError("F5ZHA source conflict guard must remain enabled")

    memories = config["memories"]
    locations = [int(item["location"]) for item in memories]
    names = [item["name"] for item in memories]
    freqs = [round(float(item["frequency_mhz"]), 6) for item in memories]
    if len(locations) != len(set(locations)):
        raise ValueError("Duplicate validation-pack memory locations")
    if len(names) != len(set(names)) or any(len(name) > 10 for name in names):
        raise ValueError("Invalid validation-pack memory names")
    if len(freqs) != len(set(freqs)):
        raise ValueError("Duplicate validation-pack RF frequencies")

    expected = {145.4675, 432.575, 431.4125}
    if set(freqs) != expected:
        raise ValueError("Unexpected F5ZHA diagnostic frequencies")
    if round(float(config["station"]["straight_line_distance_to_mortain_km"]), 1) != 65.6:
        raise ValueError("Unexpected F5ZHA/Mortain geometry reference")
    if config["station"]["geometry_is_reception_proof"] is not False:
        raise ValueError("Geometry must never be treated as reception proof")
    return config


def write_validation_pack(root: Path, output_dir: Path) -> tuple[Path, Path, dict[str, Any]]:
    config = build_validation_pack(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "f5zha-mortain-rx-diagnostic.json"
    csv_path = output_dir / "f5zha-mortain-rx-diagnostic.csv"

    manifest = {
        "status": "diagnostic_validation_pack_not_public",
        "public_export_allowed": False,
        "station": config["station"],
        "memory_count": len(config["memories"]),
        "current_pair_primary_probes_mhz": config["validation"]["current_pair_primary_probes_mhz"],
        "legacy_conflict_probe_mhz": config["validation"]["legacy_conflict_probe_mhz"],
        "rules": {
            "chirp_duplex": "off",
            "chirp_offset": "0.000000",
            "tx_disabled": True,
            "ctcss_rx_filter_enabled": False,
            "source_conflict_closed": False,
        },
    }
    json_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CHIRP_COLUMNS, lineterminator="\n")
        writer.writeheader()
        for item in sorted(config["memories"], key=lambda row: int(row["location"])):
            writer.writerow(chirp_row(item))

    return json_path, csv_path, manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    root = args.root.resolve()
    output_dir = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    json_path, csv_path, manifest = write_validation_pack(root, output_dir)
    print(
        "F5ZHA RX DIAGNOSTIC PACK: "
        f"{manifest['memory_count']} memories; public_export_allowed=false; source_conflict_closed=false"
    )
    print(json_path)
    print(csv_path)


if __name__ == "__main__":
    main()
