#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "research/bretagne-v0.3/airac09-handoff.json"
PUBLIC = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"
PUBLIC_V03 = ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.3.csv"

data = json.loads(HANDOFF.read_text(encoding="utf-8"))
assert data["status"] == "airac09_future_handoff_prepared"
assert data["current_cycle"]["id"] == "AIRAC 08/26"
assert data["current_cycle"]["effective_until_inclusive"] == "2026-09-02"
assert data["next_required_cycle"]["id"] == "AIRAC 09/26"
assert data["next_required_cycle"]["effective_from"] == "2026-09-03"
assert data["next_required_cycle"]["must_not_be_treated_as_current_before"] == "2026-09-03"
assert data["candidate_memory_count"] == 151 and data["candidate_memory_delta"] == 0
assert data["publication_allowed_before_airac09_revalidation"] is False
assert data["rules"]["future_airac_not_current_evidence"] is True
assert data["rules"]["private_or_unpublished_rf_inferred"] is False
assert len(data["open_non_airac_dossiers"]) == 6
assert not PUBLIC_V03.exists()
assert hashlib.sha256(PUBLIC.read_bytes()).hexdigest() == "73aa3d530ae9f6c572eb01794b0861ecba61df0faf7884ee766085d3de7601a4"
print("Sprint 91 Bretagne v0.3 AIRAC09 handoff: current 08/26 through 2026-09-02; future 09/26 gated to 2026-09-03; candidate 151, no publication OK")
