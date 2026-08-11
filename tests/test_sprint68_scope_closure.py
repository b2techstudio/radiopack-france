import csv, importlib.util, io, json
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def mod(name,path):
    s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
scope=json.loads((ROOT/'research/normandie-v0.4/release-scope.json').read_text(encoding='utf-8'))
plan=json.loads((ROOT/'research/normandie-v0.4/pack-plan.json').read_text(encoding='utf-8'))
assert scope['final_memory_count']==142 and scope['final_positions_assigned'] is True
assert scope['deferred_gate_ids']==['R3_MORTAIN_RX','F5ZHA_SOURCE_AND_COVERAGE','F1ZOV_OPERATIONAL_STATUS','F6ZES_RESOLVED']
assert all(x is True for x in scope['rules'].values() if isinstance(x,bool))
assert plan['memory_plan']['expected_memory_count']==142 and plan['memory_plan']['memory_positions_assigned'] is True
check=mod('check',ROOT/'tools/build_normandie_v04_review_checklist.py').build(ROOT,date(2026,8,11))
block=mod('block',ROOT/'tools/build_normandie_v04_release_blockers.py').build(ROOT)
audit=mod('audit',ROOT/'tools/run_normandie_v04_prepublication_audit.py').build(ROOT,date(2026,8,11))
candidate_manifest,candidate_bytes=mod('candidate',ROOT/'tools/build_normandie_v04_internal_candidate.py').build_candidate(ROOT)
rows=list(csv.DictReader(io.StringIO(candidate_bytes.decode('utf-8'))))
assert candidate_manifest['memory_count']==142 and len(rows)==142
assert check['completed_count']==9 and check['blocking_open_count']==0 and check['release_review_complete'] is True
assert block['blocking_count']==0 and block['prepublication_ready'] is True

dry=mod('dry',ROOT/'tools/run_normandie_v04_publication_dry_run.py').build(ROOT,ROOT/'research/normandie-v0.4/review-baseline.json',date(2026,8,11))
assert dry['publication_completed'] is True and dry['activation_ready'] is False
assert set(dry['activation_blockers'])=={'REVIEW_DRIFT_DETECTED','PUBLICATION_ALREADY_COMPLETED'}
assert audit['integrity_ok'] is True and audit['review_completed_count']==9 and audit['review_blocking_open_count']==0 and audit['release_blocking_count']==0 and audit['prepublication_ready'] is True
assert (ROOT/'website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv').exists()
assert 'version: "v0.4"' in (ROOT/'website/src/lib/packRegistry.ts').read_text(encoding='utf-8')
for f in [145.075,145.675,145.4675,432.575,431.975]: assert all(abs(float(r['Frequency'])-f)>1e-9 for r in rows)
print('Sprint 68 scope closure replay: 142 frozen, 4 unresolved dossiers deferred to v0.5, 9/9, zero blockers; later publication is recorded and cannot be reactivated, OK')
