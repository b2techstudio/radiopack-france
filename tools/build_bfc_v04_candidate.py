#!/usr/bin/env python3
"""Build the internal Bourgogne-Franche-Comté v0.4 inland-VHF candidate.

The public BFC v0.3 route remains immutable and public. This builder consumes the
CSV produced by a fresh Astro production build, verifies its frozen publication
SHA-256, then appends only the seven verified inland-navigation VHF memories.
It does not publish or replace any public route.
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
BASE_RECORD = Path("research/bourgogne-franche-comte-v0.3/publication-record.json")
DEFAULT_BASE_CSV = Path(
    "website/dist/downloads/bourgogne-franche-comte/"
    "radiopack-france-bourgogne-franche-comte-v0.3.csv"
)
INLAND_DATA = Path("data/regional/bourgogne-franche-comte-inland-vhf-rx.json")
VALIDATION = Path("research/bourgogne-franche-comte-v0.4/inland-vhf-validation-2026-08-22.json")
OUTPUT = Path(
    "research/bourgogne-franche-comte-v0.4/generated/internal-candidate/"
    "radiopack-france-bourgogne-franche-comte-v0.4-candidate.csv"
)
MANIFEST = Path(
    "research/bourgogne-franche-comte-v0.4/generated/internal-candidate/"
    "candidate-manifest.json"
)

EXPECTED_BASE_SHA = "b5af25a6766b1181e735d376d3f70ab47ffb9ed67b9e38e35bee15e8a86ae7a5"
EXPECTED_BASE_COUNT = 54
EXPECTED_INLAND_COUNT = 7
EXPECTED_CANDIDATE_COUNT = 61
INLAND_LOCATION_START = 120

COLUMNS = [
    "Location", "Name", "Frequency", "Duplex", "Offset", "Tone",
    "rToneFreq", "cToneFreq", "DtcsCode", "DtcsPolarity", "RxDtcsCode",
    "CrossMode", "Mode", "TStep", "Skip", "Power", "Comment",
    "URCALL", "RPT1CALL", "RPT2CALL", "DVCODE",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_under(root: Path, path: Path) -> Path:
    return path if path.is_absolute() else root / path


def chirp_row(
    location: int,
    name: str,
    frequency: float,
    mode: str,
    step: float,
    comment: str,
) -> list[str]:
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
        raise ValueError("Unexpected BFC v0.3 CSV header")
    rows = list(reader)
    if len(rows) != EXPECTED_BASE_COUNT:
        raise ValueError(f"Expected {EXPECTED_BASE_COUNT} base memories, got {len(rows)}")
    if any(len(row) != len(COLUMNS) for row in rows):
        raise ValueError("Malformed BFC v0.3 CSV row")
    return rows


def inland_rows(root: Path) -> list[list[str]]:
    data = load_json(root / INLAND_DATA)
    channels = data.get("channels", [])
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


def build(root: Path, base_csv: Path = DEFAULT_BASE_CSV) -> tuple[bytes, dict[str, Any]]:
    record = load_json(root / BASE_RECORD)
    if record.get("status") != "published_immutable" or record.get("version") != "0.3":
        raise ValueError("Unexpected BFC v0.3 publication record")
    if int(record.get("memory_count", -1)) != EXPECTED_BASE_COUNT:
        raise ValueError("Unexpected BFC v0.3 memory count")
    if record.get("public_csv_sha256") != EXPECTED_BASE_SHA:
        raise ValueError("Unexpected BFC v0.3 publication-record SHA")

    validation = load_json(root / VALIDATION)
    if validation.get("status") != "minimum_verified_internal_candidate_scope_closed":
        raise ValueError("BFC v0.4 inland validation is not ready for internal candidate build")
    if validation.get("gates", {}).get("public_export_allowed") is not False:
        raise ValueError("Internal candidate unexpectedly marked public")

    base_path = resolve_under(root, base_csv)
    if not base_path.is_file():
        raise ValueError(f"BFC v0.3 built CSV not found: {base_path}")
    base_raw = base_path.read_bytes()
    base_sha = hashlib.sha256(base_raw).hexdigest()
    if base_sha != EXPECTED_BASE_SHA:
        raise ValueError(f"BFC v0.3 public CSV SHA mismatch: {base_sha}")

    base_rows = parse_base_csv(base_raw)
    additions = inland_rows(root)
    rows = sorted(base_rows + additions, key=lambda row: int(row[0]))
    validate(rows)

    candidate = csv_bytes(rows)
    candidate_sha = hashlib.sha256(candidate).hexdigest()
    manifest = {
        "schema_version": "1.0",
        "status": "internal_candidate_reproducible",
        "generated_on": "2026-08-22",
        "pack": "Bourgogne-Franche-Comté",
        "target_version": "0.4",
        "published_base_version": "0.3",
        "published_base_memory_count": EXPECTED_BASE_COUNT,
        "published_base_sha256": base_sha,
        "base_csv_source": str(DEFAULT_BASE_CSV),
        "candidate_memory_count": EXPECTED_CANDIDATE_COUNT,
        "candidate_inland_vhf_memory_count": EXPECTED_INLAND_COUNT,
        "candidate_memory_delta": EXPECTED_INLAND_COUNT,
        "candidate_sha256": candidate_sha,
        "candidate_csv": str(OUTPUT),
        "builder": "tools/build_bfc_v04_candidate.py",
        "inland_validation": str(VALIDATION),
        "inland_dataset": str(INLAND_DATA),
        "validation": {
            "public_base_sha_matches_frozen_record": True,
            "base_rows_preserved": rows[:EXPECTED_BASE_COUNT] == base_rows,
            "rx_only": True,
            "rf_deduplicated": True,
            "unique_locations": True,
            "unique_names": True,
            "memory_limit_passed": True,
            "inland_scope_minimum_verified": True,
        },
        "public_export_allowed": False,
        "published": False,
        "immutable": False,
    }
    return candidate, manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--base-csv", type=Path, default=DEFAULT_BASE_CSV)
    parser.add_argument("--write", action="store_true", help="write internal candidate and manifest")
    parser.add_argument("--check", action="store_true", help="compare against candidate written in this workspace")
    args = parser.parse_args()

    root = args.root.resolve()
    candidate, manifest = build(root, args.base_csv)
    output = root / OUTPUT
    manifest_path = root / MANIFEST

    if args.write:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(candidate)
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    if args.check:
        if not output.is_file() or output.read_bytes() != candidate:
            raise ValueError("Workspace BFC v0.4 candidate differs from deterministic rebuild")
        if not manifest_path.is_file() or load_json(manifest_path) != manifest:
            raise ValueError("Workspace BFC v0.4 manifest differs from deterministic rebuild")

    print(
        "BFC V0.4 INTERNAL CANDIDATE: "
        f"{EXPECTED_CANDIDATE_COUNT} RX, inland={EXPECTED_INLAND_COUNT}, "
        f"sha256={manifest['candidate_sha256']}, public=false"
    )


if __name__ == "__main__":
    main()
