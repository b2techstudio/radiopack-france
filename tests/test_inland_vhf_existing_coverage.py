#!/usr/bin/env python3
"""Verify coastal packs already RF-cover the national VHF plan.

Normandie and Bretagne are stored as static public CSVs. The other six coastal
metropolitan v0.2 packs are generated at site build time from
`metropolitanPack.ts`; for those, verify `includeMarine: true` and the generator
contract that injects the complete national marine VHF dataset.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STATIC_COASTAL_PACKS = {
    "normandie": "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv",
    "bretagne": "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv",
}

GENERATED_COASTAL_PACKS = [
    "hauts-de-france",
    "pays-de-la-loire",
    "nouvelle-aquitaine",
    "occitanie",
    "provence-alpes-cote-d-azur",
    "corse",
]

marine = json.loads((ROOT / "data/national/marine-vhf-rx.json").read_text(encoding="utf-8"))
marine_rf = {f"{float(channel['frequency_mhz']):.6f}" for channel in marine["channels"]}
assert marine_rf, "National marine VHF dataset is empty"

inland_core_rf = {
    "156.300000",  # 06
    "156.400000",  # 08
    "156.475000",  # 69
    "156.500000",  # 10
    "156.550000",  # 11
    "156.600000",  # 12
    "156.625000",  # 72
    "156.650000",  # 13
    "156.700000",  # 14
    "156.875000",  # 77
    "156.900000", "161.500000",  # 18 paired plan
    "156.950000", "161.550000",  # 19 paired plan
    "157.000000", "161.600000",  # 20 paired plan
    "157.100000", "161.700000",  # 22 paired plan
    "157.125000", "161.725000",  # 82 paired plan
}
assert inland_core_rf <= marine_rf

# Static legacy packs: prove the frequencies are already physically present.
for pack, relative in STATIC_COASTAL_PACKS.items():
    path = ROOT / relative
    assert path.is_file(), f"Missing static public coastal pack: {pack} -> {relative}"
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    frequencies = {row["Frequency"] for row in rows}
    missing_marine = marine_rf - frequencies
    assert not missing_marine, f"{pack} is missing national marine VHF RF: {sorted(missing_marine)}"
    assert inland_core_rf <= frequencies

# Generated metropolitan packs: prove the source definition enables the same
# complete marine dataset and that the generator actually injects that dataset.
metropolitan_source = (ROOT / "website/src/lib/metropolitanPack.ts").read_text(encoding="utf-8")
definitions_start = metropolitan_source.index("export const metropolitanPackDefinitions")
definitions = metropolitan_source[definitions_start:]

assert 'loadChannels("data/national/marine-vhf-rx.json")' in metropolitan_source
assert "definition.includeMarine" in metropolitan_source

for pack in GENERATED_COASTAL_PACKS:
    marker = f'id: "{pack}"'
    start = definitions.index(marker)
    window = definitions[start:start + 550]
    assert 'version: "v0.2"' in window, f"{pack}: current generated definition is not v0.2"
    assert "includeMarine: true" in window, f"{pack}: marine block is not enabled"

print(
    "Coastal VHF coverage: Normandie/Bretagne physically contain the full marine RF set; "
    "6 generated coastal v0.2 packs enable the same complete marine dataset. "
    "Shared inland assignments require no duplicate RF memories."
)
