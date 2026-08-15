#!/usr/bin/env python3
"""Build the frozen, non-public Annecy–Alpes–Léman v0.3 release candidate."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_annecy_v03_internal_candidate as internal  # noqa: E402

RESEARCH = Path("research/annecy-alpes-leman-v0.3")
SCOPE = RESEARCH / "release-scope.json"
REVIEW = RESEARCH / "review-checklist.json"
REVALIDATION = RESEARCH / "current-source-revalidation.json"
DEFAULT_OUTPUT_DIR = RESEARCH / "generated/release-candidate"

FULL_FILENAME = "radiopack-france-annecy-alpes-leman-v0.3.csv"
NO_AIR_FILENAME = "radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv"
REVIEW_MAP_FILENAME = "prepublication-reviewed-memory-map.json"
MANIFEST_FILENAME = "release-candidate-manifest.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_release_inputs(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    scope = load_json(root / SCOPE)
    review = load_json(root / REVIEW)
    revalidation = load_json(root / REVALIDATION)

    if scope["status"] != "release_scope_frozen_prepublication" or scope["version"] != "0.3":
        raise ValueError("Annecy v0.3 release scope is not frozen")
    if scope["full_memory_count"] != 76 or scope["without_aviation_memory_count"] != 59:
        raise ValueError("Unexpected frozen Annecy v0.3 counts")
    if scope["new_unique_rf_memory_count"] != 11 or scope["publication_blocker_count"] != 0:
        raise ValueError("Annecy v0.3 scope delta/blocker contract failed")
    if scope["prepublication_ready"] is not True or scope["public_export_allowed"] is not False:
        raise ValueError("Release candidate must remain non-public before explicit publication")

    if review["status"] != "prepublication_review_complete":
        raise ValueError("Annecy v0.3 review is incomplete")
    if review["completed"] != review["total"] or review["blocker_count"] != 0:
        raise ValueError("Annecy v0.3 review has blockers")
    if review["scope_frozen"] is not True or review["prepublication_ready"] is not True:
        raise ValueError("Annecy v0.3 review is not ready")
    if not all(item["passed"] is True for item in review["items"]):
        raise ValueError("Annecy v0.3 review contains a failed item")

    if revalidation["status"] != "current_sources_revalidated_prepublication":
        raise ValueError("Annecy v0.3 current-source revalidation missing")
    if revalidation["publication_blocker_count"] != 0:
        raise ValueError("Annecy v0.3 source revalidation has blockers")
    if len(revalidation["approved_new_rf_mhz"]) != 11:
        raise ValueError("Annecy v0.3 source revalidation must approve 11 new RF memories")

    expected = {round(float(value), 6) for value in scope["approved_new_rf_mhz"]}
    approved = {round(float(value), 6) for value in revalidation["approved_new_rf_mhz"]}
    if expected != approved:
        raise ValueError("Release scope and source revalidation RF sets differ")

    excluded = {item["id"]: item for item in scope["excluded_from_v0_3"]}
    if excluded["F1ZTH_50M_DEVICE_COMPATIBILITY"]["frequency_mhz"] != 50.5375:
        raise ValueError("F1ZTH 50 MHz exclusion is missing")
    if excluded["F1ZJV_F1ZYT_ADRASEC_UHF_TRANSPONDER"]["frequency_mhz"] is not None:
        raise ValueError("Unpublished ADRASEC UHF RF must stay unknown")

    return scope, review, revalidation


def csv_rows(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in sorted(candidate["memories"], key=lambda row: int(row["location"])):
        rows.append(internal.base.internal.chirp_row(int(item["location"]), item["channel"]))
    return rows


def write_csv(candidate: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=internal.base.internal.CHIRP_COLUMNS,
            lineterminator="\r\n",
        )
        writer.writeheader()
        writer.writerows(csv_rows(candidate))


def build_review_map(full_candidate: dict[str, Any]) -> dict[str, Any]:
    schema = [
        "location",
        "name",
        "frequency_mhz",
        "mode",
        "step_khz",
        "block",
        "comment_sha256",
    ]
    rows = []
    for item in sorted(full_candidate["memories"], key=lambda row: int(row["location"])):
        channel = item["channel"]
        rows.append([
            int(item["location"]),
            channel["name"],
            round(float(channel["frequency_mhz"]), 6),
            channel["mode"],
            float(channel["step_khz"]),
            channel.get("candidate_block", "Annecy v0.3"),
            hashlib.sha256(channel["comment"].encode("utf-8")).hexdigest(),
        ])
    return {
        "pack": "Annecy–Alpes–Léman",
        "target_version": "0.3",
        "review": "Sprint 87 frozen prepublication line-by-line release map",
        "reviewed": "2026-08-15",
        "status": "reviewed_prepublication_not_public",
        "schema": schema,
        "expected_memory_count": 76,
        "expected_memory_count_without_aviation": 59,
        "new_unique_rf_memory_count": 11,
        "public_export_allowed": False,
        "rows": rows,
    }


def build_release(root: Path, output_dir: Path) -> dict[str, Any]:
    scope, review, revalidation = validate_release_inputs(root)
    full = internal.build_candidate(root, include_aviation=True)
    no_air = internal.build_candidate(root, include_aviation=False)

    if full["memory_count"] != 76 or no_air["memory_count"] != 59:
        raise ValueError("Annecy v0.3 candidate counts changed after scope freeze")
    if full["new_unique_rf_memory_count"] != 11 or no_air["new_unique_rf_memory_count"] != 11:
        raise ValueError("Annecy v0.3 new RF delta changed after scope freeze")

    full_freqs = {round(float(item["channel"]["frequency_mhz"]), 6) for item in full["memories"]}
    no_air_freqs = {round(float(item["channel"]["frequency_mhz"]), 6) for item in no_air["memories"]}
    if len(full_freqs) != 76 or len(no_air_freqs) != 59:
        raise ValueError("Annecy v0.3 RF deduplication failed")
    if 50.5375 in full_freqs or 50.5375 in no_air_freqs:
        raise ValueError("F1ZTH 50 MHz scope exclusion leaked into v0.3")

    approved_new = {round(float(value), 6) for value in scope["approved_new_rf_mhz"]}
    base_full = internal.base.build_prepublication(root, True, "disabled")
    base_freqs = {round(float(item["channel"]["frequency_mhz"]), 6) for item in base_full["memories"]}
    actual_new = full_freqs - base_freqs
    if actual_new != approved_new:
        raise ValueError("Annecy v0.3 actual new RF set differs from frozen approved set")

    output_dir.mkdir(parents=True, exist_ok=True)
    full_path = output_dir / FULL_FILENAME
    no_air_path = output_dir / NO_AIR_FILENAME
    review_map_path = output_dir / REVIEW_MAP_FILENAME
    manifest_path = output_dir / MANIFEST_FILENAME

    write_csv(full, full_path)
    write_csv(no_air, no_air_path)
    review_map = build_review_map(full)
    review_map_path.write_text(json.dumps(review_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    manifest = {
        "schema_version": "1.0",
        "status": "release_candidate_built_not_public",
        "pack": "Annecy–Alpes–Léman",
        "version": "0.3",
        "built_on": "2026-08-15",
        "full_memory_count": 76,
        "without_aviation_memory_count": 59,
        "aviation_memory_count": 17,
        "new_unique_rf_memory_count": 11,
        "publication_blocker_count": 0,
        "public_export_allowed": False,
        "source_revalidation_status": revalidation["status"],
        "review_status": review["status"],
        "scope_status": scope["status"],
        "files": {
            "full": {"filename": full_path.name, "sha256": sha256_file(full_path)},
            "without_aviation": {"filename": no_air_path.name, "sha256": sha256_file(no_air_path)},
            "review_map": {"filename": review_map_path.name, "sha256": sha256_file(review_map_path)},
        },
        "rules": {
            "rx_only": True,
            "same_rf_frequency_deduplicated": True,
            "published_v0_2_immutable": True,
            "f1zth_50m_excluded": True,
            "unpublished_adrasec_frequency_inferred": False,
            "automatic_publication_allowed": False,
        },
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()
    root = args.root.resolve()
    output_dir = args.output_dir if args.output_dir.is_absolute() else root / args.output_dir
    manifest = build_release(root, output_dir)
    print(
        "ANNECY V0.3 RELEASE CANDIDATE: "
        f"{manifest['full_memory_count']} / {manifest['without_aviation_memory_count']} RX, "
        f"new_unique_rf={manifest['new_unique_rf_memory_count']}, blockers=0, public=false"
    )
    print(output_dir / FULL_FILENAME)
    print(output_dir / NO_AIR_FILENAME)
    print(output_dir / REVIEW_MAP_FILENAME)
    print(output_dir / MANIFEST_FILENAME)


if __name__ == "__main__":
    main()
