import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AVIATION = ROOT / "research/bretagne-v0.2/aviation-airac-08.json"
DELTA = ROOT / "research/bretagne-v0.2/candidate-memory-delta.json"
V02_BUILDER = ROOT / "tools/build_bretagne_v02_internal_candidate.py"
V01_BUILDER = ROOT / "tools/build_bretagne_internal_candidate.py"
PUBLIC_V01 = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.1.csv"
PUBLIC_V02 = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"
REGISTRY = ROOT / "website/src/lib/packRegistry.ts"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


aviation = json.loads(AVIATION.read_text(encoding="utf-8"))
delta = json.loads(DELTA.read_text(encoding="utf-8"))
assert aviation["status"] == "verified_for_internal_candidate_not_public"
assert aviation["cycle"]["validation_cycle"] == "AIRAC 08/26"
assert aviation["cycle"]["effective_from"] == "2026-08-06"
assert aviation["cycle"]["effective_until_inclusive"] == "2026-09-02"
assert aviation["cycle"]["current_product_verified"] is True
assert aviation["cycle"]["current_xml_export_bytes_extracted_in_repository_workflow"] is False
assert aviation["methodology"]["latest_effective_public_aip_page_may_predate_cycle_start"] is True
assert aviation["methodology"]["does_not_claim_current_xml_field_match_without_xml_extraction"] is True
assert aviation["methodology"]["public_export_allowed"] is False
assert aviation["selection"]["scoped_airfields"] == ["LFRN", "LFRB", "LFRD", "LFRQ"]
assert aviation["selection"]["airfield_unique_memory_count"] == 15
assert aviation["selection"]["generic_emergency_memory_count"] == 1
assert aviation["selection"]["total_memory_count"] == 16
assert aviation["selection"]["candidate_locations_used"] == [130, 145]
assert aviation["selection"]["unused_reserved_locations"] == [146, 149]
assert aviation["selection"]["no_artificial_fill"] is True
assert len(aviation["channels"]) == 16
assert all(c["tx_policy"] == "rx_only" for c in aviation["channels"])
assert all(c["mode"] == "AM" for c in aviation["channels"])
assert all(c["step_khz"] == 8.33 for c in aviation["channels"])
assert all(c["verification"] == "verified_airac08_latest_effective_public" for c in aviation["channels"])
assert len({round(float(c["frequency_mhz"]), 6) for c in aviation["channels"]}) == 16
assert len({c["name"] for c in aviation["channels"]}) == 16
assert all(len(c["name"]) <= 10 for c in aviation["channels"])

expected = {
    "AIR-EMERG": 121.500,
    "RNS-COT-A": 120.350,
    "RNS-NORD": 126.950,
    "RNS-SUD": 134.000,
    "RNS-COT-B": 134.200,
    "RNS-GND": 121.730,
    "RNS-TWR": 120.505,
    "RNS-ATIS": 136.405,
    "BES-IRO1": 119.575,
    "BES-IRO2": 135.830,
    "BES-APP": 125.860,
    "BES-TWR": 120.105,
    "BES-ATIS": 129.355,
    "DIN-TWR": 120.155,
    "DIN-ATIS": 124.580,
    "QUIM-TWR": 118.625,
}
assert {c["name"]: round(float(c["frequency_mhz"]), 6) for c in aviation["channels"]} == expected

assert delta["base"] == {"published_version": "0.1", "memory_count": 135, "immutable": True}
assert delta["delta"]["aviation_airac08_memory_count"] == 16
assert delta["delta"]["other_new_memory_count"] == 0
assert delta["delta"]["total_new_memory_count"] == 16
assert delta["delta"]["candidate_memory_count"] == 151
assert delta["rules"]["published_v0_1_must_not_be_modified"] is True
assert delta["rules"]["candidate_must_reproduce_v0_1_base_exactly"] is True
assert delta["rules"]["no_artificial_fill"] is True
assert delta["rules"]["public_pack_mutation_allowed"] is False

v01 = load_module("bretagne_v01", V01_BUILDER)
v02 = load_module("bretagne_v02", V02_BUILDER)
base = v01.build_candidate(ROOT)
candidate = v02.build_candidate(ROOT)
assert base["memory_count"] == 135
assert candidate["target_version"] == "0.2"
assert candidate["status"] == "internal_candidate_not_for_publication"
assert candidate["public_export_allowed"] is False
assert candidate["published_base_version"] == "0.1"
assert candidate["published_base_memory_count"] == 135
assert candidate["memory_count"] == 151
assert candidate["new_memory_count"] == 16
assert candidate["aviation_memory_count"] == 16
assert candidate["aviation_cycle"] == "AIRAC 08/26"
assert candidate["rules"]["published_v0_1_immutable"] is True
assert candidate["rules"]["no_artificial_fill"] is True
assert candidate["rules"]["public_pack_mutation_allowed"] is False

base_by_location = {int(item["location"]): item["channel"] for item in base["memories"]}
candidate_by_location = {int(item["location"]): item["channel"] for item in candidate["memories"]}
for location, channel in base_by_location.items():
    assert candidate_by_location[location] == channel
for location in range(130, 146):
    assert location in candidate_by_location
    assert candidate_by_location[location]["candidate_block"] == "Aviation Bretagne AIRAC 08/26"
for location in range(146, 150):
    assert location not in candidate_by_location

locations = [int(item["location"]) for item in candidate["memories"]]
names = [item["channel"]["name"] for item in candidate["memories"]]
frequencies = [round(float(item["channel"]["frequency_mhz"]), 6) for item in candidate["memories"]]
assert len(locations) == len(set(locations)) == 151
assert len(names) == len(set(names)) == 151
assert len(frequencies) == len(set(frequencies)) == 151

with tempfile.TemporaryDirectory(prefix="radiopack-bretagne-v02-") as td:
    subprocess.run(
        [sys.executable, str(V02_BUILDER), "--root", str(ROOT), "--output-dir", td],
        check=True,
    )
    csv_path = Path(td) / "bretagne-v0.2-internal.csv"
    json_path = Path(td) / "bretagne-v0.2-internal.json"
    assert csv_path.is_file() and json_path.is_file()
    with csv_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 151
    assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
    aviation_rows = [row for row in rows if 130 <= int(row["Location"]) <= 145]
    assert len(aviation_rows) == 16
    assert all(row["Mode"] == "AM" and row["TStep"] == "8.33" for row in aviation_rows)

assert PUBLIC_V01.is_file()
assert not PUBLIC_V02.exists()
registry = REGISTRY.read_text(encoding="utf-8")
assert '/downloads/bretagne/radiopack-france-bretagne-v0.1.csv' in registry
assert '/downloads/bretagne/radiopack-france-bretagne-v0.2.csv' not in registry

print("Sprint 75 Bretagne aviation: AIRAC 08/26 internal candidate adds 16 RX-only AM memories at 130-145, base v0.1 remains immutable, total 151, public untouched OK")
