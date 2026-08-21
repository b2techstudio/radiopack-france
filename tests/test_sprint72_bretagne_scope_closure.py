import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
state=json.loads((ROOT/'research/project-resume-state.json').read_text(encoding='utf-8'))
scope=json.loads((ROOT/'research/bretagne-v0.1/release-scope.json').read_text(encoding='utf-8'))
record=json.loads((ROOT/'research/bretagne-v0.1/publication-record.json').read_text(encoding='utf-8'))
review=json.loads((ROOT/'research/bretagne-v0.1/review-checklist.json').read_text(encoding='utf-8'))
assert state['current_sprint']>=72 and state['state_version']>='0.21.61'
assert record['pack']=='Bretagne' and record['version']=='0.1'
assert record['memory_count']==135 and record['published_version_is_immutable'] is True
assert review['completed']==8 and review['total']==8 and review['blocker_count']==0
assert scope['status']=='scope_frozen_135_prepublication_not_public' and scope['final_candidate_memory_count']==135
assert scope['prepublication_ready'] is True and scope['public_export_allowed'] is False
assert scope['included']['channel64_pair_mhz']==[156.225,160.825]
assert scope['included']['channel79_pair_mhz']==[156.975,161.575]
assert scope['rules']['explicit_publication_is_separate_step'] is True
current=state['public_packs']['bretagne']
assert current['immutable'] is True
assert current['version']=='0.2' and current['memory_count']==151
assert current['previous_immutable_version']=='0.1' and current['previous_memory_count']==135
print('Sprint 72: Bretagne v0.1 scope frozen at 135 remains auditable from immutable artifacts after explicit v0.2 publication OK')
