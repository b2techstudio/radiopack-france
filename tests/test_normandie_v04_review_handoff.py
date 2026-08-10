import importlib.util
import json
import tempfile
from copy import deepcopy
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "tools/build_normandie_v04_review_snapshot.py"
MANIFEST = ROOT / "tools/build_normandie_v04_review_manifest.py"
DRIFT = ROOT / "tools/check_normandie_v04_review_drift.py"
DRY_RUN = ROOT / "tools/run_normandie_v04_publication_dry_run.py"

for path in (SNAPSHOT, MANIFEST, DRIFT, DRY_RUN):
    assert path.is_file(), f"Missing expected file: {path}"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


snapshot_builder = load_module("review_snapshot_test", SNAPSHOT)
manifest_builder = load_module("review_manifest_test", MANIFEST)
drift_checker = load_module("review_drift_test", DRIFT)
dry_run_builder = load_module("publication_dry_run_test", DRY_RUN)

current_day = date(2026, 8, 10)

snapshot = snapshot_builder.build(ROOT, current_day)
assert snapshot["status"] == "review_snapshot_not_public"
assert snapshot["integrity_ok"] is True
assert snapshot["release_ready"] is False
assert snapshot["published_base_memory_count"] == 139
assert snapshot["internal_candidate_memory_count"] == 142
assert snapshot["guarded_preview_memory_count"] == 142
assert snapshot["eligible_future_addition_count"] == 0
assert snapshot["review_completed_count"] == 3
assert snapshot["review_item_count"] == 9
assert len(snapshot["review_blocking_open_ids"]) == 6
assert len(snapshot["snapshot_id"]) == 64
assert snapshot_builder.build(ROOT, current_day)["snapshot_id"] == snapshot["snapshot_id"]

manifest = manifest_builder.build(ROOT, current_day)
assert manifest["status"] == "review_fingerprint_manifest_not_public"
assert manifest["review_snapshot_id"] == snapshot["snapshot_id"]
assert manifest["reviewed_input_count"] == 11
assert len(manifest["reviewed_input_sha256"]) == 11
assert all(len(digest) == 64 for digest in manifest["reviewed_input_sha256"].values())
assert manifest["internal_candidate_memory_count"] == 142
assert manifest["guarded_preview_memory_count"] == 142
assert len(manifest["internal_candidate_sha256"]) == 64
assert len(manifest["guarded_preview_sha256"]) == 64
assert len(manifest["manifest_id"]) == 64

clean = drift_checker.compare(ROOT, manifest)
assert clean["drift_detected"] is False
assert clean["review_must_be_repeated"] is False
assert clean["changed_input_count"] == 0
assert clean["candidate_changed"] is False
assert clean["preview_changed"] is False
assert clean["review_snapshot_changed"] is False

synthetic_old = deepcopy(manifest)
first_path = next(iter(synthetic_old["reviewed_input_sha256"]))
synthetic_old["reviewed_input_sha256"][first_path] = "0" * 64
synthetic_old["manifest_id"] = "1" * 64
drifted = drift_checker.compare(ROOT, synthetic_old)
assert drifted["drift_detected"] is True
assert drifted["review_must_be_repeated"] is True
assert drifted["changed_input_count"] == 1
assert drifted["changed_inputs"][0]["path"] == first_path

without_baseline = dry_run_builder.build(ROOT, None, current_day)
assert without_baseline["status"] == "publication_dry_run_not_public"
assert without_baseline["prepublication_ready"] is False
assert without_baseline["baseline_provided"] is False
assert without_baseline["review_drift_clean"] is None
assert without_baseline["activation_ready"] is False
assert without_baseline["would_publish_memory_count"] is None
assert without_baseline["candidate_mutated"] is False
assert without_baseline["public_files_written"] is False
assert {"PREPUBLICATION_NOT_READY", "REVIEW_BASELINE_NOT_PROVIDED"}.issubset(set(without_baseline["activation_blockers"]))

with tempfile.TemporaryDirectory(prefix="radiopack-v04-review-handoff-") as tmp:
    baseline = Path(tmp) / "baseline.json"
    baseline.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    clean_dry_run = dry_run_builder.build(ROOT, baseline, current_day)
    assert clean_dry_run["baseline_provided"] is True
    assert clean_dry_run["review_drift_clean"] is True
    assert clean_dry_run["prepublication_ready"] is False
    assert clean_dry_run["activation_ready"] is False
    assert clean_dry_run["activation_blockers"] == ["PREPUBLICATION_NOT_READY"]

    jp, mp, written = snapshot_builder.write(ROOT, Path(tmp) / "snapshot", current_day)
    assert jp.is_file() and mp.is_file()
    assert written["snapshot_id"] == snapshot["snapshot_id"]
    jp2, mp2, written_manifest = manifest_builder.write(ROOT, Path(tmp) / "manifest", current_day)
    assert jp2.is_file() and mp2.is_file()
    assert written_manifest["manifest_id"] == manifest["manifest_id"]

print(
    "Tests Normandie v0.4 review handoff: deterministic review snapshot and SHA-256 manifest built, "
    "clean baseline stays clean, synthetic input drift forces re-review, publication dry-run remains non-public and blocked, OK"
)
