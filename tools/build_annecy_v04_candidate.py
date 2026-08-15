#!/usr/bin/env python3
"""Build Annecy–Alpes–Léman v0.4 from immutable public v0.3 + F1ZTH 50 MHz RX."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_DIR = ROOT / "website/public/downloads/annecy-alpes-leman"
BASE_FULL = BASE_DIR / "radiopack-france-annecy-alpes-leman-v0.3.csv"
BASE_NO_AIR = BASE_DIR / "radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv"
REVIEW = ROOT / "research/annecy-alpes-leman-v0.4/compatibility-and-source-review.json"
BASE_FULL_SHA = "fa4095c0af9b4fa5758449e09c9a32eb5c7cc103e0d90b7c9da8e74c77796af7"
BASE_NO_AIR_SHA = "e639aff0d045e5a20db3b03fb6175b68452700b4b6ee2e1edf78e9510c2eb649"
FULL_NAME = "radiopack-france-annecy-alpes-leman-v0.4.csv"
NO_AIR_NAME = "radiopack-france-annecy-alpes-leman-v0.4-sans-aviation.csv"
MANIFEST_NAME = "annecy-v0.4-manifest.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def validate_base() -> None:
    if sha256(BASE_FULL) != BASE_FULL_SHA:
        raise ValueError("Annecy v0.3 full CSV drifted")
    if sha256(BASE_NO_AIR) != BASE_NO_AIR_SHA:
        raise ValueError("Annecy v0.3 no-air CSV drifted")
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    decision = review["decision"]
    required = [
        "stock_uvk5_receive_baseline_cleared",
        "chirp_stock_driver_memory_band_cleared",
        "current_public_rf_source_cleared",
        "promotion_to_v0_4_candidate_allowed",
    ]
    if not all(decision[key] is True for key in required):
        raise ValueError("Annecy v0.4 compatibility/source gate not cleared")
    if decision["private_or_unpublished_frequency_used"] is not False:
        raise ValueError("Private/unpublished RF cannot enter v0.4")


def new_row(location: int, fields: list[str]) -> dict[str, str]:
    row = {field: "" for field in fields}
    row.update({
        "Location": str(location),
        "Name": "ZTH-6M",
        "Frequency": "50.537500",
        "Duplex": "off",
        "Offset": "0.000000",
        "rToneFreq": "88.5",
        "cToneFreq": "88.5",
        "DtcsCode": "023",
        "DtcsPolarity": "NN",
        "RxDtcsCode": "023",
        "CrossMode": "Tone->Tone",
        "Mode": "FM",
        "TStep": "12.50",
        "Comment": "F1ZTH Bourgoin-Jallieu — sortie 6 m analogique FM 50.5375 MHz; REF actif; RX-only",
    })
    return row


def build_variant(base: Path, expected_count: int, output: Path) -> tuple[int, str]:
    fields, rows = read_rows(base)
    if len(rows) != expected_count:
        raise ValueError(f"Unexpected base count for {base.name}: {len(rows)}")
    freqs = {round(float(row["Frequency"]), 6) for row in rows}
    if 50.5375 in freqs:
        raise ValueError("50.5375 MHz already present in v0.3")
    locations = [int(row["Location"]) for row in rows]
    rows.append(new_row(max(locations) + 1, fields))
    if any(row["Duplex"] != "off" or row["Offset"] != "0.000000" for row in rows):
        raise ValueError("RX-only contract failed")
    if len({round(float(row["Frequency"]), 6) for row in rows}) != len(rows):
        raise ValueError("RF deduplication failed")
    if len({row["Name"] for row in rows}) != len(rows):
        raise ValueError("Memory-name uniqueness failed")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\r\n")
        writer.writeheader()
        writer.writerows(rows)
    return len(rows), sha256(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    validate_base()
    output_dir = args.output_dir.resolve()
    full_count, full_sha = build_variant(BASE_FULL, 76, output_dir / FULL_NAME)
    no_air_count, no_air_sha = build_variant(BASE_NO_AIR, 59, output_dir / NO_AIR_NAME)
    manifest = {
        "schema_version": "1.0",
        "status": "candidate_built_rx_only",
        "pack": "Annecy–Alpes–Léman",
        "version": "0.4",
        "based_on": "0.3",
        "full_memory_count": full_count,
        "without_aviation_memory_count": no_air_count,
        "aviation_memory_count": 17,
        "new_unique_rf_memory_count": 1,
        "added_frequency_mhz": 50.5375,
        "full_sha256": full_sha,
        "without_aviation_sha256": no_air_sha,
        "public_mutation": False,
    }
    (output_dir / MANIFEST_NAME).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"ANNECY V0.4 CANDIDATE: {full_count}/{no_air_count} RX, +1 RF, public=false")
    print(full_sha)
    print(no_air_sha)


if __name__ == "__main__":
    main()
