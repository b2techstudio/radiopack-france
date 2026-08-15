#!/usr/bin/env python3
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "research/normandie-v0.5/sprint90-source-refresh.json"
PUBLIC = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv"
PUBLIC_V05 = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.5.csv"

data = json.loads(EVIDENCE.read_text(encoding="utf-8"))
assert data["status"] == "current_sources_refreshed_zero_delta"
assert data["candidate_memory_count_before"] == 142
assert data["candidate_memory_count_after"] == 142
assert data["candidate_memory_delta"] == 0
assert data["promotion_count"] == 0
assert data["known_potential_ceiling_excluding_f6zes"] == 147
by_id = {item["id"]: item for item in data["dossiers"]}
assert by_id["R3_F1ZBX"]["status"] == "field_validation_required"
assert by_id["F5ZHA"]["status"] == "field_validation_required"
assert by_id["F1ZOV"]["status"] == "operator_local_maintenance"
assert by_id["F6ZES"]["frequency_mhz"] is None and by_id["F6ZES"]["mode"] is None
assert data["rules"]["field_gates_not_closed_by_web"] is True
assert data["rules"]["no_frequency_inference"] is True
assert not PUBLIC_V05.exists()
assert hashlib.sha256(PUBLIC.read_bytes()).hexdigest() == "3da26f18cefbf7ec1dfb6a991101d07f6a8ce9fb921015a7202870fc9b9db66d"
with PUBLIC.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 142
assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in rows)
print("Sprint 90 Normandie v0.5 source refresh: 142 RX, delta 0; R3/F5ZHA field-only; F1ZOV maintenance; F6ZES unresolved OK")
