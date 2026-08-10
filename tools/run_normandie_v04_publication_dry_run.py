#!/usr/bin/env python3
"""Run a guarded, non-public Normandie v0.4 publication dry-run."""
from __future__ import annotations

import argparse
import importlib.util
import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = Path("research/normandie-v0.4/generated/publication-dry-run")


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build(root: Path, baseline_path: Path | None = None, as_of: date | None = None) -> dict[str, Any]:
    audit = load_module("publication_dry_run_audit", root / "tools/run_normandie_v04_prepublication_audit.py").build(root, as_of)
    manifest = load_module("publication_dry_run_manifest", root / "tools/build_normandie_v04_review_manifest.py").build(root, as_of)

    drift = None
    if baseline_path is not None:
        path = baseline_path if baseline_path.is_absolute() else root / baseline_path
        drift = load_module("publication_dry_run_drift", root / "tools/check_normandie_v04_review_drift.py").compare(root, load_json(path))

    baseline_provided = drift is not None
    drift_clean = bool(baseline_provided and drift["drift_detected"] is False)
    activation_ready = bool(
        audit["prepublication_ready"]
        and baseline_provided
        and drift_clean
        and audit["public_registry_has_v04"] is False
    )

    activation_blockers = list(audit.get("integrity_errors", []))
    if not audit["prepublication_ready"]:
        activation_blockers.append("PREPUBLICATION_NOT_READY")
    if not baseline_provided:
        activation_blockers.append("REVIEW_BASELINE_NOT_PROVIDED")
    elif not drift_clean:
        activation_blockers.append("REVIEW_DRIFT_DETECTED")
    if audit["public_registry_has_v04"]:
        activation_blockers.append("PUBLIC_REGISTRY_ALREADY_CHANGED")

    return {
        "schema_version": "1.0",
        "status": "publication_dry_run_not_public",
        "as_of": audit["as_of"],
        "review_manifest_id": manifest["manifest_id"],
        "prepublication_ready": audit["prepublication_ready"],
        "baseline_provided": baseline_provided,
        "review_drift_clean": drift_clean if baseline_provided else None,
        "activation_blocking_count": len(activation_blockers),
        "activation_blockers": activation_blockers,
        "activation_ready": activation_ready,
        "would_publish_memory_count": audit["internal_candidate_memory_count"] if activation_ready else None,
        "public_registry_has_v04": audit["public_registry_has_v04"],
        "candidate_mutated": False,
        "public_files_written": False,
        "public_export_allowed": False,
        "rules": {
            "dry_run_never_writes_public_files": True,
            "dry_run_never_changes_pack_registry": True,
            "activation_requires_prepublication_ready": True,
            "activation_requires_captured_review_baseline": True,
            "activation_requires_zero_review_drift": True,
            "activation_ready_is_not_automatic_publication": True,
            "published_v0_3_1_remains_immutable": True,
        },
    }


def markdown(data: dict[str, Any]) -> str:
    lines = [
        "# Normandie v0.4 — dry-run de publication",
        "",
        f"- Prépublication prête : **{'oui' if data['prepublication_ready'] else 'non'}**",
        f"- Baseline de revue fournie : **{'oui' if data['baseline_provided'] else 'non'}**",
        f"- Dérive de revue propre : **{('oui' if data['review_drift_clean'] else 'non') if data['review_drift_clean'] is not None else 'non vérifiée'}**",
        f"- Activation prête : **{'oui' if data['activation_ready'] else 'non'}**",
        f"- Blocages activation : **{data['activation_blocking_count']}**",
        "",
    ]
    for blocker in data["activation_blockers"]:
        lines.append(f"- `{blocker}`")
    lines.extend([
        "",
        "Aucun CSV public, aucune route et aucune entrée du registre public ne sont modifiés par ce dry-run.",
        "",
    ])
    return "\n".join(lines)


def write(root: Path, output_dir: Path, baseline_path: Path | None = None, as_of: date | None = None) -> tuple[Path, Path, dict[str, Any]]:
    data = build(root, baseline_path, as_of)
    output_dir.mkdir(parents=True, exist_ok=True)
    jp = output_dir / "normandie-v04-publication-dry-run.json"
    mp = output_dir / "normandie-v04-publication-dry-run.md"
    jp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mp.write_text(markdown(data), encoding="utf-8")
    return jp, mp, data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--require-activation-ready", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    out = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    jp, mp, data = write(root, out, args.baseline)
    print(
        "NORMANDIE V0.4 PUBLICATION DRY RUN: "
        f"prepublication_ready={str(data['prepublication_ready']).lower()} "
        f"baseline={str(data['baseline_provided']).lower()} "
        f"activation_ready={str(data['activation_ready']).lower()} public=false"
    )
    print(jp)
    print(mp)
    if args.require_activation_ready and not data["activation_ready"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
