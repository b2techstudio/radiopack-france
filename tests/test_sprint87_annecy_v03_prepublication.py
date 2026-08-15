import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research/annecy-alpes-leman-v0.3"
SCOPE = RESEARCH / "release-scope.json"
REVIEW = RESEARCH / "review-checklist.json"
REVALIDATION = RESEARCH / "current-source-revalidation.json"
BUILDER = ROOT / "tools/build_annecy_v03_release_candidate.py"
PUBLIC_FULL = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv"
PUBLIC_NO_AIR = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv"

for path in [SCOPE, REVIEW, REVALIDATION, BUILDER]:
    assert path.is_file(), f"Missing Sprint 87 dependency: {path.relative_to(ROOT)}"

scope = json.loads(SCOPE.read_text(encoding="utf-8"))
review = json.loads(REVIEW.read_text(encoding="utf-8"))
revalidation = json.loads(REVALIDATION.read_text(encoding="utf-8"))

assert scope["status"] == "release_scope_frozen_prepublication"
assert scope["full_memory_count"] == 76
assert scope["without_aviation_memory_count"] == 59
assert scope["aviation_memory_count"] == 17
assert scope["new_unique_rf_memory_count"] == 11
assert scope["publication_blocker_count"] == 0
assert scope["prepublication_ready"] is True
assert scope["public_export_allowed"] is False
assert scope["public_registry_allowed"] is False
assert scope["carry_forward_aviation"]["france_cycle"] == "AIRAC 08/26"
assert scope["carry_forward_aviation"]["france_effective_until_inclusive"] == "2026-09-02"

excluded = {item["id"]: item for item in scope["excluded_from_v0_3"]}
assert excluded["F1ZTH_50M_DEVICE_COMPATIBILITY"]["frequency_mhz"] == 50.5375
assert excluded["F1ZTH_50M_DEVICE_COMPATIBILITY"]["blocks_publication"] is False
assert excluded["F1ZJV_F1ZYT_ADRASEC_UHF_TRANSPONDER"]["frequency_mhz"] is None
assert excluded["F1ZJV_F1ZYT_ADRASEC_UHF_TRANSPONDER"]["blocks_publication"] is False

assert review["status"] == "prepublication_review_complete"
assert review["completed"] == review["total"] == 12
assert review["blocker_count"] == 0
assert review["scope_frozen"] is True
assert review["prepublication_ready"] is True
assert review["publication_ready_after_deterministic_release_build"] is True
assert all(item["passed"] is True for item in review["items"])

assert revalidation["status"] == "current_sources_revalidated_prepublication"
assert revalidation["checked_on"] == "2026-08-15"
assert revalidation["candidate_memory_count"] == 76
assert revalidation["candidate_without_aviation_memory_count"] == 59
assert revalidation["candidate_new_unique_rf_memory_count"] == 11
assert revalidation["publication_blocker_count"] == 0
assert len(revalidation["approved_new_rf_mhz"]) == 11
assert revalidation["rules"]["unpublished_adrasec_frequency_must_not_be_inferred"] is True
assert revalidation["rules"]["private_professional_or_ppdr_frequencies_excluded"] is True

with tempfile.TemporaryDirectory(prefix="radiopack-annecy-v03-release-") as td:
    completed = subprocess.run(
        [sys.executable, str(BUILDER), "--root", str(ROOT), "--output-dir", td],
        text=True,
        capture_output=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    out = Path(td)
    full = out / "radiopack-france-annecy-alpes-leman-v0.3.csv"
    no_air = out / "radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv"
    review_map_path = out / "prepublication-reviewed-memory-map.json"
    manifest_path = out / "release-candidate-manifest.json"
    for path in [full, no_air, review_map_path, manifest_path]:
        assert path.is_file(), f"Missing generated Sprint 87 file: {path.name}"

    def rows(path):
        with path.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    full_rows = rows(full)
    no_air_rows = rows(no_air)
    assert len(full_rows) == 76
    assert len(no_air_rows) == 59
    assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in full_rows)
    assert all(row["Tone"] == "" and row["Power"] == "" for row in full_rows)
    assert len({row["Location"] for row in full_rows}) == 76
    assert len({row["Name"] for row in full_rows}) == 76
    assert len({row["Frequency"] for row in full_rows}) == 76
    assert all(len(row["Name"]) <= 10 for row in full_rows)
    assert "50.537500" not in {row["Frequency"] for row in full_rows}

    expected_new = {
        "145.850000", "435.250000", "439.625000", "145.037500", "145.050000",
        "430.325000", "431.425000", "145.187500", "145.787500", "145.125000", "431.500000",
    }
    assert expected_new.issubset({row["Frequency"] for row in full_rows})

    review_map = json.loads(review_map_path.read_text(encoding="utf-8"))
    assert review_map["status"] == "reviewed_prepublication_not_public"
    assert review_map["expected_memory_count"] == 76
    assert review_map["expected_memory_count_without_aviation"] == 59
    assert review_map["new_unique_rf_memory_count"] == 11
    assert len(review_map["rows"]) == 76

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["status"] == "release_candidate_built_not_public"
    assert manifest["full_memory_count"] == 76
    assert manifest["without_aviation_memory_count"] == 59
    assert manifest["aviation_memory_count"] == 17
    assert manifest["new_unique_rf_memory_count"] == 11
    assert manifest["publication_blocker_count"] == 0
    assert manifest["public_export_allowed"] is False
    assert manifest["rules"]["f1zth_50m_excluded"] is True
    assert manifest["rules"]["unpublished_adrasec_frequency_inferred"] is False

# Sprint 87 is prepublication-only; a later explicit publication may make these files exist.
if PUBLIC_FULL.exists() or PUBLIC_NO_AIR.exists():
    assert PUBLIC_FULL.is_file() and PUBLIC_NO_AIR.is_file()
    record = json.loads((ROOT / "research/annecy-alpes-leman-v0.3/publication-record.json").read_text(encoding="utf-8"))
    assert record["status"] == "published_immutable"
    assert record["full_memory_count"] == 76 and record["without_aviation_memory_count"] == 59

print("Sprint 87 Annecy v0.3 prepublication: frozen 76/59, +11 RF, 12/12 review, blockers=0 OK")
