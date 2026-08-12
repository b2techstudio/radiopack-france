from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one occurrence, found {count}: {old!r}")
    return text.replace(old, new, 1)


# Current public region metadata must match the published registry.
regions_path = ROOT / "website/src/data/regions.json"
regions = json.loads(regions_path.read_text(encoding="utf-8"))
bretagne = next(item for item in regions if item["slug"] == "bretagne")
bretagne["status"] = "v0.2 disponible"
bretagne["description"] = "Pack de 151 mémoires RX : socle Bretagne v0.1 complété par 16 mémoires aviation AIRAC 08/26, toujours en réception seule."
bretagne["memoryCount"] = 151
bretagne["categories"] = [
    "PMR446 RX",
    "VHF marine RX",
    "Radioamateur RX",
    "Aviation RX",
    "Ch64 / Ch79 RX",
]
regions_path.write_text(json.dumps(regions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Historical site test now checks the current Bretagne release while retaining v0.1 archive existence.
test_path = ROOT / "tests/test_site_files.py"
test = test_path.read_text(encoding="utf-8")
test = replace_once(
    test,
    'assert next(region for region in regions if region["slug"] == "bretagne")["memoryCount"] == 135',
    'assert next(region for region in regions if region["slug"] == "bretagne")["memoryCount"] == 151',
    "Bretagne regions memory count",
)
test = replace_once(test, "    'memoryCount: 135',", "    'memoryCount: 151',", "registry current Bretagne memory count")
test = replace_once(test, "assert 'version: \"v0.1\"' in registry", "assert 'version: \"v0.2\"' in registry", "registry current Bretagne version")
test = replace_once(
    test,
    'assert (ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.1.csv").is_file()',
    'assert (ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.1.csv").is_file()\nassert (ROOT / "website/public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv").is_file()',
    "Bretagne historical and current public CSVs",
)
test_path.write_text(test, encoding="utf-8")

# Complete local synchronization commands in README.
readme_path = ROOT / "README.md"
readme = readme_path.read_text(encoding="utf-8")
old = "python tools\\run_bretagne_v02_prepublication_audit.py --require-prepublication-ready\npython tests\\test_sprint79_bretagne_v02_maturity.py\npython tests\\test_site_files.py"
new = "python tools\\run_bretagne_v02_prepublication_audit.py --require-prepublication-ready\npython tests\\test_sprint79_bretagne_v02_maturity.py\npython tests\\test_bretagne_v02_public_release.py\npython tests\\test_sprint80_bretagne_v02_publication.py\npython tests\\test_site_files.py"
readme = replace_once(readme, old, new, "README local Sprint 80 commands")
readme_path.write_text(readme, encoding="utf-8")

print("Sprint 80 post-publication metadata and compatibility fixes applied")
