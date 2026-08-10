#!/usr/bin/env python3
"""Build a non-public dry-run preview of the Normandie v0.4 candidate plus eligible gated additions."""
from __future__ import annotations

import argparse
import csv
import importlib.util
import io
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.4/generated/candidate-preview")
NAME_MAP = {"ZBX-IN": "35-ZBX-IN", "ZBX-OUT": "35-ZBX-OUT", "ZHA-A": "53-ZHA-A", "ZHA-B": "53-ZHA-B", "ZOV-B": "50-ZOV-B"}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def preview_row(addition: dict[str, Any]) -> dict[str, str]:
    name = NAME_MAP[addition["name_hint"]]
    if len(name) > 10:
        raise ValueError("Preview memory name exceeds 10 characters")
    return {
        "Location": str(addition["proposed_internal_location"]),
        "Name": name,
        "Frequency": f"{float(addition['frequency_mhz']):.6f}",
        "Duplex": "off",
        "Offset": "0.000000",
        "Tone": "",
        "rToneFreq": "88.5",
        "cToneFreq": "88.5",
        "DtcsCode": "023",
        "DtcsPolarity": "NN",
        "RxDtcsCode": "023",
        "CrossMode": "Tone->Tone",
        "Mode": "NFM",
        "TStep": "12.50",
        "Skip": "",
        "Power": "",
        "Comment": f"Preview {addition['role']} - RX seule - non public",
        "URCALL": "",
        "RPT1CALL": "",
        "RPT2CALL": "",
        "DVCODE": "",
    }


def build_preview(root: Path, plan_override: dict[str, Any] | None = None) -> tuple[dict[str, Any], bytes]:
    candidate_builder = load_module("candidate_builder_preview", root / "tools/build_normandie_v04_internal_candidate.py")
    promotion_builder = load_module("promotion_builder_preview", root / "tools/build_normandie_v04_internal_promotion_plan.py")
    base_manifest, base_bytes = candidate_builder.build_candidate(root)
    plan = plan_override if plan_override is not None else promotion_builder.build_plan(root)
    if plan["public_export_allowed"] is not False or plan["plan_applied"] is not False:
        raise ValueError("Promotion preview requires a non-public unapplied plan")

    rows = list(csv.DictReader(io.StringIO(base_bytes.decode("utf-8"))))
    locations = {int(r["Location"]) for r in rows}
    names = {r["Name"] for r in rows}
    freqs = {round(float(r["Frequency"]), 6) for r in rows}

    additions = []
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=candidate_builder.CHIRP_COLUMNS, lineterminator="\n")
    for item in plan["additions"]:
        row = preview_row(item)
        loc = int(row["Location"])
        freq = round(float(row["Frequency"]), 6)
        if loc in locations or row["Name"] in names or freq in freqs:
            raise ValueError("Preview addition collides with existing candidate")
        locations.add(loc); names.add(row["Name"]); freqs.add(freq)
        writer.writerow(row)
        additions.append({"location": loc, "name": row["Name"], "frequency_mhz": freq, "gate_id": item["gate_id"]})

    preview_bytes = base_bytes + buffer.getvalue().encode("utf-8")
    manifest = {
        "schema_version": "1.0",
        "status": "guarded_candidate_preview_not_public",
        "base_internal_candidate_memory_count": base_manifest["memory_count"],
        "eligible_addition_count": len(additions),
        "preview_memory_count": base_manifest["memory_count"] + len(additions),
        "additions": additions,
        "candidate_mutated": False,
        "plan_applied": False,
        "public_export_allowed": False,
        "rules": {
            "preview_only": True,
            "published_base_is_exact_prefix": True,
            "chirp_duplex": "off",
            "chirp_offset": "0.000000",
            "tx_disabled": True,
            "final_public_positions_not_defined": True
        }
    }
    return manifest, preview_bytes


def write(root: Path, output_dir: Path) -> tuple[Path, Path, dict[str, Any]]:
    manifest, data = build_preview(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    jp = output_dir / "normandie-v04-candidate-preview.json"
    cp = output_dir / "normandie-v04-candidate-preview.csv"
    jp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cp.write_bytes(data)
    return jp, cp, manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    root = args.root.resolve()
    out = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    jp, cp, m = write(root, out)
    print(f"NORMANDIE V0.4 PREVIEW: {m['preview_memory_count']} memories; eligible={m['eligible_addition_count']}; public=false")
    print(jp)
    print(cp)


if __name__ == "__main__":
    main()
