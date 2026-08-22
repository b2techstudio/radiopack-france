#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
required = [
    "research/annecy-alpes-leman-v0.4/compatibility-and-source-review.json",
    "research/annecy-alpes-leman-v0.4/publication-record.json",
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
# Historical integrity guard: later releases can move active_work and the current
# sprint without rewriting the Sprint 89/90/91 decisions.
assert state["current_sprint"] >= 91
version_parts = tuple(int(part) for part in state["state_version"].split("."))
assert version_parts >= (0, 21, 80)

# Older resume schemas carried a dedicated Annecy v0.4 candidate block. Compact
# later states may omit that duplicate because the immutable Sprint 89 summary,
# compatibility review and publication record retain the same evidence.
annecy_checkpoint = state.get("annecy_v0_4_research")
if annecy_checkpoint is not None:
    assert annecy_checkpoint["status"] == "historical_candidate_state_before_publication"
    assert annecy_checkpoint["based_on_public_version"] == "0.3"
    assert annecy_checkpoint["candidate_memory_count"] == 77
    assert annecy_checkpoint["candidate_without_aviation_memory_count"] == 60
    assert annecy_checkpoint["candidate_memory_delta"] == 1
    assert annecy_checkpoint["added_frequency_mhz"] == 50.5375
    assert annecy_checkpoint["added_memory_name"] == "ZTH-6M"
else:
    compatibility = json.loads((ROOT / "research/annecy-alpes-leman-v0.4/compatibility-and-source-review.json").read_text(encoding="utf-8"))
    assert compatibility["target_version"] == "0.4"
    assert compatibility["based_on_public_version"] == "0.3"
    assert compatibility["candidate_memory_count"] == 77
    assert compatibility["candidate_without_aviation_memory_count"] == 60
    assert compatibility["candidate_memory_delta"] == 1

# Sprint 89 was pre-publication. The current public pointer may legitimately be
# the later immutable v0.4 release, while the historical candidate evidence
# remains unchanged.
v04_record = ROOT / "research/annecy-alpes-leman-v0.4/publication-record.json"
current = state["public_packs"]["annecy_alpes_leman"]
assert current["version"] == "0.4"
assert current["memory_count"] == 77
assert current["without_aviation_memory_count"] == 60
assert current["immutable"] is True
assert current["previous_immutable_version"] == "0.3"
assert current["previous_memory_count"] == 76
assert current["previous_without_aviation_memory_count"] == 59
publication = json.loads(v04_record.read_text(encoding="utf-8"))
assert publication["status"] == "published_immutable"
assert publication["based_on_public_version"] == "0.3"

# Sprint 90 remains a historical pre-theory snapshot.
assert state["normandie_v0_5_latest_refresh"]["candidate_memory_count"] == 142
assert state["normandie_v0_5_latest_refresh"]["candidate_memory_delta"] == 0

bretagne = state["bretagne_v0_3_airac_handoff"]
assert bretagne["pack"] == "Bretagne"
assert bretagne["target_version"] == "0.3"
assert bretagne["candidate_memory_count"] == 151
assert bretagne["candidate_memory_delta"] == 0
assert bretagne["airac_next_effective_from"] == "2026-09-03"
assert bretagne["publication_allowed_before_airac09_revalidation"] is False

# Sprint 101 publication remains immutable even when a later IDF version becomes
# current. The state pointer may advance; the frozen Sprint 101 block and v0.3
# publication record are the historical source of truth.
if state["current_sprint"] >= 101:
    idf = state["public_packs"]["ile_de_france"]
    current_idf_version = tuple(int(part) for part in idf["version"].split("."))
    assert current_idf_version >= (0, 3)
    assert idf["immutable"] is True
    if current_idf_version == (0, 3):
        assert idf["memory_count"] == 57
        assert idf["previous_immutable_version"] == "0.2"
        assert idf["previous_memory_count"] == 58
        assert idf["public_csv_sha256"] == "e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125"
    elif idf.get("previous_immutable_version") == "0.3":
        assert idf["previous_memory_count"] == 57

    s101 = state["latest_sprint101_idf_v03_research"]
    assert s101["candidate_memory_count"] == 57
    assert s101["candidate_aviation_memory_count"] == 18
    assert s101["candidate_regional_radio_memory_count"] == 15
    assert s101["public_csv_sha256"] == "e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125"
    assert s101["published"] is True
    assert s101["published_version_is_immutable"] is True

    idf_v03_record = json.loads((ROOT / "research/ile-de-france-v0.3/publication-record.json").read_text(encoding="utf-8"))
    assert idf_v03_record["status"] == "published_immutable"
    assert idf_v03_record["memory_count"] == 57
    assert idf_v03_record["public_csv_sha256"] == "e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125"

# Current docs can focus on Sprint 113; historical Sprint 89/90/91 details remain
# frozen in their dedicated summaries rather than duplicated in every resume.
project = (ROOT / "PROJECT_STATUS.md").read_text(encoding="utf-8")
assert "Annecy–Alpes–Léman v0.4" in project
assert "77 mémoires RX" in project
assert "Normandie v0.5" in project
assert "Bretagne v0.3" in project

readme = (ROOT / "README.md").read_text(encoding="utf-8")
assert "**Annecy–Alpes–Léman v0.4** — 77 mémoires RX" in readme
assert "**Normandie v0.5**" in readme
assert "**Bretagne v0.3**" in readme
if state["current_sprint"] >= 113:
    assert "Sprint 113 / 0.22.01" in readme

s89 = (ROOT / "research/sprint-89-summary.md").read_text(encoding="utf-8")
s90 = (ROOT / "research/sprint-90-summary.md").read_text(encoding="utf-8")
s91 = (ROOT / "research/sprint-91-summary.md").read_text(encoding="utf-8")
assert "Sprint 89" in s89 and "77" in s89 and "60" in s89
assert "Sprint 90" in s90 and "142" in s90
assert "Sprint 91" in s91 and "3 septembre 2026" in s91

print("Sprints 89-91 integrity: historical checkpoints remain exact with compact Sprint 113 state and current immutable publications OK")
