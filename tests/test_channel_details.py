from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEBSITE = ROOT / "website"

BRETAGNE_CSV = WEBSITE / "public/downloads/bretagne/radiopack-france-bretagne-v0.2.csv"
REGIONAL_PAGES = {
    "bretagne": WEBSITE / "src/pages/regions/bretagne.astro",
    "normandie": WEBSITE / "src/pages/regions/normandie.astro",
    "annecy": WEBSITE / "src/pages/regions/annecy-haute-savoie.astro",
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_bretagne_aviation_groups_match_public_csv() -> None:
    rows = read_rows(BRETAGNE_CSV)
    assert len(rows) == 151

    by_prefix = {
        "RNS-": [row for row in rows if row["Name"].startswith("RNS-")],
        "BES-": [row for row in rows if row["Name"].startswith("BES-")],
        "DIN-": [row for row in rows if row["Name"].startswith("DIN-")],
        "QUIM-": [row for row in rows if row["Name"].startswith("QUIM-")],
    }

    assert len(by_prefix["RNS-"]) == 7
    assert len(by_prefix["BES-"]) == 5
    assert len(by_prefix["DIN-"]) == 2
    assert len(by_prefix["QUIM-"]) == 1
    assert len([row for row in rows if row["Name"] == "AIR-EMERG"]) == 1

    assert [row["Frequency"] for row in by_prefix["BES-"]] == [
        "119.575000",
        "135.830000",
        "125.860000",
        "120.105000",
        "129.355000",
    ]


def test_all_regional_pages_use_csv_backed_channel_details() -> None:
    for name, page in REGIONAL_PAGES.items():
        source = page.read_text(encoding="utf-8")
        assert "ChannelGroupDetails" in source, name
        assert "loadPublicPackMemories" in source, name
        assert "Tous les canaux du pack" in source, name

    bretagne = REGIONAL_PAGES["bretagne"].read_text(encoding="utf-8")
    assert "buildBretagneChannelGroups" in bretagne
    assert "Clique sur Rennes, Brest, Dinard, Quimper" in bretagne


def test_channel_detail_component_is_collapsible_and_complete() -> None:
    component = (WEBSITE / "src/components/ChannelGroupDetails.astro").read_text(encoding="utf-8")
    helper = (WEBSITE / "src/lib/channelDetails.ts").read_text(encoding="utf-8")

    assert '<details class="channel-group"' in component
    assert "group.memories.length" in component
    assert "Fréquence" in component
    assert "Mode" in component
    assert "memory.comment" in component

    assert "readFileSync" in helper
    assert "../../public/" in helper
    assert "buildStandardChannelGroups" in helper
    assert "buildBretagneChannelGroups" in helper


if __name__ == "__main__":
    test_bretagne_aviation_groups_match_public_csv()
    test_all_regional_pages_use_csv_backed_channel_details()
    test_channel_detail_component_is_collapsible_and_complete()
    print("Regional channel details: OK")
