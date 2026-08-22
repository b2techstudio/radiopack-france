#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "research/project-resume-state.json"
EXPECTED_SHA = "14e1d1d95b38ef44d01b9cccb989a3f1567153ac64875594cc24bd4b57a1cdc2"
V03_SHA = "e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125"

state = json.loads(STATE.read_text(encoding="utf-8"))
assert state["updated"] == "2026-08-22"
assert state["current_sprint"] >= 105

# Sprint 105 is a frozen historical checkpoint. Later sprints may replace
# active_work, advance the state version and publish another regional pack.
current = state["public_packs"]["ile_de_france"]
assert current["version"] == "0.4"
assert current["memory_count"] == 64
assert current["immutable"] is True
assert current["previous_immutable_version"] == "0.3"
assert current["previous_memory_count"] == 57
assert current["publication_record"] == "research/ile-de-france-v0.4/publication-record.json"
assert current["public_csv_sha256"] == EXPECTED_SHA

s105 = state["latest_sprint105_idf_v04_publication"]
assert s105["sprint"] == 105
assert s105["state_version"] == "0.21.93"
assert s105["status"] == "idf_v04_published_immutable"
assert s105["memory_count"] == 64
assert s105["previous_public_version"] == "0.3"
assert s105["previous_memory_count"] == 57
assert s105["aviation_memory_count"] == 18
assert s105["aviation_memory_delta"] == 0
assert s105["regional_radio_memory_count"] == 15
assert s105["regional_radio_memory_delta"] == 0
assert s105["inland_vhf_memory_count"] == 7
assert s105["inland_vhf_memory_delta"] == 7
assert s105["inland_channels"] == [10, 18, 20, 22]
assert s105["channel_69_promoted"] is False
assert s105["public_csv_sha256"] == EXPECTED_SHA
assert s105["published"] is True
assert s105["published_version_is_immutable"] is True

s104 = state["latest_sprint104_grand_est_v04_publication"]
assert s104["status"] == "grand_est_v04_published_immutable"
assert s104["memory_count"] == 97

rules = state["resume_rules"]
assert rules["inland_navigation_vhf_is_distinct_from_marine_vhf"] is True
assert rules["shared_inland_marine_rf_must_not_be_duplicated"] is True
assert rules["undocumented_local_navigation_channel_must_not_be_guessed"] is True
assert rules["temporary_navigation_channel_requires_current_evidence_before_promotion"] is True

record = json.loads((ROOT / "research/ile-de-france-v0.4/publication-record.json").read_text(encoding="utf-8"))
assert record["status"] == "published_immutable"
assert record["version"] == "0.4"
assert record["memory_count"] == 64
assert record["previous_public_version"] == "0.3"
assert record["previous_public_memory_count"] == 57
assert record["public_csv_sha256"] == EXPECTED_SHA
assert record["published_version_is_immutable"] is True

v03_record = json.loads((ROOT / "research/ile-de-france-v0.3/publication-record.json").read_text(encoding="utf-8"))
assert v03_record["status"] == "published_immutable"
assert v03_record["version"] == "0.3"
assert v03_record["memory_count"] == 57
assert v03_record["public_csv_sha256"] == V03_SHA

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert '{ id: "ile-de-france", name: "Île-de-France", memoryCount: 64, marine: false, aviation: 18, version: "v0.4" }' in registry

regions = json.loads((ROOT / "website/src/data/regions.json").read_text(encoding="utf-8"))
idf = next(item for item in regions if item["slug"] == "ile-de-france")
assert idf["memoryCount"] == 64 and idf["status"] == "v0.4 disponible"

readme = (ROOT / "README.md").read_text(encoding="utf-8")
assert "**Île-de-France v0.4** — 64 mémoires RX" in readme
assert "## Sprint 105" in readme
assert "## Sprint 104" in readme

status = (ROOT / "PROJECT_STATUS.md").read_text(encoding="utf-8")
assert "Île-de-France v0.4" in status and "64" in status

summary = (ROOT / "research/sprint-105-summary.md").read_text(encoding="utf-8")
assert "64 mémoires RX" in summary
assert "+7 mémoires VHF de navigation intérieure" in summary
assert EXPECTED_SHA in summary

assert state["recent_sprints"][0]["sprint"] >= 105

print("Sprint 105 historical guard: IDF v0.4 / 64 RX / +7 inland VHF remains immutable after later state advances OK")
