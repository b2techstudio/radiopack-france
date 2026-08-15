#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
required = [
    "research/annecy-alpes-leman-v0.4/compatibility-and-source-review.json",
    "tools/build_annecy_v04_candidate.py",
    "tests/test_sprint89_annecy_v04_candidate.py",
    "research/normandie-v0.5/sprint90-source-refresh.json",
    "tests/test_sprint90_normandie_v05_source_refresh.py",
    "research/bretagne-v0.3/airac09-handoff.json",
    "tests/test_sprint91_bretagne_airac09_handoff.py",
    "research/sprint-89-summary.md",
    "research/sprint-90-summary.md",
    "research/sprint-91-summary.md",
    "README.md",
    "PROJECT_STATUS.md",
    "CHANGELOG.md",
    "research/project-resume-state.json",
]
for relative in required:
    path = ROOT / relative
    assert path.is_file(), f"Missing sprints89-91 file: {relative}"
    assert path.stat().st_size > 20, f"Incomplete sprints89-91 file: {relative}"

state = json.loads((ROOT / "research/project-resume-state.json").read_text(encoding="utf-8"))
# This is a historical integrity guard for Sprints 89-91. Later sprints may advance
# the project head, but they must preserve the 89-91 decisions and public releases.
assert state["current_sprint"] >= 91
version_parts = tuple(int(part) for part in state["state_version"].split("."))
assert version_parts >= (0, 21, 80)
assert state["public_packs"]["annecy_alpes_leman"]["version"] == "0.3"
assert state["public_packs"]["annecy_alpes_leman"]["memory_count"] == 76
assert state["annecy_v0_4_research"]["candidate_memory_count"] == 77
assert state["annecy_v0_4_research"]["candidate_without_aviation_memory_count"] == 60
assert state["annecy_v0_4_research"]["published"] is False
assert state["normandie_v0_5_latest_refresh"]["candidate_memory_count"] == 142
assert state["normandie_v0_5_latest_refresh"]["candidate_memory_delta"] == 0
assert state["active_work"]["pack"] == "Bretagne"
assert state["active_work"]["candidate_memory_count"] == 151
assert state["active_work"]["airac_next_effective_from"] == "2026-09-03"
assert state["active_work"]["publication_allowed_before_airac09_revalidation"] is False

project = (ROOT / "PROJECT_STATUS.md").read_text(encoding="utf-8")
assert f'Sprint courant : **{state["current_sprint"]}**' in project
assert f'État logique : **{state["state_version"]}**' in project
assert "Annecy–Alpes–Léman v0.3 : **76 mémoires RX**" in project
assert "Annecy–Alpes–Léman v0.2 : 65 mémoires RX, variante 48 sans aviation." not in project
assert "## Sprint 91 —" in project
assert "## Sprint 90 —" in project
assert "## Sprint 89 —" in project

readme = (ROOT / "README.md").read_text(encoding="utf-8")
assert f'Sprint {state["current_sprint"]} / {state["state_version"]}' in readme
assert "Annecy v0.4 = 77 RX / 60 sans aviation" in readme
assert "Normandie v0.5 reste à **142 RX**" in readme
assert "Bretagne v0.3 reste à **151 RX**" in readme
assert "## Sprint 91 —" in readme
assert "## Sprint 90 —" in readme
assert "## Sprint 89 —" in readme

print("Sprints 89-91 integrity: historical decisions preserved across later project-state advances; public releases unchanged and future/field gates preserved OK")
