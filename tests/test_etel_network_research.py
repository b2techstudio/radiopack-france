import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research/bretagne-v0.1/etel-network.json"
EVIDENCE = ROOT / "research/bretagne-v0.1/etel-channel64-evidence.json"

assert PATH.is_file(), "Fichier de recherche CROSS Etel manquant"
assert EVIDENCE.is_file(), "Dossier de preuve canal 64 manquant"

data = json.loads(PATH.read_text(encoding="utf-8"))
evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
assert data["schema_version"] == "1.1"
assert data["status"] == "current_network_dimensions_verified_channel64_primary_conflict_documented"
assert data["cross"] == "CROSS Etel"
assert data["official_srr_extent"].startswith("Pointe de Penmarc'h")
assert data["channel64_evidence_file"] == "research/bretagne-v0.1/etel-channel64-evidence.json"

network = data["current_radio_network"]
assert network["maintenance_station_count_2026"] == 17
assert network["annual_report_2025_vhf_station_count"] == 16
assert network["annual_report_2025_mf_station_count"] == 2
assert network["maintenance_extent"] == "Pointe de Penmarc'h aux Pyrénées-Atlantiques (Biarritz)"
assert network["maintained_by"] == "service technique du CROSS Etel"
assert network["status"] == "primary_current_network_dimensions_verified_counting_units_not_reconciled"

source_statuses = {item["status"] for item in data["primary_sources"]}
assert "primary_current_2026_morbihan_channels_63_64_statement" in source_statuses
assert "primary_current_16_vhf_2_mf_and_weather_emitter_inventory" in source_statuses
assert "primary_current_linked_weather_schedule_no_channel64_site" in source_statuses

sites = {item["site"]: item for item in data["known_weather_sites"]}
assert set(sites) == {"Penmarc'h", "Groix", "Belle-Ile", "Etel", "Chassiron"}
assert sites["Penmarc'h"]["channel"] == 80
assert sites["Groix"]["channel"] == 80
assert sites["Belle-Ile"]["channel"] == 80
assert sites["Etel"]["channel"] == 63
assert sites["Chassiron"]["channel"] == 63
assert "outside_brittany" in sites["Chassiron"]["status"]

ch64 = data["channel_64_research"]
assert ch64["ministry_page_updated"] == "2026-06-19"
assert ch64["ministry_statement_rechecked"] == "2026-08-10"
assert ch64["current_cross_etel_html_names_etel_continuous_channel_63"] is True
assert ch64["current_cross_etel_schedule_mentions_channel64"] is False
assert ch64["annual_report_2025_mentions_channel64"] is False
assert ch64["annual_report_2025_names_etel_as_reinforced_channel63_emitter"] is True
assert ch64["current_cross_etel_html_names_brittany_channel_64_site"] is False
assert ch64["local_primary_site_identified"] is False
assert ch64["candidate_station_name"] is None
assert ch64["primary_source_conflict_open"] is True
assert ch64["status"] == "primary_current_ministry_regional_ch64_statement_conflicts_with_local_cross_documents_omitting_ch64_site_unresolved"

assert evidence["schema_version"] == "1.0"
assert evidence["status"] == "primary_current_channel64_conflict_documented_site_unresolved"
assert evidence["paired_rx"]["ship_to_coast_mhz"] == 156.225
assert evidence["paired_rx"]["coast_to_ship_mhz"] == 160.825
assert evidence["paired_rx"]["new_rf_memory_delta"] == 0
assert evidence["assessment"]["primary_current_regional_channel64_statement_exists"] is True
assert evidence["assessment"]["primary_current_local_cross_channel64_site_exists"] is False
assert evidence["assessment"]["primary_current_local_cross_documents_mention_channel64"] is False
assert evidence["assessment"]["channel64_site_confirmed"] is False
assert evidence["assessment"]["candidate_station_name"] is None
assert evidence["assessment"]["site_assignment_can_be_promoted"] is False
assert evidence["network_count_note"]["must_not_be_arithmetically_reconciled_without_source_definition"] is True

rules = data["rules"]
assert rules["station_count_does_not_imply_station_names"] is True
assert rules["network_counting_units_must_not_be_reconciled_without_definition"] is True
assert rules["known_weather_sites_are_not_complete_network_inventory"] is True
assert rules["network_extent_does_not_imply_channel_assignment"] is True
assert rules["absence_from_current_local_documents_is_not_negative_operational_evidence"] is True
assert rules["primary_source_conflict_requires_reconciliation"] is True
assert rules["ministry_regional_channel_statement_does_not_identify_transmitter_site"] is True
assert rules["channel_64_site_must_not_be_guessed"] is True
assert rules["paired_rx_policy_applies_after_channel_validation"] is True
assert rules["frequency_promoted_to_public_pack"] is False
assert rules["public_export_allowed"] is False

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'id: "bretagne"' not in registry

print("Tests CROSS Etel network research: 2026 maintenance view 17 stations and 2025 annual report 16 VHF + 2 MF kept as distinct counting dimensions; current ministry 63/64 Morbihan statement now explicitly conflicts with local CROSS page/schedule/annual-report evidence naming channel 63 but no channel 64 site, 0 public promotion OK")
