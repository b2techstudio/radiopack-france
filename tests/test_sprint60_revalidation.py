import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

f6zes = json.loads((ROOT / "research/normandie-v0.4/f6zes-revalidation.json").read_text(encoding="utf-8"))
corsen = json.loads((ROOT / "research/bretagne-v0.1/corsen-channel79-evidence.json").read_text(encoding="utf-8"))

assert f6zes["status"] == "current_ref_revalidated_frequency_mode_unresolved"
assert f6zes["station"] == {
    "callsign": "F6ZES",
    "site": "Sourdeval",
    "responsible": "F1SMB",
    "locator": "IN98MR93XV",
    "altitude_m": 230,
}
observed = f6zes["current_primary_or_associative_evidence"][0]["observed"]
for key in ("operational_state", "band", "tx_mhz", "rx_mhz", "mode"):
    assert observed[key] is None
assert f6zes["decision"]["frequency_resolved"] is False
assert f6zes["decision"]["mode_resolved"] is False
assert f6zes["decision"]["paired_rx_candidate_frequencies_mhz"] == []
assert f6zes["decision"]["candidate_memory_delta"] == 0
assert f6zes["decision"]["promote_to_internal_candidate"] is False
assert f6zes["rules"]["sourdeval_must_not_be_guessed"] is True
assert f6zes["rules"]["search_failure_is_not_negative_evidence"] is True
assert f6zes["rules"]["frequency_promoted_to_internal_candidate"] is False
assert f6zes["rules"]["frequency_promoted_to_public_pack"] is False
assert f6zes["rules"]["public_export_allowed"] is False

assert corsen["status"].endswith("primary_current_channel79_site_validation_pending")
assert corsen["channel"] == 79
assert corsen["paired_rx"]["ship_to_coast_mhz"] == 156.975
assert corsen["paired_rx"]["coast_to_ship_mhz"] == 161.575
assert corsen["paired_rx"]["both_frequencies_already_in_bretagne_research_plan"] is True
assert corsen["paired_rx"]["new_rf_memory_delta"] == 0
assert all(item["channel_79_transmitter_site_identified"] is False for item in corsen["primary_current_context"])
clue = corsen["secondary_current_clues"][0]
assert clue["source_class"] == "local_secondary_current"
assert clue["reported_channel"] == 79
assert [item["site"] for item in clue["reported_sites"]] == ["Cap Fréhel", "Bodic"]
assert corsen["assessment"]["primary_current_channel79_transmitter_site_confirmed"] is False
assert corsen["assessment"]["secondary_clue_sites"] == ["Cap Fréhel", "Bodic"]
assert corsen["assessment"]["site_assignment_can_be_promoted"] is False
assert corsen["rules"]["secondary_current_clue_is_not_primary_validation"] is True
assert corsen["rules"]["channel79_site_must_not_be_guessed"] is True
assert corsen["rules"]["no_new_rf_memory_from_site_metadata"] is True
assert corsen["rules"]["frequency_promoted_to_public_pack"] is False
assert corsen["rules"]["public_export_allowed"] is False

print(
    "Sprint 60 revalidation: F6ZES remains frequency/mode unresolved with zero candidate delta; "
    "Corsen channel 79 gains guarded local clues for Cap Frehel/Bodic without primary site promotion or public side effects, OK"
)
