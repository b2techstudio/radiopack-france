#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FULL_SHA = "2557076fcb198b830cd3b5ba64d7ff894c8e0d6e90eafc0fa40b691a3c6a5d98"
NO_AIR_SHA = "e31bfc6fce402af117b4f79caf6547b60a23c91ef36491e1351c74e96329aa6c"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    scope = json.loads((ROOT / "research/annecy-alpes-leman-v0.4/release-scope.json").read_text(encoding="utf-8"))
    review = json.loads((ROOT / "research/annecy-alpes-leman-v0.4/review-checklist.json").read_text(encoding="utf-8"))
    sources = json.loads((ROOT / "research/annecy-alpes-leman-v0.4/current-source-revalidation.json").read_text(encoding="utf-8"))
    assert scope["prepublication_ready"] is True and scope["publication_blocker_count"] == 0
    assert scope["public_export_allowed"] is False and scope["public_registry_allowed"] is False
    assert review["completed"] == review["total"] == 12 and review["blocker_count"] == 0
    assert all(item["passed"] is True for item in review["items"])
    assert sources["approved_new_rf_mhz"] == [50.5375]
    assert sources["device_compatibility"]["stock_chirp_driver"]["modified_firmware_required"] is False
    assert sources["policy_checks"]["unpublished_adrasec_frequency_inferred"] is False

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp)
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools/build_annecy_v04_release_candidate.py"), "--output-dir", str(out)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        assert "77 / 60 RX" in proc.stdout
        full = out / "radiopack-france-annecy-alpes-leman-v0.4.csv"
        no_air = out / "radiopack-france-annecy-alpes-leman-v0.4-sans-aviation.csv"
        assert sha(full) == FULL_SHA
        assert sha(no_air) == NO_AIR_SHA
        full_rows = rows(full)
        no_air_rows = rows(no_air)
        assert len(full_rows) == 77 and len(no_air_rows) == 60
        for variant in (full_rows, no_air_rows):
            assert sum(row["Name"] == "ZTH-6M" and row["Frequency"] == "50.537500" for row in variant) == 1
            assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in variant)
            assert len({row["Frequency"] for row in variant}) == len(variant)
            assert len({row["Name"] for row in variant}) == len(variant)
        manifest = json.loads((out / "release-candidate-manifest.json").read_text(encoding="utf-8"))
        memory_map = json.loads((out / "prepublication-reviewed-memory-map.json").read_text(encoding="utf-8"))
        assert manifest["status"] == "release_candidate_built_not_public"
        assert manifest["publication_blocker_count"] == 0
        assert manifest["files"]["full"]["sha256"] == FULL_SHA
        assert manifest["files"]["without_aviation"]["sha256"] == NO_AIR_SHA
        assert memory_map["status"] == "reviewed_prepublication_not_public"
        assert len(memory_map["rows"]) == 77

    public_dir = ROOT / "website/public/downloads/annecy-alpes-leman"
    assert not (public_dir / "radiopack-france-annecy-alpes-leman-v0.4.csv").exists()
    assert not (public_dir / "radiopack-france-annecy-alpes-leman-v0.4-sans-aviation.csv").exists()
    print("Sprint 94 Annecy v0.4 prepublication: 77/60 RX, deterministic SHAs, blockers=0, public=false")


if __name__ == "__main__":
    main()
