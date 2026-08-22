#!/usr/bin/env python3
"""Build the deterministic Grand Est v0.3 internal candidate.

The builder reconstructs the immutable public v0.2 from repository source data and
refuses to continue unless its SHA-256 matches the frozen publication record. It keeps
the exact national + 19-memory aviation blocks and replaces only the regional radio
block with the Sprint 102 closed 41-RF scope.

This is an internal research candidate only: it does not create or update any public CSV.
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
RECORD = Path("research/grand-est-v0.2/publication-record.json")
OUTPUT = Path("research/grand-est-v0.3/generated/release-candidate/radiopack-france-grand-est-v0.3-candidate.csv")
MANIFEST = Path("research/grand-est-v0.3/generated/release-candidate/candidate-manifest.json")

COLUMNS = [
    "Location", "Name", "Frequency", "Duplex", "Offset", "Tone",
    "rToneFreq", "cToneFreq", "DtcsCode", "DtcsPolarity", "RxDtcsCode",
    "CrossMode", "Mode", "TStep", "Skip", "Power", "Comment",
    "URCALL", "RPT1CALL", "RPT2CALL", "DVCODE",
]

AVIATION = [
    ("AIR-EMERG", 121.5, "France / aviation", "EMERGENCY", None),
    ("SXB-FIS1", 119.58, "Strasbourg", "FIS", "LFST"),
    ("SXB-FIS2", 132.215, "Strasbourg", "FIS", "LFST"),
    ("SXB-FIS3", 136.135, "Strasbourg", "FIS", "LFST"),
    ("SXB-APP", 118.185, "Strasbourg", "APP", "LFST"),
    ("MLH-FIS1", 129.25, "Bâle-Mulhouse", "FIS", "LFSB"),
    ("MLH-FIS2", 130.9, "Bâle-Mulhouse", "FIS", "LFSB"),
    ("MLH-FIS3", 134.68, "Bâle-Mulhouse", "FIS", "LFSB"),
    ("MLH-APP1", 125.16, "Bâle-Mulhouse", "APP", "LFSB"),
    ("MLH-APP2", 127.285, "Bâle-Mulhouse", "APP", "LFSB"),
    ("MLH-DEL", 121.955, "Bâle-Mulhouse", "DEL", "LFSB"),
    ("MLH-GND", 121.605, "Bâle-Mulhouse", "GND", "LFSB"),
    ("MLH-TWR", 118.3, "Bâle-Mulhouse", "TWR", "LFSB"),
    ("MLH-ATIS", 127.88, "Bâle-Mulhouse", "ATIS", "LFSB"),
    ("ETZ-APP", 119.125, "Metz-Nancy", "APP", "LFJL"),
    ("ETZ-GND", 121.705, "Metz-Nancy", "GND", "LFJL"),
    ("ETZ-TWR", 122.075, "Metz-Nancy", "TWR", "LFJL"),
    ("ETZ-ATIS", 136.58, "Metz-Nancy", "ATIS", "LFJL"),
    ("ENC-INFO", 119.605, "Nancy-Essey", "AFIS", "LFSN"),
]

V02_REPEATERS = [
    ("F5ZAU", "Dabo / Col du Valsberg", 145.6125),
    ("F1ZDG", "Sondernach / Petit Ballon", 145.625),
    ("F5ZDL", "Tilloy", 145.6375),
    ("F1ZAE", "Metz", 145.675),
    ("F5ZEC", "Chaumont", 145.7),
    ("F5ZCQ", "Wissembourg", 145.725),
    ("F1ZPJ", "Saint-Avold", 145.75),
    ("F1ZAX", "Cosnes-et-Romain", 145.7625),
]

V03_REGIONAL = [
    ("F5ZAU-O", 145.6125, "F5ZAU · Dabo / Col du Valsberg · sortie RX · Grand Est v0.3 radio scope · validé 2026-08-22"),
    ("F5ZAU-I", 145.0125, "F5ZAU · Dabo / Col du Valsberg · entrée RX · Grand Est v0.3 radio scope · validé 2026-08-22"),
    ("F1ZDG-O", 145.625, "F1ZDG · Petit Ballon · sortie RX · Grand Est v0.3 radio scope · validé 2026-08-22"),
    ("F1ZDG-I", 145.025, "F1ZDG · Petit Ballon · entrée RX · Grand Est v0.3 radio scope · validé 2026-08-22"),
    ("F5ZDL-O", 145.6375, "F5ZDL · Tilloy-et-Bellay · sortie RX · Grand Est v0.3 radio scope · validé 2026-08-22"),
    ("F5ZDL-I", 145.0375, "F5ZDL · Tilloy-et-Bellay · entrée RX · Grand Est v0.3 radio scope · validé 2026-08-22"),
    ("F1ZAE-O", 145.675, "F1ZAE · Pierrevillers / Metz · sortie RX · Grand Est v0.3 radio scope · validé 2026-08-22"),
    ("F1ZAE-I", 145.075, "F1ZAE · Pierrevillers / Metz · entrée RX · Grand Est v0.3 radio scope · validé 2026-08-22"),
    ("F5ZEC-O", 145.7, "F5ZEC · Sexfontaines / Chaumont · sortie RX · Grand Est v0.3 radio scope · validé 2026-08-22"),
    ("F5ZEC-I", 145.1, "F5ZEC · Sexfontaines / Chaumont · entrée RX · Grand Est v0.3 radio scope · validé 2026-08-22"),
    ("F5ZCQ-O", 145.725, "F5ZCQ · Rott / Wissembourg · sortie RX · Grand Est v0.3 radio scope · validé 2026-08-22"),
    ("F5ZCQ-I", 145.125, "F5ZCQ · Rott / Wissembourg · entrée RX · Grand Est v0.3 radio scope · validé 2026-08-22"),
    ("F1ZPJ-O", 145.75, "F1ZPJ · Saint-Avold · sortie RX · Grand Est v0.3 radio scope · validé 2026-08-22"),
    ("F1ZPJ-I", 145.15, "F1ZPJ · Saint-Avold · entrée RX · Grand Est v0.3 radio scope · validé 2026-08-22"),
    ("F5ZUD-O", 145.7125, "F5ZUD · Nancy / Vandoeuvre · sortie RX · F6KIM + REF · validé 2026-08-22"),
    ("F5ZUD-I", 145.1125, "F5ZUD · Nancy / Vandoeuvre · entrée RX · F6KIM + REF · validé 2026-08-22"),
    ("F1ZUV-A", 144.75, "F1ZUV · Strasbourg · crossband RX 144.750 · REF67 + REF · validé 2026-08-22"),
    ("F1ZUV-B", 439.75, "F1ZUV · Strasbourg · crossband RX 439.750 · REF67 + REF · validé 2026-08-22"),
    ("F5ZAW-A", 145.2125, "F5ZAW · Bellefosse / Champ du Feu · crossband RX 145.2125 · validé 2026-08-22"),
    ("F5ZAW-B", 433.425, "F5ZAW · Bellefosse / Champ du Feu · crossband RX 433.425 · validé 2026-08-22"),
    ("F5ZYS-A", 439.775, "F5ZYS · Dogneville / Bianlout · RX 439.775 · RA88 + REF · validé 2026-08-22"),
    ("F5ZYS-B", 430.375, "F5ZYS · Dogneville / Bianlout · RX 430.375 · RA88 + REF · validé 2026-08-22"),
    ("XBD-4325", 432.5375, "RF partagée crossband · F1ZEK/F5ZFT/F1ZGN/F1ZGP · dédupliquée une seule fois · validée 2026-08-22"),
    ("F1ZEK-V", 145.25, "F1ZEK · Ardennes / Monthermé · côté VHF RX · REF + ADRASEC08 · validé 2026-08-22"),
    ("F1ZXX-U", 432.775, "F1ZXX · Warcq · côté UHF RX · REF + ADRASEC08 · validé 2026-08-22"),
    ("F1ZXX-V", 145.4125, "F1ZXX · Warcq · côté VHF RX · REF + ADRASEC08 · validé 2026-08-22"),
    ("F5ZFT-V", 145.475, "F5ZFT · Saint-Menges · côté VHF RX · UHF 432.5375 partagé · validé 2026-08-22"),
    ("F1ZGN-V", 145.425, "F1ZGN · Sommedieue · côté VHF RX · UHF 432.5375 partagé · validé 2026-08-22"),
    ("F1ZGP-V", 145.2875, "F1ZGP · Bar-le-Duc · côté VHF RX · UHF 432.5375 partagé · validé 2026-08-22"),
    ("F5ZDJ-O", 430.275, "F5ZDJ · Verdun · sortie RX · REF + ADRASEC08 · validé 2026-08-22"),
    ("F5ZDJ-I", 431.875, "F5ZDJ · Verdun · entrée RX · REF + ADRASEC08 · validé 2026-08-22"),
    ("F1ZDA-O", 430.075, "F1ZDA · Petit Ballon · sortie RX · REF68 · validé 2026-08-22"),
    ("F1ZDA-I", 431.675, "F1ZDA · Petit Ballon · entrée RX · REF68 · validé 2026-08-22"),
    ("F1ZBV-O", 145.6625, "F1ZBV · Vosges · sortie RX · RA88 + REF · validé 2026-08-22"),
    ("F1ZBV-I", 145.0625, "F1ZBV · Vosges · entrée RX · RA88 + REF · validé 2026-08-22"),
    ("F1ZFL-O", 430.125, "F1ZFL · Erching · sortie RX · REF + AMRA57 · validé 2026-08-22"),
    ("F1ZFL-I", 431.725, "F1ZFL · Erching · entrée RX · REF + AMRA57 · validé 2026-08-22"),
    ("F5ZCC-O", 430.15, "F5ZCC · Theding · sortie RX · REF + AMRA57/F6KFT · validé 2026-08-22"),
    ("F5ZCC-I", 431.75, "F5ZCC · Theding · entrée RX · REF + AMRA57/F6KFT · validé 2026-08-22"),
    ("F1ZJS-O", 439.125, "F1ZJS · Tromborn · sortie RX · REF + AMRA57 · validé 2026-08-22"),
    ("F1ZJS-I", 431.525, "F1ZJS · Tromborn · entrée RX · REF + AMRA57 · validé 2026-08-22"),
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
    return [
        chirp_row(70 + index, name, frequency, "FM", 12.5, comment)
        for index, (name, frequency, comment) in enumerate(V03_REGIONAL)
    ]


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
    if record["status"] != "published_immutable" or record["version"] != "0.2" or int(record["memory_count"]) != 59:
        raise ValueError("Unexpected Grand Est v0.2 publication record")

    common = national_rows(root) + aviation_rows()
    base_rows = sorted(common + v02_regional_rows(), key=lambda item: int(item[0]))
    validate(base_rows, 59)
    base_bytes = csv_bytes(base_rows)
    base_sha = hashlib.sha256(base_bytes).hexdigest()
    if base_sha != record["public_csv_sha256"]:
        raise ValueError(f"Reconstructed public v0.2 SHA mismatch: {base_sha}")

    candidate_rows = sorted(common + v03_regional_rows(), key=lambda item: int(item[0]))
    validate(candidate_rows, 84)
    candidate_bytes = csv_bytes(candidate_rows)
    candidate_sha = hashlib.sha256(candidate_bytes).hexdigest()

    manifest = {
        "schema_version": "1.0",
        "status": "internal_candidate_radio_scope_frozen_aviation_gate_pending",
        "generated_on": "2026-08-22",
        "pack": "Grand Est",
        "target_version": "0.3",
        "published_base_version": "0.2",
        "published_base_memory_count": 59,
        "published_base_sha256": base_sha,
        "candidate_memory_count": 84,
        "candidate_aviation_memory_count": 19,
        "candidate_regional_radio_memory_count": 41,
        "candidate_sha256": candidate_sha,
        "candidate_csv": str(OUTPUT),
        "builder": "tools/build_grand_est_v03_candidate.py",
        "radio_scope": "research/grand-est-v0.3/radio-validation-pass3-2026-08-22.json",
        "airac_cycle_inherited_from_base": "08/26",
        "airac_valid_through_inclusive": "2026-09-02",
        "airac09_revalidation_required_on_or_after": "2026-09-03",
        "validation": {
            "public_base_sha_matches_frozen_record": True,
            "rx_only": True,
            "rf_deduplicated": True,
            "unique_locations": True,
            "unique_names": True,
            "memory_limit_passed": True,
            "radio_scope_frozen": True,
        },
        "aviation_publication_gate_complete": False,
        "review_checklist_complete": False,
        "publication_gates_zero_blockers": False,
        "public_export_allowed": False,
        "published": False,
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
            raise ValueError("Frozen Grand Est v0.3 candidate CSV differs from deterministic rebuild")
        frozen_manifest = load_json(manifest_path)
        if frozen_manifest != manifest:
            raise ValueError("Frozen Grand Est v0.3 candidate manifest differs from deterministic rebuild")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(candidate_bytes)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "GRAND EST V0.3 INTERNAL CANDIDATE: "
        f"84 RX, aviation=19, regional=41, sha256={manifest['candidate_sha256']}, public=false"
    )


if __name__ == "__main__":
    main()
