import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
state=json.loads((ROOT/'research/project-resume-state.json').read_text(encoding='utf-8'))
scope=json.loads((ROOT/'research/bretagne-v0.1/release-scope.json').read_text(encoding='utf-8'))
assert state['current_sprint']>=72 and state['state_version']>='0.21.61'
historical_v01=state.get('completed_bretagne_v0_1_release')
if historical_v01 is None:
    historical_v01=state['active_work']
    assert historical_v01['pack']=='Bretagne' and historical_v01['target_version']=='0.1'
    assert historical_v01['internal_candidate_memory_count']==135
    assert historical_v01['prepublication_ready'] is True
    assert historical_v01['public_export_allowed'] is False and historical_v01['public_release_ready'] is False
else:
    assert historical_v01['pack']=='Bretagne' and historical_v01['version']=='0.1'
    assert historical_v01['memory_count']==135 and historical_v01['immutable'] is True
    assert historical_v01['review_completed']==8 and historical_v01['review_total']==8
    assert historical_v01['review_blocker_count']==0
assert scope['status']=='scope_frozen_135_prepublication_not_public' and scope['final_candidate_memory_count']==135
assert scope['prepublication_ready'] is True and scope['public_export_allowed'] is False
assert scope['included']['channel64_pair_mhz']==[156.225,160.825]
assert scope['included']['channel79_pair_mhz']==[156.975,161.575]
assert scope['rules']['explicit_publication_is_separate_step'] is True
if state['current_sprint'] == 72:
    assert state['public_packs']['bretagne']['research_only'] is True and state['public_packs']['bretagne']['memory_count']==0
elif state['current_sprint'] < 80:
    assert state['public_packs']['bretagne']['immutable'] is True and state['public_packs']['bretagne']['memory_count']==135
else:
    assert state['public_packs']['bretagne']['immutable'] is True
    assert state['public_packs']['bretagne']['version']=='0.2' and state['public_packs']['bretagne']['memory_count']==151
    assert state['public_packs']['bretagne']['previous_immutable_version']=='0.1'
    assert state['public_packs']['bretagne']['previous_memory_count']==135
print('Sprint 72: Bretagne v0.1 scope frozen at 135 remains auditable after explicit v0.2 publication OK')
