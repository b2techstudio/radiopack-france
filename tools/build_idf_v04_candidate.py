#!/usr/bin/env python3
"""Build the deterministic Île-de-France v0.4 inland-VHF publication basis.

Île-de-France v0.3 is immutable. This builder reads that exact public CSV,
verifies its SHA-256 against the frozen publication record, then adds only the
validated 7-memory inland-navigation VHF block. The resulting bytes are the
immutable Île-de-France v0.4 publication basis.
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
BASE_RECORD = Path("research/ile-de-france-v0.3/publication-record.json")
BASE_PUBLIC = Path("website/public/downloads/ile-de-france/radiopack-france-ile-de-france-v0.3.csv")
INLAND_DATA = Path("data/regional/ile-de-france-inland-vhf-rx.json")
OUTPUT = Path("research/ile-de-france-v0.4/generated/release-candidate/radiopack-france-ile-de-france-v0.4-candidate.csv")
MANIFEST = Path("research/ile-de-france-v0.4/generated/release-candidate/candidate-manifest.json")
PUBLIC = Path("website/public/downloads/ile-de-france/radiopack-france-ile-de-france-v0.4.csv")

EXPECTED_BASE_SHA = "e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125"
EXPECTED_BASE_COUNT = 57
EXPECTED_INLAND_COUNT = 7
EXPECTED_CANDIDATE_COUNT = 64
EXPECTED_PUBLIC_SHA = "14e1d1d95b38ef44d01b9cccb989a3f1567153ac64875594cc24bd4b57a1cdc2"
INLAND_LOCATION_START = 120

COLUMNS = [
    "Location", "Name", "Frequency", "Duplex", "Offset", "Tone",
    "rToneFreq", "cToneFreq", "DtcsCode", "DtcsPolarity", "RxDtcsCode",
    "CrossMode", "Mode", "TStep", "Skip", "Power", "Comment",
    "URCALL", "RPT1CALL", "RPT2CALL", "DVCODE",
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


def parse_base_csv(raw: bytes) -> list[list[str]]:
    reader = csv.reader(io.StringIO(raw.decode("utf-8"), newline=""))
    header = next(reader)
    if header != COLUMNS:
        raise ValueError("Unexpected Île-de-France v0.3 CSV header")
    rows = [row for row in reader]
    if len(rows) != EXPECTED_BASE_COUNT:
        raise ValueError(f"Expected {EXPECTED_BASE_COUNT} base memories, got {len(rows)}")
    if any(len(row) != len(COLUMNS) for row in rows):
        raise ValueError("Malformed Île-de-France v0.3 CSV row")
    return rows


def inland_rows(root: Path) -> list[list[str]]:
    data = load_json(root / INLAND_DATA)
    channels = data["channels"]
    if len(channels) != EXPECTED_INLAND_COUNT:
        raise ValueError(f"Expected {EXPECTED_INLAND_COUNT} inland channels, got {len(channels)}")
    return [
        chirp_row(
            INLAND_LOCATION_START + index,
            channel["name"],
            float(channel["frequency_mhz"]),
            channel["mode"],
            float(channel["step_khz"]),
            channel["comment"],
        )
        for index, channel in enumerate(channels)
    ]


def validate(rows: list[list[str]]) -> None:
    if len(rows) != EXPECTED_CANDIDATE_COUNT:
        raise ValueError(f"Expected {EXPECTED_CANDIDATE_COUNT} memories, got {len(rows)}")
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
    if any(len(name) > 10 for name in names):
        raise ValueError("CHIRP name exceeds 10 characters")
    if not all(row[3] == "off" and row[4] == "0.000000" for row in rows):
        raise ValueError("RX-only contract violated")


def build(root: Path) -> tuple[bytes, dict[str, Any]]:
    record = load_json(root / BASE_RECORD)
    if record.get("status") != "published_immutable" or record.get("version") != "0.3":
        raise ValueError("Unexpected Île-de-France v0.3 publication record")
    if int(record.get("memory_count", -1)) != EXPECTED_BASE_COUNT:
        raise ValueError("Unexpected Île-de-France v0.3 memory count")
    if record.get("public_csv_sha256") != EXPECTED_BASE_SHA:
        raise ValueError("Unexpected Île-de-France v0.3 publication-record SHA")

    base_raw = (root / BASE_PUBLIC).read_bytes()
    base_sha = hashlib.sha256(base_raw).hexdigest()
    if base_sha != EXPECTED_BASE_SHA:
        raise ValueError(f"Île-de-France v0.3 public CSV SHA mismatch: {base_sha}")

    base_rows = parse_base_csv(base_raw)
    additions = inland_rows(root)
    rows = sorted(base_rows + additions, key=lambda row: int(row[0]))
    validate(rows)

    candidate = csv_bytes(rows)
    candidate_sha = hashlib.sha256(candidate).hexdigest()
    if candidate_sha != EXPECTED_PUBLIC_SHA:
        raise ValueError(f"Île-de-France v0.4 publication SHA mismatch: {candidate_sha}")

    manifest = {
        "schema_version": "1.0",
        "status": "published_basis_immutable",
        "generated_on": "2026-08-22",
        "published_on": "2026-08-22",
        "pack": "Île-de-France",
        "target_version": "0.4",
        "published_base_version": "0.3",
        "published_base_memory_count": EXPECTED_BASE_COUNT,
        "published_base_sha256": base_sha,
        "candidate_memory_count": EXPECTED_CANDIDATE_COUNT,
        "candidate_aviation_memory_count": 18,
        "candidate_regional_radio_memory_count": 15,
        "candidate_inland_vhf_memory_count": EXPECTED_INLAND_COUNT,
        "candidate_memory_delta": EXPECTED_INLAND_COUNT,
        "candidate_sha256": candidate_sha,
        "public_csv_sha256": candidate_sha,
        "candidate_csv": str(OUTPUT),
        "public_csv": str(PUBLIC),
        "builder": "tools/build_idf_v04_candidate.py",
        "inland_validation": "research/ile-de-france-v0.4/inland-vhf-validation-2026-08-22.json",
        "inland_dataset": str(INLAND_DATA),
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
            "inland_scope_frozen": True,
            "candidate_public_sha_equal": True,
        },
        "public_export_allowed": True,
        "published": True,
        "immutable": True,
    }
    return candidate, manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--write", action="store_true", help="write publication-basis candidate and manifest")
    parser.add_argument("--check", action="store_true", help="compare against frozen candidate, manifest and public CSV")
    args = parser.parse_args()
    root = args.root.resolve()
    candidate, manifest = build(root)
    output = root / OUTPUT
    manifest_path = root / MANIFEST
    public_path = root / PUBLIC

    if args.write:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(candidate)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.check:
        if not output.is_file() or output.read_bytes() != candidate:
            raise ValueError("Frozen Île-de-France v0.4 candidate CSV differs from deterministic rebuild")
        if not manifest_path.is_file() or load_json(manifest_path) != manifest:
            raise ValueError("Frozen Île-de-France v0.4 candidate manifest differs from deterministic rebuild")
        if not public_path.is_file() or public_path.read_bytes() != candidate:
            raise ValueError("Public Île-de-France v0.4 CSV differs from deterministic publication basis")

    print(
        "IDF V0.4 PUBLISHED BASIS: "
        f"{EXPECTED_CANDIDATE_COUNT} RX, aviation=18, regional=15, inland={EXPECTED_INLAND_COUNT}, "
        f"sha256={manifest['candidate_sha256']}, public=true"
    )


if __name__ == "__main__":
    main()
