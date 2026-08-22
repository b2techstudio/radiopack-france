#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
pass1 = json.loads((ROOT / "research/sprint-103-inland-vhf-audit.json").read_text(encoding="utf-8"))
pass2 = json.loads((ROOT / "research/sprint-103-inland-vhf-audit-pass2.json").read_text(encoding="utf-8"))

assert pass1["status"] == "national_inland_vhf_audit_pass1"
assert pass2["status"] == "rf_delta_pass2_closed_non_exhaustive"
assert pass2["public_mutation_performed"] is False

results = {item["pack"]: item for item in pass2["results"]}
expected_packs = {
    "Grand Est", "Île-de-France", "Bourgogne-Franche-Comté", "Auvergne-Rhône-Alpes",
    "Centre-Val de Loire", "Normandie", "Bretagne", "Hauts-de-France",
    "Pays de la Loire", "Nouvelle-Aquitaine", "Occitanie",
    "Provence-Alpes-Côte d’Azur", "Corse", "Annecy–Alpes–Léman",
}
assert set(results) == expected_packs

assert results["Grand Est"]["new_rf_count"] == 13
assert results["Île-de-France"]["minimum_new_rf_count"] == 1
assert results["Bourgogne-Franche-Comté"]["minimum_new_rf_count"] == 7
assert results["Auvergne-Rhône-Alpes"]["minimum_new_rf_count"] == 9
assert results["Centre-Val de Loire"]["minimum_new_rf_count"] == 0

for coastal in [
    "Normandie", "Bretagne", "Hauts-de-France", "Pays de la Loire",
    "Nouvelle-Aquitaine", "Occitanie", "Provence-Alpes-Côte d’Azur", "Corse",
]:
    assert results[coastal]["new_rf_count"] == 0

queue = pass2["actionable_non_coastal_queue"]
assert [(item["pack"], item["verified_minimum_new_rf"]) for item in queue] == [
    ("Grand Est", 13),
    ("Île-de-France", 1),
    ("Bourgogne-Franche-Comté", 7),
    ("Auvergne-Rhône-Alpes", 9),
]

print("Sprint 103 inland VHF audit: 14 packs classified; coastal RF dedup policy and non-coastal queue OK")
