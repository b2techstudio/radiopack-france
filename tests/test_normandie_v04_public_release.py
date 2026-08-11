import csv
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv'
BASE = ROOT / 'website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv'
RECORD = ROOT / 'research/normandie-v0.4/publication-record.json'
REGISTRY = ROOT / 'website/src/lib/packRegistry.ts'

spec = importlib.util.spec_from_file_location('normandie_builder', ROOT / 'tools/build_normandie_v04_internal_candidate.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
manifest, candidate = mod.build_candidate(ROOT)
assert PUBLIC.read_bytes() == candidate
assert manifest['memory_count'] == 142
with PUBLIC.open(encoding='utf-8', newline='') as f: rows=list(csv.DictReader(f))
assert len(rows)==142
assert all(r['Duplex']=='off' and r['Offset']=='0.000000' for r in rows)
assert all(len(r['Name']) <= 10 for r in rows)
assert len({r['Location'] for r in rows})==142
assert len({r['Name'] for r in rows})==142
freqs={round(float(r['Frequency']),6) for r in rows}
for blocked in [145.075,145.675,145.4675,432.575,431.975]: assert blocked not in freqs
record=json.loads(RECORD.read_text(encoding='utf-8'))
assert record['status']=='published_immutable' and record['version']=='0.4' and record['memory_count']==142
assert record['public_csv_sha256']==hashlib.sha256(PUBLIC.read_bytes()).hexdigest()
assert record['base_csv_sha256']==hashlib.sha256(BASE.read_bytes()).hexdigest()
assert record['base_memory_count']==139 and record['published_version_is_immutable'] is True
registry=REGISTRY.read_text(encoding='utf-8')
assert 'version: "v0.4"' in registry and 'memoryCount: 142' in registry
assert '/downloads/normandie/radiopack-france-normandie-v0.4.csv' in registry
print('Normandie v0.4 public release: immutable 142-memory RX-only CSV exactly matches reviewed candidate OK')
