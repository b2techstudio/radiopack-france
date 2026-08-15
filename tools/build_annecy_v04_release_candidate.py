#!/usr/bin/env python3
"""Build the frozen, non-public Annecy–Alpes–Léman v0.4 release candidate."""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research/annecy-alpes-leman-v0.4"
SCOPE = RESEARCH / "release-scope.json"
REVIEW = RESEARCH / "review-checklist.json"
REVALIDATION = RESEARCH / "current-source-revalidation.json"
CANDIDATE_BUILDER = ROOT / "tools/build_annecy_v04_candidate.py"
DEFAULT_OUTPUT_DIR = RESEARCH / "generated/release-candidate"
FULL_FILENAME = "radiopack-france-annecy-alpes-leman-v0.4.csv"
NO_AIR_FILENAME = "radiopack-france-annecy-alpes-leman-v0.4-sans-aviation.csv"
REVIEW_MAP_FILENAME = "prepublication-reviewed-memory-map.json"
MANIFEST_FILENAME = "release-candidate-manifest.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def load_candidate_module():
    spec = importlib.util.spec_from_file_location("annecy_v04_candidate", CANDIDATE_BUILDER)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load Annecy v0.4 candidate builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    scope = load_json(SCOPE)
    review = load_json(REVIEW)
    revalidation = load_json(REVALIDATION)
    if scope["status"] != "release_scope_frozen_prepublication" or scope["version"] != "0.4":
        raise ValueError("Annecy v0.4 release scope is not frozen")
    if scope["full_memory_count"] != 77 or scope["without_aviation_memory_count"] != 60:
        raise ValueError("Unexpected frozen Annecy v0.4 counts")
    if scope["new_unique_rf_memory_count"] != 1 or scope["approved_new_rf_mhz"] != [50.5375]:
        raise ValueError("Unexpected Annecy v0.4 RF delta")
    if scope["publication_blocker_count"] != 0 or not scope["prepublication_ready"]:
        raise ValueError("Annecy v0.4 scope has blockers")
    if scope["public_export_allowed"] or scope["public_registry_allowed"]:
        raise ValueError("Prepublication scope cannot mutate public release")

    if review["status"] != "prepublication_review_complete":
        raise ValueError("Annecy v0.4 review incomplete")
    if review["completed"] != review["total"] or review["blocker_count"] != 0:
        raise ValueError("Annecy v0.4 review has blockers")
    if not all(item["passed"] is True for item in review["items"]):
        raise ValueError("Annecy v0.4 review contains failed item")

    if revalidation["status"] != "current_sources_revalidated_prepublication":
        raise ValueError("Annecy v0.4 current-source revalidation missing")
    if revalidation["publication_blocker_count"] != 0:
        raise ValueError("Annecy v0.4 source revalidation has blockers")
    if revalidation["approved_new_rf_mhz"] != [50.5375]:
        raise ValueError("Annecy v0.4 source revalidation RF set changed")
    return scope, review, revalidation


def build_review_map(full_csv: Path) -> dict[str, Any]:
    with full_csv.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    mapped = []
    for row in rows:
        mapped.append([
            int(row["Location"]),
            row["Name"],
            round(float(row["Frequency"]), 6),
            row["Mode"],
            float(row["TStep"]),
            hashlib.sha256(row["Comment"].encode("utf-8")).hexdigest(),
        ])
    return {
        "pack": "Annecy–Alpes–Léman",
        "target_version": "0.4",
        "review": "Sprint 94 frozen prepublication line-by-line release map",
        "reviewed": "2026-08-15",
        "status": "reviewed_prepublication_not_public",
        "schema": ["location", "name", "frequency_mhz", "mode", "step_khz", "comment_sha256"],
        "expected_memory_count": 77,
        "expected_memory_count_without_aviation": 60,
        "new_unique_rf_memory_count": 1,
        "public_export_allowed": False,
        "rows": mapped,
    }


def build_release(output_dir: Path) -> dict[str, Any]:
    scope, review, revalidation = validate_inputs()
    candidate = load_candidate_module()
    candidate.validate_base()
    output_dir.mkdir(parents=True, exist_ok=True)
    full_path = output_dir / FULL_FILENAME
    no_air_path = output_dir / NO_AIR_FILENAME
    full_count, full_sha = candidate.build_variant(candidate.BASE_FULL, 76, full_path)
    no_air_count, no_air_sha = candidate.build_variant(candidate.BASE_NO_AIR, 59, no_air_path)
    if (full_count, no_air_count) != (77, 60):
        raise ValueError("Annecy v0.4 candidate counts drifted")
    expected_shas = {
        "full": "2557076fcb198b830cd3b5ba64d7ff894c8e0d6e90eafc0fa40b691a3c6a5d98",
        "without_aviation": "e31bfc6fce402af117b4f79caf6547b60a23c91ef36491e1351c74e96329aa6c",
    }
    if full_sha != expected_shas["full"] or no_air_sha != expected_shas["without_aviation"]:
        raise ValueError("Annecy v0.4 deterministic CSV SHA drift")

    review_map = build_review_map(full_path)
    map_path = output_dir / REVIEW_MAP_FILENAME
    map_path.write_text(json.dumps(review_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "schema_version": "1.0",
        "status": "release_candidate_built_not_public",
        "pack": "Annecy–Alpes–Léman",
        "version": "0.4",
        "built_on": "2026-08-15",
        "full_memory_count": 77,
        "without_aviation_memory_count": 60,
        "aviation_memory_count": 17,
        "new_unique_rf_memory_count": 1,
        "publication_blocker_count": 0,
        "public_export_allowed": False,
        "source_revalidation_status": revalidation["status"],
        "review_status": review["status"],
        "scope_status": scope["status"],
        "files": {
            "full": {"filename": FULL_FILENAME, "sha256": full_sha},
            "without_aviation": {"filename": NO_AIR_FILENAME, "sha256": no_air_sha},
            "review_map": {"filename": REVIEW_MAP_FILENAME, "sha256": sha256_file(map_path)},
        },
        "rules": {
            "rx_only": True,
            "same_rf_frequency_deduplicated": True,
            "published_v0_3_immutable": True,
            "f1zth_50m_approved": True,
            "modified_firmware_required": False,
            "unpublished_adrasec_frequency_inferred": False,
            "automatic_publication_allowed": False,
        },
    }
    (output_dir / MANIFEST_FILENAME).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    manifest = build_release(output_dir.resolve())
    print(
        "ANNECY V0.4 RELEASE CANDIDATE: "
        f"{manifest['full_memory_count']} / {manifest['without_aviation_memory_count']} RX, "
        "new_unique_rf=1, blockers=0, public=false"
    )
    print(output_dir / FULL_FILENAME)
    print(output_dir / NO_AIR_FILENAME)
    print(output_dir / REVIEW_MAP_FILENAME)
    print(output_dir / MANIFEST_FILENAME)


if __name__ == "__main__":
    main()
