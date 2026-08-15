import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

policy = json.loads((ROOT / "research/emergency-radio-policy.json").read_text(encoding="utf-8"))
assert policy["status"] == "active_research_policy"
assert policy["publication_rules"]["rx_only"] is True
assert policy["publication_rules"]["duplex"] == "off"
assert policy["publication_rules"]["offset"] == "0.000000"
assert policy["publication_rules"]["no_private_operational_channel"] is True
assert policy["publication_rules"]["published_versions_are_immutable"] is True
excluded_ids = {item["id"] for item in policy["research_only_or_excluded_categories"]}
assert "private_ppdr_pmr" in excluded_ids
assert "private_association_operational_channels" in excluded_ids
assert "digital_only_incompatible" in excluded_ids

normandie_plan = json.loads((ROOT / "research/normandie-v0.4/pack-plan.json").read_text(encoding="utf-8"))
normandie = json.loads((ROOT / "research/normandie-v0.4/emergency-relays.json").read_text(encoding="utf-8"))
assert normandie_plan["status"] == "research_next_version_not_public"
assert normandie_plan["based_on_published_version"] == "0.3.1"
assert normandie_plan["published_base_is_immutable"] is True
assert normandie_plan["priority_focus"]["label"] == "Mortain-Bocage / Sud-Manche"
assert normandie_plan["priority_focus"]["adjacent_departments_to_check"] == [35, 53, 61]
assert normandie_plan["publication"]["public_export_allowed"] is False
n_candidates = {item["id"]: item for item in normandie["candidates"]}
assert n_candidates["F5ZHY"]["output_mhz"] == 145.6875
assert n_candidates["F5ZHY"]["rx_pack_candidate"] is True
assert n_candidates["F6ZES"]["site"] == "Sourdeval"
assert n_candidates["F6ZES"]["output_mhz"] is None
assert n_candidates["F6ZCE"]["department"] == 53
assert n_candidates["F6ZCE"]["output_mhz"] == 145.7000
assert n_candidates["F1ZBX"]["department"] == 35
assert n_candidates["F5ZTE"]["rx_pack_candidate"] is False
assert all(item["frequency_promoted_to_public_pack"] is False for item in normandie["candidates"])
assert normandie["rules"]["published_v0_3_1_must_not_change"] is True
assert normandie["rules"]["private_ppdr_operational_frequencies_excluded"] is True

annecy_plan = json.loads((ROOT / "research/annecy-alpes-leman-v0.3/pack-plan.json").read_text(encoding="utf-8"))
annecy = json.loads((ROOT / "research/annecy-alpes-leman-v0.3/emergency-relays.json").read_text(encoding="utf-8"))
annecy_record_path = ROOT / "research/annecy-alpes-leman-v0.3/publication-record.json"
if annecy_record_path.exists():
    annecy_record = json.loads(annecy_record_path.read_text(encoding="utf-8"))
    assert annecy_plan["status"] == "published_immutable_v0_3"
    assert annecy_plan["publication"]["public_export_allowed"] is True
    assert annecy_plan["publication"]["public_registry_allowed"] is True
    assert annecy_plan["publication"]["published"] is True
    assert annecy_record["status"] == "published_immutable"
    assert annecy_record["version"] == "0.3"
else:
    assert annecy_plan["status"] == "research_next_version_not_public"
    assert annecy_plan["publication"]["public_export_allowed"] is False
assert annecy_plan["based_on_published_version"] == "0.2"
assert annecy_plan["published_base_is_immutable"] is True
a_candidates = {item["id"]: item for item in annecy["candidates"]}
assert a_candidates["F1ZJV"]["output_mhz"] == 145.7875
assert a_candidates["F1ZJV"]["rx_pack_candidate"] is True
assert a_candidates["F1ZYT"]["output_mhz"] == 145.7875
assert a_candidates["F1ZYT"]["rx_pack_candidate"] is False
assert a_candidates["F1ZHG"]["output_mhz"] == 145.2875
assert a_candidates["F5ZGT"]["output_mhz"] == 145.4500
# This emergency inventory is historical research evidence. Publication is recorded
# separately and must not rewrite the original per-candidate research flags.
assert all(item["frequency_promoted_to_public_pack"] is False for item in annecy["candidates"])
assert annecy["rules"]["published_v0_2_must_not_change"] is True
assert annecy["rules"]["same_output_frequency_must_not_be_duplicated_for_site_label_only"] is True

bretagne = json.loads((ROOT / "research/bretagne-v0.1/emergency-relays.json").read_text(encoding="utf-8"))
bretagne_gates = json.loads((ROOT / "research/bretagne-v0.1/publication-gates.json").read_text(encoding="utf-8"))
assert bretagne["schema_version"] == "1.4"
assert {item["id"] for item in bretagne["organisations"]} == {"ADRASEC-22", "ADRASEC-29", "ADRASEC-35", "ADRASEC-56"}
b_candidates = {item["id"]: item for item in bretagne["candidates"]}
assert b_candidates["F1ZUG-4"]["frequency_mhz"] == 144.8000
assert b_candidates["F1ZUG-4"]["adrasec_transponder_frequency_mhz"] is None
assert b_candidates["F1ZUG-4"]["adrasec_transponder_role_status"] == "public_ara35_2024_role_documented_frequency_unpublished"
assert b_candidates["F1ZUG-4"]["rx_pack_candidate"] is False
assert b_candidates["F5ZZC-4"]["frequency_mhz"] is None
assert b_candidates["F1ZBX"]["output_mhz"] == 145.6750
assert b_candidates["F5ZEB"]["output_mhz"] == 438.6750
assert b_candidates["F5ZEB"]["input_mhz"] == 431.0750
assert b_candidates["F5ZEB"]["ctcss_hz"] == 71.9
assert b_candidates["F5ZEB"]["rx_pack_candidate"] is False
assert b_candidates["F5ZPV"]["output_mhz"] == 439.8750
assert b_candidates["F5ZPV"]["status"] == "temporarily_stopped_current_ara35_page"
assert b_candidates["F5ZPV"]["rx_pack_candidate"] is False
assert b_candidates["F5ZZH"]["output_mhz"] == 145.7875
assert b_candidates["F5ZZH"]["input_mhz"] == 145.1875
assert b_candidates["F5ZZH"]["status"] == "temporarily_stopped_searching_new_site_current_ara35_page"
assert b_candidates["F5ZZH"]["rx_pack_candidate"] is False
for relay_id, output_mhz in {"F1ZGS": 431.4250, "F5ZDV": 438.7000, "F5ZZL": 431.3750}.items():
    assert b_candidates[relay_id]["department"] == 29
    assert b_candidates[relay_id]["output_mhz"] == output_mhz
    assert b_candidates[relay_id]["input_mhz"] == 145.2625
    assert b_candidates[relay_id]["ctcss_hz"] == 71.9
    assert b_candidates[relay_id]["mode"] == "FM"
    assert b_candidates[relay_id]["rx_pack_candidate"] is True
assert b_candidates["F1ZAJ"]["department"] == 56
assert b_candidates["F1ZAJ"]["frequency_mhz"] == 144.8000
assert b_candidates["F1ZAJ"]["rx_pack_candidate"] is False
assert bretagne["rules"]["private_ppdr_operational_frequencies_excluded"] is True
assert bretagne["rules"]["aprs_same_frequency_not_duplicated_by_site"] is True
assert bretagne["rules"]["adrasec_transponder_frequency_must_not_be_inferred_from_aprs_frequency"] is True
assert bretagne["rules"]["temporarily_stopped_repeaters_not_active_candidates"] is True
assert bretagne["rules"]["north_south_zoning_required"] is True
assert bretagne["rules"]["adrasec_role_must_not_be_inferred_from_geography_only"] is True
assert all(item["frequency_promoted_to_public_pack"] is False for item in bretagne["candidates"])
gates = {gate["id"]: gate for gate in bretagne_gates["gates"]}
assert gates["emergency_relay_inventory"]["required_for_public_release"] is True
assert gates["emergency_relay_inventory"]["status"] != "passed"

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'id: "bretagne"' in registry
assert 'version: "v0.4"' in registry
assert 'version: "v0.3"' in registry
assert not (ROOT / "website/src/pages/downloads/bretagne").exists()
assert not (ROOT / "website/src/pages/downloads/normandie/radiopack-france-normandie-v0.4.csv.ts").exists()
# Annecy v0.3 is published as a static immutable CSV, not a dynamic .ts route.
assert not (ROOT / "website/src/pages/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv.ts").exists()
assert (ROOT / "website/public/downloads/annecy-alpes-leman/radiopack-france-annecy-alpes-leman-v0.3.csv").is_file()

published_normandie = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv"
assert published_normandie.is_file()

print("Tests RadioPack Sprint 29 emergency/ADRASEC research: historical emergency inventories remain auditable, Annecy v0.3 publication is recognized separately, private operational RF stays excluded, OK")
