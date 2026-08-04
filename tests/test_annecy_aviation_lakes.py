import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research/annecy-alpes-leman-v0.2"

aviation_path = RESEARCH / "aviation-france-pre-airac-08.json"
navigation_path = RESEARCH / "navigation-lakes-findings.json"

for path in [aviation_path, navigation_path]:
    assert path.is_file(), f"Fichier de recherche manquant: {path.relative_to(ROOT)}"
    assert path.stat().st_size > 100, f"Fichier incomplet: {path.relative_to(ROOT)}"

aviation = json.loads(aviation_path.read_text(encoding="utf-8"))
navigation = json.loads(navigation_path.read_text(encoding="utf-8"))

assert aviation["production_ready"] is False
assert navigation["production_ready"] is False
assert aviation["default_export_policy"] == "rx_only"
assert navigation["default_export_policy"] == "rx_only"

cycle = aviation["cycle"]
assert cycle["source_cycle"] == "AIRAC 07/26"
assert cycle["valid_until_inclusive"] == "2026-08-05"
assert cycle["mandatory_recheck_from"] == "2026-08-06"
assert cycle["next_cycle"] == "AIRAC 08/26"

channels = aviation["channels"]
assert len(channels) == 11, f"Pré-inventaire aviation inattendu: {len(channels)}"
assert len({channel["name"] for channel in channels}) == len(channels)
assert len({float(channel["frequency_mhz"]) for channel in channels}) == len(channels)

for channel in channels:
    assert len(channel["name"]) <= 10, f"Nom aviation trop long: {channel['name']}"
    assert channel["mode"] == "AM"
    assert float(channel["step_khz"]) == 8.33
    assert channel["tx_policy"] == "rx_only"
    assert channel["verification"] == "pre_airac_recheck"
    assert channel["source_ids"], f"Source aviation absente: {channel['name']}"

expected = {
    "ANNCY-TWR": 118.2,
    "ANNMS-A-A": 125.875,
    "CHAM-INFO": 123.7,
    "CHAM-APP": 121.205,
    "CHAM-TWR": 118.3,
    "CHAM-ATIS": 127.1,
    "VERSD-A-A": 121.0,
    "GREN-GND": 121.93,
    "GREN-TWR": 119.3,
    "GREN-ATIS": 133.855,
    "GENEV-INFO": 126.35,
}
assert {channel["name"]: float(channel["frequency_mhz"]) for channel in channels} == expected

assert navigation["channels"] == [], "Aucune fréquence lacustre ne doit être publiée à ce stade"

conditional = navigation["conditional_candidates"]
assert len(conditional) == 1
channel16 = conditional[0]
assert channel16["name"] == "CH-LAC16"
assert float(channel16["frequency_mhz"]) == 156.8
assert channel16["status"] == "licensed_radar_context_not_public_pack"

excluded_frequencies = {
    float(item["frequency_mhz"])
    for item in navigation["excluded"]
    if "frequency_mhz" in item
}
assert excluded_frequencies == {161.975, 162.025}
assert not excluded_frequencies.intersection(
    {float(channel["frequency_mhz"]) for channel in navigation["channels"]}
)

lake_statuses = {item["lake"]: item["status"] for item in navigation["lake_reviews"]}
assert lake_statuses["Léman"] == "no_public_general_channel_validated"
assert lake_statuses["Annecy"] == "official_navigation_rules_reviewed_no_radio_channel_identified"
assert lake_statuses["Bourget"] == "official_navigation_rules_reviewed_no_radio_channel_identified"
assert lake_statuses["Aiguebelette"] == "official_navigation_radio_source_pending"

print("Tests Annecy–Alpes–Léman aviation/lakes research: OK")
