#!/usr/bin/env python3
"""Audit frozen Bretagne v0.2 candidate; never writes public files."""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--require-prepublication-ready", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    research = root / "research/bretagne-v0.2"

    maturity = load_json(research / "maturity-review.json")
    scope = load_json(research / "release-scope.json")
    checklist = load_json(research / "review-checklist.json")
    gates = load_json(research / "publication-gates.json")
    aviation = load_json(research / "aviation-airac-08.json")

    errors: list[str] = []

    if maturity["candidate_memory_count"] != 151:
        errors.append("maturity candidate count not 151")
    if maturity["release_blockers"] != []:
        errors.append("maturity review still has release blockers")
    if maturity["prepublication_ready"] is not True:
        errors.append("maturity review not prepublication ready")
    if scope["final_candidate_memory_count"] != 151 or scope["prepublication_ready"] is not True:
        errors.append("release scope is not frozen/prepublication ready at 151")
    if checklist["completed"] != 10 or checklist["total"] != 10 or checklist["blocker_count"] != 0:
        errors.append("review checklist incomplete")
    if checklist["prepublication_ready"] is not True:
        errors.append("review checklist not prepublication ready")
    if gates["prepublication_ready"] is not True or gates["public_release_allowed"] is not False:
        errors.append("publication gates have unexpected state")

    cycle = aviation["cycle"]
    if cycle["validation_cycle"] != "AIRAC 08/26":
        errors.append("unexpected aviation AIRAC cycle")
    if cycle["effective_from"] != "2026-08-06" or cycle["effective_until_inclusive"] != "2026-09-02":
        errors.append("unexpected aviation validity window")
    if cycle["current_xml_export_bytes_extracted_in_repository_workflow"] is not False:
        errors.append("audit assumptions changed: XML extraction unexpectedly true")
    if aviation["methodology"]["does_not_claim_current_xml_field_match_without_xml_extraction"] is not True:
        errors.append("aviation methodology no longer guards unperformed XML field match")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        subprocess.run(
            [
                sys.executable,
                str(root / "tools/build_bretagne_v02_internal_candidate.py"),
                "--root",
                str(root),
                "--output-dir",
                str(temp),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        csv_path = temp / "bretagne-v0.2-internal.csv"
        json_path = temp / "bretagne-v0.2-internal.json"
        with csv_path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        candidate = load_json(json_path)

    if len(rows) != 151 or candidate["memory_count"] != 151:
        errors.append("candidate row count mismatch")
    if candidate["new_memory_count"] != 16 or candidate["aviation_memory_count"] != 16:
        errors.append("candidate aviation delta mismatch")
    if candidate["public_export_allowed"] is not False:
        errors.append("internal candidate unexpectedly allows public export")
    if any(row["Duplex"] != "off" or row["Offset"] != "0.000000" for row in rows):
        errors.append("RX-only CHIRP contract broken")
    if len({round(float(row["Frequency"]), 6) for row in rows}) != 151:
        errors.append("duplicate RF in candidate")
    if any(len(row["Name"]) > 10 for row in rows):
        errors.append("memory name longer than 10 characters")

    aviation_memories = [
        item for item in candidate["memories"]
        if item["channel"].get("candidate_block") == "Aviation Bretagne AIRAC 08/26"
    ]
    if len(aviation_memories) != 16:
        errors.append("candidate does not contain exactly 16 aviation memories")
    for item in aviation_memories:
        channel = item["channel"]
        if channel.get("mode") != "AM" or float(channel.get("step_khz", 0)) != 8.33:
            errors.append(f"invalid aviation mode/step: {channel.get('name')}")
        if channel.get("tx_policy") != "rx_only":
            errors.append(f"aviation TX policy broken: {channel.get('name')}")

    public_v02 = root / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"
    if public_v02.exists():
        errors.append("public Bretagne v0.2 CSV exists before publication sprint")
    registry = (root / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
    if "radiopack-france-bretagne-v0.2.csv" in registry:
        errors.append("public registry already points to Bretagne v0.2")

    ready = not errors and all(
        item is True
        for item in (
            maturity["prepublication_ready"],
            scope["prepublication_ready"],
            checklist["prepublication_ready"],
            gates["prepublication_ready"],
        )
    )
    result = {
        "schema_version": "1.0",
        "status": "prepublication_audit_not_public",
        "memory_count": 151,
        "review": "10/10",
        "blocker_count": len(errors),
        "errors": errors,
        "prepublication_ready": ready,
        "public_export_allowed": False,
    }
    output = research / "generated/prepublication-audit"
    output.mkdir(parents=True, exist_ok=True)
    (output / "bretagne-v02-prepublication-audit.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        "BRETAGNE V0.2 PREPUBLICATION AUDIT: "
        f"integrity={'OK' if not errors else 'FAIL'} review=10/10 "
        f"blockers={len(errors)} prepublication_ready={str(ready).lower()}"
    )
    if errors or (args.require_prepublication_ready and not ready):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
