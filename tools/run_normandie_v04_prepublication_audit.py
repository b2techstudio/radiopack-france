#!/usr/bin/env python3
"""Run the non-public Normandie v0.4 prepublication integrity audit."""
from __future__ import annotations

import argparse
import importlib.util
import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.4/generated/prepublication-audit")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(root: Path, as_of: date | None = None) -> dict[str, Any]:
    consistency = load_module("audit_consistency", root / "tools/check_normandie_v04_source_consistency.py").evaluate(root)
    freshness = load_module("audit_freshness", root / "tools/check_normandie_v04_source_freshness.py").evaluate(root, as_of)
    checklist = load_module("audit_checklist", root / "tools/build_normandie_v04_review_checklist.py").build(root, as_of)
    diff = load_module("audit_diff", root / "tools/build_normandie_v04_candidate_diff.py").build(root)
    blockers = load_module("audit_blockers", root / "tools/build_normandie_v04_release_blockers.py").build(root)

    integrity_checks = {
        "source_truth_consistent": bool(consistency["consistent"]),
        "source_revalidations_fresh": bool(freshness["all_revalidations_fresh"]),
        "published_base_exact_prefix": bool(diff["published_base_is_exact_prefix_of_internal_candidate"]),
        "internal_candidate_exact_preview_prefix": bool(diff["internal_candidate_is_exact_prefix_of_guarded_preview"]),
        "candidate_not_mutated": diff["candidate_mutated"] is False,
        "public_export_stays_disabled": diff["public_export_allowed"] is False and checklist["public_export_allowed"] is False and blockers["public_export_allowed"] is False,
    }
    integrity_errors = [key for key, value in integrity_checks.items() if not value]
    release_ready = checklist["release_review_complete"] and blockers["blocking_count"] == 0

    return {
        "schema_version": "1.0",
        "status": "prepublication_audit_not_public",
        "as_of": freshness["as_of"],
        "integrity_ok": not integrity_errors,
        "integrity_error_count": len(integrity_errors),
        "integrity_errors": integrity_errors,
        "integrity_checks": integrity_checks,
        "published_base_memory_count": diff["published_base_memory_count"],
        "internal_candidate_memory_count": diff["current_internal_candidate_memory_count"],
        "guarded_preview_memory_count": diff["guarded_preview_memory_count"],
        "currently_eligible_future_addition_count": diff["currently_eligible_future_addition_count"],
        "review_completed_count": checklist["completed_count"],
        "review_item_count": checklist["item_count"],
        "review_blocking_open_count": checklist["blocking_open_count"],
        "release_blocking_count": blockers["blocking_count"],
        "release_ready": release_ready,
        "public_export_allowed": False,
        "rules": {
            "integrity_ok_does_not_mean_release_ready": True,
            "release_ready_requires_zero_review_and_release_blockers": True,
            "audit_never_mutates_candidate": True,
            "audit_never_publishes": True,
            "published_v0_3_1_remains_immutable": True,
        },
    }


def markdown(data: dict[str, Any]) -> str:
    return "\n".join([
        "# Normandie v0.4 — audit prépublication",
        "",
        f"- Intégrité du pipeline : **{'OK' if data['integrity_ok'] else 'ERREUR'}**",
        f"- Base publique : **{data['published_base_memory_count']}**",
        f"- Candidat interne : **{data['internal_candidate_memory_count']}**",
        f"- Preview : **{data['guarded_preview_memory_count']}**",
        f"- Ajouts futurs éligibles : **{data['currently_eligible_future_addition_count']}**",
        f"- Checklist revue : **{data['review_completed_count']}/{data['review_item_count']}**",
        f"- Blocages revue : **{data['review_blocking_open_count']}**",
        f"- Blocages publication : **{data['release_blocking_count']}**",
        f"- Release ready : **{'oui' if data['release_ready'] else 'non'}**",
        "",
        "Un audit d'intégrité OK signifie seulement que le pipeline est cohérent ; il ne vaut jamais autorisation de publication.",
        "",
    ])


def write(root: Path, output_dir: Path, as_of: date | None = None) -> tuple[Path, Path, dict[str, Any]]:
    data = build(root, as_of)
    output_dir.mkdir(parents=True, exist_ok=True)
    jp = output_dir / "normandie-v04-prepublication-audit.json"
    mp = output_dir / "normandie-v04-prepublication-audit.md"
    jp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mp.write_text(markdown(data), encoding="utf-8")
    return jp, mp, data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--require-release-ready", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    out = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    jp, mp, data = write(root, out)
    print(
        "NORMANDIE V0.4 PREPUBLICATION AUDIT: "
        f"integrity={'OK' if data['integrity_ok'] else 'ERROR'} "
        f"review={data['review_completed_count']}/{data['review_item_count']} "
        f"blockers={data['release_blocking_count']} "
        f"release_ready={str(data['release_ready']).lower()}"
    )
    print(jp)
    print(mp)
    if not data["integrity_ok"]:
        raise SystemExit(1)
    if args.require_release_ready and not data["release_ready"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
