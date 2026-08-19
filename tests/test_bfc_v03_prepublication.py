import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/bourgogne-franche-comte-v0.3"

scope = json.loads((BASE / "release-scope.json").read_text(encoding="utf-8"))
checklist = json.loads((BASE / "review-checklist.json").read_text(encoding="utf-8"))
gates = json.loads((BASE / "publication-gates.json").read_text(encoding="utf-8"))
candidate = json.loads((BASE / "internal-candidate-v0.3.json").read_text(encoding="utf-8"))
record02 = json.loads((ROOT / "research/bourgogne-franche-comte-v0.2/publication-record.json").read_text(encoding="utf-8"))
registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
regions = json.loads((ROOT / "website/src/data/regions.json").read_text(encoding="utf-8"))
route = ROOT / "website/src/pages/downloads/bourgogne-franche-comte/radiopack-france-bourgogne-franche-comte-v0.3.csv.ts"

assert record02["version"] == "0.2"
assert record02["memory_count"] == 37
assert record02["public_csv_sha256"] == "828af205aa07fe6685e3ad395ec2f0f56222fcfb5bb2f7b8f6a0bd4082714c0a"
assert record02["published_version_is_immutable"] is True

assert scope["status"] == "scope_closed"
assert scope["version"] == "0.3"
assert scope["memory_count"] == 54
assert scope["new_memory_count"] == 17
assert scope["radioamateur_new_memory_count"] == 10
assert scope["aviation_new_memory_count"] == 7
assert scope["aviation_total_memory_count"] == 14
assert scope["airac_cycle"] == "AIRAC 08/26"
assert scope["historical_v0_2_immutable"] is True
assert scope["release_is_non_exhaustive"] is True
assert scope["rx_only"] is True
assert set(scope["deferred"]["radioamateur_calls"]) == {"F5ZNS", "F5ZFE", "F5ZKM", "F5ZMS", "F5ZTJ"}
assert scope["deferred"]["aviation"] == ["LFLM 119.005 MHz"]

assert checklist["status"] == "completed"
assert checklist["item_count"] == 10
assert checklist["reviewed_count"] == 10
assert all(item["reviewed"] is True for item in checklist["items"])

assert gates["status"] == "ready_for_publication"
assert gates["blocker_count"] == 0
assert all(item["pass"] is True for item in gates["checks"])

assert candidate["status"] == "release_candidate_prepublication"
assert candidate["memory_count"] == 54
assert candidate["new_memory_count"] == 17
new_rows = candidate["new_rx_memories"]
assert len(new_rows) == 17
assert len([row for row in new_rows if row["mode"] == "FM"]) == 10
assert len([row for row in new_rows if row["mode"] == "AM"]) == 7
assert all(row["duplex"] == "off" and row["offset"] == "0.000000" for row in new_rows)
assert len({row["name"] for row in new_rows}) == 17
assert len({round(float(row["frequency_mhz"]), 6) for row in new_rows}) == 17
assert any(row["name"] == "CHAL-INFO" and float(row["frequency_mhz"]) == 118.605 for row in new_rows)

assert route.is_file()
route_text = route.read_text(encoding="utf-8")
assert 'buildMetropolitanPack("bourgogne-franche-comte", "v0.2")' in route_text
assert 'name: "CHAL-INFO"' in route_text
assert 'frequency_mhz: 118.605' in route_text

assert '{ id: "bourgogne-franche-comte", name: "Bourgogne-Franche-Comté", memoryCount: 54, marine: false, aviation: 14, version: "v0.3" }' in registry
region = next(item for item in regions if item["slug"] == "bourgogne-franche-comte")
assert region["status"] == "v0.3 disponible"
assert region["memoryCount"] == 54
assert region["available"] is True

print("BFC v0.3 prepublication: scope/checklist/gates complete, 54 RX release candidate, website endpoint and metadata synchronized, OK")
