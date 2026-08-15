#!/usr/bin/env python3
"""Build the non-public Normandie v0.5 RX-only field validation kit."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KIT_PATH = Path("research/normandie-v0.5/field-validation-kit.json")
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.5/generated/field-validation-kit")

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


def validate_kit(root: Path) -> dict[str, Any]:
    kit = load_json(root / KIT_PATH)
    if kit["status"] != "field_validation_kit_not_public":
        raise ValueError("Unexpected field validation kit status")
    if kit["target_version"] != "0.5":
        raise ValueError("Unexpected target version")
    if kit["candidate_memory_count_before"] != 142 or kit["candidate_memory_count_after"] != 142:
        raise ValueError("Field kit must not change the Normandie v0.5 candidate count")
    if kit["candidate_memory_delta"] != 0 or kit["public_export_allowed"] is not False:
        raise ValueError("Field kit must remain non-public and zero-delta")

    rules = kit["rules"]
    if rules["chirp_duplex"] != "off" or rules["chirp_offset"] != "0.000000":
        raise ValueError("Field kit must enforce the RX-only CHIRP contract")
    if rules["tx_disabled"] is not True or rules["ctcss_rx_filter_enabled"] is not False:
        raise ValueError("Field kit must disable TX and RX CTCSS filtering")

    memories = kit["memories"]
    locations = [int(item["location"]) for item in memories]
    names = [item["name"] for item in memories]
    freqs = [round(float(item["frequency_mhz"]), 6) for item in memories]
    if len(memories) != 6:
        raise ValueError(f"Expected 6 field memories, got {len(memories)}")
    if len(locations) != len(set(locations)):
        raise ValueError("Duplicate field-kit CHIRP locations")
    if len(names) != len(set(names)) or any(len(name) > 10 for name in names):
        raise ValueError("Invalid or duplicate field-kit names")
    if len(freqs) != len(set(freqs)):
        raise ValueError("Duplicate field-kit RF frequencies")

    expected = {145.675, 145.075, 145.4675, 432.575, 431.4125, 145.6875}
    if set(freqs) != expected:
        raise ValueError("Unexpected field-kit RF set")

    gates = kit["gates"]
    r3 = gates["R3_MORTAIN_RX"]
    if r3["primary_probe_mhz"] != 145.675 or r3["minimum_independent_sessions"] != 2:
        raise ValueError("Unexpected R3 field gate")
    if r3["if_gate_clears_pair_memory_delta"] != 2:
        raise ValueError("R3 pair must remain two distinct RX memories")

    zha = gates["F5ZHA_SOURCE_AND_COVERAGE"]
    if zha["current_pair_mhz"] != [145.4675, 432.575]:
        raise ValueError("Unexpected F5ZHA current diagnostic pair")
    if zha["legacy_conflict_probe_mhz"] != 431.4125 or zha["legacy_probe_is_promotion_evidence"] is not False:
        raise ValueError("Legacy F5ZHA probe must remain diagnostic only")
    if zha["minimum_independent_sessions"] != 2 or zha["if_gate_clears_pair_memory_delta"] != 2:
        raise ValueError("Unexpected F5ZHA coverage gate")

    if not kit["session_log_columns"]:
        raise ValueError("Missing field session log columns")
    return kit


def write_outputs(root: Path, output_dir: Path) -> tuple[Path, Path, Path]:
    kit = validate_kit(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    chirp_path = output_dir / "normandie-v0.5-field-rx.csv"
    log_path = output_dir / "normandie-v0.5-field-session-template.csv"
    manifest_path = output_dir / "normandie-v0.5-field-kit-manifest.json"

    with chirp_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CHIRP_COLUMNS, lineterminator="\n")
        writer.writeheader()
        for item in sorted(kit["memories"], key=lambda row: int(row["location"])):
            writer.writerow(chirp_row(item))

    with log_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=kit["session_log_columns"], lineterminator="\n")
        writer.writeheader()

    manifest = {
        "schema_version": "1.0",
        "status": "field_validation_kit_built_not_public",
        "pack": kit["pack"],
        "target_version": kit["target_version"],
        "memory_count": len(kit["memories"]),
        "candidate_memory_count": 142,
        "candidate_memory_delta": 0,
        "public_export_allowed": False,
        "outputs": {
            "chirp_rx_csv": chirp_path.name,
            "session_template_csv": log_path.name,
        },
        "gates": kit["gates"],
        "rules": kit["rules"],
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return chirp_path, log_path, manifest_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    root = args.root.resolve()
    output_dir = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    chirp_path, log_path, manifest_path = write_outputs(root, output_dir)
    print("NORMANDIE V0.5 FIELD KIT: 6 RX memories, candidate delta=0, public=false")
    print(chirp_path)
    print(log_path)
    print(manifest_path)


if __name__ == "__main__":
    main()
