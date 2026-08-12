#!/usr/bin/env python3
"""Audit frozen Bretagne v0.1 candidate; never writes public files."""
from __future__ import annotations
import argparse, csv, json, subprocess, sys, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument('--root',type=Path,default=ROOT); p.add_argument('--require-prepublication-ready',action='store_true'); a=p.parse_args(); root=a.root.resolve()
    r=root/'research/bretagne-v0.1'
    checklist=json.loads((r/'review-checklist.json').read_text(encoding='utf-8')); scope=json.loads((r/'release-scope.json').read_text(encoding='utf-8')); gates=json.loads((r/'publication-gates.json').read_text(encoding='utf-8')); sia=json.loads((r/'sia-airac-08-review.json').read_text(encoding='utf-8'))
    errors=[]
    if checklist['completed']!=8 or checklist['total']!=8 or checklist['blocker_count']!=0: errors.append('review checklist incomplete')
    if scope['final_candidate_memory_count']!=135: errors.append('scope memory count not 135')
    if gates['public_release_allowed'] is not False: errors.append('public release unexpectedly allowed')
    if sia['decision']['aviation_memory_count_v0_1']!=0: errors.append('aviation unexpectedly promoted')
    with tempfile.TemporaryDirectory() as td:
        temp=Path(td); subprocess.run([sys.executable,str(root/'tools/build_bretagne_internal_candidate.py'),'--root',str(root),'--output-dir',str(temp)],check=True,stdout=subprocess.DEVNULL)
        with (temp/'bretagne-v0.1-internal.csv').open(encoding='utf-8',newline='') as h: rows=list(csv.DictReader(h))
        if len(rows)!=135: errors.append('candidate row count mismatch')
        if any(x['Duplex']!='off' or x['Offset']!='0.000000' for x in rows): errors.append('RX-only CHIRP contract broken')
        if len({float(x['Frequency']) for x in rows})!=135: errors.append('duplicate RF in candidate')
        names={x['Name']:x for x in rows}
        expected={'M64-S':156.225,'M64-C':160.825,'M79-S':156.975,'M79-C':161.575}
        for n,f in expected.items():
            if n not in names or float(names[n]['Frequency'])!=f: errors.append(f'missing {n}')
            elif any(site in names[n]['Comment'].lower() for site in ['etel','corsen','fréhel','stiff','bodic']): errors.append(f'unproven site claim in {n}')
    registry=(root/'website/src/lib/packRegistry.ts').read_text(encoding='utf-8').lower()
    if 'id: "bretagne"' in registry or (root/'website/public/downloads/bretagne').exists(): errors.append('Bretagne public mutation detected')
    ready=not errors and checklist['prepublication_ready'] is True and scope['prepublication_ready'] is True
    result={'schema_version':'1.0','status':'prepublication_audit_not_public','memory_count':135,'review':'8/8','blocker_count':len(errors),'errors':errors,'prepublication_ready':ready,'public_export_allowed':False}
    out=r/'generated/prepublication-audit'; out.mkdir(parents=True,exist_ok=True); (out/'bretagne-v01-prepublication-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"BRETAGNE V0.1 PREPUBLICATION AUDIT: integrity={'OK' if not errors else 'FAIL'} review=8/8 blockers={len(errors)} prepublication_ready={str(ready).lower()}")
    if errors or (a.require_prepublication_ready and not ready): raise SystemExit(1)
if __name__=='__main__': main()
