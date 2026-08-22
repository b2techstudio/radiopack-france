#!/usr/bin/env python3
"""Verify that coastal public packs already RF-cover the national VHF plan.

Inland and maritime uses can share the same RF. A coastal pack that already
contains the full national marine VHF RX dataset must not receive duplicate
memories merely because a channel also has an inland-navigation assignment.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CURRENT_COASTAL_PACKS = {
    "normandie": "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv",
    "bretagne": "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv",
    "hauts-de-france": "website/public/downloads/hauts-de-france/radiopack-france-hauts-de-france-v0.2.csv",
    "pays-de-la-loire": "website/public/downloads/pays-de-la-loire/radiopack-france-pays-de-la-loire-v0.2.csv",
    "nouvelle-aquitaine": "website/public/downloads/nouvelle-aquitaine/radiopack-france-nouvelle-aquitaine-v0.2.csv",
    "occitanie": "website/public/downloads/occitanie/radiopack-france-occitanie-v0.2.csv",
    "provence-alpes-cote-d-azur": "website/public/downloads/provence-alpes-cote-d-azur/radiopack-france-provence-alpes-cote-d-azur-v0.2.csv",
    "corse": "website/public/downloads/corse/radiopack-france-corse-v0.2.csv",
}

marine = json.loads((ROOT / "data/national/marine-vhf-rx.json").read_text(encoding="utf-8"))
marine_rf = {f"{float(channel['frequency_mhz']):.6f}" for channel in marine["channels"]}
assert marine_rf, "National marine VHF dataset is empty"

# Frequencies known to be useful in inland navigation and expected to be part
# of the international VHF plan. This catches accidental regressions clearly.
inland_core_rf = {
    "156.300000",  # 06
    "156.400000",  # 08
    "156.500000",  # 10
    "156.550000",  # 11
    "156.600000",  # 12
    "156.625000",  # 72
    "156.650000",  # 13
    "156.700000",  # 14
    "156.875000",  # 77
    "156.900000", "161.500000",  # 18 paired RX
    "156.950000", "161.550000",  # 19 paired RX
    "157.000000", "161.600000",  # 20 paired RX
    "157.100000", "161.700000",  # 22 paired RX
}
assert inland_core_rf <= marine_rf

for pack, relative in CURRENT_COASTAL_PACKS.items():
    path = ROOT / relative
    assert path.is_file(), f"Missing public coastal pack: {pack} -> {relative}"
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    frequencies = {row["Frequency"] for row in rows}
    missing_marine = marine_rf - frequencies
    assert not missing_marine, f"{pack} is missing national marine VHF RF: {sorted(missing_marine)}"
    assert inland_core_rf <= frequencies, f"{pack} is missing inland-core RF already expected from marine block"

print(
    "Coastal VHF coverage: 8 public packs contain the full national marine VHF RF dataset; "
    "shared inland assignments require provenance updates, not duplicate RF memories"
)
