#!/usr/bin/env python3
"""Build deterministic Bretagne v0.1 review snapshot without publishing files."""
from __future__ import annotations
import argparse, hashlib, json, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path, default=ROOT)
    p.add_argument('--output-dir', type=Path, default=Path('research/bretagne-v0.1/generated/review-snapshot'))
    a = p.parse_args(); root=a.root.resolve(); out=a.output_dir
    if not out.is_absolute(): out=root/out
    with tempfile.TemporaryDirectory() as td:
        temp=Path(td)
        subprocess.run([sys.executable, str(root/'tools/build_bretagne_internal_candidate.py'), '--root', str(root), '--output-dir', str(temp)], check=True, stdout=subprocess.DEVNULL)
        csvp=temp/'bretagne-v0.1-internal.csv'; jsonp=temp/'bretagne-v0.1-internal.json'
        candidate=json.loads(jsonp.read_text(encoding='utf-8'))
        checklist=json.loads((root/'research/bretagne-v0.1/review-checklist.json').read_text(encoding='utf-8'))
        scope=json.loads((root/'research/bretagne-v0.1/release-scope.json').read_text(encoding='utf-8'))
        snap={
          'schema_version':'1.0','status':'review_snapshot_not_public','pack':'Bretagne','version':'0.1',
          'memory_count':candidate['memory_count'],'candidate_csv_sha256':sha256(csvp),'candidate_json_sha256':sha256(jsonp),
          'review_completed':checklist['completed'],'review_total':checklist['total'],'blocker_count':checklist['blocker_count'],
          'prepublication_ready':checklist['prepublication_ready'],'public_export_allowed':False,
          'scope_status':scope['status'],'deferred_ids':[x['id'] for x in scope['deferred_to_v0_2']],
        }
        out.mkdir(parents=True, exist_ok=True)
        (out/'bretagne-v01-review-snapshot.json').write_text(json.dumps(snap,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (out/'bretagne-v01-review-snapshot.md').write_text(
          f"# Bretagne v0.1 review snapshot\n\n- Mémoires : **{snap['memory_count']}**\n- Revue : **{snap['review_completed']}/{snap['review_total']}**\n- Blocages : **{snap['blocker_count']}**\n- Prépublication prête : **{str(snap['prepublication_ready']).lower()}**\n- Public : **false**\n- SHA-256 CSV candidat : `{snap['candidate_csv_sha256']}`\n", encoding='utf-8')
        print(f"BRETAGNE V0.1 REVIEW SNAPSHOT: review={snap['review_completed']}/{snap['review_total']} blockers={snap['blocker_count']} memories={snap['memory_count']} public=false")
        print(out/'bretagne-v01-review-snapshot.json')
if __name__=='__main__': main()
