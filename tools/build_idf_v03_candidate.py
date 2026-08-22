#!/usr/bin/env python3
"""Build the deterministic Île-de-France v0.3 publication basis.

The builder first reconstructs the immutable public v0.2 from repository source data
and refuses to continue unless its SHA-256 still matches the frozen publication record.
It then keeps the exact national + 18-memory aviation blocks and replaces only the
regional radio block with the Sprint 101 pass-3 scope. The resulting bytes are the
immutable basis of the published v0.3 CSV.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RECORD = Path("research/ile-de-france-v0.2/publication-record.json")
OUTPUT = Path("research/ile-de-france-v0.3/generated/release-candidate/radiopack-france-ile-de-france-v0.3-candidate.csv")
MANIFEST = Path("research/ile-de-france-v0.3/generated/release-candidate/candidate-manifest.json")

COLUMNS = [
    "Location", "Name", "Frequency", "Duplex", "Offset", "Tone",
    "rToneFreq", "cToneFreq", "DtcsCode", "DtcsPolarity", "RxDtcsCode",
    "CrossMode", "Mode", "TStep", "Skip", "Power", "Comment",
    "URCALL", "RPT1CALL", "RPT2CALL", "DVCODE",
]

AVIATION = [
    ("AIR-EMERG", 121.5, "France / aviation", "EMERGENCY", None),
    ("CDG-APP1", 118.155, "Paris CDG", "APP", "LFPG"),
    ("CDG-APP2", 119.855, "Paris CDG", "APP", "LFPG"),
    ("CDG-APP3", 121.155, "Paris CDG", "APP", "LFPG"),
    ("CDG-APP4", 124.355, "Paris CDG", "APP", "LFPG"),
    ("ORY-APP1", 118.855, "Paris Orly", "APP", "LFPO"),
    ("ORY-APP2", 124.45, "Paris Orly", "APP", "LFPO"),
    ("ORY-APP3", 127.75, "Paris Orly", "APP", "LFPO"),
    ("ORY-GND1", 121.555, "Paris Orly", "GND", "LFPO"),
    ("ORY-GND2", 121.705, "Paris Orly", "GND", "LFPO"),
    ("ORY-TWR", 118.7, "Paris Orly", "TWR", "LFPO"),
    ("ORY-ATIS", 126.505, "Paris Orly", "ATIS", "LFPO"),
    ("ORY-INFO", 131.355, "Paris Orly", "INFO", "LFPO"),
    ("LBG-FIS", 123.835, "Le Bourget", "FIS", "LFPB"),
    ("LBG-GND1", 121.955, "Le Bourget", "GND", "LFPB"),
    ("LBG-GND2", 121.905, "Le Bourget", "GND", "LFPB"),
    ("LBG-TWR", 118.93, "Le Bourget", "TWR", "LFPB"),
    ("LBG-ATIS", 120.005, "Le Bourget", "ATIS", "LFPB"),
]

V02_REPEATERS = [
    ("F5ZAD", "Clamart", 145.6),
    ("F5ZNG", "Provins", 145.625),
    ("F5ZNN", "Coulommiers", 145.65),
    ("F1ZSY", "Paris", 145.7),
    ("F1ZUX", "Achères", 145.7125),
    ("F5ZMH", "Linas", 145.7375),
    ("F5ZEQ", "Sartrouville", 145.75),
    ("F1ZHK", "Nangis", 145.7625),
]

V03_REGIONAL = [
    ("F5ZNG-O", 145.625, "F5ZNG · Provins · sortie RX · Île-de-France v0.3 pass3 · sources recoupées 2026-08-21"),
    ("F5ZNG-I", 145.025, "F5ZNG · Provins · entrée RX · Île-de-France v0.3 pass3 · sources recoupées 2026-08-21"),
    ("F5ZNN-O", 145.650, "F5ZNN · Saint-Rémy-la-Vanne · sortie RX · Île-de-France v0.3 pass3 · sources recoupées 2026-08-21"),
    ("F5ZNN-I", 145.050, "F5ZNN · Saint-Rémy-la-Vanne · entrée RX · Île-de-France v0.3 pass3 · sources recoupées 2026-08-21"),
    ("F6ZEE-O", 145.700, "F6ZEE · Pontault-Combault · sortie RX · attribution courante validée 2026-08-21"),
    ("F6ZEE-I", 145.100, "F6ZEE · Pontault-Combault · entrée RX · attribution courante validée 2026-08-21"),
    ("F5ZMH-O", 145.7375, "F5ZMH · Linas · sortie RX · Île-de-France v0.3 pass3 · sources recoupées 2026-08-21"),
    ("F5ZMH-I", 145.1375, "F5ZMH · Linas · entrée RX · Île-de-France v0.3 pass3 · sources recoupées 2026-08-21"),
    ("F1ZHK-O", 145.7625, "F1ZHK · Nangis · sortie RX · REF + RepeaterBook recoupés 2026-08-21"),
    ("F1ZHK-I", 145.1625, "F1ZHK · Nangis · entrée RX · REF + RepeaterBook recoupés 2026-08-21"),
    ("F5ZMR-A", 431.525, "F5ZMR · Provins · paire 70 cm RX A · sources recoupées 2026-08-21"),
    ("F5ZMR-B", 439.125, "F5ZMR · Provins · paire 70 cm RX B · sources recoupées 2026-08-21"),
    ("F5ZSY-A", 145.325, "F5ZSY · Issy-les-Moulineaux · crossband RX A · sources recoupées 2026-08-21"),
    ("F5ZSY-B", 430.325, "F5ZSY · Issy-les-Moulineaux · crossband RX B · sources recoupées 2026-08-21"),
    ("F5ZNN-X", 430.650, "F5ZNN · Saint-Rémy-la-Vanne · crossband RX unique après déduplication · validé 2026-08-21"),
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def chirp_row(location: int, name: str, frequency: float, mode: str, step: float, comment: str) -> list[str]:
    return [
        str(location), name, f"{frequency:.6f}", "off", "0.000000", "", "88.5", "88.5",
        "023", "NN", "023", "Tone->Tone", mode, f"{step:.2f}", "", "", comment,
        "", "", "", "",
    ]


def csv_bytes(rows: list[list[str]]) -> bytes:
    out = io.StringIO(newline="")
    writer = csv.writer(out, lineterminator="\r\n")
    writer.writerow(COLUMNS)
    writer.writerows(rows)
    return out.getvalue().encode("utf-8")


def national_rows(root: Path) -> list[list[str]]:
    rows: list[list[str]] = []
    sources = [
        ("data/national/pmr446.json", 0),
        ("data/national/amateur-calls-rx.json", 20),
        ("data/national/amateur-listening-rx.json", 30),
    ]
    for rel, start in sources:
        channels = load_json(root / rel)["channels"]
        for index, channel in enumerate(channels):
            rows.append(chirp_row(
                start + index,
                channel["name"],
                float(channel["frequency_mhz"]),
                channel["mode"],
                float(channel["step_khz"]),
                channel["comment"],
            ))
    return rows


def aviation_rows() -> list[list[str]]:
    rows: list[list[str]] = []
    for index, (name, frequency, area, service, icao) in enumerate(AVIATION):
        comment = f"{area} · {service}" + (f" · {icao}" if icao else "") + " · SIA AIRAC 08/26 / eAIP courant · RX seule"
        rows.append(chirp_row(40 + index, name, frequency, "AM", 8.33, comment))
    return rows


def v02_regional_rows() -> list[list[str]]:
    rows: list[list[str]] = []
    location = 70
    for call, site, output in V02_REPEATERS:
        for suffix, frequency, side in [
            ("O", output, "sortie"),
            ("I", round(output - 0.6, 4), "entrée"),
        ]:
            rows.append(chirp_row(
                location,
                f"{call}-{suffix}",
                frequency,
                "FM",
                12.5,
                f"{call} · {site} · {side} RX · recoupé REF/F5AIB + RepeaterBook le 2026-08-19",
            ))
            location += 1
    return rows


def v03_regional_rows() -> list[list[str]]:
    return [chirp_row(70 + index, name, frequency, "FM", 12.5, comment)
            for index, (name, frequency, comment) in enumerate(V03_REGIONAL)]


def validate(rows: list[list[str]], expected_count: int) -> None:
    if len(rows) != expected_count:
        raise ValueError(f"Expected {expected_count} memories, got {len(rows)}")
    locations = [int(row[0]) for row in rows]
    names = [row[1] for row in rows]
    frequencies = [row[2] for row in rows]
    if len(locations) != len(set(locations)):
        raise ValueError("Duplicate CHIRP locations")
    if len(names) != len(set(names)):
        raise ValueError("Duplicate CHIRP names")
    if len(frequencies) != len(set(frequencies)):
        raise ValueError("Duplicate RF frequencies")
    if max(locations) > 199:
        raise ValueError("Memory limit exceeded")
    if not all(row[3] == "off" and row[4] == "0.000000" for row in rows):
        raise ValueError("RX-only contract violated")
    if any(len(name) > 10 for name in names):
        raise ValueError("CHIRP name exceeds 10 characters")


def build(root: Path) -> tuple[bytes, dict[str, Any]]:
    record = load_json(root / RECORD)
    if record["status"] != "published_immutable" or record["version"] != "0.2" or int(record["memory_count"]) != 58:
        raise ValueError("Unexpected Île-de-France v0.2 publication record")

    common = national_rows(root) + aviation_rows()
    base_rows = sorted(common + v02_regional_rows(), key=lambda row: int(row[0]))
    validate(base_rows, 58)
    base_bytes = csv_bytes(base_rows)
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != record["public_csv_sha256"]:
        raise ValueError(f"Reconstructed public v0.2 SHA mismatch: {base_sha}")

    candidate_rows = sorted(common + v03_regional_rows(), key=lambda row: int(row[0]))
    validate(candidate_rows, 57)
    candidate_bytes = csv_bytes(candidate_rows)
    candidate_sha = hashlib.sha256(candidate_bytes).hexdigest()

    manifest = {
        "schema_version": "1.0",
        "status": "published_basis_immutable",
        "generated_on": "2026-08-21",
        "published_on": "2026-08-22",
        "pack": "Île-de-France",
        "target_version": "0.3",
        "published_base_version": "0.2",
        "published_base_memory_count": 58,
        "published_base_sha256": base_sha,
        "candidate_memory_count": 57,
        "candidate_aviation_memory_count": 18,
        "candidate_regional_radio_memory_count": 15,
        "candidate_sha256": candidate_sha,
        "public_csv_sha256": candidate_sha,
        "candidate_csv": str(OUTPUT),
        "public_csv": "website/public/downloads/ile-de-france/radiopack-france-ile-de-france-v0.3.csv",
        "builder": "tools/build_idf_v03_candidate.py",
        "airac_cycle": "08/26",
        "airac_valid_through_inclusive": "2026-09-02",
        "airac09_revalidation_required_on_or_after": "2026-09-03",
        "validation": {
            "public_base_sha_matches_frozen_record": True,
            "rx_only": True,
            "rf_deduplicated": True,
            "unique_locations": True,
            "unique_names": True,
            "memory_limit_passed": True,
            "public_csv_byte_identical_to_candidate": True,
        },
        "public_export_allowed": True,
        "published": True,
        "published_version_is_immutable": True,
    }
    return candidate_bytes, manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--check", action="store_true", help="validate frozen generated files without rewriting")
    args = parser.parse_args()
    root = args.root.resolve()
    candidate_bytes, manifest = build(root)
    output = root / OUTPUT
    manifest_path = root / MANIFEST

    if args.check:
        if output.read_bytes() != candidate_bytes:
            raise ValueError("Frozen candidate CSV differs from deterministic rebuild")
        frozen_manifest = load_json(manifest_path)
        if frozen_manifest != manifest:
            raise ValueError("Frozen candidate manifest differs from deterministic rebuild")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(candidate_bytes)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"IDF V0.3 PUBLISHED BASIS: 57 RX, aviation=18, sha256={manifest['candidate_sha256']}, public=true")


if __name__ == "__main__":
    main()
