#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
state = json.loads((ROOT / "research/project-resume-state.json").read_text(encoding="utf-8"))
readme = (ROOT / "README.md").read_text(encoding="utf-8")
project = (ROOT / "PROJECT_STATUS.md").read_text(encoding="utf-8")
changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
bfc = json.loads((ROOT / "research/bourgogne-franche-comte-v0.3/publication-record.json").read_text(encoding="utf-8"))
centre = json.loads((ROOT / "research/centre-val-de-loire-v0.3/publication-record.json").read_text(encoding="utf-8"))

# Sprint 100 is now a historical publication guard. Advancing the current
# project state must not mutate the immutable BFC/Centre publication facts.
assert state["current_sprint"] >= 100
assert "## Sprint 100 — Centre-Val de Loire v0.3" in readme
assert "## Sprint 100 — Centre-Val de Loire v0.3" in project
assert "## 0.21.89 - 2026-08-20" in changelog

pbfc = state["public_packs"]["bourgogne_franche_comte"]
assert pbfc["version"] == "0.3" and pbfc["memory_count"] == 54 and pbfc["immutable"] is True
assert pbfc["previous_immutable_version"] == "0.2" and pbfc["previous_memory_count"] == 37
assert pbfc["public_csv_sha256"] == bfc["public_csv_sha256"]
assert pbfc["publication_record"] == "research/bourgogne-franche-comte-v0.3/publication-record.json"

pcentre = state["public_packs"]["centre_val_de_loire"]
assert pcentre["version"] == "0.3" and pcentre["memory_count"] == 51 and pcentre["immutable"] is True
assert pcentre["previous_immutable_version"] == "0.2" and pcentre["previous_memory_count"] == 42
assert pcentre["public_csv_sha256"] == centre["public_csv_sha256"]
assert pcentre["publication_record"] == "research/centre-val-de-loire-v0.3/publication-record.json"

s99 = state["latest_sprint99_bfc_v03_publication"]
assert s99["sprint"] == 99 and s99["state_version"] == "0.21.88" and s99["memory_count"] == 54
assert s99["public_csv_sha256"] == bfc["public_csv_sha256"]
s100 = state["latest_sprint100_centre_v03_publication"]
assert s100["sprint"] == 100 and s100["state_version"] == "0.21.89" and s100["memory_count"] == 51
assert s100["public_csv_sha256"] == centre["public_csv_sha256"]

assert (ROOT / "research/sprint-99-summary.md").is_file()
assert (ROOT / "research/sprint-100-summary.md").is_file()
assert any(item["sprint"] == 100 and item["state_version"] == "0.21.89" for item in state["recent_sprints"])

bretagne = state.get("bretagne_v0_3_airac_handoff", state.get("active_work", {}))
assert bretagne["pack"] == "Bretagne" and bretagne["target_version"] == "0.3"
assert bretagne["candidate_memory_count"] == 151 and bretagne["candidate_memory_delta"] == 0
assert bretagne["airac_next_effective_from"] == "2026-09-03"
assert bretagne["publication_allowed_before_airac09_revalidation"] is False

normandie = state["normandie_v0_5_latest_refresh"]
assert normandie["candidate_memory_count"] == 142 and normandie["candidate_memory_delta"] == 0
assert normandie["known_potential_ceiling_excluding_f6zes"] == 147

print("Sprint 100 historical guard: BFC v0.3=54 and Centre v0.3=51 remain immutable OK")
