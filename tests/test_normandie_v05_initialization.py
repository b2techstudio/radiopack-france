import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
plan=json.loads((ROOT/'research/normandie-v0.5/pack-plan.json').read_text(encoding='utf-8'))
backlog=json.loads((ROOT/'research/normandie-v0.5/backlog.json').read_text(encoding='utf-8'))
assert plan['status']=='research_next_version_not_public'
assert plan['target_version']=='0.5' and plan['based_on_published_version']=='0.4'
assert plan['published_base_memory_count']==142 and plan['published_base_is_immutable'] is True
assert plan['current_candidate_memory_count']==142 and plan['current_new_memory_count']==0
assert plan['public_export_allowed'] is False and plan['public_registry_allowed'] is False
items={x['id']:x for x in backlog['items']}
assert set(items)=={'R3_MORTAIN_RX','F5ZHA_SOURCE_AND_COVERAGE','F1ZOV_OPERATIONAL_STATUS','F6ZES_RESOLVED'}
assert items['R3_MORTAIN_RX']['frequencies_mhz']==[145.075,145.675] and items['R3_MORTAIN_RX']['potential_memory_delta']==2
assert items['R3_MORTAIN_RX']['sessions_are_evidence_not_memories'] is True
assert items['F5ZHA_SOURCE_AND_COVERAGE']['frequencies_mhz']==[145.4675,432.575] and items['F5ZHA_SOURCE_AND_COVERAGE']['potential_memory_delta']==2
assert items['F5ZHA_SOURCE_AND_COVERAGE']['field_observations_can_close_source_conflict'] is False
assert items['F1ZOV_OPERATIONAL_STATUS']['frequencies_mhz']==[431.975] and items['F1ZOV_OPERATIONAL_STATUS']['potential_memory_delta']==1
assert items['F6ZES_RESOLVED']['frequencies_mhz']==[] and items['F6ZES_RESOLVED']['potential_memory_delta'] is None and items['F6ZES_RESOLVED']['must_not_guess'] is True
assert backlog['rules']['deferred_item_is_not_validated'] is True
assert backlog['rules']['rx_only'] is True and backlog['rules']['chirp_duplex']=='off' and backlog['rules']['chirp_offset']=='0.000000'
print('Normandie v0.5 initialized from immutable public v0.4=142 with four unvalidated deferred dossiers OK')
