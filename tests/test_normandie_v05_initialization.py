import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
plan = json.loads((ROOT / 'research/normandie-v0.5/pack-plan.json').read_text(encoding='utf-8'))
backlog = json.loads((ROOT / 'research/normandie-v0.5/backlog.json').read_text(encoding='utf-8'))
record = json.loads((ROOT / 'research/normandie-v0.4/publication-record.json').read_text(encoding='utf-8'))

# Sprint 70 invariant: v0.5 was created from immutable public v0.4=142.
# Later sprints may legitimately advance the current candidate without rewriting that base.
assert plan['target_version'] == '0.5' and plan['based_on_published_version'] == '0.4'
assert plan['published_base_memory_count'] == 142 and plan['published_base_is_immutable'] is True
assert record['status'] == 'published_immutable'
assert record['version'] == '0.4' and record['memory_count'] == 142
assert record['public_csv_sha256'] == plan['published_base_sha256']
assert plan['public_export_allowed'] is False and plan['public_registry_allowed'] is False

if plan['status'] == 'research_next_version_not_public':
    assert plan['current_candidate_memory_count'] == 142 and plan['current_new_memory_count'] == 0
else:
    assert plan['status'] == 'research_next_version_theoretical_candidate_not_public'
    assert plan['current_candidate_memory_count'] == 146 and plan['current_new_memory_count'] == 4
    assert plan['last_revalidation_sprint'] == 112
    assert plan['rules']['theoretical_coverage_may_close_coverage_gate'] is True
    assert plan['rules']['field_reception_required_for_candidate_promotion'] is False
    assert plan['rules']['theory_is_not_measured_reception'] is True

items = {x['id']: x for x in backlog['items']}
assert set(items) == {'R3_MORTAIN_RX', 'F5ZHA_SOURCE_AND_COVERAGE', 'F1ZOV_OPERATIONAL_STATUS', 'F6ZES_RESOLVED'}
assert items['R3_MORTAIN_RX']['frequencies_mhz'] == [145.075, 145.675]
assert items['R3_MORTAIN_RX']['potential_memory_delta'] == 2
assert items['F5ZHA_SOURCE_AND_COVERAGE']['frequencies_mhz'] == [145.4675, 432.575]
assert items['F5ZHA_SOURCE_AND_COVERAGE']['potential_memory_delta'] == 2
assert items['F1ZOV_OPERATIONAL_STATUS']['frequencies_mhz'] == [431.975]
assert items['F1ZOV_OPERATIONAL_STATUS']['potential_memory_delta'] == 1
assert items['F1ZOV_OPERATIONAL_STATUS']['local_operator_status'] == 'maintenance'
assert items['F6ZES_RESOLVED']['frequencies_mhz'] == []
assert items['F6ZES_RESOLVED']['potential_memory_delta'] is None
assert items['F6ZES_RESOLVED']['must_not_guess'] is True
assert backlog['rules']['deferred_item_is_not_validated'] is True
assert backlog['rules']['rx_only'] is True
assert backlog['rules']['chirp_duplex'] == 'off' and backlog['rules']['chirp_offset'] == '0.000000'

print('Sprint 70 historical initialization guard: Normandie v0.5 remains based on immutable public v0.4=142; later theoretical candidate evolution is allowed OK')
