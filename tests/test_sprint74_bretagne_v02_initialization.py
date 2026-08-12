import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = json.loads((ROOT / 'research/bretagne-v0.2/pack-plan.json').read_text(encoding='utf-8'))
BACKLOG = json.loads((ROOT / 'research/bretagne-v0.2/backlog.json').read_text(encoding='utf-8'))

assert PLAN['target_version'] == '0.2'
assert PLAN['based_on_published_version'] == '0.1'
assert PLAN['published_base_memory_count'] == 135
assert PLAN['published_base_is_immutable'] is True
assert PLAN['current_candidate_memory_count'] >= 135
assert PLAN['current_new_memory_count'] == PLAN['current_candidate_memory_count'] - 135
assert PLAN['public_export_allowed'] is False
assert PLAN['public_registry_allowed'] is False
assert PLAN['inherited_generic_maritime_pairs']['channel64_present_in_published_base'] is True
assert PLAN['inherited_generic_maritime_pairs']['channel79_present_in_published_base'] is True
assert PLAN['inherited_generic_maritime_pairs']['new_rf_memory_delta'] == 0

items = {item['id']: item for item in BACKLOG['items']}
assert set(items) == {
    'AVIATION_CURRENT_SOURCE_EXTRACT',
    'ADRASEC_PUBLIC_DATA_REVALIDATION',
    'F1ZUG_ADRASEC35_ROLE_REVALIDATION',
    'CROSS_ETEL_CH64_LOCAL_MAPPING',
    'CROSS_CORSEN_CH79_LOCAL_MAPPING',
    'AMATEUR_INFRASTRUCTURE_REVALIDATION',
}

aviation = items['AVIATION_CURRENT_SOURCE_EXTRACT']
assert aviation['current_cycle_at_initialization'] == 'AIRAC 08/26'
assert aviation['valid_from'] == '2026-08-06'
assert aviation['valid_through'] == '2026-09-02'
assert aviation['promoted'] is False
if PLAN['current_candidate_memory_count'] == 135:
    assert PLAN['current_new_memory_count'] == 0
    assert aviation['potential_memory_delta'] is None
else:
    assert PLAN['current_candidate_memory_count'] == 151
    assert PLAN['current_new_memory_count'] == 16
    assert aviation['potential_memory_delta'] == 16
    assert aviation['internal_candidate_memory_delta'] == 16
    assert aviation['internal_candidate_promoted'] is True
    assert aviation['public_promotion'] is False

adrasec = items['ADRASEC_PUBLIC_DATA_REVALIDATION']
assert adrasec['departments'] == [22, 29, 35, 56]
assert adrasec['potential_memory_delta'] is None
assert adrasec['promoted'] is False

f1zug = items['F1ZUG_ADRASEC35_ROLE_REVALIDATION']
assert f1zug['must_not_infer_from_aprs'] is True
assert f1zug['potential_memory_delta'] is None
assert f1zug['promoted'] is False

for item_id in ('CROSS_ETEL_CH64_LOCAL_MAPPING', 'CROSS_CORSEN_CH79_LOCAL_MAPPING'):
    item = items[item_id]
    assert item['generic_memory_already_present_in_published_base'] is True
    assert item['potential_new_rf_memory_delta'] == 0
    assert item['promoted_local_site_mapping'] is False

amateur = items['AMATEUR_INFRASTRUCTURE_REVALIDATION']
if 'reviewed_ids' in amateur:
    assert set(amateur['reviewed_ids']) == {'F5ZPV', 'F5ZZH', 'F1ZBZ', 'F5ZZC-4'}
    assert set(amateur['resolved_zero_delta_ids']) == {'F1ZBZ'}
    assert set(amateur['priority_ids']) == {'F5ZPV', 'F5ZZH', 'F5ZZC-4'}
    assert amateur['potential_memory_delta'] == 0
    assert amateur['candidate_memory_delta'] == 0
else:
    assert set(amateur['priority_ids']) == {'F5ZPV', 'F5ZZH', 'F1ZBZ', 'F5ZZC-4'}
    assert amateur['potential_memory_delta'] is None
assert amateur['promoted'] is False

assert BACKLOG['rules']['deferred_item_is_not_validated'] is True
assert BACKLOG['rules']['published_base_is_immutable'] is True
assert BACKLOG['rules']['rx_only'] is True
assert BACKLOG['rules']['unpublished_data_must_not_be_inferred'] is True
assert BACKLOG['rules']['private_ppdr_operational_data_excluded'] is True
assert BACKLOG['rules']['public_export_allowed'] is False

print('Sprint 74 Bretagne v0.2 initialization remains auditable from immutable public v0.1=135 while later internal candidate and backlog revalidations remain non-public OK')
