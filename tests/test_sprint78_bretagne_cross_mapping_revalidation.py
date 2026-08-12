import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = json.loads((ROOT / "research/bretagne-v0.2/cross-local-mapping-revalidation.json").read_text(encoding="utf-8"))
BACKLOG = json.loads((ROOT / "research/bretagne-v0.2/backlog.json").read_text(encoding="utf-8"))
PLAN = json.loads((ROOT / "research/bretagne-v0.2/pack-plan.json").read_text(encoding="utf-8"))

assert EVIDENCE["status"] == "primary_current_cross_local_mapping_revalidated_unresolved_zero_rf_delta_not_public"
assert EVIDENCE["checked_on"] == "2026-08-12"
assert EVIDENCE["candidate_memory_count_before_review"] == 151
assert EVIDENCE["candidate_memory_count_after_review"] == 151
assert EVIDENCE["candidate_memory_delta"] == 0
assert EVIDENCE["public_export_allowed"] is False

reviews = {item["id"]: item for item in EVIDENCE["reviews"]}
assert set(reviews) == {"CROSS_ETEL_CH64_LOCAL_MAPPING", "CROSS_CORSEN_CH79_LOCAL_MAPPING"}

etel = reviews["CROSS_ETEL_CH64_LOCAL_MAPPING"]
assert etel["channel"] == 64
assert etel["paired_rx_mhz"] == [156.225, 160.825]
assert etel["generic_pair_already_present"] is True
assert etel["new_rf_memory_delta"] == 0
assert etel["local_site_mapping_promoted"] is False
assert etel["assessment"]["channel64_regional_current_statement_exists"] is True
assert etel["assessment"]["etel_current_channel63_mapping_exists"] is True
assert etel["assessment"]["channel64_brittany_transmitter_site_confirmed"] is False
assert etel["assessment"]["channel64_stopped_proven"] is False
assert etel["assessment"]["primary_source_conflict_open"] is True
assert etel["assessment"]["promotion_allowed"] is False
pdf_source = [source for source in etel["primary_sources"] if source["title"].startswith("Heures de diffusion")][0]
assert pdf_source["pdf_text_extracted_by_web_parser"] is True
assert pdf_source["pdf_screenshot_attempted"] is True
assert pdf_source["pdf_screenshot_succeeded"] is False

corsen = reviews["CROSS_CORSEN_CH79_LOCAL_MAPPING"]
assert corsen["channel"] == 79
assert corsen["paired_rx_mhz"] == [156.975, 161.575]
assert corsen["generic_pair_already_present"] is True
assert corsen["new_rf_memory_delta"] == 0
assert corsen["local_site_mapping_promoted"] is False
assert corsen["assessment"]["current_cross_network_confirmed"] is True
assert corsen["assessment"]["primary_current_channel79_transmitter_site_confirmed"] is False
assert corsen["assessment"]["secondary_site_chain_exists"] is True
assert corsen["assessment"]["secondary_site_chain_promotable"] is False
assert corsen["assessment"]["promotion_allowed"] is False
secondary = {item["source"]: item for item in corsen["secondary_clues"]}
assert secondary["Club de Voile de la Baie d'Erquy"]["reported_sites"] == ["Cap Frehel", "Bodic"]
assert secondary["Randonnée Kayak"]["reported_sites"] == ["Cap Frehel", "Bodic", "Batz", "Stiff", "Pointe du Raz"]
assert all(item["current_primary_validation"] is False for item in secondary.values())

assert EVIDENCE["promotion_decision"]["new_unique_rf_memory_count"] == 0
assert EVIDENCE["promotion_decision"]["candidate_memory_count"] == 151
assert EVIDENCE["promotion_decision"]["local_site_metadata_promoted_count"] == 0
assert EVIDENCE["promotion_decision"]["public_pack_mutation_allowed"] is False

items = {item["id"]: item for item in BACKLOG["items"]}
for item_id in ("CROSS_ETEL_CH64_LOCAL_MAPPING", "CROSS_CORSEN_CH79_LOCAL_MAPPING"):
    item = items[item_id]
    assert item["candidate_memory_delta"] == 0
    assert item["promoted_local_site_mapping"] is False
    assert item["evidence"] == "research/bretagne-v0.2/cross-local-mapping-revalidation.json"
    assert item["resolved_zero_delta_for_current_review"] is True

assert PLAN["current_candidate_memory_count"] == 151
assert PLAN["current_new_memory_count"] == 16
cross = PLAN["latest_cross_revalidation"]
assert cross["candidate_memory_count_before"] == 151
assert cross["candidate_memory_count_after"] == 151
assert cross["candidate_memory_delta"] == 0
assert cross["local_site_metadata_promoted_count"] == 0
assert cross["etel_channel64_current_brittany_site_confirmed"] is False
assert cross["corsen_channel79_primary_current_transmitter_site_confirmed"] is False
assert PLAN["public_export_allowed"] is False
assert PLAN["public_registry_allowed"] is False

assert EVIDENCE["rules"]["generic_rf_pair_must_not_be_duplicated_for_site_metadata"] is True
assert EVIDENCE["rules"]["secondary_site_clue_is_not_primary_validation"] is True
assert EVIDENCE["rules"]["unread_primary_pdf_is_not_negative_evidence"] is True
assert EVIDENCE["rules"]["site_assignment_must_not_be_guessed"] is True
assert EVIDENCE["rules"]["rx_only"] is True

print("Sprint 78 Bretagne CROSS mapping revalidation: Ch64/Ch79 remain generic, no primary current site mapping promoted, candidate stays 151 RX OK")
