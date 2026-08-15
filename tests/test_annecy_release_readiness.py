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
PUBLIC_ROUTE = ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv.ts"
PACK_REGISTRY = ROOT / "website/src/lib/packRegistry.ts"
V03_RECORD = ROOT / "research/annecy-alpes-leman-v0.3/publication-record.json"
V03_FULL = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv"
V03_NO_AIR = ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv"

for path in [CHECKER, PLAN, OPERATIONS, SATELLITES, OPTIONS, BUILDER, REVIEW_MAP, PUBLIC_ROUTE, PACK_REGISTRY, V03_RECORD, V03_FULL, V03_NO_AIR]:
    assert path.is_file(), f"Fichier readiness manquant: {path.relative_to(ROOT)}"

spec = importlib.util.spec_from_file_location("annecy_readiness", CHECKER)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

# Historical v0.2 readiness remains replayable and auditable.
result = module.evaluate(ROOT)
assert result["ready_for_public_prepublication"] is True
assert result["candidate_memory_count"] == 65
assert result["notam_blocks_generation"] is False
assert result["include_aviation_default"] is True
assert result["blockers"] == []
assert {item["id"] for item in result["advisories"]} == {"notam_fr", "notam_ch"}

plan = json.loads(PLAN.read_text(encoding="utf-8"))
assert plan["status"] == "published_v0.2"
assert plan["candidate_memory_count"] == 65
assert plan["candidate_memory_count_without_aviation"] == 48
assert plan["public_file_created"] is True
assert plan["public_export_allowed"] is True
assert plan["publication_completed"] is True
assert plan["publication_completed_on"] == "2026-08-08"
assert plan["review_completed"] is True
assert plan["review_required_before_public_export"] is False
assert plan["publication_ready_after_explicit_action"] is False
assert plan["blocking_gates"] == []
assert set(plan["passed_blocking_gates"]) == {"airac_fr", "airac_ch", "pending_airfields", "dynamic_satellites"}
assert set(plan["advisory_checks"]) == {"notam_fr", "notam_ch"}
assert plan["public_delivery_mode"] == "astro_prerendered_csv_routes_and_browser_generator"

review = json.loads(REVIEW_MAP.read_text(encoding="utf-8"))
assert review["expected_memory_count"] == 65
assert review["expected_memory_count_without_aviation"] == 48
assert len(review["rows"]) == 65

operations = json.loads(OPERATIONS.read_text(encoding="utf-8"))
gates = {gate["id"]: gate for gate in operations["gates"]}
assert operations["public_release_allowed"] is True
assert gates["dynamic_satellites"]["status"] == "passed_official_amsat_recheck"

satellites = json.loads(SATELLITES.read_text(encoding="utf-8"))
assert satellites["release_recheck"]["status"] == "passed_official_amsat_recheck"
assert satellites["release_recheck"]["ao91_limit_confirmed"] == "sunlight_only_due_to_battery"

options = json.loads(OPTIONS.read_text(encoding="utf-8"))
assert options["schema_version"] == "3.0"
assert options["status"] == "multi_region_public_generator"
assert options["implementation"]["public_ui_wired"] is True
assert options["implementation"]["public_download_created"] is True
assert options["implementation"]["public_pack_registry"] == "website/src/lib/packRegistry.ts"
assert options["implementation"]["default_pack"] == "annecy-alpes-leman"
assert {pack["id"] for pack in options["pack_selection"]["packs"]} == {"annecy-alpes-leman", "normandie", "bretagne"}
assert options["options"]["include_aviation"]["scope"] == ["annecy-alpes-leman"]
assert options["options"]["include_aviation"]["annecy_memory_count_when_enabled"] == 76
assert options["options"]["include_aviation"]["annecy_memory_count_when_disabled"] == 59
assert options["options"]["notam_check"]["scope"] == ["annecy-alpes-leman"]

# The current public registry now points to immutable v0.3, while the v0.2 route
# above remains available as historical release evidence.
registry = PACK_REGISTRY.read_text(encoding="utf-8")
assert 'id: "annecy-alpes-leman"' in registry
assert 'version: "v0.3"' in registry
assert 'memoryCount: 76' in registry
assert 'memoryCount: 59' in registry
assert '/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv' in registry
assert '/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv' in registry

record = json.loads(V03_RECORD.read_text(encoding="utf-8"))
assert record["status"] == "published_immutable"
assert record["version"] == "0.3"
assert record["full_memory_count"] == 76
assert record["without_aviation_memory_count"] == 59
assert record["aviation_memory_count"] == 17
assert record["new_unique_rf_memory_count"] == 11
assert record["rules"]["immutable"] is True
assert record["rules"]["rx_only"] is True

completed = subprocess.run(
    [sys.executable, str(CHECKER), "--root", str(ROOT), "--json"],
    text=True,
    capture_output=True,
)
assert completed.returncode == 0, completed.stdout + completed.stderr
cli_result = json.loads(completed.stdout)
assert cli_result["ready_for_public_prepublication"] is True
assert cli_result["blockers"] == []

print("Tests Annecy–Alpes–Léman release readiness: PUBLISHED v0.2 + multi-region generator; historical readiness replayed and current immutable v0.3 76/59 recognized OK")
