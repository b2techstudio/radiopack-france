import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ETEL = ROOT / "research/bretagne-v0.1/etel-channel64-evidence.json"
CORSEN = ROOT / "research/bretagne-v0.1/corsen-channel79-evidence.json"

for path in (ETEL, CORSEN):
    assert path.is_file(), f"Missing Sprint 62 evidence file: {path}"

etel = json.loads(ETEL.read_text(encoding="utf-8"))
assert etel["status"] == "primary_current_channel64_conflict_documented_site_unresolved"
assert etel["updated"] == "2026-08-11"
assert etel["paired_rx"]["ship_to_coast_mhz"] == 156.225
assert etel["paired_rx"]["coast_to_ship_mhz"] == 160.825
assert etel["paired_rx"]["new_rf_memory_delta"] == 0

conv = etel["operational_primary_convergence"]
assert conv["current_cross_page_explicit_channel63"] is True
assert conv["current_cross_schedule_explicit_channel63"] is True
assert conv["annual_report_2025_explicit_channel63"] is True
assert conv["current_local_operational_sources_explicit_channel63_count"] == 3
assert conv["current_local_operational_sources_explicit_channel64_count"] == 0
assert conv["current_local_operational_evidence_converges_on_channel63"] is True
assert conv["channel64_current_operation_proven"] is False
assert conv["channel64_stopped_proven"] is False

mf_etel = etel["primary_reference_targets"][0]
assert mf_etel["authority"] == "Météo-France"
assert mf_etel["page_updated"] == "2026-08-05"
assert mf_etel["guide_pdf_content_extracted_in_current_workflow"] is False
assert mf_etel["channel64_conclusion_from_unread_guide"] is None
assert etel["assessment"]["generic_ministry_statement_still_conflicts_with_local_operational_documentation"] is True
assert etel["assessment"]["channel64_current_operation_proven"] is False
assert etel["assessment"]["channel64_stopped_proven"] is False
assert etel["assessment"]["channel64_site_confirmed"] is False
assert etel["assessment"]["site_assignment_can_be_promoted"] is False
assert etel["rules"]["unread_primary_reference_is_not_negative_evidence"] is True
assert etel["rules"]["local_operational_channel63_convergence_does_not_disprove_channel64"] is True
assert etel["rules"]["public_export_allowed"] is False

corsen = json.loads(CORSEN.read_text(encoding="utf-8"))
assert corsen["status"].endswith("primary_current_channel79_site_validation_pending")
assert corsen["updated"] == "2026-08-11"
assert corsen["paired_rx"]["new_rf_memory_delta"] == 0
assert corsen["assessment"]["primary_current_channel79_transmitter_site_confirmed"] is False
assert corsen["assessment"]["current_primary_infrastructure_sites_verified"] == ["Cap Fréhel", "Stiff / Ouessant"]
assert corsen["assessment"]["secondary_clue_sites"] == ["Cap Fréhel", "Bodic"]
assert corsen["assessment"]["historical_primary_channel79_context_exists"] is True
assert corsen["assessment"]["site_assignment_can_be_promoted"] is False
assert corsen["primary_revalidation_search"]["direct_primary_channel79_site_match_found"] is False

hist = corsen["historical_primary_channel79_context"][0]
assert hist["source_class"] == "historical_primary"
assert hist["current_site_channel_validation"] is False
assert hist["historical_evidence_can_promote_current_site_assignment"] is False

mf_corsen = corsen["primary_reference_targets"][0]
assert mf_corsen["authority"] == "Météo-France"
assert mf_corsen["page_updated"] == "2026-08-05"
assert mf_corsen["guide_pdf_content_extracted_in_current_workflow"] is False
assert mf_corsen["channel79_site_conclusion_from_unread_guide"] is None
assert corsen["rules"]["historical_primary_channel_assignment_is_not_current_validation"] is True
assert corsen["rules"]["current_radio_infrastructure_does_not_imply_channel_assignment"] is True
assert corsen["rules"]["unread_primary_reference_is_not_negative_evidence"] is True
assert corsen["rules"]["public_export_allowed"] is False

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8").lower()
assert 'id: "bretagne"' not in registry
assert 'version: "0.4"' not in registry

normandie_public = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv"
assert normandie_public.is_file()
assert len(normandie_public.read_text(encoding="utf-8").splitlines()) == 140

print(
    "Sprint 62 primary reference guards: Etel local operational evidence converges on channel 63 without "
    "proving channel 64 active or stopped; Corsen current Cap Frehel/Stiff infrastructure and historical "
    "channel 79 context remain distinct from a current site-channel assignment; unread Meteo-France Guide "
    "Marine creates no inference; public packs unchanged, OK"
)
