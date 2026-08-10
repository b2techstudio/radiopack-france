#!/usr/bin/env python3
"""Compare a captured Normandie v0.4 review manifest with current repository truth."""
from __future__ import annotations

import argparse
import importlib.util
import json
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def compare(root: Path, baseline: dict[str, Any]) -> dict[str, Any]:
    if baseline.get("status") != "review_fingerprint_manifest_not_public":
        raise ValueError("Baseline is not a Normandie v0.4 review fingerprint manifest")
    if baseline.get("public_export_allowed") is not False:
        raise ValueError("Baseline must be non-public")
    as_of = date.fromisoformat(baseline["as_of"])
    current = load_module("review_drift_manifest", root / "tools/build_normandie_v04_review_manifest.py").build(root, as_of)

    baseline_files = baseline["reviewed_input_sha256"]
    current_files = current["reviewed_input_sha256"]
    changed = []
    for path in sorted(set(baseline_files) | set(current_files)):
        before = baseline_files.get(path)
        after = current_files.get(path)
        if before != after:
            changed.append({"path": path, "baseline_sha256": before, "current_sha256": after})

    candidate_changed = baseline["internal_candidate_sha256"] != current["internal_candidate_sha256"]
    preview_changed = baseline["guarded_preview_sha256"] != current["guarded_preview_sha256"]
    snapshot_changed = baseline["review_snapshot_id"] != current["review_snapshot_id"]
    manifest_changed = baseline["manifest_id"] != current["manifest_id"]
    drift_detected = bool(changed or candidate_changed or preview_changed or snapshot_changed or manifest_changed)

    return {
        "schema_version": "1.0",
        "status": "review_drift_check_not_public",
        "baseline_manifest_id": baseline["manifest_id"],
        "current_manifest_id": current["manifest_id"],
        "baseline_as_of": baseline["as_of"],
        "changed_input_count": len(changed),
        "changed_inputs": changed,
        "candidate_changed": candidate_changed,
        "preview_changed": preview_changed,
        "review_snapshot_changed": snapshot_changed,
        "manifest_changed": manifest_changed,
        "drift_detected": drift_detected,
        "review_must_be_repeated": drift_detected,
        "public_export_allowed": False,
        "rules": {
            "any_reviewed_input_change_requires_re_review": True,
            "candidate_or_preview_change_requires_re_review": True,
            "drift_checker_never_mutates_repository": True,
            "drift_checker_never_publishes": True,
            "a_clean_drift_check_is_not_release_approval": True,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--require-clean", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    baseline_path = args.baseline if args.baseline.is_absolute() else root / args.baseline
    result = compare(root, load_json(baseline_path))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.require_clean and result["drift_detected"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
