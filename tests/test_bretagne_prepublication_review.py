import json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; R=ROOT/'research/bretagne-v0.1'
check=json.loads((R/'review-checklist.json').read_text(encoding='utf-8')); scope=json.loads((R/'release-scope.json').read_text(encoding='utf-8')); gates=json.loads((R/'publication-gates.json').read_text(encoding='utf-8')); sia=json.loads((R/'sia-airac-08-review.json').read_text(encoding='utf-8'))
assert (check['completed'],check['total'],check['blocker_count'])==(8,8,0)
assert check['prepublication_ready'] is True and check['public_export_allowed'] is False
assert scope['final_candidate_memory_count']==135 and scope['prepublication_ready'] is True and scope['public_export_allowed'] is False
assert {x['id'] for x in scope['deferred_to_v0_2']}=={'AVIATION_CURRENT_SIA','ADRASEC_UNPUBLISHED_OPERATIONAL_FREQUENCIES','CROSS_LOCAL_TRANSMITTER_SITE_MAPPING','STOPPED_OR_UNRESOLVED_AMATEUR_INFRASTRUCTURE'}
assert gates['status']=='prepublication_ready_135_explicit_publication_pending' and gates['public_release_allowed'] is False
assert all(g['status'].startswith('passed_') or g['id']=='explicit_publication' for g in gates['gates'])
assert sia['current_cycle']['valid_from']=='2026-08-06' and sia['current_cycle']['valid_through']=='2026-09-02'
assert sia['current_cycle']['exact_export_extracted_in_repository_workflow'] is False
assert sia['decision']['aviation_memory_count_v0_1']==0 and sia['decision']['defer_to_v0_2'] is True
with tempfile.TemporaryDirectory() as td:
    subprocess.run([sys.executable,str(ROOT/'tools/build_bretagne_review_snapshot.py'),'--root',str(ROOT),'--output-dir',td],check=True)
    snap=json.loads((Path(td)/'bretagne-v01-review-snapshot.json').read_text(encoding='utf-8'))
assert snap['memory_count']==135 and snap['review_completed']==8 and snap['review_total']==8 and snap['blocker_count']==0 and snap['prepublication_ready'] is True
subprocess.run([sys.executable,str(ROOT/'tools/run_bretagne_prepublication_audit.py'),'--root',str(ROOT),'--require-prepublication-ready'],check=True)
assert 'id: "bretagne"' not in (ROOT/'website/src/lib/packRegistry.ts').read_text(encoding='utf-8').lower()
print('Bretagne v0.1 prepublication review: frozen 135 RX memories, review 8/8, zero blockers, aviation/ADRASEC/site metadata deferred, public untouched OK')
