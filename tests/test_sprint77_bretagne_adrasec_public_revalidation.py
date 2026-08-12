import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = json.loads((ROOT / 'research/bretagne-v0.2/adrasec-public-revalidation.json').read_text(encoding='utf-8'))
PLAN = json.loads((ROOT / 'research/bretagne-v0.2/pack-plan.json').read_text(encoding='utf-8'))
BACKLOG = json.loads((ROOT / 'research/bretagne-v0.2/backlog.json').read_text(encoding='utf-8'))

assert EVIDENCE['status'] == 'public_revalidation_completed_zero_rf_delta_not_public'
assert EVIDENCE['checked_on'] == '2026-08-12'
assert EVIDENCE['scope']['departments'] == [22, 29, 35, 56]
assert EVIDENCE['scope']['operational_private_frequency_research_performed'] is False
assert EVIDENCE['private_ppdr_operational_data_excluded'] is True
assert EVIDENCE['candidate_memory_count_before_review'] == 151
assert EVIDENCE['candidate_memory_count_after_review'] == 151
assert EVIDENCE['candidate_memory_delta'] == 0
assert set(EVIDENCE['national_membership']['confirmed_members']) == {
    'ADRASEC 22', 'ADRASEC 29', 'ADRASEC 35', 'ADRASEC 56'
}
assert EVIDENCE['national_membership']['frequency_data_present'] is False

reviews = {item['department']: item for item in EVIDENCE['department_reviews']}
assert set(reviews) == {22, 29, 35, 56}

assert reviews[22]['public_current_adrasec_frequency_validated'] is False
assert reviews[22]['candidate_memory_delta'] == 0

assert reviews[29]['public_current_adrasec_frequency_validated'] is True
assert reviews[29]['validated_public_role_frequency']['frequency_mhz'] == 144.8
assert reviews[29]['already_present_in_national_pack'] is True
assert reviews[29]['candidate_memory_delta'] == 0
assert {site['callsign'] for site in reviews[29]['validated_public_role_frequency']['sites']} == {'F1ZBH-3', 'F1ZGQ-3'}

assert reviews[35]['public_current_adrasec_frequency_validated'] is False
assert reviews[35]['f1zug_aprs_frequency_mhz'] == 144.8
assert reviews[35]['aprs_frequency_already_present_nationally'] is True
assert reviews[35]['f1zug_adrasec_transponder_frequency_mhz'] is None
assert reviews[35]['must_not_infer_transponder_frequency_from_aprs'] is True
assert reviews[35]['candidate_memory_delta'] == 0

assert reviews[56]['public_current_adrasec_frequency_validated'] is False
assert reviews[56]['candidate_memory_delta'] == 0

assert EVIDENCE['promotion_decision']['new_unique_rf_memory_count'] == 0
assert EVIDENCE['promotion_decision']['candidate_memory_count'] == 151
assert EVIDENCE['promotion_decision']['public_pack_mutation_allowed'] is False
assert EVIDENCE['rules']['organisation_membership_does_not_publish_frequency'] is True
assert EVIDENCE['rules']['geography_does_not_prove_adrasec_role'] is True
assert EVIDENCE['rules']['aprs_role_does_not_imply_other_service_frequency'] is True
assert EVIDENCE['rules']['historical_role_does_not_equal_current_role'] is True
assert EVIDENCE['rules']['unpublished_operational_frequency_must_not_be_inferred'] is True
assert EVIDENCE['rules']['private_ppdr_operational_data_excluded'] is True

adrasec = next(item for item in BACKLOG['items'] if item['id'] == 'ADRASEC_PUBLIC_DATA_REVALIDATION')
assert adrasec['state'] == 'public_revalidation_completed_zero_rf_delta'
assert adrasec['potential_memory_delta'] == 0
assert adrasec['candidate_memory_delta'] == 0
assert adrasec['resolved_zero_delta'] is True
assert adrasec['promoted'] is False

f1zug = next(item for item in BACKLOG['items'] if item['id'] == 'F1ZUG_ADRASEC35_ROLE_REVALIDATION')
assert f1zug['aprs_frequency_mhz'] == 144.8
assert f1zug['aprs_frequency_already_present_nationally'] is True
assert f1zug['adrasec_transponder_frequency_mhz'] is None
assert f1zug['must_not_infer_from_aprs'] is True

latest = PLAN['latest_adrasec_revalidation']
assert latest['departments'] == [22, 29, 35, 56]
assert latest['current_membership_confirmed_for_all_departments'] is True
assert latest['resolved_zero_delta'] is True
assert latest['new_unique_rf_memory_count'] == 0
assert latest['candidate_memory_delta'] == 0
assert latest['candidate_memory_count_after_review'] == 151
assert latest['department29_current_public_role_frequency_validated'] is True
assert latest['department29_frequency_mhz'] == 144.8
assert latest['department29_frequency_already_present_nationally'] is True
assert latest['department35_f1zug_adrasec_transponder_frequency_published'] is False
assert latest['department56_service_specific_adrasec_frequency_promoted'] is False
assert latest['private_ppdr_operational_data_excluded'] is True

assert PLAN['current_candidate_memory_count'] == 151
assert PLAN['current_new_memory_count'] == 16
assert PLAN['public_export_allowed'] is False
assert PLAN['public_registry_allowed'] is False

print('Sprint 77 Bretagne ADRASEC public revalidation: 4 memberships confirmed, public RF evidence deduplicated, delta 0, private operational data excluded OK')
