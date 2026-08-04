import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research/annecy-alpes-leman-v0.2"

france_path = RESEARCH / "radioamateur-france-inventory.json"
switzerland_path = RESEARCH / "radioamateur-switzerland-candidates.json"
conflicts_path = RESEARCH / "conflicts.csv"

for path in [france_path, switzerland_path, conflicts_path]:
    assert path.is_file(), f"Fichier de recherche manquant: {path.relative_to(ROOT)}"

france = json.loads(france_path.read_text(encoding="utf-8"))
switzerland = json.loads(switzerland_path.read_text(encoding="utf-8"))

assert france["production_ready"] is False
assert switzerland["production_ready"] is False
assert france["default_export_policy"] == "rx_only"
assert switzerland["default_export_policy"] == "rx_only"

fr_channels = france["channels"]
assert len(fr_channels) == 19, f"Inventaire France inattendu: {len(fr_channels)} fréquences"

fr_names = [channel["name"] for channel in fr_channels]
fr_frequencies = [float(channel["frequency_mhz"]) for channel in fr_channels]
assert len(fr_names) == len(set(fr_names)), "Noms dupliqués dans l'inventaire France"
assert len(fr_frequencies) == len(set(fr_frequencies)), "Fréquences non fusionnées dans l'inventaire France"

for channel in fr_channels:
    assert len(channel["name"]) <= 10, f"Nom trop long: {channel['name']}"
    assert channel["mode"] == "NFM"
    assert channel["tx_policy"] == "rx_only"
    assert channel["verification"] in {"verified", "verified_merged"}
    assert channel["source_ids"], f"Source absente: {channel['name']}"
    assert "F1ZJV" not in channel.get("callsigns", []), "F1ZJV ne doit pas passer en production"

expected_merged = {
    432.65: {"F5ZDT", "F5ZLV"},
    432.55: {"F1ZFX", "F1ZIC"},
    145.2875: {"F1ZJQ", "F1ZHG"},
    432.5125: {"F1ZHE", "F1ZHG", "F5ZGT"},
}
for frequency, callsigns in expected_merged.items():
    channel = next(item for item in fr_channels if float(item["frequency_mhz"]) == frequency)
    assert set(channel["callsigns"]) == callsigns, f"Fusion incorrecte sur {frequency} MHz"

ch_channels = switzerland["channels"]
assert len(ch_channels) == 8
assert len({channel["name"] for channel in ch_channels}) == len(ch_channels)
assert len({float(channel["frequency_mhz"]) for channel in ch_channels}) == len(ch_channels)

allowed_ch_statuses = {
    "verified_current",
    "current_use_needs_owner_crosscheck",
    "pending_recheck",
}
for channel in ch_channels:
    assert len(channel["name"]) <= 10, f"Nom suisse trop long: {channel['name']}"
    assert channel["mode"] == "NFM"
    assert channel["tx_policy"] == "rx_only"
    assert channel["verification"] in allowed_ch_statuses
    assert channel["source_ids"], f"Source suisse absente: {channel['name']}"

verified_swiss = [channel for channel in ch_channels if channel["verification"] == "verified_current"]
assert {channel["name"] for channel in verified_swiss} == {"CH-HB9G-V", "CH-HB9G-U"}

with conflicts_path.open(encoding="utf-8", newline="") as handle:
    conflicts = list(csv.DictReader(handle))

f1zjv = next(row for row in conflicts if row["item"] == "F1ZJV")
assert f1zjv["status"] == "open"
assert "Exclure" in f1zjv["production_action"]

print("Tests Annecy–Alpes–Léman research: OK")
