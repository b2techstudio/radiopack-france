import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_annecy_release_readiness.py"
PLAN = ROOT / "research/annecy-alpes-leman-v0.2/prepublication-plan.json"
OPERATIONS = ROOT / "research/annecy-alpes-leman-v0.2/aviation-operational-gates.json"
SATELLITES = ROOT / "research/annecy-alpes-leman-v0.2/satellites-fm-inventory.json"
OPTIONS = ROOT / "generator/options.json"
BUILDER = ROOT / "tools/build_annecy_prepublication.py"
REVIEW_MAP = ROOT / "research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json"

for path in [CHECKER, PLAN, OPERATIONS, SATELLITES, OPTIONS, BUILDER, REVIEW_MAP]:
    assert path.is_file(), f"Fichier readiness manquant: {path.relative_to(ROOT)}"

spec = importlib.util.spec_from_file_location("annecy_readiness", CHECKER)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

result = module.evaluate(ROOT)
assert result["ready_for_public_prepublication"] is True
assert result["candidate_memory_count"] == 65
assert result["notam_blocks_generation"] is False
assert result["include_aviation_default"] is True
assert result["blockers"] == []
assert {item["id"] for item in result["advisories"]} == {"notam_fr", "notam_ch"}

plan = json.loads(PLAN.read_text(encoding="utf-8"))
assert plan["status"] == "prepublication_reviewed_not_public"
assert plan["candidate_memory_count"] == 65
assert plan["candidate_memory_count_without_aviation"] == 48
assert plan["prepublication_generation_allowed"] is True
assert plan["public_file_created"] is False
assert plan["public_export_allowed"] is False
assert plan["review_completed"] is True
assert plan["review_completed_on"] == "2026-08-08"
assert plan["review_required_before_public_export"] is False
assert plan["publication_ready_after_explicit_action"] is True
assert plan["review_map"] == "research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json"
assert plan["blocking_gates"] == []
assert set(plan["passed_blocking_gates"]) == {
    "airac_fr", "airac_ch", "pending_airfields", "dynamic_satellites"
}
assert set(plan["advisory_checks"]) == {"notam_fr", "notam_ch"}
assert plan["generator_options"]["notam_check_blocks_generation"] is False
assert plan["builder"] == "tools/build_annecy_prepublication.py"
assert not (ROOT / plan["reserved_public_output"]).exists(), "CSV v0.2 publié avant l'action explicite de publication"

review = json.loads(REVIEW_MAP.read_text(encoding="utf-8"))
assert review["status"] == "reviewed_prepublication_not_public"
assert review["expected_memory_count"] == 65
assert review["expected_memory_count_without_aviation"] == 48
assert len(review["rows"]) == 65

operations = json.loads(OPERATIONS.read_text(encoding="utf-8"))
gates = {gate["id"]: gate for gate in operations["gates"]}
assert operations["public_release_allowed"] is True
assert gates["dynamic_satellites"]["status"] == "passed_official_amsat_recheck"
assert gates["dynamic_satellites"]["checked"] == "2026-08-08"

satellites = json.loads(SATELLITES.read_text(encoding="utf-8"))
recheck = satellites["release_recheck"]
assert recheck["status"] == "passed_official_amsat_recheck"
assert recheck["checked"] == "2026-08-08"
assert recheck["ao91_limit_confirmed"] == "sunlight_only_due_to_battery"
assert {channel["name"] for channel in satellites["channels"]} == {
    "SAT-SO50", "SAT-AO91", "SAT-AO123"
}

options = json.loads(OPTIONS.read_text(encoding="utf-8"))
assert options["status"] == "backend_wired_prepublication_not_public_ui"
assert options["implementation"]["annecy_prepublication_builder"] == "tools/build_annecy_prepublication.py"
assert options["implementation"]["public_ui_wired"] is False
assert options["implementation"]["public_download_created"] is False

completed = subprocess.run(
    [sys.executable, str(CHECKER), "--root", str(ROOT), "--json"],
    text=True,
    capture_output=True,
)
assert completed.returncode == 0, completed.stdout + completed.stderr
cli_result = json.loads(completed.stdout)
assert cli_result["ready_for_public_prepublication"] is True
assert cli_result["blockers"] == []

print("Tests Annecy–Alpes–Léman release readiness: REVIEWED and still non-public")
