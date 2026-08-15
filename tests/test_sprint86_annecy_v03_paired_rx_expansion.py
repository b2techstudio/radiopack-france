import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPANSION = ROOT / "research/annecy-alpes-leman-v0.3/paired-rx-expansion.json"
PLAN = ROOT / "research/annecy-alpes-leman-v0.3/pack-plan.json"
STATE = ROOT / "research/project-resume-state.json"
BASE_REVIEW = ROOT / "research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json"
BASE_BUILDER = ROOT / "tools/build_annecy_prepublication.py"
V03_BUILDER = ROOT / "tools/build_annecy_v03_internal_candidate.py"
PUBLIC_V02_ROUTE = ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv.ts"
PUBLIC_V03_ROUTE = ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv.ts"
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"

for path in [EXPANSION, PLAN, STATE, BASE_REVIEW, BASE_BUILDER, V03_BUILDER, PUBLIC_V02_ROUTE, REGISTRY]:
    assert path.is_file(), f"Missing Sprint 86 dependency: {path.relative_to(ROOT)}"
assert not PUBLIC_V03_ROUTE.exists(), "Annecy v0.3 must not have a public route during Sprint 86"

state = json.loads(STATE.read_text(encoding="utf-8"))
assert state["current_sprint"] >= 86
version_tuple = tuple(int(part) for part in state["state_version"].split("."))
assert version_tuple >= (0, 21, 75)
active = state["active_work"]
assert active["pack"] == "Annecy–Alpes–Léman"
assert active["target_version"] == "0.3"
assert active["published_base_version"] == "0.2"
assert active["published_base_memory_count"] == 65
assert active["published_base_without_aviation_memory_count"] == 48
assert active["published_base_is_immutable"] is True
assert active["internal_candidate_memory_count"] == 76
assert active["internal_candidate_without_aviation_memory_count"] == 59
assert active["internal_candidate_new_memory_count"] == 11
assert active["known_potential_ceiling_if_f1zth_50m_clears"] == 77
publication_record = ROOT / "research/annecy-alpes-leman-v0.3/publication-record.json"
if publication_record.exists():
    assert active["public_export_allowed"] is True
    assert active["public_registry_allowed"] is True
    assert active["public_release_ready"] is True
else:
    assert active["public_export_allowed"] is False
    assert active["public_registry_allowed"] is False
    assert active["public_release_ready"] is False

expansion = json.loads(EXPANSION.read_text(encoding="utf-8"))
assert expansion["status"] == "paired_rx_expansion_reviewed_sprint86_not_public"
assert expansion["target_version"] == "0.3"
assert expansion["based_on"]["version"] == "0.2"
assert expansion["based_on"]["full_memory_count"] == 65
assert expansion["based_on"]["without_aviation_memory_count"] == 48
assert expansion["based_on"]["immutable"] is True
result = expansion["result"]
assert result["candidate_full_memory_count"] == 76
assert result["candidate_without_aviation_memory_count"] == 59
assert result["candidate_new_unique_rf_memory_count"] == 11
assert result["potential_ceiling_if_f1zth_50m_clears"] == 77
assert result["public_export_allowed"] is False

additions = expansion["candidate_additions"]
assert len(additions) == 11
assert all(item["candidate_status"] == "promote_internal_candidate" for item in additions)
expected_added = {
    145.850000,
    435.250000,
    439.625000,
    145.037500,
    145.050000,
    430.325000,
    431.425000,
    145.187500,
    145.787500,
    145.125000,
    431.500000,
}
assert {round(float(item["frequency_mhz"]), 6) for item in additions} == expected_added
assert {int(item["location"]) for item in additions} == {29, 32, 59, 60, 61, 62, 63, 64, 65, 92, 93}
assert {item["name"] for item in additions} == {
    "SAT-UP145", "SAT-UP435", "01-ZOH-IN", "01-ZJD-IN", "38-ZCQ-IN", "38-ZCR-IN",
    "38-ZDC-IN", "74-R7X-IN", "74-R7X-OUT", "CH-HG-VIN", "CH-HG-UIN",
}
assert all(len(item["name"]) <= 10 for item in additions)

review = json.loads(BASE_REVIEW.read_text(encoding="utf-8"))
schema = review["schema"]
base_rows = [dict(zip(schema, row)) for row in review["rows"]]
assert len(base_rows) == 65
base_freqs = {round(float(row["frequency_mhz"]), 6) for row in base_rows}
assert not expected_added.intersection(base_freqs), "Sprint 86 additions must be unique RF relative to public v0.2"

# Paired-RX cases already fully represented in v0.2 must remain zero-delta.
dedup_text = "\n".join(item["station"] + " " + item["reason"] for item in expansion["deduplicated_existing"])
for token in ["F1ZPY", "F1ZWY", "F5ZDT", "F1ZFX", "F1ZIC", "F1ZHE", "F1ZHG", "F5ZGT", "F5ZLV"]:
    assert token in dedup_text
assert "145.850" in dedup_text and "SO-50 / AO-123" in dedup_text

# F1ZTH 50 MHz is a documented conditional +1, not a Sprint 86 promotion.
deferred = {item["id"]: item for item in expansion["deferred"]}
f1zth = deferred["F1ZTH_50M_DEVICE_COMPATIBILITY"]
assert f1zth["frequency_mhz"] == 50.5375
assert f1zth["source_currently_publishes_rf"] is True
assert f1zth["potential_memory_delta"] == 1
assert f1zth["promoted"] is False
assert 50.5375 not in expected_added
assert "device_firmware_rx_compatibility_not_project_verified" in f1zth["state"]

# The locally mentioned ADRASEC UHF link has no public RF and is never inferred.
uhf = deferred["F1ZJV_F1ZYT_ADRASEC_UHF_TRANSPONDER"]
assert uhf["frequency_mhz"] is None
assert uhf["promoted"] is False
assert "frequency_not_public" in uhf["state"]
assert expansion["rules"]["unpublished_adrasec_frequency_must_not_be_inferred"] is True
assert expansion["rules"]["private_professional_or_ppdr_emergency_frequencies_excluded"] is True

plan = json.loads(PLAN.read_text(encoding="utf-8"))
assert plan["memory_plan"]["status"] == "sprint86_internal_candidate_defined_not_public"
assert plan["memory_plan"]["expected_memory_count"] == 76
assert plan["memory_plan"]["expected_memory_count_without_aviation"] == 59
assert plan["memory_plan"]["new_unique_rf_memory_count"] == 11
assert plan["memory_plan"]["potential_ceiling_if_f1zth_50m_clears"] == 77
if publication_record.exists():
    assert plan["publication"]["public_export_allowed"] is True
    assert plan["publication"]["public_registry_allowed"] is True
    assert plan["publication"]["review_completed"] is True
else:
    assert plan["publication"]["public_export_allowed"] is False
    assert plan["publication"]["public_registry_allowed"] is False
    assert plan["publication"]["review_completed"] is False


def build(builder: Path, include_aviation: bool):
    temp = tempfile.TemporaryDirectory(prefix="radiopack-annecy-v03-")
    args = [sys.executable, str(builder), "--root", str(ROOT), "--output-dir", temp.name]
    if builder == V03_BUILDER and not include_aviation:
        args.append("--no-aviation")
    elif builder == BASE_BUILDER and not include_aviation:
        args.append("--no-aviation")
    completed = subprocess.run(args, text=True, capture_output=True)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    csv_files = list(Path(temp.name).glob("*.csv"))
    json_files = list(Path(temp.name).glob("*.json"))
    assert len(csv_files) == 1 and len(json_files) == 1
    with csv_files[0].open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    manifest = json.loads(json_files[0].read_text(encoding="utf-8"))
    return temp, rows, manifest

for include_aviation, expected_base_count, expected_v03_count in [(True, 65, 76), (False, 48, 59)]:
    base_temp, old_rows, old_manifest = build(BASE_BUILDER, include_aviation)
    v03_temp, new_rows, new_manifest = build(V03_BUILDER, include_aviation)
    try:
        assert len(old_rows) == expected_base_count
        assert len(new_rows) == expected_v03_count
        assert new_manifest["memory_count"] == expected_v03_count
        assert new_manifest["new_unique_rf_memory_count"] == 11
        assert new_manifest["public_export_allowed"] is False
        assert new_manifest["public_registry_allowed"] is False
        assert new_manifest["deferred_frequency_mhz"] == [50.5375]

        old_by_location = {int(row["Location"]): row for row in old_rows}
        new_by_location = {int(row["Location"]): row for row in new_rows}
        for location, row in old_by_location.items():
            assert new_by_location[location] == row, f"Immutable v0.2 base drifted at location {location}"

        new_only = [row for row in new_rows if int(row["Location"]) not in old_by_location]
        assert len(new_only) == 11
        assert {round(float(row["Frequency"]), 6) for row in new_only} == expected_added
        assert all(row["Duplex"] == "off" for row in new_rows)
        assert all(row["Offset"] == "0.000000" for row in new_rows)
        assert all(row["Tone"] == "" for row in new_rows)
        assert len({row["Frequency"] for row in new_rows}) == expected_v03_count
    finally:
        base_temp.cleanup()
        v03_temp.cleanup()

registry = REGISTRY.read_text(encoding="utf-8")
old_full_route = ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv.ts"
old_no_air_route = ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv.ts"
assert old_full_route.is_file() and old_no_air_route.is_file()
assert "buildAnnecyCsv(true)" in old_full_route.read_text(encoding="utf-8")
assert "buildAnnecyCsv(false)" in old_no_air_route.read_text(encoding="utf-8")
publication_record = ROOT / "research/annecy-alpes-leman-v0.3/publication-record.json"
if publication_record.exists():
    assert "radiopack-france-annecy-alpes-leman-v0.3.csv" in registry
else:
    assert "radiopack-france-annecy-alpes-leman-v0.3.csv" not in registry

print("Sprint 86 Annecy v0.3 paired RX: 65 -> 76 (+11), no-aviation 48 -> 59, F1ZTH 50 MHz deferred, no public mutation OK")
