#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "research/project-resume-state.json"
EXPECTED_SHA = "ba34604b11b75ae7f0e7aa17e3734053ff37bbe7910218af1ab66e59f3428a5d"
V03_SHA = "45aef8547a701e7541e620fa9a2d8394595576921e793b75238146ff6e42e720"

state = json.loads(STATE.read_text(encoding="utf-8"))
assert state["current_sprint"] >= 104

# Sprint 104 is a frozen historical checkpoint; later sprints may legitimately
# replace active_work and advance other packs.
s104 = state["latest_sprint104_grand_est_v04_publication"]
assert s104["sprint"] == 104
assert s104["state_version"] == "0.21.92"
assert s104["status"] == "grand_est_v04_published_immutable"
assert s104["memory_count"] == 97
assert s104["previous_public_version"] == "0.3"
assert s104["previous_memory_count"] == 84
assert s104["aviation_memory_count"] == 19
assert s104["aviation_memory_delta"] == 0
assert s104["regional_radio_memory_count"] == 41
assert s104["inland_vhf_memory_count"] == 13
assert s104["public_csv_sha256"] == EXPECTED_SHA

rules = state["resume_rules"]
assert rules["inland_navigation_vhf_is_distinct_from_marine_vhf"] is True
assert rules["shared_inland_marine_rf_must_not_be_duplicated"] is True
assert rules["undocumented_local_navigation_channel_must_not_be_guessed"] is True

record = json.loads((ROOT / "research/grand-est-v0.4/publication-record.json").read_text(encoding="utf-8"))
assert record["status"] == "published_immutable"
assert record["version"] == "0.4"
assert record["memory_count"] == 97
assert record["previous_public_version"] == "0.3"
assert record["previous_public_memory_count"] == 84
assert record["public_csv_sha256"] == EXPECTED_SHA
assert record["published_version_is_immutable"] is True

v03_record = json.loads((ROOT / "research/grand-est-v0.3/publication-record.json").read_text(encoding="utf-8"))
assert v03_record["status"] == "published_immutable"
assert v03_record["version"] == "0.3"
assert v03_record["memory_count"] == 84
assert v03_record["public_csv_sha256"] == V03_SHA

# If Grand Est v0.4 is still current, its registry entry must remain exact.
# A future Grand Est release may advance the registry without invalidating this
# historical publication record.
registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
if 'id: "grand-est", name: "Grand Est", memoryCount: 97, marine: false, aviation: 19, version: "v0.4"' in registry:
    assert '{ id: "grand-est", name: "Grand Est", memoryCount: 97, marine: false, aviation: 19, version: "v0.4" }' in registry

readme = (ROOT / "README.md").read_text(encoding="utf-8")
assert "**Grand Est v0.4** — 97 mémoires RX" in readme
assert "## Sprint 104" in readme
assert "## Sprint 103 — audit VHF navigation intérieure" in readme

status = (ROOT / "PROJECT_STATUS.md").read_text(encoding="utf-8")
assert "Grand Est v0.4" in status and "97" in status

summary = (ROOT / "research/sprint-104-summary.md").read_text(encoding="utf-8")
assert "97 mémoires RX" in summary
assert "+13 mémoires VHF de navigation intérieure" in summary
assert EXPECTED_SHA in summary

assert state["recent_sprints"][0]["sprint"] >= 104

print("Sprint 104 historical guard: Grand Est v0.4 / 97 RX / +13 inland VHF remains immutable after later state advances OK")
