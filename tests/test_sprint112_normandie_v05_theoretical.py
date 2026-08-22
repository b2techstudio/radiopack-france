#!/usr/bin/env python3
import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research/normandie-v0.5"
POLICY = json.loads((RESEARCH / "theoretical-coverage-policy.json").read_text(encoding="utf-8"))
THEORY = json.loads((RESEARCH / "sprint112-theoretical-coverage.json").read_text(encoding="utf-8"))
PLAN = json.loads((RESEARCH / "pack-plan.json").read_text(encoding="utf-8"))
BACKLOG = json.loads((RESEARCH / "backlog.json").read_text(encoding="utf-8"))
BUILDER = ROOT / "tools/build_normandie_v05_internal_candidate.py"
PUBLIC_V04 = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv"
PUBLIC_V05 = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.5.csv"

assert POLICY["decision_model"]["theoretical_coverage_may_close_coverage_gate"] is True
assert POLICY["decision_model"]["field_reception_required_for_candidate_promotion"] is False
assert POLICY["decision_model"]["field_reception_required_for_publication"] is False
assert POLICY["rules"]["theory_is_not_measurement"] is True
assert POLICY["rules"]["unresolved_frequency_must_not_be_guessed"] is True
assert POLICY["publication_language"]["required_label"] == "couverture théorique"

assert THEORY["status"] == "theoretical_coverage_promotes_four_internal_memories_not_public"
assert THEORY["candidate_memory_count_before"] == 142
assert THEORY["candidate_memory_count_after"] == 146
assert THEORY["candidate_memory_delta"] == 4
assert len(THEORY["promotions"]) == 2
r3, zha = THEORY["promotions"]
assert r3["pair_mhz"] == [145.075, 145.675]
assert r3["memory_delta"] == 2
assert r3["candidate_locations"] == [178, 179]
assert r3["theory"]["great_circle_distance_km"] == 118.32
assert r3["theory"]["distance_within_operator_usage_radius"] is True
assert r3["theory"]["distance_within_endpoint_elevation_envelope"] is True
assert r3["field_reception_verified"] is False
assert r3["field_reception_required"] is False
assert zha["pair_mhz"] == [145.4675, 432.575]
assert zha["memory_delta"] == 2
assert zha["candidate_locations"] == [180, 181]
assert zha["theory"]["great_circle_distance_km"] == 65.66
assert zha["theory"]["distance_within_endpoint_elevation_envelope"] is True
assert zha["stale_secondary_frequency_mhz_excluded"] == 431.4125
assert zha["field_reception_verified"] is False
assert zha["field_reception_required"] is False

assert PLAN["current_candidate_memory_count"] == 146
assert PLAN["current_new_memory_count"] == 4
assert PLAN["last_revalidation_sprint"] == 112
assert PLAN["last_revalidation_memory_delta"] == 4
assert PLAN["field_validation_role"] == "optional_post_publication_quality_feedback"
assert PLAN["rules"]["theoretical_coverage_may_close_coverage_gate"] is True
assert PLAN["rules"]["field_reception_required_for_candidate_promotion"] is False
assert PLAN["public_export_allowed"] is False

items = {item["id"]: item for item in BACKLOG["items"]}
assert BACKLOG["current_candidate_memory_count"] == 146
assert BACKLOG["current_candidate_memory_delta"] == 4
assert items["R3_MORTAIN_RX"]["promoted"] is True
assert items["F5ZHA_SOURCE_AND_COVERAGE"]["promoted"] is True
assert items["F1ZOV_OPERATIONAL_STATUS"]["promoted"] is False
assert items["F1ZOV_OPERATIONAL_STATUS"]["local_operator_status"] == "maintenance"
assert items["F6ZES_RESOLVED"]["promoted"] is False
assert items["F6ZES_RESOLVED"]["usable_frequency_published"] is False
assert BACKLOG["rules"]["theory_is_not_measured_reception"] is True

spec = importlib.util.spec_from_file_location("normandie_v05_theory", BUILDER)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
candidate = module.build_candidate(ROOT)
assert candidate["memory_count"] == 146
assert candidate["new_memory_count"] == 4
assert candidate["theoretical_coverage_memory_count"] == 4
assert candidate["field_reception_verified_memory_count"] == 0
assert candidate["status"] == "internal_candidate_theoretical_coverage_not_for_publication"
assert candidate["public_export_allowed"] is False

rows = candidate["rows"]
assert len(rows) == 146
base_rows = rows[:142]
new_rows = rows[142:]
with PUBLIC_V04.open(encoding="utf-8", newline="") as handle:
    public_base = list(csv.DictReader(handle))
assert base_rows == public_base
assert [int(row["Location"]) for row in new_rows] == [178, 179, 180, 181]
assert [row["Name"] for row in new_rows] == ["35-R3-IN", "35-R3-OUT", "53-ZHA-V", "53-ZHA-U"]
assert [round(float(row["Frequency"]), 6) for row in new_rows] == [145.075, 145.675, 145.4675, 432.575]
assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in new_rows)
assert all(row["Mode"] == "NFM" and row["TStep"] == "12.50" for row in new_rows)
assert all("couverture theorique Mortain" in row["Comment"] for row in new_rows)

all_freqs = [round(float(row["Frequency"]), 6) for row in rows]
all_names = [row["Name"] for row in rows]
all_locations = [int(row["Location"]) for row in rows]
new_freqs = [round(float(row["Frequency"]), 6) for row in new_rows]
assert len(all_freqs) == len(set(all_freqs)) == 146
assert len(all_names) == len(set(all_names)) == 146
assert len(all_locations) == len(set(all_locations)) == 146
assert 431.4125 not in new_freqs
assert 431.975 not in new_freqs
assert 430.375 not in new_freqs

with tempfile.TemporaryDirectory(prefix="radiopack-normandie-v05-theory-") as td:
    subprocess.run([
        sys.executable,
        str(BUILDER),
        "--root",
        str(ROOT),
        "--output-dir",
        td,
    ], check=True)
    output = Path(td) / "normandie-v0.5-internal.csv"
    manifest = Path(td) / "normandie-v0.5-internal.json"
    assert output.is_file() and manifest.is_file()
    with output.open(encoding="utf-8", newline="") as handle:
        rebuilt_rows = list(csv.DictReader(handle))
    assert len(rebuilt_rows) == 146
    info = json.loads(manifest.read_text(encoding="utf-8"))
    assert info["memory_count"] == 146
    assert len(info["candidate_csv_sha256"]) == 64

assert PUBLIC_V04.is_file()
assert not PUBLIC_V05.exists()

print("Sprint 112 Normandie v0.5: theoretical coverage promotes R3+F5ZHA to 146 RX internal candidate; theory labelled, F1ZOV/F6ZES remain deferred, no public v0.5 OK")
