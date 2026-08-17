#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

README = ROOT / "README.md"
PROJECT_STATUS = ROOT / "PROJECT_STATUS.md"
CHANGELOG = ROOT / "CHANGELOG.md"
STATE = ROOT / "research/project-resume-state.json"
SPRINT_SUMMARY = ROOT / "research/sprint-97-summary.md"
SPRINT_DELTA = ROOT / "research/sprint-97-post96-ui-state.json"
CI = ROOT / ".github/workflows/ci.yml"

for path in [README, PROJECT_STATUS, CHANGELOG, STATE, SPRINT_SUMMARY, SPRINT_DELTA, CI]:
    assert path.is_file(), f"Missing Sprint 97 state file: {path.relative_to(ROOT)}"
    assert path.stat().st_size > 20, f"Incomplete Sprint 97 state file: {path.relative_to(ROOT)}"

state = json.loads(STATE.read_text(encoding="utf-8"))
delta = json.loads(SPRINT_DELTA.read_text(encoding="utf-8"))
readme = README.read_text(encoding="utf-8")
project = PROJECT_STATUS.read_text(encoding="utf-8")
changelog = CHANGELOG.read_text(encoding="utf-8")
summary = SPRINT_SUMMARY.read_text(encoding="utf-8")
ci = CI.read_text(encoding="utf-8")

assert state["updated"] == "2026-08-17"
assert state["current_sprint"] == 97
assert state["state_version"] == "0.21.86"

assert "**État courant : Sprint 97 / 0.21.86" in readme
assert "## État actuel — Sprint 97 / 0.21.86" in readme
assert "## Sprint 97 —" in readme
assert "research/sprint-97-summary.md" in readme
assert "research/sprint-97-post96-ui-state.json" in readme

assert "Sprint courant : **97**" in project
assert "État logique : **0.21.86**" in project
assert "## Sprint 97 —" in project
assert "research/sprint-97-summary.md" in project
assert "research/sprint-97-post96-ui-state.json" in project

assert changelog.startswith("# Changelog\n\n## 0.21.86 - 2026-08-17")
assert "**Sprint 97**" in changelog.split("## 0.21.85", 1)[0]

assert summary.startswith("# Sprint 97 —")
assert "État logique : **0.21.86**" in summary
assert "tests/test_sprint97_state_sync.py" in summary

assert delta["status"] == "sprint97_closed_official_state_consolidation"
assert delta["sprint"] == 97
assert delta["state_version"] == "0.21.86"
assert delta["official_state_current_sprint"] == 97
assert delta["official_state_version"] == "0.21.86"
assert delta["supplements_official_state"] is True
assert delta["is_official_state_replacement"] is False
assert delta["state_sync"]["completed"] is True

public = state["public_packs"]
assert public["normandie"]["version"] == "0.4"
assert public["normandie"]["memory_count"] == 142
assert public["normandie"]["immutable"] is True
assert public["annecy_alpes_leman"]["version"] == "0.4"
assert public["annecy_alpes_leman"]["memory_count"] == 77
assert public["annecy_alpes_leman"]["without_aviation_memory_count"] == 60
assert public["annecy_alpes_leman"]["immutable"] is True
assert public["bretagne"]["version"] == "0.2"
assert public["bretagne"]["memory_count"] == 151
assert public["bretagne"]["immutable"] is True

active = state["active_work"]
assert active["pack"] == "Bretagne"
assert active["target_version"] == "0.3"
assert active["candidate_memory_count"] == 151
assert active["candidate_memory_delta"] == 0
assert active["airac_next_effective_from"] == "2026-09-03"
assert active["publication_allowed_before_airac09_revalidation"] is False

normandie = state["normandie_v0_5_latest_refresh"]
assert normandie["candidate_memory_count"] == 142
assert normandie["candidate_memory_delta"] == 0
assert normandie["known_potential_ceiling_excluding_f6zes"] == 147

sprint97 = state["latest_sprint97_state_consolidation"]
assert sprint97["sprint"] == 97
assert sprint97["state_version"] == "0.21.86"
assert sprint97["regional_channel_details_csv_backed"] is True
assert sprint97["generator_pack_shortcuts_keyboard_accessible"] is True
assert sprint97["generator_memory_counts_are_published_csv_counts"] is True
assert sprint97["public_csv_mutation"] is False
assert sprint97["rf_data_mutation"] is False

sources = set(state["sources_of_truth"])
for required in [
    "research/sprint-97-summary.md",
    "research/sprint-97-post96-ui-state.json",
    "website/src/components/ChannelGroupDetails.astro",
    "website/src/lib/channelDetails.ts",
    "website/src/scripts/generator-pack-shortcuts.js",
    "website/src/pages/generateur.astro",
    "tests/test_sprint97_state_sync.py",
]:
    assert required in sources, f"Sprint 97 source of truth missing: {required}"

assert state["recent_sprints"][0]["sprint"] == 97
assert state["recent_sprints"][0]["state_version"] == "0.21.86"
assert state["recent_sprints"][0]["summary_file"] == "research/sprint-97-summary.md"

assert "- name: Test Sprint 97 state synchronization" in ci
assert "run: python tests/test_sprint97_state_sync.py" in ci

print("Sprint 97 state sync: README, status, changelog, machine state, UX consolidation and CI guard aligned at 97 / 0.21.86 OK")
