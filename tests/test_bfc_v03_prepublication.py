import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "research/bourgogne-franche-comte-v0.3"

scope = json.loads((BASE / "release-scope.json").read_text(encoding="utf-8"))
checklist = json.loads((BASE / "review-checklist.json").read_text(encoding="utf-8"))
gates = json.loads((BASE / "publication-gates.json").read_text(encoding="utf-8"))
candidate = json.loads((BASE / "internal-candidate-v0.3.json").read_text(encoding="utf-8"))
record03 = json.loads((BASE / "publication-record.json").read_text(encoding="utf-8"))
record02 = json.loads((ROOT / "research/bourgogne-franche-comte-v0.2/publication-record.json").read_text(encoding="utf-8"))
record04 = json.loads((ROOT / "research/bourgogne-franche-comte-v0.4/publication-record.json").read_text(encoding="utf-8"))
registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
regions = json.loads((ROOT / "website/src/data/regions.json").read_text(encoding="utf-8"))
route03 = ROOT / "website/src/pages/downloads/bourgogne-franche-comte/radiopack-france-bourgogne-franche-comte-v0.3.csv.ts"
route04 = ROOT / "website/src/pages/downloads/bourgogne-franche-comte/radiopack-france-bourgogne-franche-comte-v0.4.csv.ts"
builder = ROOT / "website/src/lib/bfcPack.ts"
region_page = ROOT / "website/src/pages/regions/[slug].astro"

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

assert gates["status"] == "published_zero_blockers"
assert gates["blocker_count"] == 0
assert all(item["pass"] is True for item in gates["checks"])

expected_sha = "b5af25a6766b1181e735d376d3f70ab47ffb9ed67b9e38e35bee15e8a86ae7a5"
assert record03["status"] == "published_immutable"
assert record03["version"] == "0.3"
assert record03["memory_count"] == 54
assert record03["previous_public_version"] == "0.2"
assert record03["previous_public_memory_count"] == 37
assert record03["public_csv_sha256"] == expected_sha
assert record03["published_version_is_immutable"] is True
assert record03["publication_sprint"] == 99
assert record03["state_version"] == "0.21.88"

assert candidate["status"] == "published_immutable"
assert candidate["memory_count"] == 54
assert candidate["new_memory_count"] == 17
assert candidate["public_export_allowed"] is True
assert candidate["public_registry_allowed"] is True
assert candidate["public_csv_sha256"] == expected_sha
new_rows = candidate["new_rx_memories"]
assert len(new_rows) == 17
assert len([row for row in new_rows if row["mode"] == "FM"]) == 10
assert len([row for row in new_rows if row["mode"] == "AM"]) == 7
assert all(row["duplex"] == "off" and row["offset"] == "0.000000" for row in new_rows)
assert len({row["name"] for row in new_rows}) == 17
assert len({round(float(row["frequency_mhz"]), 6) for row in new_rows}) == 17
assert any(row["name"] == "CHAL-INFO" and float(row["frequency_mhz"]) == 118.605 for row in new_rows)

assert route03.is_file() and route04.is_file() and builder.is_file()
route03_text = route03.read_text(encoding="utf-8")
builder_text = builder.read_text(encoding="utf-8")
region_page_text = region_page.read_text(encoding="utf-8")
assert "buildBfcV03Pack" in route03_text
assert "buildBfcV03Pack" in region_page_text and "buildBfcV04Pack" in region_page_text
assert 'buildMetropolitanPack("bourgogne-franche-comte", "v0.2")' in builder_text
assert 'name: "CHAL-INFO"' in builder_text
assert 'frequency_mhz: 118.605' in builder_text
assert 'bfcV03MemoryCount = 54' in builder_text
assert 'bfcV04MemoryCount = 61' in builder_text

# v0.3 remains an immutable historical publication even though v0.4 is now current.
assert record04["status"] == "published_immutable"
assert record04["previous_public_version"] == "0.3"
assert record04["previous_public_memory_count"] == 54
assert record04["previous_public_sha256"] == expected_sha
assert '{ id: "bourgogne-franche-comte", name: "Bourgogne-Franche-Comté", memoryCount: 61, marine: false, aviation: 14, version: "v0.4" }' in registry
region = next(item for item in regions if item["slug"] == "bourgogne-franche-comte")
assert region["status"] == "v0.4 disponible"
assert region["memoryCount"] == 61
assert region["available"] is True
assert "VHF navigation intérieure RX" in region["categories"]

print("BFC v0.3 historical guard: 54 RX immutable release and hash preserved after v0.4 promotion, OK")
