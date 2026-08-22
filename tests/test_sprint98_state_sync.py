#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
state = json.loads((ROOT / "research/project-resume-state.json").read_text(encoding="utf-8"))
manifest = json.loads((ROOT / "research/sprint-98-metropolitan-publication-manifest.json").read_text(encoding="utf-8"))
ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")

# Sprint 98 is historical: later official states and v0.3+ publications must
# not invalidate its frozen v0.2 evidence or force those v0.2 versions to stay
# current forever.
assert state["current_sprint"] >= 100
version_parts = tuple(int(part) for part in state["state_version"].split("."))
assert version_parts >= (0, 21, 89)
assert manifest["region_count"] == 11
assert manifest["memory_count"] == 1135
assert manifest["all_rx_only"] is True

historical = {
    "hauts-de-france": ("hauts_de_france", 144),
    "ile-de-france": ("ile_de_france", 58),
    "grand-est": ("grand_est", 59),
    "centre-val-de-loire": ("centre_val_de_loire", 42),
    "pays-de-la-loire": ("pays_de_la_loire", 130),
    "bourgogne-franche-comte": ("bourgogne_franche_comte", 37),
    "nouvelle-aquitaine": ("nouvelle_aquitaine", 151),
    "auvergne-rhone-alpes": ("auvergne_rhone_alpes", 62),
    "occitanie": ("occitanie", 156),
    "provence-alpes-cote-d-azur": ("provence_alpes_cote_d_azur", 159),
    "corse": ("corse", 137),
}

entries = {entry["id"]: entry for entry in manifest["entries"]}
assert set(entries) == set(historical)
for slug, (state_key, count) in historical.items():
    entry = entries[slug]
    assert entry["memory_count"] == count
    base = ROOT / "research" / f"{slug}-v0.2"
    for name in ["release-scope.json", "review-checklist.json", "publication-gates.json", "publication-record.json"]:
        assert (base / name).is_file(), f"Sprint 98 artifact missing: {slug}/{name}"
    review = json.loads((base / "review-checklist.json").read_text(encoding="utf-8"))
    gates = json.loads((base / "publication-gates.json").read_text(encoding="utf-8"))
    record = json.loads((base / "publication-record.json").read_text(encoding="utf-8"))
    assert review["completed"] == review["total"] == 10 and review["blocker_count"] == 0
    assert gates["public_release_allowed"] is True and gates["blocker_count"] == 0
    assert record["public_csv_sha256"] == entry["sha256"]
    assert record["published_version_is_immutable"] is True

    # The current public pack may legitimately have advanced past v0.2. The
    # Sprint 98 invariant is that the frozen v0.2 record remains immutable and
    # that no current state regresses below it. When v0.2 is the immediate
    # predecessor, its historical count must still be carried exactly.
    current = state["public_packs"][state_key]
    current_version = tuple(int(part) for part in current["version"].split("."))
    assert current_version >= (0, 2)
    assert current["immutable"] is True
    if current["version"] == "0.2":
        assert current["memory_count"] == count
    elif current.get("previous_immutable_version") == "0.2":
        assert current["previous_memory_count"] == count

s98 = state["latest_sprint98_metropolitan_consolidation"]
assert s98["sprint"] == 98
assert s98["state_version"] == "0.21.87"
assert s98["region_count"] == 11
assert s98["rf_data_mutation"] is False and s98["public_csv_mutation"] is False
assert any(item.get("sprint") == 98 for item in state["recent_sprints"])
assert (ROOT / "research/sprint-98-summary.md").is_file()
assert "- name: Test Sprint 98 state synchronization" in ci
assert "python tools/check_metropolitan_v02_publication_records.py --dist website/dist" in ci

print("Sprint 98 historical integrity: eleven immutable v0.2 records retained across later official releases OK")
