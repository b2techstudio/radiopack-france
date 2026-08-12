import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
state = json.loads((ROOT / "research/project-resume-state.json").read_text(encoding="utf-8"))
record = json.loads((ROOT / "research/bretagne-v0.1/publication-record.json").read_text(encoding="utf-8"))
scope = json.loads((ROOT / "research/bretagne-v0.1/release-scope.json").read_text(encoding="utf-8"))
plan = json.loads((ROOT / "research/bretagne-v0.1/pack-plan.json").read_text(encoding="utf-8"))
gates = json.loads((ROOT / "research/bretagne-v0.1/publication-gates.json").read_text(encoding="utf-8"))
assert state["current_sprint"] >= 73 and state["state_version"] >= "0.21.62"
assert state["public_packs"]["bretagne"]["version"] in {"0.1", "0.2"}
assert state["public_packs"]["bretagne"]["memory_count"] in {135, 151}
assert state["public_packs"]["bretagne"]["immutable"] is True
assert state["public_packs"]["normandie"]["version"] == "0.4" and state["public_packs"]["normandie"]["memory_count"] == 142
assert state["public_packs"]["annecy_alpes_leman"]["version"] == "0.2" and state["public_packs"]["annecy_alpes_leman"]["memory_count"] == 65
assert record["status"] == "published_immutable" and record["memory_count"] == 135
assert record["version"] == "0.1" and record["published_version_is_immutable"] is True
assert scope["status"] == "scope_frozen_135_prepublication_not_public" and scope["sprint"] == 72
assert plan["status"] == "prepublication_ready_135_not_public" and plan["publication"]["explicit_publication_required"] is True
assert gates["status"] == "published_immutable_135"
assert next(g for g in gates["gates"] if g["id"] == "explicit_publication")["status"] == "passed_publication_completed_immutable"
assert scope["included"]["channel64_pair_mhz"] == [156.225,160.825]
assert scope["included"]["channel79_pair_mhz"] == [156.975,161.575]
assert {x["id"] for x in scope["deferred_to_v0_2"]} == {"AVIATION_CURRENT_SIA","ADRASEC_UNPUBLISHED_OPERATIONAL_FREQUENCIES","CROSS_LOCAL_TRANSMITTER_SITE_MAPPING","STOPPED_OR_UNRESOLVED_AMATEUR_INFRASTRUCTURE"}
assert (ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.1.csv").is_file()
if state["current_sprint"] >= 80:
    assert state["public_packs"]["bretagne"]["version"] == "0.2"
    assert state["public_packs"]["bretagne"]["memory_count"] == 151
print("Sprint 73: Bretagne v0.1 historical publication remains immutable and auditable after later Bretagne releases OK")
