#!/usr/bin/env python3
"""Build a non-public structural diff between published v0.3.1, internal v0.4 candidate and guarded preview."""
from __future__ import annotations

import argparse
import csv
import importlib.util
import io
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.4/generated/candidate-diff")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rows(data: bytes) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(data.decode("utf-8"))))


def compact(row: dict[str, str]) -> dict[str, Any]:
    return {
        "location": int(row["Location"]),
        "name": row["Name"],
        "frequency_mhz": float(row["Frequency"]),
        "duplex": row["Duplex"],
        "offset": row["Offset"],
        "mode": row["Mode"],
    }


def build(root: Path) -> dict[str, Any]:
    candidate_builder = load_module("candidate_builder_diff", root / "tools/build_normandie_v04_internal_candidate.py")
    preview_builder = load_module("preview_builder_diff", root / "tools/build_normandie_v04_candidate_preview.py")

    candidate_manifest, candidate_bytes = candidate_builder.build_candidate(root)
    preview_manifest, preview_bytes = preview_builder.build_preview(root)
    candidate_rows = rows(candidate_bytes)
    preview_rows = rows(preview_bytes)

    if preview_rows[: len(candidate_rows)] != candidate_rows:
        raise ValueError("Guarded preview rewrites the current internal candidate")
    if candidate_manifest["published_base_is_exact_prefix"] is not True:
        raise ValueError("Internal candidate no longer preserves published v0.3.1 as exact prefix")

    current_additions = candidate_rows[candidate_manifest["base_memory_count"] :]
    future_additions = preview_rows[len(candidate_rows) :]
    for row in current_additions + future_additions:
        if row["Duplex"] != "off" or row["Offset"] != "0.000000":
            raise ValueError("Candidate diff found a non RX-only addition")

    return {
        "schema_version": "1.0",
        "status": "candidate_structural_diff_not_public",
        "published_base_memory_count": candidate_manifest["base_memory_count"],
        "current_internal_candidate_memory_count": candidate_manifest["memory_count"],
        "current_internal_addition_count": len(current_additions),
        "current_internal_additions": [compact(row) for row in current_additions],
        "guarded_preview_memory_count": preview_manifest["preview_memory_count"],
        "currently_eligible_future_addition_count": len(future_additions),
        "currently_eligible_future_additions": [compact(row) for row in future_additions],
        "published_base_is_exact_prefix_of_internal_candidate": True,
        "internal_candidate_is_exact_prefix_of_guarded_preview": True,
        "candidate_mutated": False,
        "public_export_allowed": False,
        "rules": {
            "diff_is_report_only": True,
            "all_reported_additions_must_be_rx_only": True,
            "published_base_rows_must_never_be_rewritten": True,
            "preview_rows_must_not_rewrite_internal_candidate": True,
            "final_public_positions_not_defined": True,
        },
    }


def markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Normandie v0.4 — diff structurel",
        "",
        f"- Base publique figée : **{data['published_base_memory_count']} mémoires**",
        f"- Candidat interne : **{data['current_internal_candidate_memory_count']} mémoires**",
        f"- Ajouts internes actuels : **{data['current_internal_addition_count']}**",
        f"- Preview gardé : **{data['guarded_preview_memory_count']} mémoires**",
        f"- Ajouts futurs actuellement éligibles : **{data['currently_eligible_future_addition_count']}**",
        "",
        "## Ajouts internes actuels",
        "",
    ]
    for row in data["current_internal_additions"]:
        lines.append(f"- {row['location']} — `{row['name']}` — {row['frequency_mhz']:.6f} MHz")
    lines.extend(["", "## Ajouts futurs actuellement éligibles", ""])
    if data["currently_eligible_future_additions"]:
        for row in data["currently_eligible_future_additions"]:
            lines.append(f"- {row['location']} — `{row['name']}` — {row['frequency_mhz']:.6f} MHz")
    else:
        lines.append("- Aucun.")
    lines.extend(["", "Aucune donnée publique ou candidate n'est modifiée par ce rapport.", ""])
    return "\n".join(lines)


def write(root: Path, output_dir: Path) -> tuple[Path, Path, dict[str, Any]]:
    data = build(root)
    output_dir.mkdir(parents=True, exist_ok=True)
    jp = output_dir / "normandie-v04-candidate-diff.json"
    mp = output_dir / "normandie-v04-candidate-diff.md"
    jp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mp.write_text(markdown(data), encoding="utf-8")
    return jp, mp, data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    root = args.root.resolve()
    out = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    jp, mp, data = write(root, out)
    print(
        "NORMANDIE V0.4 CANDIDATE DIFF: "
        f"published={data['published_base_memory_count']} "
        f"internal={data['current_internal_candidate_memory_count']} "
        f"preview={data['guarded_preview_memory_count']} "
        f"eligible={data['currently_eligible_future_addition_count']} public=false"
    )
    print(jp)
    print(mp)


if __name__ == "__main__":
    main()
