#!/usr/bin/env python3
"""Build Bretagne v0.3 initial internal candidate from immutable public v0.2."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_V02 = Path("website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv")
PUBLICATION_RECORD = Path("research/bretagne-v0.2/publication-record.json")
PLAN = Path("research/bretagne-v0.3/pack-plan.json")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def build_candidate(root: Path) -> dict[str, Any]:
    public_path = root / PUBLIC_V02
    record = load_json(root / PUBLICATION_RECORD)
    plan = load_json(root / PLAN)
    public_bytes = public_path.read_bytes()
    public_sha = hashlib.sha256(public_bytes).hexdigest()

    if record["status"] != "published_immutable":
        raise ValueError("Bretagne v0.2 publication record is not immutable")
    if record["version"] != "0.2" or int(record["memory_count"]) != 151:
        raise ValueError("Unexpected Bretagne v0.2 publication record")
    if record["public_csv_sha256"] != public_sha:
        raise ValueError("Bretagne v0.2 public CSV SHA-256 does not match publication record")
    if plan["target_version"] != "0.3" or plan["based_on_published_version"] != "0.2":
        raise ValueError("Unexpected Bretagne v0.3 plan")
    if plan["published_base_sha256"] != public_sha:
        raise ValueError("Bretagne v0.3 plan base SHA-256 does not match public v0.2")

    with public_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 151:
        raise ValueError(f"Expected 151 public base memories, got {len(rows)}")
    if not all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows):
        raise ValueError("Public v0.2 base violates RX-only CHIRP contract")
    if len({int(row["Location"]) for row in rows}) != 151:
        raise ValueError("Duplicate CHIRP locations in public v0.2 base")
    if len({row["Name"] for row in rows}) != 151:
        raise ValueError("Duplicate CHIRP names in public v0.2 base")
    if len({round(float(row["Frequency"]), 6) for row in rows}) != 151:
        raise ValueError("Duplicate RF frequencies in public v0.2 base")

    return {
        "schema_version": "1.0",
        "pack": "Bretagne",
        "target_version": "0.3",
        "status": "initial_internal_candidate_exact_public_v0_2_base_not_for_publication",
        "updated": "2026-08-12",
        "public_export_allowed": False,
        "published_base_version": "0.2",
        "published_base_memory_count": 151,
        "published_base_sha256": public_sha,
        "memory_count": 151,
        "new_memory_count": 0,
        "aviation_baseline_cycle": "AIRAC 08/26",
        "aviation_baseline_valid_through_inclusive": "2026-09-02",
        "next_airac_cycle": "AIRAC 09/26",
        "next_airac_effective_from": "2026-09-03",
        "rules": {
            "rx_only": True,
            "chirp_duplex": "off",
            "chirp_offset": "0.000000",
            "same_rf_frequency_deduplicated": True,
            "published_v0_2_immutable": True,
            "no_artificial_fill": True,
            "public_pack_mutation_allowed": False,
            "post_2026_09_02_aviation_publication_requires_revalidation": True,
        },
        "rows": rows,
    }


def write_candidate(candidate: dict[str, Any], output_dir: Path, root: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "bretagne-v0.3-internal.csv"
    json_path = output_dir / "bretagne-v0.3-internal.json"
    csv_path.write_bytes((root / PUBLIC_V02).read_bytes())
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
        default=Path("research/bretagne-v0.3/generated/internal-candidate"),
    )
    args = parser.parse_args()
    root = args.root.resolve()
    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = root / output_dir
    candidate = build_candidate(root)
    write_candidate(candidate, output_dir, root)
    print(
        "BRETAGNE V0.3 INITIAL INTERNAL CANDIDATE: "
        f"{candidate['memory_count']} RX memories, delta=0, exact public v0.2 base, public=false"
    )


if __name__ == "__main__":
    main()
