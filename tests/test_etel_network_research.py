import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research/bretagne-v0.1/etel-network.json"

assert PATH.is_file(), "Fichier de recherche CROSS Etel manquant"

data = json.loads(PATH.read_text(encoding="utf-8"))
assert data["schema_version"] == "1.0"
assert data["status"] == "current_network_size_verified_site_inventory_pending"
assert data["cross"] == "CROSS Etel"
assert data["official_srr_extent"].startswith("Pointe de Penmarc'h")

network = data["current_radio_network"]
assert network["station_count"] == 17
assert network["maintenance_extent"] == "Pointe de Penmarc'h aux Pyrénées-Atlantiques (Biarritz)"
assert network["maintained_by"] == "service technique du CROSS Etel"
assert network["status"] == "primary_current_2026_network_size_verified_station_names_pending"

sites = {item["site"]: item for item in data["known_weather_sites"]}
assert set(sites) == {"Penmarc'h", "Groix", "Belle-Ile", "Etel", "Chassiron"}
assert sites["Penmarc'h"]["channel"] == 80
assert sites["Groix"]["channel"] == 80
assert sites["Belle-Ile"]["channel"] == 80
assert sites["Etel"]["channel"] == 63
assert sites["Chassiron"]["channel"] == 63
assert "outside_brittany" in sites["Chassiron"]["status"]

ch64 = data["channel_64_research"]
assert ch64["local_primary_site_identified"] is False
assert ch64["candidate_station_name"] is None
assert ch64["status"] == "current_network_context_strengthened_transmitter_still_unidentified"

rules = data["rules"]
assert rules["station_count_does_not_imply_station_names"] is True
assert rules["known_weather_sites_are_not_complete_network_inventory"] is True
assert rules["network_extent_does_not_imply_channel_assignment"] is True
assert rules["channel_64_site_must_not_be_guessed"] is True
assert rules["paired_rx_policy_applies_after_channel_validation"] is True
assert rules["frequency_promoted_to_public_pack"] is False
assert rules["public_export_allowed"] is False

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'id: "bretagne"' not in registry

print("Tests CROSS Etel network research: 17 current radio stations Penmarch-to-Biarritz verified, known weather sites remain partial inventory, channel 64 transmitter unresolved, 0 public promotion OK")
