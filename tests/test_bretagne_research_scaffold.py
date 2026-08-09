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
    RESEARCH / "maritime-zones.json",
    RESEARCH / "emergency-relays.json",
]
for path in required:
    assert path.is_file(), f"Fichier Bretagne manquant: {path.relative_to(ROOT)}"

plan = json.loads((RESEARCH / "pack-plan.json").read_text(encoding="utf-8"))
sources = json.loads((RESEARCH / "source-registry.json").read_text(encoding="utf-8"))
gates = json.loads((RESEARCH / "publication-gates.json").read_text(encoding="utf-8"))
memory = json.loads((RESEARCH / "memory-plan.json").read_text(encoding="utf-8"))
maritime = json.loads((RESEARCH / "maritime-zones.json").read_text(encoding="utf-8"))
emergency = json.loads((RESEARCH / "emergency-relays.json").read_text(encoding="utf-8"))

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

assert sources["status"] == "seed_sources_identified_maritime_zoning_in_progress_no_frequency_extraction"
assert sources["pack"]["slug"] == "bretagne"
assert len(sources["sources"]) == 10
source_ids = {source["id"] for source in sources["sources"]}
for expected in {
    "SIA-LFRB-EAIP-2026-06-11",
    "SIA-LFRN-EAIP-2026-06-11",
    "ANFR-OPEN-DATA",
    "ANFR-RADIOAMATEUR-MISSIONS",
    "ANFR-RADIOAMATEUR-ANNUAIRE",
    "MER-VHF-CANAL16-2026",
    "PREMAR-ATL-CROSS-SRR",
    "PREMAR-CORSEN-AUDIERNE-2026",
    "PREMAR-ETEL-CONCARNEAU-2026",
    "MER-VHF-METEO-CHANNELS",
}:
    assert expected in source_ids
assert all(source["accessed"] == "2026-08-09" for source in sources["sources"])
assert all(source["frequency_data_promoted"] is False for source in sources["sources"])
assert sources["rules"]["prefer_primary_sources"] is True
assert sources["rules"]["seed_source_does_not_equal_validated_frequency"] is True
assert sources["rules"]["maritime_cross_assignment_must_be_zone_specific"] is True
assert sources["rules"]["exact_current_srr_boundary_required_before_publication"] is True

assert gates["status"] == "blocked_research_in_progress"
assert gates["public_release_allowed"] is False
assert len(gates["gates"]) == 8
assert all(gate["required_for_public_release"] is True for gate in gates["gates"])
assert all(not gate["status"].startswith("passed_") for gate in gates["gates"])
gate_map = {gate["id"]: gate for gate in gates["gates"]}
assert gate_map["maritime_zoning"]["status"] == "etel_penmarch_interface_verified_corsen_sites_and_radio_overlap_pending"
assert gate_map["emergency_relay_inventory"]["status"] == "adrasec_22_29_35_56_and_regional_relays_pending"

assert memory["status"] == "draft_no_channels"
assert memory["expected_memory_count"] is None
assert memory["blocks"] == []
assert memory["reserved_positions"] == []
assert memory["rules"]["duplex"] == "off"
assert memory["rules"]["no_artificial_fill"] is True

assert maritime["status"] == "research_zoning_penmarch_interface_confirmed_vhf_overlap_pending"
assert maritime["rules"]["single_bretagne_maritime_zone_forbidden"] is True
assert maritime["rules"]["north_south_operational_split_required"] is True
assert maritime["rules"]["channel_16_frequency_is_common_but_cross_context_is_zone_specific"] is True
assert maritime["rules"]["cross_remote_sites_must_be_researched_by_zone"] is True
assert maritime["rules"]["weather_broadcast_channels_must_be_researched_by_zone"] is True
assert maritime["rules"]["amateur_repeaters_must_be_tagged_by_breton_subzone"] is True
assert maritime["rules"]["etel_srr_starts_at_pointe_de_penmarch_primary_sourced"] is True
assert maritime["rules"]["corsen_detailed_srr_and_vhf_overlap_still_pending"] is True
assert maritime["rules"]["no_frequency_promoted_from_this_file"] is True
zones = {zone["id"]: zone for zone in maritime["zones"]}
assert set(zones) == {"bretagne-nord-ouest", "bretagne-sud-atlantique", "transition-finistere-sud"}
assert zones["bretagne-nord-ouest"]["cross"] == "CROSS Corsen"
assert zones["bretagne-sud-atlantique"]["cross"] == "CROSS Etel"
assert zones["bretagne-sud-atlantique"]["official_extent"].startswith("Pointe de Penmarc'h")
assert zones["transition-finistere-sud"]["cross"] is None
assert zones["transition-finistere-sud"]["status"] == "etel_srr_start_at_penmarch_confirmed_vhf_overlap_pending"
weather_sites = {item["site"]: item for item in zones["bretagne-sud-atlantique"]["verified_weather_emitters"]}
assert set(weather_sites) == {"Penmarc'h", "Groix", "Belle-Ile", "Etel"}
assert weather_sites["Etel"]["channel"] == 63
assert maritime["channel_16"]["memory_strategy"] == "do_not_duplicate_same_frequency_only_to_label_cross"
assert maritime["channel_16"]["frequency_promoted"] is False
assert maritime["weather_and_safety"]["frequency_promoted"] is False
assert maritime["repeaters"]["maritime_remote_sites"]["status"] == "etel_weather_emitters_partial_inventory_corsen_inventory_required"
assert maritime["repeaters"]["amateur_repeaters"]["status"] == "inventory_required"
assert maritime["publication"]["public_export_allowed"] is False
assert maritime["publication"]["public_registry_allowed"] is False
assert maritime["publication"]["public_routes_allowed"] is False

assert emergency["status"] == "research_inventory_not_public"
assert {item["id"] for item in emergency["organisations"]} == {"ADRASEC-22", "ADRASEC-29", "ADRASEC-35", "ADRASEC-56"}
emergency_candidates = {item["id"]: item for item in emergency["candidates"]}
assert emergency_candidates["F1ZUG-4"]["frequency_mhz"] == 144.8000
assert emergency_candidates["F1ZUG-4"]["rx_pack_candidate"] is False
assert emergency_candidates["F5ZZC-4"]["frequency_mhz"] is None
assert emergency_candidates["F1ZBX"]["output_mhz"] == 145.6750
assert emergency_candidates["F1ZBX"]["rx_pack_candidate"] is True
assert emergency_candidates["F1ZBH"]["frequency_mhz"] == 144.8000
assert emergency_candidates["F1ZGQ"]["frequency_mhz"] == 144.8000
assert all(item["frequency_promoted_to_public_pack"] is False for item in emergency["candidates"])
assert emergency["rules"]["private_ppdr_operational_frequencies_excluded"] is True
assert emergency["rules"]["aprs_same_frequency_not_duplicated_by_site"] is True
assert emergency["rules"]["north_south_zoning_required"] is True
assert emergency["rules"]["public_export_allowed"] is False

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8").lower()
regions = (ROOT / "website/src/data/regions.json").read_text(encoding="utf-8").lower()
assert 'id: "bretagne"' not in registry
assert '"slug": "bretagne"' not in regions
assert not (ROOT / "website/src/pages/regions/bretagne.astro").exists()
assert not (ROOT / "website/public/downloads/bretagne").exists()
assert not (ROOT / "website/src/pages/downloads/bretagne").exists()

readme = (RESEARCH / "README.md").read_text(encoding="utf-8")
for expected in [
    "Bretagne Nord / Manche Ouest",
    "CROSS Corsen",
    "Bretagne Sud / Atlantique",
    "CROSS Etel",
    "zone de transition du Finistère Sud",
    "Pointe de Penmarc'h",
    "Penmarc'h — canal 80",
    "Étel — canal 63",
    "stations VHF déportées",
    "relais radioamateurs",
    "ne devra donc pas créer deux mémoires identiques",
]:
    assert expected in readme, f"Cadrage Bretagne absent: {expected}"

print("Tests RadioPack Bretagne maritime + emergency zoning: Penmarc'h interface + Etel weather emitters verified, Corsen inventory pending, ADRASEC inventory, 0 public side effects OK")
