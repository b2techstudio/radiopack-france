#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "website/public/downloads/annecy-alpes-leman"
FULL = PUBLIC / "radiopack-france-annecy-alpes-leman-v0.4.csv"
NO_AIR = PUBLIC / "radiopack-france-annecy-alpes-leman-v0.4-sans-aviation.csv"
V03_FULL = PUBLIC / "radiopack-france-annecy-alpes-leman-v0.3.csv"
V03_NO_AIR = PUBLIC / "radiopack-france-annecy-alpes-leman-v0.3-sans-aviation.csv"
FULL_SHA = "2557076fcb198b830cd3b5ba64d7ff894c8e0d6e90eafc0fa40b691a3c6a5d98"
NO_AIR_SHA = "e31bfc6fce402af117b4f79caf6547b60a23c91ef36491e1351c74e96329aa6c"
V03_FULL_SHA = "fa4095c0af9b4fa5758449e09c9a32eb5c7cc103e0d90b7c9da8e74c77796af7"
V03_NO_AIR_SHA = "e639aff0d045e5a20db3b03fb6175b68452700b4b6ee2e1edf78e9510c2eb649"
REVIEW_MAP_SHA = "3b115b6d54361d7c4cfc31459ac689119ef5fc6d2fb683cb604c57378ea50dab"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_variant(path: Path, expected_count: int, expected_sha: str) -> list[dict[str, str]]:
    assert path.exists(), path
    assert sha(path) == expected_sha
    data = rows(path)
    assert len(data) == expected_count
    assert len({row["Frequency"] for row in data}) == expected_count
    assert len({row["Name"] for row in data}) == expected_count
    assert all(row["Duplex"] == "off" and row["Offset"] == "0.000000" for row in data)
    zth = [row for row in data if row["Name"] == "ZTH-6M"]
    assert len(zth) == 1
    assert zth[0]["Frequency"] == "50.537500"
    assert zth[0]["Mode"] == "FM"
    assert zth[0]["TStep"] == "12.50"
    return data


def main() -> None:
    full_rows = validate_variant(FULL, 77, FULL_SHA)
    no_air_rows = validate_variant(NO_AIR, 60, NO_AIR_SHA)
    assert [row for row in full_rows if row["Name"] == "ZTH-6M"][0]["Location"] == "161"
    assert [row for row in no_air_rows if row["Name"] == "ZTH-6M"][0]["Location"] == "94"

    assert sha(V03_FULL) == V03_FULL_SHA
    assert sha(V03_NO_AIR) == V03_NO_AIR_SHA

    record = json.loads((ROOT / "research/annecy-alpes-leman-v0.4/publication-record.json").read_text(encoding="utf-8"))
    assert record["status"] == "published_immutable"
    assert record["version"] == "0.4"
    assert record["based_on_public_version"] == "0.3"
    assert record["full_memory_count"] == 77
    assert record["without_aviation_memory_count"] == 60
    assert record["new_unique_rf_memory_count"] == 1
    assert record["public_files"]["full"]["sha256"] == FULL_SHA
    assert record["public_files"]["without_aviation"]["sha256"] == NO_AIR_SHA
    assert record["review_map"]["sha256"] == REVIEW_MAP_SHA
    assert record["rules"]["immutable"] is True
    assert record["rules"]["rx_only"] is True
    assert record["rules"]["published_v0_3_remains_immutable"] is True
    assert record["rules"]["unpublished_adrasec_frequency_inferred"] is False
    assert record["rules"]["modified_firmware_required"] is False

    review_map = ROOT / record["review_map"]["path"]
    assert sha(review_map) == REVIEW_MAP_SHA
    mapped = json.loads(review_map.read_text(encoding="utf-8"))
    assert mapped["expected_memory_count"] == 77
    assert mapped["expected_memory_count_without_aviation"] == 60
    assert len(mapped["rows"]) == 77

    registry = (ROOT / "website/src/lib/packRegistry.ts").read_text(encoding="utf-8")
    assert 'version: "v0.4"' in registry
    assert 'memoryCount: 77' in registry
    assert 'memoryCount: 60' in registry
    assert 'radiopack-france-annecy-alpes-leman-v0.4.csv' in registry
    assert 'radiopack-france-annecy-alpes-leman-v0.4-sans-aviation.csv' in registry

    regions = json.loads((ROOT / "website/src/data/regions.json").read_text(encoding="utf-8"))
    annecy = next(item for item in regions if item["slug"] == "annecy-haute-savoie")
    assert annecy["status"] == "v0.4 disponible"
    assert annecy["memoryCount"] == 77

    page = (ROOT / "website/src/pages/regions/annecy-haute-savoie.astro").read_text(encoding="utf-8")
    assert "Annecy–Alpes–Léman v0.4" in page
    assert "77 mémoires avec aviation · 60 sans aviation" in page
    assert "50.5375 MHz est ajouté en v0.4" in page

    print("Annecy v0.4 public release: 77/60 RX, immutable SHAs, v0.3 preserved")


if __name__ == "__main__":
    main()
