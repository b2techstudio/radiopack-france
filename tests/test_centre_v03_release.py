import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/centre-val-de-loire-v0.3"

plan = json.loads((BASE / "pack-plan.json").read_text(encoding="utf-8"))
radio = json.loads((BASE / "radio-validation-2026-08-20.json").read_text(encoding="utf-8"))
aviation = json.loads((BASE / "aviation-airac08-2026-08-20.json").read_text(encoding="utf-8"))
scope = json.loads((BASE / "release-scope.json").read_text(encoding="utf-8"))
checklist = json.loads((BASE / "review-checklist.json").read_text(encoding="utf-8"))
gates = json.loads((BASE / "publication-gates.json").read_text(encoding="utf-8"))
record02 = json.loads((ROOT / "research/centre-val-de-loire-v0.2/publication-record.json").read_text(encoding="utf-8"))
registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
regions = json.loads((ROOT / "website/src/data/regions.json").read_text(encoding="utf-8"))
helper = (ROOT / "website/src/lib/centrePack.ts").read_text(encoding="utf-8")
route = ROOT / "website/src/pages/downloads/centre-val-de-loire/radiopack-france-centre-val-de-loire-v0.3.csv.ts"
region_page = (ROOT / "website/src/pages/regions/[slug].astro").read_text(encoding="utf-8")

assert record02["status"] == "published_immutable"
assert record02["version"] == "0.2"
assert record02["memory_count"] == 42
assert record02["public_csv_sha256"] == "68e164763834e69dcd85dd9b1b67777e42922134be33d5e25738f4df71f2bb29"
assert record02["published_version_is_immutable"] is True

assert plan["status"] in {"release_candidate_prepublication", "published_immutable"}
assert plan["target_version"] == "0.3"
assert plan["published_base_memory_count"] == 42
assert plan["published_base_is_immutable"] is True
assert plan["current_candidate_memory_count"] == 51
assert plan["current_net_memory_delta"] == 9
assert plan["rules"]["rx_only"] is True
assert plan["rules"]["source_conflict_blocks_promotion"] is True

assert radio["result"]["kept_station_count"] == 4
assert radio["result"]["new_station_count"] == 6
assert radio["result"]["analog_radio_memory_count"] == 20
assert {item["call"] for item in radio["promoted"]} == {"F5ZSQ", "F5ZXW", "F6ZAW", "F5ZUZ", "F5ZAP", "F1ZFY"}
assert {item["call"] for item in radio["not_carried_forward_from_v0_2"]} == {"F5ZQY", "F5ZNX"}

assert aviation["cycle"] == "AIRAC 08/26"
assert aviation["valid_through_inclusive"] == "2026-09-02"
assert aviation["changes_from_v0_2"]["aviation_memory_count_v0_3"] == 7
assert any(item["name"] == "CHR-TWR1" and item["frequency_mhz"] == 125.88 for item in aviation["memories"])
assert any(item["name"] == "SDH-AFIS" and item["frequency_mhz"] == 122.405 for item in aviation["memories"])

assert scope["status"] == "scope_closed"
assert scope["memory_count"] == 51
assert scope["net_memory_delta_vs_v0_2"] == 9
assert scope["historical_v0_2_immutable"] is True
assert scope["release_is_non_exhaustive"] is True
assert checklist["status"] == "completed"
assert checklist["reviewed_count"] == checklist["item_count"] == 10
assert gates["status"] in {"ready_for_publication", "published_zero_blockers"}
assert gates["blocker_count"] == 0
assert all(check["pass"] is True for check in gates["checks"])

assert 'centreV03MemoryCount = 51' in helper
assert 'name: "CHR-TWR1", frequency_mhz: 125.88' in helper
assert 'name: "SDH-AFIS", frequency_mhz: 122.405' in helper
assert '"F5ZHF", "F5ZDE", "F5ZVB", "F5ZLP"' in helper
assert route.is_file()
assert "buildCentreV03Pack" in route.read_text(encoding="utf-8")
assert '{ id: "centre-val-de-loire", name: "Centre-Val de Loire", memoryCount: 51, marine: false, aviation: 7, version: "v0.3" }' in registry
region = next(item for item in regions if item["slug"] == "centre-val-de-loire")
assert region["status"] == "v0.3 disponible"
assert region["memoryCount"] == 51
assert "buildCentreV03Pack" in region_page

record03 = BASE / "publication-record.json"
if record03.exists():
    publication = json.loads(record03.read_text(encoding="utf-8"))
    assert publication["status"] == "published_immutable"
    assert publication["version"] == "0.3"
    assert publication["memory_count"] == 51
    assert publication["previous_public_version"] == "0.2"
    assert publication["previous_public_memory_count"] == 42
    assert len(publication["public_csv_sha256"]) == 64
    assert publication["published_version_is_immutable"] is True

print("Centre-Val de Loire v0.3 release guard: 51 RX scope, stale/conflicting relays removed, aviation corrections and public metadata synchronized, OK")
