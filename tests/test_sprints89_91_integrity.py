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
# Historical integrity guard: later releases may advance the current public pack
# and active work, but the Sprint 89 research decision plus the Normandie and
# Bretagne gates must remain represented without being rewritten as current work.
assert state["current_sprint"] >= 91
version_parts = tuple(int(part) for part in state["state_version"].split("."))
assert version_parts >= (0, 21, 80)
assert state["annecy_v0_4_research"]["candidate_memory_count"] == 77
assert state["annecy_v0_4_research"]["candidate_without_aviation_memory_count"] == 60
assert state["annecy_v0_4_research"]["published"] is False

v04_record = ROOT / "research/annecy-alpes-leman-v0.4/publication-record.json"
if v04_record.exists():
    current = state["public_packs"]["annecy_alpes_leman"]
    assert current["version"] == "0.4"
    assert current["memory_count"] == 77
    assert current["without_aviation_memory_count"] == 60
    assert current["previous_immutable_version"] == "0.3"
    assert current["previous_memory_count"] == 76
    assert current["previous_without_aviation_memory_count"] == 59
    publication = json.loads(v04_record.read_text(encoding="utf-8"))
    assert publication["status"] == "published_immutable"
    assert publication["based_on_public_version"] == "0.3"
else:
    assert state["public_packs"]["annecy_alpes_leman"]["version"] == "0.3"
    assert state["public_packs"]["annecy_alpes_leman"]["memory_count"] == 76

assert state["normandie_v0_5_latest_refresh"]["candidate_memory_count"] == 142
assert state["normandie_v0_5_latest_refresh"]["candidate_memory_delta"] == 0

bretagne = state.get("bretagne_v0_3_airac_handoff", state.get("active_work", {}))
assert bretagne["pack"] == "Bretagne"
assert bretagne["target_version"] == "0.3"
assert bretagne["candidate_memory_count"] == 151
assert bretagne["candidate_memory_delta"] == 0
assert bretagne["airac_next_effective_from"] == "2026-09-03"
assert bretagne["publication_allowed_before_airac09_revalidation"] is False

# Starting with Sprint 101, active_work can move on while the Sprint 91 handoff
# remains a historical/future gate in its dedicated machine-readable block.
# A later pack may legitimately reach prepublication readiness. If so, this
# historical guard must ensure that readiness has NOT silently mutated the
# currently published pack rather than forcing publication_ready to stay false.
if state["current_sprint"] >= 101:
    active = state["active_work"]
    assert active["pack"] == "Île-de-France"
    assert active["target_version"] == "0.3"
    if active["publication_ready"]:
        assert active["release_candidate_memory_count"] == 57
        assert active["publication_record_frozen"] is True
        assert active["candidate_sha256"] == "e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125"
        idf_public = state["public_packs"]["ile_de_france"]
        assert idf_public["version"] == "0.2"
        assert idf_public["memory_count"] == 58
        assert idf_public["immutable"] is True
        assert idf_public["public_csv_sha256"] == "dbcadbcef403d7272dc374a7010def7276b06048a8e863277fcdb3558a8f624d"

project = (ROOT / "PROJECT_STATUS.md").read_text(encoding="utf-8")
assert f'Sprint courant : **{state["current_sprint"]}**' in project
assert f'État logique : **{state["state_version"]}**' in project
if v04_record.exists():
    assert "Annecy–Alpes–Léman v0.4 : **77 mémoires RX**" in project
    assert "Annecy–Alpes–Léman v0.3 : **76 / 59**, historique immuable." in project
else:
    assert "Annecy–Alpes–Léman v0.3 : **76 mémoires RX**" in project
assert "Annecy–Alpes–Léman v0.2 : 65 mémoires RX, variante 48 sans aviation." not in project
assert "## Sprint 91 —" in project
assert "## Sprint 90 —" in project
assert "## Sprint 89 —" in project

readme = (ROOT / "README.md").read_text(encoding="utf-8")
assert f'Sprint {state["current_sprint"]} / {state["state_version"]}' in readme
if v04_record.exists():
    assert "Annecy–Alpes–Léman v0.4" in readme
    assert "77 RX / 60 sans aviation" in readme
else:
    assert "Annecy v0.4 = 77 RX / 60 sans aviation" in readme
assert "Normandie v0.5 reste à **142 RX**" in readme
assert "Bretagne v0.3 reste à **151 RX**" in readme
assert "## Sprint 91 —" in readme
assert "## Sprint 90 —" in readme
assert "## Sprint 89 —" in readme

print("Sprints 89-91 integrity: historical decisions preserved across later state/release advances; future and field gates preserved OK")
