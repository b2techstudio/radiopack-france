import csv
import importlib.util
import io
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools/build_normandie_v04_internal_candidate.py"
MAP_PATH = ROOT / "research/normandie-v0.4/internal-candidate-map.json"
BASE_PATH = ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.3.1.csv"

spec = importlib.util.spec_from_file_location("normandie_v04_builder", TOOL_PATH)
builder = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(builder)

config = json.loads(MAP_PATH.read_text(encoding="utf-8"))
assert config["schema_version"] == "1.0"
assert config["status"] == "internal_candidate_map_not_public"
assert config["base"]["version"] == "0.3.1"
assert config["base"]["memory_count"] == 139
assert config["base"]["immutable"] is True
assert config["candidate"]["memory_count"] == 142
assert config["candidate"]["new_memory_count"] == 3
assert config["candidate"]["positions_are_internal_provisional"] is True
assert config["candidate"]["public_export_allowed"] is False

expected = [
    (175, "50-ZHY-IN", 145.0875),
    (176, "53-ZCE-IN", 145.1000),
    (177, "50-ZBL-U", 431.2500),
]
assert [(item["location"], item["name"], item["frequency_mhz"]) for item in config["additions"]] == expected
assert all(len(item["name"]) <= 10 for item in config["additions"])
assert config["rules"]["chirp_duplex"] == "off"
assert config["rules"]["chirp_offset"] == "0.000000"
assert config["rules"]["tx_disabled"] is True
assert config["rules"]["public_export_allowed"] is False

base_bytes_before = BASE_PATH.read_bytes()
base_rows = list(csv.DictReader(io.StringIO(base_bytes_before.decode("utf-8"))))
assert len(base_rows) == 139

with tempfile.TemporaryDirectory(prefix="radiopack-normandie-v04-") as tmp:
    output_dir = Path(tmp)
    json_path, csv_path, manifest = builder.write_candidate(ROOT, output_dir)
    assert json_path.is_file()
    assert csv_path.is_file()
    candidate_bytes = csv_path.read_bytes()
    assert candidate_bytes.startswith(base_bytes_before)
    assert BASE_PATH.read_bytes() == base_bytes_before

    rows = list(csv.DictReader(io.StringIO(candidate_bytes.decode("utf-8"))))
    assert len(rows) == 142
    assert manifest["memory_count"] == 142
    assert manifest["new_memory_count"] == 3
    assert manifest["base_memory_count"] == 139
    assert manifest["published_base_is_exact_prefix"] is True
    assert manifest["public_export_allowed"] is False
    assert manifest["rules"]["published_base_rows_rewritten"] is False
    assert manifest["rules"]["tx_disabled"] is True
    assert manifest["rules"]["final_public_memory_plan_defined"] is False

    added = rows[-3:]
    assert [(int(row["Location"]), row["Name"], float(row["Frequency"])) for row in added] == expected
    for row in added:
        assert row["Duplex"] == "off"
        assert row["Offset"] == "0.000000"
        assert row["Tone"] == ""
        assert row["Mode"] == "NFM"
        assert row["TStep"] == "12.50"
        assert len(row["Name"]) <= 10

    locations = [int(row["Location"]) for row in rows]
    names = [row["Name"] for row in rows]
    frequencies = [round(float(row["Frequency"]), 6) for row in rows]
    assert len(locations) == len(set(locations))
    assert len(names) == len(set(names))
    assert len(frequencies) == len(set(frequencies))

registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
assert 'version: "v0.4"' not in registry
assert not (ROOT / "website/public/downloads/normandie/radiopack-france-normandie-v0.4.csv").exists()

print("Tests Normandie v0.4 internal candidate: frozen 139-row v0.3.1 is exact prefix + locations 175-177 for ZHY-IN/ZCE-IN/ZBL-U = 142 RX-only memories, generated outside public tree, no public mutation OK")
