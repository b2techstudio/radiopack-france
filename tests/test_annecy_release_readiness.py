import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "tools/check_annecy_release_readiness.py"
PLAN = ROOT / "research/annecy-alpes-leman-v0.2/prepublication-plan.json"
OPERATIONS = ROOT / "research/annecy-alpes-leman-v0.2/aviation-operational-gates.json"
OPTIONS = ROOT / "generator/options.json"

for path in [CHECKER, PLAN, OPERATIONS, OPTIONS]:
    assert path.is_file(), f"Fichier readiness manquant: {path.relative_to(ROOT)}"

spec = importlib.util.spec_from_file_location("annecy_readiness", CHECKER)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

result = module.evaluate(ROOT)
assert result["ready_for_public_prepublication"] is False
assert result["candidate_memory_count"] == 65
assert result["notam_blocks_generation"] is False
assert result["include_aviation_default"] is True
assert [item["id"] for item in result["blockers"]] == ["dynamic_satellites"]
assert {item["id"] for item in result["advisories"]} == {"notam_fr", "notam_ch"}

plan = json.loads(PLAN.read_text(encoding="utf-8"))
assert plan["status"] == "blocked_dynamic_satellite_recheck"
assert plan["candidate_memory_count"] == 65
assert plan["public_file_created"] is False
assert plan["public_export_allowed"] is False
assert plan["blocking_gates"] == ["dynamic_satellites"]
assert set(plan["advisory_checks"]) == {"notam_fr", "notam_ch"}
assert plan["generator_options"]["notam_check_blocks_generation"] is False
assert not (ROOT / plan["reserved_public_output"]).exists(), "CSV v0.2 publié trop tôt"

completed = subprocess.run(
    [sys.executable, str(CHECKER), "--root", str(ROOT), "--json"],
    text=True,
    capture_output=True,
)
assert completed.returncode == 2, completed.stdout + completed.stderr
cli_result = json.loads(completed.stdout)
assert cli_result["ready_for_public_prepublication"] is False
assert [item["id"] for item in cli_result["blockers"]] == ["dynamic_satellites"]

print("Tests Annecy–Alpes–Léman release readiness: OK")
