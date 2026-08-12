import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
state=json.loads((ROOT/'research/project-resume-state.json').read_text(encoding='utf-8'))
scope=json.loads((ROOT/'research/bretagne-v0.1/release-scope.json').read_text(encoding='utf-8'))
assert state['current_sprint']==72 and state['state_version']=='0.21.61'
assert state['active_work']['pack']=='Bretagne' and state['active_work']['target_version']=='0.1'
assert state['active_work']['internal_candidate_memory_count']==135
assert state['active_work']['prepublication_ready'] is True
assert state['active_work']['public_export_allowed'] is False and state['active_work']['public_release_ready'] is False
assert scope['status']=='scope_frozen_135_prepublication_not_public' and scope['final_candidate_memory_count']==135
assert scope['included']['channel64_pair_mhz']==[156.225,160.825]
assert scope['included']['channel79_pair_mhz']==[156.975,161.575]
assert scope['rules']['explicit_publication_is_separate_step'] is True
assert state['public_packs']['bretagne']['research_only'] is True and state['public_packs']['bretagne']['memory_count']==0
print('Sprint 72: Bretagne v0.1 scope frozen at 135, prepublication ready 8/8 with zero blockers, public publication remains explicit and separate OK')
