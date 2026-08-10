import csv
import importlib.util
import io
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_CHECK = ROOT / "tools/check_normandie_v04_source_consistency.py"
DOSSIER = ROOT / "tools/build_normandie_v04_decision_dossier.py"
PREVIEW = ROOT / "tools/build_normandie_v04_candidate_preview.py"
BLOCKERS = ROOT / "tools/build_normandie_v04_release_blockers.py"
CONTRACT = ROOT / "research/normandie-v0.4/source-consistency-contract.json"

for p in (SOURCE_CHECK, DOSSIER, PREVIEW, BLOCKERS, CONTRACT):
    assert p.is_file(), f"Missing expected file: {p}"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


source = load_module("source_check_test", SOURCE_CHECK)
dossier_builder = load_module("decision_dossier_test", DOSSIER)
preview_builder = load_module("candidate_preview_test", PREVIEW)
blocker_builder = load_module("release_blockers_test", BLOCKERS)

check = source.evaluate(ROOT)
assert check["consistent"] is True
assert check["error_count"] == 0
assert check["public_export_allowed"] is False

D = dossier_builder.build(ROOT)
assert D["status"] == "internal_decision_dossier_not_public"
assert D["source_truth_consistent"] is True
assert D["current_internal_candidate_memory_count"] == 142
assert D["known_gate_ceiling"] == 147
assert D["eligible_addition_count"] == 0
assert D["candidate_memory_count_if_current_plan_applied"] == 142
assert D["public_release_ready"] is False
assert D["public_export_allowed"] is False
assert D["station_decisions"]["F1ZOV_EQUEURDREVILLE"]["decision"] == "blocked"
assert D["station_decisions"]["F6ZES_SOURDEVAL"]["decision"] == "unresolved"

manifest, data = preview_builder.build_preview(ROOT)
assert manifest["status"] == "guarded_candidate_preview_not_public"
assert manifest["base_internal_candidate_memory_count"] == 142
assert manifest["eligible_addition_count"] == 0
assert manifest["preview_memory_count"] == 142
assert manifest["candidate_mutated"] is False
assert manifest["public_export_allowed"] is False
rows = list(csv.DictReader(io.StringIO(data.decode("utf-8"))))
assert len(rows) == 142

synthetic_plan = {
    "public_export_allowed": False,
    "plan_applied": False,
    "additions": [
        {"gate_id": "R3_MORTAIN_RX", "name_hint": "ZBX-IN", "frequency_mhz": 145.075, "role": "R3 input RX", "proposed_internal_location": 178},
        {"gate_id": "R3_MORTAIN_RX", "name_hint": "ZBX-OUT", "frequency_mhz": 145.675, "role": "R3 output RX", "proposed_internal_location": 179},
    ],
}
synthetic_manifest, synthetic_data = preview_builder.build_preview(ROOT, synthetic_plan)
assert synthetic_manifest["preview_memory_count"] == 144
assert synthetic_manifest["eligible_addition_count"] == 2
synthetic_rows = list(csv.DictReader(io.StringIO(synthetic_data.decode("utf-8"))))
assert len(synthetic_rows) == 144
for row in synthetic_rows[-2:]:
    assert row["Duplex"] == "off"
    assert row["Offset"] == "0.000000"
    assert len(row["Name"]) <= 10

with tempfile.TemporaryDirectory(prefix="radiopack-v04-decision-") as tmp:
    jp, mp, written = dossier_builder.write(ROOT, Path(tmp) / "dossier")
    assert jp.is_file() and mp.is_file()
    assert written["eligible_addition_count"] == 0
    jp2, cp2, preview_written = preview_builder.write(ROOT, Path(tmp) / "preview")
    assert jp2.is_file() and cp2.is_file()
    assert preview_written["preview_memory_count"] == 142
    jp3, mp3, blockers_written = blocker_builder.write(ROOT, Path(tmp) / "blockers")
    assert jp3.is_file() and mp3.is_file()
    assert blockers_written["release_allowed"] is False
    assert blockers_written["prepublication_ready"] is False

blockers = blocker_builder.build(ROOT)
assert blockers["status"] == "prepublication_blockers_not_public"
assert blockers["blocking_count"] == 6
assert blockers["prepublication_ready"] is False
assert blockers["public_registry_has_v04"] is False
assert blockers["public_activation_pending"] is True
assert blockers["release_allowed"] is False
assert blockers["public_export_allowed"] is False
ids = {x["id"] for x in blockers["blockers"]}
assert {"F1ZBX_R3", "F5ZHA_LAVAL", "F1ZOV_EQUEURDREVILLE", "F6ZES_SOURDEVAL", "FINAL_REVIEW", "FINAL_MEMORY_PLAN"} == ids

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'version: "v0.4"' not in registry

print(
    "Tests Normandie v0.4 decision pipeline: source truth consistent, internal decision dossier blocked, "
    "current preview remains 142 memories, synthetic gated preview safely reaches 144 RX-only memories, "
    "6 prepublication blockers remain and public activation stays separate, no public mutation OK"
)
