#!/usr/bin/env python3
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V03 = ROOT / "research" / "grand-est-v0.3"
CANDIDATE = V03 / "generated/release-candidate/radiopack-france-grand-est-v0.3-candidate.csv"
PUBLIC = ROOT / "website/public/downloads/grand-est/radiopack-france-grand-est-v0.3.csv"
MANIFEST = V03 / "generated/release-candidate/candidate-manifest.json"
EXPECTED_SHA = "45aef8547a701e7541e620fa9a2d8394595576921e793b75238146ff6e42e720"
BASE_SHA = "a50416bd8a88af249bb691daa657ffd4b578daf1324bd0ca4dd632a2f1a0e5c1"

subprocess.run(
    [sys.executable, str(ROOT / "tools/build_grand_est_v03_candidate.py"), "--check"],
    cwd=ROOT,
    check=True,
)

raw = CANDIDATE.read_bytes()
assert hashlib.sha256(raw).hexdigest() == EXPECTED_SHA
assert PUBLIC.read_bytes() == raw
assert hashlib.sha256(PUBLIC.read_bytes()).hexdigest() == EXPECTED_SHA

with CANDIDATE.open("r", encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))
assert len(rows) == 84
assert sum(row["Mode"] == "AM" for row in rows) == 19
regional = [row for row in rows if int(row["Location"]) >= 70]
assert len(regional) == 41
assert all(row["Duplex"] == "off" for row in rows)
assert all(row["Offset"] == "0.000000" for row in rows)

locations = [int(row["Location"]) for row in rows]
names = [row["Name"] for row in rows]
frequencies = [row["Frequency"] for row in rows]
assert len(locations) == len(set(locations))
assert len(names) == len(set(names))
assert len(frequencies) == len(set(frequencies))
assert max(locations) <= 199
assert max(map(len, names)) <= 10
assert sum(row["Frequency"] == "432.537500" for row in rows) == 1
assert any(row["Name"] == "XBD-4325" and row["Frequency"] == "432.537500" for row in rows)

# The manifest is the immutable prepublication freeze produced by the deterministic builder.
# Publication evidence lives in release-scope/publication-record and must not rewrite that history.
manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
assert manifest["status"] == "internal_candidate_radio_scope_frozen_aviation_gate_pending"
assert manifest["published_base_version"] == "0.2"
assert manifest["published_base_memory_count"] == 59
assert manifest["published_base_sha256"] == BASE_SHA
assert manifest["candidate_memory_count"] == 84
assert manifest["candidate_aviation_memory_count"] == 19
assert manifest["candidate_regional_radio_memory_count"] == 41
assert manifest["candidate_sha256"] == EXPECTED_SHA
assert manifest["validation"]["public_base_sha_matches_frozen_record"] is True
assert manifest["validation"]["rx_only"] is True
assert manifest["validation"]["rf_deduplicated"] is True
assert manifest["validation"]["radio_scope_frozen"] is True
assert manifest["public_export_allowed"] is False
assert manifest["published"] is False
assert manifest["airac09_revalidation_required_on_or_after"] == "2026-09-03"

record = json.loads((V03 / "publication-record.json").read_text(encoding="utf-8"))
assert record["status"] == "published_immutable"
assert record["public_csv_sha256"] == EXPECTED_SHA
assert record["candidate_csv_sha256"] == EXPECTED_SHA
assert record["published"] is True

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert '{ id: "grand-est", name: "Grand Est", memoryCount: 84, marine: false, aviation: 19, version: "v0.3" }' in registry

print("Sprint 102 Grand Est v0.3 deterministic basis: 84 RX / 19 aviation / 41 regional, candidate=public bytes, SHA frozen OK")
