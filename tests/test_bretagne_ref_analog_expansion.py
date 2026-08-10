import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "research/bretagne-v0.1/ref-analog-expansion.json"
assert path.is_file()

data = json.loads(path.read_text(encoding="utf-8"))
assert data["schema_version"] == "1.0"
assert data["status"] == "current_ref_active_analog_expansion_research_not_public"
assert data["source"]["authority"] == "Réseau des Émetteurs Français (REF)"

candidates = {item["id"]: item for item in data["new_active_candidates"]}
assert set(candidates) == {"F5ZIU", "F5ZIV", "F5ZJR", "F1ZMU"}

assert candidates["F5ZIU"]["site"] == "La Harmoye"
assert candidates["F5ZIU"]["locator"] == "IN88LI87TK"
assert candidates["F5ZIU"]["altitude_m"] == 318
assert candidates["F5ZIU"]["side_a_rx_mhz"] == 145.4625
assert candidates["F5ZIU"]["side_b_rx_mhz"] == 432.6500
assert candidates["F5ZIU"]["ctcss_hz"] == 71.9

assert candidates["F5ZIV"]["site"] == "Saint-Brieuc"
assert candidates["F5ZIV"]["locator"] == "IN88OM43CW"
assert candidates["F5ZIV"]["altitude_m"] == 119
assert candidates["F5ZIV"]["side_a_rx_mhz"] == 145.4875
assert candidates["F5ZIV"]["side_b_rx_mhz"] == 432.6500
assert candidates["F5ZIV"]["antenna_gain_dbi"] == 8

assert candidates["F5ZJR"]["site"] == "Plessala"
assert candidates["F5ZJR"]["locator"] == "IN88QH97WI"
assert candidates["F5ZJR"]["altitude_m_by_ref_row"] == {"vhf_side": 335, "uhf_side": 339}
assert candidates["F5ZJR"]["side_a_rx_mhz"] == 145.2875
assert candidates["F5ZJR"]["side_b_rx_mhz"] == 432.6500

assert candidates["F1ZMU"]["site"] == "Saint-Nolff"
assert candidates["F1ZMU"]["locator"] == "IN87QR21GN"
assert candidates["F1ZMU"]["output_mhz"] == 430.3250
assert candidates["F1ZMU"]["input_mhz"] == 439.7250
assert candidates["F1ZMU"]["power_w"] == 50

for item in candidates.values():
    assert item["status"] == "current_ref_active"
    assert item["review_priority"] == "next_coverage_review"
    assert item["coverage_claim"] is None
    assert item["frequency_promoted_to_public_pack"] is False

lorient = data["resolved_multi_path_candidate"]
assert lorient["id"] == "F1ZBZ"
assert lorient["site"] == "Lorient"
assert lorient["shared_uhf_mhz"] == 431.2000
assert lorient["status"] == "current_ref_active_multi_path_explicit_rows"
assert lorient["unique_rx_frequencies_mhz"] == [431.2000, 145.6250, 145.0250, 145.7375, 145.1375]
paths = {(item["repeater_emission_mhz"], item["repeater_reception_mhz"]) for item in lorient["documented_ref_rows"] if item["function"] == "Transpond."}
assert paths == {
    (431.2000, 145.6250),
    (145.0250, 431.2000),
    (431.2000, 145.7375),
    (145.1375, 431.2000),
}
assert lorient["coverage_claim"] is None
assert lorient["frequency_promoted_to_public_pack"] is False

clusters = {item["frequency_mhz"]: item for item in data["shared_frequency_clusters"]}
assert set(clusters[432.6500]["roles"]) == {"F5ZIS", "F5ZIT", "F5ZIU", "F5ZIV", "F5ZJR"}
assert set(clusters[145.1375]["roles"]) == {"F5ZPE input", "F1ZBZ repeater emission path"}
assert set(clusters[145.7375]["roles"]) == {"F5ZPE output", "F1ZBZ repeater reception path"}

assert data["rules"]["coverage_not_inferred_from_altitude_power_or_antenna_gain"] is True
assert data["rules"]["adrasec_role_not_inferred_from_geography"] is True
assert data["rules"]["multi_path_rows_preserve_ref_emission_reception_direction"] is True
assert data["rules"]["shared_rf_frequency_deduplicated"] is True
assert data["rules"]["tx_disabled_in_future_export"] is True
assert data["rules"]["public_export_allowed"] is False

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'id: "bretagne"' not in registry

print("Tests Bretagne REF analog expansion: F5ZIU/F5ZIV/F5ZJR/F1ZMU active, F1ZBZ multi-path explicit, no coverage or ADRASEC inference, no public mutation OK")
