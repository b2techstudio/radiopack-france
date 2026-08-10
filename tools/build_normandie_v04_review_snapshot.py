#!/usr/bin/env python3
"""Build a deterministic non-public Normandie v0.4 review snapshot."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.4/generated/review-snapshot")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(data: dict[str, Any]) -> bytes:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def build(root: Path, as_of: date | None = None) -> dict[str, Any]:
    audit = load_module("review_snapshot_audit", root / "tools/run_normandie_v04_prepublication_audit.py").build(root, as_of)
    checklist = load_module("review_snapshot_checklist", root / "tools/build_normandie_v04_review_checklist.py").build(root, as_of)
    diff = load_module("review_snapshot_diff", root / "tools/build_normandie_v04_candidate_diff.py").build(root)
    dossier = load_module("review_snapshot_dossier", root / "tools/build_normandie_v04_decision_dossier.py").build(root)

    body = {
        "schema_version": "1.0",
        "status": "review_snapshot_not_public",
        "as_of": audit["as_of"],
        "integrity_ok": audit["integrity_ok"],
        "release_ready": audit["release_ready"],
        "published_base_memory_count": diff["published_base_memory_count"],
        "internal_candidate_memory_count": diff["current_internal_candidate_memory_count"],
        "guarded_preview_memory_count": diff["guarded_preview_memory_count"],
        "eligible_future_addition_count": diff["currently_eligible_future_addition_count"],
        "review_completed_count": checklist["completed_count"],
        "review_item_count": checklist["item_count"],
        "review_blocking_open_ids": list(checklist["blocking_open_ids"]),
        "station_decisions": {
            key: {"decision": value["decision"], "reason": value["reason"]}
            for key, value in dossier["station_decisions"].items()
        },
        "public_export_allowed": False,
        "rules": {
            "snapshot_is_review_evidence_only": True,
            "snapshot_does_not_complete_review": True,
            "snapshot_does_not_mutate_candidate": True,
            "snapshot_does_not_publish": True,
            "published_v0_3_1_remains_immutable": True,
        },
    }
    snapshot_id = hashlib.sha256(canonical_bytes(body)).hexdigest()
    return {**body, "snapshot_id": snapshot_id}


def markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Normandie v0.4 — snapshot de revue interne",
        "",
        f"- Date logique : **{data['as_of']}**",
        f"- Snapshot : `{data['snapshot_id']}`",
        f"- Intégrité : **{'OK' if data['integrity_ok'] else 'ERREUR'}**",
        f"- Release ready : **{'oui' if data['release_ready'] else 'non'}**",
        f"- Base / candidat / preview : **{data['published_base_memory_count']} / {data['internal_candidate_memory_count']} / {data['guarded_preview_memory_count']}**",
        f"- Revue : **{data['review_completed_count']}/{data['review_item_count']}**",
        f"- Blocages : **{len(data['review_blocking_open_ids'])}**",
        "",
        "## Décisions stations",
        "",
    ]
    for station, item in data["station_decisions"].items():
        lines.append(f"- **{station}** — {item['decision']} — {item['reason']}")
    lines.extend(["", "Ce snapshot fige un état de revue ; il n'autorise ni mutation ni publication.", ""])
    return "\n".join(lines)


def write(root: Path, output_dir: Path, as_of: date | None = None) -> tuple[Path, Path, dict[str, Any]]:
    data = build(root, as_of)
    output_dir.mkdir(parents=True, exist_ok=True)
    jp = output_dir / "normandie-v04-review-snapshot.json"
    mp = output_dir / "normandie-v04-review-snapshot.md"
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
        "NORMANDIE V0.4 REVIEW SNAPSHOT: "
        f"id={data['snapshot_id'][:12]} review={data['review_completed_count']}/{data['review_item_count']} "
        f"release_ready={str(data['release_ready']).lower()} public=false"
    )
    print(jp)
    print(mp)


if __name__ == "__main__":
    main()
