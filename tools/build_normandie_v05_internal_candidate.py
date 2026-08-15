#!/usr/bin/env python3
"""Build Normandie v0.5 internal candidate from immutable public v0.4."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_V04 = Path("website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv")
PUBLICATION_RECORD = Path("research/normandie-v0.4/publication-record.json")
PLAN = Path("research/normandie-v0.5/pack-plan.json")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def build_candidate(root: Path) -> dict[str, Any]:
    public_path = root / PUBLIC_V04
    record = load_json(root / PUBLICATION_RECORD)
    plan = load_json(root / PLAN)
    public_bytes = public_path.read_bytes()
    public_sha = hashlib.sha256(public_bytes).hexdigest()

    if record["status"] != "published_immutable":
        raise ValueError("Normandie v0.4 publication record is not immutable")
    if record["version"] != "0.4" or int(record["memory_count"]) != 142:
        raise ValueError("Unexpected Normandie v0.4 publication record")
    if record["public_csv_sha256"] != public_sha:
        raise ValueError("Normandie v0.4 public CSV SHA-256 does not match publication record")
    if plan["target_version"] != "0.5" or plan["based_on_published_version"] != "0.4":
        raise ValueError("Unexpected Normandie v0.5 plan")
    if plan.get("published_base_sha256") not in (None, public_sha):
        raise ValueError("Normandie v0.5 plan base SHA-256 does not match public v0.4")

    with public_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 142:
        raise ValueError(f"Expected 142 public base memories, got {len(rows)}")
    if not all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows):
        raise ValueError("Public Normandie v0.4 base violates RX-only CHIRP contract")
    if len({int(row["Location"]) for row in rows}) != 142:
        raise ValueError("Duplicate CHIRP locations in public Normandie v0.4 base")
    if len({row["Name"] for row in rows}) != 142:
        raise ValueError("Duplicate CHIRP names in public Normandie v0.4 base")
    if len({round(float(row["Frequency"]), 6) for row in rows}) != 142:
        raise ValueError("Duplicate RF frequencies in public Normandie v0.4 base")

    return {
        "schema_version": "1.0",
        "pack": "Normandie",
        "target_version": "0.5",
        "status": "internal_candidate_exact_public_v0_4_base_not_for_publication",
        "updated": "2026-08-15",
        "public_export_allowed": False,
        "published_base_version": "0.4",
        "published_base_memory_count": 142,
        "published_base_sha256": public_sha,
        "memory_count": 142,
        "new_memory_count": 0,
        "known_potential_ceiling_excluding_f6zes": 147,
        "rules": {
            "rx_only": True,
            "chirp_duplex": "off",
            "chirp_offset": "0.000000",
            "same_rf_frequency_deduplicated": True,
            "published_v0_4_immutable": True,
            "no_artificial_fill": True,
            "public_pack_mutation_allowed": False,
            "field_evidence_required_where_gate_demands_it": True,
            "unresolved_frequency_must_not_be_guessed": True,
        },
        "rows": rows,
    }


def write_candidate(candidate: dict[str, Any], output_dir: Path, root: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "normandie-v0.5-internal.csv"
    json_path = output_dir / "normandie-v0.5-internal.json"
    csv_path.write_bytes((root / PUBLIC_V04).read_bytes())
    json_path.write_text(
        json.dumps(candidate, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("research/normandie-v0.5/generated/internal-candidate"),
    )
    args = parser.parse_args()
    root = args.root.resolve()
    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = root / output_dir
    candidate = build_candidate(root)
    write_candidate(candidate, output_dir, root)
    print(
        "NORMANDIE V0.5 INTERNAL CANDIDATE: "
        f"{candidate['memory_count']} RX memories, delta=0, exact public v0.4 base, public=false"
    )


if __name__ == "__main__":
    main()
