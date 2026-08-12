import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
state = json.loads((ROOT / "research/project-resume-state.json").read_text(encoding="utf-8"))
record = json.loads((ROOT / "research/bretagne-v0.2/publication-record.json").read_text(encoding="utf-8"))
gates = json.loads((ROOT / "research/bretagne-v0.2/publication-gates.json").read_text(encoding="utf-8"))
assert state["current_sprint"] == 80
assert state["state_version"] == "0.21.69"
assert state["public_packs"]["bretagne"]["version"] == "0.2"
assert state["public_packs"]["bretagne"]["memory_count"] == 151
assert state["public_packs"]["bretagne"]["immutable"] is True
assert record["status"] == "published_immutable" and record["version"] == "0.2" and record["memory_count"] == 151
assert record["new_memory_count_vs_v0_1"] == 16
assert record["aviation"]["cycle"] == "AIRAC 08/26"
assert record["aviation"]["freshness_rechecked_on"] == "2026-08-12"
assert record["aviation"]["direct_xml_field_match_claimed"] is False
assert gates["status"] == "published_immutable_151"
assert next(g for g in gates["gates"] if g["id"] == "explicit_publication")["status"] == "passed_publication_completed_immutable"
assert (ROOT / record["public_csv"]).is_file()
assert (ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.1.csv").is_file()
print("Sprint 80: Bretagne v0.2 published immutable at 151 RX memories with AIRAC 08/26 boundary preserved OK")
