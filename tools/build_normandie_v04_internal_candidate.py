#!/usr/bin/env python3
"""Build the non-public Normandie v0.4 internal candidate from frozen v0.3.1."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = Path("research/normandie-v0.4/internal-candidate-map.json")
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.4/generated/internal-candidate")

CHIRP_COLUMNS = [
    "Location", "Name", "Frequency", "Duplex", "Offset", "Tone", "rToneFreq",
    "cToneFreq", "DtcsCode", "DtcsPolarity", "RxDtcsCode", "CrossMode", "Mode",
    "TStep", "Skip", "Power", "Comment", "URCALL", "RPT1CALL", "RPT2CALL", "DVCODE",
]


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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


def build_candidate(root: Path) -> tuple[dict[str, Any], bytes]:
    config = load_json(root / MAP_PATH)
    if config["status"] != "internal_candidate_map_not_public":
        raise ValueError("Unexpected internal candidate map status")
    if config["candidate"]["public_export_allowed"] is not False:
        raise ValueError("Internal candidate must remain non-public")

    base_path = root / config["base"]["csv"]
    base_bytes = base_path.read_bytes()
    base_text = base_bytes.decode("utf-8")
    if not base_text.endswith("\n"):
        raise ValueError("Frozen base CSV must end with a newline before safe append")

    base_rows = list(csv.DictReader(io.StringIO(base_text)))
    if len(base_rows) != config["base"]["memory_count"]:
        raise ValueError("Frozen base memory count does not match candidate map")

    base_locations = {int(row["Location"]) for row in base_rows}
    base_names = {row["Name"] for row in base_rows}
    base_frequencies = {round(float(row["Frequency"]), 6) for row in base_rows}

    additions = config["additions"]
    if len(additions) != config["candidate"]["new_memory_count"]:
        raise ValueError("Candidate addition count mismatch")

    addition_locations = [int(item["location"]) for item in additions]
    addition_names = [item["name"] for item in additions]
    addition_frequencies = [round(float(item["frequency_mhz"]), 6) for item in additions]

    if len(addition_locations) != len(set(addition_locations)) or base_locations.intersection(addition_locations):
        raise ValueError("Candidate memory location collision")
    if len(addition_names) != len(set(addition_names)) or base_names.intersection(addition_names):
        raise ValueError("Candidate memory name collision")
    if len(addition_frequencies) != len(set(addition_frequencies)) or base_frequencies.intersection(addition_frequencies):
        raise ValueError("Candidate RF frequency collision")
    if any(len(name) > 10 for name in addition_names):
        raise ValueError("Candidate memory name exceeds 10 characters")

    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=CHIRP_COLUMNS, lineterminator="\n")
    for item in sorted(additions, key=lambda row: int(row["location"])):
        writer.writerow(chirp_row(item))
    appended_bytes = buffer.getvalue().encode("utf-8")
    candidate_bytes = base_bytes + appended_bytes

    manifest = {
        "pack": config["pack"],
        "target_version": config["target_version"],
        "status": "internal_candidate_not_public",
        "public_export_allowed": False,
        "base_version": config["base"]["version"],
        "base_memory_count": len(base_rows),
        "new_memory_count": len(additions),
        "memory_count": len(base_rows) + len(additions),
        "positions_are_internal_provisional": True,
        "published_base_is_exact_prefix": True,
        "base_sha256": sha256_bytes(base_bytes),
        "candidate_sha256": sha256_bytes(candidate_bytes),
        "additions": [
            {
                "location": int(item["location"]),
                "name": item["name"],
                "frequency_mhz": float(item["frequency_mhz"]),
                "role": item["role"],
                "source_authority": item["source_authority"],
            }
            for item in additions
        ],
        "rules": {
            "published_base_rows_rewritten": False,
            "chirp_duplex": "off",
            "chirp_offset": "0.000000",
            "tx_disabled": True,
            "final_public_memory_plan_defined": False,
        },
    }
    if manifest["memory_count"] != config["candidate"]["memory_count"]:
        raise ValueError("Internal candidate total count mismatch")
    return manifest, candidate_bytes


def write_candidate(root: Path, output_dir: Path) -> tuple[Path, Path, dict[str, Any]]:
    manifest, candidate_bytes = build_candidate(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "normandie-v0.4-internal-candidate.json"
    csv_path = output_dir / "normandie-v0.4-internal-candidate.csv"
    json_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    csv_path.write_bytes(candidate_bytes)
    return json_path, csv_path, manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    root = args.root.resolve()
    output_dir = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    json_path, csv_path, manifest = write_candidate(root, output_dir)
    print(f"INTERNAL CANDIDATE: {manifest['memory_count']} memories ({manifest['new_memory_count']} new); public_export_allowed=false")
    print(json_path)
    print(csv_path)


if __name__ == "__main__":
    main()
