import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "tools/create_regional_pack.py"
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"
REGIONS = ROOT / "website/src/data/regions.json"

for path in [STARTER, REGISTRY, REGIONS]:
    assert path.is_file(), f"Fichier starter manquant: {path.relative_to(ROOT)}"

tracked_before = {
    REGISTRY: REGISTRY.read_bytes(),
    REGIONS: REGIONS.read_bytes(),
}

with tempfile.TemporaryDirectory(prefix="radiopack-regional-starter-") as tmp:
    output_root = Path(tmp)
    completed = subprocess.run(
        [
            sys.executable,
            str(STARTER),
            "--root",
            str(ROOT),
            "--output-root",
            str(output_root),
            "--name",
            "Pack Test",
            "--slug",
            "pack-test",
            "--version",
            "0.1",
        ],
        text=True,
        capture_output=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "NOT PUBLIC" in completed.stdout

    target = output_root / "research/pack-test-v0.1"
    expected_files = {
        "README.md",
        "pack-plan.json",
        "source-registry.json",
        "publication-gates.json",
        "memory-plan.json",
    }
    assert target.is_dir()
    assert {path.name for path in target.iterdir()} == expected_files
    assert not (output_root / "website").exists()

    plan = json.loads((target / "pack-plan.json").read_text(encoding="utf-8"))
    assert plan["status"] == "research_scaffold_not_public"
    assert plan["pack"] == {"name": "Pack Test", "slug": "pack-test", "target_version": "0.1"}
    assert plan["memory_plan"]["expected_memory_count"] is None
    assert plan["memory_plan"]["blocks"] == []
    assert plan["publication"]["public_export_allowed"] is False
    assert plan["publication"]["public_registry_allowed"] is False
    assert plan["publication"]["public_routes_allowed"] is False
    assert plan["publication"]["review_required"] is True
    assert plan["publication"]["review_completed"] is False
    assert plan["rules"]["rx_only"] is True
    assert plan["rules"]["duplex"] == "off"
    assert plan["rules"]["offset"] == "0.000000"
    assert plan["rules"]["max_memories"] == 200
    assert plan["rules"]["max_name_length"] == 10
    assert plan["rules"]["no_artificial_fill"] is True
    assert plan["rules"]["published_versions_are_immutable"] is True

    sources = json.loads((target / "source-registry.json").read_text(encoding="utf-8"))
    assert sources["status"] == "research_sources_empty"
    assert sources["sources"] == []
    assert sources["rules"]["prefer_primary_sources"] is True
    assert sources["rules"]["unverified_data_must_not_enter_public_pack"] is True

    memory = json.loads((target / "memory-plan.json").read_text(encoding="utf-8"))
    assert memory["status"] == "draft_no_channels"
    assert memory["expected_memory_count"] is None
    assert memory["blocks"] == []
    assert memory["reserved_positions"] == []

    gates = json.loads((target / "publication-gates.json").read_text(encoding="utf-8"))
    assert gates["public_release_allowed"] is False
    assert gates["status"] == "blocked_research_not_started"
    gate_by_id = {gate["id"]: gate for gate in gates["gates"]}
    assert set(gate_by_id) == {
        "sources",
        "memory_plan",
        "data_validation",
        "dynamic_rechecks",
        "review_map",
        "explicit_publication",
    }
    assert all(gate["required_for_public_release"] is True for gate in gates["gates"])
    assert gate_by_id["explicit_publication"]["status"] == "blocked_until_all_previous_gates_pass"

    starter_readme = (target / "README.md").read_text(encoding="utf-8")
    assert "aucune fréquence n'est encore retenue" in starter_readme
    assert "aucun nombre cible de mémoires n'est imposé" in starter_readme
    assert "aucune entrée n'est ajoutée à `website/src/lib/packRegistry.ts`" in starter_readme

    second = subprocess.run(
        [
            sys.executable,
            str(STARTER),
            "--root",
            str(ROOT),
            "--output-root",
            str(output_root),
            "--name",
            "Pack Test",
            "--slug",
            "pack-test",
            "--version",
            "0.1",
        ],
        text=True,
        capture_output=True,
    )
    assert second.returncode != 0
    assert "existe déjà" in second.stderr

with tempfile.TemporaryDirectory(prefix="radiopack-regional-invalid-") as tmp:
    invalid = subprocess.run(
        [
            sys.executable,
            str(STARTER),
            "--output-root",
            tmp,
            "--name",
            "Pack invalide",
            "--slug",
            "Pack Invalide",
        ],
        text=True,
        capture_output=True,
    )
    assert invalid.returncode != 0
    assert "Slug invalide" in invalid.stderr

for path, before in tracked_before.items():
    assert path.read_bytes() == before, f"Le starter a modifié un fichier public suivi: {path.relative_to(ROOT)}"

assert "pack-test" not in REGISTRY.read_text(encoding="utf-8")
assert "Pack Test" not in REGIONS.read_text(encoding="utf-8")

print("Tests RadioPack Sprint 25 regional starter: research-only, no public side effects OK")
