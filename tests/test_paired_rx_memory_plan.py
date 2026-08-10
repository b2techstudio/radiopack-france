import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

plan = json.loads((ROOT / "research/paired-rx-deduplicated-memory-plan.json").read_text(encoding="utf-8"))
assert plan["schema_version"] == "1.2"
assert plan["status"] == "research_deduplicated_memory_plan_not_public"
assert plan["source_plan"] == "research/paired-rx-next-version-plan.json"
assert plan["policy"] == "research/paired-rx-policy.json"
assert plan["export_contract"]["chirp_duplex"] == "off"
assert plan["export_contract"]["chirp_offset"] == "0.000000"
assert plan["export_contract"]["tx_disabled"] is True
assert plan["export_contract"]["same_rf_frequency_kept_once_per_region"] is True
assert plan["export_contract"]["memory_positions_assigned"] is False
assert plan["export_contract"]["public_pack_mutation_allowed"] is False

regions = {region["id"]: region for region in plan["regions"]}
assert set(regions) == {"normandie-v0.4", "annecy-alpes-leman-v0.3", "bretagne-v0.1"}
assert regions["normandie-v0.4"]["unique_frequency_count"] == 12
assert regions["annecy-alpes-leman-v0.3"]["unique_frequency_count"] == 10
assert regions["bretagne-v0.1"]["unique_frequency_count"] == 29

for region in regions.values():
    memories = region["memories"]
    assert len(memories) == region["unique_frequency_count"]
    frequencies = [item["frequency_mhz"] for item in memories]
    assert len(frequencies) == len(set(frequencies)), f"Duplicate RF frequency in {region['id']}"
    for item in memories:
        assert len(item["name_hint"]) <= 10
        assert item["roles"]
        assert item["selection_status"]

normandie = {item["name_hint"]: item for item in regions["normandie-v0.4"]["memories"]}
for name, frequency in {
    "ZHY-IN": 145.0875,
    "ZHY-OUT": 145.6875,
    "ZCE-IN": 145.1000,
    "ZCE-OUT": 145.7000,
    "ZBX-IN": 145.0750,
    "ZBX-OUT": 145.6750,
    "ZHA-A": 145.4675,
    "ZHA-B": 432.5750,
    "ZBL-A": 145.2500,
    "ZBL-B": 431.2500,
    "ZOV-A": 430.3750,
    "ZOV-B": 431.9750,
}.items():
    assert normandie[name]["frequency_mhz"] == frequency
excluded_normandie = "\n".join(regions["normandie-v0.4"]["excluded_or_unresolved"])
assert "F6ZES" in excluded_normandie
assert "F1ZBL" not in excluded_normandie
assert "F5ZHA" not in excluded_normandie

annecy = {item["name_hint"]: item for item in regions["annecy-alpes-leman-v0.3"]["memories"]}
assert annecy["SAT-UP850"]["frequency_mhz"] == 145.8500
assert set(annecy["SAT-UP850"]["roles"]) == {"SO-50 uplink RX", "AO-123 uplink RX"}
assert annecy["X432512"]["frequency_mhz"] == 432.5125
assert set(annecy["X432512"]["roles"]) == {"F1ZHG transponder side B", "F5ZGT transponder side B"}

bretagne = {item["name_hint"]: item for item in regions["bretagne-v0.1"]["memories"]}
expected_marine = {
    "M63-S": 156.1750,
    "M63-C": 160.7750,
    "M64-S": 156.2250,
    "M64-C": 160.8250,
    "M79-S": 156.9750,
    "M79-C": 161.5750,
    "M80-S": 157.0250,
    "M80-C": 161.6250,
}
for name, frequency in expected_marine.items():
    assert bretagne[name]["frequency_mhz"] == frequency

assert bretagne["X432650"]["frequency_mhz"] == 432.6500
assert set(bretagne["X432650"]["roles"]) == {
    "F5ZIS transponder side B",
    "F5ZIT transponder side B",
    "F5ZIU transponder side B",
    "F5ZIV transponder side B",
    "F5ZJR transponder side B",
}
for name, frequency in {
    "ZIU-A": 145.4625,
    "ZIV-A": 145.4875,
    "ZJR-A": 145.2875,
    "ZMU-OUT": 430.3250,
    "ZMU-IN": 439.7250,
    "ZBZ-U": 431.2000,
    "ZBZ-VA": 145.6250,
    "ZBZ-VB": 145.0250,
}.items():
    assert bretagne[name]["frequency_mhz"] == frequency

assert bretagne["X145262"]["frequency_mhz"] == 145.2625
assert set(bretagne["X145262"]["roles"]) == {
    "F1ZGS transponder side A",
    "F5ZDV transponder side A",
    "F5ZZL transponder side A",
}
assert set(bretagne["ZPE-IN"]["roles"]) == {"F5ZPE repeater input", "F1ZBZ repeater emission path"}
assert set(bretagne["ZPE-OUT"]["roles"]) == {"F5ZPE repeater output", "F1ZBZ repeater reception path"}

excluded_bretagne = "\n".join(regions["bretagne-v0.1"]["excluded_or_unresolved"])
assert "F5ZPV" in excluded_bretagne
assert "F5ZZH" in excluded_bretagne
assert "F1ZUG" in excluded_bretagne
assert "F1ZBZ" not in excluded_bretagne
assert all(name not in bretagne for name in ("ZPV-IN", "ZPV-OUT", "ZZH-IN", "ZZH-OUT"))

assert plan["rules"]["counts_are_research_counts_not_pack_targets"] is True
assert plan["rules"]["memory_names_are_hints_not_final_public_names"] is True
assert plan["rules"]["stopped_or_unresolved_links_excluded_from_active_memory_list"] is True
assert plan["rules"]["no_public_export"] is True

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'id: "bretagne"' not in registry
assert 'version: "v0.4"' not in registry
assert 'version: "v0.3"' not in registry

print("Tests RadioPack paired RX deduplicated memory research plan: Normandie 12, Annecy 10, Bretagne 29 unique RX frequencies, REF expansion and resolved Normandie pairs deduplicated, TX-off contract and no public mutation OK")
