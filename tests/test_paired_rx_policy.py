import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

policy = json.loads((ROOT / "research/paired-rx-policy.json").read_text(encoding="utf-8"))
next_plan = json.loads((ROOT / "research/paired-rx-next-version-plan.json").read_text(encoding="utf-8"))
emergency_policy = json.loads((ROOT / "research/emergency-radio-policy.json").read_text(encoding="utf-8"))
normandie_plan = json.loads((ROOT / "research/normandie-v0.4/pack-plan.json").read_text(encoding="utf-8"))
annecy_plan = json.loads((ROOT / "research/annecy-alpes-leman-v0.3/pack-plan.json").read_text(encoding="utf-8"))
bretagne_plan = json.loads((ROOT / "research/bretagne-v0.1/pack-plan.json").read_text(encoding="utf-8"))
bretagne_maritime = json.loads((ROOT / "research/bretagne-v0.1/public-maritime-radio.json").read_text(encoding="utf-8"))

assert policy["status"] == "active_project_policy"
assert policy["core_rule"]["native_duplex_or_split_pair_exports_both_rx_frequencies"] is True
assert policy["core_rule"]["implementation"] == "two_rx_only_memories_when_frequencies_differ"
assert policy["core_rule"]["tx_disabled"] is True
assert policy["core_rule"]["chirp_duplex"] == "off"
assert policy["core_rule"]["chirp_offset"] == "0.000000"
assert policy["deduplication"]["same_rf_frequency_kept_once_per_pack"] is True
assert policy["tone_policy"]["transmit_ctcss_or_activation_tones_never_enable_transmit"] is True
assert policy["versioning"]["published_versions_are_immutable"] is True
assert policy["versioning"]["apply_to_next_versions_and_new_packs"] is True

assert emergency_policy["schema_version"] == "1.1"
assert emergency_policy["paired_rx_policy"] == "research/paired-rx-policy.json"
assert emergency_policy["publication_rules"]["rx_only"] is True
assert emergency_policy["publication_rules"]["duplex"] == "off"
assert emergency_policy["publication_rules"]["offset"] == "0.000000"
assert emergency_policy["publication_rules"]["native_duplex_or_split_both_directions_rx"] is True
assert emergency_policy["publication_rules"]["paired_distinct_frequencies_use_separate_rx_memories"] is True
assert emergency_policy["publication_rules"]["same_rf_frequency_deduplicated"] is True

for plan in (normandie_plan, annecy_plan, bretagne_plan):
    assert plan["paired_rx_policy"] == "research/paired-rx-policy.json"

assert normandie_plan["paired_rx"]["published_v0_3_1_maritime_pair_model_already_compliant"] is True
assert normandie_plan["paired_rx"]["future_analog_repeaters_and_transponders_include_both_verified_sides"] is True
assert annecy_plan["paired_rx"]["satellite_uplink_and_downlink_both_rx"] is True
assert annecy_plan["paired_rx"]["analog_repeater_input_and_output_both_rx"] is True
assert annecy_plan["paired_rx"]["crossband_transponder_both_sides_rx"] is True
assert bretagne_plan["rules"]["native_duplex_or_split_both_directions_rx"] is True
assert bretagne_plan["rules"]["paired_distinct_frequencies_use_separate_rx_memories"] is True

assert bretagne_maritime["schema_version"] == "1.7"
assert bretagne_maritime["rules"]["rx_only_duplex_channels_include_both_ship_and_coast_frequencies"] is True
assert bretagne_maritime["rules"]["paired_distinct_frequencies_use_separate_rx_memories"] is True
assert bretagne_maritime["rules"]["all_exported_memories_tx_disabled"] is True
channels = {item["channel"]: item for item in bretagne_maritime["channels"]}
for channel_number in (63, 64, 79, 80):
    channel = channels[channel_number]
    assert channel["mode"] == "duplex"
    memories = channel["rx_memories"]
    assert len(memories) == 2
    assert {item["direction"] for item in memories} == {"ship_to_coast", "coast_to_ship"}
    freq_by_direction = {item["direction"]: item["frequency_mhz"] for item in memories}
    assert freq_by_direction["ship_to_coast"] == channel["ship_tx_mhz"]
    assert freq_by_direction["coast_to_ship"] == channel["coast_tx_ship_rx_mhz"]
    assert freq_by_direction["ship_to_coast"] != freq_by_direction["coast_to_ship"]
assert channels[16]["mode"] == "simplex"
assert len(channels[16]["rx_memories"]) == 1

regions = {item["id"]: item for item in next_plan["regions"]}
assert set(regions) == {"normandie-v0.4", "annecy-alpes-leman-v0.3", "bretagne-v0.1"}

annecy_links = {item["id"]: item for item in regions["annecy-alpes-leman-v0.3"]["paired_links"]}
assert annecy_links["SAT-SO50"]["uplink_rx_mhz"] == 145.8500
assert annecy_links["SAT-SO50"]["downlink_rx_mhz"] == 436.7950
assert annecy_links["SAT-AO91"]["uplink_rx_mhz"] == 435.2500
assert annecy_links["SAT-AO91"]["downlink_rx_mhz"] == 145.9600
assert annecy_links["SAT-AO123"]["uplink_rx_mhz"] == 145.8500
assert annecy_links["SAT-AO123"]["downlink_rx_mhz"] == 435.4000
assert annecy_links["F1ZJV_F1ZYT_SHARED"]["uplink_rx_mhz"] == 145.1875
assert annecy_links["F1ZJV_F1ZYT_SHARED"]["downlink_rx_mhz"] == 145.7875

bretagne_links = {item["id"]: item for item in regions["bretagne-v0.1"]["paired_links"]}
assert bretagne_links["MARINE-79"]["ship_to_coast_rx_mhz"] == 156.9750
assert bretagne_links["MARINE-79"]["coast_to_ship_rx_mhz"] == 161.5750
assert bretagne_links["MARINE-80"]["ship_to_coast_rx_mhz"] == 157.0250
assert bretagne_links["MARINE-80"]["coast_to_ship_rx_mhz"] == 161.6250

# Published Normandie v0.3.1 is immutable but already demonstrates the paired RX model
# for native maritime duplex channels. Both rows must remain RX-only.
public_normandie = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv"
rows = list(csv.DictReader(io.StringIO(public_normandie.read_text(encoding="utf-8"))))
row_by_name = {row["Name"]: row for row in rows}
assert row_by_name["M01-S"]["Frequency"] == "156.050000"
assert row_by_name["M01-C"]["Frequency"] == "160.650000"
for name in ("M01-S", "M01-C"):
    assert row_by_name[name]["Duplex"] == "off"
    assert row_by_name[name]["Offset"] == "0.000000"

# The generic CHIRP builder must continue to hard-disable TX on every generated memory.
chirp_pack = (ROOT / "website/src/lib/chirpPack.ts").read_text(encoding="utf-8")
assert '"off"' in chirp_pack
assert '"0.000000"' in chirp_pack

# Published packs remain frozen; the new paired RX behaviour targets only new versions.
registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'version: "v0.4"' in registry
assert 'version: "v0.2"' in registry
assert 'version: "v0.4"' in registry
assert 'version: "v0.3"' not in registry
assert 'id: "bretagne"' in registry

print("Tests RadioPack paired RX policy: native duplex/split links expose both RX directions, TX remains off/zero, shared RF frequencies stay deduplicated, published packs remain immutable OK")
