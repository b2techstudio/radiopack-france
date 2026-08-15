import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / "research/annecy-alpes-leman-v0.2"

FRANCE = RESEARCH / "aviation-france-airac-08.json"
SWITZERLAND = RESEARCH / "aviation-switzerland-airac-08.json"
OPERATIONS = RESEARCH / "aviation-operational-gates.json"
GENERATOR_OPTIONS = ROOT / "generator/options.json"
PREVIOUS = RESEARCH / "aviation-france-pre-airac-08.json"

for path in [FRANCE, SWITZERLAND, OPERATIONS, GENERATOR_OPTIONS, PREVIOUS]:
    assert path.is_file(), f"Fichier aviation/générateur manquant: {path.relative_to(ROOT)}"

france = json.loads(FRANCE.read_text(encoding="utf-8"))
switzerland = json.loads(SWITZERLAND.read_text(encoding="utf-8"))
operations = json.loads(OPERATIONS.read_text(encoding="utf-8"))
generator_options = json.loads(GENERATOR_OPTIONS.read_text(encoding="utf-8"))
previous = json.loads(PREVIOUS.read_text(encoding="utf-8"))

assert france["production_ready"] is False
assert france["internal_candidate_allowed"] is True
assert france["cycle"]["validation_cycle"] == "AIRAC 08/26"
assert france["cycle"]["effective_from"] == "2026-08-06"
assert france["cycle"]["effective_until_inclusive"] == "2026-09-02"

fr_channels = france["channels"]
assert len(fr_channels) == 11
assert all(channel["verification"] == "verified_airac08_public" for channel in fr_channels)
assert all(channel["mode"] == "AM" for channel in fr_channels)
assert all(channel["step_khz"] == 8.33 for channel in fr_channels)
assert all(channel["tx_policy"] == "rx_only" for channel in fr_channels)

fr_by_name = {channel["name"]: channel for channel in fr_channels}
assert set(fr_by_name) == {
    "ANNCY-TWR", "ANNMS-A-A", "CHAM-INFO", "CHAM-APP", "CHAM-TWR",
    "CHAM-ATIS", "VERSD-A-A", "GREN-GND", "GREN-TWR", "GREN-ATIS",
    "GENEV-INFO",
}
assert fr_by_name["ANNCY-TWR"]["frequency_mhz"] == 118.2
assert fr_by_name["ANNMS-A-A"]["frequency_mhz"] == 125.875
assert fr_by_name["CHAM-INFO"]["frequency_mhz"] == 123.7
assert fr_by_name["CHAM-APP"]["frequency_mhz"] == 121.205
assert fr_by_name["CHAM-TWR"]["frequency_mhz"] == 118.3
assert fr_by_name["CHAM-ATIS"]["frequency_mhz"] == 127.1
assert fr_by_name["VERSD-A-A"]["frequency_mhz"] == 121.0
assert fr_by_name["GREN-GND"]["frequency_mhz"] == 121.93
assert fr_by_name["GREN-TWR"]["frequency_mhz"] == 119.3
assert fr_by_name["GREN-ATIS"]["frequency_mhz"] == 133.855
assert fr_by_name["GENEV-INFO"]["frequency_mhz"] == 126.35
assert set(fr_by_name["CHAM-INFO"]["services"]) == {"FIS", "APP", "A/A"}

assert france["pending"] == []
fr_excluded = {item["icao"]: item for item in france["excluded"]}
assert set(fr_excluded) == {"LFKA", "LFHM", "LFHZ"}
assert fr_excluded["LFKA"]["status"] == "excluded_scope_unverified_primary"
assert fr_excluded["LFHM"]["status"] == "excluded_scope_unverified_primary"
assert fr_excluded["LFHZ"]["status"] == "excluded_closed_aerodrome"
assert fr_excluded["LFHZ"]["effective_from"] == "2020-09-01"
assert "SIA-LFKA-VAC-CATALOG" in fr_excluded["LFKA"]["source_ids"]
assert "SIA-LFHM-VAC-CATALOG" in fr_excluded["LFHM"]["source_ids"]
assert "LEGIFRANCE-LFHZ-CLOSED-2020" in fr_excluded["LFHZ"]["source_ids"]
assert all(channel["verification"] == "pre_airac_recheck" for channel in previous["channels"])

assert switzerland["production_ready"] is False
assert switzerland["internal_candidate_allowed"] is True
assert switzerland["cycle"]["aip_airac_amdt_effective"] == "2026-08-06"

ch_channels = switzerland["channels"]
assert len(ch_channels) == 6
assert all(channel["verification"] == "verified_current_public" for channel in ch_channels)
assert all(channel["mode"] == "AM" for channel in ch_channels)
assert all(channel["step_khz"] == 8.33 for channel in ch_channels)
assert all(channel["tx_policy"] == "rx_only" for channel in ch_channels)

ch_by_name = {channel["name"]: channel for channel in ch_channels}
assert set(ch_by_name) == {
    "CH-LSGLAD", "CH-LSGLAP", "CH-SIONGND", "CH-SIONTWR",
    "CH-SIONATI", "CH-SIONAPP",
}
assert ch_by_name["CH-LSGLAD"]["frequency_mhz"] == 123.205
assert ch_by_name["CH-LSGLAP"]["frequency_mhz"] == 118.83
assert ch_by_name["CH-SIONGND"]["frequency_mhz"] == 121.705
assert ch_by_name["CH-SIONTWR"]["frequency_mhz"] == 118.275
assert ch_by_name["CH-SIONATI"]["frequency_mhz"] == 130.63
assert ch_by_name["CH-SIONAPP"]["frequency_mhz"] == 126.825
assert switzerland["pending"] == []

ch_excluded = switzerland["excluded"]
excluded_ch_frequencies = {
    frequency
    for item in ch_excluded
    for frequency in item.get("frequencies_mhz", [])
}
assert excluded_ch_frequencies == {131.475, 131.67, 131.955, 110.7, 112.15}
geneva = next(item for item in ch_excluded if item["icao"] == "LSGG")
assert geneva["status"] == "excluded_scope_unverified_primary"
assert "BAZL-LSGG" in geneva["source_ids"]

all_channels = fr_channels + ch_channels
assert len({channel["frequency_mhz"] for channel in all_channels}) == len(all_channels)
assert all(len(channel["name"]) <= 10 for channel in all_channels)
assert not excluded_ch_frequencies.intersection({channel["frequency_mhz"] for channel in ch_channels})

assert operations["public_release_allowed"] is True
assert operations["generator_options_contract"] == "generator/options.json"
gates = {gate["id"]: gate for gate in operations["gates"]}
assert gates["airac_fr"]["status"] == "passed_research_validation"
assert gates["airac_ch"]["status"] == "passed_research_validation"
assert gates["notam_fr"]["status"] == "advisory_optional_pre_generation"
assert gates["notam_ch"]["status"] == "advisory_optional_pre_generation"
assert gates["notam_fr"]["required_for_public_release"] is False
assert gates["notam_ch"]["required_for_public_release"] is False
assert gates["notam_fr"]["generator_option_id"] == "notam_check"
assert gates["notam_ch"]["generator_option_id"] == "notam_check"
assert gates["pending_airfields"]["status"] == "passed_scope_closed"
assert gates["pending_airfields"]["items"] == []
assert gates["pending_airfields"]["excluded_from_v0_2"] == ["LFKA", "LFHM", "LSGG", "LFHZ"]
assert gates["dynamic_satellites"]["status"] == "passed_official_amsat_recheck"
assert gates["dynamic_satellites"]["checked"] == "2026-08-08"
for required_gate in ["airac_fr", "airac_ch", "pending_airfields", "dynamic_satellites"]:
    assert gates[required_gate]["required_for_public_release"] is True

assert generator_options["schema_version"] == "3.0"
assert generator_options["status"] == "multi_region_public_generator"
implementation = generator_options["implementation"]
assert implementation["generic_pack_library"] == "website/src/lib/chirpPack.ts"
assert implementation["annecy_pack_library"] == "website/src/lib/annecyPack.ts"
assert implementation["public_pack_registry"] == "website/src/lib/packRegistry.ts"
assert implementation["published_pack_count"] >= 2
assert implementation["default_pack"] == "annecy-alpes-leman"
assert implementation["public_ui_wired"] is True
assert implementation["public_ui_download_locked"] is False
assert implementation["public_download_created"] is True

include_aviation = generator_options["options"]["include_aviation"]
notam = generator_options["options"]["notam_check"]
assert include_aviation["scope"] == ["annecy-alpes-leman"]
assert include_aviation["type"] == "boolean"
assert include_aviation["default"] is True
assert include_aviation["affects_csv_content"] is True
assert include_aviation["annecy_memory_count_when_enabled"] == 76
assert include_aviation["annecy_memory_count_when_disabled"] == 59
assert notam["scope"] == ["annecy-alpes-leman"]
assert notam["default"] == "disabled"
assert notam["affects_csv_content"] is False
assert notam["blocks_generation"] is False
assert notam["states"] == ["disabled", "requested_unconfirmed", "user_confirmed"]
assert notam["future_state_reserved"] == "automatic_verified"
assert generator_options["ui_contract"]["pack_selector"] is True
assert generator_options["ui_contract"]["generation_allowed_when_notam_unconfirmed"] is True
assert generator_options["ui_contract"]["download_enabled"] is True
assert generator_options["ui_contract"]["unsupported_options_hidden"] is True

# AIRAC 08/26 research material remains the validated aviation basis inherited by v0.3;
# publication is recorded separately and does not rewrite the historical research files.
publication_record = json.loads((ROOT / "research/annecy-alpes-leman-v0.3/publication-record.json").read_text(encoding="utf-8"))
assert publication_record["status"] == "published_immutable"
assert publication_record["version"] == "0.3"
assert publication_record["aviation_memory_count"] == 17
assert publication_record["full_memory_count"] == 76
assert publication_record["without_aviation_memory_count"] == 59

print("Tests Annecy–Alpes–Léman AIRAC 08 aviation + multi-region generator: AIRAC 08/26 historical basis intact, current public v0.3 counts 76/59 OK")
