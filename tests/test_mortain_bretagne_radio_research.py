import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

mortain_path = ROOT / "research/normandie-v0.4/mortain-bocage-coverage.json"
maritime_path = ROOT / "research/bretagne-v0.1/public-maritime-radio.json"
maritime_zones_path = ROOT / "research/bretagne-v0.1/maritime-zones.json"
bretagne_relays_path = ROOT / "research/bretagne-v0.1/emergency-relays.json"

for path in (mortain_path, maritime_path, maritime_zones_path, bretagne_relays_path):
    assert path.is_file(), f"Fichier de recherche manquant: {path.relative_to(ROOT)}"

mortain = json.loads(mortain_path.read_text(encoding="utf-8"))
assert mortain["status"] == "research_coverage_priorities_not_public"
assert mortain["focus"]["name"] == "Mortain-Bocage / Sud-Manche"
assert mortain["focus"]["departments_checked"] == [50, 35, 53, 61]
assert mortain["priority_tiers"]["tier_1_immediate"] == ["F6ZES", "F5ZHY"]
assert mortain["rules"]["sourdeval_must_not_be_guessed"] is True
assert mortain["rules"]["coverage_must_be_verified_before_publication"] is True
assert mortain["rules"]["digital_only_repeaters_do_not_consume_analog_memory"] is True
assert mortain["rules"]["national_aprs_frequency_not_duplicated_by_site"] is True
assert mortain["rules"]["published_normandie_v0_3_1_must_not_change"] is True
assert mortain["rules"]["public_export_allowed"] is False

stations = {item["id"]: item for item in mortain["stations"]}
assert stations["F6ZES"]["site"] == "Sourdeval"
assert stations["F6ZES"]["locator"] == "IN98MR93XV"
assert stations["F6ZES"]["altitude_m"] == 230
assert stations["F6ZES"]["responsible"] == "F1SMB"
assert stations["F6ZES"]["output_mhz"] is None
assert stations["F6ZES"]["mode"] is None
assert stations["F6ZES"]["rx_pack_candidate"] is False
assert "seconde source actuelle" in stations["F6ZES"]["blocking_reason"]

assert stations["F5ZHY"]["output_mhz"] == 145.6875
assert stations["F5ZHY"]["input_mhz"] == 145.0875
assert stations["F5ZHY"]["mode"] == "FM"
assert stations["F5ZHY"]["rx_pack_candidate"] is True
assert stations["F6ZCE"]["output_mhz"] == 145.7000
assert stations["F6ZCE"]["input_mhz"] == 145.1000
assert stations["F6ZCE"]["ctcss_hz"] == 123.0
assert stations["F6ZCE"]["rx_pack_candidate"] is True
assert stations["F1ZBX"]["output_mhz"] == 145.6750
assert stations["F1ZBX"]["input_mhz"] == 145.0750
assert stations["F1ZBX"]["ctcss_hz"] == 71.9
assert stations["F1ZBX"]["rx_pack_candidate"] is True
assert stations["F5ZIX"]["output_mhz"] == 144.8000
assert stations["F5ZIX"]["rx_pack_candidate"] is False
assert stations["F5ZPO"]["output_mhz"] == 144.8000
assert stations["F5ZPO"]["rx_pack_candidate"] is False
assert stations["F1ZKC"]["mode"] == "C4FM"
assert stations["F1ZKC"]["rx_pack_candidate"] is False
assert stations["F5ZTQ"]["current_directory_status"] == "stopped"
assert stations["F5ZTQ"]["rx_pack_candidate"] is False
assert all(item["frequency_promoted_to_public_pack"] is False for item in mortain["stations"])

maritime = json.loads(maritime_path.read_text(encoding="utf-8"))
assert maritime["schema_version"] == "1.3"
assert maritime["status"] == "official_channel_frequencies_and_etel_weather_emitters_verified_corsen_sites_pending"
channels = {item["channel"]: item for item in maritime["channels"]}
assert set(channels) == {16, 63, 64, 79, 80}
assert channels[16]["mode"] == "simplex"
assert channels[16]["rx_memory_mhz"] == 156.8000
assert channels[16]["memory_strategy"] == "reuse_single_common_channel_and_store_cross_as_zone_metadata"
assert channels[79]["coast_tx_ship_rx_mhz"] == 161.5750
assert channels[79]["rx_memory_mhz"] == 161.5750
assert channels[79]["historical_corsen_primary_status"] == "channel_79_weather_broadcast_documented_in_2003_requires_current_revalidation"
assert channels[79]["zone_assignment"] == "corsen_current_emitter_inventory_pending_etel_brittany_schedule_has_no_channel_79_site"
assert channels[80]["coast_tx_ship_rx_mhz"] == 161.6250
assert channels[80]["rx_memory_mhz"] == 161.6250
assert channels[80]["verified_etel_brittany_emitters"] == ["Penmarc'h", "Groix", "Belle-Ile"]
assert channels[63]["coast_tx_ship_rx_mhz"] == 160.7750
assert channels[63]["rx_memory_mhz"] == 160.7750
assert channels[63]["verified_etel_brittany_emitters"] == ["Etel"]
assert channels[64]["coast_tx_ship_rx_mhz"] == 160.8250
assert channels[64]["rx_memory_mhz"] == 160.8250
assert channels[64]["current_ministry_statement_revalidated_2026"] is True
assert channels[64]["zone_assignment"] == "current_brittany_transmitter_requires_primary_reconciliation"
assert all(item["frequency_promoted_to_public_pack"] is False for item in maritime["channels"])
assert maritime["rules"]["rx_only_uses_coast_transmit_frequency_on_duplex_channels"] is True
assert maritime["rules"]["channel_16_not_duplicated_by_cross_label"] is True
assert maritime["rules"]["weather_channels_require_site_and_coverage_validation_before_publication"] is True
assert maritime["rules"]["cross_remote_vhf_sites_must_be_primary_sourced"] is True
assert maritime["rules"]["historical_primary_radio_sites_must_be_revalidated_before_current_use"] is True
assert maritime["rules"]["etel_srr_starts_at_penmarch_primary_verified"] is True
assert maritime["rules"]["channel_64_requires_current_brittany_transmitter_reconciliation"] is True
assert maritime["rules"]["corsen_frehel_radio_infrastructure_primary_verified"] is True
assert maritime["rules"]["corsen_current_network_size_known_site_names_pending"] is True
assert maritime["rules"]["corsen_remote_vhf_sites_still_pending"] is True
assert maritime["rules"]["public_export_allowed"] is False
crosses = {item["cross"]: item for item in maritime["cross_zones"]}
assert set(crosses) == {"CROSS Corsen", "CROSS Etel"}
corsen = crosses["CROSS Corsen"]
assert corsen["current_network_summary"]["vhf_station_count"] == 10
assert corsen["current_network_summary"]["mf_station_count"] == 2
assert corsen["remote_vhf_sites"] == []
assert corsen["remote_vhf_sites_status"] == "official_current_site_inventory_pending"
corsen_infra = {item["site"]: item for item in corsen["verified_remote_radio_infrastructure_sites"]}
assert set(corsen_infra) == {"Cap Fréhel"}
assert corsen_infra["Cap Fréhel"]["role"] == "traffic_surveillance_and_vessel_liaison"
assert corsen_infra["Cap Fréhel"]["radio_service_or_channel"] is None
historical_sites = {item["site"]: item for item in corsen["historical_primary_radio_architecture"]}
assert set(historical_sites) == {"Stiff / Ouessant", "Pointe du Raz", "Corsen"}
assert all(item["current_validation"] is False for item in historical_sites.values())
assert corsen["historical_channel_79_context"]["status"] == "primary_2003_weather_and_information_broadcast_requires_current_revalidation"
assert crosses["CROSS Etel"]["official_srr_extent"].startswith("Pointe de Penmarc'h")
etel_sites = {item["site"]: item for item in crosses["CROSS Etel"]["remote_vhf_sites"]}
assert set(etel_sites) == {"Penmarc'h", "Groix", "Belle-Ile", "Etel"}
assert etel_sites["Penmarc'h"]["channel"] == 80
assert etel_sites["Groix"]["channel"] == 80
assert etel_sites["Belle-Ile"]["channel"] == 80
assert etel_sites["Etel"]["channel"] == 63
assert etel_sites["Etel"]["broadcast"] == "continuous_coastal_weather"
assert crosses["CROSS Etel"]["remote_vhf_sites_status"] == "official_weather_emitter_inventory_partially_verified"

zones_data = json.loads(maritime_zones_path.read_text(encoding="utf-8"))
assert zones_data["schema_version"] == "1.2"
assert zones_data["status"] == "research_zoning_penmarch_interface_confirmed_vhf_overlap_pending"
assert zones_data["rules"]["etel_srr_starts_at_pointe_de_penmarch_primary_sourced"] is True
assert zones_data["rules"]["corsen_frehel_radio_infrastructure_primary_sourced"] is True
assert zones_data["rules"]["corsen_detailed_srr_and_vhf_overlap_still_pending"] is True
zones = {item["id"]: item for item in zones_data["zones"]}
assert zones["bretagne-sud-atlantique"]["official_extent"].startswith("Pointe de Penmarc'h")
assert zones["transition-finistere-sud"]["status"] == "etel_srr_start_at_penmarch_confirmed_vhf_overlap_pending"
north_infra = {item["site"]: item for item in zones["bretagne-nord-ouest"]["verified_remote_radio_infrastructure_sites"]}
assert set(north_infra) == {"Cap Fréhel"}
assert north_infra["Cap Fréhel"]["radio_service_or_channel"] is None
weather_emitters = {item["site"]: item for item in zones["bretagne-sud-atlantique"]["verified_weather_emitters"]}
assert set(weather_emitters) == {"Penmarc'h", "Groix", "Belle-Ile", "Etel"}
assert weather_emitters["Etel"]["channel"] == 63
assert zones_data["publication"]["public_export_allowed"] is False

bretagne = json.loads(bretagne_relays_path.read_text(encoding="utf-8"))
assert bretagne["schema_version"] == "1.3"
relays = {item["id"]: item for item in bretagne["candidates"]}
assert relays["F1ZUG-4"]["frequency_mhz"] == 144.8000
assert relays["F1ZUG-4"]["adrasec_transponder_frequency_mhz"] is None
assert relays["F1ZUG-4"]["adrasec_transponder_role_status"] == "public_ara35_2024_role_documented_frequency_unpublished"
assert relays["F5ZEB"]["site"] == "Rennes (Est)"
assert relays["F5ZEB"]["output_mhz"] == 438.6750
assert relays["F5ZEB"]["input_mhz"] == 431.0750
assert relays["F5ZEB"]["rx_pack_candidate"] is False
assert relays["F5ZPV"]["output_mhz"] == 439.8750
assert relays["F5ZPV"]["status"] == "temporarily_stopped_current_ara35_page"
assert relays["F5ZPV"]["rx_pack_candidate"] is False
assert relays["F5ZIS"]["site"] == "Matignon"
assert relays["F5ZIS"]["output_mhz"] == 145.2375
assert relays["F5ZIS"]["paired_mhz"] == 432.6500
assert relays["F5ZIS"]["ctcss_hz"] == 71.9
assert relays["F5ZIT"]["site"] == "Perros-Guirec"
assert relays["F5ZIT"]["output_mhz"] == 145.2250
assert relays["F5ZIT"]["paired_mhz"] == 432.6500
for relay_id, output_mhz in {"F1ZGS": 431.4250, "F5ZDV": 438.7000, "F5ZZL": 431.3750}.items():
    assert relays[relay_id]["department"] == 29
    assert relays[relay_id]["output_mhz"] == output_mhz
    assert relays[relay_id]["input_mhz"] == 145.2625
    assert relays[relay_id]["ctcss_hz"] == 71.9
    assert relays[relay_id]["mode"] == "FM"
    assert relays[relay_id]["rx_pack_candidate"] is True
assert relays["F1ZAJ"]["site"] == "Plouray"
assert relays["F1ZAJ"]["frequency_mhz"] == 144.8000
assert relays["F1ZAJ"]["rx_pack_candidate"] is False
assert relays["F1ZBZ"]["site"] == "Lorient"
assert relays["F1ZBZ"]["output_mhz"] == 431.2000
assert relays["F1ZBZ"]["rx_pack_candidate"] is False
assert relays["F5ZPE"]["site"] == "Bignan"
assert relays["F5ZPE"]["output_mhz"] == 145.7375
assert relays["F5ZPE"]["input_mhz"] == 145.1375
assert relays["F5ZPE"]["ctcss_hz"] == 71.9
assert relays["F5ZPE"]["rx_pack_candidate"] is True
assert bretagne["rules"]["adrasec_transponder_frequency_must_not_be_inferred_from_aprs_frequency"] is True
assert bretagne["rules"]["temporarily_stopped_repeaters_not_active_candidates"] is True
assert bretagne["rules"]["aprs_same_frequency_not_duplicated_by_site"] is True
assert bretagne["rules"]["adrasec_role_must_not_be_inferred_from_geography_only"] is True
assert bretagne["rules"]["public_export_allowed"] is False
assert all(item["frequency_promoted_to_public_pack"] is False for item in bretagne["candidates"])

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'id: "bretagne"' not in registry
assert 'version: "v0.4"' not in registry
assert 'version: "v0.3"' not in registry
assert not (ROOT / "website/src/pages/downloads/bretagne").exists()
assert not (ROOT / "website/src/pages/downloads/normandie/radiopack-france-normandie-v0.4.csv.ts").exists()
assert not (ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv.ts").exists()

print("Tests RadioPack Sprint 29 Mortain + Bretagne radio research: Sourdeval unresolved safely, Etel emitters primary-verified, Corsen current network 10 VHF + 2 MF with site list pending, Cap Frehel primary-verified, historical Stiff/Pointe du Raz/Corsen leads kept non-current, channel 64 current ministry statement revalidated but transmitter unresolved, ADRASEC35 role split, Finistere analog candidates, APRS metadata only, 0 public mutations OK")
