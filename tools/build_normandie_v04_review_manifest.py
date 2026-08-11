#!/usr/bin/env python3
"""Build a byte-level fingerprint manifest for the non-public Normandie v0.4 review inputs."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.4/generated/review-manifest")
REVIEWED_INPUTS = [
    "research/normandie-v0.4/candidate-memory-delta.json",
    "research/normandie-v0.4/internal-candidate-map.json",
    "research/normandie-v0.4/promotion-gates.json",
    "research/normandie-v0.4/blocked-station-revalidation.json",
    "research/normandie-v0.4/external-evidence-matrix.json",
    "research/normandie-v0.4/source-consistency-contract.json",
    "research/normandie-v0.4/source-freshness-policy.json",
    "research/normandie-v0.4/r3-mortain-field-validation.json",
    "research/normandie-v0.4/f5zha-mortain-validation.json",
    "research/normandie-v0.4/release-scope.json",
    "research/normandie-v0.4/pack-plan.json",
    "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv",
    "website/src/lib/packRegistry.ts",
]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(data: dict[str, Any]) -> bytes:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def build(root: Path, as_of: date | None = None) -> dict[str, Any]:
    snapshot = load_module("review_manifest_snapshot", root / "tools/build_normandie_v04_review_snapshot.py").build(root, as_of)
    candidate_builder = load_module("review_manifest_candidate", root / "tools/build_normandie_v04_internal_candidate.py")
    preview_builder = load_module("review_manifest_preview", root / "tools/build_normandie_v04_candidate_preview.py")
    candidate_manifest, candidate_bytes = candidate_builder.build_candidate(root)
    preview_manifest, preview_bytes = preview_builder.build_preview(root)

    file_hashes: dict[str, str] = {}
    for relative in REVIEWED_INPUTS:
        path = root / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        file_hashes[relative] = sha256(path.read_bytes())

    body = {
        "schema_version": "1.0",
        "status": "review_fingerprint_manifest_not_public",
        "as_of": snapshot["as_of"],
        "review_snapshot_id": snapshot["snapshot_id"],
        "reviewed_input_count": len(file_hashes),
        "reviewed_input_sha256": file_hashes,
        "internal_candidate_memory_count": candidate_manifest["memory_count"],
        "internal_candidate_sha256": sha256(candidate_bytes),
        "guarded_preview_memory_count": preview_manifest["preview_memory_count"],
        "guarded_preview_sha256": sha256(preview_bytes),
        "public_export_allowed": False,
        "rules": {
            "manifest_is_integrity_evidence_only": True,
            "all_hashes_are_sha256": True,
            "manifest_does_not_mutate_candidate": True,
            "manifest_does_not_publish": True,
            "pack_registry_is_reviewed_for_public_absence_or_later_explicit_change": True,
        },
    }
    return {**body, "manifest_id": sha256(canonical_bytes(body))}


def markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Normandie v0.4 — manifeste d'empreintes de revue",
        "",
        f"- Manifest : `{data['manifest_id']}`",
        f"- Snapshot : `{data['review_snapshot_id']}`",
        f"- Entrées suivies : **{data['reviewed_input_count']}**",
        f"- Candidat : **{data['internal_candidate_memory_count']}** mémoires — `{data['internal_candidate_sha256']}`",
        f"- Preview : **{data['guarded_preview_memory_count']}** mémoires — `{data['guarded_preview_sha256']}`",
        "",
        "## Empreintes des entrées",
        "",
    ]
    for path, digest in data["reviewed_input_sha256"].items():
        lines.append(f"- `{path}` — `{digest}`")
    lines.extend(["", "Ce manifeste permet de détecter une dérive après capture d'une revue ; il ne publie rien.", ""])
    return "\n".join(lines)


def write(root: Path, output_dir: Path, as_of: date | None = None) -> tuple[Path, Path, dict[str, Any]]:
    data = build(root, as_of)
    output_dir.mkdir(parents=True, exist_ok=True)
    jp = output_dir / "normandie-v04-review-manifest.json"
    mp = output_dir / "normandie-v04-review-manifest.md"
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
        "NORMANDIE V0.4 REVIEW MANIFEST: "
        f"id={data['manifest_id'][:12]} inputs={data['reviewed_input_count']} "
        f"candidate={data['internal_candidate_memory_count']} preview={data['guarded_preview_memory_count']} public=false"
    )
    print(jp)
    print(mp)


if __name__ == "__main__":
    main()
