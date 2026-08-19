#!/usr/bin/env python3
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
state = json.loads((ROOT / "research/project-resume-state.json").read_text(encoding="utf-8"))
manifest = json.loads((ROOT / "research/sprint-98-metropolitan-publication-manifest.json").read_text(encoding="utf-8"))
readme = (ROOT / "README.md").read_text(encoding="utf-8")
project = (ROOT / "PROJECT_STATUS.md").read_text(encoding="utf-8")
changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
assert state["updated"] == "2026-08-19"
assert state["current_sprint"] == 98
assert state["state_version"] == "0.21.87"
assert "**État courant : Sprint 98 / 0.21.87" in readme
assert "## État actuel — Sprint 98 / 0.21.87" in readme
assert "Sprint courant : **98**" in project
assert "État logique : **0.21.87**" in project
assert changelog.startswith("# Changelog\n\n## 0.21.87 - 2026-08-19")
assert manifest["region_count"] == 11 and manifest["memory_count"] == 1135
assert manifest["all_rx_only"] is True
expected = {"hauts_de_france": 144, "ile_de_france": 58, "grand_est": 59, "centre_val_de_loire": 42, "pays_de_la_loire": 130, "bourgogne_franche_comte": 37, "nouvelle_aquitaine": 151, "auvergne_rhone_alpes": 62, "occitanie": 156, "provence_alpes_cote_d_azur": 159, "corse": 137}
for key, count in expected.items():
    p = state["public_packs"][key]
    assert p["version"] == "0.2" and p["memory_count"] == count and p["immutable"] is True
    assert p["previous_immutable_version"] == "0.1" and len(p["public_csv_sha256"]) == 64
for entry in manifest["entries"]:
    base = ROOT / "research" / f"{entry['id']}-v0.2"
    for name in ["release-scope.json", "review-checklist.json", "publication-gates.json", "publication-record.json"]:
        assert (base / name).is_file()
    review = json.loads((base / "review-checklist.json").read_text(encoding="utf-8"))
    gates = json.loads((base / "publication-gates.json").read_text(encoding="utf-8"))
    record = json.loads((base / "publication-record.json").read_text(encoding="utf-8"))
    assert review["completed"] == review["total"] == 10 and review["blocker_count"] == 0
    assert gates["public_release_allowed"] is True and gates["blocker_count"] == 0
    assert record["public_csv_sha256"] == entry["sha256"] and record["published_version_is_immutable"] is True
s98 = state["latest_sprint98_metropolitan_consolidation"]
assert s98["sprint"] == 98 and s98["state_version"] == "0.21.87" and s98["region_count"] == 11
assert s98["rf_data_mutation"] is False and s98["public_csv_mutation"] is False
assert state["recent_sprints"][0]["sprint"] == 98
assert "- name: Test Sprint 98 state synchronization" in ci
assert "python tools/check_metropolitan_v02_publication_records.py --dist website/dist" in ci
print("Sprint 98 state sync: 11 metropolitan v0.2 records, hashes, scopes, reviews and official state 98 / 0.21.87 OK")
