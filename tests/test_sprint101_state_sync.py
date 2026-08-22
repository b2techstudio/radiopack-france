#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
state = json.loads((ROOT / "research/project-resume-state.json").read_text(encoding="utf-8"))
record = json.loads((ROOT / "research/ile-de-france-v0.3/publication-record.json").read_text(encoding="utf-8"))
scope = json.loads((ROOT / "research/ile-de-france-v0.3/release-scope.json").read_text(encoding="utf-8"))
manifest = json.loads((ROOT / "research/ile-de-france-v0.3/generated/release-candidate/candidate-manifest.json").read_text(encoding="utf-8"))
checklist = json.loads((ROOT / "research/ile-de-france-v0.3/review-checklist.json").read_text(encoding="utf-8"))
gates = json.loads((ROOT / "research/ile-de-france-v0.3/publication-gates.json").read_text(encoding="utf-8"))
public_csv = ROOT / "website/public/downloads/ile-de-france/radiopack-france-ile-de-france-v0.3.csv"

EXPECTED_SHA = "e04e6dbbf869661305068bac55cd8044abdcea7321d67e4c28111c9d057da125"

# Sprint 101 is historical: later official sprints may become current without
# changing any immutable Île-de-France v0.3 publication fact.
assert state["current_sprint"] >= 101
version_parts = tuple(int(part) for part in state["state_version"].split("."))
assert version_parts >= (0, 21, 90)

idf = state["public_packs"]["ile_de_france"]
assert idf["version"] == "0.3"
assert idf["memory_count"] == 57
assert idf["immutable"] is True
assert idf["previous_immutable_version"] == "0.2"
assert idf["previous_memory_count"] == 58
assert idf["publication_record"] == "research/ile-de-france-v0.3/publication-record.json"
assert idf["public_csv_sha256"] == EXPECTED_SHA

s101 = state["latest_sprint101_idf_v03_research"]
assert s101["sprint"] == 101
assert s101["state_version"] == "0.21.90"
assert s101["completed_on"] == "2026-08-22"
assert s101["status"] == "ile_de_france_v03_published_immutable"
assert s101["candidate_memory_count"] == 57
assert s101["candidate_aviation_memory_count"] == 18
assert s101["candidate_regional_radio_memory_count"] == 15
assert s101["candidate_sha256"] == EXPECTED_SHA
assert s101["public_csv_sha256"] == EXPECTED_SHA
assert s101["publication_ready"] is True
assert s101["published"] is True
assert s101["published_version_is_immutable"] is True
assert s101["public_mutation_performed"] is True

assert record["status"] == "published_immutable"
assert record["memory_count"] == 57
assert record["candidate_csv_sha256"] == EXPECTED_SHA
assert record["public_csv_sha256"] == EXPECTED_SHA
assert record["published"] is True
assert record["public_csv_created"] is True
assert record["public_registry_updated"] is True
assert record["published_version_is_immutable"] is True
assert public_csv.is_file()

assert scope["status"] == "published_immutable"
assert scope["publication_ready"] is True
assert scope["published"] is True
assert scope["published_version_is_immutable"] is True
assert manifest["candidate_memory_count"] == 57
assert manifest["candidate_sha256"] == EXPECTED_SHA
assert manifest["public_csv_sha256"] == EXPECTED_SHA
assert manifest["published"] is True
assert checklist["reviewed_count"] == checklist["item_count"] == 12
assert checklist["published"] is True
assert gates["blocker_count"] == 0
assert all(item["pass"] for item in gates["checks"])
assert gates["published"] is True

recent101 = next(item for item in state["recent_sprints"] if item.get("sprint") == 101)
assert "published immutable at 57 RX / 18 aviation" in recent101["summary"]

print("Sprint 101 historical integrity: IDF v0.3 immutable 57/18/15 and exact public SHA retained across later sprints OK")
