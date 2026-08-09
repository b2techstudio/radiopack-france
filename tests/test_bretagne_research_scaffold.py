import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research/bretagne-v0.1"

required = [
    RESEARCH / "README.md",
    RESEARCH / "pack-plan.json",
    RESEARCH / "source-registry.json",
    RESEARCH / "publication-gates.json",
    RESEARCH / "memory-plan.json",
]
for path in required:
    assert path.is_file(), f"Fichier Bretagne manquant: {path.relative_to(ROOT)}"

plan = json.loads((RESEARCH / "pack-plan.json").read_text(encoding="utf-8"))
sources = json.loads((RESEARCH / "source-registry.json").read_text(encoding="utf-8"))
gates = json.loads((RESEARCH / "publication-gates.json").read_text(encoding="utf-8"))
memory = json.loads((RESEARCH / "memory-plan.json").read_text(encoding="utf-8"))

assert plan["status"] == "research_scaffold_not_public"
assert plan["pack"] == {"name": "Bretagne", "slug": "bretagne", "target_version": "0.1"}
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

assert sources["status"] == "seed_sources_identified_no_frequency_extraction"
assert sources["pack"]["slug"] == "bretagne"
assert len(sources["sources"]) == 5
source_ids = {source["id"] for source in sources["sources"]}
assert source_ids == {
    "SIA-LFRB-EAIP-2026-06-11",
    "SIA-LFRN-EAIP-2026-06-11",
    "ANFR-OPEN-DATA",
    "ANFR-RADIOAMATEUR-MISSIONS",
    "ANFR-RADIOAMATEUR-ANNUAIRE",
}
assert all(source["accessed"] == "2026-08-09" for source in sources["sources"])
assert all(source["frequency_data_promoted"] is False for source in sources["sources"])
assert all("not_yet_extracted" in source["status"] for source in sources["sources"])
assert sources["rules"]["prefer_primary_sources"] is True
assert sources["rules"]["seed_source_does_not_equal_validated_frequency"] is True

assert gates["status"] == "blocked_research_not_started"
assert gates["public_release_allowed"] is False
assert len(gates["gates"]) == 6
assert all(gate["required_for_public_release"] is True for gate in gates["gates"])
assert all(not gate["status"].startswith("passed_") for gate in gates["gates"])

assert memory["status"] == "draft_no_channels"
assert memory["expected_memory_count"] is None
assert memory["blocks"] == []
assert memory["reserved_positions"] == []
assert memory["rules"]["duplex"] == "off"
assert memory["rules"]["no_artificial_fill"] is True

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8").lower()
regions = (ROOT / "website/src/data/regions.json").read_text(encoding="utf-8").lower()
assert 'id: "bretagne"' not in registry
assert '"slug": "bretagne"' not in regions
assert not (ROOT / "website/src/pages/regions/bretagne.astro").exists()
assert not (ROOT / "website/public/downloads/bretagne").exists()
assert not (ROOT / "website/src/pages/downloads/bretagne").exists()

readme = (RESEARCH / "README.md").read_text(encoding="utf-8")
assert "aucune fréquence n'est encore retenue" in readme
assert "aucune entrée n'est ajoutée" in readme
assert "sources de départ" in readme

print("Tests RadioPack Sprint 26 Bretagne research scaffold: 0 frequencies, 0 public side effects OK")
