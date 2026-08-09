import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

required_files = [
    "README.md",
    ".gitignore",
    ".github/workflows/ci.yml",
    "REGIONAL-PACK-WORKFLOW.md",
    "SPRINT-23-MULTI-REGION-GENERATOR.md",
    "SPRINT-24-ISOLATED-GENERATOR-TESTS.md",
    "SPRINT-25-REGIONAL-STARTER.md",
    "SPRINT-26-BRETAGNE-INITIALIZATION.md",
    "generator/options.json",
    "generator/generate_chirp_csv.py",
    "tools/create_regional_pack.py",
    "tests/test_generator.py",
    "tests/test_regional_pack_starter.py",
    "tests/test_bretagne_research_scaffold.py",
    "tests/test_web_generator.py",
    "tests/test_pack_registry.py",
    "tests/test_built_public_pack_catalog.py",
    "research/bretagne-v0.1/README.md",
    "research/bretagne-v0.1/pack-plan.json",
    "research/bretagne-v0.1/source-registry.json",
    "research/bretagne-v0.1/publication-gates.json",
    "research/bretagne-v0.1/memory-plan.json",
    "research/annecy-alpes-leman-v0.2/prepublication-plan.json",
    "research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json",
    "website/src/lib/chirpPack.ts",
    "website/src/lib/annecyPack.ts",
    "website/src/lib/packRegistry.ts",
    "website/src/pages/generateur.astro",
    "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2.csv.ts",
    "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.2-sans-aviation.csv.ts",
    "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv",
]
for relative in required_files:
    path = ROOT / relative
    assert path.is_file(), f"Fichier manquant: {relative}"
    assert path.stat().st_size > 20, f"Fichier vide ou incomplet: {relative}"

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for expected in [
    "État actuel — Sprint 26",
    "Normandie v0.3.1** — 139 mémoires RX",
    "Annecy–Alpes–Léman v0.2** — 65 mémoires RX",
    "Bretagne v0.1 — recherche",
    "0 fréquence retenue",
    "aucun nombre cible de mémoires",
    "research/bretagne-v0.1/",
    "frequency_data_promoted: false",
    "Bretagne ne doit pas encore apparaître",
    "tools/create_regional_pack.py",
    "tests/test_bretagne_research_scaffold.py",
    "website/src/lib/packRegistry.ts",
    "Tests de génération isolés",
    "--output-root <dossier>",
    "nothing to commit, working tree clean",
    "SPRINT-26-BRETAGNE-INITIALIZATION.md",
    "Le `README.md` doit être mis à jour à chaque changement important et à la fin de chaque sprint",
]:
    assert expected in readme, f"README non actualisé: {expected}"

gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
assert "research/annecy-alpes-leman-v0.2/generated/" in gitignore
assert "__pycache__/" in gitignore
assert "*.py[cod]" in gitignore

options = json.loads((ROOT / "generator/options.json").read_text(encoding="utf-8"))
assert options["schema_version"] == "3.0"
assert options["status"] == "multi_region_public_generator"
assert options["implementation"]["published_pack_count"] == 2
assert options["implementation"]["public_pack_registry"] == "website/src/lib/packRegistry.ts"
assert {pack["id"] for pack in options["pack_selection"]["packs"]} == {"annecy-alpes-leman", "normandie"}
assert options["options"]["notam_check"]["affects_csv_content"] is False
assert options["options"]["notam_check"]["blocks_generation"] is False

bretagne_plan = json.loads((ROOT / "research/bretagne-v0.1/pack-plan.json").read_text(encoding="utf-8"))
bretagne_sources = json.loads((ROOT / "research/bretagne-v0.1/source-registry.json").read_text(encoding="utf-8"))
bretagne_gates = json.loads((ROOT / "research/bretagne-v0.1/publication-gates.json").read_text(encoding="utf-8"))
bretagne_memory = json.loads((ROOT / "research/bretagne-v0.1/memory-plan.json").read_text(encoding="utf-8"))
assert bretagne_plan["status"] == "research_scaffold_not_public"
assert bretagne_plan["memory_plan"]["expected_memory_count"] is None
assert bretagne_plan["memory_plan"]["blocks"] == []
assert bretagne_plan["publication"]["public_export_allowed"] is False
assert bretagne_plan["publication"]["public_registry_allowed"] is False
assert bretagne_plan["publication"]["public_routes_allowed"] is False
assert len(bretagne_sources["sources"]) == 5
assert all(source["frequency_data_promoted"] is False for source in bretagne_sources["sources"])
assert bretagne_gates["public_release_allowed"] is False
assert all(not gate["status"].startswith("passed_") for gate in bretagne_gates["gates"])
assert bretagne_memory["expected_memory_count"] is None
assert bretagne_memory["blocks"] == []

plan = json.loads((ROOT / "research/annecy-alpes-leman-v0.2/prepublication-plan.json").read_text(encoding="utf-8"))
assert plan["status"] == "published_v0.2"
assert plan["candidate_memory_count"] == 65
assert plan["candidate_memory_count_without_aviation"] == 48
assert plan["public_export_allowed"] is True

review = json.loads((ROOT / "research/annecy-alpes-leman-v0.2/prepublication-reviewed-memory-map.json").read_text(encoding="utf-8"))
assert review["expected_memory_count"] == 65
assert review["expected_memory_count_without_aviation"] == 48
assert len(review["rows"]) == 65

regions = json.loads((ROOT / "website/src/data/regions.json").read_text(encoding="utf-8"))
assert len(regions) == 2
assert {region["slug"] for region in regions} == {"annecy-haute-savoie", "normandie"}
assert next(region for region in regions if region["slug"] == "annecy-haute-savoie")["memoryCount"] == 65
assert next(region for region in regions if region["slug"] == "normandie")["memoryCount"] == 139

generic_library = (ROOT / "website/src/lib/chirpPack.ts").read_text(encoding="utf-8")
for expected in ["assemblePack", "validatePlacedChannels", "buildChirpCsv", '"off"', '"0.000000"']:
    assert expected in generic_library, f"Moteur générique incomplet: {expected}"

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
for expected in [
    'id: "annecy-alpes-leman"',
    'id: "normandie"',
    'memoryCount: 65',
    'memoryCount: 48',
    'memoryCount: 139',
    '/downloads/normandie/radiopack-france-normandie-v0.3.1.csv',
]:
    assert expected in registry, f"Registre public incomplet: {expected}"
assert registry.count('downloadUrl: "') == 3
assert 'id: "bretagne"' not in registry
assert not (ROOT / "website/src/pages/regions/bretagne.astro").exists()
assert not (ROOT / "website/public/downloads/bretagne").exists()
assert not (ROOT / "website/src/pages/downloads/bretagne").exists()

historical_generator = (ROOT / "generator/generate_chirp_csv.py").read_text(encoding="utf-8")
for expected in ['"--output-root"', "sortie isolée", "Normandie v0.3.1 est un artefact publié figé"]:
    assert expected in historical_generator, f"Isolation générateur absente: {expected}"
assert "radiopack-france-normandie-v0.3.1.csv" not in historical_generator

generator_test = (ROOT / "tests/test_generator.py").read_text(encoding="utf-8")
for expected in ["tempfile.TemporaryDirectory", '"--output-root"', "FROZEN_NORMANDIE", "read_bytes() == original_bytes"]:
    assert expected in generator_test, f"Garde-fou test générateur absent: {expected}"

starter = (ROOT / "tools/create_regional_pack.py").read_text(encoding="utf-8")
for expected in [
    "research_scaffold_not_public",
    '"public_export_allowed": False',
    '"public_registry_allowed": False',
    '"public_routes_allowed": False',
    '"expected_memory_count": None',
    '"no_artificial_fill": True',
    '"published_versions_are_immutable": True',
    '"--output-root"',
    "Le dossier existe déjà",
    "NOT PUBLIC",
]:
    assert expected in starter, f"Starter régional incomplet: {expected}"
assert "packRegistry.ts" in starter
assert "website/public" not in starter

starter_test = (ROOT / "tests/test_regional_pack_starter.py").read_text(encoding="utf-8")
for expected in [
    "TemporaryDirectory",
    "pack-test-v0.1",
    "public_export_allowed",
    "public_registry_allowed",
    "public_routes_allowed",
    "assert not (output_root / \"website\").exists()",
    "Le starter a modifié un fichier public suivi",
]:
    assert expected in starter_test, f"Test starter incomplet: {expected}"

bretagne_test = (ROOT / "tests/test_bretagne_research_scaffold.py").read_text(encoding="utf-8")
for expected in [
    "0 public side effects OK",
    "frequency_data_promoted",
    'id: "bretagne"',
    '"slug": "bretagne"',
    "website/src/pages/regions/bretagne.astro",
]:
    assert expected in bretagne_test, f"Test Bretagne incomplet: {expected}"

workflow_doc = (ROOT / "REGIONAL-PACK-WORKFLOW.md").read_text(encoding="utf-8")
for expected in ["chirpPack.ts", "packRegistry.ts", "carte de revue", "artefact immuable", "README.md"]:
    assert expected in workflow_doc, f"Workflow régional incomplet: {expected}"

workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
for expected in [
    "Test CSV generator in isolated output",
    "python tests/test_generator.py",
    "python tests/test_site_files.py",
    "python tests/test_pack_registry.py",
    "Test regional pack research starter",
    "python tests/test_regional_pack_starter.py",
    "Test Bretagne research scaffold",
    "python tests/test_bretagne_research_scaffold.py",
    "python tests/test_web_generator.py",
    "python tests/test_built_public_pack_catalog.py",
    "npm run build",
    "radiopack-ci/complete",
]:
    assert expected in workflow, f"Étape CI absente: {expected}"

print("Tests RadioPack Sprint 26 Bretagne research-only initialization: OK")
